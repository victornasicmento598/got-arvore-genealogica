# -*- coding: utf-8 -*-
"""Gera thumb quadrado (retrato, foco no topo) e versão grande para o lightbox."""
import os, sys, json
sys.path.insert(0, os.path.dirname(__file__))
import data_chars as D
from PIL import Image, ImageOps

ROOT = os.path.join(os.path.dirname(__file__), "..")
RAW = os.path.join(ROOT, "img_raw")
SITE = os.path.join(ROOT, "docs")
TH = os.path.join(SITE, "img", "t")
BG = os.path.join(SITE, "img", "f")
for d in (TH, BG):
    os.makedirs(d, exist_ok=True)

TS, FS = 220, 620


def square_top(im, size, bias=0.34):
    """Recorta quadrado privilegiando o terço superior (onde está o rosto)."""
    w, h = im.size
    if h > w:
        side = w
        top = int((h - side) * bias)
        im = im.crop((0, top, w, top + side))
    elif w > h:
        side = h
        left = int((w - side) / 2)
        im = im.crop((left, 0, left + side, h))
    return im.resize((size, size), Image.LANCZOS)


def main():
    manifest = {}
    for pid in D.P:
        src = os.path.join(RAW, pid + ".img")
        if not os.path.exists(src):
            print("SEM ARQUIVO", pid)
            continue
        im = Image.open(src)
        if im.mode in ("RGBA", "LA", "P"):
            im = im.convert("RGBA")
            bgim = Image.new("RGB", im.size, (26, 22, 16))
            bgim.paste(im, mask=im.split()[-1] if im.mode == "RGBA" else None)
            im = bgim
        else:
            im = im.convert("RGB")
        im = ImageOps.exif_transpose(im)
        square_top(im, TS).save(os.path.join(TH, pid + ".jpg"), "JPEG", quality=82, optimize=True)
        big = im.copy()
        big.thumbnail((FS, FS * 2), Image.LANCZOS)
        big.save(os.path.join(BG, pid + ".jpg"), "JPEG", quality=86, optimize=True)
        manifest[pid] = True
    print("processadas:", len(manifest))
    sizes = sum(os.path.getsize(os.path.join(r, f)) for r in (TH, BG) for f in os.listdir(r))
    print("peso total: %.1f MB" % (sizes / 1e6))


if __name__ == "__main__":
    main()
