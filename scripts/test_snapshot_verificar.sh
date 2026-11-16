#!/usr/bin/env bash
# Prova de teste do snapshot que alimenta /verificar.
#
# O que este teste prova, em ordem:
#   1. o script compila (node --check);
#   2. com as fontes reais, o snapshot sai "ok" e o commit de origem é DERIVADO:
#      o commit apontado tem, na sua árvore, o manifesto byte a byte igual;
#   3. a derivação segue o conteúdo: em um repositório de teste, mudar o
#      manifesto muda o commit apontado (não é id escrito à mão);
#   4. manifesto ilegível => exit 1, snapshot reescrito como "falhou" com
#      evidência vazia — o snapshot bom anterior NÃO é reaproveitado (regressão
#      do achado de auditoria: "preserva snapshot anterior e exit 0");
#   5. TRUTH_LOG ilegível => exit 1, mesmo comportamento;
#   6. sem clone do repositório, o commit fica explicitamente ausente (id null,
#      fonte "ausente", motivo), e o build não inventa id;
#   7. manifesto vazio (nenhum hash válido) => exit 1.
#
# Uso: bash scripts/test_snapshot_verificar.sh
# Sai com 0 se todas as provas passarem.

set -uo pipefail

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SCRIPT="$REPO_DIR/scripts/snapshot-verificar.mjs"
CAMINHO_MANIFESTO="VIVOS_MASTER_BUNDLE/SHA256SUMS"
MANIFESTO_REAL="${VIVOS_BUNDLE_SHA256SUMS:-/home/team/shared/VIVOS_MASTER_BUNDLE/SHA256SUMS}"

FALHAS=0
passou() { printf 'PASS  %s\n' "$1"; }
falhou() { printf 'FAIL  %s\n' "$1"; FALHAS=$((FALHAS + 1)); }

for ferramenta in node python3 git; do
  if ! command -v "$ferramenta" >/dev/null 2>&1; then
    echo "FAIL  $ferramenta não encontrado no PATH"
    exit 1
  fi
done

TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT

campo() { # campo <arquivo.json> <expressão python, com o dict em "d">
  python3 - "$1" "$2" <<'PY'
import json, sys
with open(sys.argv[1], encoding="utf-8") as fh:
    dados = json.load(fh)
print(eval(sys.argv[2], {"d": dados}))
PY
}

sha_de_arquivo() { sha256sum "$1" | cut -d' ' -f1; }
sha_de_blob() { git -C "$1" show "$2:$3" | sha256sum | cut -d' ' -f1; }

# --- 0. cópias em sincronia (site x repositório) ---------------------------
COPIA_DO_SITE="/home/team/shared/site/scripts/snapshot-verificar.mjs"
if [ ! -f "$COPIA_DO_SITE" ]; then
  passou "cópia do site ausente nesta máquina: comparação de cópias pulada"
elif cmp -s "$SCRIPT" "$COPIA_DO_SITE"; then
  passou "cópia do site é byte a byte igual a esta"
else
  falhou "cópia do site ($COPIA_DO_SITE) difere da versada no repositório"
fi

# --- 1. sintaxe ------------------------------------------------------------
if node --check "$SCRIPT" >/dev/null 2>&1; then
  passou "node --check em scripts/snapshot-verificar.mjs"
else
  falhou "node --check em scripts/snapshot-verificar.mjs"
fi

# --- 2. fontes reais: status ok + commit com o manifesto na árvore ---------
SAIDA_OK="$TMP/ok.json"
VIVOS_REPO_DIR="$REPO_DIR" VIVOS_SNAPSHOT_OUT="$SAIDA_OK" node "$SCRIPT" >"$TMP/ok.log" 2>&1
CODIGO=$?
if [ "$CODIGO" -eq 0 ]; then
  passou "fontes reais => exit 0"
else
  falhou "fontes reais => exit $CODIGO (esperado 0); log: $(cat "$TMP/ok.log")"
fi

if [ -f "$SAIDA_OK" ] && [ "$(campo "$SAIDA_OK" 'd["status"]')" = "ok" ]; then
  passou "fontes reais => status \"ok\""
else
  falhou "fontes reais => status diferente de \"ok\""
fi

