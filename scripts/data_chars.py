# -*- coding: utf-8 -*-
"""Base de dados de personagens — Game of Thrones / House of the Dragon /
A Knight of the Seven Kingdoms + linhagens dos livros (Fogo & Sangue, ASOIAF).

Campos:
  id, name, house, born/died (aprox., AC = Após a Conquista), titles(pt),
  actor (quando aparece em série), show (GOT|HOTD|AKOTSK|None), wiki (título p/ busca de imagem)
"""

P = {}          # pessoas
U = []          # uniões: (a, b, [filhos], kind)  kind: 'm'=casamento, 'b'=bastardo/união informal


def p(pid, name, house, life="", titles="", actor=None, show=None, wiki=None,
      gen=None, note="", sex="m", nick=""):
    P[pid] = dict(id=pid, name=name, nick=nick, house=house, life=life, titles=titles,
                  actor=actor, show=show, wiki=wiki or name, gen=gen, note=note, sex=sex)
    return pid


def u(a, b, children=(), kind="m", note=""):
    U.append(dict(a=a, b=b, children=list(children), kind=kind, note=note))


# ══════════════════════════════════════════════════════════════════
# CASA TARGARYEN — ancestrais e a Conquista
# ══════════════════════════════════════════════════════════════════
p("aerion_lord", "Aerion Targaryen", "Targaryen", "? – 27 AC", "Senhor de Pedra do Dragão",
  wiki="Aerion Targaryen (son of Daenys)", note="Pai de Aegon o Conquistador.")
p("valaena", "Valaena Velaryon", "Velaryon", "?", "Senhora de Pedra do Dragão", sex="f",
  wiki="Valaena Velaryon", note="Mãe de Aegon, Visenya e Rhaenys.")
p("visenya", "Visenya Targaryen", "Targaryen", "28 AC – 44 DC", "Rainha; montava Vhagar", sex="f",
  wiki="Visenya Targaryen")
p("aegon1", "Aegon I Targaryen", "Targaryen", "27 AC – 37 DC", "O Conquistador · 1º Rei dos Sete Reinos",
  nick="o Conquistador", wiki="Aegon I Targaryen")
p("rhaenys_c", "Rhaenys Targaryen", "Targaryen", "26 AC – 10 DC", "Rainha; montava Meraxes", sex="f",
  wiki="Rhaenys Targaryen (sister of Aegon I)")
p("orys", "Orys Baratheon", "Baratheon", "? – 38 DC", "1º Senhor de Ponta Tempestade · Mão do Rei",
  wiki="Orys Baratheon", note="Meio-irmão bastardo de Aegon I. Fundador da Casa Baratheon.")
p("argella", "Argella Durrandon", "Durrandon", "?", "Última da Casa Durrandon", sex="f",
  wiki="Argella Durrandon")

u("aerion_lord", "valaena", ["visenya", "aegon1", "rhaenys_c"])
u("aegon1", "visenya", ["maegor1"])
u("aegon1", "rhaenys_c", ["aenys1"])
u("orys", "argella", ["davos_b"])

# ── Filhos de Aegon I
p("aenys1", "Aenys I Targaryen", "Targaryen", "7 – 42 DC", "2º Rei dos Sete Reinos", wiki="Aenys I Targaryen")
p("maegor1", "Maegor I Targaryen", "Targaryen", "12 – 48 DC", "O Cruel · 3º Rei dos Sete Reinos",
  nick="o Cruel", wiki="Maegor I Targaryen")
p("alyssa_v", "Alyssa Velaryon", "Velaryon", "22 – 58 DC", "Rainha Consorte", sex="f", wiki="Alyssa Velaryon")
p("ceryse", "Ceryse Hightower", "Hightower", "? – 45 DC", "Rainha Consorte", sex="f", wiki="Ceryse Hightower")
p("alys_harroway", "Alys Harroway", "Harroway", "? – 44 DC", "Rainha Negra", sex="f", wiki="Alys Harroway")
p("tyanna", "Tyanna de Pentos", "—", "? – 45 DC", "A Bruxa de Pentos", sex="f", wiki="Tyanna of the Tower")
p("elinor", "Elinor Costayne", "Costayne", "?", "Rainha Consorte", sex="f", wiki="Elinor Costayne")

u("aenys1", "alyssa_v", ["rhaena_a", "aegon_uncrowned", "viserys_a", "jaehaerys1", "alysanne", "vaella_a"])
u("maegor1", "ceryse", [])
u("maegor1", "alys_harroway", [])
u("maegor1", "tyanna", [])
u("maegor1", "elinor", [])

p("rhaena_a", "Rhaena Targaryen", "Targaryen", "23 – 73 DC", "Rainha; montava Sonhofogo", sex="f",
  wiki="Rhaena Targaryen (daughter of Aenys I)")
p("aegon_uncrowned", "Aegon Targaryen", "Targaryen", "24 – 43 DC", "O Não-Coroado · Príncipe de Pedra do Dragão",
  nick="o Não-Coroado", wiki="Aegon Targaryen (son of Aenys I)")
p("viserys_a", "Viserys Targaryen", "Targaryen", "26 – 44 DC", "Príncipe", wiki="Viserys Targaryen (son of Aenys I)")
p("jaehaerys1", "Jaehaerys I Targaryen", "Targaryen", "34 – 103 DC", "O Conciliador · 4º Rei dos Sete Reinos",
  nick="o Conciliador", actor="Michael Carter", show="HOTD", wiki="Jaehaerys I Targaryen")
p("alysanne", "Alysanne Targaryen", "Targaryen", "36 – 100 DC", "A Boa Rainha", sex="f", wiki="Alysanne Targaryen")
p("vaella_a", "Vaella Targaryen", "Targaryen", "37 DC", "Princesa (morreu no berço)", sex="f", wiki="Vaella Targaryen")

u("aegon_uncrowned", "rhaena_a", ["aerea", "rhaella_t"])
u("maegor1", "rhaena_a", [], note="casamento forçado")
p("aerea", "Aerea Targaryen", "Targaryen", "43 – 56 DC", "Princesa", sex="f", wiki="Aerea Targaryen")
p("rhaella_t", "Rhaella Targaryen", "Targaryen", "43 – ? DC", "Septã", sex="f", wiki="Rhaella Targaryen (daughter of Aegon)")

# ── Jaehaerys I & Alysanne
u("jaehaerys1", "alysanne", ["aegon_ja", "daenerys_ja", "aemon_ja", "baelon", "alyssa_ja", "maegelle",
                             "vaegon", "daella", "saera", "viserra", "gaemon_ja", "valerion_ja", "gael"])
p("aegon_ja", "Aegon Targaryen", "Targaryen", "52 DC", "Príncipe (morreu no berço)", wiki="Aegon Targaryen (son of Jaehaerys I)")
p("daenerys_ja", "Daenerys Targaryen", "Targaryen", "55 – 62 DC", "Princesa", sex="f", wiki="Daenerys Targaryen (daughter of Jaehaerys I)")
p("aemon_ja", "Aemon Targaryen", "Targaryen", "55 – 92 DC", "Príncipe de Pedra do Dragão", wiki="Aemon Targaryen (son of Jaehaerys I)")
p("baelon", "Baelon Targaryen", "Targaryen", "57 – 101 DC", "O Bravo · Príncipe de Pedra do Dragão",
  nick="o Bravo", wiki="Baelon Targaryen")
