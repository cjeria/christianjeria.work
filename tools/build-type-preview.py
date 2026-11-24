#!/usr/bin/env python3
"""Preview the site in another serif without touching the real pages.

    python3 tools/build-type-preview.py

For each typeface below, copies the homepage, the MetaMask case study and the
About page into explorations/type/<slug>/ with the headline serif swapped for
Instrument Serif. The mono font, the drawings and everything else stay the
same. Re-run after page changes.

PP Editorial New is licensed for personal use only (no public websites, no
uploading the files), so its previews load the fonts from the local folder and
both are kept out of git and deploys (.gitignore, .vercelignore). They only
work when the site is served locally.
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PAGES = [("home", "index.html", "/"), ("metamask", "metamask/index.html", "/metamask/"), ("about", "about/index.html", "/about/")]
INSTRUMENT = "family=Instrument+Serif:ital@0;1&amp;"
PP_DIR = "/PPEditorialNew-Free%20for%20personal%20use"


def pp_faces():
    faces = [("Ultralight", 200, "normal"), ("UltralightItalic", 200, "italic"), ("Regular", 400, "normal"),
             ("Italic", 400, "italic"), ("Ultrabold", 800, "normal"), ("UltraboldItalic", 800, "italic")]
    return "\n".join(
        f'    @font-face{{font-family:"PP Editorial New";src:url("{PP_DIR}/PPEditorialNew-{f}.otf") format("opentype");font-weight:{w};font-style:{s};font-display:swap}}'
        for f, w, s in faces
    )


TYPEFACES = [
    {
        "slug": "noto-serif-display",
        "name": "Noto Serif Display, Condensed Light",
        "family_link": "family=Noto+Serif+Display:ital,wdth,wght@0,62.5..100,100..900;1,62.5..100,100..900&amp;",
        "css": """    :root{--serif:"Noto Serif Display",Georgia,serif}
    .page{font-stretch:75%;font-weight:300}
    .page :is(h1,h2,h3,em){font-weight:300}""",
    },
    {
        "slug": "pp-editorial-new",
        "name": "PP Editorial New, Regular (local preview only)",
        "family_link": "",
        "css": pp_faces() + """
    :root{--serif:"PP Editorial New",Georgia,serif}
    .page :is(h1,h2,h3,em){font-weight:400}""",
    },
    {
        "slug": "pp-editorial-new-ultralight",
        "name": "PP Editorial New, Ultralight (local preview only)",
        "family_link": "",
        "css": pp_faces() + """
    :root{--serif:"PP Editorial New",Georgia,serif}
    .page{font-weight:200}
    .page :is(h1,h2,h3,em){font-weight:200}""",
    },
]

BADGE_CSS = """    .type-badge{position:fixed;left:16px;bottom:16px;z-index:50;display:flex;flex-wrap:wrap;gap:6px 14px;align-items:center;
      font:400 13px var(--mono);font-stretch:100%;background:#1C1C1C;color:#ECECEA;border-radius:999px;padding:8px 14px;box-shadow:0 6px 20px rgba(0,0,0,.18)}
    .type-badge a{color:#ECECEA}
    .type-badge a:hover{color:#fff}
    @media (max-width:600px){ .type-badge{right:12px;left:12px;bottom:12px;border-radius:16px;font-size:12px} }"""


def badge(face, here, real):
    pages = " · ".join(
        f'<a href="/explorations/type/{face["slug"]}/{slug}/">{slug}</a>' if slug != here else f"<strong>{slug}</strong>"
        for slug, _, _ in PAGES
    )
    faces = " · ".join(
        f'<a href="/explorations/type/{f["slug"]}/{here}/">{f["slug"]}</a>' if f is not face else f"<strong>{f['slug']}</strong>"
        for f in TYPEFACES
    )
    return (
        f'\n<nav class="type-badge" aria-label="Type preview"><span>Preview: {face["name"]}</span>'
        f"<span>{pages}</span><span>{faces}</span><a href=\"{real}\">Instrument Serif →</a></nav>\n"
    )


for face in TYPEFACES:
    out_dir = ROOT / "explorations" / "type" / face["slug"]
    for slug, src, real in PAGES:
        html = (ROOT / src).read_text()
        assert INSTRUMENT in html, f"{src}: font link not found"
        html = html.replace(INSTRUMENT, face["family_link"], 1)
        # Relative image paths keep pointing at the real page's folder.
        html = re.sub(r'(<meta charset="utf-8">)', rf'\1\n  <base href="{real}">', html, count=1)
        style = f'\n  <meta name="robots" content="noindex">\n  <style>\n    /* Type preview: {face["name"]} in place of Instrument Serif */\n{face["css"]}\n{BADGE_CSS}\n  </style>\n</head>'
        html = html.replace("</head>", style, 1)
        html = html.replace("</body>", badge(face, slug, real) + "</body>", 1)
        out = out_dir / slug / "index.html"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(html)
    print(f"wrote explorations/type/{face['slug']}/ ({len(PAGES)} pages)")
