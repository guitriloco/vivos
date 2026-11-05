#!/usr/bin/env bash
# ╔══════════════════════════════════════════════════════════════════╗
# ║  ⚜️  VIVOS_MASTER.sh — INSTALADOR UNIVERSAL DO IMPÉRIO VIVOS V17  ║
# ║  Deploy do império completo em 1 comando, com auto-repair.        ║
# ║                                                                    ║
# ║  Uso:                                                             ║
# ║    ./vivos_master.sh                          # instala (local)   ║
# ║    ./vivos_master.sh --dry-run                # simula sem mudar  ║
# ║    ./vivos_master.sh --source DIR --target DIR                    ║
# ║    ./vivos_master.sh --source git --repo guitriloco/vivos         ║
# ╚══════════════════════════════════════════════════════════════════╝
set -u

VERSION="17.0.0"
SCRIPT_NAME="$(basename "$0")"
SOURCE="${SOURCE:-/home/team/shared}"
TARGET="${TARGET:-$HOME/vivos-empire}"
MODE="install"
GIT_REPO="guitriloco/vivos"
LOG_LINES=0
FAILURES=0
REPAIRED=0

# ---------- Argumentos ----------
while [[ $# -gt 0 ]]; do
  case "$1" in
    --dry-run) MODE="dry-run"; shift ;;
    --source) SOURCE="$2"; shift 2 ;;
    --target) TARGET="$2"; shift 2 ;;
    --repo) GIT_REPO="$2"; shift 2 ;;
    --help|-h) sed -n '2,14p' "$0" | sed 's/^# \{0,1\}//'; exit 0 ;;
    *) echo "⚠️  Argumento desconhecido: $1 (use --help)"; exit 2 ;;
  esac
done

# ---------- Logging ----------
log()  { printf '  \033[0;32m[%s]\033[0m %s\n' "$(date -u +%H:%M:%S)" "$*"; LOG_LINES=$((LOG_LINES+1)); }
warn() { printf '  \033[0;33m[WARN]\033[0m %s\n' "$*"; LOG_LINES=$((LOG_LINES+1)); }
fail() { printf '  \033[0;31m[FAIL]\033[0m %s\n' "$*"; LOG_LINES=$((LOG_LINES+1)); FAILURES=$((FAILURES+1)); }
banner() {
  echo "╔══════════════════════════════════════════════════╗"
  echo "║ ⚜️ VIVOS_MASTER v$VERSION — IMPÉRIO VIVOS PHASE 17 ║"
  echo "╚══════════════════════════════════════════════════╝"
  log "modo=$MODE fonte=$SOURCE destino=$TARGET"
}

# ---------- AUTO-REPAIR: dependências ----------
repair_dep() {  # $1=comando  $2=pacote  $3=comando de instalação
  if command -v "$1" >/dev/null 2>&1; then
    log "dependência ok: $1"
  else
    warn "dependência ausente: $1 — auto-repair tentando instalar ($2)"
    if [[ "$MODE" == "dry-run" ]]; then
      log "dry-run: pularia → $3"
    else
      if eval "$3" >/dev/null 2>&1; then
        log "auto-repair ok: $1 instalado"
        REPAIRED=$((REPAIRED+1))
      else
        fail "auto-repair falhou para $1 (instale manualmente: $3)"
      fi
    fi
  fi
}

auto_repair() {
  log "── AUTO-REPAIR: verificando dependências ──"
  local PM="apt-get"
  command -v apt-get >/dev/null 2>&1 || PM="apk"
  repair_dep git    git    "sudo $PM install -y git 2>/dev/null || $PM install -y git"
  repair_dep python3 python3 "sudo $PM install -y python3 2>/dev/null || $PM install -y python3"
  repair_dep rsync  rsync  "sudo $PM install -y rsync 2>/dev/null || $PM install -y rsync"
  repair_dep tar    tar    "sudo $PM install -y tar 2>/dev/null || $PM install -y tar"
  repair_dep curl   curl   "sudo $PM install -y curl 2>/dev/null || $PM install -y curl"
}

