# Baut die Grafiken der Profil-README im Stil von halograph.app.  python3 tools/build_assets.py contrib.json
import json, os, sys, collections
sys.path.insert(0, os.path.dirname(__file__))
from style import *
A = os.path.join(os.path.dirname(__file__), "..", "assets")
d = json.load(open(sys.argv[1])); total = d["totalContributions"]
m = collections.OrderedDict()
for w in d["weeks"]:
    for x in w["contributionDays"]: m[x["date"][:7]] = m.get(x["date"][:7], 0) + x["contributionCount"]
months = [(k, v) for k, v in m.items() if k >= "2026-05"]

# Titelbild
inner = sphere(990, 170, 150) + \
  f'<text x="64" y="86" fill="{MUTED}" font-family="{F}" font-size="17">founder · builds with AI</text>' + \
  f'<text x="61" y="184" fill="{TEXT}" font-family="{F}" font-size="72" font-weight="600" letter-spacing="-2.4">Elias Conrad</text>' + \
  f'<text x="64" y="230" fill="{MUTED}" font-family="{F}" font-size="24">Agentic infrastructure and the products on top of it.</text>' + \
  pill(64, 268, f"{total:,} contributions since May 2026")
open(f"{A}/hero.svg", "w").write(frame(1200, 340, inner, "Elias Conrad. Agentic infrastructure and the products on top of it."))

# Animierte Zeile
words = ["agentic infrastructure", "open-weight models in production", "iOS apps people actually use", "memory for AI agents", "products, from idea to App Store"]
items = [f'<text x="234" y="31" fill="{TEXT}" font-family="{M}" font-size="16">{w}</text>' for w in words]
tag = f'<text x="64" y="31" fill="{DIM}" font-family="{M}" font-size="16">$ now building</text>{cycle(items, 0, 0, step=3)}' + \
      f'<rect x="1128" y="16" width="8" height="18" fill="{TEXT}"><animate attributeName="opacity" values="1;0;1" dur="1.1s" repeatCount="indefinite"/></rect>'
open(f"{A}/tagline.svg", "w").write(f'<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="48" viewBox="0 0 1200 48" role="img" aria-label="Now building: agentic infrastructure, open-weight models, iOS apps, memory for AI agents">{tag}</svg>')

