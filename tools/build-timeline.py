"""Rebuild the hero timeline's product row in site/index.html.

Takes the six product drawings from the original prototype, places them in
two staggered depths on an extruded platform so neighbors overlap, tags the
small parts that animate on hover, and writes the group back into the page.
Usage: python3 build_tl.py <prototype Main.dc.html> <site/index.html> [dots.json]
"""
import json, re, sys

proto, page = sys.argv[1], sys.argv[2]
dots = json.load(open(sys.argv[3])) if len(sys.argv) > 3 else {}

src = open(proto).read().replace("{{accent}}", "currentColor")
head = '<g fill="none" stroke="#1C1C1C" stroke-width="1.2" stroke-linejoin="round">'
start = src.index(head) + len(head)
end = src.index('<g fill="none" stroke="currentColor" stroke-width="1">', start)
items = re.findall(r'<g transform="translate[\s\S]*?\n</g>', src[start:end])
assert len(items) == 6, len(items)


def tag(s, old, new):
    assert s.count(old) == 1, (old, s.count(old))
    return s.replace(old, new)


# --- moving parts, per product -------------------------------------------
a = items[0]  # Apple display: the selection hops across the grid, shapes bob
a = tag(a, '<rect x="66" y="32" width="48" height="48" rx="3" fill="url(#tlRed)"></rect>',
        '<rect x="66" y="32" width="48" height="48" rx="3"></rect>'
        '<use href="#apple-logo" x="77.8" y="41" width="24.4" height="30" fill="#1C1C1C" stroke="none"></use>'
        '<rect class="an-tile" x="66" y="32" width="48" height="48" rx="3" fill="url(#tlRed)"></rect>')
a = tag(a, '<path d="M130 72 L144 48 L158 72 Z M184 72 C184 52 212 52 212 72"></path>',
        '<path class="an-shapes" d="M130 72 L144 48 L158 72 Z M184 72 C184 52 212 52 212 72"></path>')
items[0] = a

p = items[1]  # Printer: the head slides, the part prints up, the progress bar fills
p = tag(p, '<rect x="124" y="98" width="16" height="18" rx="2" fill="#F7F7F5"></rect>\n<path d="M128 116 L132 124 L136 116"></path>',
        '<g class="an-head"><rect x="124" y="98" width="16" height="18" rx="2" fill="#F7F7F5"></rect>\n<path d="M128 116 L132 124 L136 116"></path></g>')
p = tag(p, '<path d="M108 186 C112 168 118 156 132 146 C146 156 152 168 156 186 Z" fill="#F7F7F5"></path>\n<line x1="112" y1="176" x2="152" y2="176" stroke="#9A9A96"></line><line x1="116" y1="166" x2="148" y2="166" stroke="#9A9A96"></line>',
        '<g class="an-print"><path d="M108 186 C112 168 118 156 132 146 C146 156 152 168 156 186 Z" fill="#F7F7F5"></path>\n<line x1="112" y1="176" x2="152" y2="176" stroke="#9A9A96"></line><line x1="116" y1="166" x2="148" y2="166" stroke="#9A9A96"></line></g>')
p = tag(p, '<rect x="70" y="217" width="40" height="18" fill="url(#tlRed)" stroke="none"></rect>',
        '<rect class="an-bar" x="70" y="217" width="40" height="18" fill="url(#tlRed)" stroke="none"></rect>')
items[1] = p

