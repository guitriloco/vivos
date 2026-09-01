#!/bin/bash
#────────────────────────────────────────────────────────────────────────────
# Empire Security — Secret Rotation Script
# Usage: ./rotate_secret.sh <SECRET_NAME> [repo-slug]
#
# This script:
#   1. Reads current secret value (prompted securely)
#   2. Sets the new value in GitHub Actions Secrets
#   3. Logs the rotation event (name only — value never logged)
#   4. Creates a snapshot of rotated secrets for audit
#
# IMPORTANT: For tokens that support it, also call the issuer's revocation API
#   after rotating. This script does NOT call external revocation APIs.
#────────────────────────────────────────────────────────────────────────────

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

if [ -z "$1" ]; then
    echo -e "${RED}Usage: $0 <SECRET_NAME> [repo-slug]${NC}"
    echo "  Prompts securely for the new secret value."
    exit 1
fi

SECRET_NAME="$1"
REPO="${2:-$(gh repo view --json nameWithOwner --jq '.nameWithOwner' 2>/dev/null)}"

# ── Confirm secret exists ─────────────────────────────────────────────────────
echo -e "${YELLOW}▸ Checking if ${SECRET_NAME} exists on ${REPO}...${NC}"
if ! gh secret list --repo "$REPO" 2>/dev/null | grep -q "$SECRET_NAME"; then
    echo -e "${RED}❌ Secret '${SECRET_NAME}' not found on ${REPO}${NC}"
    echo -e "${YELLOW}   Use add_secret.sh to create a new one${NC}"
    exit 1
fi
echo -e "${GREEN}✓ Found existing secret '${SECRET_NAME}'${NC}"

# ── Read new value securely ────────────────────────────────────────────────────
echo -e "${YELLOW}▸ Enter new value for ${SECRET_NAME}:${NC}"
read -rs NEW_SECRET_VALUE
echo ""

if [ -z "$NEW_SECRET_VALUE" ]; then
    echo -e "${RED}❌ Empty value — cannot set empty secret${NC}"
    exit 1
fi

# ── Rotate via GH API ────────────────────────────────────────────────────────
echo -e "${YELLOW}▸ Rotating ${SECRET_NAME} on ${REPO}...${NC}"

OUTPUT=$(gh secret set "$SECRET_NAME" \
    --body "$NEW_SECRET_VALUE" \
    --repo "$REPO" 2>&1)

if echo "$OUTPUT" | grep -q "✓"; then
    echo -e "${GREEN}✓ Secret '${SECRET_NAME}' rotated successfully${NC}"
else
    echo -e "${RED}❌ Rotation failed: $OUTPUT${NC}"
    exit 1
fi

# ── Audit log (value never stored) ───────────────────────────────────────────
TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
echo "[${TIMESTAMP}] SECRET_ROTATED repo=${REPO} name=${SECRET_NAME}" \
    >> /home/team/shared/secret_rotation.log

echo -e "${GREEN}✓ Rotation logged to /home/team/shared/secret_rotation.log${NC}"
echo -e "${YELLOW}⚠️  If this secret had an external issuer (GitHub PAT, AWS keys, etc.),${NC}"
echo -e "${YELLOW}   revoke the old value via the issuer's dashboard.${NC}"