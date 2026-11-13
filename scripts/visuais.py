"""Gera os SVGs animados do perfil do Emanuel (tema hacker verde).

Uso: python scripts/visuais.py   (grava em assets/)
Para mudar textos, edite as listas no final do arquivo e rode de novo.
"""
import math
import os
import random
from xml.sax.saxutils import escape

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets")
os.makedirs(os.path.join(OUT, "projetos"), exist_ok=True)
random.seed(1337)

G = "#00ff41"       # verde neon
G2 = "#00c832"      # verde médio
G3 = "#0a7a2a"      # verde escuro
DIM = "#3ddc6a"     # verde para detalhes
SOFT = "#c4ffd3"    # texto claro
TBG = "#001a0c"     # fundo sólido das janelas
MONO = "'Courier New', Courier, monospace"
BOLD = "Consolas, 'SF Mono', Menlo, 'DejaVu Sans Mono', 'Courier New', monospace"
CW = 0.6            # largura do caractere (em) da fonte mono


def save(name, svg):
    with open(os.path.join(OUT, name), "w", encoding="utf-8") as f:
        f.write(svg)
    print("ok", name)


def defs(W, H, R):
    """Gradiente verde, grade, scanlines, brilho e recorte arredondado."""
    return f"""
  <radialGradient id="bgg" cx="50%" cy="35%" r="80%">
    <stop offset="0" stop-color="#005c25"/>
    <stop offset=".5" stop-color="#002a11"/>
    <stop offset="1" stop-color="#000f06"/>
  </radialGradient>
  <pattern id="grid" width="22" height="22" patternUnits="userSpaceOnUse">
    <path d="M22 0H0V22" fill="none" stroke="{G}" stroke-opacity=".08"/>
  </pattern>
  <pattern id="lines" width="3" height="3" patternUnits="userSpaceOnUse">
    <rect width="3" height="1" fill="#000" fill-opacity=".22"/>
  </pattern>
  <linearGradient id="scan" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="{G}" stop-opacity="0"/>
    <stop offset=".5" stop-color="{G}" stop-opacity=".09"/>
    <stop offset="1" stop-color="{G}" stop-opacity="0"/>
  </linearGradient>
  <filter id="glow" x="-30%" y="-60%" width="160%" height="220%">
    <feGaussianBlur stdDeviation="3" result="b"/>
    <feMerge><feMergeNode in="b"/><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
  </filter>
  <filter id="glowS" x="-30%" y="-60%" width="160%" height="220%">
    <feGaussianBlur stdDeviation="1.5" result="b"/>
    <feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
  </filter>
  <clipPath id="round"><rect width="{W}" height="{H}" rx="{R}"/></clipPath>"""


def base_css(W, H, R):
    per = 2 * (W + H)
    return f"""
  text {{ font-family: {MONO}; }}
  .b {{ font-family: {BOLD}; font-weight: 700; }}
  .blink {{ animation: blink 1s steps(1) infinite; }}
  @keyframes blink {{ 50% {{ opacity: 0; }} }}
  .scanbar {{ animation: scan 7s linear infinite; }}
  @keyframes scan {{ from {{ transform: translateY(-120px); }} to {{ transform: translateY({H}px); }} }}
  .run {{ animation: run 6s linear infinite; }}
  @keyframes run {{ to {{ stroke-dashoffset: -{per}; }} }}
  .spin {{ transform-box: fill-box; transform-origin: center; animation: spin 8s linear infinite; }}
  .spinr {{ transform-box: fill-box; transform-origin: center; animation: spin 5s linear infinite reverse; }}
  @keyframes spin {{ to {{ transform: rotate(360deg); }} }}
  .show {{ opacity: 0; animation: appear .2s ease-out forwards; }}
  @keyframes appear {{ to {{ opacity: 1; }} }}"""


def frame(W, H, R, lw=2):
    """Borda neon com um ponto de luz que corre em volta."""
    per = 2 * (W + H)
    return (
        f'<rect x="1" y="1" width="{W-2}" height="{H-2}" rx="{R-1}" fill="none" stroke="{G}" stroke-opacity=".45" stroke-width="{lw}"/>'
        f'<rect class="run" x="1" y="1" width="{W-2}" height="{H-2}" rx="{R-1}" fill="none" stroke="{G}" stroke-width="{lw+1}" '
        f'stroke-dasharray="140 {per - 140}" filter="url(#glowS)"/>'
    )


def bg(W, H):
    return f'<rect width="{W}" height="{H}" fill="url(#bgg)"/><rect width="{W}" height="{H}" fill="url(#grid)"/>'


def overlay(W, H):
    return f'<rect class="scanbar" width="{W}" height="120" fill="url(#scan)"/><rect width="{W}" height="{H}" fill="url(#lines)"/>'


def svg_open(W, H, label, extra_defs="", css=""):
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="{escape(label)}">'
        f"<defs>{defs(W, H, 14)}{extra_defs}</defs><style>{base_css(W, H, 14)}{css}</style>"
    )


# ===================================================================== banner
NOME = "EMANUEL FELIPE"
SUBTITULO = "> Eng. de Software & Cyber Segurança"
TROFEU = "1º LUGAR · SELETIVA WORLDSKILLS · MOBILE"


def trophy(cx, cy, s=1.0, cls=""):
    """Troféu desenhado em linhas (cx, cy = centro da taça)."""
    return f"""<g class="{cls}" transform="translate({cx} {cy}) scale({s})">
    <path d="M-14 -16 H14 V-4 Q14 12 0 14 Q-14 12 -14 -4 Z" fill="{G}" fill-opacity=".25" stroke="{G}" stroke-width="2.5"/>
    <path d="M-14 -11 H-21 Q-22 2 -12 4 M14 -11 H21 Q22 2 12 4" fill="none" stroke="{G}" stroke-width="2.5"/>
    <path d="M0 14 V21 M-9 25 H9 V21 H-9 Z" fill="{G}" stroke="{G}" stroke-width="2"/>
    <text x="0" y="3" font-size="13" font-weight="700" fill="{G}" text-anchor="middle">1</text>
  </g>"""


