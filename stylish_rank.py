"""Gera assets/stylish-rank.svg com seus dados do GitHub.

Roda sozinho pela GitHub Action (.github/workflows/stylish-rank.yml) todo dia.
Precisa da variável de ambiente GITHUB_TOKEN. Sem token, gera o card zerado.
"""
import datetime as dt
import json
import os
import urllib.request

from svgkit import LINE, MUTED, PANEL, RED, RED_DARK, RED_HOT, ROOT, TEXT, esc, font_css

USER = os.environ.get("GH_USER", "pedropacheico")
OUT = ROOT / "assets" / "stylish-rank.svg"

# (contribuições no último ano, letra, nome do rank)
RANKS = [
    (0, "D", "Despertar"),
    (50, "C", "Caçador"),
    (120, "B", "Brutal"),
    (250, "A", "Apocalíptico"),
    (450, "S", "Selvagem"),
    (700, "SS", "Sanguinário"),
    (1000, "SSS", "Supremo"),
]

QUERY = """
query($login: String!) {
  user(login: $login) {
    followers { totalCount }
    contributionsCollection {
      totalCommitContributions
      contributionCalendar { totalContributions weeks { contributionDays { contributionCount date } } }
    }
    repositories(ownerAffiliations: OWNER, isFork: false, privacy: PUBLIC, first: 100) {
      totalCount
      nodes { stargazerCount languages(first: 10, orderBy: {field: SIZE, direction: DESC}) { edges { size node { name } } } }
    }
  }
}"""


