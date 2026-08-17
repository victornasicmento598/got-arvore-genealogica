#!/usr/bin/env bash
# Cria o repositório no GitHub e envia o projeto.
#
#   GITHUB_USER=seu-usuario GITHUB_TOKEN=ghp_xxx ./scripts/push_github.sh
#
# O token precisa do escopo "repo" (clássico) ou permissão de escrita
# em Contents + Administration (fine-grained).

set -euo pipefail

REPO="${REPO_NAME:-got-arvore-genealogica}"
: "${GITHUB_USER:?defina GITHUB_USER}"
: "${GITHUB_TOKEN:?defina GITHUB_TOKEN}"

cd "$(dirname "$0")/.."

DESC="Árvore genealógica interativa de Game of Thrones — 249 personagens, busca, destaque de linhagem e versão offline"

echo "==> criando repositório $GITHUB_USER/$REPO"
code=$(curl -s -o /tmp/gh_create.json -w '%{http_code}' \
  -X POST https://api.github.com/user/repos \
  -H "Authorization: Bearer $GITHUB_TOKEN" \
  -H "Accept: application/vnd.github+json" \
  -d "{\"name\":\"$REPO\",\"description\":\"$DESC\",\"private\":false,\"has_issues\":true,\"has_wiki\":false}")

if [ "$code" = "201" ]; then
  echo "    criado."
elif [ "$code" = "422" ]; then
  echo "    já existe, seguindo para o push."
else
  echo "    ERRO HTTP $code:"; cat /tmp/gh_create.json; exit 1
fi

echo "==> enviando (~21 MB, pode levar um minuto)"
git remote remove origin 2>/dev/null || true
git remote add origin "https://${GITHUB_USER}:${GITHUB_TOKEN}@github.com/${GITHUB_USER}/${REPO}.git"
git push -u origin main --quiet
# não deixa o token gravado no .git/config
git remote set-url origin "https://github.com/${GITHUB_USER}/${REPO}.git"
echo "    enviado."

echo "==> ativando GitHub Pages (branch main, pasta /site)"
code=$(curl -s -o /tmp/gh_pages.json -w '%{http_code}' \
  -X POST "https://api.github.com/repos/${GITHUB_USER}/${REPO}/pages" \
  -H "Authorization: Bearer $GITHUB_TOKEN" \
  -H "Accept: application/vnd.github+json" \
  -d '{"source":{"branch":"main","path":"/site"}}')
case "$code" in
  201|204) echo "    ativado." ;;
  409)     echo "    já estava ativo." ;;
  *)       echo "    não foi possível ativar automaticamente (HTTP $code)."
           echo "    ative em Settings > Pages: branch main, pasta /site." ;;
esac

echo
echo "Repositório: https://github.com/${GITHUB_USER}/${REPO}"
echo "Site:        https://${GITHUB_USER}.github.io/${REPO}/  (leva ~1 min no primeiro deploy)"