# ---------- AUTO-REPAIR: estrutura do império ----------
EMPIRE_DIRS=(nectars fusion skills powers scripts docs vault site database)
repair_structure() {
  log "── AUTO-REPAIR: estrutura de diretórios ──"
  for d in "${EMPIRE_DIRS[@]}"; do
    if [[ -d "$TARGET/$d" ]]; then
      log "estrutura ok: $d/"
    else
      if [[ "$MODE" == "dry-run" ]]; then
        log "dry-run: criaria $TARGET/$d/"
      else
        mkdir -p "$TARGET/$d" && log "auto-repair ok: criado $TARGET/$d/" && REPAIRED=$((REPAIRED+1))
      fi
    fi
  done
}

# ---------- Instalação ----------
install_from_local() {
  if [[ ! -d "$SOURCE" ]]; then
    fail "fonte local não existe: $SOURCE"
    return 1
  fi
  log "── INSTALAÇÃO a partir de $SOURCE ──"
  if [[ "$MODE" == "dry-run" ]]; then
    local n
    n=$(find "$SOURCE" -type f 2>/dev/null | wc -l)
    log "dry-run: copiaria ~$n arquivos de $SOURCE → $TARGET"
    log "dry-run: exclusões: .git __pycache__ *.pyc .run .git-credentials .netrc .ssh *.pem *.key .env* .claude* .mcp.json"
    return 0
  fi
  mkdir -p "$TARGET"
  if rsync -a \
      --exclude='.git' --exclude='__pycache__' --exclude='*.pyc' --exclude='.run' \
      --exclude='.git-credentials' --exclude='.netrc' --exclude='.ssh' \
      --exclude='*.pem' --exclude='*.key' --exclude='.env*' \
      --exclude='.claude*' --exclude='.mcp.json' \
      "$SOURCE/" "$TARGET/"; then
    local n
    n=$(find "$TARGET" -type f | wc -l)
    log "instalados $n arquivos em $TARGET"
  else
    fail "rsync falhou"
    return 1
  fi
}

install_from_git() {
  log "── INSTALAÇÃO a partir do GitHub ($GIT_REPO, branch machine-state-snapshot) ──"
  if [[ "$MODE" == "dry-run" ]]; then
    log "dry-run: clonaria https://github.com/$GIT_REPO.git (branch machine-state-snapshot) → $TARGET"
    return 0
  fi
  mkdir -p "$TARGET"
  if git clone -q --depth 1 --branch machine-state-snapshot \
      "https://github.com/$GIT_REPO.git" "$TARGET/empire" 2>/dev/null; then
    local n
    n=$(find "$TARGET/empire" -type f -not -path '*/.git/*' | wc -l)
    log "instalados $n arquivos em $TARGET/empire"
  else
    fail "clone do GitHub falhou (verifique rede/acesso)"
    return 1
  fi
}

write_state() {
  [[ "$MODE" == "dry-run" ]] && return 0
  cat > "$TARGET/VIVOS_INSTALL_STATE.json" <<EOF
{
  "version": "$VERSION",
  "installed_at": "$(date -u '+%Y-%m-%dT%H:%M:%SZ')",
  "source": "$SOURCE",
  "mode": "$MODE",
  "repairs": $REPAIRED,
  "failures": $FAILURES,
  "plan": "VIVOS PHASE 17 — A COROAÇÃO SUPREMA"
}
EOF
  log "estado salvo: $TARGET/VIVOS_INSTALL_STATE.json"
}

# ---------- Main ----------
banner
auto_repair
repair_structure

case "$SOURCE" in
  git) install_from_git ;;
  *)   install_from_local ;;
esac

write_state

echo "──────────────────────────────────────────────────"
if [[ $FAILURES -eq 0 ]]; then
  echo "⚜️  IMPÉRIO VIVOS INSTALADO ($LOG_LINES linhas de log, $REPAIRED auto-repairs)"
  echo "    Linha reta. Coroação VIVOS. TOTAL AFIRMAÇÃO."
  exit 0
else
  echo "⚠️  INSTALAÇÃO COM $FAILURES FALHA(S) — verifique os [FAIL] acima"
  exit 1
fi
