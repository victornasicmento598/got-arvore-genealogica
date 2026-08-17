# -*- coding: utf-8 -*-
"""Motor de layout das árvores genealógicas -> site/data.json"""
import os, sys, json
sys.path.insert(0, os.path.dirname(__file__))
import data_chars as D
import crowns

NODEW, NODEH = 150, 196
HGAP = 26            # espaço entre irmãos / cônjuges
UGAP = 60            # espaço entre grupos de filhos de uniões diferentes
ROWH = 300           # distância vertical entre gerações

ROOT = os.path.join(os.path.dirname(__file__), "..")

# Pessoas cujos descendentes NÃO são expandidos em determinada aba
# (evita que uma aba puxe a dinastia inteira por um casamento lateral).
STOPS = {
    "outras": {"aemma", "elia", "rhaelle", "lyanna", "catelyn", "cersei"},
    "akotsk": {"aerys2", "steffon_bar"},
    "hotd": {"viserys2", "daeron1", "baelor1", "daena", "rhaena_a3", "elaena"},
    "lannister": {"sansa"},
    "stark": {"rhaella_m"},
}


def compute_gens(members=None, unions=None):
    """Geração de cada pessoa.

    Cônjuges são fundidos em uma única unidade (union-find) para que casais
    fiquem sempre na mesma linha; a profundidade é o caminho mais longo
    pai->filho entre unidades. Assim irmãos permanecem alinhados mesmo quando
    um deles se casa em outro ramo da árvore.
    """
    pids = list(members) if members is not None else list(D.P)
    inset = set(pids)
    us = unions if unions is not None else list(range(len(D.U)))
    us = [i for i in us
          if (D.U[i]["a"] in inset or D.U[i]["b"] in inset
              or any(c in inset for c in D.U[i]["children"]))]

    par = {p: p for p in pids}

    def find(x):
        while par[x] != x:
            par[x] = par[par[x]]
            x = par[x]
        return x

    def join(x, y):
        rx, ry = find(x), find(y)
        if rx != ry:
            par[rx] = ry

    for i in us:
        u = D.U[i]
        if u["a"] in inset and u["b"] in inset:
            join(u["a"], u["b"])

    # arestas unidade-pai -> unidade-filho
    edges = set()
    for i in us:
        u = D.U[i]
        ps = [p for p in (u["a"], u["b"]) if p in inset]
        if not ps:
            continue
        pu = find(ps[0])
        for c in u["children"]:
            if c in inset and find(c) != pu:
                edges.add((pu, find(c)))

    # Propagação por BFS sobre o grafo de unidades (percorrido nos dois
    # sentidos): cada aresta impõe filho = pai + 1. Casamentos entre gerações
    # diferentes (tio/sobrinha, comuns entre os Targaryen) criam ciclos, então
    # vale a primeira atribuição e a aresta conflitante é apenas desenhada.
    adj = {}
    for a_, b_ in edges:
        adj.setdefault(a_, []).append((b_, 1))
        adj.setdefault(b_, []).append((a_, -1))

    units = list({find(p) for p in pids})
    ndesc = {u: 0 for u in units}
    for a_, b_ in edges:
        ndesc[a_] = ndesc.get(a_, 0) + 1
    depth = {}
    for start in sorted(units, key=lambda u: -ndesc.get(u, 0)):
        if start in depth:
            continue
        depth[start] = 0
        queue = [start]
        comp = [start]
        while queue:
            cur = queue.pop(0)
            for nxt, delta in adj.get(cur, ()):
                if nxt not in depth:
                    depth[nxt] = depth[cur] + delta
                    queue.append(nxt)
                    comp.append(nxt)
        lo = min(depth[u] for u in comp)
        for u in comp:
            depth[u] -= lo

    return {p: depth[find(p)] for p in pids}


GEN = compute_gens()


class L:
    __slots__ = ("nodes", "contour")

    def __init__(self):
        self.nodes = {}
        self.contour = {}

    def add(self, pid, x, d):
        self.nodes[pid] = (x, d)
        if d in self.contour:
            lo, hi = self.contour[d]
            self.contour[d] = (min(lo, x), max(hi, x + NODEW))
        else:
            self.contour[d] = (x, x + NODEW)

    def shift(self, dx):
        for k, (x, d) in self.nodes.items():
            self.nodes[k] = (x + dx, d)
        self.contour = {d: (a + dx, b + dx) for d, (a, b) in self.contour.items()}

    def absorb(self, o):
        self.nodes.update(o.nodes)
        for d, (a, b) in o.contour.items():
            if d in self.contour:
                lo, hi = self.contour[d]
                self.contour[d] = (min(lo, a), max(hi, b))
            else:
                self.contour[d] = (a, b)