def banner():
    W, H, R = 1000, 380, 14
    n = 34
    step = W / n
    cols = []
    for i in range(n):
        x = step * i + step / 2
        length = random.randint(10, 20)
        dur = random.uniform(5, 11)
        delay = -random.uniform(0, dur)
        size = random.choice([14, 16, 18])
        tsp = "".join(
            f'<tspan x="{x:.0f}" dy="{size + 4}" fill="{"#eafff0" if k == length - 1 else G}" fill-opacity="{(k + 1) / length:.2f}">{random.choice("01")}</tspan>'
            for k in range(length)
        )
        cols.append(
            f'<g class="rain" style="animation-duration:{dur:.2f}s;animation-delay:{delay:.2f}s"><text font-size="{size}" text-anchor="middle">{tsp}</text></g>'
        )
    sub = SUBTITULO
    fs = 28
    cw = fs * CW
    tw = len(sub) * cw
    sx = (W - tw) / 2
    binary = " ".join(format(ord(c), "08b") for c in "EMANUEL")
    tf = 16
    ttw = len(TROFEU) * tf * CW
    pill_w = ttw + 70
    px = (W - pill_w) / 2
    css = f"""
  .rain {{ animation-name: fall; animation-timing-function: linear; animation-iteration-count: infinite; }}
  @keyframes fall {{ from {{ transform: translateY(-460px); }} to {{ transform: translateY({H + 20}px); }} }}
  .g1 {{ animation: glitch1 5s steps(1) infinite; }}
  .g2 {{ animation: glitch2 5s steps(1) infinite; }}
  @keyframes glitch1 {{ 0%,91%,100% {{ opacity:0; transform:translate(0,0); }} 92% {{ opacity:.9; transform:translate(-5px,1px); }} 94% {{ opacity:.9; transform:translate(4px,-2px); }} 96% {{ opacity:0; }} }}
  @keyframes glitch2 {{ 0%,92%,100% {{ opacity:0; transform:translate(0,0); }} 93% {{ opacity:.8; transform:translate(5px,2px); }} 95% {{ opacity:.8; transform:translate(-3px,-1px); }} 97% {{ opacity:0; }} }}
  .flick {{ animation: flick 5s steps(1) infinite; }}
  @keyframes flick {{ 0%,91%,97%,100% {{ opacity:1; }} 92%,94% {{ opacity:.35; }} 93%,95% {{ opacity:.85; }} }}
  .type {{ animation: type 9s infinite; }}
  @keyframes type {{
    0% {{ transform: translateX(0); animation-timing-function: steps({len(sub)}); }}
    45% {{ transform: translateX({tw:.1f}px); animation-timing-function: linear; }}
    85% {{ transform: translateX({tw:.1f}px); animation-timing-function: steps({len(sub)}); }}
    100% {{ transform: translateX(0); }}
  }}
  .shine {{ animation: shine 3s ease-in-out infinite; }}
  @keyframes shine {{ 0%,100% {{ transform: translateX(-120px); }} 60% {{ transform: translateX({pill_w + 40:.0f}px); }} }}
  .glowp {{ animation: glowp 2s ease-in-out infinite; }}
  @keyframes glowp {{ 50% {{ stroke-opacity: .35; }} }}"""
    PB = "#00150a"
    svg = svg_open(W, H, f"{NOME.title()} - Engenharia de Software e Cyber Segurança. {TROFEU}", css=css) + f"""
<defs>
  <linearGradient id="shineg" x1="0" x2="1"><stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset=".5" stop-color="#eafff0" stop-opacity=".35"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>
  <clipPath id="pillclip"><rect x="{px:.1f}" y="262" width="{pill_w:.1f}" height="40" rx="20"/></clipPath>
</defs>
<g clip-path="url(#round)">
  {bg(W, H)}
  <g opacity=".75">{''.join(cols)}</g>
  <rect x="110" y="84" width="780" height="236" rx="8" fill="{PB}" fill-opacity=".97" stroke="{G}" stroke-opacity=".6"/>
  <path d="M110 108 V84 H134 M866 84 H890 V108 M890 296 V320 H866 M134 320 H110 V296" fill="none" stroke="{G}" stroke-width="3" filter="url(#glowS)"/>
  <text x="132" y="109" font-size="13" fill="{DIM}">// root@itumbiara:~# ./apresentar.sh</text>
  <g class="flick">
    <text class="b g1" x="{W/2}" y="176" font-size="62" letter-spacing="4" text-anchor="middle" fill="#9dffb6">{NOME}</text>
    <text class="b g2" x="{W/2}" y="176" font-size="62" letter-spacing="4" text-anchor="middle" fill="{G3}">{NOME}</text>
    <text class="b" x="{W/2}" y="176" font-size="62" letter-spacing="4" text-anchor="middle" fill="{G}" filter="url(#glow)">{NOME}</text>
  </g>
  <text x="{sx:.1f}" y="226" font-size="{fs}" fill="{SOFT}" textLength="{tw:.1f}" lengthAdjust="spacingAndGlyphs">{escape(sub)}</text>
  <g class="type">
    <rect x="{sx:.1f}" y="200" width="{tw + 4:.1f}" height="34" fill="{PB}"/>
    <rect class="blink" x="{sx + 1:.1f}" y="204" width="{cw - 2:.1f}" height="28" fill="{G}"/>
  </g>
  <rect class="glowp" x="{px:.1f}" y="262" width="{pill_w:.1f}" height="40" rx="20" fill="{G}" fill-opacity=".14" stroke="{G}" stroke-width="2" filter="url(#glowS)"/>
  {trophy(px + 30, 280, 0.72)}
  <text class="b" x="{px + 54:.1f}" y="288" font-size="{tf}" fill="{G}" textLength="{ttw:.1f}" lengthAdjust="spacingAndGlyphs">{escape(TROFEU)}</text>
  <g clip-path="url(#pillclip)"><rect class="shine" x="{px:.1f}" y="262" width="80" height="40" fill="url(#shineg)" transform="skewX(-20)"/></g>
  <rect x="20" y="20" width="238" height="26" rx="5" fill="{PB}" stroke="{G}" stroke-opacity=".5"/>
  <text x="32" y="38" font-size="14" fill="{G}">[ root@itumbiara-go ]</text>
  <rect x="{W-186}" y="20" width="166" height="26" rx="5" fill="{PB}" stroke="{G}" stroke-opacity=".5"/>
  <circle class="blink" cx="{W-168}" cy="33" r="5" fill="{G}" filter="url(#glowS)"/>
  <text x="{W-154}" y="38" font-size="14" fill="{G}">OPEN TO WORK</text>
  <rect x="{W/2 - 320}" y="{H-44}" width="640" height="26" rx="5" fill="{PB}" stroke="{G}" stroke-opacity=".35"/>
  <text x="{W/2}" y="{H-26}" font-size="14" fill="{DIM}" text-anchor="middle" letter-spacing="1">{binary}</text>
  {overlay(W, H)}
</g>
{frame(W, H, R, 2)}
</svg>"""
    save("banner.svg", svg)



# ===================================================================== divisor
def divider():
    W, H = 1000, 34
    chunk = "".join(random.choice("01") for _ in range(160))
    fs = 14
    tw = len(chunk) * fs * CW
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="divisor">
<defs>
  <linearGradient id="edge" x1="0" x2="1">
    <stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset=".12" stop-color="#fff"/>
    <stop offset=".88" stop-color="#fff"/><stop offset="1" stop-color="#fff" stop-opacity="0"/>
  </linearGradient>
  <mask id="m"><rect width="{W}" height="{H}" fill="url(#edge)"/></mask>