p("alyssa_ja", "Alyssa Targaryen", "Targaryen", "60 – 84 DC", "Princesa", sex="f", wiki="Alyssa Targaryen (daughter of Jaehaerys I)")
p("maegelle", "Maegelle Targaryen", "Targaryen", "63 – 96 DC", "Septã", sex="f", wiki="Maegelle Targaryen")
p("vaegon", "Vaegon Targaryen", "Targaryen", "64 – ? DC", "O Dragão Sem Dragão · Grande Meistre", wiki="Vaegon Targaryen")
p("daella", "Daella Targaryen", "Targaryen", "66 – 82 DC", "Princesa", sex="f", wiki="Daella Targaryen")
p("saera", "Saera Targaryen", "Targaryen", "67 – ? DC", "Princesa exilada", sex="f", wiki="Saera Targaryen")
p("viserra", "Viserra Targaryen", "Targaryen", "74 – 90 DC", "Princesa", sex="f", wiki="Viserra Targaryen")
p("gaemon_ja", "Gaemon Targaryen", "Targaryen", "70 – 71 DC", "Príncipe", wiki="Gaemon Targaryen")
p("valerion_ja", "Valerion Targaryen", "Targaryen", "71 – 72 DC", "Príncipe", wiki="Valerion Targaryen")
p("gael", "Gael Targaryen", "Targaryen", "80 – 99 DC", "A Filha do Inverno", sex="f", wiki="Gael Targaryen")

p("jocelyn_b", "Jocelyn Baratheon", "Baratheon", "?", "Princesa Consorte", sex="f", wiki="Jocelyn Baratheon")
u("aemon_ja", "jocelyn_b", ["rhaenys_qwnw"])
u("baelon", "alyssa_ja", ["viserys1", "daemon", "aegon_bal"])
p("aegon_bal", "Aegon Targaryen", "Targaryen", "84 DC", "Príncipe (morreu no berço)", wiki="Aegon Targaryen (son of Baelon)")

p("rodrik_arryn", "Rodrik Arryn", "Arryn", "?", "Senhor do Ninho da Águia", wiki="Rodrik Arryn")
u("rodrik_arryn", "daella", ["aemma"])

# ══════════════════════════════════════════════════════════════════
# ERA DE HOUSE OF THE DRAGON
# ══════════════════════════════════════════════════════════════════
p("rhaenys_qwnw", "Rhaenys Targaryen", "Targaryen", "74 – 129 DC", "A Rainha Que Nunca Foi",
  nick="A Rainha Que Nunca Foi", actor="Eve Best", show="HOTD", sex="f",
  wiki="Rhaenys Targaryen (daughter of Aemon)")
p("corlys", "Corlys Velaryon", "Velaryon", "53 – 132 DC", "A Serpente do Mar · Senhor das Marés",
  nick="A Serpente do Mar", actor="Steve Toussaint", show="HOTD", wiki="Corlys Velaryon")
p("vaemond", "Vaemond Velaryon", "Velaryon", "? – 130 DC", "Comandante da frota Velaryon",
  actor="Wil Johnson", show="HOTD", wiki="Vaemond Velaryon")
u("corlys", "rhaenys_qwnw", ["laena", "laenor"])

p("viserys1", "Viserys I Targaryen", "Targaryen", "77 – 129 DC", "5º Rei dos Sete Reinos",
  actor="Paddy Considine", show="HOTD", wiki="Viserys I Targaryen")
p("aemma", "Aemma Arryn", "Arryn", "82 – 105 DC", "Rainha Consorte", sex="f",
  actor="Sian Brooke", show="HOTD", wiki="Aemma Arryn")
p("alicent", "Alicent Hightower", "Hightower", "88 – 131 DC", "Rainha Consorte · Rainha Viúva", sex="f",
  actor="Olivia Cooke / Emily Carey", show="HOTD", wiki="Alicent Hightower")
p("daemon", "Daemon Targaryen", "Targaryen", "81 – 130 DC", "Príncipe Canalha · Rei do Mar Estreito",
  nick="o Príncipe Canalha", actor="Matt Smith", show="HOTD", wiki="Daemon Targaryen", gen=None)
p("rhaenyra", "Rhaenyra Targaryen", "Targaryen", "97 – 130 DC", "A Rainha Negra · Princesa de Pedra do Dragão",
  nick="a Realeza Negra", actor="Emma D'Arcy / Milly Alcock", show="HOTD", sex="f", wiki="Rhaenyra Targaryen")

p("otto", "Otto Hightower", "Hightower", "? – 130 DC", "Mão do Rei",
  actor="Rhys Ifans", show="HOTD", wiki="Otto Hightower")
p("gwayne_h", "Gwayne Hightower", "Hightower", "?", "Ser · Cavaleiro de Vilavelha",
  actor="Freddie Fox", show="HOTD", wiki="Gwayne Hightower")
p("hobert_h", "Hobert Hightower", "Hightower", "? – 130 DC", "Senhor de Vilavelha",
  actor="Steffan Rhodri", show="HOTD", wiki="Hobert Hightower")
p("ormund_h", "Ormund Hightower", "Hightower", "? – 130 DC", "Senhor de Vilavelha",
  show="HOTD", wiki="Ormund Hightower")
u("otto", None, ["alicent"])
u(None, None, [], kind="m")  # placeholder ignorado
U.pop()
u("otto_father", None, [], kind="m")
U.pop()

u("viserys1", "aemma", ["rhaenyra", "baelon_son"])
p("baelon_son", "Baelon Targaryen", "Targaryen", "105 DC", "Príncipe (morreu no parto)",
  show="HOTD", wiki="Baelon Targaryen (son of Viserys I)")
u("viserys1", "alicent", ["aegon2", "helaena", "aemond", "daeron_v"])

p("aegon2", "Aegon II Targaryen", "Targaryen", "107 – 131 DC", "O Usurpador · 6º Rei dos Sete Reinos",
  actor="Tom Glynn-Carney", show="HOTD", wiki="Aegon II Targaryen")
p("helaena", "Helaena Targaryen", "Targaryen", "109 – 130 DC", "Rainha Consorte; montava Sonhofogo", sex="f",
  actor="Phia Saban", show="HOTD", wiki="Helaena Targaryen")
p("aemond", "Aemond Targaryen", "Targaryen", "110 – 130 DC", "O Caolho; montava Vhagar",
  nick="Caolho", actor="Ewan Mitchell", show="HOTD", wiki="Aemond Targaryen")
p("daeron_v", "Daeron Targaryen", "Targaryen", "114 – 131 DC", "O Ousado; montava Tessarion",
  show="HOTD", wiki="Daeron Targaryen (son of Viserys I)")

u("aegon2", "helaena", ["jaehaerys_ii_son", "jaehaera", "maelor"])
p("jaehaerys_ii_son", "Jaehaerys Targaryen", "Targaryen", "123 – 130 DC", "Príncipe herdeiro",
  show="HOTD", wiki="Jaehaerys Targaryen (son of Aegon II)")
p("jaehaera", "Jaehaera Targaryen", "Targaryen", "123 – 133 DC", "Rainha Consorte", sex="f",
  show="HOTD", wiki="Jaehaera Targaryen")
p("maelor", "Maelor Targaryen", "Targaryen", "127 – 130 DC", "Príncipe",
  wiki="Maelor Targaryen")

# Rhaenyra & Laenor / Daemon
p("laenor", "Laenor Velaryon", "Velaryon", "94 – 120 DC", "Príncipe consorte; montava Fogo do Mar",
  actor="John Macmillan", show="HOTD", wiki="Laenor Velaryon")
p("laena", "Laena Velaryon", "Velaryon", "93 – 120 DC", "Senhora; montava Vhagar", sex="f",
  actor="Nanna Blondell", show="HOTD", wiki="Laena Velaryon")
