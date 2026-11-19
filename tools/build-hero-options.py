#!/usr/bin/env python3
"""Build side-by-side options for the homepage nav and hero.

    python3 tools/build-hero-options.py

Reads the live homepage (index.html) and writes explorations/hero/option-N/
pages that keep everything identical (the product drawing and its hover
interactions, the work section, the footer, the scripts) except the nav and
the text around the drawing. explorations/hero/index.html shows them all
next to the current homepage. Re-run after changing the homepage so every
option picks up the change.
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "explorations" / "hero"
src = (ROOT / "index.html").read_text()

head, rest = src.split('<div class="page">', 1)
header = re.search(r'\s*<header class="site-head">[\s\S]*?</header>\n', rest).group(0)
hero = re.search(r'\s*<section class="hero">[\s\S]*?</section>\n', rest).group(0)
timeline = re.search(r'<svg class="timeline"[\s\S]*?</svg>', hero).group(0)
before_header, after_header = rest.split(header, 1)
_, after_hero = after_header.split(hero, 1)  # keeps "<main>" placement intact
between = after_header.split(hero, 1)[0]  # "\n    <main>"

NAV = """<a href="#work">work</a>
        <a href="#built">built</a>
        <a href="/about/">about</a>"""
WORDMARK = '<a class="wordmark" href="/">christian <em>jeria</em></a>'
LEDE = "Specializing in UI/UX, web design, branding and motion."
PREVIOUSLY = '<p class="previously">previously <em>at</em> <span class="tag">Apple</span> <em>and</em> <span class="tag">MetaMask</span></p>'

OPTIONS = [
    {
        "slug": "option-1",
        "name": "Centered masthead",
        "why": "Name and nav centered like a magazine masthead; the headline sits centered over the drawing, so the page reads as one symmetrical poster.",
        "header": f"""
    <header class="site-head">
      {WORDMARK}
      <nav class="site-nav" aria-label="Primary">
        {NAV}
        <a class="contact" href="/contact/">[contact]</a>
      </nav>
    </header>
""",
        "hero": f"""
    <section class="hero">
      <div class="hero-top">
        <h1>Freelance product <em>designer</em></h1>
        <p class="hero-lede">{LEDE}</p>
      </div>
      {timeline}
      {PREVIOUSLY}
    </section>
""",
        "css": """
.site-head{flex-direction:column;justify-content:center;gap:12px;padding:24px 8px 12px}
.wordmark{font-size:38px}
.site-nav{gap:10px 0}
.site-nav a + a::before{content:"/";margin:0 14px;color:var(--rule)}
.hero-top{flex-direction:column;align-items:center;text-align:center;gap:16px}
.hero h1{flex:none}
.hero-lede{flex:none;max-width:44ch}
""",
    },
    {
        "slug": "option-2",
        "name": "Name as the headline",
        "why": "A slim utility bar for the nav, your name set very large as the hero, and role, focus and background in a three-column row. The drawing sits straight on the page with no panel around it.",
        "header": f"""
    <header class="site-head o-bar">
      <p class="o-status"><span class="status-dot" aria-hidden="true"></span>open to work · seattle, wa</p>
      <nav class="site-nav" aria-label="Primary">
        {NAV}
        <a class="contact" href="/contact/">[contact]</a>
      </nav>
    </header>
""",
        "hero": f"""
    <section class="o-hero">
      <h1 class="o-name">Christian <em>Jeria</em></h1>
      <div class="o-facts">
        <p><span>[role]</span>Freelance product designer</p>
        <p><span>[focus]</span>{LEDE}</p>
        <p><span>[before]</span>Previously at Apple and MetaMask</p>
      </div>
      {timeline}
    </section>
""",
        "css": """