m = items[2]  # Phone: a MetaMask wallet. The fox grows a little, the actions light up, the tokens slide in
WALLET = """<g class="an-fox"><use href="#mm-fox" x="152" y="68" width="34" height="31.6" fill="#1C1C1C" stroke="#1C1C1C" stroke-width="3.8" stroke-linejoin="round"></use></g>
<line x1="146" y1="114" x2="192" y2="114" stroke-width="3" stroke-linecap="round"></line>
<line x1="156" y1="123" x2="182" y2="123" stroke="#9A9A96"></line>
<circle class="an-key" style="--i:0" cx="143" cy="142" r="8"></circle>
<circle class="an-key" style="--i:1" cx="169" cy="142" r="8"></circle>
<circle class="an-key" style="--i:2" cx="195" cy="142" r="8"></circle>
<path d="M140 145 L146 139 M141.5 139 H146 V143.5" stroke-linecap="round"></path>
<path d="M169 138 V146 M165.5 142.5 L169 146 L172.5 142.5" stroke-linecap="round"></path>
<path d="M191 140 H199 M196.5 137.5 L199 140 L196.5 142.5 M199 144 H191 M193.5 141.5 L191 144 L193.5 146.5" stroke-linecap="round"></path>
<line x1="138" y1="157" x2="148" y2="157" stroke="#9A9A96"></line><line x1="164" y1="157" x2="174" y2="157" stroke="#9A9A96"></line><line x1="190" y1="157" x2="200" y2="157" stroke="#9A9A96"></line>
<line x1="124" y1="166" x2="214" y2="166" stroke="#9A9A96"></line>
""" + "\n".join(f"""<g class="an-row" style="--i:{i}">
<circle cx="131" cy="{y}" r="6"{' fill="url(#tlRed)"' if i == 0 else ''}></circle>
<line x1="142" y1="{y - 2}" x2="{166 - 4 * i}" y2="{y - 2}"></line><line x1="142" y1="{y + 4}" x2="{158 - 2 * i}" y2="{y + 4}" stroke="#9A9A96"></line>
<line x1="{188 + 3 * i}" y1="{y - 2}" x2="210" y2="{y - 2}"></line><line x1="198" y1="{y + 4}" x2="210" y2="{y + 4}" stroke="#9A9A96"></line>
</g>""" for i, y in enumerate((180, 199, 218))) + "\n"
m, n_sub = re.subn(r'<rect x="132" y="80" [\s\S]*?(?=<rect x="130" y="234")', lambda _: WALLET, m)
assert n_sub == 1
# The island and the bottom button are outlined like the rest of the line work, not solid black.
m = tag(m, '<rect x="150" y="52" width="38" height="10" rx="5" fill="#1C1C1C"></rect>', '<rect x="150" y="52" width="38" height="10" rx="5"></rect>')
m = tag(m, '<rect x="130" y="234" width="78" height="18" rx="9" fill="#1C1C1C"></rect>', '<rect x="130" y="234" width="78" height="18" rx="9"></rect>')
items[2] = m

w = items[3]  # Portal: the card slides forward, its two circles spread apart
w = tag(w, '<rect x="12" y="41" width="140" height="88" rx="12" fill="#E3E3E0"></rect>',
        '<g class="an-card"><rect x="12" y="41" width="140" height="88" rx="12" fill="#E3E3E0"></rect>')
w = tag(w, '<circle cx="110" cy="117" r="8"></circle><circle cx="120" cy="117" r="8"></circle>',
        '<circle class="an-c1" cx="110" cy="117" r="8"></circle><circle class="an-c2" cx="120" cy="117" r="8"></circle></g>')
items[3] = w

n = items[4]  # Intuition: the core pulses, the nodes answer one after another
n = tag(n, '<circle cx="160" cy="118" r="24" fill="url(#tlRed)" stroke="none"></circle>',
        '<circle class="an-core" cx="160" cy="118" r="24" fill="url(#tlRed)" stroke="none"></circle>')
for i, c in enumerate(['cx="92" cy="76" r="12"', 'cx="236" cy="70" r="14"', 'cx="240" cy="166" r="11"', 'cx="160" cy="186" r="7"', 'cx="84" cy="162" r="10"']):
    n = tag(n, f'<circle {c} fill="#F7F7F5"></circle>', f'<circle class="an-node" style="--i:{i}" {c} fill="#F7F7F5"></circle>')
items[4] = n

l = items[5]  # Laptop: code types itself out, the small window bobs
for i, ln in enumerate([
    '<line x1="80" y1="32" x2="130" y2="32"></line>',
    '<line x1="90" y1="44" x2="150" y2="44" stroke="currentColor"></line>',
    '<line x1="90" y1="56" x2="138" y2="56"></line>',
    '<line x1="100" y1="68" x2="160" y2="68" stroke="#9A9A96"></line>',
    '<line x1="90" y1="80" x2="124" y2="80"></line>',
    '<line x1="80" y1="92" x2="112" y2="92" stroke="currentColor"></line>',
    '<line x1="80" y1="104" x2="140" y2="104" stroke="#9A9A96"></line>',
]):
    l = tag(l, ln, ln.replace("<line ", f'<line class="an-code" style="--i:{i}" ', 1))