p("harwin", "Harwin Strong", "Strong", "? – 120 DC", "Quebra-Ossos · Comandante da Patrulha",
  nick="Quebra-Ossos", actor="Ryan Corr", show="HOTD", wiki="Harwin Strong")
p("lyonel_s", "Lyonel Strong", "Strong", "? – 120 DC", "Mão do Rei · Senhor de Harrenhal",
  actor="Gavin Spokes", show="HOTD", wiki="Lyonel Strong")
p("larys", "Larys Strong", "Strong", "? – 131 DC", "Pé Torto · Mestre dos Sussurros",
  nick="Pé Torto", actor="Matthew Needham", show="HOTD", wiki="Larys Strong")
p("criston", "Criston Cole", "Cole", "? – 130 DC", "Lorde Comandante da Guarda Real",
  actor="Fabien Frankel", show="HOTD", wiki="Criston Cole")
p("alys_rivers", "Alys Rivers", "Rivers", "?", "Feiticeira de Harrenhal", sex="f",
  actor="Gayle Rankin", show="HOTD", wiki="Alys Rivers")

u("lyonel_s", None, ["harwin", "larys"])
u("laenor", "rhaenyra", ["jacaerys", "lucerys", "joffrey_v"], note="filhos gerados por Harwin Strong")
u("harwin", "rhaenyra", ["jacaerys", "lucerys", "joffrey_v"], kind="b")
u("daemon", "laena", ["baela", "rhaena_d"])
u("daemon", "rhaenyra", ["aegon3", "viserys2", "visenya_d"])
p("rhea_royce", "Rhea Royce", "Royce", "? – 120 DC", "Senhora de Pedrarruna", sex="f",
  actor="Rachel Redford", show="HOTD", wiki="Rhea Royce")
u("daemon", "rhea_royce", [])
u("aemond", "alys_rivers", [], kind="b")

p("jacaerys", "Jacaerys Velaryon", "Velaryon", "114 – 130 DC", "Príncipe de Pedra do Dragão; montava Vermax",
  actor="Harry Collett", show="HOTD", wiki="Jacaerys Velaryon")
p("lucerys", "Lucerys Velaryon", "Velaryon", "115 – 129 DC", "Herdeiro de Derivamarca; montava Arrax",
  actor="Elliot Grihault", show="HOTD", wiki="Lucerys Velaryon")
p("joffrey_v", "Joffrey Velaryon", "Velaryon", "117 – 130 DC", "Príncipe; montava Tyraxes",
  show="HOTD", wiki="Joffrey Velaryon")
p("baela", "Baela Targaryen", "Targaryen", "116 – ? DC", "Senhora de Derivamarca; montava Dançarina da Lua", sex="f",
  actor="Bethany Antonia", show="HOTD", wiki="Baela Targaryen")
p("rhaena_d", "Rhaena Targaryen", "Targaryen", "116 – ? DC", "Senhora de Pedrarruna", sex="f",
  actor="Phoebe Campbell", show="HOTD", wiki="Rhaena Targaryen (daughter of Daemon)")
p("visenya_d", "Visenya Targaryen", "Targaryen", "129 DC", "Princesa (natimorta)", sex="f",
  show="HOTD", wiki="Visenya Targaryen (daughter of Daemon)")
p("aegon3", "Aegon III Targaryen", "Targaryen", "120 – 157 DC", "Veneno de Dragão · 7º Rei dos Sete Reinos",
  nick="Veneno de Dragão", show="HOTD", wiki="Aegon III Targaryen")
p("viserys2", "Viserys II Targaryen", "Targaryen", "122 – 172 DC", "10º Rei dos Sete Reinos",
  show="HOTD", wiki="Viserys II Targaryen")

# Velaryon bastardos / Hull
p("marilda", "Marilda de Casco", "—", "?", "Armadora de navios", sex="f", wiki="Marilda of Hull")
p("addam", "Addam Velaryon", "Velaryon", "114 – 130 DC", "Cavaleiro-dragão; montava Ladra de Ovelhas",
  actor="Clinton Liberty", show="HOTD", wiki="Addam of Hull")
p("alyn", "Alyn Velaryon", "Velaryon", "116 – ? DC", "Punho de Carvalho · Senhor das Marés",
  nick="Punho de Carvalho", actor="Abubakar Salim", show="HOTD", wiki="Alyn of Hull")
u("corlys", "marilda", ["addam", "alyn"], kind="b")
u("alyn", "baela", ["corlys_y"])
p("corlys_y", "Corlys Velaryon, o Jovem", "Velaryon", "?", "Senhor das Marés", wiki="Corlys Velaryon (son of Alyn)")

# Aliados/nobres HOTD
p("jason_l", "Jason Lannister", "Lannister", "? – 129 DC", "Senhor de Rochedo Casterly",
  actor="Jefferson Hall", show="HOTD", wiki="Jason Lannister")
p("tyland_l", "Tyland Lannister", "Lannister", "? – 131 DC", "Mão do Rei · Mestre da Moeda",
  actor="Jefferson Hall", show="HOTD", wiki="Tyland Lannister")
p("jeyne_arryn", "Jeyne Arryn", "Arryn", "? – 134 DC", "A Donzela do Vale · Senhora do Ninho da Águia", sex="f",
  actor="Amanda Collin", show="HOTD", wiki="Jeyne Arryn")
p("borros", "Borros Baratheon", "Baratheon", "? – 130 DC", "Senhor de Ponta Tempestade",
  actor="Roger Evans", show="HOTD", wiki="Borros Baratheon")
p("boremund", "Boremund Baratheon", "Baratheon", "? – 111 DC", "Senhor de Ponta Tempestade",
  actor="Julian Lewis Jones", show="HOTD", wiki="Boremund Baratheon")
p("floris_b", "Floris Baratheon", "Baratheon", "?", "Filha de Borros", sex="f", wiki="Floris Baratheon")
p("cassandra_b", "Cassandra Baratheon", "Baratheon", "?", "Filha mais velha de Borros", sex="f", wiki="Cassandra Baratheon")
u("boremund", None, ["borros"])
u("borros", None, ["cassandra_b", "floris_b"])
p("cregan_stark", "Cregan Stark", "Stark", "108 – ? DC", "Senhor de Winterfell · Mão do Rei (um dia)",
  actor="Tom Taylor", show="HOTD", wiki="Cregan Stark")
p("dalton_g", "Dalton Greyjoy", "Greyjoy", "? – 132 DC", "A Serpente Vermelha · Senhor das Ilhas de Ferro",
  nick="A Serpente Vermelha", show="HOTD", wiki="Dalton Greyjoy")
p("rickon_s_old", "Rickon Stark", "Stark", "?", "Senhor de Winterfell", wiki="Rickon Stark (son of Cregan)")
u("cregan_stark", None, ["rickon_s_old"])

# ══════════════════════════════════════════════════════════════════
# PÓS-DANÇA: Aegon III → Aegon IV
# ══════════════════════════════════════════════════════════════════
p("daenaera", "Daenaera Velaryon", "Velaryon", "126 – ? DC", "Rainha Consorte", sex="f", wiki="Daenaera Velaryon")
p("larra", "Larra Rogare", "Rogare", "121 – ? DC", "Princesa de Lys", sex="f", wiki="Larra Rogare")
u("aegon3", "jaehaera", [])
u("aegon3", "daenaera", ["daeron1", "baelor1", "daena", "rhaena_a3", "elaena"])
u("viserys2", "larra", ["aegon4", "aemon_dk", "naerys"])

p("daeron1", "Daeron I Targaryen", "Targaryen", "143 – 161 DC", "O Jovem Dragão · 8º Rei", nick="o Jovem Dragão",
  wiki="Daeron I Targaryen")
