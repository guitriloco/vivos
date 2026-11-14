#!/usr/bin/env bash
# ╔══════════════════════════════════════════════════════════════════╗
# ║  ⚜️  VIVOS_MASTER_BUNDLE — VERIFICADOR DE INTEGRIDADE (FASE 17)    ║
# ║                                                                    ║
# ║  Confere, sem confiar em nada declarado:                           ║
# ║    1. o sha256 de TODO arquivo listado em SHA256SUMS               ║
# ║    2. se existe arquivo no bundle que NÃO está no SHA256SUMS       ║
# ║    3. se as contagens do VIVOS_SUPREME_MANIFEST.json são verdade    ║
# ║                                                                    ║
# ║  exit 0 → bundle íntegro · exit 1 → adulterado, incompleto ou       ║
# ║            manifesto mentindo. Nunca "quase": 0 ou 1.              ║
# ║                                                                    ║
# ║  Uso: ./verify_bundle.sh [--quiet]                                 ║
# ╚══════════════════════════════════════════════════════════════════╝
set -u

QUIET=0
[[ "${1:-}" == "--quiet" ]] && QUIET=1

BUNDLE_ROOT="$(cd "$(dirname "$0")" && pwd)" || exit 1
cd "$BUNDLE_ROOT" || exit 1

SUMS_FILE="SHA256SUMS"
MANIFEST="VIVOS_SUPREME_MANIFEST.json"

# ── Isenção nominal única (achado §4 do INSTALL_PROOF) ──────────────
# installer/vivos_master.sh grava "$TARGET/VIVOS_INSTALL_STATE.json" no
# destino da instalação — que é a raiz desta árvore. O arquivo é artefato de
# runtime, gerado na instalação, nunca fez parte do pacote. Ele é ignorado
# EXATAMENTE neste caminho (raiz, nome exato). Qualquer outro arquivo
# desconhecido — inclusive um VIVOS_INSTALL_STATE.json em subdiretório —
# continua reprovando a verificação.
EXEMPT_FILE="VIVOS_INSTALL_STATE.json"
EXEMPT_PATH="./$EXEMPT_FILE"

TMPDIR_V="$(mktemp -d 2>/dev/null || echo /tmp/vivos_verify.$$)"
mkdir -p "$TMPDIR_V"
cleanup() { rm -rf "$TMPDIR_V"; }
trap cleanup EXIT INT TERM

FAILURES=0
divergent_list() { printf '%s\n' "$@"; }

say() { [[ $QUIET -eq 1 ]] || echo "$*"; }

say "╔══════════════════════════════════════════════════════════╗"
say "║ ⚜️  VIVOS_MASTER_BUNDLE — VERIFICAÇÃO DE INTEGRIDADE       ║"
say "╚══════════════════════════════════════════════════════════╝"
say "raiz: $BUNDLE_ROOT"

# ────────────────────────────────────────────────────────────────
# 0) Pré-condições
# ────────────────────────────────────────────────────────────────
if [[ ! -f "$SUMS_FILE" ]]; then
  echo "[FALHA] $SUMS_FILE ausente — bundle não verificável."
  exit 1
fi
if ! command -v sha256sum >/dev/null 2>&1; then
  echo "[FALHA] sha256sum não encontrado (coreutils) — verificação impossível."
  exit 1
fi

LISTED=$(grep -cE '^[0-9a-f]{64}  ' "$SUMS_FILE" 2>/dev/null || echo 0)

# ────────────────────────────────────────────────────────────────
# 1) sha256 de cada arquivo listado
# ────────────────────────────────────────────────────────────────
say ""
say "[1/3] sha256 de $LISTED arquivos listados em $SUMS_FILE"
sha256sum -c "$SUMS_FILE" > "$TMPDIR_V/check.out" 2>&1
CHECK_RC=$?

OK_COUNT=$(grep -cE ': OK$' "$TMPDIR_V/check.out" 2>/dev/null || true)
OK_COUNT=${OK_COUNT:-0}
BAD_COUNT=$(grep -cE ': FAILED$' "$TMPDIR_V/check.out" 2>/dev/null || true)
BAD_COUNT=${BAD_COUNT:-0}
MISSING_COUNT=$(grep -cE 'FAILED open or read' "$TMPDIR_V/check.out" 2>/dev/null || true)
MISSING_COUNT=${MISSING_COUNT:-0}

