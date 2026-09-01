#!/bin/bash
#────────────────────────────────────────────────────────────────────────────
# Empire Security — Local IaC Scan Runner
# Run this script locally to validate Terraform/ IaC before pushing
# Requires: checkov, tfsec
#────────────────────────────────────────────────────────────────────────────

set -e

REPORT_DIR="/home/team/shared/security-reports"
mkdir -p "$REPORT_DIR"

echo "═══════════════════════════════════════════════════════"
echo "  EMPIRE SECURITY — IaC VULNERABILITY SCANNER"
echo "═══════════════════════════════════════════════════════"
echo ""

# ── Checkov ──────────────────────────────────────────────────────────────────
echo "▸ Running Checkov (Terraform/ IaC misconfiguration)..."
if command -v checkov &>/dev/null; then
    checkov --directory . \
        --output json \
        --output-file "$REPORT_DIR/checkov-results.json" \
        --compact \
        2>/dev/null || true
    
    CRITICAL=$(grep -o '"critical": [0-9]*' "$REPORT_DIR/checkov-results.json" 2>/dev/null | head -1 | grep -o '[0-9]*' || echo "0")
    HIGH=$(grep -o '"high": [0-9]*' "$REPORT_DIR/checkov-results.json" 2>/dev/null | head -1 | grep -o '[0-9]*' || echo "0")
    echo "  Checkov — Critical: $CRITICAL | High: $HIGH"
    
    if [ "$CRITICAL" -gt "0" ] || [ "$HIGH" -gt "0" ]; then
        echo "  ❌ FAILED — CRITICAL/HIGH misconfigurations detected"
        exit 1
    fi
    echo "  ✅ PASSED"
else
    echo "  ⚠️  Checkov not installed (pip install checkov)"
fi

echo ""

# ── tfsec ───────────────────────────────────────────────────────────────────
echo "▸ Running tfsec (Terraform security analysis)..."
if command -v tfsec &>/dev/null; then
    tfsec . \
        --no-color \
        --format json \
        --output "$REPORT_DIR/tfsec-results.json" \
        2>/dev/null || true
    
    if [ -s "$REPORT_DIR/tfsec-results.json" ]; then
        CRITICAL=$(grep -c '"critical"' "$REPORT_DIR/tfsec-results.json" 2>/dev/null || echo "0")
        HIGH=$(grep -c '"high"' "$REPORT_DIR/tfsec-results.json" 2>/dev/null || echo "0")
        echo "  tfsec — Critical: $CRITICAL | High: $HIGH"
        
        if [ "$CRITICAL" -gt "0" ] || [ "$HIGH" -gt "0" ]; then
            echo "  ❌ FAILED — CRITICAL/HIGH issues detected"
            exit 1
        fi
        echo "  ✅ PASSED"
    else
        echo "  ✅ PASSED — no issues"
    fi
else
    echo "  ⚠️  tfsec not installed"
fi

echo ""
echo "═══════════════════════════════════════════════════════"
echo "  Scan complete. Reports saved to:"
echo "  $REPORT_DIR/"
echo "═══════════════════════════════════════════════════════"