l = tag(l, '<rect x="182" y="-38" width="74" height="58" rx="7" fill="#E3E3E0"></rect>',
        '<g class="an-pop"><rect x="182" y="-38" width="74" height="58" rx="7" fill="#E3E3E0"></rect>')
l = tag(l, '<line x1="182" y1="14" x2="222" y2="14" stroke="#9A9A96"></line>',
        '<line x1="182" y1="14" x2="222" y2="14" stroke="#9A9A96"></line></g>')
items[5] = l

# --- extrusions --------------------------------------------------------------
# Each product fakes depth with a back panel offset up and to the right plus
# loose corner ticks, which miss the rounded corners. Replace each with one
# solid shape: the front panel swept back to the rear one (convex hull, so its
# edges are tangent to the rounded corners), and a single ridge line where the
# top and side faces meet.
import math


def rounded_pts(x, y, w, h, r, n=12):
    pts = []
    for cx, cy, a0 in ((x + w - r, y + r, -90), (x + w - r, y + h - r, 0), (x + r, y + h - r, 90), (x + r, y + r, 180)):
        for i in range(n + 1):
            a = math.radians(a0 + 90 * i / n)
            pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    return pts


def hull(pts):
    pts = sorted(set((round(px, 2), round(py, 2)) for px, py in pts))
    cross = lambda o, a, b: (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])
    lower, upper = [], []
    for pt in pts:
        while len(lower) >= 2 and cross(lower[-2], lower[-1], pt) <= 0:
            lower.pop()
        lower.append(pt)
    for pt in reversed(pts):
        while len(upper) >= 2 and cross(upper[-2], upper[-1], pt) <= 0:
            upper.pop()
        upper.append(pt)
    return lower[:-1] + upper[:-1]


def solid(front, dx, dy, side="#E3E3E0"):
    """Front panel <rect ...> plus depth (dx, dy) -> extruded body, ridge, front panel."""
    v = {k: float(re.search(rf' {k}="([-\d.]+)"', front).group(1)) for k in ("x", "y", "width", "height", "rx")}
    x, y, w, h, r = v["x"], v["y"], v["width"], v["height"], v["rx"]
    pts = rounded_pts(x, y, w, h, r) + [(px + dx, py + dy) for px, py in rounded_pts(x, y, w, h, r)]
    body = "M" + " L".join(f"{px:g} {py:g}" for px, py in hull(pts)) + " Z"
    k = math.sqrt(0.5)
    rx0, ry0 = x + w - r + r * k, y + r - r * k
    ridge = f'<path d="M{rx0:.2f} {ry0:.2f} L{rx0 + dx:.2f} {ry0 + dy:.2f}"></path>'
    return f'<path class="xt-body" d="{body}" fill="{side}"></path>\n{ridge}\n{front}'


def extrude(s, back, ticks, front, dx, dy):
    old = f"{back}\n{ticks}\n{front}"
    assert s.count(old) == 1, ("extrude", back)
    return s.replace(old, solid(front, dx, dy))


E = '<rect x="{}" y="{}" width="{}" height="{}" rx="{}" fill="{}"></rect>'
items[0] = extrude(items[0], E.format(10, -7, 240, 150, 8, "#E3E3E0"), '<path d="M2 6 L12 -1 M238 6 L248 -1 M238 144 L248 137"></path>', E.format(0, 0, 240, 150, 8, "#F7F7F5"), 10, -7)
items[2] = extrude(items[2], E.format(124, 26, 116, 236, 24, "#E3E3E0"), '<path d="M134 26 L122 36 M230 262 L218 272"></path>', E.format(110, 36, 118, 236, 24, "#F7F7F5"), 13, -10)
items[3] = extrude(items[3], E.format(52, -9, 150, 110, 8, "#E3E3E0"), '<path d="M44 4 L54 -3 M188 4 L198 -3 M188 104 L198 97"></path>', E.format(40, 0, 150, 110, 8, "#F7F7F5"), 12, -9)
items[3] = extrude(items[3], E.format(12, 41, 140, 88, 12, "#E3E3E0"), '<path d="M4 58 L14 51 M136 58 L146 51 M136 134 L146 127"></path>', E.format(0, 50, 140, 88, 12, "#F7F7F5"), 12, -9)
items[4] = extrude(items[4], E.format(44, 6, 260, 186, 10, "#E3E3E0"), '<path d="M33 22 L46 10 M287 22 L300 10 M287 202 L300 190"></path>', E.format(30, 18, 260, 186, 10, "#F7F7F5"), 14, -12)
items[5] = extrude(items[5], E.format(30, -7, 200, 132, 8, "#E3E3E0"), '<path d="M22 6 L32 -1 M218 6 L228 -1"></path>', E.format(20, 0, 200, 132, 8, "#F7F7F5"), 10, -7)
items[5] = extrude(items[5], E.format(182, -38, 74, 58, 7, "#E3E3E0"), '<path d="M175 -27 L184 -33 M245 -27 L254 -33 M245 24 L254 18"></path>', E.format(172, -31, 74, 58, 7, "#F7F7F5"), 10, -7)

