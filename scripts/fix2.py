# -*- coding: utf-8 -*-
"""Segunda passada: busca por prefixo em allimages (mais confiável) + lista curada."""
import json, os, sys, time, urllib.request, urllib.parse, io
sys.path.insert(0, os.path.dirname(__file__))
import data_chars as D
from PIL import Image

UA = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/122 Safari/537.36"}
GOT = "https://gameofthrones.fandom.com/api.php"
IAF = "https://iceandfire.fandom.com/api.php"
ROOT = os.path.join(os.path.dirname(__file__), "..")
OUT = os.path.join(ROOT, "img_raw")
CACHE_F = os.path.join(ROOT, "img_sources.json")
cache = json.load(open(CACHE_F))

# (pid, wiki, prefixo em File:) — prefixo tem que ser bem específico
CURATED = {
    "viserys3":        [(GOT, "Viserys Targaryen")],
    "aegon_r":         [(IAF, "Young Griff"), (IAF, "Aegon VI")],
    "mya_stone":       [(IAF, "Mya Stone")],
    "edwyle":          [(IAF, "Edwyle")],
    "tygett":          [(IAF, "Tygett")],
    "gerion":          [(IAF, "Gerion")],
    "luthor_t":        [(IAF, "Luthor")],
    "alerie":          [(IAF, "Alerie")],
    "mellario":        [(IAF, "Mellario")],
    "melissa_bw":      [(IAF, "Melissa")],
    "barba_br":        [(IAF, "Barba")],
    "betha":           [(IAF, "Betha")],
    "shaera":          [(IAF, "Shaera")],
    "duncan_small":    [(IAF, "Duncan Targaryen"), (IAF, "Prince Duncan")],
    "aelinor":         [(IAF, "Aelinor")],
    "rohanne_bf":      [(IAF, "Rohanne")],
    "daemon_bf2":      [(IAF, "Daemon II")],
    "haegon_bf":       [(IAF, "Haegon")],
    "aegon_bf":        [(IAF, "Aegon Blackfyre")],
    "aemon_bf":        [(IAF, "Aemon Blackfyre")],
    "aemon_ja":        [(IAF, "Aemon Targaryen (son")],
    "rodrik_arryn":    [(IAF, "Rodrik Arryn")],
    "marilda":         [(IAF, "Marilda")],
    "valaena":         [(IAF, "Valaena")],
    "alyssa_v":        [(IAF, "Alyssa Velaryon")],
    "urrigon":         [(IAF, "Urrigon")],
    "matarys":         [(IAF, "Matarys")],
    "aelor":           [(IAF, "Aelor")],
    "aelora":          [(IAF, "Aelora")],
    "daenora":         [(IAF, "Daenora")],
    "rhae":            [(IAF, "Rhae Targaryen")],
    "daella_mk":       [(IAF, "Daella Targaryen (dau")],
    "shaena":          [(IAF, "Shaena")],
    "daenerys_a4":     [(IAF, "Daenerys Targaryen (dau")],
    "rhaena_a3":       [(IAF, "Rhaena Targaryen (dau")],
    "aegon_uncrowned": [(IAF, "Aegon Targaryen (son of Aenys")],
    "cassandra_b":     [(IAF, "Cassandra")],
    "floris_b":        [(IAF, "Floris")],
    "rickon_s_old":    [(IAF, "Rickon Stark (son")],
    "corlys_y":        [(IAF, "Corlys Velaryon (son")],
    "jaehaerys_ii_son": [(GOT, "Jaehaerys Targaryen")],
    "daeron_ae5":      [(IAF, "Daeron Targaryen (son of Aegon V")],
}


def api(u, p):
    q = urllib.parse.urlencode(p)
    r = urllib.request.Request(u + "?" + q, headers=UA)
    for _ in range(2):
        try:
            return json.load(urllib.request.urlopen(r, timeout=35))
        except Exception:
            time.sleep(1)
    return {}


def by_prefix(wiki, prefix):
    d = api(wiki, {"action": "query", "list": "allimages", "format": "json",
                   "aiprefix": prefix, "ailimit": 20, "aiprop": "url"})
    imgs = d.get("query", {}).get("allimages", [])
    best = None
    for im in imgs:
        n = im["name"].lower()
        if not n.endswith((".jpg", ".jpeg", ".png", ".webp")):
            continue
        # descarta banners/sigilos/logos
        if any(k in n for k in ("sigil", "shield", "banner", "logo", "house-", "house_")):
            continue
        return im["url"]
    return best


def download(url, path):
    u = url.split("/revision/")[0]
    for cand in (u + "/revision/latest/scale-to-width-down/500", url, u):
        try:
            req = urllib.request.Request(cand, headers=UA)
            data = urllib.request.urlopen(req, timeout=45).read()
            if len(data) < 800:
                continue
            Image.open(io.BytesIO(data)).load()
            open(path, "wb").write(data)
            return True
        except Exception:
            continue
    return False


def main():
    still = []
    for pid, tries in CURATED.items():
        got = None
        for wiki, pref in tries:
            got = by_prefix(wiki, pref)
            if got:
                break
        if got and download(got, os.path.join(OUT, pid + ".img")):
            cache[pid] = got
            print("FIX2 " + pid.ljust(18) + D.P[pid]["name"].ljust(28) + got.split("/")[-1].split("?")[0][:55], flush=True)
        else:
            still.append(pid)
            print("SIG  " + pid.ljust(18) + D.P[pid]["name"], flush=True)
    prev = json.load(open(os.path.join(ROOT, "need_sigil.json")))
    need = sorted(set(still) | (set(prev) - set(CURATED)))
    json.dump(cache, open(CACHE_F, "w"), indent=1)
    json.dump(need, open(os.path.join(ROOT, "need_sigil.json"), "w"), indent=1)
    print("\nAinda sem retrato:", len(need))
    for n in need:
        print("   ", n, D.P[n]["name"], "|", D.P[n]["house"])


if __name__ == "__main__":
    main()