</defs>
<style>
  text {{ font-family: {MONO}; }}
  .s {{ animation: slide 30s linear infinite; }}
  @keyframes slide {{ to {{ transform: translateX(-{tw:.1f}px); }} }}
</style>
<g mask="url(#m)">
  <rect x="0" y="4" width="{W}" height="{H-8}" fill="#003314"/>
  <line x1="0" y1="4" x2="{W}" y2="4" stroke="{G}" stroke-opacity=".7"/>
  <line x1="0" y1="{H-4}" x2="{W}" y2="{H-4}" stroke="{G}" stroke-opacity=".7"/>
  <g class="s">
    <text x="0" y="22" font-size="{fs}" fill="{G}" textLength="{tw:.1f}" lengthAdjust="spacingAndGlyphs">{chunk}</text>
    <text x="{tw:.1f}" y="22" font-size="{fs}" fill="{G}" textLength="{tw:.1f}" lengthAdjust="spacingAndGlyphs">{chunk}</text>
  </g>
</g>
</svg>"""
    save("divider.svg", svg)


# ===================================================================== títulos
def heading(fname, label, num):
    W, H, R = 640, 64, 12
    fs = 28
    cw = fs * CW
    full = f"> {label}"
    tw = len(full) * cw
    x = 30
    svg = svg_open(W, H, label) + f"""
<g clip-path="url(#round)">
  {bg(W, H)}
  <rect x="0" y="0" width="7" height="{H}" fill="{G}" filter="url(#glowS)"/>
  <text class="b" x="{x}" y="42" font-size="{fs}" fill="{G}" filter="url(#glowS)" textLength="{tw:.1f}" lengthAdjust="spacingAndGlyphs">{escape(full)}</text>
  <rect class="blink" x="{x + tw + 6:.1f}" y="20" width="{cw - 2:.1f}" height="26" fill="{G}"/>
  <text x="{W - 20}" y="39" font-size="14" fill="{DIM}" text-anchor="end">[ 0{num} ]</text>
  {overlay(W, H)}
</g>
{frame(W, H, R, 2)}
</svg>"""
    save(fname, svg)


# ===================================================================== terminal
def terminal(lines):
    W, R = 620, 14
    fs, lh, top, left = 18, 30, 76, 26
    cw = fs * CW
    H = top + lh * (len(lines) - 1) + 40
    body, css = [], []
    t = 0.6
    for i, (kind, txt) in enumerate(lines):
        y = top + i * lh
        if kind in ("cmd", "end"):
            body.append(f'<text x="{left}" y="{y}" font-size="{fs}" fill="{G}" font-weight="700">$</text>')
            cx = left + 2 * cw
            if kind == "end":
                body.append(f'<g class="show" style="animation-delay:{t:.2f}s"><rect class="blink" x="{cx:.1f}" y="{y - fs + 3}" width="{cw:.1f}" height="{fs + 2}" fill="{G}"/></g>')
                break
            tw = len(txt) * cw
            dur = len(txt) * 0.055
            k = f"k{i}"
            css.append(f"@keyframes {k} {{ to {{ transform: translateX({tw + cw:.1f}px); }} }}")
            body.append(f'<text x="{cx:.1f}" y="{y}" font-size="{fs}" fill="#eafff0" textLength="{tw:.1f}" lengthAdjust="spacingAndGlyphs">{escape(txt)}</text>')
            body.append(f'<rect style="animation:{k} {dur:.2f}s steps({len(txt)}) {t:.2f}s forwards" x="{cx - 1:.1f}" y="{y - fs}" width="{tw + cw + 4:.1f}" height="{fs + 8}" fill="{TBG}"/>')
            body.append(f'<rect class="cur" style="animation:{k} {dur:.2f}s steps({len(txt)}) {t:.2f}s forwards, on {dur + 0.25:.2f}s linear {t:.2f}s" x="{cx:.1f}" y="{y - fs + 3}" width="{cw:.1f}" height="{fs + 2}" fill="{G}"/>')
            t += dur + 0.35
        else:
            color = G if kind == "hi" else SOFT
            body.append(f'<text class="show" xml:space="preserve" style="animation-delay:{t:.2f}s" x="{left + 2 * cw:.1f}" y="{y}" font-size="{fs}" fill="{color}">{escape(txt)}</text>')
            t += 0.18
            if i + 1 < len(lines) and lines[i + 1][0] in ("cmd", "end"):
                t += 0.45
    css.append(".cur { opacity: 0; } @keyframes on { from { opacity: 1; } to { opacity: 1; } }")
    label = "Terminal: " + " ".join(t for k, t in lines if k in ("out", "hi"))
    svg = svg_open(W, H, label, css="".join(css)) + f"""
<g clip-path="url(#round)">
  <rect width="{W}" height="{H}" fill="{TBG}"/>
  <rect width="{W}" height="40" fill="#003a17"/>
  <line x1="0" y1="40" x2="{W}" y2="40" stroke="{G}" stroke-opacity=".5"/>
  <circle cx="22" cy="20" r="6" fill="{G}"/><circle cx="42" cy="20" r="6" fill="{G2}"/><circle cx="62" cy="20" r="6" fill="{G3}"/>
  <text x="{W/2}" y="25" font-size="14" fill="{DIM}" text-anchor="middle">emanuel@itumbiara: ~</text>
  {''.join(body)}
  <rect y="40" width="{W}" height="{H}" fill="url(#grid)"/>
  {overlay(W, H)}