say "      OK: $OK_COUNT · hash divergente: $BAD_COUNT · ausente/ilegível: $MISSING_COUNT"

if [[ $BAD_COUNT -gt 0 ]]; then
  echo ""
  echo "[FALHA] arquivos com CONTEÚDO DIVERGENTE do SHA256SUMS:"
  grep -E ': FAILED$' "$TMPDIR_V/check.out" | sed 's/^/        ✗ /'
  FAILURES=$((FAILURES+1))
fi
if [[ $MISSING_COUNT -gt 0 ]]; then
  echo ""
  echo "[FALHA] arquivos LISTADOS mas AUSENTES/ilegíveis no bundle:"
  grep -E 'FAILED open or read' "$TMPDIR_V/check.out" | sed 's/^/        ✗ /'
  FAILURES=$((FAILURES+1))
fi
if [[ $CHECK_RC -ne 0 && $BAD_COUNT -eq 0 && $MISSING_COUNT -eq 0 ]]; then
  echo ""
  echo "[FALHA] sha256sum -c retornou $CHECK_RC (saída inesperada):"
  sed 's/^/        ✗ /' "$TMPDIR_V/check.out"
  FAILURES=$((FAILURES+1))
fi
if [[ $OK_COUNT -ne $LISTED ]]; then
  echo ""
  echo "[FALHA] $SUMS_FILE lista $LISTED arquivos, mas só $OK_COUNT foram confirmados."
  FAILURES=$((FAILURES+1))
fi

# ────────────────────────────────────────────────────────────────
# 2) arquivo presente no bundle e NÃO listado (adição posterior)
# ────────────────────────────────────────────────────────────────
say ""
say "[2/3] arquivos presentes no bundle que NÃO estão em $SUMS_FILE"
# EXEMPT_PATH é excluído AQUI e só aqui: é o artefato de runtime que o próprio
# instalador grava no destino. Qualquer outro arquivo desconhecido reprova.
find . -type f \
     -not -path './.git/*' \
     -not -name "$SUMS_FILE" \
     -not -name '.DS_Store' \
     -not -path "$EXEMPT_PATH" \
     | sed 's|^\./||' | LC_ALL=C sort > "$TMPDIR_V/actual.txt"

if [[ -f "$EXEMPT_PATH" ]]; then
  say "      isento (artefato de runtime do instalador): $EXEMPT_FILE"
fi

awk '{ sub(/^[0-9a-f]+  /, ""); print }' "$SUMS_FILE" | LC_ALL=C sort > "$TMPDIR_V/listed.txt"
comm -23 "$TMPDIR_V/actual.txt" "$TMPDIR_V/listed.txt" > "$TMPDIR_V/extra.txt"
EXTRA_COUNT=$(grep -c . "$TMPDIR_V/extra.txt" 2>/dev/null || true)
EXTRA_COUNT=${EXTRA_COUNT:-0}

if [[ $EXTRA_COUNT -gt 0 ]]; then
  echo "[FALHA] $EXTRA_COUNT arquivo(s) no bundle fora do $SUMS_FILE (não verificados):"
  sed 's/^/        ✗ /' "$TMPDIR_V/extra.txt"
  FAILURES=$((FAILURES+1))
else
  say "      nenhum arquivo fora do manifesto de hashes"
fi

# ────────────────────────────────────────────────────────────────
# 3) contagens declaradas no manifesto × realidade no disco
# ────────────────────────────────────────────────────────────────
say ""
say "[3/3] contagens do manifesto × realidade"
MANIFEST_FAILS=0
manifest_fail() { echo "        ✗ $*"; MANIFEST_FAILS=$((MANIFEST_FAILS+1)); }

REAL_PANTHEON=$(find pantheon -maxdepth 1 -type f 2>/dev/null | wc -l | tr -d ' ')
# dossiês = arquivos NN-*.md (01-engineer.md … 35-zenith-overlord.md); o índice 00_INDICE.md não conta
REAL_DOSSIERS=$(find pantheon -maxdepth 1 -type f -name '[0-9][0-9]-*.md' 2>/dev/null | wc -l | tr -d ' ')
REAL_INSTALLER=$(wc -c < installer/vivos_master.sh 2>/dev/null | tr -d ' ' || echo 0)
REAL_TOTAL=$(wc -l < "$TMPDIR_V/actual.txt" | tr -d ' ')