def merge(units, gap):
    out = L()
    for u in units:
        if not u.nodes:
            continue
        if out.nodes:
            shared = set(out.contour) & set(u.contour)
            if shared:
                dx = max(out.contour[d][1] + gap - u.contour[d][0] for d in shared)
            else:
                dx = max(b for _, b in out.contour.values()) + gap - min(a for a, _ in u.contour.values())
            if dx:
                u.shift(dx)
        out.absorb(u)
    return out


class TabBuilder:
    def __init__(self, tab, gen=None):
        self.tab = tab
        self.gen = gen if gen is not None else GEN
        self.stops = STOPS.get(tab["id"], set())
        self.placed = {}          # pid -> (x, depth) final
        self.used_unions = set()
        self.marr = []            # (uidx)
        self.childlinks = []      # (uidx, child)
        # união primária de cada filho: preferir 'm'
        self.primary = {}
        for i, u in enumerate(D.U):
            for c in u["children"]:
                if c not in self.primary:
                    self.primary[c] = i
                elif u["kind"] == "m" and D.U[self.primary[c]]["kind"] != "m":
                    self.primary[c] = i

    def unions_of(self, pid):
        out = []
        for i, u in enumerate(D.U):
            if i in self.used_unions:
                continue
            if u["a"] == pid or u["b"] == pid:
                out.append(i)
        out.sort(key=lambda i: (D.U[i]["kind"] != "m", i))
        return out

    def build(self, pid):
        """Constrói o bloco familiar de pid: ele, seus cônjuges (e os cônjuges
        destes) na mesma linha, com todos os descendentes abaixo."""
        lay = L()
        if pid in self.placed:
            return lay

        # 1) cadeia horizontal de cônjuges, expandida transitivamente
        chain = [pid]
        self.placed[pid] = None
        unions = []                      # (uidx, a, b) na ordem de leitura
        i = 0
        while i < len(chain):
            person = chain[i]
            if person not in self.stops:
                for ui in self.unions_of(person):
                    self.used_unions.add(ui)
                    u = D.U[ui]
                    partner = u["b"] if u["a"] == person else u["a"]
                    if partner and partner not in self.placed:
                        self.placed[partner] = None
                        chain.append(partner)
                        unions.append((ui, person, partner))
                    elif partner and partner in chain:
                        unions.append((ui, person, partner))
                    else:
                        unions.append((ui, person, None))
            i += 1
        order = {p: k for k, p in enumerate(chain)}

        # 2) subárvores de filhos, na ordem das uniões
        groups = []
        for ui, a, b in unions:
            kids = [c for c in D.U[ui]["children"]
                    if self.primary.get(c) == ui and c not in self.placed]
            sub = merge([self.build(k) for k in kids], HGAP)
            if sub.nodes:
                groups.append((ui, a, b, sub, [k for k in kids if k in sub.nodes]))

        combined = merge([g[3] for g in groups], UGAP)
        lay.absorb(combined)

        centers = {}
        for ui, a, b, _sub, kids in groups:
            xs = [lay.nodes[k][0] + NODEW / 2 for k in kids]
            centers[ui] = sum(xs) / len(xs)

        # 3) a cadeia de cônjuges é mantida compacta (todos lado a lado) e
        # centrada sobre o conjunto dos filhos. Manter os casais adjacentes é
        # mais legível do que centrar cada pessoa sobre a própria prole, que
        # afastava cônjuges por milhares de pixels quando havia muitos filhos.
        chain_w = len(chain) * NODEW + (len(chain) - 1) * HGAP
        if centers:
            lo = min(centers.values())
            hi = max(centers.values())
            x0 = (lo + hi) / 2 - chain_w / 2
        else:
            x0 = 0.0
        for k, p in enumerate(chain):
            lay.add(p, x0 + k * (NODEW + HGAP), self.gen[p])
            self.placed[p] = True
        return lay

    def run(self):
        glob = L()
        for r in sorted(self.tab["roots"], key=lambda p: self.gen.get(p, 0)):
            if r in self.placed:
                continue
            u = self.build(r)
            if not u.nodes:
                continue
            glob = merge([glob, u], UGAP)
        for k, v in glob.nodes.items():
            self.placed[k] = v
        self.glob = glob
        return glob


