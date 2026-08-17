# -*- coding: utf-8 -*-
"""Corrige imagens que a busca automática atribuiu a pessoa errada.
Estratégia: busca em namespace File (ns=6) nas wikis por nome exato;
se não achar nada específico, gera um brasão heráldico local da casa.
"""
import json, os, sys, time, urllib.request, urllib.parse, io
sys.path.insert(0, os.path.dirname(__file__))
import data_chars as D
from PIL import Image

UA = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/122 Safari/537.36"}
WIKIS = ["https://iceandfire.fandom.com/api.php",
         "https://gameofthrones.fandom.com/api.php",
         "https://awoiaf.fandom.com/api.php"]
ROOT = os.path.join(os.path.dirname(__file__), "..")
OUT = os.path.join(ROOT, "img_raw")
CACHE_F = os.path.join(ROOT, "img_sources.json")
cache = json.load(open(CACHE_F))

# personagens cuja imagem automática ficou errada -> termos de busca em File:
FIX = {
    "viserys3":       ["Viserys Targaryen beggar king", "Viserys Targaryen"],   # GOT, Harry Lloyd
    "aegon_uncrowned": ["Aegon Targaryen son of Aenys", "Aegon the Uncrowned"],
    "aegon_ja":       [], "aegon_bal": [], "aegon_a2": [], "gaemon_ja": [], "valerion_ja": [],
    "aegon_r":        ["Aegon Targaryen son of Rhaegar", "Aegon VI"],
    "maegor_ae":      [], "vaella_a": [], "visenya_d": [], "rhaella_t": [],
    "aemon_ja":       ["Aemon Targaryen son of Jaehaerys"],
    "rodrik_arryn":   ["Rodrik Arryn"],
    "corlys_y":       ["Corlys Velaryon son of Alyn"],
    "jaehaerys_a2":   [], "jaehaerys_ii_son": ["Jaehaerys Targaryen son of Aegon II"],
    "marilda":        ["Marilda of Hull"],
    "melissa_bw":     ["Melissa Blackwood", "Missy Blackwood"],
    "barba_br":       ["Barba Bracken"],
    "rohanne_bf":     ["Rohanne of Tyrosh"],
    "daemon_bf2":     ["Daemon II Blackfyre"],
    "haegon_bf":      ["Haegon Blackfyre"],
    "aegon_bf":       ["Aegon Blackfyre"], "aemon_bf": ["Aemon Blackfyre"],
    "aelinor":        ["Aelinor Penrose"],
    "betha":          ["Betha Blackwood"],
    "duncan_small":   ["Duncan Targaryen dragonflies", "Prince Duncan Targaryen"],
    "shaera":         ["Shaera Targaryen"],
    "daeron_ae5":     ["Daeron Targaryen son of Aegon V"],
    "daeron_a2":      [],
    "edwyle":         ["Edwyle Stark"],
    "tygett":         ["Tygett Lannister"], "gerion": ["Gerion Lannister"],
    "mellario":       ["Mellario of Norvos"],
    "luthor_t":       ["Luthor Tyrell"],
    "alerie":         ["Alerie Hightower"],
    "valaena":        ["Valaena Velaryon"], "alyssa_v": ["Alyssa Velaryon"],
    "urrigon":        ["Urrigon Greyjoy"],
    "mya_stone":      ["Mya Stone"],
    "edmure_son":     [],
    "martell_parent": [],
    "shaena":         ["Shaena Targaryen"],
    "daenerys_a4":    ["Daenerys Targaryen daughter of Aegon IV"],
    "rhaena_a3":      ["Rhaena Targaryen daughter of Aegon III"],
    "aelor":          ["Aelor Targaryen"], "aelora": ["Aelora Targaryen"],
    "daenora":        ["Daenora Targaryen"],
    "matarys":        ["Matarys Targaryen"],
    "rhae":           ["Rhae Targaryen"], "daella_mk": ["Daella Targaryen daughter of Maekar"],
    "floris_b":       ["Floris Baratheon"], "cassandra_b": ["Cassandra Baratheon"],
    "rickon_s_old":   ["Rickon Stark son of Cregan"],
}


def api(url, params):
    q = urllib.parse.urlencode(params)
    req = urllib.request.Request(url + "?" + q, headers=UA)
    for _ in range(2):
        try:
            return json.load(urllib.request.urlopen(req, timeout=35))
        except Exception:
            time.sleep(1)
    return {}


def file_search(term):
    """Procura arquivos de imagem cujo título casa com o termo."""
    words = [w.lower() for w in term.split() if len(w) > 3]
    for wiki in WIKIS:
        d = api(wiki, {"action": "query", "list": "search", "format": "json",
                       "srsearch": term, "srnamespace": "6", "srlimit": 8})
        try:
            hits = [r["title"] for r in d["query"]["search"]]
        except Exception:
            continue
        for h in hits:
            t = h.lower()
            if not any(w in t for w in words[:1]):
                continue
            info = api(wiki, {"action": "query", "prop": "imageinfo", "format": "json",
                              "iiprop": "url", "titles": h})
            try:
                for p in info["query"]["pages"].values():
                    u = p["imageinfo"][0]["url"]
                    if u.lower().split("?")[0].endswith((".jpg", ".jpeg", ".png", ".webp")):
                        return u
            except Exception:
                continue
    return None


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
    unresolved = []
    for pid, terms in FIX.items():
        if pid not in D.P:
            continue
        got = None
        for t in terms:
            got = file_search(t)
            if got:
                break
        if got:
            if download(got, os.path.join(OUT, pid + ".img")):
                cache[pid] = got
                print("FIX  " + pid + "  " + D.P[pid]["name"] + "  " + got.split("/")[-1][:60], flush=True)
                continue
        unresolved.append(pid)
        print("SIGIL " + pid + "  " + D.P[pid]["name"], flush=True)
    json.dump(cache, open(CACHE_F, "w"), indent=1)
    json.dump(unresolved, open(os.path.join(ROOT, "need_sigil.json"), "w"), indent=1)
    print("\nSem retrato próprio (usarão brasão):", len(unresolved))


if __name__ == "__main__":
    main()