.o-bar{padding:10px 8px 12px;border-bottom:1px solid var(--ink)}
.o-status{display:flex;align-items:center;gap:10px;margin:0;font-family:var(--mono);font-size:13px;color:var(--muted)}
.status-dot{width:8px;height:8px;border-radius:50%;background:#2E9E5B;box-shadow:0 0 0 4px rgba(46,158,91,.15)}
.o-hero{display:flex;flex-direction:column;gap:28px;padding:28px 8px 0}
.o-name{margin:0;font-weight:400;font-size:clamp(72px,12.5vw,200px);line-height:.86;letter-spacing:-.035em}
.o-facts{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:20px 32px;border-top:1px solid var(--rule);padding-top:16px}
.o-facts p{margin:0;font-family:var(--mono);font-size:14px;line-height:1.6}
.o-facts span{display:block;color:var(--muted);margin-bottom:4px}
@media (max-width:760px){ .o-facts{grid-template-columns:minmax(0,1fr)} }
""",
    },
    {
        "slug": "option-3",
        "name": "Index grid",
        "why": "The nav becomes a Swiss-style index strip (name, role, place and status, links) between two rules. The headline gets two big lines, and the focus has its own labeled column.",
        "header": f"""
    <header class="site-head o-index">
      {WORDMARK}
      <p>Freelance product designer</p>
      <p><span class="status-dot" aria-hidden="true"></span>Seattle, WA · open to work</p>
      <nav class="site-nav" aria-label="Primary">
        {NAV}
        <a class="contact" href="/contact/">[contact]</a>
      </nav>
    </header>
""",
        "hero": f"""
    <section class="hero">
      <div class="o-top">
        <h1>Freelance product<br><em>designer</em></h1>
        <div class="o-focus">
          <p class="o-label">[specializing in]</p>
          <p class="o-list">UI/UX, web design, branding and motion</p>
        </div>
      </div>
      {timeline}
      {PREVIOUSLY}
    </section>
""",
        "css": """
.o-index{display:grid;grid-template-columns:1.2fr 1fr 1fr auto;align-items:center;gap:12px 24px;padding:14px 8px;border-top:1px solid var(--ink);border-bottom:1px solid var(--ink)}
.o-index p{margin:0;font-family:var(--mono);font-size:13px;color:var(--muted);display:flex;align-items:center;gap:8px}
.status-dot{width:8px;height:8px;border-radius:50%;background:#2E9E5B;box-shadow:0 0 0 4px rgba(46,158,91,.15)}
.o-top{display:grid;grid-template-columns:minmax(0,2.2fr) minmax(220px,1fr);align-items:end;gap:24px 48px}
.o-top h1{margin:0;font-weight:400;font-size:clamp(52px,7.4vw,112px);line-height:.94;letter-spacing:-.025em}
.o-focus{border-top:1px solid var(--ink);padding-top:12px}
.o-label{margin:0 0 6px;font-family:var(--mono);font-size:13px;color:var(--muted)}
.o-list{margin:0;font-size:30px;line-height:1.1}
@media (max-width:900px){
  .o-index{grid-template-columns:minmax(0,1fr)}
  .o-index p{display:none}
  .o-index .site-nav{gap:20px}
  .o-top{grid-template-columns:minmax(0,1fr)}
}
""",
    },
    {
        "slug": "option-4",
        "name": "Title block",
        "why": "Drawing first. The headline is set into the empty sky at the top of the drawing, and an architect-style title block in the corner holds the details, leaning into the drawn-in-line idea.",
        "header": f"""
    <header class="site-head">
      {WORDMARK}
      <nav class="site-nav o-pill" aria-label="Primary">
        {NAV}
        <a class="contact" href="/contact/">[contact]</a>
      </nav>
    </header>
""",
        "hero": f"""
    <section class="hero o-sheet">
      <div class="o-overlay">
        <h1>Freelance product <em>designer</em></h1>
        <p class="hero-lede">{LEDE}</p>
      </div>
      {timeline}
      <dl class="o-titleblock">
        <div><dt>designer</dt><dd>Christian Jeria</dd></div>
        <div><dt>previously</dt><dd>Apple, MetaMask</dd></div>
        <div><dt>based in</dt><dd>Seattle, WA</dd></div>
        <div><dt>status</dt><dd><span class="status-dot" aria-hidden="true"></span>open to work</dd></div>
      </dl>
    </section>
""",
        "css": """
.o-pill{border:1px solid var(--line);background:var(--panel);border-radius:999px;padding:10px 22px}
.timeline > g:first-of-type{display:none}
.o-sheet{position:relative;padding-top:32px}
.o-overlay{position:absolute;top:48px;left:48px;right:48px;display:flex;flex-wrap:wrap;justify-content:space-between;align-items:flex-end;gap:12px 32px;pointer-events:none}
.o-overlay h1{margin:0;font-weight:400;font-size:clamp(40px,5.2vw,80px);line-height:1;letter-spacing:-.02em}
.o-overlay .hero-lede{flex:0 1 320px}
.o-titleblock{align-self:flex-end;margin:0;display:grid;grid-template-columns:repeat(4,auto);border:1px solid var(--ink);font-family:var(--mono);font-size:12.5px}
.o-titleblock div{padding:8px 14px;border-left:1px solid var(--ink)}
.o-titleblock div:first-child{border-left:0}
.o-titleblock dt{color:var(--muted);text-transform:uppercase;letter-spacing:.06em;font-size:10.5px}
.o-titleblock dd{margin:2px 0 0;display:flex;align-items:center;gap:6px}
.status-dot{width:7px;height:7px;border-radius:50%;background:#2E9E5B}
@media (max-width:900px){
  .o-overlay{position:static;padding:0 0 8px}
  .o-titleblock{grid-template-columns:repeat(2,auto);align-self:stretch}
  .o-titleblock div:nth-child(3){border-left:0}
  .o-titleblock div:nth-child(n+3){border-top:1px solid var(--ink)}
}
""",
    },
    {
        "slug": "option-5",
        "name": "Pill nav with calls to action",
        "why": "A floating pill nav that stays put as you scroll, with a solid contact button. The hero splits into a three-line headline and a right column with the focus, availability and two clear next steps.",
        "header": f"""
    <header class="site-head o-float">
      <div class="o-pillbar">
        {WORDMARK}
        <nav class="site-nav" aria-label="Primary">
          {NAV}
        </nav>
        <a class="o-solid" href="/contact/">contact</a>
      </div>
    </header>
""",
        "hero": f"""
    <section class="o-split">
      <h1>Freelance<br>product <em>designer</em></h1>
      <div class="o-side">
        <p class="o-lede">{LEDE}</p>
        <p class="o-status"><span class="status-dot" aria-hidden="true"></span>open to work · previously at Apple and MetaMask</p>
        <div class="o-ctas">
          <a class="o-btn o-btn-ink" href="#work">[see the work ↓]</a>
          <a class="cta" href="/contact/">[get in touch →]</a>
        </div>
      </div>
    </section>
    <section class="hero o-drawing">
      {timeline}
    </section>
""",
        "css": """
.o-float{position:sticky;top:12px;z-index:20;justify-content:center;padding:4px 0}
.o-pillbar{display:flex;align-items:center;gap:28px;background:rgba(242,242,240,.86);backdrop-filter:blur(10px);-webkit-backdrop-filter:blur(10px);border:1px solid var(--line);border-radius:999px;padding:8px 8px 8px 22px}
.o-pillbar .wordmark{font-size:24px}
.o-solid{font-family:var(--mono);font-size:14px;text-decoration:none;background:var(--accent);color:#fff;border-radius:999px;padding:9px 18px}
.o-solid:hover{color:#fff;background:#A82815}
.o-split{display:grid;grid-template-columns:minmax(0,1.5fr) minmax(280px,1fr);align-items:end;gap:32px 56px;padding:40px 8px 12px}
.o-split h1{margin:0;font-weight:400;font-size:clamp(56px,8.4vw,128px);line-height:.92;letter-spacing:-.03em}
.o-lede{margin:0 0 18px;font-size:30px;line-height:1.15}
.o-status{display:flex;align-items:center;gap:10px;margin:0 0 22px;font-family:var(--mono);font-size:13px;color:var(--muted)}
.status-dot{width:8px;height:8px;border-radius:50%;background:#2E9E5B;box-shadow:0 0 0 4px rgba(46,158,91,.15)}
.o-ctas{display:flex;flex-wrap:wrap;gap:12px}
.o-btn{font-family:var(--mono);font-size:15px;text-decoration:none;border-radius:999px;padding:14px 22px}
.o-btn-ink{background:var(--ink);color:var(--bg)}
.o-btn-ink:hover{color:var(--bg);background:#000}
.o-drawing{padding-top:24px}
@media (max-width:760px){
  .o-pillbar{flex-wrap:wrap;justify-content:space-between;gap:10px 14px;border-radius:24px;padding:10px 10px 12px 18px;width:100%}
  .o-pillbar .site-nav{order:3;width:100%;gap:22px}
  .o-split{grid-template-columns:minmax(0,1fr)}
}
""",
    },
]

BADGE_CSS = """
.o-badge{position:fixed;left:16px;bottom:16px;z-index:50;display:flex;gap:10px;align-items:center;font:13px var(--mono);background:var(--ink);color:var(--bg);border-radius:999px;padding:8px 14px;box-shadow:0 6px 20px rgba(0,0,0,.18)}
.o-badge a{color:var(--bg);text-decoration:none}
.o-badge a:hover{color:#fff;text-decoration:underline}
@media (max-width:760px){ .o-badge{left:12px;bottom:12px;font-size:12px} .o-badge-name{display:none} }
"""


def page(opt, n):
    style = f'<meta name="robots" content="noindex">\n  <style>\n/* {opt["name"]}: only the nav and hero differ from the homepage */\n{scoped(opt["css"])}{BADGE_CSS}  </style>\n</head>'
    out = head.replace("</head>", style, 1).replace("<body>", f'<body class="opt">', 1)
    badge = f'\n<nav class="o-badge" aria-label="Hero options"><a href="/explorations/hero/">← all options</a><span>option {n} of {len(OPTIONS)}<span class="o-badge-name"> · {opt["name"]}</span></span></nav>\n'
    body = '<div class="page">' + before_header + opt["header"] + between + opt["hero"] + after_hero
    return out + body.replace("</body>", badge + "</body>", 1)


def scoped(css):
    """Prefix every rule's selectors with body.opt so the option's CSS wins over site.css.
    Works on each selector{...} block wherever it sits, including inside @media."""
    def fix(m):
        selectors, body = m.group(1), m.group(2)
        lead = selectors[: len(selectors) - len(selectors.lstrip())]
        scoped_sel = ",".join("body.opt " + sel.strip() for sel in selectors.split(","))
        return f"{lead}{scoped_sel}{{{body}}}"
    return re.sub(r"([^{}]+)\{([^{}]*)\}", fix, css.strip()) + "\n"


def overview():
    cards = []
    entries = [{"slug": "", "name": "Current homepage", "why": "What is on the redesign branch now, for reference.", "href": "/"}] + [
        {**o, "href": f"/explorations/hero/{o['slug']}/"} for o in OPTIONS
    ]
    for i, o in enumerate(entries):
        label = "current" if i == 0 else f"option {i}"
        cards.append(f"""
    <article class="cmp">
      <div class="cmp-head">
        <div><p class="cmp-num">{label}</p><h2>{o["name"]}</h2></div>
        <p class="cmp-links"><a href="{o["href"]}" target="_blank" rel="noopener">open ↗</a></p>
      </div>
      <p class="cmp-why">{o["why"]}</p>
      <div class="cmp-views">
        <div class="frame frame-desktop" data-w="1440" data-h="900"><iframe src="{o["href"]}" title="{o["name"]}, desktop" loading="lazy" tabindex="-1"></iframe></div>
        <div class="frame frame-phone" data-w="390" data-h="844"><iframe src="{o["href"]}" title="{o["name"]}, phone" loading="lazy" tabindex="-1"></iframe></div>
      </div>
    </article>""")
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <meta name="robots" content="noindex">
  <title>Hero options, compared</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Instrument+Serif:ital@0;1&amp;family=IBM+Plex+Mono:wght@400;500&amp;display=swap" rel="stylesheet">
  <link rel="stylesheet" href="/site.css">
  <style>
    .cmp-wrap{{max-width:1320px;margin:0 auto;display:flex;flex-direction:column;gap:28px}}
    .cmp-intro h1{{margin:0;font-weight:400;font-size:clamp(40px,5vw,64px);letter-spacing:-.02em}}
    .cmp-intro p{{margin:8px 0 0;font-family:var(--mono);font-size:14px;color:var(--muted);max-width:70ch;line-height:1.6}}
    .cmp{{background:var(--panel);border:1px solid var(--line);border-radius:24px;padding:24px;display:flex;flex-direction:column;gap:14px}}
    .cmp-head{{display:flex;justify-content:space-between;align-items:flex-end;gap:16px}}
    .cmp-num{{margin:0;font-family:var(--mono);font-size:13px;color:var(--accent)}}
    .cmp h2{{margin:2px 0 0;font-weight:400;font-size:36px;letter-spacing:-.01em}}
    .cmp-links{{margin:0;font-family:var(--mono);font-size:14px}}
    .cmp-links a{{text-decoration:none}}
    .cmp-why{{margin:0;font-family:var(--mono);font-size:14px;line-height:1.6;color:var(--muted);max-width:90ch}}
    .cmp-views{{display:grid;grid-template-columns:minmax(0,1fr) 220px;gap:16px;align-items:start}}
    .frame{{position:relative;overflow:hidden;border:1px solid var(--line);border-radius:14px;background:var(--bg)}}
    .frame iframe{{position:absolute;top:0;left:0;border:0;transform-origin:0 0;pointer-events:none}}
    @media (max-width:760px){{ .cmp-views{{grid-template-columns:minmax(0,1fr)}} .frame-phone{{max-width:220px}} }}
  </style>
</head>
<body>
<div class="page">
  <div class="cmp-wrap">
    <header class="cmp-intro">
      <h1>Nav and hero, <em>five ways</em></h1>
      <p>Each option keeps the product drawing, its hover interactions and the rest of the homepage exactly as they are; only the nav and the text around the drawing change. Previews show the top of each page at desktop and phone size. Open one to try it for real.</p>
    </header>
{"".join(cards)}
  </div>
</div>
<script>
  // Scale each 1440x900 (or 390x844) page down to fit its preview box.
  function fit() {{
    document.querySelectorAll(".frame").forEach((f) => {{
      const w = +f.dataset.w, h = +f.dataset.h, s = f.clientWidth / w;
      f.style.height = h * s + "px";
      const i = f.querySelector("iframe");
      i.style.width = w + "px"; i.style.height = h + "px"; i.style.transform = `scale(${{s}})`;
    }});
  }}
  addEventListener("resize", fit); fit();
</script>
</body>
</html>
"""


for n, opt in enumerate(OPTIONS, 1):
    d = OUT / opt["slug"]
    d.mkdir(parents=True, exist_ok=True)
    (d / "index.html").write_text(page(opt, n))
(OUT / "index.html").write_text(overview())
print(f"wrote {len(OPTIONS)} options and the overview to {OUT.relative_to(ROOT)}/")