def separate_rows(nodes, gen):
    """Passada final: elimina sobreposições residuais dentro de cada linha.

    A centralização das cadeias de cônjuges pode encostar dois blocos irmãos;
    aqui empurramos o excedente para a direita, preservando a ordem.
    """
    rows = {}
    for pid, (x, d) in nodes.items():
        rows.setdefault(d, []).append(pid)
    moved = 0
    for d, ids in rows.items():
        ids.sort(key=lambda p: nodes[p][0])
        for prev, cur in zip(ids, ids[1:]):
            need = nodes[prev][0] + NODEW + HGAP
            if nodes[cur][0] < need - 1:
                nodes[cur] = (need, d)
                moved += 1
    return moved


def build_tab(tab):
    # 1ª passada: descobre quem pertence à aba usando gerações globais
    probe = TabBuilder(tab)
    probe.run()
    members = set(probe.glob.nodes)
    uidx = [i for i, u in enumerate(D.U)
            if (u["a"] in members and u["b"] in members)
            or ((u["a"] in members or u["b"] in members)
                and any(c in members for c in u["children"]))]
    # 2ª passada: gerações recalculadas só com os membros da aba
    tb = TabBuilder(tab, compute_gens(members, uidx))
    g = tb.run()
    nodes = g.nodes
    if not nodes:
        return None
    for _ in range(4):
        if not separate_rows(nodes, tb.gen):
            break
    mind = min(d for _, d in nodes.values())
    minx = min(x for x, _ in nodes.values())
    out_nodes = []
    for pid, (x, d) in nodes.items():
        p = D.P[pid]
        out_nodes.append({
            "id": pid, "x": round(x - minx, 1), "y": (d - mind) * ROWH,
            "gen": d - mind,
            "name": p["name"], "nick": p["nick"], "house": p["house"],
            "life": p["life"], "titles": p["titles"], "actor": p["actor"],
            "show": p["show"], "note": p["note"], "sex": p["sex"],
            "crown": crowns.crown_of(pid, p["titles"]),
            "reign": crowns.REIGN_ORDER.get(pid),
        })
    pos = {n["id"]: n for n in out_nodes}
    marr, links = [], []
    seen = set()
    for i, u in enumerate(D.U):
        a, b = u["a"], u["b"]
        if a in pos and b in pos and i not in seen:
            seen.add(i)
            marr.append({"a": a, "b": b, "kind": u["kind"], "note": u["note"]})
        # ligações pai/mãe -> filho
        kids = [c for c in u["children"] if c in pos]
        if not kids:
            continue
        anchors = [p for p in (a, b) if p in pos]
        if not anchors:
            continue
        links.append({"p": anchors, "kids": kids, "kind": u["kind"]})
    return {"id": tab["id"], "label": tab["label"], "sub": tab["sub"],
            "nodes": out_nodes, "marriages": marr, "links": links}


def main():
    tabs = []
    for t in D.TREES:
        r = build_tab(t)
        if r:
            tabs.append(r)
            w = max(n["x"] for n in r["nodes"]) + NODEW
            h = max(n["y"] for n in r["nodes"]) + NODEH
            print("%-10s %3d nós  %5d x %4d px  %d gerações" %
                  (r["id"], len(r["nodes"]), w, h, max(n["gen"] for n in r["nodes"]) + 1))
    data = {"tabs": tabs, "nodew": NODEW, "nodeh": NODEH, "rowh": ROWH,
            "colors": {k.strip(): v for k, v in D.HOUSE_COLORS.items()}}
    os.makedirs(os.path.join(ROOT, "site"), exist_ok=True)
    with open(os.path.join(ROOT, "site", "data.json"), "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, separators=(",", ":"))
    tot = sum(len(t["nodes"]) for t in tabs)
    print("total de nós renderizados:", tot)


if __name__ == "__main__":
    main()