</g>
{frame(W, H, R, 2)}
</svg>"""
    save("terminal.svg", svg)


# ===================================================================== ícones
def icon_drone(cx, cy):
    rot = "".join(
        f'<ellipse class="rotor" style="animation-delay:-{d}s" cx="{cx + dx}" cy="{cy - 20}" rx="22" ry="3" fill="{G}" fill-opacity=".5" stroke="{G}"/>'
        for dx, d in ((-55, 0), (55, 0.1))
    )
    crops = "".join(
        f'<path d="M{x} 140 v-8 M{x} 136 l-4 -4 M{x} 136 l4 -4" stroke="{G2}" stroke-width="1.5" fill="none"/>'
        for x in range(cx - 95, cx + 100, 19)
    )
    return f"""
  <g class="hover">
    <path d="M{cx-14} {cy+16} L{cx+14} {cy+16} L{cx+52} {cy+56} L{cx-52} {cy+56} Z" fill="url(#beam)" class="beamp"/>
    <g fill="none" stroke="{G}" stroke-width="2.5" filter="url(#glowS)">
      <path d="M{cx-22} {cy-4} H{cx-55} V{cy-18} M{cx+22} {cy-4} H{cx+55} V{cy-18}"/>
      <rect x="{cx-24}" y="{cy-14}" width="48" height="26" rx="8" fill="{TBG}"/>
      <circle cx="{cx}" cy="{cy+16}" r="6" fill="{TBG}"/>
      <path d="M{cx-18} {cy+12} l-8 10 M{cx+18} {cy+12} l8 10"/>
    </g>
    <circle class="blink" cx="{cx}" cy="{cy-2}" r="3" fill="{G}"/>
    {rot}
  </g>
  {crops}"""


def icon_truck(cx, cy):
    wheels = "".join(
        f'<g><circle cx="{x}" cy="{cy+28}" r="10" fill="{TBG}" stroke="{G}" stroke-width="2.5"/>'
        f'<path class="spin" d="M{x-7} {cy+28} H{x+7} M{x} {cy+21} V{cy+35}" stroke="{G}" stroke-width="2"/></g>'
        for x in (cx - 44, cx + 30)
    )
    return f"""
  <line class="road" x1="{cx-110}" y1="{cy+40}" x2="{cx+110}" y2="{cy+40}" stroke="{G2}" stroke-width="2" stroke-dasharray="14 10"/>
  <g class="speed" stroke="{G}" stroke-width="2" stroke-linecap="round">
    <line x1="{cx-108}" y1="{cy-10}" x2="{cx-84}" y2="{cy-10}"/>
    <line x1="{cx-100}" y1="{cy+4}" x2="{cx-80}" y2="{cy+4}"/>
    <line x1="{cx-110}" y1="{cy+18}" x2="{cx-86}" y2="{cy+18}"/>
  </g>
  <g class="bounce">
    <g fill="{TBG}" stroke="{G}" stroke-width="2.5" filter="url(#glowS)">
      <rect x="{cx-70}" y="{cy-26}" width="80" height="50" rx="4"/>
      <path d="M{cx+12} {cy-8} H{cx+38} L{cx+54} {cy+8} V{cy+24} H{cx+12} Z"/>
    </g>
    <path d="M{cx+20} {cy-2} H{cx+36} L{cx+46} {cy+8} H{cx+20} Z" fill="{G}" fill-opacity=".35"/>
    <g fill="none" stroke="{G2}" stroke-width="1.6">
      <rect x="{cx-58}" y="{cy-14}" width="24" height="24"/><path d="M{cx-58} {cy-6} H{cx-34} M{cx-46} {cy-14} V{cy-6}"/>
      <rect x="{cx-28}" y="{cy-14}" width="24" height="24"/><path d="M{cx-28} {cy-6} H{cx-4} M{cx-16} {cy-14} V{cy-6}"/>
    </g>
    {wheels}
  </g>"""


def icon_book(cx, cy):
    def page(sign):
        x2 = cx + sign * 72
        return (f'M{cx} {cy-30} Q{cx + sign * 34} {cy-42} {x2} {cy-34} V{cy+30} '
                f'Q{cx + sign * 34} {cy+22} {cx} {cy+34} Z')
    lines = "".join(
        f'<path d="M{cx + s * 14} {cy - 18 + i * 11} Q{cx + s * 36} {cy - 25 + i * 11} {cx + s * 60} {cy - 21 + i * 11}" stroke="{G2}" stroke-width="1.5" fill="none"/>'
        for s in (-1, 1) for i in range(5)
    )
    bits = "".join(
        f'<text class="rise" style="animation-delay:{d}s" x="{cx + dx}" y="{cy - 30}" font-size="14" fill="{G}" text-anchor="middle">{b}</text>'
        for dx, d, b in ((-40, 0, "1"), (-10, 1.1, "0"), (22, 0.5, "1"), (50, 1.7, "0"), (0, 2.3, "1"))
    )
    return f"""
  {bits}
  <g fill="{TBG}" stroke="{G}" stroke-width="2.5" filter="url(#glowS)">
    <path d="{page(-1)}"/><path d="{page(1)}"/>
  </g>
  {lines}
  <path class="flip" d="{page(1)}" fill="#00331a" stroke="{G}" stroke-width="2"/>
  <line x1="{cx}" y1="{cy-30}" x2="{cx}" y2="{cy+34}" stroke="{G}" stroke-width="3"/>"""


def gear_path(cx, cy, r_out, r_in, teeth):
    pts = []
    for i in range(teeth * 4):
        a = 2 * math.pi * i / (teeth * 4)
        r = r_out if i % 4 in (1, 2) else r_in
        pts.append(f"{cx + r * math.cos(a):.1f},{cy + r * math.sin(a):.1f}")
    return "M" + " L".join(pts) + " Z"


def icon_code(cx, cy):
    return f"""
  <path class="spin" d="{gear_path(cx - 8, cy + 4, 50, 40, 10)}" fill="{TBG}" stroke="{G}" stroke-width="2.5" filter="url(#glowS)"/>
  <circle cx="{cx-8}" cy="{cy+4}" r="28" fill="#00331a" stroke="{G2}" stroke-width="2"/>
  <path class="spinr" d="{gear_path(cx + 44, cy - 40, 22, 16, 7)}" fill="{TBG}" stroke="{G2}" stroke-width="2"/>
  <text class="b" x="{cx-8}" y="{cy+11}" font-size="20" fill="{G}" text-anchor="middle" filter="url(#glowS)">&lt;/&gt;</text>"""


def icon_shield(cx, cy):
    return f"""
  <circle cx="{cx}" cy="{cy}" r="58" fill="none" stroke="{G}" stroke-opacity=".25"/>
  <circle cx="{cx}" cy="{cy}" r="40" fill="none" stroke="{G}" stroke-opacity=".2"/>
  <path class="spin" d="M{cx} {cy} L{cx} {cy-58} A58 58 0 0 1 {cx + 58 * math.sin(math.radians(60)):.1f} {cy - 58 * math.cos(math.radians(60)):.1f} Z" fill="url(#sweep)" style="transform-origin:{cx}px {cy}px;transform-box:view-box;animation-duration:3s"/>
  <circle class="pulse" cx="{cx}" cy="{cy}" r="40" fill="none" stroke="{G}" stroke-width="2"/>
  <path d="M{cx} {cy-44} L{cx+34} {cy-30} V{cy} Q{cx+34} {cy+30} {cx} {cy+46} Q{cx-34} {cy+30} {cx-34} {cy} V{cy-30} Z" fill="{TBG}" stroke="{G}" stroke-width="3" filter="url(#glowS)"/>
  <path class="shackle" d="M{cx-11} {cy-2} V{cy-12} A11 11 0 0 1 {cx+11} {cy-12} V{cy-2}" fill="none" stroke="{G}" stroke-width="3.5"/>
  <rect x="{cx-17}" y="{cy-3}" width="34" height="26" rx="4" fill="{G}"/>
  <circle cx="{cx}" cy="{cy+8}" r="4" fill="{TBG}"/><rect x="{cx-1.5}" y="{cy+9}" width="3" height="8" fill="{TBG}"/>"""


ICON_CSS = f"""
  .hover {{ animation: hover 3s ease-in-out infinite; }}
  @keyframes hover {{ 50% {{ transform: translateY(-6px); }} }}
  .rotor {{ transform-box: fill-box; transform-origin: center; animation: rotor .18s linear infinite; }}
  @keyframes rotor {{ 50% {{ transform: scaleX(.15); }} }}
  .beamp {{ animation: beam 1.6s ease-in-out infinite; }}
  @keyframes beam {{ 50% {{ opacity: .35; }} }}
  .road {{ animation: road .6s linear infinite; }}
  @keyframes road {{ to {{ stroke-dashoffset: 24; }} }}
  .bounce {{ animation: bounce .5s ease-in-out infinite; }}
  @keyframes bounce {{ 50% {{ transform: translateY(-2px); }} }}
  .speed {{ animation: speed .5s steps(2) infinite; }}
  @keyframes speed {{ 50% {{ opacity: .3; transform: translateX(-6px); }} }}
  .rise {{ opacity: 0; animation: rise 2.8s ease-out infinite; }}
  @keyframes rise {{ 0% {{ opacity: 0; transform: translateY(0); }} 20% {{ opacity: 1; }} 100% {{ opacity: 0; transform: translateY(-34px); }} }}
  .pulse {{ transform-box: fill-box; transform-origin: center; animation: pulse 2.4s ease-out infinite; }}
  @keyframes pulse {{ from {{ transform: scale(.8); opacity: .9; }} to {{ transform: scale(1.6); opacity: 0; }} }}
  .shackle {{ animation: lock 3s ease-in-out infinite; }}
  @keyframes lock {{ 0%,60%,100% {{ transform: translateY(0); }} 75% {{ transform: translateY(-5px); }} }}"""

ICON_DEFS = f"""
  <linearGradient id="beam" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="{G}" stop-opacity=".55"/><stop offset="1" stop-color="{G}" stop-opacity="0"/>
  </linearGradient>
  <linearGradient id="sweep" x1="0" y1="1" x2="1" y2="0">
    <stop offset="0" stop-color="{G}" stop-opacity=".05"/><stop offset="1" stop-color="{G}" stop-opacity=".5"/>
  </linearGradient>"""


def icon_phone(cx, cy):
    tiles = "".join(
        f'<rect class="pop" style="animation-delay:{(r * 2 + c) * 0.35:.2f}s" x="{cx - 19 + c * 20}" y="{cy - 30 + r * 20}" width="16" height="16" rx="4" fill="{G}" fill-opacity="{0.9 - 0.15 * ((r + c) % 3):.2f}"/>'
        for r in range(3) for c in range(2)
    )
    waves = "".join(
        f'<path class="wave" style="animation-delay:{i * 0.3:.1f}s" d="M{cx + 40 + i * 9} {cy - 46 - i * 6} a{14 + i * 9} {14 + i * 9} 0 0 1 {10 + i * 6} {12 + i * 6}" fill="none" stroke="{G}" stroke-width="2.5" stroke-linecap="round"/>'
        for i in range(3)
    )
    return f"""
  <rect x="{cx-32}" y="{cy-54}" width="64" height="108" rx="11" fill="{TBG}" stroke="{G}" stroke-width="2.5" filter="url(#glowS)"/>
  <rect x="{cx-25}" y="{cy-42}" width="50" height="80" rx="3" fill="#00331a"/>
  <rect x="{cx-8}" y="{cy-49}" width="16" height="3" rx="1.5" fill="{G2}"/>
  <circle cx="{cx}" cy="{cy+46}" r="3.5" fill="none" stroke="{G2}" stroke-width="1.5"/>
  {tiles}
  {waves}"""


def icon_game(cx, cy):
    cards = "".join(
        f'<g class="flipc" style="animation-delay:{i * 0.6:.1f}s">'
        f'<rect x="{cx - 44 + (i % 2) * 48}" y="{cy - 46 + (i // 2) * 52}" width="40" height="46" rx="6" fill="{TBG}" stroke="{G}" stroke-width="2.2"/>'
        f'<text x="{cx - 24 + (i % 2) * 48}" y="{cy - 16 + (i // 2) * 52}" font-size="22" font-weight="700" fill="{G}" text-anchor="middle">{s}</text></g>'
        for i, s in enumerate("?A?B")
    )
    return f"""
  {cards}
  <text class="rise" x="{cx + 50}" y="{cy - 40}" font-size="14" font-weight="700" fill="{G}">+10</text>
  <text class="rise" style="animation-delay:1.4s" x="{cx - 66}" y="{cy - 30}" font-size="14" font-weight="700" fill="{G}">+10</text>"""


def icon_design(cx, cy):
    handles = "".join(
        f'<rect x="{x - 3}" y="{y - 3}" width="6" height="6" fill="{TBG}" stroke="{G}" stroke-width="1.5"/>'
        for x, y in ((cx - 34, cy - 50), (cx + 34, cy - 50), (cx - 34, cy + 50), (cx + 34, cy + 50))
    )
    return f"""
  <rect x="{cx-34}" y="{cy-50}" width="68" height="100" rx="8" fill="{TBG}" stroke="{G}" stroke-width="2" stroke-dasharray="6 4" class="ants"/>
  <rect x="{cx-24}" y="{cy-38}" width="48" height="20" rx="3" fill="{G}" fill-opacity=".35"/>
  <rect x="{cx-24}" y="{cy-12}" width="30" height="5" rx="2" fill="{G2}"/>
  <rect x="{cx-24}" y="{cy-2}" width="44" height="5" rx="2" fill="{G3}"/>
  <rect x="{cx-24}" y="{cy+8}" width="38" height="5" rx="2" fill="{G3}"/>
  <rect class="pop" x="{cx-24}" y="{cy+24}" width="48" height="14" rx="7" fill="{G}"/>
  {handles}
  <g class="pen">
    <path d="M0 0 L0 22 L6 16 L11 26 L15 24 L10 14 L18 14 Z" fill="{G}" stroke="{TBG}" stroke-width="1.5" transform="translate({cx + 18} {cy - 4})"/>
  </g>"""


def icon_calendar(cx, cy):
    days = "".join(
        f'<rect x="{cx - 42 + c * 22}" y="{cy - 12 + r * 18}" width="16" height="12" rx="2" fill="{G}" fill-opacity=".18"/>'
        for r in range(3) for c in range(4)
    )
    return f"""
  <rect x="{cx-52}" y="{cy-46}" width="104" height="100" rx="8" fill="{TBG}" stroke="{G}" stroke-width="2.5" filter="url(#glowS)"/>
  <rect x="{cx-52}" y="{cy-46}" width="104" height="24" rx="8" fill="{G}" fill-opacity=".35"/>
  <path d="M{cx-28} {cy-56} V{cy-38} M{cx+28} {cy-56} V{cy-38}" stroke="{G}" stroke-width="4" stroke-linecap="round"/>
  <text x="{cx}" y="{cy-29}" font-size="11" font-weight="700" fill="{G}" text-anchor="middle">AGENDA</text>
  {days}
  <rect class="hop" x="{cx-43}" y="{cy-13}" width="18" height="14" rx="3" fill="none" stroke="{G}" stroke-width="2.5" filter="url(#glowS)"/>"""


def icon_article(cx, cy):
    bars = "".join(
        f'<rect class="eq" style="animation-delay:-{random.uniform(0, 1):.2f}s" x="{cx + 12 + i * 8}" y="{cy + 2}" width="5" height="34" rx="2" fill="{G}"/>'
        for i in range(6)
    )
    return f"""
  <rect x="{cx-58}" y="{cy-50}" width="62" height="80" rx="5" fill="{TBG}" stroke="{G}" stroke-width="2.5" filter="url(#glowS)"/>
  <path d="M{cx-48} {cy-36} H{cx-8} M{cx-48} {cy-26} H{cx-14} M{cx-48} {cy-16} H{cx-8} M{cx-48} {cy-6} H{cx-20} M{cx-48} {cy+4} H{cx-12} M{cx-48} {cy+14} H{cx-24}" stroke="{G2}" stroke-width="2"/>
  <circle cx="{cx+34}" cy="{cy-26}" r="18" fill="{TBG}" stroke="{G}" stroke-width="2.5"/>
  <path d="M{cx+28} {cy-35} L{cx+42} {cy-26} L{cx+28} {cy-17} Z" fill="{G}"/>
  {bars}
  <rect x="{cx+8}" y="{cy+38}" width="56" height="3" fill="{G2}"/>
  <circle class="blink" cx="{cx-50}" cy="{cy+44}" r="5" fill="{G}"/>
  <text x="{cx-40}" y="{cy+48}" font-size="11" fill="{G}">REC</text>"""


def icon_tractor(cx, cy):
    def wheel(x, y, r):
        return (f'<circle cx="{x}" cy="{y}" r="{r}" fill="{TBG}" stroke="{G}" stroke-width="2.5"/>'
                f'<path class="spin" style="animation-duration:2s" d="M{x - r + 4} {y} H{x + r - 4} M{x} {y - r + 4} V{y + r - 4}" stroke="{G2}" stroke-width="2"/>'
                f'<circle cx="{x}" cy="{y}" r="3" fill="{G}"/>')
    return f"""
  <line class="road" x1="{cx-110}" y1="{cy+38}" x2="{cx+110}" y2="{cy+38}" stroke="{G2}" stroke-width="2" stroke-dasharray="14 10"/>
  <g class="bounce">
    <g fill="{TBG}" stroke="{G}" stroke-width="2.5" filter="url(#glowS)">
      <path d="M{cx-48} {cy+8} V{cy-38} H{cx-6} L{cx+2} {cy-10} H{cx+46} V{cy+14} H{cx-48} Z"/>
      <path d="M{cx+24} {cy-10} V{cy-24}"/>
    </g>
    <rect x="{cx-40}" y="{cy-30}" width="30" height="20" fill="{G}" fill-opacity=".3"/>
    {wheel(cx - 26, cy + 14, 22)}
    {wheel(cx + 32, cy + 24, 13)}
  </g>
  <g class="wrench" style="transform-origin:{cx + 62}px {cy - 30}px">
    <path d="M{cx + 50} {cy - 18} L{cx + 70} {cy - 38} m-6 -6 a8 8 0 1 0 12 12" fill="none" stroke="{G}" stroke-width="4" stroke-linecap="round"/>
  </g>"""


def icon_building(cx, cy):
    wins = "".join(
        f'<rect class="win" style="animation-delay:-{random.uniform(0, 4):.2f}s;animation-duration:{random.uniform(2.5, 5):.2f}s" '
        f'x="{cx - 30 + c * 16}" y="{cy - 36 + r * 16}" width="10" height="10" fill="{G}"/>'
        for r in range(5) for c in range(4)
    )
    return f"""
  <line x1="{cx-100}" y1="{cy+52}" x2="{cx+100}" y2="{cy+52}" stroke="{G2}" stroke-width="2"/>
  <rect x="{cx+42}" y="{cy}" width="40" height="52" fill="{TBG}" stroke="{G2}" stroke-width="2"/>
  <rect x="{cx-86}" y="{cy+12}" width="36" height="40" fill="{TBG}" stroke="{G2}" stroke-width="2"/>
  <rect x="{cx-40}" y="{cy-46}" width="80" height="98" fill="{TBG}" stroke="{G}" stroke-width="2.5" filter="url(#glowS)"/>
  <path d="M{cx} {cy-46} V{cy-64}" stroke="{G}" stroke-width="2"/>
  <circle class="blink" cx="{cx}" cy="{cy-66}" r="3.5" fill="{G}" filter="url(#glowS)"/>
  {wins}
  <rect x="{cx-8}" y="{cy+38}" width="16" height="14" fill="{G}" fill-opacity=".4"/>"""


ICON_CSS += f"""
  .pop {{ opacity: 0; animation: pop 3.2s ease-out infinite; transform-box: fill-box; transform-origin: center; }}
  @keyframes pop {{ 0% {{ opacity: 0; transform: scale(.3); }} 15%,85% {{ opacity: 1; transform: scale(1); }} 100% {{ opacity: 0; }} }}
  .wave {{ animation: wave 1.8s ease-out infinite; }}
  @keyframes wave {{ 0% {{ opacity: 0; }} 30% {{ opacity: 1; }} 100% {{ opacity: 0; }} }}
  .flipc {{ transform-box: fill-box; transform-origin: center; animation: flipc 3s ease-in-out infinite; }}
  @keyframes flipc {{ 0%,40%,100% {{ transform: scaleX(1); }} 55% {{ transform: scaleX(0); }} 70% {{ transform: scaleX(1); }} }}
  .ants {{ animation: ants 1s linear infinite; }}
  @keyframes ants {{ to {{ stroke-dashoffset: -20; }} }}
  .pen {{ animation: pen 4s ease-in-out infinite; }}
  @keyframes pen {{ 0%,100% {{ transform: translate(0,0); }} 25% {{ transform: translate(-40px,-30px); }} 50% {{ transform: translate(-30px,26px); }} 75% {{ transform: translate(10px,-40px); }} }}
  .hop {{ animation: hop 6s steps(1) infinite; }}
  @keyframes hop {{ 0% {{ transform: translate(0,0); }} 16% {{ transform: translate(22px,0); }} 33% {{ transform: translate(66px,0); }} 50% {{ transform: translate(22px,18px); }} 66% {{ transform: translate(44px,36px); }} 83% {{ transform: translate(0,36px); }} }}
  .eq {{ transform-box: fill-box; transform-origin: bottom; animation: eq .9s ease-in-out infinite alternate; }}
  @keyframes eq {{ from {{ transform: scaleY(.2); }} to {{ transform: scaleY(1); }} }}
  .wrench {{ animation: wrench 1.6s ease-in-out infinite; }}
  @keyframes wrench {{ 0%,100% {{ transform: rotate(0); }} 50% {{ transform: rotate(-25deg); }} }}
  .win {{ animation-name: win; animation-iteration-count: infinite; animation-timing-function: steps(1); }}
  @keyframes win {{ 0% {{ opacity: .9; }} 50% {{ opacity: .15; }} }}"""

ICONS = {
    "truck": icon_truck, "code": icon_code, "shield": icon_shield, "phone": icon_phone,
    "game": icon_game, "design": icon_design, "calendar": icon_calendar, "article": icon_article,
    "tractor": icon_tractor, "building": icon_building,
}


# ===================================================================== cards
def tags_svg(tags, y, x0, max_w, fs=11):
    out, x = [], x0
    for tg in tags:
        w = len(tg) * fs * CW + 14
        out.append(
            f'<rect x="{x:.1f}" y="{y}" width="{w:.1f}" height="22" rx="11" fill="{G}" fill-opacity=".12" stroke="{G}" stroke-opacity=".7"/>'
            f'<text x="{x + w / 2:.1f}" y="{y + 15}" font-size="{fs}" fill="{G}" text-anchor="middle">{escape(tg)}</text>'
        )
        x += w + 6
    assert x - 6 - x0 <= max_w, f"tags largas demais: {tags}"
    return "".join(out)


def _finish(svg, extra_clip):
    return svg.replace("</defs>", extra_clip + "</defs>", 1)


def project_card(slug, title, desc, tags, icon, idx):
    """Card vertical 270x350 (outros projetos)."""
    W, H, R = 270, 350, 14
    cx, cy = W // 2, 84
    desc_svg = "".join(f'<text x="20" y="{232 + i * 20}" font-size="14" fill="{SOFT}">{escape(l)}</text>' for i, l in enumerate(desc))
    svg = svg_open(W, H, f"Projeto {title}: {' '.join(desc)}", ICON_DEFS, ICON_CSS) + f"""
