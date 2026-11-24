#!/usr/bin/env python3
"""Build the case-study pages in the new design.

    python3 tools/build-projects.py --extract   # read content from the v1 pages into tools/projects.json
    python3 tools/build-projects.py             # render each <slug>/index.html from tools/projects.json

The content (title, summary, hero media, overview, role details, tags and
highlight images) comes from the pages as they were live at tag v1-live, so
nothing is rewritten. Sections that were hidden on the live site are left out.
After extracting once, edit tools/projects.json (or the generated pages) and
re-render.
"""
import html
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "tools" / "projects.json"
REF = "v1-live"

# Order, number and short label match the "selected work" cards on the homepage.
PROJECTS = [
    ("apple", "01", "Internal Tools"),
    ("origin-labs", "02", "Hardware · Fleet App"),
    ("metamask", "03", "Mobile · Web3"),
    ("portal", "04", "Wallet · Brand"),
    ("intuition-systems", "05", "Web · Knowledge Graph"),
    ("mobina", "06", "Motion · AI Assistant"),
]


def one(pattern, text, flags=0, default=""):
    m = re.search(pattern, text, flags)
    return m.group(1).strip() if m else default


def visible(text):
    """Drop the sections that the live pages hid with display: none."""
    return re.sub(r'<div class="project-section" style="display: none;">[\s\S]*?\n          </div>\n', "", text)


def extract():
    out = []
    for slug, num, label in PROJECTS:
        page = subprocess.run(["git", "show", f"{REF}:{slug}/index.html"], cwd=ROOT, check=True, capture_output=True, text=True).stdout
        page = visible(page)
        hero = one(r'<div class="project-hero-img-wrap[^"]*">([\s\S]*?)</div>\s*</div>\s*</div>\s*</section>', page)
        kind = "video" if "<video" in hero else "logo" if "logo" in hero else "image"
        overview = one(r'<div class="project-overview-text">([\s\S]*?)</div>\s*<div class="project-role-details">', page)
        details = one(r'<div class="project-role-details">([\s\S]*?)</div>\s*</div>\s*</div>', page)
        facts = [
            {"label": m.group(1).strip(), "value": m.group(2).strip()}
            for m in re.finditer(r'<span class="project-role-label">([\s\S]*?)</span>\s*<span class="project-role-value">([\s\S]*?)</span>\s*</div>', details)
        ]
        tags = re.findall(r'<span class="tag">([\s\S]*?)</span>', one(r'<div class="project-role-item project-role-tags">([\s\S]*?)</div>', page))
        shots = []
        block = one(r'<section class="project-highlights">([\s\S]*?)</section>', page)
        starts = list(re.finditer(r'<div class="project-highlight( project-highlight--dark)? reveal">', block))
        for i, m in enumerate(starts):
            chunk = block[m.end(): starts[i + 1].start() if i + 1 < len(starts) else len(block)]
            media = re.findall(r"<img\b[^>]*>|<video\b[\s\S]*?</video>", chunk)
            shots.append({"alt_bg": bool(m.group(1)), "pair": "project-highlight-pair" in chunk, "media": media})
        nav_tag = one(rf'<a href="\.\./{slug}/" class="project-nav-card[^"]*">[\s\S]*?<span class="tag">([\s\S]*?)</span>', page)
        out.append({
            "slug": slug, "num": num, "label": label,
            "title": html.unescape(one(r"<h1[^>]*>([\s\S]*?)</h1>", page)),
            "page_title": html.unescape(one(r"<title>([\s\S]*?)</title>", page)),
            "description": html.unescape(one(r'<meta name="description" content="([^"]*)"', page)),
            "summary": one(r'<p class="project-desc[^"]*">([\s\S]*?)</p>', page),
            "hero": {"kind": kind, "html": hero},
            "overview": re.findall(r'<p class="about-bio">([\s\S]*?)</p>', overview),
            "facts": facts, "tags": tags, "shots": shots, "nav_tag": nav_tag,
        })
    DATA.write_text(json.dumps(out, indent=2, ensure_ascii=False) + "\n")
    print(f"extracted {len(out)} projects from {REF} into {DATA.relative_to(ROOT)}")


def clean_media(tag):
    """Strip the old site's animation and layout classes from an <img>/<video>."""
    tag = re.sub(r'\sclass="[^"]*"', "", tag, count=1)
    tag = re.sub(r'\sstyle="[^"]*"', "", tag)
    if tag.startswith("<img") and "loading=" not in tag:
        tag = tag.replace("<img", '<img loading="lazy" decoding="async"', 1)
    return tag