def fetch():
    token = os.environ.get("GITHUB_TOKEN")
    if not token:
        return None
    req = urllib.request.Request(
        "https://api.github.com/graphql",
        data=json.dumps({"query": QUERY, "variables": {"login": USER}}).encode(),
        headers={"Authorization": f"bearer {token}", "Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)["data"]["user"]


def resumir(u):
    if not u:
        return dict(total=0, commits=0, streak=0, best=0, repos=0, stars=0, followers=0, langs=[])
    cal = u["contributionsCollection"]["contributionCalendar"]
    days = [d for w in cal["weeks"] for d in w["contributionDays"]]
    hoje = dt.date.today().isoformat()
    days = [d for d in days if d["date"] <= hoje]
    best = run = 0
    for d in days:
        run = run + 1 if d["contributionCount"] else 0
        best = max(best, run)
    streak = 0
    for i, d in enumerate(reversed(days)):
        if d["contributionCount"]:
            streak += 1
        elif i == 0:  # hoje ainda sem commit não quebra a sequência
            continue
        else:
            break
    sizes = {}
    repos = u["repositories"]["nodes"]
    for r in repos:
        for e in r["languages"]["edges"]:
            sizes[e["node"]["name"]] = sizes.get(e["node"]["name"], 0) + e["size"]
    total_size = sum(sizes.values()) or 1
    langs = sorted(sizes.items(), key=lambda kv: -kv[1])[:5]
    return dict(
        total=cal["totalContributions"],
        commits=u["contributionsCollection"]["totalCommitContributions"],
        streak=streak,
        best=best,
        repos=u["repositories"]["totalCount"],
        stars=sum(r["stargazerCount"] for r in repos),
        followers=u["followers"]["totalCount"],
        langs=[(n, s / total_size * 100) for n, s in langs],
    )


def rank_de(total):
    atual = RANKS[0]
    prox = None
    for i, r in enumerate(RANKS):
        if total >= r[0]:
            atual = r
            prox = RANKS[i + 1] if i + 1 < len(RANKS) else None
    if prox:
        prog = (total - atual[0]) / (prox[0] - atual[0])
    else:
        prog = 1.0
    return atual, prox, max(0.0, min(1.0, prog))


def render(s):
    W, H = 850, 250
    (_, letra, nome), prox, prog = rank_de(s["total"])
    tam = {1: 120, 2: 92, 3: 70}[len(letra)]
    falta = f"PRÓXIMO: {prox[1]} EM {prox[0] - s['total']}" if prox else "RANK MÁXIMO"

    stats = [
        ("CONTRIBUIÇÕES", s["total"]), ("COMMITS", s["commits"]), ("COMBO ATUAL", f"{s['streak']}d"),
        ("MAIOR COMBO", f"{s['best']}d"), ("REPOS", s["repos"]), ("ESTRELAS", s["stars"]),
    ]
    cells = []
    for i, (lbl, val) in enumerate(stats):
        x = 250 + (i % 3) * 112
        y = 78 + (i // 3) * 74
        cor = RED_HOT if lbl.startswith("COMBO") else TEXT
        cells.append(
            f'<text x="{x}" y="{y}" class="m" font-size="8.5" letter-spacing="1.2" fill="{MUTED}">{lbl}</text>'
            f'<text x="{x}" y="{y + 36}" class="o" font-size="32" fill="{cor}">{esc(val)}</text>'
        )

    bars = []
    if s["langs"]:
        for i, (n, pct) in enumerate(s["langs"]):
            y = 80 + i * 32
            cor = RED_HOT if i == 0 else ("#e8dede" if i == 1 else "#7d7276")
            bars.append(
                f'<text x="600" y="{y}" class="m" font-size="11" fill="{TEXT}">{esc(n)}</text>'
                f'<text x="820" y="{y}" class="m" font-size="10" text-anchor="end" fill="{MUTED}">{pct:.1f}%</text>'
                f'<rect x="600" y="{y + 7}" width="220" height="3" fill="#1d1a1f"/>'
                f'<rect x="600" y="{y + 7}" width="{220 * pct / 100:.1f}" height="3" fill="{cor}"><animate attributeName="width" from="0" to="{220 * pct / 100:.1f}" dur="1.2s"/></rect>'
            )
    else:
        bars.append(f'<text x="600" y="100" class="m" font-size="11" fill="{MUTED}">Aguardando dados…</text>')

    atualizado = dt.datetime.now(dt.timezone.utc).strftime("%d/%m/%Y")
    body = f"""
<defs><filter id="g" x="-30%" y="-30%" width="160%" height="160%"><feGaussianBlur stdDeviation="7" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
<linearGradient id="rk" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#ff5a50"/><stop offset="1" stop-color="{RED_DARK}"/></linearGradient></defs>
<rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="8" fill="{PANEL}" stroke="{LINE}"/>
<path d="M14 14 h18 M14 14 v18 M{W - 14} {H - 14} h-18 M{W - 14} {H - 14} v-18" stroke="{RED}" stroke-width="2" fill="none"/>
<text x="30" y="40" class="m" font-size="10" letter-spacing="3" fill="{MUTED}">STYLISH RANK // @{esc(USER)}</text>
<g filter="url(#g)">
  <text x="120" y="{150 + tam * 0.18:.0f}" text-anchor="middle" class="p" font-size="{tam}" fill="url(#rk)">{letra}
    <animate attributeName="opacity" values="1;0.75;1" dur="2.2s" repeatCount="indefinite"/></text>
</g>
<text x="120" y="194" text-anchor="middle" class="p" font-size="24" fill="{TEXT}">{esc(nome)}</text>
<rect x="40" y="208" width="160" height="4" fill="#1d1a1f"/>
<rect x="40" y="208" width="{160 * prog:.1f}" height="4" fill="{RED_HOT}"><animate attributeName="width" from="0" to="{160 * prog:.1f}" dur="1.5s"/></rect>
<text x="120" y="228" text-anchor="middle" class="m" font-size="8.5" letter-spacing="1.5" fill="{MUTED}">{falta}</text>
<line x1="230" y1="58" x2="230" y2="222" stroke="{LINE}"/>
{''.join(cells)}
<line x1="580" y1="58" x2="580" y2="222" stroke="{LINE}"/>
<text x="600" y="40" class="m" font-size="9" letter-spacing="2" fill="{MUTED}">ARMAS MAIS USADAS</text>
{''.join(bars)}
<text x="250" y="232" class="m" font-size="8" letter-spacing="2" fill="#4d4448">DADOS DOS ÚLTIMOS 12 MESES</text>
<text x="{W - 40}" y="240" text-anchor="end" class="m" font-size="8" letter-spacing="1.5" fill="#4d4448">ATUALIZADO {atualizado}</text>"""
    css = ".p{font-family:'Pirata',serif}.o{font-family:'Oswald',sans-serif}.m{font-family:'Mono',monospace}"
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">'
        f"<style>{font_css('Pirata', 'Oswald', 'Mono')}{css}</style>{body}</svg>"
    )


if __name__ == "__main__":
    OUT.write_text(render(resumir(fetch())), encoding="utf-8")
    print("ok", OUT.name)