if [[ ! -f "$MANIFEST" ]]; then
  manifest_fail "$MANIFEST ausente — não é possível conferir contagens"
else
  if command -v python3 >/dev/null 2>&1; then
    DECL=$(python3 - "$MANIFEST" <<'PY' 2>/dev/null
import json, sys
try:
    m = json.load(open(sys.argv[1], encoding="utf-8"))
except Exception:
    print("PARSE_ERROR"); raise SystemExit(0)
c = m.get("counts", {})
print(c.get("pantheon_files", "MISSING"),
      c.get("pantheon_dossiers", "MISSING"),
      c.get("installer_bytes", "MISSING"),
      c.get("files_total", "MISSING"))
PY
)
    if [[ "$DECL" == "PARSE_ERROR" || -z "$DECL" ]]; then
      manifest_fail "$MANIFEST não é JSON válido"
    else
      read -r D_PANTHEON D_DOSSIERS D_INSTALLER D_TOTAL <<< "$DECL"
      [[ "$D_PANTHEON"  == "$REAL_PANTHEON"  ]] || manifest_fail "counts.pantheon_files=$D_PANTHEON · realidade=$REAL_PANTHEON"
      [[ "$D_DOSSIERS"  == "$REAL_DOSSIERS"  ]] || manifest_fail "counts.pantheon_dossiers=$D_DOSSIERS · realidade=$REAL_DOSSIERS"
      [[ "$D_INSTALLER" == "$REAL_INSTALLER" ]] || manifest_fail "counts.installer_bytes=$D_INSTALLER · realidade=$REAL_INSTALLER"
      [[ "$D_TOTAL"     == "$REAL_TOTAL"     ]] || manifest_fail "counts.files_total=$D_TOTAL · realidade=$REAL_TOTAL (arquivos no bundle, sem SHA256SUMS)"
    fi
  else
    # fallback sem python3: extração simples de inteiros
    g() { grep -o "\"$1\"[[:space:]]*:[[:space:]]*[0-9]\+" "$MANIFEST" | grep -o '[0-9]\+$' | head -1; }
    D_PANTHEON=$(g pantheon_files); D_DOSSIERS=$(g pantheon_dossiers)
    D_INSTALLER=$(g installer_bytes); D_TOTAL=$(g files_total)
    [[ "$D_PANTHEON"  == "$REAL_PANTHEON"  ]] || manifest_fail "counts.pantheon_files=$D_PANTHEON · realidade=$REAL_PANTHEON"
    [[ "$D_DOSSIERS"  == "$REAL_DOSSIERS"  ]] || manifest_fail "counts.pantheon_dossiers=$D_DOSSIERS · realidade=$REAL_DOSSIERS"
    [[ "$D_INSTALLER" == "$REAL_INSTALLER" ]] || manifest_fail "counts.installer_bytes=$D_INSTALLER · realidade=$REAL_INSTALLER"
    [[ "$D_TOTAL"     == "$REAL_TOTAL"     ]] || manifest_fail "counts.files_total=$D_TOTAL · realidade=$REAL_TOTAL"
  fi
fi

if [[ $MANIFEST_FAILS -eq 0 ]]; then
  say "      manifesto confere: pantheon=$REAL_PANTHEON dossiês=$REAL_DOSSIERS installer=${REAL_INSTALLER}B total=$REAL_TOTAL"
else
  echo "[FALHA] manifesto diverge da realidade ($MANIFEST_FAILS divergência(s))"
  FAILURES=$((FAILURES+1))
fi

# ────────────────────────────────────────────────────────────────
# Veredito
# ────────────────────────────────────────────────────────────────
echo "──────────────────────────────────────────────────────────"
if [[ $FAILURES -eq 0 ]]; then
  echo "BUNDLE ÍNTEGRO — $OK_COUNT arquivos verificados"
  echo "⚜️  sha256 confere, nenhum arquivo fora do manifesto, contagens honestas."
  exit 0
else
  echo "BUNDLE NÃO VERIFICADO — $FAILURES bloco(s) de falha"
  echo "⚠️  NÃO instale este pacote. Restaure uma cópia limpa do repositório."
  exit 1
fi