COMMIT_NO_SNAPSHOT="$(campo "$SAIDA_OK" 'd["commit"]["id"]' 2>/dev/null)"
if [ "${#COMMIT_NO_SNAPSHOT}" -eq 40 ] \
  && [ "$(sha_de_blob "$REPO_DIR" "$COMMIT_NO_SNAPSHOT" "$CAMINHO_MANIFESTO")" = "$(sha_de_arquivo "$MANIFESTO_REAL")" ]; then
  passou "commit derivado ($COMMIT_NO_SNAPSHOT) carrega o manifesto byte a byte"
else
  falhou "commit derivado (${COMMIT_NO_SNAPSHOT:-vazio}) não carrega o manifesto lido"
fi

if [ "$(campo "$SAIDA_OK" 'd["fontes"]["commit"]')" = "derivado" ]; then
  passou "fontes.commit = derivado"
else
  falhou "fontes.commit != derivado"
fi

HASHES_MANIFESTO="$(grep -cE '^[0-9a-f]{64} ' "$MANIFESTO_REAL" 2>/dev/null || true)"
HASHES_SNAPSHOT="$(campo "$SAIDA_OK" 'len(d["arquivos"])' 2>/dev/null)"
if [ -n "$HASHES_MANIFESTO" ] && [ "$HASHES_SNAPSHOT" = "$HASHES_MANIFESTO" ]; then
  passou "manifesto completo no snapshot ($HASHES_SNAPSHOT hashes)"
else
  falhou "hashes no snapshot ($HASHES_SNAPSHOT) != manifesto ($HASHES_MANIFESTO)"
fi

# --- 3. a derivação segue o conteúdo do manifesto --------------------------
FALSO="$TMP/repo-falso"
mkdir -p "$FALSO/VIVOS_MASTER_BUNDLE"
git -C "$FALSO" init -q
git -C "$FALSO" config user.email teste@exemplo.invalid
git -C "$FALSO" config user.name "Teste"
cp "$MANIFESTO_REAL" "$FALSO/$CAMINHO_MANIFESTO"
git -C "$FALSO" add "$CAMINHO_MANIFESTO"
git -C "$FALSO" commit -q -m "manifesto v1"

printf '%s  ARQUIVO_ADICIONADO.md\n' "$(printf 'a%.0s' $(seq 1 64))" >>"$FALSO/$CAMINHO_MANIFESTO"
git -C "$FALSO" add "$CAMINHO_MANIFESTO"
git -C "$FALSO" commit -q -m "manifesto v2"
COMMIT_V2="$(git -C "$FALSO" rev-parse HEAD)"

SAIDA_FALSO="$TMP/falso.json"
VIVOS_REPO_DIR="$FALSO" \
  VIVOS_BUNDLE_SHA256SUMS="$FALSO/$CAMINHO_MANIFESTO" \
  VIVOS_SNAPSHOT_OUT="$SAIDA_FALSO" \
  node "$SCRIPT" >"$TMP/falso.log" 2>&1
if [ "$(campo "$SAIDA_FALSO" 'd["commit"]["id"]' 2>/dev/null)" = "$COMMIT_V2" ]; then
  passou "derivação segue o conteúdo: aponta o commit que tem ESTE manifesto ($COMMIT_V2)"
else
  falhou "derivação não seguiu o conteúdo (esperado $COMMIT_V2, obtido $(campo "$SAIDA_FALSO" 'd["commit"]["id"]' 2>/dev/null))"
fi

printf '%s  ARQUIVO_ADICIONADO_2.md\n' "$(printf 'b%.0s' $(seq 1 64))" >>"$FALSO/$CAMINHO_MANIFESTO"
git -C "$FALSO" add "$CAMINHO_MANIFESTO"
git -C "$FALSO" commit -q -m "manifesto v3"
COMMIT_V3="$(git -C "$FALSO" rev-parse HEAD)"
VIVOS_REPO_DIR="$FALSO" \
  VIVOS_BUNDLE_SHA256SUMS="$FALSO/$CAMINHO_MANIFESTO" \
  VIVOS_SNAPSHOT_OUT="$SAIDA_FALSO" \
  node "$SCRIPT" >"$TMP/falso2.log" 2>&1
if [ "$(campo "$SAIDA_FALSO" 'd["commit"]["id"]' 2>/dev/null)" = "$COMMIT_V3" ]; then
  passou "derivação acompanha o manifesto novo ($COMMIT_V3)"
else
  falhou "derivação não acompanhou o manifesto novo (esperado $COMMIT_V3)"
fi

