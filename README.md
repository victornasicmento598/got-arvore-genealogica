# As Casas de Westeros — árvore genealógica interativa

Árvore genealógica interativa dos personagens de *Game of Thrones*, *House of the Dragon* e
*A Knight of the Seven Kingdoms*, em português (BR) com os termos originais em inglês.

**249 personagens · 86 uniões · 9 casas · ~300 anos de história**, de Aegon o Conquistador a Daenerys.

## Ver o site

- **Online:** <https://victornasicmento598.github.io/got-arvore-genealogica/>
- **No celular, sem internet:** baixe [`arvore-westeros.html`](arvore-westeros.html) e abra no navegador.
  É um arquivo único de 7,3 MB com CSS, JavaScript, dados e **todas as imagens embutidas em base64** —
  funciona em modo avião, sem nenhuma requisição de rede.

## Recursos

| Recurso | Como usar |
|---|---|
| **Busca** | Campo no topo. Procura por nome, apelido, casa, **ator** e títulos. Digitar `clarke` acha Daenerys. Troca de aba automaticamente e centraliza a pessoa. |
| **Destaque de linhagem** | Clique no **nome** de um cartão: 🔴 a pessoa · 🔵 ascendentes · 🟢 descendentes · 🟡 cônjuges. Um painel lista a ascendência direta, cônjuges e filhos, com totais navegáveis. |
| **Realeza** | ♛ 24 monarcas dos Sete Reinos (moldura dourada, em ordem de reinado) · ♔ 13 reis regionais e pretendentes (moldura vermelha) · ♁ 23 consortes coroados. |
| **Filtros** | "Só realeza" e "Só nas séries" (esconde quem só existe nos livros). |
| **Imagens** | Clique na foto para ampliar. Quem apareceu na TV tem foto do ator; os demais têm ilustração ou o brasão da casa. |
| **Zoom / navegação** | Arraste para mover, role para dar zoom, pinça no celular. |
| **Teclado** | `/` busca · `↑`/`↓` navega · `Enter` confirma · `Esc` limpa · `+` `−` `0` zoom. |

## Abas

| Aba | Nós | Conteúdo |
|---|---|---|
| Targaryen | 182 | Linhagem completa, de Aegon I a Daenerys |
| House of the Dragon | 63 | A Dança dos Dragões |
| O Cavaleiro dos Sete Reinos | 77 | Era de Dunk & Egg, com os Blackfyre |
| Stark | 33 | Winterfell e o Norte |
| Lannister & Baratheon | 45 | Rochedo Casterly e Ponta Tempestade |
| Tully, Arryn, Greyjoy, Martell & Tyrell | 49 | Demais grandes casas |

## Publicar no GitHub Pages

O site é estático, sem build. Depois de subir o repositório:

1. **Settings › Pages**
2. Em *Source*, escolha **Deploy from a branch**
3. Branch **`main`**, pasta **`/docs`** → *Save*

Em cerca de um minuto o site estará em `https://<usuario>.github.io/<repositorio>/`.

> A pasta se chama `docs/` porque o GitHub Pages só aceita `/` ou `/docs` como raiz do site.
> Se mudar de lugar, mantenha `index.html`, `style.css`, `app.js`, `data.json` e `img/` juntos.

Para rodar localmente:

```bash
python3 -m http.server 8080 --directory docs
# abra http://localhost:8080
```

## Estrutura

```
docs/                     # o site (é isto que o GitHub Pages publica)
  index.html
  style.css
  app.js                  # render SVG, zoom/pan, busca, linhagem, lightbox
  data.json               # saída do layout: 449 nós posicionados
  img/t/  img/f/          # miniaturas (150px) e imagens ampliadas
arvore-westeros.html      # build offline: tudo em um arquivo só
scripts/
  data_chars.py           # dataset: pessoas, uniões e as 6 árvores
  crowns.py               # taxonomia curada de realeza
  layout.py               # motor de layout → docs/data.json
  fetch_images.py         # baixa retratos das wikis
  fix_images.py  fix2.py  # tenta preencher os faltantes
  sigils.py               # gera brasões para quem não tem retrato
  process_images.py       # recorta e gera as duas resoluções
  build_singlefile.py     # gera arvore-westeros.html
img_raw/                  # imagens originais (fora do Git, veja .gitignore)
```

## Regerar

```bash
python3 scripts/layout.py            # recalcula posições → docs/data.json
python3 scripts/build_singlefile.py  # regera o HTML offline
```

O layout resolve gerações com union-find (funde cônjuges) + BFS bidirecional no grafo de
unidades familiares. Casamentos entre tio e sobrinha, comuns entre os Targaryen, criam ciclos
sem solução consistente: a aresta conflitante é apenas desenhada, sem alterar as gerações.

## Fontes

Dados e imagens de [Game of Thrones Wiki](https://gameofthrones.fandom.com),
[A Wiki of Ice and Fire](https://iceandfire.fandom.com) e Wikipedia.

Projeto de fãs, sem fins lucrativos. *Game of Thrones* e *House of the Dragon* são marcas da HBO;
os livros de *As Crônicas de Gelo e Fogo* são de George R. R. Martin. Todas as imagens
pertencem aos respectivos detentores de direitos e são usadas aqui a título ilustrativo.