HEAD = """<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <title>{page_title}</title>
  <meta name="description" content="{description}">
  <meta name="theme-color" content="#ECECEA">
  <link rel="canonical" href="https://christianjeria.work/{slug}/">
  <meta property="og:title" content="{page_title}">
  <meta property="og:description" content="{description}">
  <meta property="og:image" content="https://christianjeria.work/og-image.png">
  <meta property="og:url" content="https://christianjeria.work/{slug}/">
  <meta property="og:type" content="article">
  <meta name="twitter:card" content="summary_large_image">
  <link rel="icon" type="image/png" sizes="32x32" href="/favicon-32x32.png">
  <link rel="icon" type="image/png" sizes="16x16" href="/favicon-16x16.png">
  <link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon.png">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Instrument+Serif:ital@0;1&amp;family=IBM+Plex+Mono:wght@400;500&amp;display=swap" rel="stylesheet">
  <link rel="stylesheet" href="/site.css">
  <script defer src="/_vercel/insights/script.js"></script>
</head>
<body>
<div class="page">
  <div class="wrap">

    <header class="site-head">
      <div class="pillbar">
        <a class="wordmark" href="/">Christian <em>Jeria</em></a>
        <nav class="site-nav" aria-label="Primary">
          <a href="/#work">Work</a>
          <a href="/#built">Built</a>
          <a href="/about/">About</a>
        </nav>
        <a class="pill-contact" href="/contact/">Contact</a>
      </div>
    </header>
"""

FOOT = """
    <footer class="site-foot">
      <p>100% <em>Human.</em></p>
      <a class="cta" href="/contact/">Get in Touch →</a>
    </footer>

  </div>
</div>
</body>
</html>
"""


def render(p, projects):
    hero = p["hero"]
    media = hero["html"].strip()
    if hero["kind"] == "video":
        media = re.sub(r'\sclass="[^"]*"', "", media, count=1)
    else:
        media = "\n".join(clean_media(t) for t in re.findall(r"<img\b[^>]*>", media))
        media = media.replace(' loading="lazy"', "")  # the hero loads straight away
    facts = "\n".join(
        f'          <div class="case-fact"><dt>{f["label"]}</dt><dd>{f["value"]}</dd></div>' for f in p["facts"]
    )
    tags = "".join(f'<span class="tag">{t}</span>' for t in p["tags"])
    overview = "\n".join(f"          <p>{para}</p>" for para in p["overview"])
    # Highlights sit straight in the body container; only a pair gets a row to sit side by side.
    shots = []
    for sh in p["shots"]:
        shot = "".join(clean_media(m) for m in sh["media"])
        shots.append(f'        <div class="case-pair">{shot}</div>' if sh["pair"] else f"        {shot}")
    gallery = ('\n    <section class="case-body" aria-label="Highlights">\n      <div class="case-gallery">\n' + "\n".join(shots) + "\n      </div>\n    </section>\n") if shots else ""
    rows = []
    for o in projects:
        here = o["slug"] == p["slug"]
        current = ' aria-current="page"' if here else ""
        rows.append(
            f'      <a class="built-row{" is-current" if here else ""}" href="/{o["slug"]}/"{current}>'
            f'<span class="built-name">{o["title"]}</span>'
            f'<span class="built-desc">{o["nav_tag"] or o["label"]} →</span></a>'
        )
    more = "\n".join(rows)
    body = f"""
    <main>
    <section class="hero case-hero">
      <div class="case-meta"><a href="/#work">← Selected Work</a><span>{p["label"]}</span></div>
      <div class="hero-top">
        <h1>{p["title"]}</h1>
        <p class="hero-lede">{p["summary"]}</p>
      </div>
      <figure class="case-media case-media-{hero["kind"]}">
        {media}
      </figure>
    </section>

    <section class="case-overview" aria-labelledby="overview-h">
      <div class="case-text">
        <h2 id="overview-h" class="case-label">Overview</h2>
{overview}
      </div>
      <dl class="case-facts">
{facts}
          <div class="case-fact case-tags"><dt>Focus</dt><dd>{tags}</dd></div>
      </dl>
    </section>
{gallery}    <section class="built case-more" aria-labelledby="more-h">
      <div class="sec-head">
        <h2 id="more-h">More <em>Work</em></h2>
      </div>
{more}
    </section>
    </main>
"""
    head = HEAD.format(
        page_title=html.escape(p["page_title"]), description=html.escape(p["description"]), slug=p["slug"]
    )
    return head + body + FOOT


def build():
    projects = json.loads(DATA.read_text())
    for p in projects:
        out = ROOT / p["slug"] / "index.html"
        out.write_text(render(p, projects))
        print(f"wrote {out.relative_to(ROOT)}: {len(p['overview'])} paragraphs, {len(p['shots'])} highlights, hero {p['hero']['kind']}")


if __name__ == "__main__":
    if "--extract" in sys.argv:
        extract()
    else:
        build()
