#!/usr/bin/env bash
# Verifica integridade do snapshot guitriloco/vivos vs. staging local da máquina.
# Uso: ./verificar_snapshot.sh [staging_full] [staging_shared]
set -u
STAGING_FULL="${1:-/tmp/vivos-full}"
STAGING_SHARED="${2:-/tmp/vivos-machine-state}"
WORK="/tmp/verify-vivos-$(date +%s)"
echo "[1/4] Clonando guitriloco/vivos..."
git clone -q https://github.com/guitriloco/vivos.git "$WORK"
cd "$WORK"
echo "[2/4] main vs $STAGING_FULL"
git checkout -q main
diff -rq "$STAGING_FULL" . --exclude=.git > /tmp/vdiff-main.txt 2>&1 || true
echo "  conteudos diferentes: $(grep -c '^Files' /tmp/vdiff-main.txt || true)"
echo "  arquivos clone: $(find . -type f -not -path './.git/*' | wc -l)"
echo "[3/4] machine-state-snapshot vs $STAGING_SHARED"
git checkout -q machine-state-snapshot
diff -rq "$STAGING_SHARED" . --exclude=.git > /tmp/vdiff-snap.txt 2>&1 || true
echo "  conteudos diferentes: $(grep -c '^Files' /tmp/vdiff-snap.txt || true)"
echo "[4/4] Detalhes em /tmp/vdiff-main.txt e /tmp/vdiff-snap.txt (entradas 'Only in' de diretorios vazios sao esperadas)."
echo "OK"