p("baelor1", "Baelor I Targaryen", "Targaryen", "144 – 171 DC", "O Abençoado · 9º Rei", nick="o Abençoado",
  wiki="Baelor I Targaryen")
p("daena", "Daena Targaryen", "Targaryen", "145 – 171 DC", "A Desafiadora", sex="f", nick="a Desafiadora",
  wiki="Daena Targaryen")
p("rhaena_a3", "Rhaena Targaryen", "Targaryen", "147 – ? DC", "Septã", sex="f",
  wiki="Rhaena Targaryen (daughter of Aegon III)")
p("elaena", "Elaena Targaryen", "Targaryen", "150 – ? DC", "Princesa", sex="f", wiki="Elaena Targaryen")
u("baelor1", "daena", [])

p("aegon4", "Aegon IV Targaryen", "Targaryen", "135 – 184 DC", "O Indigno · 11º Rei", nick="o Indigno",
  wiki="Aegon IV Targaryen")
p("aemon_dk", "Aemon Targaryen", "Targaryen", "136 – 183 DC", "O Cavaleiro-Dragão", nick="o Cavaleiro-Dragão",
  wiki="Aemon Targaryen (Dragonknight)")
p("naerys", "Naerys Targaryen", "Targaryen", "138 – 179 DC", "Rainha Consorte", sex="f", wiki="Naerys Targaryen")
u("aegon4", "naerys", ["daeron2", "daenerys_a4"])
p("daenerys_a4", "Daenerys Targaryen", "Targaryen", "172 – ? DC", "Princesa de Dorne", sex="f",
  wiki="Daenerys Targaryen (daughter of Aegon IV)")

# Os Grandes Bastardos
p("melissa_bw", "Melissa Blackwood", "Blackwood", "?", "Amante real", sex="f", wiki="Melissa Blackwood")
p("barba_br", "Barba Bracken", "Bracken", "?", "Amante real", sex="f", wiki="Barba Bracken")
p("serenei", "Serenei de Lys", "—", "?", "Amante real", sex="f", wiki="Serenei of Lys")
p("daemon_bf", "Daemon Blackfyre", "Blackfyre", "170 – 196 DC", "O Dragão Negro · 1º Pretendente",
  nick="o Dragão Negro", wiki="Daemon Blackfyre")
p("bloodraven", "Brynden Rivers", "Rivers", "175 – ? DC", "Corvo de Sangue · Mão do Rei · Corvo de Três Olhos",
  nick="Corvo de Sangue", actor="Struan Rodger / Max von Sydow", show="GOT", wiki="Brynden Rivers")
p("bittersteel", "Aegor Rivers", "Rivers", "172 – ? DC", "Aço Amargo · Fundador da Companhia Dourada",
  nick="Aço Amargo", wiki="Aegor Rivers")
p("shiera", "Shiera Seastar", "Rivers", "178 – ? DC", "Estrela do Mar", sex="f", wiki="Shiera Seastar")
u("aegon4", "daena", ["daemon_bf"], kind="b")
u("aegon4", "melissa_bw", ["bloodraven"], kind="b")
u("aegon4", "barba_br", ["bittersteel"], kind="b")
u("aegon4", "serenei", ["shiera"], kind="b")
p("rohanne_bf", "Rohanne de Tyrosh", "—", "?", "Esposa de Daemon Blackfyre", sex="f", wiki="Rohanne of Tyrosh")
p("aegon_bf", "Aegon Blackfyre", "Blackfyre", "? – 196 DC", "Filho de Daemon", wiki="Aegon Blackfyre")
p("aemon_bf", "Aemon Blackfyre", "Blackfyre", "? – 196 DC", "Filho de Daemon", wiki="Aemon Blackfyre")
p("daemon_bf2", "Daemon II Blackfyre", "Blackfyre", "?", "2º Pretendente Negro", wiki="Daemon II Blackfyre")
p("haegon_bf", "Haegon Blackfyre", "Blackfyre", "?", "Pretendente Negro", wiki="Haegon Blackfyre")
u("daemon_bf", "rohanne_bf", ["aegon_bf", "aemon_bf", "daemon_bf2", "haegon_bf"])

# ══════════════════════════════════════════════════════════════════
# ERA DE "O CAVALEIRO DOS SETE REINOS"
# ══════════════════════════════════════════════════════════════════
p("daeron2", "Daeron II Targaryen", "Targaryen", "153 – 209 DC", "O Bom · 12º Rei dos Sete Reinos",
  nick="o Bom", wiki="Daeron II Targaryen")
p("myriah", "Myriah Martell", "Martell", "?", "Rainha Consorte · Princesa de Dorne", sex="f", wiki="Myriah Martell")
u("daeron2", "myriah", ["baelor_bs", "aerys1", "rhaegel", "maekar", "maekar_sister"])
P.pop("maekar_sister", None)
U[-1]["children"] = ["baelor_bs", "aerys1", "rhaegel", "maekar"]

p("baelor_bs", "Baelor Targaryen", "Targaryen", "170 – 209 DC", "Quebra-Lanças · Príncipe herdeiro · Mão do Rei",
  nick="Quebra-Lanças", actor="Bertie Carvel", show="AKOTSK", wiki="Baelor Targaryen (son of Daeron II)")
p("aerys1", "Aerys I Targaryen", "Targaryen", "171 – 233 DC", "13º Rei dos Sete Reinos",
  wiki="Aerys I Targaryen")
p("rhaegel", "Rhaegel Targaryen", "Targaryen", "173 – 215 DC", "Príncipe (dito louco)", wiki="Rhaegel Targaryen")
p("maekar", "Maekar I Targaryen", "Targaryen", "175 – 233 DC", "A Bigorna · 14º Rei dos Sete Reinos",
  nick="a Bigorna", actor="Sam Spruell", show="AKOTSK", wiki="Maekar Targaryen")

p("jena_d", "Jena Dondarrion", "Dondarrion", "?", "Princesa Consorte", sex="f", wiki="Jena Dondarrion")
p("aelinor", "Aelinor Penrose", "Penrose", "?", "Rainha Consorte", sex="f", wiki="Aelinor Penrose")
p("alys_arryn", "Alys Arryn", "Arryn", "?", "Princesa Consorte", sex="f", wiki="Alys Arryn")
p("dyanna", "Dyanna Dayne", "Dayne", "?", "Princesa Consorte", sex="f", wiki="Dyanna Dayne")
u("baelor_bs", "jena_d", ["valarr", "matarys"])
u("aerys1", "aelinor", [])
u("rhaegel", "alys_arryn", ["aelor", "aelora", "daenora"])
u("maekar", "dyanna", ["daeron_dr", "aerion", "aemon_maester", "aegon5", "daella_mk", "rhae"])

p("valarr", "Valarr Targaryen", "Targaryen", "183 – 209 DC", "O Jovem Príncipe",
  actor="Oscar Morgan", show="AKOTSK", wiki="Valarr Targaryen")
p("matarys", "Matarys Targaryen", "Targaryen", "? – 209 DC", "O Príncipe Que Nunca Foi", wiki="Matarys Targaryen")
p("aelor", "Aelor Targaryen", "Targaryen", "?", "Príncipe", wiki="Aelor Targaryen")
p("aelora", "Aelora Targaryen", "Targaryen", "?", "Princesa", sex="f", wiki="Aelora Targaryen")
p("daenora", "Daenora Targaryen", "Targaryen", "?", "Princesa", sex="f", wiki="Daenora Targaryen")
p("daeron_dr", "Daeron Targaryen", "Targaryen", "190 – 219 DC", "O Bêbado", nick="o Bêbado",
  actor="Henry Ashton", show="AKOTSK", wiki="Daeron Targaryen (son of Maekar)")