# Mobina (case study 06): the laptop again, playing a film instead of code.
mobina = items[5]
mobina = re.sub(r'<g class="an-pop">[\s\S]*?</g>', "", mobina)
mobina = re.sub(r'<line class="an-code"[^>]*></line>\n?', "", mobina)
for ln in ['<line x1="70" y1="20" x2="70" y2="124"></line>',
           '<line x1="36" y1="30" x2="62" y2="30" stroke="#9A9A96"></line><line x1="36" y1="40" x2="58" y2="40" stroke="#9A9A96"></line><line x1="36" y1="50" x2="60" y2="50" stroke="#9A9A96"></line>']:
    assert mobina.count(ln) == 1, ln
    mobina = mobina.replace(ln, "")
mobina = mobina.replace("</g>", """<path class="an-play" d="M120 41.5 L126.5 48 L120 54.5 L113.5 48 Z M110 51.5 L116.5 58 L110 64.5 L103.5 58 Z M130 51.5 L136.5 58 L130 64.5 L123.5 58 Z M120 61.5 L126.5 68 L120 74.5 L113.5 68 Z" stroke-width="2.2" stroke-linejoin="miter"></path>
<rect x="44" y="94" width="152" height="8" fill="#F7F7F5"></rect>
<rect class="an-progress" x="44" y="94" width="152" height="8" fill="url(#tlRed)" stroke="none"></rect>
<line x1="44" y1="112" x2="150" y2="112" stroke="#9A9A96"></line>
</g>""", 1)

# --- placement --------------------------------------------------------------
# (name, original left, right, top, column x, scale, front?)
GEOM = [
    ("apple", 90, 290, 418, 190, 1.22, True),
    ("printer", 309.5, 489.7, 403.7, 400, 1.22, False),
    ("phone", 551, 668, 364.4, 610, 1.18, True),
    ("portal", 720, 922, 439, 820, 1.22, False),
    ("intuition", 935, 1127, 447, 1030, 1.22, True),
    ("laptop", 1140, 1345, 437, 1240, 1.12, False),
]
OVERLAP = 30
BASE0 = 586  # where the drawings sit in the prototype
BASE = {True: 610, False: 591}  # front row, back row
DELAY = ["-0.2s", "-1.1s", "-0.6s", "-1.7s", "-0.9s", "-1.4s"]

placed, prev = [], None
for (name, l0, r0, top, X, k, front) in GEOM:
    c0 = (l0 + r0) / 2
    hw = (r0 - l0) / 2 * k
    c = c0 if prev is None else prev + hw - OVERLAP
    placed.append(dict(name=name, c0=c0, c=c, hw=hw, top=top, X=X, k=k, front=front))
    prev = c + hw
shift = 700 - (placed[0]["c"] - placed[0]["hw"] + placed[-1]["c"] + placed[-1]["hw"]) / 2
for g in placed:
    g["c"] += shift

