#!/usr/bin/env python3
"""Preview the site in another serif without touching the real pages.

    python3 tools/build-type-preview.py

Copies the homepage, the MetaMask case study and the About page into
explorations/type/<font>/ with the headline serif swapped from Instrument
Serif to Noto Serif Display, Condensed (75% width) Light (300). The mono font,
the drawings and everything else stay the same. Re-run after page changes.
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FONT_SLUG = "noto-serif-display"
FONT_NAME = "Noto Serif Display, Condensed Light"
OUT = ROOT / "explorations" / "type" / FONT_SLUG
PAGES = [("home", "index.html", "/"), ("metamask", "metamask/index.html", "/metamask/"), ("about", "about/index.html", "/about/")]

OLD_FAMILY = "family=Instrument+Serif:ital@0;1&amp;"
NEW_FAMILY = "family=Noto+Serif+Display:ital,wdth,wght@0,62.5..100,100..900;1,62.5..100,100..900&amp;"

OVERRIDE = """
  <meta name="robots" content="noindex">
  <style>
    /* Type preview: Noto Serif Display, Condensed (75%) Light (300) in place of Instrument Serif */
    :root{--serif:"Noto Serif Display",Georgia,serif}
    .page{font-stretch:75%;font-weight:300}
    .page :is(h1,h2,h3,em){font-weight:300}
    .type-badge{position:fixed;left:16px;bottom:16px;z-index:50;display:flex;flex-wrap:wrap;gap:6px 14px;align-items:center;
      font:13px var(--mono);font-stretch:100%;background:#1C1C1C;color:#ECECEA;border-radius:999px;padding:8px 14px;box-shadow:0 6px 20px rgba(0,0,0,.18)}
    .type-badge a{color:#ECECEA}
    .type-badge a:hover{color:#fff}
    @media (max-width:600px){ .type-badge{right:12px;left:12px;bottom:12px;border-radius:16px;font-size:12px} }
  </style>
</head>"""


def badge(here, real):
    links = " · ".join(
        f'<a href="/explorations/type/{FONT_SLUG}/{slug}/">{slug}</a>' if slug != here else f"<strong>{slug}</strong>" for slug, _, _ in PAGES
    )
    return (
        f'\n<nav class="type-badge" aria-label="Type preview"><span>Preview: {FONT_NAME}</span>'
        f"<span>{links}</span><a href=\"{real}\">see it in Instrument Serif →</a></nav>\n"
    )


for slug, src, real in PAGES:
    html = (ROOT / src).read_text()
    assert OLD_FAMILY in html, f"{src}: font link not found"
    html = html.replace(OLD_FAMILY, NEW_FAMILY, 1)
    # Relative image paths keep pointing at the real page's folder.
    html = re.sub(r"(<meta charset=\"utf-8\">)", rf'\1\n  <base href="{real}">', html, count=1)
    html = html.replace("</head>", OVERRIDE, 1)
    html = html.replace("</body>", badge(slug, real) + "</body>", 1)
    out = OUT / slug / "index.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(html)
    print(f"wrote {out.relative_to(ROOT)}")