<g clip-path="url(#round)">
  {bg(W, H)}
  <rect x="14" y="14" width="{W-28}" height="140" rx="10" fill="#000f06" fill-opacity=".6" stroke="{G}" stroke-opacity=".3"/>
  <g clip-path="url(#iconclip)">{ICONS[icon](cx, cy)}</g>
  <text x="22" y="32" font-size="11" fill="{DIM}">0{idx}</text>
  <text x="20" y="180" font-size="12" fill="{DIM}">~/projetos/</text>
  <text class="b" x="20" y="205" font-size="20" fill="{G}" filter="url(#glowS)">{escape(title)}</text>
  <rect class="blink" x="{20 + len(title) * 20 * CW + 6:.0f}" y="190" width="9" height="18" fill="{G}"/>
  {desc_svg}
  {tags_svg(tags, 292, 20, W - 40)}
  <text x="20" y="{H-16}" font-size="12" fill="{DIM}">&gt; abrir repositório_</text>
  {overlay(W, H)}
</g>
{frame(W, H, R, 2)}
</svg>"""
    save(f"projetos/{slug}.svg", _finish(svg, f'<clipPath id="iconclip"><rect x="14" y="14" width="{W-28}" height="140" rx="10"/></clipPath>'))


def focus_card(slug, num, title_lines, desc, icon):
    """Card vertical 270 de área de foco."""
    W, R = 270, 14
    cx, cy = W // 2, 84
    y = 182
    parts = [f'<text x="20" y="{y}" font-size="12" fill="{DIM}">[ foco_0{num} ]</text>']
    for l in title_lines:
        y += 26
        parts.append(f'<text class="b" x="20" y="{y}" font-size="21" fill="{G}" filter="url(#glowS)">{escape(l)}</text>')
    y += 8
    for l in desc:
        y += 20
        parts.append(f'<text x="20" y="{y}" font-size="14" fill="{SOFT}">{escape(l)}</text>')
    H = y + 26
    svg = svg_open(W, H, f"Foco: {' '.join(title_lines)}. {' '.join(desc)}", ICON_DEFS, ICON_CSS) + f"""
