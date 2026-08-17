# -*- coding: utf-8 -*-
"""Baixa imagem para cada personagem.
Prioridade:
  - personagens de série (GOT/HOTD/AKOTSK): gameofthrones.fandom (foto real do ator)
  - demais: iceandfire.fandom / awoiaf.fandom / gameofthrones (ilustração)
"""
import json, os, sys, time, urllib.request, urllib.parse, io
sys.path.insert(0, os.path.dirname(__file__))
import data_chars as D
from PIL import Image

UA = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/122 Safari/537.36"}
GOT = "https://gameofthrones.fandom.com/api.php"
IAF = "https://iceandfire.fandom.com/api.php"
AWO = "https://awoiaf.fandom.com/api.php"
OUT = os.path.join(os.path.dirname(__file__), "..", "img_raw")
os.makedirs(OUT, exist_ok=True)
CACHE_F = os.path.join(os.path.dirname(__file__), "..", "img_sources.json")
cache = json.load(open(CACHE_F)) if os.path.exists(CACHE_F) else {}


def api(url, params):
    q = urllib.parse.urlencode(params)
    req = urllib.request.Request(url + "?" + q, headers=UA)
    for _ in range(3):
        try:
            return json.load(urllib.request.urlopen(req, timeout=40))
        except Exception:
            time.sleep(1.5)
    return {}


def pageimage(wiki, title):
    d = api(wiki, {"action": "query", "prop": "pageimages", "format": "json",
                   "piprop": "original", "redirects": "1", "titles": title})
    try:
        for p in d["query"]["pages"].values():
            if "missing" in p:
                continue
            s = p.get("original", {}).get("source")
            if s:
                return s
    except Exception:
        pass
    return None


def search_img(wiki, term):
    d = api(wiki, {"action": "query", "list": "search", "format": "json",
                   "srsearch": term, "srlimit": 4})
    try:
        cands = [r["title"] for r in d["query"]["search"]]
    except Exception:
        return None
    for c in cands:
        s = pageimage(wiki, c)
        if s:
            return s
    return None


def find(pid, rec):
    title = rec["wiki"]
    base = title.split(" (")[0]
    order = [GOT, IAF, AWO] if rec["show"] else [IAF, AWO, GOT]
    for wiki in order:
        s = pageimage(wiki, title)
        if s:
            return s
    if base != title:
        for wiki in order:
            s = pageimage(wiki, base)
            if s:
                return s
    terms = [title]
    if base != title:
        terms.append(base)
    if rec["name"] != title:
        terms.append(rec["name"])
    for t in terms:
        for wiki in order:
            s = search_img(wiki, t)
            if s:
                return s
    return None


def download(url, path):
    u = url.split("/revision/")[0]
    for cand in (u + "/revision/latest/scale-to-width-down/500", url, u):
        try:
            req = urllib.request.Request(cand, headers=UA)
            data = urllib.request.urlopen(req, timeout=60).read()
            if len(data) < 800:
                continue
            im = Image.open(io.BytesIO(data))
            im.load()
            open(path, "wb").write(data)
            return True
        except Exception:
            continue
    return False


def main():
    ids = list(D.P)
    miss = []
    for i, pid in enumerate(ids):
        rec = D.P[pid]
        dest = os.path.join(OUT, pid + ".img")
        if os.path.exists(dest) and os.path.getsize(dest) > 800:
            continue
        src = cache.get(pid)
        if not src:
            src = find(pid, rec)
            cache[pid] = src
            if i % 10 == 0:
                json.dump(cache, open(CACHE_F, "w"), indent=1)
        ok = download(src, dest) if src else False
        print(("OK   " if ok else "MISS ") + pid + "  " + rec["name"] + "  " + str(src)[:90], flush=True)
        if not ok:
            miss.append(pid)
    json.dump(cache, open(CACHE_F, "w"), indent=1)
    print("\n=== FALTANDO:", len(miss))
    for m in miss:
        print("   ", m, D.P[m]["name"], "| show=", D.P[m]["show"])
    json.dump(miss, open(os.path.join(os.path.dirname(__file__), "..", "missing.json"), "w"), indent=1)


if __name__ == "__main__":
    main()
