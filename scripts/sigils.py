# -*- coding: utf-8 -*-
"""Gera brasões heráldicos (PNG) para personagens sem retrato conhecido."""
import os, sys, math, json
sys.path.insert(0, os.path.dirname(__file__))
import data_chars as D
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.join(os.path.dirname(__file__), "..")
OUT = os.path.join(ROOT, "img_raw")
S = 400

# casa -> (fundo, campo secundário, cor do símbolo, glifo)
SPEC = {
    "Targaryen": ("#0e0d10", "#241014", "#c0392b", "dragon"),
    "Blackfyre": ("#0b0b0c", "#1a1416", "#8e1d1d", "dragon"),
    "Velaryon":  ("#07222c", "#0e3949", "#7fd8e8", "seahorse"),
    "Stark":     ("#1c2024", "#2b3238", "#c8d2da", "wolf"),
    "Lannister": ("#3a2c05", "#5c4708", "#e0b423", "lion"),
    "Baratheon": ("#241a06", "#3d2c08", "#e0b423", "stag"),
    "Tully":     ("#0f2c4d", "#7a1414", "#c8d2da", "fish"),
    "Arryn":     ("#123a63", "#1d5591", "#eaf2fa", "falcon"),
    "Greyjoy":   ("#131313", "#232323", "#c9b06a", "kraken"),
    "Martell":   ("#7a2a08", "#a83c0c", "#f0a92a", "sun"),
    "Tyrell":    ("#1d4a20", "#2c6b30", "#e8d98a", "rose"),
    "Blackwood": ("#141414", "#241010", "#b02b2b", "tree"),
    "Penrose":   ("#3a2a12", "#5a4020", "#d8c48a", "quill"),
    "Bracken":   ("#5a1414", "#7a2020", "#e0c86a", "horse"),
    "Hightower": ("#1b2410", "#2d3a19", "#e6d68a", "tower"),
    "Dayne":     ("#2a1f4a", "#3d2e6b", "#e8e2ff", "star"),
    "Strong":    ("#2e2314", "#463620", "#c9a961", "tower"),
    "Rivers":    ("#22222c", "#33333f", "#a9a9c0", "dragon"),
    "Frey":      ("#2b3540", "#3d4b5a", "#cfd8e0", "tower"),
    "Bolton":    ("#2b0f0f", "#451818", "#d4a5a5", "flay"),
    "Dothraki":  ("#3a2410", "#5a3818", "#d9a441", "arakh"),
    "Sand":      ("#7a4a1a", "#a06a2a", "#f0c86a", "sun"),
    "—":         ("#241f18", "#3a3226", "#c9b78a", "cross"),
}
DEFAULT = ("#241f18", "#3a3226", "#c9b78a", "cross")


def poly(d, pts, fill=None, outline=None, w=3):
    d.polygon(pts, fill=fill, outline=outline)


