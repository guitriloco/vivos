#!/usr/bin/env bash
# ╔══════════════════════════════════════════════════════════════════╗
# ║  ⚜️  VIVOS_MASTER_BUNDLE — INSTALADOR DE 1 COMANDO (FASE 17)      ║
# ║                                                                    ║
# ║  Regra de ouro: NADA é instalado antes da integridade ser provada. ║
# ║    1. roda verify_bundle.sh (sha256 + contagens)                   ║
# ║    2. se e só se o verificador sair 0 → roda o instalador          ║
# ║                                                                    ║
# ║  Uso:                                                              ║
# ║    ./install.sh                          # verifica e instala      ║
# ║    ./install.sh --dry-run                # verifica e simula       ║
# ║    ./install.sh --target /caminho        # destino alternativo     ║
# ║    VIVOS_TARGET=/caminho ./install.sh    # idem, por variável      ║
# ╚══════════════════════════════════════════════════════════════════╝
set -u

BUNDLE_ROOT="$(cd "$(dirname "$0")" && pwd)" || exit 1
TARGET="${VIVOS_TARGET:-${TARGET:-$HOME/vivos-empire}}"

# Espelha --target para a mensagem de erro ser verdadeira (o valor também é
# repassado ao instalador em "$@" logo abaixo).
_prev=""
for _arg in "$@"; do
  [[ "$_prev" == "--target" ]] && TARGET="$_arg"
  _prev="$_arg"
done
unset _prev _arg

echo "╔══════════════════════════════════════════════════════════╗"
echo "║ ⚜️  VIVOS_MASTER_BUNDLE — INSTALAÇÃO VERIFICADA            ║"
echo "╚══════════════════════════════════════════════════════════╝"
echo "bundle: $BUNDLE_ROOT"
echo "destino: $TARGET"
echo ""

# ── Etapa 1: integridade. Sem esta etapa, o instalador não roda. ──
if ! bash "$BUNDLE_ROOT/verify_bundle.sh"; then
  echo ""
  echo "══════════════════════════════════════════════════════════"
  echo "⛔ INSTALAÇÃO ABORTADA: o bundle não passou na verificação."
  echo "   Um pacote que não prova a própria integridade não é instalado."
  echo "   Nenhum arquivo foi copiado para $TARGET."
  exit 1
fi

echo ""
echo "── integridade provada · iniciando instalador ──"

# ── Etapa 2: instalador, apontado para o próprio bundle ──
# --source $BUNDLE_ROOT: o que se instala é exatamente o que foi verificado.
exec bash "$BUNDLE_ROOT/installer/vivos_master.sh" \
     --source "$BUNDLE_ROOT" --target "$TARGET" "$@"