<g clip-path="url(#round)">
  {bg(W, H)}
  <rect x="14" y="14" width="{W-28}" height="140" rx="10" fill="#000f06" fill-opacity=".6" stroke="{G}" stroke-opacity=".3"/>
  <g clip-path="url(#iconclip)">{ICONS[icon](cx, cy)}</g>
  {''.join(parts)}
  {overlay(W, H)}
</g>
{frame(W, H, R, 2)}
</svg>"""
    save(f"foco-{slug}.svg", _finish(svg, f'<clipPath id="iconclip"><rect x="14" y="14" width="{W-28}" height="140" rx="10"/></clipPath>'))


def ws_card(slug, code, subtitle, desc, tags, icon):
    """Card horizontal 410x210 dos módulos WorldSkills."""
    W, H, R = 410, 210, 14
    cx, cy = 88, H // 2
    tx = 178
    d = "".join(f'<text x="{tx}" y="{120 + i * 19}" font-size="13" fill="{SOFT}">{escape(l)}</text>' for i, l in enumerate(desc))
    title = f"Aprender+ {code}"
    svg = svg_open(W, H, f"WorldSkills {title}: {subtitle}. {' '.join(desc)}", ICON_DEFS, ICON_CSS) + f"""
<g clip-path="url(#round)">
  {bg(W, H)}
  <rect x="14" y="14" width="148" height="{H-28}" rx="10" fill="#000f06" fill-opacity=".6" stroke="{G}" stroke-opacity=".3"/>
  <g clip-path="url(#iconclip)">{ICONS[icon](cx, cy)}</g>
  <text x="{tx}" y="38" font-size="12" fill="{DIM}">[ worldskills · {code} ]</text>
  {trophy(W - 30, 30, 0.55)}
  <text class="b" x="{tx}" y="68" font-size="22" fill="{G}" filter="url(#glowS)">{escape(title)}</text>
  <text x="{tx}" y="92" font-size="14" fill="{G}">{escape(subtitle)}</text>
  {d}
  {tags_svg(tags, 158, tx, W - tx - 14)}
  <text x="{tx}" y="{H-14}" font-size="11" fill="{DIM}">&gt; abrir repositório_</text>
  {overlay(W, H)}