p("aerion", "Aerion Targaryen", "Targaryen", "191 – 232 DC", "Chama Clara · Príncipe", nick="Chama Clara",
  actor="Finn Bennett", show="AKOTSK", wiki="Aerion Targaryen")
p("aemon_maester", "Aemon Targaryen", "Targaryen", "198 – 300 DC", "Meistre da Patrulha da Noite",
  actor="Peter Vaughan", show="GOT", wiki="Aemon Targaryen")
p("aegon5", "Aegon V Targaryen", "Targaryen", "200 – 259 DC", "Ovo · O Improvável · 15º Rei", nick="Ovo",
  actor="Dexter Sol Ansell", show="AKOTSK", wiki="Egg")
p("daella_mk", "Daella Targaryen", "Targaryen", "?", "Princesa", sex="f", wiki="Daella Targaryen (daughter of Maekar)")
p("rhae", "Rhae Targaryen", "Targaryen", "?", "Princesa", sex="f", wiki="Rhae Targaryen")
p("maegor_ae", "Maegor Targaryen", "Targaryen", "?", "Filho de Aerion", wiki="Maegor Targaryen (son of Aerion)")
u("aerion", None, ["maegor_ae"])

# Companheiros de Dunk & Ovo
p("dunk", "Duncan, o Alto", "—", "192 – 259 DC", "Ser · Lorde Comandante da Guarda Real",
  nick="Dunk", actor="Peter Claffey", show="AKOTSK", wiki="Duncan the Tall")
p("arlan", "Arlan de Pennytree", "—", "? – 209 DC", "Cavaleiro errante",
  actor="Danny Webb", show="AKOTSK", wiki="Arlan of Pennytree")
p("tanselle", "Tanselle", "—", "?", "Titeriteira de Dorne", sex="f",
  actor="Tanzyn Crawford", show="AKOTSK", wiki="Tanselle")
p("lyonel_bar", "Lyonel Baratheon", "Baratheon", "?", "A Tempestade Risonha · Senhor de Ponta Tempestade",
  nick="A Tempestade Risonha", actor="Daniel Ings", show="AKOTSK", wiki="Lyonel Baratheon")
p("steffon_f", "Steffon Fossoway", "Fossoway", "?", "Ser · herdeiro de Pomar",
  actor="Edward Ashley", show="AKOTSK", wiki="Steffon Fossoway")
p("raymun_f", "Raymun Fossoway", "Fossoway", "?", "Ser · Maçã Verde",
  actor="Shaun Thomas", show="AKOTSK", wiki="Raymun Fossoway")
p("manfred_d", "Manfred Dondarrion", "Dondarrion", "?", "Ser de Refúgio Negro",
  actor="Daniel Monks", show="AKOTSK", wiki="Manfred Dondarrion")
p("humfrey_h", "Humfrey Hardyng", "Hardyng", "?", "Ser",
  actor="Ross Anderson", show="AKOTSK", wiki="Humfrey Hardyng")
p("steely_pate", "Pate de Aço", "—", "?", "Ferreiro-armeiro",
  actor="Youssef Kerkour", show="AKOTSK", wiki="Steely Pate")
p("plummer", "Plummer", "—", "?", "Mordomo de Ashford",
  actor="Tom Vaughan-Lawlor", show="AKOTSK", wiki="Plummer")

# ══════════════════════════════════════════════════════════════════
# AEGON V → A REBELIÃO DE ROBERT
# ══════════════════════════════════════════════════════════════════
p("betha", "Betha Blackwood", "Blackwood", "?", "Rainha Consorte · Corvo Negro", sex="f", wiki="Betha Blackwood")
u("aegon5", "betha", ["duncan_small", "jaehaerys2", "shaera", "daeron_ae5", "rhaelle"])
p("duncan_small", "Duncan Targaryen", "Targaryen", "? – 259 DC", "O Príncipe das Libélulas",
  nick="Príncipe das Libélulas", wiki="Duncan Targaryen")
p("jenny", "Jenny de Pedrasvelhas", "—", "?", "Amada do Príncipe Duncan", sex="f", wiki="Jenny of Oldstones")
u("duncan_small", "jenny", [])
p("jaehaerys2", "Jaehaerys II Targaryen", "Targaryen", "225 – 262 DC", "16º Rei dos Sete Reinos",
  wiki="Jaehaerys II Targaryen")
p("shaera", "Shaera Targaryen", "Targaryen", "226 – ? DC", "Rainha Consorte", sex="f", wiki="Shaera Targaryen")
p("daeron_ae5", "Daeron Targaryen", "Targaryen", "?", "Príncipe", wiki="Daeron Targaryen (son of Aegon V)")
p("rhaelle", "Rhaelle Targaryen", "Targaryen", "?", "Senhora de Ponta Tempestade", sex="f", wiki="Rhaelle Targaryen")
u("jaehaerys2", "shaera", ["aerys2", "rhaella"])

p("ormund_bar", "Ormund Baratheon", "Baratheon", "? – 260 DC", "Senhor de Ponta Tempestade", wiki="Ormund Baratheon")
u("ormund_bar", "rhaelle", ["steffon_bar"])

p("aerys2", "Aerys II Targaryen", "Targaryen", "244 – 283 DC", "O Rei Louco · 17º Rei", nick="o Rei Louco",
  actor="David Rintoul", show="GOT", wiki="Aerys II Targaryen")
p("rhaella", "Rhaella Targaryen", "Targaryen", "245 – 284 DC", "Rainha Consorte", sex="f", wiki="Rhaella Targaryen")
u("aerys2", "rhaella", ["rhaegar", "shaena", "daeron_a2", "aegon_a2", "jaehaerys_a2", "viserys3", "daenerys"])
p("shaena", "Shaena Targaryen", "Targaryen", "?", "Princesa", sex="f", wiki="Shaena Targaryen")
p("daeron_a2", "Daeron Targaryen", "Targaryen", "?", "Príncipe", wiki="Daeron Targaryen (son of Aerys II)")
p("aegon_a2", "Aegon Targaryen", "Targaryen", "?", "Príncipe", wiki="Aegon Targaryen (son of Aerys II)")
p("jaehaerys_a2", "Jaehaerys Targaryen", "Targaryen", "?", "Príncipe", wiki="Jaehaerys Targaryen (son of Aerys II)")

p("rhaegar", "Rhaegar Targaryen", "Targaryen", "259 – 283 DC", "Príncipe de Pedra do Dragão",
  actor="Wilf Scolding", show="GOT", wiki="Rhaegar Targaryen")
p("viserys3", "Viserys Targaryen", "Targaryen", "276 – 298 DC", "O Rei Mendigo", nick="Rei Mendigo",
  actor="Harry Lloyd", show="GOT", wiki="Viserys Targaryen")
p("daenerys", "Daenerys Targaryen", "Targaryen", "284 – 305 DC", "Mãe dos Dragões · A Não-Queimada", sex="f",
  nick="Mãe dos Dragões", actor="Emilia Clarke", show="GOT", wiki="Daenerys Targaryen")
p("elia", "Elia Martell", "Martell", "257 – 283 DC", "Princesa de Dorne", sex="f",
  actor="Indira Varma (voz)", show="GOT", wiki="Elia Martell")
p("rhaenys_r", "Rhaenys Targaryen", "Targaryen", "280 – 283 DC", "Princesa", sex="f",
  wiki="Rhaenys Targaryen (daughter of Rhaegar)")
