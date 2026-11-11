# Gemeinsamer Stil der Grafiken: wie halograph.app (Schwarz, Punkt-Kugel, Weiß, keine Farbakzente).
import math
BG = "#0a0a0a"; CARD = "#0f0f0f"; LINE = "#232323"; TEXT = "#ededed"; MUTED = "#8a8a8a"; DIM = "#5c5c5c"
F = "-apple-system,BlinkMacSystemFont,'SF Pro Display','Helvetica Neue',Inter,system-ui,sans-serif"
M = "'JetBrains Mono',ui-monospace,SFMono-Regular,Menlo,monospace"

def sphere(cx, cy, r, n=420, tilt=0.42, spin=0.6, size=2.3, maxop=0.9):
    """Kugel aus Punkten (Fibonacci), orthografisch projiziert. Vorn hell, hinten blass."""
    out = []; ga = math.pi * (3 - math.sqrt(5))
    for i in range(n):
        y = 1 - (i / (n - 1)) * 2; rad = math.sqrt(1 - y * y); th = ga * i + spin
        x, z = math.cos(th) * rad, math.sin(th) * rad
        y2 = y * math.cos(tilt) - z * math.sin(tilt); z2 = y * math.sin(tilt) + z * math.cos(tilt)
        if z2 < -0.15: continue
        op = maxop * (0.18 + 0.82 * (z2 + 0.15) / 1.15)
        out.append(f'<circle cx="{cx + x * r:.1f}" cy="{cy - y2 * r:.1f}" r="{size * (0.7 + 0.5 * z2):.2f}" fill="#fff" opacity="{op:.2f}"/>')
    return "".join(out)

def mark(x, y, s, fill=TEXT):
    """Halograph-Zeichen (aus public/mark.svg), s = Kantenlänge in px."""
    k = s / 800; g = []
    for a in range(0, 360, 60):
        g.append(f'<g transform="rotate({a} 512 512)"><rect x="362" y="202" width="300" height="140" rx="70" transform="rotate(-30 512 272)"/></g>')
    return f'<g transform="translate({x},{y}) scale({k:.4f}) translate(-112,-112)" fill="{fill}">{"".join(g)}<circle cx="512" cy="512" r="58"/></g>'

def frame(w, h, inner, label, rx=24):
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="{label}"><rect width="{w}" height="{h}" rx="{rx}" fill="{BG}"/>{inner}</svg>'

def pill(x, y, text, pulse=True):
    w = len(text) * 7.6 + 40
    dot = f'<circle cx="{x+14}" cy="{y+13}" r="3.5" fill="{TEXT}">' + ('<animate attributeName="opacity" values="1;.3;1" dur="2.2s" repeatCount="indefinite"/>' if pulse else '') + '</circle>'
    return f'<rect x="{x}" y="{y}" width="{w:.0f}" height="26" rx="13" fill="#fff" fill-opacity=".07" stroke="{LINE}"/>{dot}<text x="{x+26}" y="{y+17.5}" fill="{TEXT}" font-family="{M}" font-size="12">{text}</text>'

def cycle(items, x, y, size=17, color=TEXT, anchor="start", step=3.2):
    n = len(items); dur = n * step; out = []
    for i, it in enumerate(items):
        a, b = i / n, (i + 1) / n
        kt = f"0;{a:.3f};{a+0.02:.3f};{b-0.02:.3f};{b:.3f};1"
        out.append(f'<g opacity="0">{it}<animate attributeName="opacity" values="0;0;1;1;0;0" keyTimes="{kt}" dur="{dur:.1f}s" repeatCount="indefinite"/></g>')
    return "".join(out)