</g>
{frame(W, H, R, 2)}
</svg>"""
    save(f"projetos/{slug}.svg", _finish(svg, f'<clipPath id="iconclip"><rect x="14" y="14" width="148" height="{H-28}" rx="10"/></clipPath>'))


def ws_highlight():
    """Destaque da conquista na WorldSkills (620x220)."""
    W, H, R = 620, 220, 14
    cx, cy = 100, 108
    rays = "".join(
        f'<line x1="{cx}" y1="{cy}" x2="{cx + 90 * math.cos(math.radians(a)):.1f}" y2="{cy + 90 * math.sin(math.radians(a)):.1f}" stroke="{G}" stroke-opacity=".25" stroke-width="6"/>'
        for a in range(0, 360, 30)
    )
    tx = 204
    css = ".rays { transform-box: view-box; transform-origin: %dpx %dpx; animation: spin 14s linear infinite; }" % (cx, cy)
    css += " .float { animation: hover 3s ease-in-out infinite; }"
    svg = svg_open(W, H, "Conquista: 1º lugar na primeira etapa da seletiva escolar da WorldSkills, Desenvolvimento de Aplicativos Móveis", ICON_DEFS, ICON_CSS + css) + f"""
<g clip-path="url(#round)">
  {bg(W, H)}
  <rect x="14" y="14" width="172" height="{H-28}" rx="10" fill="#000f06" fill-opacity=".6" stroke="{G}" stroke-opacity=".3"/>
  <g clip-path="url(#iconclip)">
    <g class="rays">{rays}</g>
    <circle class="pulse" cx="{cx}" cy="{cy}" r="44" fill="none" stroke="{G}" stroke-width="2"/>
    <g class="float" filter="url(#glow)">{trophy(cx, cy - 4, 2.3)}</g>
  </g>
  <text x="{tx}" y="44" font-size="13" fill="{DIM}">[ conquista ]</text>
  <text class="b" x="{tx}" y="92" font-size="44" fill="{G}" filter="url(#glow)">1º LUGAR</text>
  <text x="{tx}" y="126" font-size="16" fill="{SOFT}">Seletiva escolar WorldSkills · 1ª etapa</text>
  <text x="{tx}" y="150" font-size="16" fill="{SOFT}">Desenvolvimento de Aplicativos Móveis</text>
  <text x="{tx}" y="186" font-size="13" fill="{DIM}">&gt; projeto-teste Aprender+ · módulos abaixo_</text>
  {overlay(W, H)}