groups = {}
for i, (g, art) in enumerate(zip(placed, items)):
    base = BASE[g["front"]]
    dx, k, c0 = g["c"] - g["c0"], g["k"], g["c0"]
    place = f"translate({dx + c0:.1f} {base}) scale({k}) translate({-c0:.1f} {-BASE0})"
    top_y = base - (BASE0 - g["top"]) * k
    dot_y = round(dots.get(g["name"], top_y), 1)
    X = g["X"]
    left, right = g["c"] - g["hw"], g["c"] + g["hw"]
    groups[g["name"]] = f'''<g class="tl-item" data-name="{g["name"]}" style="--len:{dot_y - 304:.1f};--d:{DELAY[i]}">
<rect class="tl-hit" x="{left:.1f}" y="228" width="{right - left:.1f}" height="{base + 4 - 228}" fill="transparent"></rect>
<ellipse class="tl-shadow" cx="{g["c"]:.1f}" cy="{base + 3}" rx="{g["hw"] * 0.62:.1f}" ry="7" fill="#1C1C1C"></ellipse>
<g class="tl-float">
<g class="tl-art" transform="{place}" fill="none" stroke="#1C1C1C" stroke-width="1.2" stroke-linejoin="round">
{art}
</g>
<circle class="tl-dot" cx="{X}" cy="{dot_y}" r="3" fill="currentColor"></circle>
</g>
<path class="tl-lead" fill="none" stroke="currentColor" stroke-width="1" d="M{X} 304 L{X} {dot_y}"></path>
</g>'''

order = [g["name"] for g in placed if not g["front"]] + [g["name"] for g in placed if g["front"]]
row = '<g class="tl-items">\n' + "\n".join(groups[n] for n in order) + "\n</g>"

# Extruded platform: the dotted top, a front face and a right-hand side face.
platform = '''<g class="tl-platform" stroke="#1C1C1C" stroke-width="1" stroke-linejoin="round">
<polygon points="50,620 1290,620 1290,636 50,636" fill="#E3E3E0"></polygon>
<polygon points="1290,620 1350,586 1350,602 1290,636" fill="#D3D3CF"></polygon>
<polygon points="50,620 110,586 1350,586 1290,620" fill="url(#tlGray)"></polygon>
</g>'''

html = open(page).read()
html, n1 = re.subn(r'<polygon points="50,620 110,586 1350,586 1290,620"[^>]*></polygon>|<g class="tl-platform"[\s\S]*?</g>', platform, html, count=1)
html, n2 = re.subn(r'<g class="tl-items">[\s\S]*?\n</g>\n(?=<g fill="currentColor" font-family)', row + "\n", html, count=1)
# The dashed drop lines start under the platform's new front face.
html = re.sub(r'M190 6\d\d L190 646 M400 6\d\d L400 646 M610 6\d\d L610 646 M820 6\d\d L820 646 M1030 6\d\d L1030 646 M1240 6\d\d L1240 646',
              "M190 636 L190 646 M400 636 L400 646 M610 636 L610 646 M820 636 L820 646 M1030 636 L1030 646 M1240 636 L1240 646", html)
assert n1 == 1 and n2 == 1, (n1, n2)

# --- selected work cards ----------------------------------------------------
# Each case-study card shows its product on a small slab of its own, drawn in
# the same coordinates as the timeline so the art is reused unchanged.
CARD_ART = [items[0], items[1], items[2], items[3], items[4], mobina]
CARD_GEOM = [GEOM[0], GEOM[1], GEOM[2], GEOM[3], GEOM[4], GEOM[5]]
def product_svg(art, geom, cls):
    """One product on a small slab of its own, in the timeline's coordinates."""
    name, l0, r0, top, X, k, front = geom
    pad = 24
    vx, vy = l0 - pad - 20, top - 46
    vw, vh = (r0 - l0) + 2 * pad + 40, (BASE0 + 30) - vy
    a, b2 = l0 - pad, r0 + pad
    slab = f"""<g class="tl-platform" stroke="#1C1C1C" stroke-width="1" stroke-linejoin="round">
<polygon points="{a - 16},{BASE0 + 10} {b2 - 16},{BASE0 + 10} {b2 - 16},{BASE0 + 18} {a - 16},{BASE0 + 18}" fill="#E3E3E0"></polygon>
<polygon points="{b2 - 16},{BASE0 + 10} {b2 + 4},{BASE0 - 6} {b2 + 4},{BASE0 + 2} {b2 - 16},{BASE0 + 18}" fill="#D3D3CF"></polygon>
<polygon points="{a - 16},{BASE0 + 10} {a + 4},{BASE0 - 6} {b2 + 4},{BASE0 - 6} {b2 - 16},{BASE0 + 10}" fill="url(#tlGray)"></polygon>
</g>"""
    cx = (l0 + r0) / 2
    return f"""<svg class="{cls}" aria-hidden="true" viewBox="{vx:g} {vy:g} {vw:g} {vh:g}">
{slab}
<g class="tl-item">
<ellipse class="tl-shadow" cx="{cx:g}" cy="{BASE0 + 2}" rx="{(r0 - l0) * 0.36:.1f}" ry="6" fill="#1C1C1C"></ellipse>
<g class="tl-float">
<g fill="none" stroke="#1C1C1C" stroke-width="1.2" stroke-linejoin="round">
{art}
</g>
</g>
</g>
</svg>"""


