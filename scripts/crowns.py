# -*- coding: utf-8 -*-
"""Classificação de realeza, curada à mão.

Não dá para inferir do campo `titles`: "Mão do Rei" (Tywin, Ned, Tyrion) e
"A Rainha dos Espinhos" (Olenna) casariam com qualquer regex de Rei/Rainha
sem nunca terem reinado. Daí a lista explícita.

    sovereign — monarca reinante dos Sete Reinos (o Trono de Ferro)
    regional  — rei/rainha de um reino menor, pretendente ou autoproclamado
    consort   — consorte coroado, sem reinar por direito próprio
"""

# Os 17 reis Targaryen na ordem de sucessão, mais os da era pós-Robert.
SOVEREIGN = [
    "aegon1",      # 1º · O Conquistador
    "aenys1",      # 2º
    "maegor1",     # 3º · O Cruel
    "jaehaerys1",  # 4º · O Conciliador
    "viserys1",    # 5º
    "rhaenyra",    # coroada em Porto Real durante a Dança
    "aegon2",      # 6º · O Usurpador
    "aegon3",      # 7º · Veneno de Dragão
    "daeron1",     # 8º · O Jovem Dragão
    "baelor1",     # 9º · O Abençoado
    "viserys2",    # 10º
    "aegon4",      # 11º · O Indigno
    "daeron2",     # 12º · O Bom
    "aerys1",      # 13º
    "maekar",      # 14º · A Bigorna
    "aegon5",      # 15º · O Improvável
    "jaehaerys2",  # 16º
    "aerys2",      # 17º · O Rei Louco
    "robert",      # Baratheon, após a Rebelião
    "joffrey",
    "tommen",
    "cersei",      # reinou por direito próprio após a explosão do Septo
    "daenerys",    # tomou Porto Real antes de morrer
    "bran",        # eleito no Grande Conselho
]

# Coroas menores: o Norte, as Ilhas de Ferro, pretendentes da Dança e Blackfyre.
REGIONAL = [
    "robb",        # Rei no Norte
    "jon_snow",    # Rei no Norte (aclamado)
    "sansa",       # Rainha no Norte, reino independente
    "stannis",     # reivindicou o Trono de Ferro
    "renly",       # coroado por Tyrell/Baratheon
    "viserys3",    # o Rei Mendigo, nunca coroado de fato
    "balon",       # Rei das Ilhas de Ferro
    "euron",
    "yara",        # reivindicou a Cadeira de Pedra do Mar
    "daemon",      # autocoroado Rei do Mar Estreito
    "daemon_bf",   # 1º Pretendente Blackfyre
    "daemon_bf2",
    "haegon_bf",
    "maelys",
]

# Consortes coroados. Detectados também por "Rainha Consorte" no título,
# mas listados aqui os que usam outra redação.
CONSORT = [
    "visenya", "rhaenys_c",   # irmãs-esposas de Aegon I
    "alysanne",               # A Boa Rainha
    "alicent", "aemma", "helaena",
    "rhaena_a", "alys_harroway", "ceryse", "elinor",
    "jaehaera", "daenaera", "alyssa_v", "aelinor",
    "naerys", "myriah", "betha", "shaera", "rhaella",
    "margaery", "selyse", "talisa", "alannys",
]


def crown_of(pid, titles):
    """Retorna 'sovereign' | 'regional' | 'consort' | None."""
    if pid in SOVEREIGN:
        return "sovereign"
    if pid in REGIONAL:
        return "regional"
    if pid in CONSORT:
        return "consort"
    if titles and "Rainha Consorte" in titles:
        return "consort"
    return None


# Ordem de reinado, para o rótulo "Nº monarca" no lightbox.
REIGN_ORDER = {pid: i + 1 for i, pid in enumerate(SOVEREIGN)}
