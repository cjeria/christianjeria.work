#!/usr/bin/env python3
"""Freeze a past version of the site into its own folder, e.g. /v1/.

    python3 tools/snapshot-version.py v1 v1-live

Copies every committed file at the given git ref (a tag, branch or commit)
into ./<name>/, then rewrites root-relative links so the archived pages keep
pointing at each other: "/contact/" becomes "/v1/contact/". Vercel's analytics
path (/_vercel/...) is left alone. Each archived page gets a noindex tag so
search engines don't treat it as a copy of the live site.

The snapshot leaves out earlier version folders (v1/, v2/ ...), tools/ and
site-wide config (vercel.json and friends), so archives never nest. Git stores
identical files once, so the copied images and video add almost nothing to the
repository; only the rewritten text files are new.
"""
import io
import re
import subprocess
import sys
import tarfile
from pathlib import Path

TEXT = {".html", ".htm", ".css", ".js", ".mjs", ".json", ".webmanifest", ".svg", ".xml", ".txt"}
SKIP_TOP = {"tools", "vercel.json", ".vercelignore", ".gitignore", "package.json", "package-lock.json"}
VERSION_DIR = re.compile(r"^v\d+$")


def rewrite(text: str, suffix: str, prefix: str) -> str:
    keep = r"(?![/_])"  # not protocol-relative (//host) and not /_vercel/
    # HTML attributes: href="/x", src="/x", poster, action, content, data-*.
    text = re.sub(rf'(\s(?:href|src|poster|action|content|data-[\w-]+)\s*=\s*["\'])/{keep}', rf"\1{prefix}/", text)
    # srcset="/a.png 1x, /b.png 2x"
    text = re.sub(
        r'(\ssrcset\s*=\s*")([^"]*)"',
        lambda m: m.group(1) + re.sub(rf"(^|,\s*)/{keep}", rf"\1{prefix}/", m.group(2)) + '"',
        text,
    )
    # CSS url(/x), in stylesheets and inline styles.
    text = re.sub(rf"(url\(\s*['\"]?)/{keep}", rf"\1{prefix}/", text)
    # JavaScript string literals that start with a root path: '/work/'.
    if suffix in {".js", ".mjs", ".html", ".htm"}:
        def js(block: str) -> str:
            return re.sub(rf"(['\"`])/{keep}(?=[A-Za-z0-9])", rf"\1{prefix}/", block)

        if suffix in {".js", ".mjs"}:
            text = js(text)
        else:
            text = re.sub(r"(<script\b[^>]*>)([\s\S]*?)(</script>)", lambda m: m.group(1) + js(m.group(2)) + m.group(3), text)
    if suffix in {".html", ".htm"} and 'name="robots"' not in text:
        text = re.sub(r"(<head[^>]*>)", r'\1\n    <meta name="robots" content="noindex" />', text, count=1)
    return text


def main() -> None:
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    name, ref = sys.argv[1], sys.argv[2]
    if not VERSION_DIR.match(name):
        sys.exit("Version folder should look like v1, v2 ...")
    out = Path(name)
    if out.exists():
        sys.exit(f"{out}/ already exists; remove it first to re-snapshot.")
    prefix = f"/{name}"
    data = subprocess.run(["git", "archive", "--format=tar", ref], check=True, capture_output=True).stdout
    files = rewritten = 0
    with tarfile.open(fileobj=io.BytesIO(data)) as tar:
        for member in tar.getmembers():
            if not member.isfile():
                continue
            top = member.name.split("/", 1)[0]
            if top in SKIP_TOP or VERSION_DIR.match(top):
                continue
            body = tar.extractfile(member).read()
            dest = out / member.name
            dest.parent.mkdir(parents=True, exist_ok=True)
            suffix = dest.suffix.lower()
            if suffix in TEXT:
                text = body.decode("utf-8")
                new = rewrite(text, suffix, prefix)
                if new != text:
                    rewritten += 1
                body = new.encode("utf-8")
            dest.write_bytes(body)
            files += 1
    print(f"{ref} -> {out}/: {files} files, {rewritten} with links rewritten")


if __name__ == "__main__":
    main()