def draw_glyph(d, kind, col, cx, cy, r):
    """Silhuetas heráldicas simplificadas."""
    def P(*pts):
        return [(cx + x * r, cy + y * r) for x, y in pts]

    if kind == "dragon":  # dragão tricéfalo dos Targaryen
        # asas membranosas
        for s in (-1, 1):
            d.polygon(P((s*0.20, 0.02), (s*1.15, -0.62), (s*1.02, -0.02),
                        (s*1.18, 0.34), (s*0.78, 0.26), (s*0.84, 0.62), (s*0.30, 0.44)), fill=col)
        # corpo
        d.polygon(P((-0.34, -0.02), (0.34, -0.02), (0.26, 0.52), (0, 0.72), (-0.26, 0.52)), fill=col)
        # cauda
        d.line([(cx, cy + r*0.62), (cx + r*0.16, cy + r*1.02), (cx - r*0.26, cy + r*1.16)],
               fill=col, width=int(r*0.13), joint="curve")
        # três pescoços + cabeças (esquerda, centro, direita)
        for s, ny, hx0 in ((-1, -0.34, -0.74), (0, -0.62, 0.0), (1, -0.34, 0.74)):
            nx = s * 0.30
            d.line([(cx + nx*r*0.55, cy - r*0.02), (cx + hx0*r*0.72, cy + ny*r*1.10)],
                   fill=col, width=int(r*0.17))
            hx = cx + hx0 * r * 0.74
            hy = cy + ny * r * 1.16
            # crânio alongado + mandíbula aberta
            d.polygon([(hx - s*r*0.10 - r*0.02, hy + r*0.16), (hx - s*r*0.14, hy - r*0.14),
                       (hx + s*r*0.46, hy - r*0.10), (hx + s*r*0.30, hy + r*0.06),
                       (hx + s*r*0.44, hy + r*0.16), (hx + s*r*0.06, hy + r*0.20)], fill=col)
            if s == 0:  # cabeça central de frente
                d.polygon([(hx - r*0.17, hy + r*0.20), (hx - r*0.13, hy - r*0.16),
                           (hx + r*0.13, hy - r*0.16), (hx + r*0.17, hy + r*0.20),
                           (hx, hy + r*0.34)], fill=col)
                d.polygon([(hx - r*0.13, hy - r*0.14), (hx - r*0.30, hy - r*0.50), (hx - r*0.02, hy - r*0.26)], fill=col)
                d.polygon([(hx + r*0.13, hy - r*0.14), (hx + r*0.30, hy - r*0.50), (hx + r*0.02, hy - r*0.26)], fill=col)
            else:       # chifres das laterais
                d.polygon([(hx - s*r*0.12, hy - r*0.12), (hx - s*r*0.34, hy - r*0.44),
                           (hx + s*r*0.04, hy - r*0.22)], fill=col)
    elif kind == "wolf":
        d.polygon(P((-0.62, -0.30), (-0.38, -0.86), (-0.14, -0.36), (0.30, -0.42),
                    (0.72, 0.02), (0.46, 0.70), (-0.30, 0.72), (-0.72, 0.24)), fill=col)
        d.polygon(P((0.30, -0.42), (0.62, -0.90), (0.70, -0.24)), fill=col)
        d.ellipse(P((-0.28, -0.10), (-0.06, 0.10)), fill="#0f1216")
        d.ellipse(P((0.16, -0.12), (0.38, 0.08)), fill="#0f1216")
    elif kind == "lion":
        # juba em raios
        for i in range(18):
            a = i * math.tau / 18
            d.polygon([(cx + math.cos(a - .09) * r * .58, cy + math.sin(a - .09) * r * .58),
                       (cx + math.cos(a) * r * 1.05, cy + math.sin(a) * r * 1.05),
                       (cx + math.cos(a + .09) * r * .58, cy + math.sin(a + .09) * r * .58)], fill=col)
        d.ellipse(P((-0.72, -0.72), (0.72, 0.72)), fill=col)
        # focinho
        d.ellipse(P((-0.46, -0.30), (0.46, 0.62)), fill="#f3dfa0")
        # orelhas
        d.ellipse(P((-0.66, -0.72), (-0.30, -0.36)), fill=col)
        d.ellipse(P((0.30, -0.72), (0.66, -0.36)), fill=col)
        # olhos
        d.polygon(P((-0.40, -0.16), (-0.10, -0.20), (-0.14, -0.02), (-0.38, 0.00)), fill="#2b1e02")
        d.polygon(P((0.40, -0.16), (0.10, -0.20), (0.14, -0.02), (0.38, 0.00)), fill="#2b1e02")
        # nariz + boca rugindo
        d.polygon(P((-0.14, 0.12), (0.14, 0.12), (0, 0.30)), fill="#2b1e02")
        d.arc(P((-0.34, 0.14), (0.34, 0.60)), 20, 160, fill="#2b1e02", width=max(2, int(r*0.07)))
        d.polygon(P((-0.20, 0.36), (-0.12, 0.36), (-0.16, 0.54)), fill="#fffaf0")
        d.polygon(P((0.12, 0.36), (0.20, 0.36), (0.16, 0.54)), fill="#fffaf0")
    elif kind == "stag":
        d.polygon(P((-0.26, 0.10), (0.26, 0.10), (0.20, 0.80), (-0.20, 0.80)), fill=col)
        d.ellipse(P((-0.30, -0.32), (0.30, 0.20)), fill=col)
        for s in (-1, 1):
            d.line([(cx + s*r*0.16, cy - r*0.28), (cx + s*r*0.50, cy - r*0.96)], fill=col, width=int(r*0.13))
            d.line([(cx + s*r*0.30, cy - r*0.56), (cx + s*r*0.76, cy - r*0.62)], fill=col, width=int(r*0.11))
            d.line([(cx + s*r*0.40, cy - r*0.76), (cx + s*r*0.84, cy - r*0.94)], fill=col, width=int(r*0.10))
    elif kind == "fish":
        d.polygon(P((-0.92, 0), (-0.20, -0.52), (0.52, -0.30), (0.92, 0),
                    (0.52, 0.30), (-0.20, 0.52)), fill=col)
        d.polygon(P((0.80, 0), (1.10, -0.46), (1.10, 0.46)), fill=col)
        d.ellipse(P((-0.62, -0.14), (-0.38, 0.10)), fill="#0f2c4d")
    elif kind == "falcon":
        d.polygon(P((0, -0.92), (0.34, -0.30), (0.96, -0.12), (0.42, 0.34),
                    (0.20, 0.94), (-0.20, 0.94), (-0.42, 0.34), (-0.96, -0.12), (-0.34, -0.30)), fill=col)
        d.ellipse(P((-0.22, -0.86), (0.22, -0.42)), fill=col)
    elif kind == "kraken":
        d.ellipse(P((-0.40, -0.86), (0.40, -0.06)), fill=col)
        for i in range(7):
            a = math.pi * (0.12 + 0.76 * i / 6)
            x0, y0 = cx + math.cos(a) * r * 0.34, cy - r * 0.12
            d.line([(x0, y0), (x0 + math.cos(a) * r * 0.55, cy + r * 0.62),
                    (x0 + math.cos(a) * r * 1.05, cy + r * 0.34)],
                   fill=col, width=int(r * 0.13), joint="curve")
    elif kind == "sun":
        d.ellipse(P((-0.56, -0.56), (0.56, 0.56)), fill=col)
        for i in range(16):
            a = i * math.tau / 16
            d.line([(cx + math.cos(a)*r*0.54, cy + math.sin(a)*r*0.54),
                    (cx + math.cos(a)*r*1.00, cy + math.sin(a)*r*1.00)], fill=col, width=int(r*0.11))
        d.line([(cx - r*0.95, cy + r*0.60), (cx + r*0.95, cy - r*0.72)], fill="#f6e7c0", width=int(r*0.13))
        d.polygon(P((0.72, -0.90), (1.02, -0.60), (0.80, -0.52)), fill="#f6e7c0")
    elif kind == "rose":
        for k, sc in enumerate((1.0, 0.72, 0.44)):
            for i in range(6):
                a = i * math.tau / 6 + k * 0.5
                px, py = cx + math.cos(a) * r * 0.40 * sc, cy + math.sin(a) * r * 0.40 * sc
                d.ellipse([px - r*0.42*sc, py - r*0.42*sc, px + r*0.42*sc, py + r*0.42*sc], fill=col)
        d.ellipse(P((-0.18, -0.18), (0.18, 0.18)), fill="#1d4a20")
    elif kind == "tree":
        d.polygon(P((-0.14, 0.20), (0.14, 0.20), (0.24, 0.96), (-0.24, 0.96)), fill=col)
        for i in range(9):
            a = -math.pi/2 + (i - 4) * 0.34
            d.line([(cx, cy + r*0.20), (cx + math.cos(a)*r*0.85, cy + r*0.20 + math.sin(a)*r*0.85)],
                   fill=col, width=int(r*0.10))
        for i in range(11):
            a = i * math.tau / 11
            d.ellipse([cx + math.cos(a)*r*0.66 - r*0.11, cy - r*0.30 + math.sin(a)*r*0.46 - r*0.11,
                       cx + math.cos(a)*r*0.66 + r*0.11, cy - r*0.30 + math.sin(a)*r*0.46 + r*0.11], fill=col)
    elif kind == "tower":
        d.polygon(P((-0.44, -0.30), (0.44, -0.30), (0.36, 0.92), (-0.36, 0.92)), fill=col)
        for x in (-0.44, -0.15, 0.15, 0.36):
            d.rectangle(P((x, -0.62), (x + 0.16, -0.28)), fill=col)
        d.ellipse(P((-0.16, 0.02), (0.16, 0.34)), fill="#f6e7c0")
        d.polygon(P((0, -1.02), (0.12, -0.72), (-0.12, -0.72)), fill="#f6e7c0")
    elif kind == "star":
        pts = []
        for i in range(16):
            rr = r * (1.0 if i % 2 == 0 else 0.42)
            a = i * math.tau / 16 - math.pi / 2
            pts.append((cx + math.cos(a) * rr, cy + math.sin(a) * rr))
        d.polygon(pts, fill=col)
    elif kind == "horse":
        d.polygon(P((-0.70, 0.60), (-0.40, -0.30), (0.10, -0.50), (0.30, -0.92),
                    (0.56, -0.80), (0.52, -0.34), (0.82, 0.10), (0.60, 0.72), (-0.30, 0.76)), fill=col)
    elif kind == "quill":
        d.polygon(P((0.70, -0.90), (0.24, 0.30), (-0.60, 0.86), (-0.20, -0.10), (0.34, -0.62)), fill=col)
        d.line([(cx + r*0.62, cy - r*0.80), (cx - r*0.50, cy + r*0.80)], fill="#1d1509", width=int(r*0.05))
    elif kind == "flay":
        d.polygon(P((0, -0.92), (0.34, -0.40), (0.28, 0.50), (0, 0.94), (-0.28, 0.50), (-0.34, -0.40)), fill=col)
        d.polygon(P((-0.34, -0.40), (-0.86, -0.10), (-0.30, 0.10)), fill=col)
        d.polygon(P((0.34, -0.40), (0.86, -0.10), (0.30, 0.10)), fill=col)
    elif kind == "arakh":
        for s in (-1, 1):
            d.arc([cx - r*0.95, cy - r*0.85, cx + r*0.95, cy + r*0.55], 200 if s < 0 else 340,
                  340 if s < 0 else 480, fill=col, width=int(r*0.16))
            d.line([(cx + s*r*0.80, cy + r*0.10), (cx + s*r*0.30, cy + r*0.92)], fill=col, width=int(r*0.14))
    elif kind == "seahorse":
        d.polygon(P((-0.10, -0.94), (0.34, -0.72), (0.20, -0.34), (0.34, 0.10),
                    (0.10, 0.56), (0.44, 0.88), (0.02, 0.94), (-0.28, 0.54),
                    (-0.10, 0.06), (-0.34, -0.36), (-0.30, -0.76)), fill=col)
        d.polygon(P((-0.10, -0.94), (0.40, -1.00), (0.26, -0.70)), fill=col)
        d.ellipse(P((-0.04, -0.80), (0.10, -0.66)), fill="#07222c")
    else:  # cross / genérico
        d.polygon(P((-0.16, -0.92), (0.16, -0.92), (0.16, -0.22), (0.86, -0.22),
                    (0.86, 0.10), (0.16, 0.10), (0.16, 0.92), (-0.16, 0.92),
                    (-0.16, 0.10), (-0.86, 0.10), (-0.86, -0.22), (-0.16, -0.22)), fill=col)