p("aegon_r", "Aegon Targaryen", "Targaryen", "281 – 283 DC", "Príncipe de Pedra do Dragão",
  wiki="Aegon Targaryen (son of Rhaegar)")
u("rhaegar", "elia", ["rhaenys_r", "aegon_r"])
u("rhaegar", "lyanna", ["jon_snow"])
p("drogo", "Khal Drogo", "Dothraki", "? – 298 DC", "Khal dos Dothraki",
  actor="Jason Momoa", show="GOT", wiki="Drogo")
p("rhaego", "Rhaego", "Dothraki", "298 DC", "O Garanhão Que Monta o Mundo", wiki="Rhaego")
u("drogo", "daenerys", ["rhaego"])

# ══════════════════════════════════════════════════════════════════
# CASA STARK
# ══════════════════════════════════════════════════════════════════
p("edwyle", "Edwyle Stark", "Stark", "?", "Senhor de Winterfell", wiki="Edwyle Stark")
p("rickard_s", "Rickard Stark", "Stark", "? – 282 DC", "Senhor de Winterfell",
  actor="Andrew Wilde", show="GOT", wiki="Rickard Stark")
p("lyarra", "Lyarra Stark", "Stark", "?", "Senhora de Winterfell", sex="f", wiki="Lyarra Stark")
u("edwyle", None, ["rickard_s"])
u("rickard_s", "lyarra", ["brandon_s", "eddard", "lyanna", "benjen"])
p("brandon_s", "Brandon Stark", "Stark", "262 – 282 DC", "Herdeiro de Winterfell",
  show="GOT", wiki="Brandon Stark (son of Rickard)")
p("eddard", "Eddard Stark", "Stark", "263 – 298 DC", "Ned · Senhor de Winterfell · Mão do Rei",
  nick="Ned", actor="Sean Bean", show="GOT", wiki="Eddard Stark")
p("lyanna", "Lyanna Stark", "Stark", "266 – 283 DC", "A Rosa de Inverno", sex="f",
  actor="Aisling Franciosi", show="GOT", wiki="Lyanna Stark")
p("benjen", "Benjen Stark", "Stark", "267 – ? DC", "Primeiro Patrulheiro da Patrulha da Noite",
  actor="Joseph Mawle", show="GOT", wiki="Benjen Stark")
p("catelyn", "Catelyn Tully", "Tully", "264 – 299 DC", "Senhora de Winterfell", sex="f",
  actor="Michelle Fairley", show="GOT", wiki="Catelyn Stark")
u("eddard", "catelyn", ["robb", "sansa", "arya", "bran", "rickon"])
p("robb", "Robb Stark", "Stark", "283 – 299 DC", "O Jovem Lobo · Rei do Norte", nick="o Jovem Lobo",
  actor="Richard Madden", show="GOT", wiki="Robb Stark")
p("sansa", "Sansa Stark", "Stark", "286 – ? DC", "Rainha no Norte", sex="f",
  actor="Sophie Turner", show="GOT", wiki="Sansa Stark")
p("arya", "Arya Stark", "Stark", "289 – ? DC", "Princesa · Homem Sem Rosto", sex="f",
  actor="Maisie Williams", show="GOT", wiki="Arya Stark")
p("bran", "Brandon Stark", "Stark", "290 – ? DC", "Bran, o Quebrado · Corvo de Três Olhos · Rei",
  nick="o Quebrado", actor="Isaac Hempstead Wright", show="GOT", wiki="Bran Stark")
p("rickon", "Rickon Stark", "Stark", "295 – 303 DC", "Príncipe de Winterfell",
  actor="Art Parkinson", show="GOT", wiki="Rickon Stark")
p("jon_snow", "Jon Snow", "Stark", "283 – ? DC", "Aegon Targaryen · Rei do Norte · Lorde Comandante",
  nick="Aegon Targaryen", actor="Kit Harington", show="GOT", wiki="Jon Snow")
p("talisa", "Talisa Maegyr", "Maegyr", "? – 299 DC", "Rainha do Norte", sex="f",
  actor="Oona Chaplin", show="GOT", wiki="Talisa Stark")
u("robb", "talisa", [])

# ══════════════════════════════════════════════════════════════════
# CASA TULLY / ARRYN
# ══════════════════════════════════════════════════════════════════
p("hoster", "Hoster Tully", "Tully", "? – 300 DC", "Senhor de Correrio",
  actor="Chris Newman", show="GOT", wiki="Hoster Tully")
p("minisa", "Minisa Whent", "Whent", "?", "Senhora de Correrio", sex="f", wiki="Minisa Tully")
p("blackfish", "Brynden Tully", "Tully", "?", "O Peixe Preto", nick="Peixe Preto",
  actor="Clive Russell", show="GOT", wiki="Brynden Tully")
u("hoster", "minisa", ["catelyn", "lysa", "edmure"])
p("lysa", "Lysa Tully", "Tully", "266 – 300 DC", "Senhora do Ninho da Águia", sex="f",
  actor="Kate Dickie", show="GOT", wiki="Lysa Arryn")
p("edmure", "Edmure Tully", "Tully", "?", "Senhor de Correrio",
  actor="Tobias Menzies", show="GOT", wiki="Edmure Tully")
p("roslin", "Roslin Frey", "Frey", "?", "Senhora de Correrio", sex="f",
  actor="Alexandra Dowling", show="GOT", wiki="Roslin Frey")
u("edmure", "roslin", ["edmure_son"])
p("edmure_son", "Filho de Edmure", "Tully", "300 DC", "Herdeiro de Correrio", wiki="Tully")
p("jon_arryn", "Jon Arryn", "Arryn", "? – 298 DC", "Senhor do Ninho da Águia · Mão do Rei",
  actor="John Standing", show="GOT", wiki="Jon Arryn")
p("robin_arryn", "Robin Arryn", "Arryn", "?", "Senhor do Ninho da Águia",
  actor="Lino Facioli", show="GOT", wiki="Robin Arryn")
u("jon_arryn", "lysa", ["robin_arryn"])
p("walder", "Walder Frey", "Frey", "? – 305 DC", "Senhor do Cruzamento",
  actor="David Bradley", show="GOT", wiki="Walder Frey")
u("walder", None, ["roslin"])

# ══════════════════════════════════════════════════════════════════
# CASA LANNISTER
# ══════════════════════════════════════════════════════════════════
p("tytos", "Tytos Lannister", "Lannister", "? – 267 DC", "Senhor de Rochedo Casterly", wiki="Tytos Lannister")
u("tytos", None, ["tywin", "kevan", "genna", "tygett", "gerion"])
p("tywin", "Tywin Lannister", "Lannister", "242 – 300 DC", "Senhor de Rochedo Casterly · Mão do Rei",
  actor="Charles Dance", show="GOT", wiki="Tywin Lannister")
p("kevan", "Kevan Lannister", "Lannister", "? – 300 DC", "Ser · Regente do Reino",
  actor="Ian Gelder", show="GOT", wiki="Kevan Lannister")
p("genna", "Genna Lannister", "Lannister", "?", "Senhora Frey", sex="f", wiki="Genna Lannister")
p("tygett", "Tygett Lannister", "Lannister", "?", "Ser", wiki="Tygett Lannister")
p("gerion", "Gerion Lannister", "Lannister", "?", "Ser (desaparecido em Valíria)", wiki="Gerion Lannister")
p("joanna", "Joanna Lannister", "Lannister", "227 – 273 DC", "Senhora de Rochedo Casterly", sex="f",
  wiki="Joanna Lannister")
