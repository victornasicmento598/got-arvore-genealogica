(function () {
  "use strict";

  var D = null, TAB = null, NW = 150, NH = 196;
  var stage = document.getElementById("stage");
  var world = document.getElementById("world");
  var edges = document.getElementById("edges");
  var SVGNS = "http://www.w3.org/2000/svg";

  var view = { x: 0, y: 0, k: 1 };
  var MINK = 0.08, MAXK = 2.4;

  function apply() {
    world.style.transform =
      "translate(" + view.x + "px," + view.y + "px) scale(" + view.k + ")";
  }

  function clampK(k) { return Math.max(MINK, Math.min(MAXK, k)); }

  function zoomAt(cx, cy, factor) {
    var k = clampK(view.k * factor);
    var r = k / view.k;
    view.x = cx - (cx - view.x) * r;
    view.y = cy - (cy - view.y) * r;
    view.k = k;
    apply();
  }

  // ---------- desenho ----------
  function line(d, cls, from, to) {
    var p = document.createElementNS(SVGNS, "path");
    p.setAttribute("d", d);
    p.setAttribute("class", cls);
    p.setAttribute("fill", "none");
    if (from) p.setAttribute("data-from", from);
    if (to) p.setAttribute("data-to", to);
    return p;
  }

  function render(tab) {
    var i;
    TAB = tab;
    world.innerHTML = "";
    world.appendChild(edges);
    // preserva o <style> interno do SVG; remove apenas os traçados anteriores
    var old = edges.querySelectorAll("path");
    for (i = 0; i < old.length; i++) old[i].remove();

    var pos = {}, n;
    for (i = 0; i < tab.nodes.length; i++) pos[tab.nodes[i].id] = tab.nodes[i];

    var W = 0, H = 0;
    for (i = 0; i < tab.nodes.length; i++) {
      n = tab.nodes[i];
      if (n.x + NW > W) W = n.x + NW;
      if (n.y + NH > H) H = n.y + NH;
    }
    edges.setAttribute("width", W + 80);
    edges.setAttribute("height", H + 80);

    // linhas de descendência
    for (i = 0; i < tab.links.length; i++) {
      var l = tab.links[i];
      var ps = [], j;
      for (j = 0; j < l.p.length; j++) if (pos[l.p[j]]) ps.push(pos[l.p[j]]);
      if (!ps.length) continue;
      var px = 0, py = 0;
      for (j = 0; j < ps.length; j++) {
        px += ps[j].x + NW / 2;
        py = Math.max(py, ps[j].y + NH);
      }
      px /= ps.length;
      var bastard = l.kind === "b";
      var mid = py + (bastard ? 58 : 42);
      // tronco: pertence à linhagem se qualquer pai estiver realçado,
      // por isso recebe o 1º pai nas duas pontas
      edges.appendChild(line("M" + px + " " + py + "V" + mid,
        bastard ? "e b" : "e", ps[0].id, ps[0].id));
      for (j = 0; j < l.kids.length; j++) {
        var c = pos[l.kids[j]];
        if (!c) continue;
        var kx = c.x + NW / 2;
        var r = Math.min(14, Math.abs(kx - px) / 2);
        var dir = kx > px ? 1 : -1;
        var d = Math.abs(kx - px) < 1
          ? "M" + px + " " + mid + "V" + c.y
          : "M" + px + " " + mid +
            "H" + (kx - r * dir) +
            "q" + (r * dir) + " 0 " + (r * dir) + " " + r +
            "V" + c.y;
        edges.appendChild(line(d, bastard ? "e b" : "e", ps[0].id, c.id));
      }
    }

    // linhas de casamento
    for (i = 0; i < tab.marriages.length; i++) {
      var m = tab.marriages[i];
      var a = pos[m.a], b = pos[m.b];
      if (!a || !b || a.y !== b.y) continue;
      var x1 = Math.min(a.x, b.x) + NW, x2 = Math.max(a.x, b.x);
      var cls = m.kind === "b" ? "m b" : "m";
      var y = a.y + NH * 0.42;
      if (x2 - x1 <= 40) {
        // cônjuges lado a lado: traço curto entre os cartões
        edges.appendChild(line("M" + x1 + " " + y + "H" + x2, cls, m.a, m.b));
      } else {
        // distantes (vários casamentos): arco por cima, sem cruzar os cartões
        var top = a.y - 16, span = x2 - x1;
        var lift = Math.min(46, 14 + span / 26);
        edges.appendChild(line(
          "M" + (x1 - NW / 2) + " " + a.y +
          "C" + (x1 - NW / 2) + " " + (top - lift) + "," +
          (x2 + NW / 2) + " " + (top - lift) + "," +
          (x2 + NW / 2) + " " + a.y, cls + " arc", m.a, m.b));
      }
    }

    // cartões
    var frag = document.createDocumentFragment();
    for (i = 0; i < tab.nodes.length; i++) {
      frag.appendChild(card(tab.nodes[i]));
    }
    world.appendChild(frag);
    G = buildGraph(tab);
    focusId = null;
    setTimeout(applyFilters, 0);
    document.body.classList.remove("focusing");
    document.body.classList.remove("lineage-open");
    document.getElementById("lineage").classList.remove("on");
    fit();
  }

  function card(n) {
    var col = D.colors[n.house] || ["#6b5a3a", "#3a3020"];
    var el = document.createElement("div");
    el.className = "node" + (n.crown ? " crown-" + n.crown : "");
    el.style.left = n.x + "px";
    el.style.top = n.y + "px";
    el.setAttribute("data-id", n.id);

    var tag = n.show
      ? '<span class="tag">' + n.show + "</span>"
      : '<span class="tag" style="background:rgba(90,60,20,.72)">livros</span>';

    var CROWN = { sovereign: "\u265B", regional: "\u2654", consort: "\u2641" };
    var crown = n.crown
      ? '<span class="crown ' + n.crown + '" title="' +
        (n.crown === "sovereign"
          ? "Monarca dos Sete Reinos" + (n.reign ? " \u00b7 " + n.reign + "\u00ba a reinar" : "")
          : n.crown === "regional" ? "Rei/Rainha regional ou pretendente"
          : "Consorte coroado") + '">' + CROWN[n.crown] + "</span>"
      : "";

    el.innerHTML =
      '<div class="bar" style="background:linear-gradient(90deg,' + col[0] + "," + col[1] + ')"></div>' + crown +
      '<figure><img loading="lazy" src="img/t/' + n.id + '.jpg" alt="' + esc(n.name) + '">' + tag + "</figure>" +
      '<div class="txt"><div class="nm" role="button" tabindex="0">' + esc(n.name) + "</div>" +
      (n.nick ? '<div class="nk">' + esc(n.nick) + "</div>" : "") +
      (n.life ? '<div class="lf">' + esc(n.life) + "</div>" : "") +
      (n.actor ? '<div class="ac">' + esc(n.actor) + "</div>" : "") +
      "</div>";
    return el;
  }

  function esc(s) {
    return String(s == null ? "" : s).replace(/[&<>"]/g, function (c) {
      return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c];
    });
  }


  // ---------- grafo de parentesco da aba ----------
  // Reconstruído a cada troca de aba: pais/filhos vêm de tab.links,
  // cônjuges de tab.marriages. Guarda também o índice do link para
  // conseguir realçar exatamente as arestas certas no SVG.
  var G = null;

  function buildGraph(tab) {
    var g = { parents: {}, kids: {}, spouse: {}, byId: {}, linkOf: {} }, i, j;
    for (i = 0; i < tab.nodes.length; i++) {
      var id = tab.nodes[i].id;
      g.byId[id] = tab.nodes[i];
      g.parents[id] = []; g.kids[id] = []; g.spouse[id] = [];
    }
    for (i = 0; i < tab.links.length; i++) {
      var l = tab.links[i];
      for (j = 0; j < l.kids.length; j++) {
        var c = l.kids[j];
        if (!(c in g.parents)) continue;
        for (var p = 0; p < l.p.length; p++) {
          if (!(l.p[p] in g.kids)) continue;
          g.parents[c].push(l.p[p]);
          g.kids[l.p[p]].push(c);
        }
      }
    }
    for (i = 0; i < tab.marriages.length; i++) {
      var m = tab.marriages[i];
      if (m.a in g.spouse && m.b in g.spouse) {
        g.spouse[m.a].push(m.b);
        g.spouse[m.b].push(m.a);
      }
    }
    return g;
  }

  function walk(start, dir) {
    // dir: "parents" sobe (ascendentes), "kids" desce (descendentes).
    // BFS com visitados — a endogamia Targaryen cria ciclos e um DFS
    // ingênuo entraria em loop infinito.
    var seen = {}, out = [], queue = [start], depth = {};
    depth[start] = 0;
    while (queue.length) {
      var cur = queue.shift();
      var nxt = G[dir][cur] || [];
      for (var i = 0; i < nxt.length; i++) {
        var v = nxt[i];
        if (seen[v] || v === start) continue;
        seen[v] = 1; depth[v] = depth[cur] + 1;
        out.push(v); queue.push(v);
      }
    }
    return { ids: out, depth: depth };
  }

  var focusId = null;

  function clearFocus() {
    focusId = null;
    document.body.classList.remove("focusing");
    var els = world.querySelectorAll(".node");
    for (var i = 0; i < els.length; i++)
      els[i].className = els[i].className
        .replace(/\s*(hl-self|hl-anc|hl-desc|hl-spouse|dim|hl)\b/g, "");
    var ps = edges.querySelectorAll("path");
    for (i = 0; i < ps.length; i++)
      ps[i].setAttribute("class", ps[i].getAttribute("data-cls") || ps[i].getAttribute("class"));
    document.getElementById("lineage").classList.remove("on");
    document.body.classList.remove("lineage-open");
  }

  function focusLineage(id) {
    if (!G || !G.byId[id]) return;
    if (focusId === id) { clearFocus(); return; }
    focusId = id;

    var anc = walk(id, "parents"), desc = walk(id, "kids");
    var role = {};
    var i;
    for (i = 0; i < anc.ids.length; i++) role[anc.ids[i]] = "hl-anc";
    for (i = 0; i < desc.ids.length; i++) role[desc.ids[i]] = "hl-desc";
    var sp = G.spouse[id] || [];
    for (i = 0; i < sp.length; i++) if (!role[sp[i]]) role[sp[i]] = "hl-spouse";
    role[id] = "hl-self";

    document.body.classList.add("focusing");
    var els = world.querySelectorAll(".node");
    for (i = 0; i < els.length; i++) {
      var el = els[i], nid = el.getAttribute("data-id");
      el.className = el.className.replace(/\s*(hl-self|hl-anc|hl-desc|hl-spouse|dim|hl)\b/g, "");
      el.className += role[nid] ? " hl " + role[nid] : " dim";
    }

    // realça as arestas em que ambas as pontas estão na linhagem
    var ps = edges.querySelectorAll("path");
    for (i = 0; i < ps.length; i++) {
      var p = ps[i];
      if (!p.getAttribute("data-cls")) p.setAttribute("data-cls", p.getAttribute("class"));
      var base = p.getAttribute("data-cls");
      var f = p.getAttribute("data-from"), t = p.getAttribute("data-to");
      var on = f && t && (role[f] || f === id) && (role[t] || t === id);
      p.setAttribute("class", base + (on ? " lit" : " faded"));
    }

    showLineagePanel(id, anc, desc);
  }

  function personLine(n) {
    return esc(n.name) + (n.life ? ' <span class="d">' + esc(n.life) + "</span>" : "");
  }

  function showLineagePanel(id, anc, desc) {
    var n = G.byId[id], i;
    // caminho direto até o ancestral mais distante (sempre o 1º pai listado)
    var chain = [], cur = id, guard = 0;
    while (guard++ < 40) {
      var ps = G.parents[cur] || [];
      if (!ps.length) break;
      var pick = ps[0];
      for (var k = 0; k < ps.length; k++) if (G.byId[ps[k]].sex === "m") { pick = ps[k]; break; }
      chain.push(pick); cur = pick;
    }
    var kids = (G.kids[id] || []).slice();
    var sp = (G.spouse[id] || []);

    function list(ids, empty) {
      if (!ids.length) return '<div class="none">' + empty + "</div>";
      var out = "";
      for (var j = 0; j < ids.length; j++) {
        var p = G.byId[ids[j]];
        if (!p) continue;
        out += '<button class="ln" data-go="' + p.id + '">' + personLine(p) + "</button>";
      }
      return out;
    }

    document.getElementById("lnbody").innerHTML =
      '<div class="who"><b>' + esc(n.name) + "</b>" +
      (n.titles ? '<div class="t">' + esc(n.titles) + "</div>" : "") + "</div>" +
      '<div class="grp"><h4>Ascendência direta <em>(' + chain.length + ")</em></h4>" +
        list(chain, "Sem ascendentes registrados") + "</div>" +
      (sp.length ? '<div class="grp"><h4>Cônjuges</h4>' + list(sp, "") + "</div>" : "") +
      '<div class="grp"><h4>Filhos <em>(' + kids.length + ")</em></h4>" +
        list(kids, "Sem descendência registrada") + "</div>" +
      '<div class="grp tot"><span>' + anc.ids.length + " ascendentes</span>" +
        "<span>" + desc.ids.length + " descendentes</span></div>";
    document.getElementById("lineage").classList.add("on");
    document.body.classList.add("lineage-open");
  }

  document.getElementById("lnx").onclick = clearFocus;
  document.getElementById("lineage").addEventListener("click", function (e) {
    var b = e.target.closest ? e.target.closest("[data-go]") : null;
    if (b) { var t = b.getAttribute("data-go"); centerOn(t); focusLineage(t); }
  });

  function centerOn(id) {
    var n = G && G.byId[id];
    if (!n) return;
    var r = stage.getBoundingClientRect();
    var k = Math.max(view.k, 0.5);
    view.k = clampK(k);
    view.x = r.width / 2 - (n.x + NW / 2) * view.k;
    view.y = r.height / 2 - (n.y + NH / 2) * view.k;
    apply();
  }

  // ---------- lightbox ----------
  var lb = document.getElementById("lb");
  function openLB(id) {
    var n = null, i;
    for (i = 0; i < TAB.nodes.length; i++) if (TAB.nodes[i].id === id) n = TAB.nodes[i];
    if (!n) return;
    document.getElementById("lbimg").src = "img/f/" + n.id + ".jpg";
    var s = [];
    if (n.titles) s.push(n.titles);
    if (n.life) s.push(n.life);
    // selo de reinado: "1º a reinar", "24º a reinar"…
    var reign = n.reign
      ? '<div class="reign">\u265B ' + n.reign + "\u00ba monarca a sentar no Trono de Ferro</div>"
      : (n.crown === "regional"
          ? '<div class="reign reg">\u2654 Rei/Rainha regional ou pretendente ao trono</div>'
          : (n.crown === "consort" ? '<div class="reign con">\u2641 Consorte coroado</div>' : ""));

    document.getElementById("lbtx").innerHTML =
      "<h3>" + esc(n.name) + (n.nick ? " <em>" + esc(n.nick) + "</em>" : "") + "</h3>" + reign +
      '<div class="s">' + esc(s.join(" · ")) + "</div>" +
      (n.actor ? '<div class="s">Interpretado por ' + esc(n.actor) +
        (n.show ? " — " + esc(n.show) : "") + "</div>" : "") +
      (n.note ? '<div class="n">' + esc(n.note) + "</div>" : "");
    lb.classList.add("on");
  }
  function closeLB() { lb.classList.remove("on"); document.getElementById("lbimg").src = ""; }
  lb.addEventListener("click", closeLB);
  document.getElementById("lbin").addEventListener("click", function (e) { e.stopPropagation(); });
  document.getElementById("lbx").addEventListener("click", closeLB);
  document.addEventListener("keydown", function (e) { if (e.key === "Escape") closeLB(); });

  world.addEventListener("click", function (e) {
    if (moved || !e.target.closest) return;
    var nd = e.target.closest(".node");
    if (!nd) return;
    if (e.target.closest("figure")) openLB(nd.getAttribute("data-id"));
    else focusLineage(nd.getAttribute("data-id"));
  });

  // ---------- pan / zoom ----------
  var down = false, sx = 0, sy = 0, ox = 0, oy = 0, moved = false, pid = null;

  stage.addEventListener("pointerdown", function (e) {
    if (e.button !== 0 && e.pointerType === "mouse") return;
    down = true; moved = false;
    sx = e.clientX; sy = e.clientY; ox = view.x; oy = view.y;
    stage.classList.add("drag");
    pid = e.pointerId;
  });
  stage.addEventListener("pointermove", function (e) {
    if (!down) return;
    var dx = e.clientX - sx, dy = e.clientY - sy;
    if (Math.abs(dx) + Math.abs(dy) > 4 && !moved) {
      moved = true;
      // só captura o ponteiro depois que vira arrasto: capturar antes
      // faria o "click" ser entregue ao stage, matando o lightbox
      try { stage.setPointerCapture(pid); } catch (err) {}
    }
    view.x = ox + dx; view.y = oy + dy;
    apply();
  });
  function up(e) {
    down = false;
    stage.classList.remove("drag");
    try { stage.releasePointerCapture(e.pointerId); } catch (_) {}
    setTimeout(function () { moved = false; }, 0);
  }
  stage.addEventListener("pointerup", up);
  stage.addEventListener("pointercancel", up);

  stage.addEventListener("wheel", function (e) {
    e.preventDefault();
    var r = stage.getBoundingClientRect();
    zoomAt(e.clientX - r.left, e.clientY - r.top, Math.pow(0.999, e.deltaY * (e.ctrlKey ? 4 : 1.6)));
  }, { passive: false });

  // pinça (dois dedos)
  var pts = {}, pdist = 0;
  stage.addEventListener("pointerdown", function (e) { pts[e.pointerId] = e; });
  stage.addEventListener("pointermove", function (e) {
    if (!(e.pointerId in pts)) return;
    pts[e.pointerId] = e;
    var ks = Object.keys(pts);
    if (ks.length !== 2) return;
    down = false; stage.classList.remove("drag");
    var a = pts[ks[0]], b = pts[ks[1]];
    var dist = Math.hypot(a.clientX - b.clientX, a.clientY - b.clientY);
    var r = stage.getBoundingClientRect();
    var cx = (a.clientX + b.clientX) / 2 - r.left, cy = (a.clientY + b.clientY) / 2 - r.top;
    if (pdist) zoomAt(cx, cy, dist / pdist);
    pdist = dist;
  });
  function clr(e) { delete pts[e.pointerId]; if (Object.keys(pts).length < 2) pdist = 0; }
  stage.addEventListener("pointerup", clr);
  stage.addEventListener("pointercancel", clr);

  // ---------- enquadrar ----------
  function bounds() {
    var W = 0, H = 0, i;
    for (i = 0; i < TAB.nodes.length; i++) {
      if (TAB.nodes[i].x + NW > W) W = TAB.nodes[i].x + NW;
      if (TAB.nodes[i].y + NH > H) H = TAB.nodes[i].y + NH;
    }
    return { w: W, h: H };
  }
  function fit() {
    var b = bounds();
    var r = stage.getBoundingClientRect();
    var top = document.querySelector("header").offsetHeight + 12;
    var narrow = r.width < 760;
    var pad = narrow ? 12 : 40;
    var k = Math.min((r.width - pad) / b.w, (r.height - top - 60) / b.h);
    // em telas estreitas, caber a árvore inteira deixaria os cartões
    // ilegíveis: prioriza a largura e deixa o usuário rolar na vertical
    if (narrow) k = Math.max(k, Math.min(0.5, (r.width - pad) / b.w * 2.2));
    k = clampK(k);
    view.k = k;
    view.x = (r.width - b.w * k) / 2;
    // telas estreitas: ancora no topo em vez de centrar (evita faixa vazia)
    view.y = narrow ? top + 8
                    : top + Math.max(0, (r.height - top - 40 - b.h * k) / 2);
    apply();
  }

  document.getElementById("zin").onclick = function () {
    var r = stage.getBoundingClientRect();
    zoomAt(r.width / 2, r.height / 2, 1.3);
  };
  document.getElementById("zout").onclick = function () {
    var r = stage.getBoundingClientRect();
    zoomAt(r.width / 2, r.height / 2, 1 / 1.3);
  };
  document.getElementById("zfit").onclick = fit;

  var rt;
  window.addEventListener("resize", function () {
    clearTimeout(rt);
    rt = setTimeout(fit, 180);
  });


  // ---------- busca ----------
  // Índice global: procura em todas as abas, não só na visível, e
  // salta para a aba certa quando o resultado está em outra.
  var INDEX = [];

  function norm(t) {
    return String(t || "").toLowerCase()
      .normalize("NFD").replace(/[\u0300-\u036f]/g, "");
  }

  function buildIndex(d) {
    // Um personagem aparece em várias abas (Tyrion está na Targaryen só
    // como marido de Sansa, mas é na Lannister que tem pais e irmãos).
    // Escolhemos como destino a aba onde ele tem MAIS parentesco desenhado.
    var best = {}, i, j, k;
    for (i = 0; i < d.tabs.length; i++) {
      var t = d.tabs[i], score = {};
      for (j = 0; j < t.links.length; j++) {
        var l = t.links[j];
        for (k = 0; k < l.p.length; k++) score[l.p[k]] = (score[l.p[k]] || 0) + l.kids.length;
        for (k = 0; k < l.kids.length; k++) score[l.kids[k]] = (score[l.kids[k]] || 0) + 2;
      }
      for (j = 0; j < t.marriages.length; j++) {
        var m = t.marriages[j];
        score[m.a] = (score[m.a] || 0) + 1;
        score[m.b] = (score[m.b] || 0) + 1;
      }
      var lab = norm(t.label + " " + t.id);
      for (j = 0; j < t.nodes.length; j++) {
        var n = t.nodes[j];
        // empates são comuns (Sansa tem os mesmos pais na aba Stark e na
        // Targaryen); nesse caso vence a aba da casa dela.
        var sc = (score[n.id] || 0) * 10 +
                 (n.house && lab.indexOf(norm(n.house)) >= 0 ? 3 : 0) -
                 t.nodes.length / 1000;
        if (best[n.id] && best[n.id].sc >= sc) continue;
        best[n.id] = { n: n, tab: t.id, sc: sc };
      }
    }
    INDEX = [];
    for (var id in best) {
      var e = best[id], x = e.n;
      INDEX.push({
        id: x.id, tab: e.tab, name: x.name, house: x.house,
        crown: x.crown, life: x.life, show: x.show,
        hay: norm([x.name, x.nick, x.house, x.actor, x.titles].join(" "))
      });
    }
    INDEX.sort(function (a, b) { return a.name.localeCompare(b.name); });
  }

  var qEl = document.getElementById("q");
  var qres = document.getElementById("qres");
  var qsel = -1;

  function runSearch() {
    var v = norm(qEl.value.trim());
    document.getElementById("qx").style.display = v ? "block" : "none";
    if (v.length < 2) { qres.classList.remove("on"); qres.innerHTML = ""; return; }
    var hits = [], i;
    for (i = 0; i < INDEX.length && hits.length < 40; i++) {
      var it = INDEX[i], p = it.hay.indexOf(v);
      if (p < 0) continue;
      // posição do casamento: começo do nome > começo de outro campo > meio
      var nm = norm(it.name);
      // "aegon i" casa como prefixo tanto em "Aegon I" quanto em "Aegon II".
      // Desempate: o caractere seguinte precisa ser fim de palavra.
      var rank;
      if (nm === v) rank = -2;
      else if (nm.indexOf(v) === 0) {
        var nxt = nm.charAt(v.length);
        rank = (nxt === "" || nxt === " ") ? -1 : 0;
      } else rank = p === 0 ? 1 : 2;
      // desempate por proeminência: há 3 "Daenerys" e 6 "Aegon" no dataset;
      // quem reinou e quem aparece na TV deve vir primeiro
      var fame = (it.crown === "sovereign" ? 0 : it.crown ? 1 : 2) + (it.show ? 0 : 1);
      hits.push({ it: it, rank: rank, fame: fame });
    }
    hits.sort(function (a, b) {
      return a.rank - b.rank || a.fame - b.fame || a.it.name.localeCompare(b.it.name);
    });
    if (!hits.length) {
      qres.innerHTML = '<div class="empty">Nenhum personagem encontrado</div>';
      qres.classList.add("on"); return;
    }
    var CR = { sovereign: "\u265B", regional: "\u2654", consort: "\u2641" };
    var html = "";
    for (i = 0; i < hits.length; i++) {
      var n = hits[i].it;
      html += '<button class="qi" data-id="' + n.id + '" data-tab="' + n.tab + '">' +
        (n.crown ? '<span class="c ' + n.crown + '">' + CR[n.crown] + "</span>" : '<span class="c"></span>') +
        "<b>" + esc(n.name) + "</b>" +
        '<span class="h">' + (n.show ? '<i class="sh">' + esc(n.show) + "</i> " : "") +
        esc(n.house || "") + (n.life ? " \u00b7 " + esc(n.life) : "") + "</span></button>";
    }
    qres.innerHTML = html;
    qres.classList.add("on");
    qsel = -1;
  }

  function gotoResult(id, tabId) {
    qres.classList.remove("on");
    qEl.blur();
    if (TAB.id !== tabId) selectTab(tabId);
    setTimeout(function () { centerOn(id); focusLineage(id); }, 60);
  }

  qEl.addEventListener("input", runSearch);
  qEl.addEventListener("focus", function () { if (qEl.value.trim().length > 1) runSearch(); });
  qres.addEventListener("click", function (e) {
    var b = e.target.closest ? e.target.closest(".qi") : null;
    if (b) gotoResult(b.getAttribute("data-id"), b.getAttribute("data-tab"));
  });
  document.getElementById("qx").onclick = function () {
    qEl.value = ""; runSearch(); qEl.focus();
  };

  qEl.addEventListener("keydown", function (e) {
    var items = qres.querySelectorAll(".qi");
    if (e.key === "ArrowDown" || e.key === "ArrowUp") {
      e.preventDefault();
      if (!items.length) return;
      qsel += e.key === "ArrowDown" ? 1 : -1;
      if (qsel < 0) qsel = items.length - 1;
      if (qsel >= items.length) qsel = 0;
      for (var i = 0; i < items.length; i++) items[i].classList.toggle("sel", i === qsel);
      items[qsel].scrollIntoView({ block: "nearest" });
    } else if (e.key === "Enter") {
      var t = qsel >= 0 ? items[qsel] : items[0];
      if (t) gotoResult(t.getAttribute("data-id"), t.getAttribute("data-tab"));
    } else if (e.key === "Escape") {
      qEl.value = ""; runSearch(); qEl.blur();
    }
  });

  document.addEventListener("click", function (e) {
    if (!e.target.closest || !e.target.closest("#searchwrap")) qres.classList.remove("on");
  });

  // ---------- filtros ----------
  var filters = { crown: false, show: false };

  function applyFilters() {
    var els = world.querySelectorAll(".node"), i;
    for (i = 0; i < els.length; i++) {
      var n = G.byId[els[i].getAttribute("data-id")];
      var hide = (filters.crown && !n.crown) || (filters.show && !n.show);
      els[i].classList.toggle("off", !!hide);
    }
    document.body.classList.toggle("filtering", filters.crown || filters.show);
  }

  document.getElementById("tgcrown").onclick = function () {
    filters.crown = !filters.crown;
    this.classList.toggle("on", filters.crown);
    applyFilters();
  };
  document.getElementById("tgshow").onclick = function () {
    filters.show = !filters.show;
    this.classList.toggle("on", filters.show);
    applyFilters();
  };

  // ---------- atalhos ----------
  document.addEventListener("keydown", function (e) {
    if (e.target === qEl) return;
    if (e.key === "/") { e.preventDefault(); qEl.focus(); qEl.select(); }
    else if (e.key === "Escape") { clearFocus(); }
    else if (e.key === "+" || e.key === "=") document.getElementById("zin").click();
    else if (e.key === "-") document.getElementById("zout").click();
    else if (e.key === "0") fit();
  });

  // ---------- abas ----------
  function selectTab(id) {
    var t = null, i;
    for (i = 0; i < D.tabs.length; i++) if (D.tabs[i].id === id) t = D.tabs[i];
    if (!t) return;
    var bs = document.querySelectorAll("nav button");
    for (i = 0; i < bs.length; i++) bs[i].classList.toggle("on", bs[i].getAttribute("data-t") === id);
    document.getElementById("sub").textContent = t.sub;
    render(t);
    location.hash = id;
  }

  fetch("data.json").then(function (r) { return r.json(); }).then(function (d) {
    D = d; NW = d.nodew; NH = d.nodeh;
    buildIndex(d);
    var nav = document.querySelector("nav"), i;
    for (i = 0; i < d.tabs.length; i++) {
      var b = document.createElement("button");
      b.textContent = d.tabs[i].label.split("—")[0].trim();
      b.title = d.tabs[i].label;
      b.setAttribute("data-t", d.tabs[i].id);
      b.onclick = (function (id) { return function () { selectTab(id); }; })(d.tabs[i].id);
      nav.appendChild(b);
    }
    var start = location.hash.replace("#", "");
    var ok = false;
    for (i = 0; i < d.tabs.length; i++) if (d.tabs[i].id === start) ok = true;
    selectTab(ok ? start : d.tabs[0].id);
    setTimeout(function () {
      var h = document.getElementById("hint");
      if (h) { h.style.opacity = 0; }
    }, 6000);
  });
})();