def _hex(c):
    c = c.lstrip("#")
    return tuple(int(c[i:i+2], 16) for i in (0, 2, 4))


def _rgb(t):
    return "#%02x%02x%02x" % tuple(max(0, min(255, int(v))) for v in t)


def shift(color, f):
    """Clareia (f>1) ou escurece (f<1) uma cor mantendo a matiz."""
    return _rgb([v * f for v in _hex(color)])


def variant(pid):
    """Fator de tom determinístico por pid: distingue brasões repetidos."""
    h = 0
    for ch in pid:
        h = (h * 131 + ord(ch)) & 0xFFFFFFFF
    return 0.80 + (h % 9) * 0.075, (h >> 8) % 4


def initials(pid):
    name = D.P[pid].get("name", "")
    parts = [w for w in name.replace("-", " ").split() if w[:1].isalpha()]
    skip = {"de", "da", "do", "of", "the", "o", "a", "e"}
    parts = [w for w in parts if w.lower() not in skip] or parts
    if not parts:
        return ""
    if len(parts) == 1:
        return parts[0][:2].upper()
    return (parts[0][0] + parts[-1][0]).upper()


def font(size):
    for p in ("/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf",
              "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"):
        if os.path.exists(p):
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()


def make(pid, house):
    bg, field, col, glyph = SPEC.get(house, DEFAULT)
    f, layout = variant(pid)
    bg, field, col = shift(bg, f), shift(field, f), shift(col, 0.72 + f * 0.32)
    im = Image.new("RGB", (S, S), bg)
    d = ImageDraw.Draw(im)
    # campo: a partição varia por personagem (4 estilos heráldicos)
    if layout == 0:      # cortado em diagonal
        d.polygon([(0, 0), (S, 0), (S, int(S * .55)), (0, int(S * .78))], fill=field)
    elif layout == 1:    # partido ao meio
        d.rectangle([0, 0, S // 2, S], fill=field)
    elif layout == 2:    # chefe (faixa superior)
        d.rectangle([0, 0, S, int(S * .34)], fill=field)
    else:                # esquartelado
        d.rectangle([0, 0, S // 2, S // 2], fill=field)
        d.rectangle([S // 2, S // 2, S, S], fill=field)
    # moldura
    d.rectangle([6, 6, S - 7, S - 7], outline="#8a7games" if False else "#8a7444", width=3)
    d.rectangle([14, 14, S - 15, S - 15], outline="#5c4a24", width=1)
    draw_glyph(d, glyph, col, S / 2, S / 2 - 26, S * 0.29)
    # monograma: iniciais em faixa inferior, para diferenciar homônimos
    ini = initials(pid)
    if ini:
        by0, by1 = int(S * .795), int(S * .925)
        d.rectangle([28, by0, S - 29, by1], fill=shift(bg, 0.55), outline="#8a7444", width=2)
        ft = font(58)
        bb = d.textbbox((0, 0), ini, font=ft)
        d.text(((S - (bb[2] - bb[0])) / 2 - bb[0], (by0 + by1 - (bb[3] - bb[1])) / 2 - bb[1]),
               ini, font=ft, fill="#e8dcb8")
    # vinheta
    im.save(os.path.join(OUT, pid + ".img"), "PNG")


if __name__ == "__main__":
    need = json.load(open(os.path.join(ROOT, "need_sigil.json")))
    for pid in need:
        make(pid, D.P[pid]["house"])
        print("SIGIL", pid, D.P[pid]["house"])
    print("gerados:", len(need))