</g>
{frame(W, H, R, 2)}
</svg>"""
    save("worldskills.svg", _finish(svg, f'<clipPath id="iconclip"><rect x="14" y="14" width="172" height="{H-28}" rx="10"/></clipPath>'))



# ===================================================================== rodapé
def footer():
    W, H, R = 1000, 150, 14
    msg = "> conexão encerrada. obrigado pela visita"
    fs = 24
    cw = fs * CW
    tw = len(msg) * cw
    sx = (W - tw) / 2
    PB = "#00150a"
    binary = " ".join(format(ord(c), "08b") for c in "EMANUEL")
    css = f"""
  .type {{ animation: type 8s infinite; }}
  @keyframes type {{
    0% {{ transform: translateX(0); animation-timing-function: steps({len(msg)}); }}
    45% {{ transform: translateX({tw:.1f}px); animation-timing-function: linear; }}
    100% {{ transform: translateX({tw:.1f}px); }}
  }}"""
    svg = svg_open(W, H, "Conexão encerrada. Obrigado pela visita!", css=css) + f"""
<g clip-path="url(#round)">
  {bg(W, H)}
  <rect x="{sx - 24:.1f}" y="38" width="{tw + 60:.1f}" height="46" rx="8" fill="{PB}" stroke="{G}" stroke-opacity=".5"/>
  <text x="{sx:.1f}" y="69" font-size="{fs}" fill="{G}" textLength="{tw:.1f}" lengthAdjust="spacingAndGlyphs" filter="url(#glowS)">{escape(msg)}</text>
  <g class="type">
    <rect x="{sx:.1f}" y="46" width="{tw + 4:.1f}" height="32" fill="{PB}"/>
    <rect class="blink" x="{sx + 1:.1f}" y="50" width="{cw - 2:.1f}" height="24" fill="{G}"/>
  </g>
  <text x="{W/2}" y="118" font-size="14" fill="{DIM}" text-anchor="middle" letter-spacing="1">{binary}</text>
  {overlay(W, H)}
</g>
{frame(W, H, R, 2)}
</svg>"""
    save("footer.svg", svg)


# ===================================================================== conteúdo
banner()
divider()
footer()
terminal([
    ("cmd", "whoami"),
    ("out", "Emanuel Felipe · 17 anos"),
    ("out", "Itumbiara - GO, Brasil"),
    ("cmd", "cat formacao.txt"),
    ("out", "Técnico em Desenvolvimento de Sistemas"),
    ("out", "Engenharia de Software (cursando)"),
    ("cmd", "cat conquistas.txt"),
    ("hi", "[1º] Seletiva escolar WorldSkills"),
    ("out", "    Desenvolvimento de Apps Móveis"),
    ("cmd", "cat status.txt"),
    ("hi", "[>] Aberto a oportunidades de emprego"),
    ("cmd", "ls ~/stack"),
    ("out", "python  php  html  css  dart  flutter"),
    ("out", "java  mysql  sql"),
    ("end", ""),
])
heading("titulo-sobre.svg", "sobre_mim", 1)
heading("titulo-foco.svg", "foco", 2)
heading("titulo-stack.svg", "tecnologias", 3)
heading("titulo-worldskills.svg", "worldskills", 4)
heading("titulo-projetos.svg", "outros_projetos", 5)
heading("titulo-stats.svg", "estatísticas", 6)
focus_card("software", 1, ["Engenharia de", "Software"], ["Projetar sistemas", "organizados, testados", "e fáceis de manter."], "code")
focus_card("cyber", 2, ["Cyber", "Segurança"], ["Proteger aplicações,", "redes e dados contra", "ataques."], "shield")
focus_card("mobile", 3, ["Desenvolvimento", "Mobile"], ["Apps Android com", "Flutter, do protótipo", "no Figma ao código."], "phone")
ws_highlight()
ws_card("aprender-mais-a1-flutter", "A1", "Jogos educativos", ["Quiz, memória e cores", "com sensores e áudio."], ["Flutter", "Dart", "Android"], "game")
ws_card("aprender-mais-b1-design", "B1", "Design de interface", ["App educacional: login,", "cursos, cadastro e perfil."], ["Figma", "UI/UX"], "design")
ws_card("aprender-mais-b2-design", "B2", "Design de interface", ["Explorar cursos, agenda", "e perfil do estudante."], ["Figma", "UI/UX"], "calendar")
ws_card("aprender-mais-c1-flutter", "C1", "Artigos e resumos", ["Artigos, vídeo e resumos", "gravados em áudio."], ["Flutter", "Dart", "Android"], "article")
project_card("Agro_Mec", "Agro_Mec", ["Gestão de máquinas", "agrícolas, peças e", "ordens de serviço."], ["Python", "Flask", "SQLite"], "tractor", 1)
project_card("sistema-gestao-frota", "gestao-frota", ["Frota e manutenção:", "veículos, peças e baixa", "automática de estoque."], ["Python", "Django", "SQL"], "truck", 2)
project_card("sistema_empresa_web", "empresa_web", ["Gestão empresarial:", "clientes, fornecedores", "e funcionários."], ["Flask", "SQLAlchemy", "MySQL"], "building", 3)