card_svgs = [product_svg(art, geom, "card-art") for art, geom in zip(CARD_ART, CARD_GEOM)]

card_re = re.compile(r'(<a class="card" [^>]*>\s*<div class="card-meta">[\s\S]*?</div>\s*)(<svg[\s\S]*?</svg>)')
found = card_re.findall(html)
assert len(found) == 6, len(found)
it = iter(card_svgs)
html = card_re.sub(lambda m: m.group(1) + next(it), html)

# --- stacked timeline for phones --------------------------------------------
# On narrow screens the wide drawing gives way to the same six products stacked
# top to bottom along a vertical timeline. Phones can't hover, so each product
# floats and plays its animation while it sits in the middle of the screen.
STEPS = [("01", "Apple", "ID tools"), ("02", "Origin Labs", "hardware UI"), ("03", "MetaMask", "wallet, 30M+ MAU"),
         ("04", "Portal", "wallet + brand"), ("05", "Intuition", "knowledge network"), ("06", "Today", "building my own apps")]
steps = "\n".join(
    f"""<li class="tl-step{' is-now' if i == len(STEPS) - 1 else ''}">
<p class="tl-step-label"><span>{num}</span> {label}</p>
<p class="tl-step-desc">{desc}</p>
{product_svg(art, geom, "tl-step-art")}
</li>"""
    for i, ((num, label, desc), art, geom) in enumerate(zip(STEPS, items, GEOM))
)
stack_html = f"""<div class="tl-stack">
<p class="tl-stack-end">earlier</p>
<ol class="tl-steps" aria-label="Timeline, earlier to now">
{steps}
</ol>
<p class="tl-stack-end">now</p>
<script>
  // Phones: float the product nearest the middle of the screen.
  (() => {{
    const steps = document.querySelectorAll(".tl-step .tl-item");
    if (!("IntersectionObserver" in window) || !steps.length) return;
    const io = new IntersectionObserver((entries) => {{
      entries.forEach((e) => e.target.classList.toggle("is-focus", e.isIntersecting));
    }}, {{ rootMargin: "-35% 0px -35% 0px" }});
    steps.forEach((s) => io.observe(s));
  }})();
</script>
</div>"""
html = re.sub(r'\n?<div class="tl-stack">[\s\S]*?</script>\n</div>', "", html)
html, n_stack = re.subn(r'(<svg class="timeline"[\s\S]*?</svg>)', lambda m: m.group(1) + "\n      " + stack_html, html, count=1)
assert n_stack == 1

# --- shared patterns ---------------------------------------------------------
# The red dot fill and the slab texture are used by the hero, the work cards and
# the phone timeline. They live in the page's always-present symbol block (next
# to the fox and Apple logo), because phones hide the wide hero drawing and some
# browsers stop painting patterns defined inside a hidden drawing.
PATTERNS = ('<pattern id="tlRed" width="5" height="5" patternUnits="userSpaceOnUse"><circle cx="2.5" cy="2.5" r="1.5" fill="currentColor"></circle></pattern>\n'
            '<pattern id="tlGray" width="6" height="6" patternUnits="userSpaceOnUse"><circle cx="3" cy="3" r="1.2" fill="#CFCFCB"></circle></pattern>')
html = re.sub(r'<defs>\s*<pattern id="tlRed"[\s\S]*?</defs>\n?', "", html)  # out of the hero drawing (and any earlier copy)
sym_open = '<svg width="0" height="0" style="position:absolute" aria-hidden="true" focusable="false">'
sym_open_new = '<svg width="0" height="0" style="position:absolute;color:var(--accent)" aria-hidden="true" focusable="false">'
html = html.replace(sym_open, sym_open_new, 1)
assert html.count(sym_open_new) == 1
html = html.replace(sym_open_new, sym_open_new + "\n<defs>\n" + PATTERNS + "\n</defs>", 1)
open(page, "w").write(html)
print("placed:", ", ".join(f'{g["name"]} c={g["c"]:.0f}' for g in placed))