# --- 4. manifesto ilegível: falha fechada, sem reaproveitar o anterior -----
VIVOS_BUNDLE_SHA256SUMS="$TMP/nao-existe-SHA256SUMS" \
  VIVOS_SNAPSHOT_OUT="$SAIDA_OK" \
  node "$SCRIPT" >"$TMP/sem-manifesto.log" 2>&1
CODIGO=$?
if [ "$CODIGO" -eq 1 ]; then
  passou "manifesto ilegível => exit 1 (falha fechada)"
else
  falhou "manifesto ilegível => exit $CODIGO (esperado 1)"
fi

if [ "$(campo "$SAIDA_OK" 'd["status"]')" = "falhou" ]; then
  passou "manifesto ilegível => snapshot reescrito como \"falhou\""
else
  falhou "manifesto ilegível => snapshot continua \"ok\" (mascaramento)"
fi

if [ "$(campo "$SAIDA_OK" 'len(d["arquivos"])')" = "0" ] \
  && [ "$(campo "$SAIDA_OK" 'd["manifesto"] is None')" = "True" ]; then
  passou "manifesto ilegível => evidência vazia (arquivos=[], manifesto=null)"
else
  falhou "manifesto ilegível => evidência antiga sobreviveu no snapshot"
fi

if [ "$(campo "$SAIDA_OK" 'len(d["problemas_no_build"]) > 0')" = "True" ]; then
  passou "manifesto ilegível => problema registrado no snapshot"
else
  falhou "manifesto ilegível => snapshot sem problema registrado"
fi

# --- 5. TRUTH_LOG ilegível -------------------------------------------------
SAIDA_GATE="$TMP/sem-gate.json"
VIVOS_TRUTH_LOG="$TMP/nao-existe-TRUTH_LOG.tsv" \
  VIVOS_SNAPSHOT_OUT="$SAIDA_GATE" \
  node "$SCRIPT" >"$TMP/sem-gate.log" 2>&1
CODIGO=$?
if [ "$CODIGO" -eq 1 ] && [ "$(campo "$SAIDA_GATE" 'd["status"]')" = "falhou" ]; then
  passou "TRUTH_LOG ilegível => exit 1 e status \"falhou\""
else
  falhou "TRUTH_LOG ilegível => exit $CODIGO, status $(campo "$SAIDA_GATE" 'd["status"]' 2>/dev/null)"
fi

# --- 6. sem repositório: commit explicitamente ausente ---------------------
SEM_REPO="$TMP/diretorio-sem-git"
mkdir -p "$SEM_REPO"
SAIDA_SEM_REPO="$TMP/sem-repo.json"
VIVOS_REPO_DIR="$SEM_REPO" VIVOS_SNAPSHOT_OUT="$SAIDA_SEM_REPO" node "$SCRIPT" >"$TMP/sem-repo.log" 2>&1
CODIGO=$?
if [ "$CODIGO" -eq 0 ]; then
  passou "sem clone do repositório => exit 0 (build segue)"
else
  falhou "sem clone do repositório => exit $CODIGO (esperado 0)"
fi

if [ "$(campo "$SAIDA_SEM_REPO" 'd["commit"]["id"] is None')" = "True" ] \
  && [ "$(campo "$SAIDA_SEM_REPO" 'd["commit"]["fonte"]')" = "ausente" ] \
  && [ "$(campo "$SAIDA_SEM_REPO" 'len(d["commit"]["motivo"]) > 0')" = "True" ]; then
  passou "sem clone => commit ausente, com motivo, sem id inventado"
else
  falhou "sem clone => commit não ficou explicitamente ausente"
fi

# --- 7. manifesto sem hash válido ------------------------------------------
: >"$TMP/SHA256SUMS-vazio"
VIVOS_BUNDLE_SHA256SUMS="$TMP/SHA256SUMS-vazio" \
  VIVOS_SNAPSHOT_OUT="$TMP/manifesto-vazio.json" \
  node "$SCRIPT" >"$TMP/manifesto-vazio.log" 2>&1
CODIGO=$?
if [ "$CODIGO" -eq 1 ]; then
  passou "manifesto sem hash válido => exit 1"
else
  falhou "manifesto sem hash válido => exit $CODIGO (esperado 1)"
fi

echo
if [ "$FALHAS" -eq 0 ]; then
  echo "TODAS AS PROVAS PASSARAM"
  exit 0
fi
echo "$FALHAS prova(s) falharam"
exit 1
