"""Gera os SVGs estáticos do perfil (cabeçalho, títulos de seção, faixas e rodapé).

Rode `python scripts/build_assets.py` depois de mudar algum texto aqui.
"""
from svgkit import (BG, BG2, LINE, MUTED, PANEL, RED, RED_DARK, RED_HOT, ROOT, TEXT,
                    esc, font_css, rain, skyline, windows)

OUT = ROOT / "assets"
W = 850

# ---------------------------------------------------------------- textos
NOME = "Pedro Pacheico"
SUBTITULO = "BACKEND DEV  ·  PYTHON  ·  DJANGO  ·  CAÇADOR DE BUGS"
LINHA_TOPO = "SYS://PEDROPACHEICO"

SECOES = [
    ("01", "SOBRE", "PLAYER.INFO"),
    ("02", "ARSENAL", "WEAPONS.LIST"),
    ("03", "MISSÕES", "MISSION.LOG"),
    ("04", "FORMAÇÃO", "LORE"),
    ("05", "STYLISH RANK", "COMBO.METER"),
    ("06", "ARENA", "BLOODY.PALACE"),
    ("07", "CONTATO", "OPEN.CHANNEL"),
]

FAIXAS = {
    "banner-arsenal": "Cada linguagem, uma lâmina",
    "banner-missoes": "Missões em andamento",
    "banner-formacao": "O treino nunca termina",
    "banner-contato": "O portal está aberto",
}


def svg(w, h, body, fonts, extra_css=""):
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">'
        f"<style>{font_css(*fonts)}{extra_css}</style>{body}</svg>"
    )


def header():
    h = 300
    sky_base = h
    body = f"""
<defs>
  <linearGradient id="sky" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="{BG}"/><stop offset="0.55" stop-color="#1a0507"/><stop offset="1" stop-color="#4a070b"/>
  </linearGradient>
  <radialGradient id="moonGlow">
    <stop offset="0.55" stop-color="{RED_HOT}" stop-opacity="0.55"/><stop offset="1" stop-color="{RED}" stop-opacity="0"/>
  </radialGradient>
  <radialGradient id="moon" cx="0.4" cy="0.38">
    <stop offset="0" stop-color="#ff6a5c"/><stop offset="0.55" stop-color="{RED}"/><stop offset="1" stop-color="#5a0508"/>
  </radialGradient>
  <filter id="glow" x="-20%" y="-40%" width="140%" height="180%">
    <feGaussianBlur stdDeviation="6" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
  </filter>
  <linearGradient id="title" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#ffffff"/><stop offset="0.6" stop-color="#f1dede"/><stop offset="1" stop-color="#b9a2a4"/>
  </linearGradient>
  <clipPath id="c"><rect width="{W}" height="{h}" rx="10"/></clipPath>
</defs>
<g clip-path="url(#c)">
  <rect width="{W}" height="{h}" fill="url(#sky)"/>
  <circle cx="680" cy="118" r="120" fill="url(#moonGlow)">
    <animate attributeName="r" values="112;128;112" dur="5s" repeatCount="indefinite"/>
  </circle>
  <circle cx="680" cy="118" r="70" fill="url(#moon)"/>
  <circle cx="660" cy="100" r="9" fill="#8a0a0f" opacity="0.5"/><circle cx="702" cy="138" r="14" fill="#8a0a0f" opacity="0.4"/><circle cx="690" cy="92" r="5" fill="#8a0a0f" opacity="0.5"/>
  {skyline(W, sky_base, 70, seed=21, fill="#2a0306")}
  {skyline(W, sky_base, 110, seed=5, fill="#050304")}
  {windows(W, sky_base, 90, seed=9, count=34)}
  {rain(W, h, seed=4, count=70)}
  <text x="34" y="34" class="mono" fill="{MUTED}" font-size="11" letter-spacing="2">{esc(LINHA_TOPO)}</text>
  <circle cx="{W - 92}" cy="30" r="4" fill="{RED_HOT}"><animate attributeName="opacity" values="1;0.15;1" dur="1.4s" repeatCount="indefinite"/></circle>
  <text x="{W - 34}" y="34" class="mono" text-anchor="end" fill="{MUTED}" font-size="11" letter-spacing="2">ONLINE</text>
  <text x="40" y="150" class="pirata" font-size="84" fill="{RED}" opacity="0.65" filter="url(#glow)">{esc(NOME)}</text>
  <text x="40" y="150" class="pirata" font-size="84" fill="url(#title)">{esc(NOME)}</text>
  <rect x="42" y="170" width="430" height="2" fill="{RED_HOT}"><animate attributeName="width" from="0" to="430" dur="1.6s"/></rect>
  <text x="42" y="196" class="oswald" font-size="13" letter-spacing="3.5" fill="{TEXT}">{esc(SUBTITULO)}</text>
  <rect x="1" y="1" width="{W - 2}" height="{h - 2}" rx="10" fill="none" stroke="{LINE}" stroke-width="2"/>
  <path d="M16 16 h22 M16 16 v22 M{W - 16} 16 h-22 M{W - 16} 16 v22 M16 {h - 16} h22 M16 {h - 16} v-22 M{W - 16} {h - 16} h-22 M{W - 16} {h - 16} v-22" stroke="{RED}" stroke-width="2" fill="none"/>
</g>"""
    css = ".pirata{font-family:'Pirata',serif}.oswald{font-family:'Oswald',sans-serif}.mono{font-family:'Mono',monospace}"
    return svg(W, h, body, ["Pirata", "Oswald", "Mono"], css)


