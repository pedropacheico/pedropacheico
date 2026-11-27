"""Peças compartilhadas pelos SVGs do perfil: fontes embutidas, paleta e skyline gótica."""
import base64
import random
from pathlib import Path

ROOT = Path(__file__).resolve().parent
FONTS = ROOT

# Paleta "sangue e trevas"
BG = "#07070a"
BG2 = "#0e0b10"
PANEL = "#0c0c11"
LINE = "#2a1a1e"
RED = "#d1141c"
RED_HOT = "#ff2a33"
RED_DARK = "#5c0a0e"
TEXT = "#ece6e6"
MUTED = "#8a7f82"

_FONT_FILES = {
    "Pirata": "pirata-one-latin-400-normal.woff2",
    "Oswald": "oswald-latin-700-normal.woff2",
    "OswaldR": "oswald-latin-400-normal.woff2",
    "Mono": "jetbrains-mono-latin-400-normal.woff2",
}


def font_css(*names):
    """GitHub mostra SVG como <img>, então a fonte precisa ir embutida em base64."""
    out = []
    for n in names:
        data = base64.b64encode((FONTS / _FONT_FILES[n]).read_bytes()).decode()
        out.append(
            f"@font-face{{font-family:'{n}';src:url(data:font/woff2;base64,{data}) format('woff2');}}"
        )
    return "\n".join(out)


def esc(s):
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def skyline(width, base_y, max_h, seed=7, fill="#000"):
    """Silhueta de cidade gótica: torres, pináculos e catedrais."""
    rnd = random.Random(seed)
    parts = []
    x = -10
    while x < width + 10:
        w = rnd.randint(14, 46)
        h = rnd.randint(int(max_h * 0.25), max_h)
        kind = rnd.random()
        top = base_y - h
        parts.append(f'<rect x="{x}" y="{top}" width="{w}" height="{h + 2}"/>')
        if kind < 0.35:  # pináculo
            sw = max(4, w // 3)
            sx = x + (w - sw) / 2
            sh = rnd.randint(18, 48)
            parts.append(f'<polygon points="{sx},{top} {sx + sw / 2},{top - sh} {sx + sw},{top}"/>')
        elif kind < 0.55:  # telhado de catedral
            parts.append(f'<polygon points="{x},{top} {x + w / 2},{top - w * 0.7} {x + w},{top}"/>')
        elif kind < 0.7:  # torres gêmeas
            for tx in (x + 2, x + w - 7):
                th = rnd.randint(10, 26)
                parts.append(f'<rect x="{tx}" y="{top - th}" width="5" height="{th}"/>')
                parts.append(f'<polygon points="{tx},{top - th} {tx + 2.5},{top - th - 9} {tx + 5},{top - th}"/>')
        x += w + rnd.randint(-4, 3)
    return f'<g fill="{fill}">{"".join(parts)}</g>'


def windows(width, base_y, max_h, seed=11, count=40):
    rnd = random.Random(seed)
    out = []
    for _ in range(count):
        x = rnd.uniform(0, width)
        y = base_y - rnd.uniform(6, max_h * 0.7)
        op = rnd.uniform(0.25, 0.9)
        dur = rnd.uniform(2.5, 7)
        out.append(
            f'<rect x="{x:.1f}" y="{y:.1f}" width="2" height="3" fill="{RED_HOT}" opacity="{op:.2f}">'
            f'<animate attributeName="opacity" values="{op:.2f};0.05;{op:.2f}" dur="{dur:.1f}s" repeatCount="indefinite"/></rect>'
        )
    return "".join(out)


def rain(width, height, seed=3, count=60):
    rnd = random.Random(seed)
    out = []
    for _ in range(count):
        x = rnd.uniform(0, width + 60)
        l = rnd.uniform(10, 26)
        d = rnd.uniform(0.7, 1.6)
        b = rnd.uniform(0, 2)
        op = rnd.uniform(0.08, 0.3)
        out.append(
            f'<line x1="{x:.0f}" y1="-30" x2="{x - l * 0.35:.0f}" y2="{-30 + l:.0f}" stroke="#c9b8bb" stroke-width="1" opacity="{op:.2f}">'
            f'<animateTransform attributeName="transform" type="translate" from="0 0" to="-{height * 0.35:.0f} {height + 60}" dur="{d:.2f}s" begin="-{b:.2f}s" repeatCount="indefinite"/></line>'
        )
    return "".join(out)