u("tywin", "joanna", ["cersei", "jaime", "tyrion"])
p("cersei", "Cersei Lannister", "Lannister", "266 – 305 DC", "Rainha dos Sete Reinos", sex="f",
  actor="Lena Headey", show="GOT", wiki="Cersei Lannister")
p("jaime", "Jaime Lannister", "Lannister", "266 – 305 DC", "O Regicida · Lorde Comandante da Guarda Real",
  nick="o Regicida", actor="Nikolaj Coster-Waldau", show="GOT", wiki="Jaime Lannister")
p("tyrion", "Tyrion Lannister", "Lannister", "273 – ? DC", "O Duende · Mão do Rei", nick="o Duende",
  actor="Peter Dinklage", show="GOT", wiki="Tyrion Lannister")
p("lancel", "Lancel Lannister", "Lannister", "? – 300 DC", "Ser · Pardal",
  actor="Eugene Simon", show="GOT", wiki="Lancel Lannister")
p("martyn_l", "Martyn Lannister", "Lannister", "?", "Escudeiro", show="GOT", wiki="Martyn Lannister")
p("willem_l", "Willem Lannister", "Lannister", "? – 299 DC", "Escudeiro", show="GOT", wiki="Willem Lannister")
u("kevan", None, ["lancel", "martyn_l", "willem_l"])

# ══════════════════════════════════════════════════════════════════
# CASA BARATHEON
# ══════════════════════════════════════════════════════════════════
p("davos_b", "Davos Baratheon", "Baratheon", "?", "Senhor de Ponta Tempestade", wiki="Davos Baratheon")
p("steffon_bar", "Steffon Baratheon", "Baratheon", "246 – 278 DC", "Senhor de Ponta Tempestade",
  wiki="Steffon Baratheon")
p("cassana", "Cassana Estermont", "Estermont", "? – 278 DC", "Senhora de Ponta Tempestade", sex="f",
  wiki="Cassana Baratheon")
u("steffon_bar", "cassana", ["robert", "stannis", "renly"])
p("robert", "Robert Baratheon", "Baratheon", "262 – 298 DC", "1º de Seu Nome · Rei dos Sete Reinos",
  actor="Mark Addy", show="GOT", wiki="Robert Baratheon")
p("stannis", "Stannis Baratheon", "Baratheon", "264 – 303 DC", "Senhor de Pedra do Dragão · Rei",
  actor="Stephen Dillane", show="GOT", wiki="Stannis Baratheon")
p("renly", "Renly Baratheon", "Baratheon", "277 – 299 DC", "Senhor de Ponta Tempestade · Rei",
  actor="Gethin Anthony", show="GOT", wiki="Renly Baratheon")
p("selyse", "Selyse Florent", "Florent", "? – 303 DC", "Rainha Consorte", sex="f",
  actor="Tara Fitzgerald", show="GOT", wiki="Selyse Baratheon")
p("shireen", "Shireen Baratheon", "Baratheon", "289 – 303 DC", "Princesa de Pedra do Dragão", sex="f",
  actor="Kerry Ingram", show="GOT", wiki="Shireen Baratheon")
u("stannis", "selyse", ["shireen"])
u("robert", "cersei", ["joffrey", "myrcella", "tommen"], note="paternidade oficial")
u("jaime", "cersei", ["joffrey", "myrcella", "tommen"], kind="b", note="paternidade real")
p("joffrey", "Joffrey Baratheon", "Baratheon", "286 – 300 DC", "1º de Seu Nome · Rei dos Sete Reinos",
  actor="Jack Gleeson", show="GOT", wiki="Joffrey Baratheon")
p("myrcella", "Myrcella Baratheon", "Baratheon", "290 – 300 DC", "Princesa", sex="f",
  actor="Nell Tiger Free", show="GOT", wiki="Myrcella Baratheon")
p("tommen", "Tommen Baratheon", "Baratheon", "291 – 300 DC", "1º de Seu Nome · Rei dos Sete Reinos",
  actor="Dean-Charles Chapman", show="GOT", wiki="Tommen Baratheon")
p("gendry", "Gendry", "Baratheon", "?", "Senhor de Ponta Tempestade (bastardo legitimado)",
  actor="Joe Dempsie", show="GOT", wiki="Gendry")
p("edric_storm", "Edric Storm", "Baratheon", "?", "Bastardo de Robert", wiki="Edric Storm")
p("mya_stone", "Mya Stone", "Baratheon", "?", "Bastarda de Robert", sex="f", wiki="Mya Stone")
u("robert", None, ["gendry", "edric_storm", "mya_stone"], kind="b")

# ══════════════════════════════════════════════════════════════════
# CASA GREYJOY
# ══════════════════════════════════════════════════════════════════
p("quellon", "Quellon Greyjoy", "Greyjoy", "? – 289 DC", "Senhor das Ilhas de Ferro", wiki="Quellon Greyjoy")
u("quellon", None, ["balon", "euron", "victarion", "aeron", "urrigon"])
p("balon", "Balon Greyjoy", "Greyjoy", "? – 303 DC", "Rei das Ilhas de Ferro",
  actor="Patrick Malahide", show="GOT", wiki="Balon Greyjoy")
p("euron", "Euron Greyjoy", "Greyjoy", "? – 305 DC", "Olho de Corvo · Rei das Ilhas de Ferro",
  nick="Olho de Corvo", actor="Pilou Asbæk", show="GOT", wiki="Euron Greyjoy")
p("victarion", "Victarion Greyjoy", "Greyjoy", "?", "Lorde Capitão da Frota de Ferro", wiki="Victarion Greyjoy")
p("aeron", "Aeron Greyjoy", "Greyjoy", "?", "Cabelo Molhado · Sacerdote do Deus Afogado",
  actor="Michael Feast", show="GOT", wiki="Aeron Greyjoy")
p("urrigon", "Urrigon Greyjoy", "Greyjoy", "?", "Irmão de Balon", wiki="Urrigon Greyjoy")
p("alannys", "Alannys Harlaw", "Harlaw", "?", "Rainha das Ilhas de Ferro", sex="f", wiki="Alannys Greyjoy")
u("balon", "alannys", ["rodrik_g", "maron_g", "yara", "theon"])
p("rodrik_g", "Rodrik Greyjoy", "Greyjoy", "? – 289 DC", "Herdeiro de Pyke", wiki="Rodrik Greyjoy")
p("maron_g", "Maron Greyjoy", "Greyjoy", "? – 289 DC", "Herdeiro de Pyke", wiki="Maron Greyjoy")
p("yara", "Yara Greyjoy", "Greyjoy", "?", "Rainha das Ilhas de Ferro", sex="f",
  actor="Gemma Whelan", show="GOT", wiki="Yara Greyjoy")
p("theon", "Theon Greyjoy", "Greyjoy", "278 – 303 DC", "Fedor · Príncipe de Pyke",
  actor="Alfie Allen", show="GOT", wiki="Theon Greyjoy")

# ══════════════════════════════════════════════════════════════════
# CASA MARTELL
# ══════════════════════════════════════════════════════════════════
p("martell_parent", "Príncipe(sa) de Dorne", "Martell", "?", "Governante de Lançassolar", wiki="House Martell")
u("martell_parent", None, ["doran", "elia", "oberyn"])
p("doran", "Doran Martell", "Martell", "? – 305 DC", "Príncipe de Dorne",
  actor="Alexander Siddig", show="GOT", wiki="Doran Martell")
p("oberyn", "Oberyn Martell", "Martell", "257 – 300 DC", "A Víbora Vermelha", nick="Víbora Vermelha",
  actor="Pedro Pascal", show="GOT", wiki="Oberyn Martell")