# Projektkarten
def card(key, name, l1, l2, status, url, withmark):
    w = 580; inner = []
    inner.append(f'<rect x="0.5" y="0.5" width="{w-1}" height="199" rx="20" fill="{CARD}" stroke="{LINE}"/>')
    if withmark: inner.append(sphere(w - 90, 100, 70, n=180, size=1.8, maxop=0.7))
    inner.append(f'<text x="24" y="38" fill="{DIM}" font-family="{M}" font-size="12.5">{url}</text>')
    if withmark: inner.append(mark(24, 56, 26))
    inner.append(f'<text x="{60 if withmark else 24}" y="78" fill="{TEXT}" font-family="{F}" font-size="28" font-weight="600" letter-spacing="-0.5">{name}</text>')
    inner.append(f'<text x="24" y="114" fill="{MUTED}" font-family="{F}" font-size="15">{l1}</text>')
    inner.append(f'<text x="24" y="135" fill="{MUTED}" font-family="{F}" font-size="15">{l2}</text>')
    inner.append(pill(24, 156, status))
    open(f"{A}/card-{key}.svg", "w").write(f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="200" viewBox="0 0 {w} 200" role="img" aria-label="{name}: {l1} {l2}">{"".join(inner)}</svg>')
card("halograph", "Halograph", "Agentic infrastructure: one memory for every AI agent.", "Mails, messages, meetings and notes, served over MCP.", "running daily · open skill", "halograph.app", True)
card("facet", "Facet", "A focus blocker for the Mac.", "Block what distracts you, keep what you need.", "mac app · download", "eliasconrad.github.io/facet", False)

# Zeitstrahl
steps = [("before 2026", "Web design", "brands, layouts, copy"), ("May 2026", "First commit", "GitHub account opened"), ("Aug 2026", "First iOS app", "on TestFlight"),
         ("Sep 2026", "Backend + payments", "running on Cloudflare"), ("Oct 2026", "Agents in parallel", "a team of AI agents"), ("Nov 2026", "Halograph", "memory for agents")]
W = 1200; x0, x1 = 90, W - 90; st = (x1 - x0) / (len(steps) - 1)
el = [f'<line x1="{x0}" y1="92" x2="{x1}" y2="92" stroke="{LINE}" stroke-width="1.5"/>',
      f'<line x1="{x0}" y1="92" x2="{x1}" y2="92" stroke="{TEXT}" stroke-opacity=".55" stroke-width="1.5" stroke-dasharray="{x1-x0}" stroke-dashoffset="{x1-x0}"><animate attributeName="stroke-dashoffset" from="{x1-x0}" to="0" dur="2.4s" fill="freeze"/></line>']
for i, (dt, t, s) in enumerate(steps):
    x = x0 + i * st; last = i == len(steps) - 1
    el.append(f'<text x="{x:.0f}" y="58" fill="{DIM}" font-family="{M}" font-size="12.5" text-anchor="middle">{dt}</text>')
    el.append(f'<circle cx="{x:.0f}" cy="92" r="{6 if last else 4.5}" fill="{TEXT if i else MUTED}" stroke="{BG}" stroke-width="3"/>')
    if last: el.append(f'<circle cx="{x:.0f}" cy="92" r="6" fill="none" stroke="{TEXT}"><animate attributeName="r" values="6;16" dur="1.8s" repeatCount="indefinite"/><animate attributeName="opacity" values=".7;0" dur="1.8s" repeatCount="indefinite"/></circle>')
    el.append(f'<text x="{x:.0f}" y="130" fill="{TEXT}" font-family="{F}" font-size="15.5" font-weight="600" text-anchor="middle">{t}</text>')
    el.append(f'<text x="{x:.0f}" y="152" fill="{MUTED}" font-family="{F}" font-size="13" text-anchor="middle">{s}</text>')
open(f"{A}/timeline.svg", "w").write(frame(W, 186, "".join(el), "Timeline from web design in 2025 to Halograph in November 2026"))

# Beiträge pro Monat
names = {"05": "May", "06": "Jun", "07": "Jul", "08": "Aug", "09": "Sep", "10": "Oct", "11": "Nov"}
W, H, base, top = 1200, 300, 236, 86; n = len(months); slot = (W - 160) / n; mx = max(v for _, v in months); bars = []
for i, (k, v) in enumerate(months):
    h = (base - top) * v / mx; x = 80 + i * slot + slot * 0.3; w = slot * 0.4
    bars.append(f'<rect x="{x:.0f}" y="{base-h:.0f}" width="{w:.0f}" height="{max(h,2):.0f}" rx="{w/2:.0f}" fill="#fff" opacity="{0.25+0.75*v/mx:.2f}"/>')
    bars.append(f'<text x="{x+w/2:.0f}" y="{base-h-12:.0f}" fill="{TEXT}" font-family="{M}" font-size="14" text-anchor="middle">{v:,}</text>')
    bars.append(f'<text x="{x+w/2:.0f}" y="{base+30:.0f}" fill="{MUTED}" font-family="{F}" font-size="14" text-anchor="middle">{names[k[5:]]}</text>')
inner = f'<text x="80" y="44" fill="{DIM}" font-family="{M}" font-size="13">contributions per month · 2026</text><line x1="80" y1="{base}" x2="{W-80}" y2="{base}" stroke="{LINE}"/>' + "".join(bars)
open(f"{A}/shipping.svg", "w").write(frame(W, H, inner, f"Contributions per month since May 2026, {total} in total"))
print("ok", total)