def secao(num, nome, tag):
    h = 56
    body = f"""
<rect x="1" y="1" width="{W - 2}" height="{h - 2}" rx="6" fill="{PANEL}" stroke="{LINE}"/>
<rect x="14" y="14" width="3" height="28" fill="{RED}"/>
<text x="30" y="34" class="mono" font-size="13" fill="{RED}">{num}</text>
<text x="56" y="34" class="mono" font-size="13" fill="{MUTED}">//</text>
<text x="84" y="36" class="oswald" font-size="21" letter-spacing="3" fill="{TEXT}">{esc(nome)}</text>
<line x1="{110 + len(nome) * 15}" y1="28" x2="{W - 170}" y2="28" stroke="{RED_DARK}"/>
<rect x="{106 + len(nome) * 15}" y="25" width="6" height="6" fill="{RED_HOT}" transform="rotate(45 {109 + len(nome) * 15} 28)"/>
<rect x="{110 + len(nome) * 15}" y="27" width="40" height="2" fill="{RED_HOT}">
  <animate attributeName="x" values="{110 + len(nome) * 15};{W - 210};{110 + len(nome) * 15}" dur="6s" repeatCount="indefinite"/>
</rect>
<text x="{W - 22}" y="33" text-anchor="end" class="mono" font-size="10" letter-spacing="2" fill="{MUTED}">{tag}</text>"""
    css = ".oswald{font-family:'Oswald',sans-serif}.mono{font-family:'Mono',monospace}"
    return svg(W, h, body, ["Oswald", "Mono"], css)


def faixa(texto):
    h = 74
    body = f"""
<defs><filter id="g" x="-10%" y="-50%" width="120%" height="200%"><feGaussianBlur stdDeviation="4" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
<linearGradient id="l" x1="0" x2="1"><stop offset="0" stop-color="{RED}" stop-opacity="0"/><stop offset="1" stop-color="{RED}"/></linearGradient>
<linearGradient id="r" x1="1" x2="0"><stop offset="0" stop-color="{RED}" stop-opacity="0"/><stop offset="1" stop-color="{RED}"/></linearGradient></defs>
<rect x="1" y="1" width="{W - 2}" height="{h - 2}" rx="6" fill="#060508" stroke="{LINE}"/>
<line x1="40" y1="37" x2="230" y2="37" stroke="url(#l)"/><line x1="{W - 230}" y1="37" x2="{W - 40}" y2="37" stroke="url(#r)"/>
<rect x="232" y="34" width="6" height="6" fill="{RED_HOT}" transform="rotate(45 235 37)"/>
<rect x="{W - 238}" y="34" width="6" height="6" fill="{RED_HOT}" transform="rotate(45 {W - 235} 37)"/>
<text x="{W / 2}" y="48" text-anchor="middle" class="p" font-size="32" fill="{RED}" opacity="0.5" filter="url(#g)">{esc(texto)}</text>
<text x="{W / 2}" y="48" text-anchor="middle" class="p" font-size="32" fill="{TEXT}">{esc(texto)}</text>"""
    return svg(W, h, body, ["Pirata"], ".p{font-family:'Pirata',serif}")


def divisor():
    h = 24
    body = f"""<line x1="40" y1="12" x2="{W / 2 - 24}" y2="12" stroke="{LINE}"/><line x1="{W / 2 + 24}" y1="12" x2="{W - 40}" y2="12" stroke="{LINE}"/>
<rect x="{W / 2 - 5}" y="7" width="10" height="10" fill="none" stroke="{RED_HOT}" transform="rotate(45 {W / 2} 12)"/>
<circle cx="{W / 2 - 16}" cy="12" r="2" fill="{MUTED}"/><circle cx="{W / 2 + 16}" cy="12" r="2" fill="{MUTED}"/>"""
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{h}" viewBox="0 0 {W} {h}">{body}</svg>'


def rodape():
    h = 110
    body = f"""
<defs><linearGradient id="f" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{BG2}"/><stop offset="1" stop-color="#5a070c"/></linearGradient>
<clipPath id="c"><rect width="{W}" height="{h}" rx="8"/></clipPath></defs>
<g clip-path="url(#c)">
<rect width="{W}" height="{h}" fill="url(#f)"/>
{skyline(W, h, 60, seed=33, fill="#050304")}
{windows(W, h, 50, seed=12, count=20)}
<text x="{W / 2}" y="34" text-anchor="middle" class="m" font-size="11" letter-spacing="5" fill="{MUTED}">CONTINUE?  ·  A MISSÃO NUNCA TERMINA  ·  ▶</text>
<text x="{W / 2}" y="34" text-anchor="middle" class="m" font-size="11" letter-spacing="5" fill="{RED_HOT}" opacity="0">CONTINUE?  ·  A MISSÃO NUNCA TERMINA  ·  ▶<animate attributeName="opacity" values="0;0.8;0" dur="2.4s" repeatCount="indefinite"/></text>
</g>"""
    return svg(W, h, body, ["Mono"], ".m{font-family:'Mono',monospace}")


def main():
    files = {"header.svg": header(), "divider.svg": divisor(), "footer.svg": rodape()}
    for num, nome, tag in SECOES:
        files[f"section-{num}.svg"] = secao(num, nome, tag)
    for nome, texto in FAIXAS.items():
        files[f"{nome}.svg"] = faixa(texto)
    for nome, conteudo in files.items():
        (OUT / nome).write_text(conteudo, encoding="utf-8")
        print("ok", nome)


if __name__ == "__main__":
    main()