p("mellario", "Mellario de Norvos", "—", "?", "Princesa Consorte", sex="f", wiki="Mellario of Norvos")
u("doran", "mellario", ["arianne", "quentyn", "trystane"])
p("arianne", "Arianne Martell", "Martell", "?", "Princesa herdeira de Dorne", sex="f", wiki="Arianne Martell")
p("quentyn", "Quentyn Martell", "Martell", "?", "Príncipe de Dorne", wiki="Quentyn Martell")
p("trystane", "Trystane Martell", "Martell", "? – 300 DC", "Príncipe de Dorne",
  actor="Toby Sebastian", show="GOT", wiki="Trystane Martell")
p("ellaria", "Ellaria Sand", "Sand", "?", "Amante de Oberyn", sex="f",
  actor="Indira Varma", show="GOT", wiki="Ellaria Sand")
u("oberyn", "ellaria", ["obara", "nymeria_s", "tyene"], kind="b")
p("obara", "Obara Sand", "Sand", "? – 300 DC", "Serpente de Areia", sex="f",
  actor="Keisha Castle-Hughes", show="GOT", wiki="Obara Sand")
p("nymeria_s", "Nymeria Sand", "Sand", "? – 300 DC", "Serpente de Areia", sex="f",
  actor="Jessica Henwick", show="GOT", wiki="Nymeria Sand")
p("tyene", "Tyene Sand", "Sand", "? – 300 DC", "Serpente de Areia", sex="f",
  actor="Rosabell Laurenti Sellers", show="GOT", wiki="Tyene Sand")

# ══════════════════════════════════════════════════════════════════
# CASA TYRELL
# ══════════════════════════════════════════════════════════════════
p("luthor_t", "Luthor Tyrell", "Tyrell", "?", "Senhor de Jardim de Cima", wiki="Luthor Tyrell")
p("olenna", "Olenna Redwyne", "Tyrell", "? – 300 DC", "A Rainha dos Espinhos", sex="f",
  nick="Rainha dos Espinhos", actor="Diana Rigg", show="GOT", wiki="Olenna Tyrell")
u("luthor_t", "olenna", ["mace"])
p("mace", "Mace Tyrell", "Tyrell", "? – 300 DC", "Senhor de Jardim de Cima · Mão do Rei",
  actor="Roger Ashton-Griffiths", show="GOT", wiki="Mace Tyrell")
p("alerie", "Alerie Hightower", "Hightower", "?", "Senhora de Jardim de Cima", sex="f", wiki="Alerie Tyrell")
u("mace", "alerie", ["willas", "garlan", "loras", "margaery"])
p("willas", "Willas Tyrell", "Tyrell", "?", "Herdeiro de Jardim de Cima", wiki="Willas Tyrell")
p("garlan", "Garlan Tyrell", "Tyrell", "?", "Ser · o Galante", wiki="Garlan Tyrell")
p("loras", "Loras Tyrell", "Tyrell", "? – 300 DC", "O Cavaleiro das Flores", nick="Cavaleiro das Flores",
  actor="Finn Jones", show="GOT", wiki="Loras Tyrell")
p("margaery", "Margaery Tyrell", "Tyrell", "? – 300 DC", "Rainha dos Sete Reinos", sex="f",
  actor="Natalie Dormer", show="GOT", wiki="Margaery Tyrell")
u("renly", "margaery", [])
u("joffrey", "margaery", [])
u("tommen", "margaery", [])
u("tyrion", "sansa", [])
u("sansa", "ramsay", [])
p("ramsay", "Ramsay Bolton", "Bolton", "? – 303 DC", "Senhor de Winterfell (bastardo legitimado)",
  actor="Iwan Rheon", show="GOT", wiki="Ramsay Bolton")
p("roose", "Roose Bolton", "Bolton", "? – 303 DC", "Senhor de Forte do Pavor · Protetor do Norte",
  actor="Michael McElhatton", show="GOT", wiki="Roose Bolton")
u("roose", None, ["ramsay"], kind="b")
u("trystane", "myrcella", [])
u("robert", "lyanna", [], note="noivado desfeito pelo rapto")
U.pop()

# limpar uniões inválidas (sem pais reais)
U[:] = [x for x in U if (x["a"] in P or x["a"] is None) and (x["b"] in P or x["b"] is None)
        and (x["a"] or x["b"])]

# ══════════════════════════════════════════════════════════════════
# ÁRVORES (abas do site)
# ══════════════════════════════════════════════════════════════════
TREES = [
  dict(id="targaryen", label="Targaryen — A Dinastia do Dragão", sub="De Aegon o Conquistador a Daenerys · 300 anos",
       roots=["aerion_lord", "orys", "corlys", "rodrik_arryn", "otto", "lyonel_s", "marilda",
              "ormund_bar", "drogo", "rickard_s", "hoster"]),
  dict(id="hotd", label="House of the Dragon — A Dança dos Dragões", sub="Verdes × Negros, 101–131 DC",
       roots=["jaehaerys1", "corlys", "otto", "lyonel_s", "rodrik_arryn", "marilda", "boremund"]),
  dict(id="akotsk", label="O Cavaleiro dos Sete Reinos", sub="A corte de Daeron II e os Blackfyre, 184–260 DC",
       roots=["viserys2", "aegon4", "dunk", "arlan", "tanselle", "lyonel_bar", "steffon_f",
              "raymun_f", "manfred_d", "humfrey_h", "steely_pate", "plummer", "ormund_bar"]),
  dict(id="stark", label="Stark — Os Lobos do Norte", sub="Inverno está chegando",
       roots=["edwyle", "hoster", "cregan_stark", "rhaegar", "walder", "roose"]),
  dict(id="lannister", label="Lannister & Baratheon", sub="Ouro de Rochedo Casterly · Fúria de Ponta Tempestade",
       roots=["tytos", "steffon_bar", "orys", "luthor_t", "ormund_bar", "boremund"]),
  dict(id="outras", label="Tully, Arryn, Greyjoy, Martell & Tyrell", sub="As demais Grandes Casas de Westeros",
       roots=["hoster", "walder", "quellon", "martell_parent", "luthor_t", "jon_arryn",
              "rodrik_arryn", "jeyne_arryn"]),
]

HOUSE_COLORS = {
  "Targaryen": ("#8b1a1a", "#1a1a1a"), "Velaryon": ("#1d5b73", "#0e2f3d"),
  "Hightower": ("#4a5d23", "#243011"), "Stark": ("#4a5259", "#22262a"),
  "Lannister": ("#9c7c14", "#4d3d05"), "Baratheon": ("#8a6a1f", "#2b2b2b"),
  "Tully": ("#1e4f8a", "#7a1414"), "Arryn": ("#3d6ea5", "#dfe9f3"),
  "Greyjoy": ("#2b2b2b", "#5a5a5a"), "Martell": ("#c25c1a", "#8a1f1f"),
  "Tyrell": ("#3f7d3f", "#2a5a2a"), "Strong": ("#6b4f2a", "#3b2a15"),
  "Blackfyre": ("#111111", "#7a1414"), "Rivers": ("#5a5a6a", "#2f2f3a"),
  "Bolton": ("#7a1f1f", "#2b1010"), "Frey": ("#5a6a7a", "#2f3742"),
  "Dothraki": ("#7a4a1a", "#3b2410"), "Sand": ("#c08a3e", "#7a4a1a"),
  "Durrandon": ("#8a6a1f", "#2b2b2b"), "Fossoway": ("#8a1f1f", "#3f7d3f"),
  "Dondarrion": ("#4a2a6a", "#2a1540"), "Blackwood": ("#2b2b2b", "#7a1414"),
  "Martell ": ("#c25c1a", "#8a1f1f"),
}
