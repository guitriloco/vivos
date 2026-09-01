#!/bin/bash
#────────────────────────────────────────────────────────────────────────────
# Empire Security — Secure Secret Addition to GitHub Actions
# Usage: ./add_secret.sh <SECRET_NAME> <SECRET_VALUE> [repo-slug]
#
# Prerequisites:
#   - gh CLI authenticated (`gh auth login`)
#   - Token must have `repo` and `workflow` scopes
#
# What this script does:
#   1. Validates secret name against naming conventions
#   2. Writes value ONLY to GitHub Actions Secrets (never to disk)
#   3. Confirms secret exists after setting
#   4. Logs the action (secret name only — never the value)
#────────────────────────────────────────────────────────────────────────────

set -e

# ── Colours ────────────────────────────────────────────────────────────────
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# ── Validate inputs ─────────────────────────────────────────────────────────
if [ -z "$1" ]; then
    echo -e "${RED}Usage: $0 <SECRET_NAME> <SECRET_VALUE> [repo-slug]${NC}"
    echo "  SECRET_NAME   : UPPER_SNAKE_CASE, alphanumeric + underscore"
    echo "  SECRET_VALUE  : the secret content (will not be echoed)"
    echo "  repo-slug     : optional, defaults to current repo"
    exit 1
fi

SECRET_NAME="$1"
SECRET_VALUE="$2"
REPO="${3:-$(gh repo view --json nameWithOwner --jq '.nameWithOwner' 2>/dev/null)}"

# ── Naming convention ───────────────────────────────────────────────────────
if ! [[ "$SECRET_NAME" =~ ^[A-Z][A-Z0-9_]*$ ]]; then
    echo -e "${RED}❌ Invalid SECRET_NAME: '$SECRET_NAME'${NC}"
    echo -e "${YELLOW}   Must be UPPER_SNAKE_CASE, start with letter, only A-Z/0-9/_${NC}"
    exit 1
fi

# ── Check gh auth ─────────────────────────────────────────────────────────────
if ! gh auth status &>/dev/null; then
    echo -e "${RED}❌ Not authenticated. Run: gh auth login${NC}"
    exit 1
fi

# ── Set the secret via GH API (encrypted, never touches disk) ────────────────
echo -e "${YELLOW}▸ Setting ${SECRET_NAME} on ${REPO}...${NC}"

OUTPUT=$(gh secret set "$SECRET_NAME" \
    --body "$SECRET_VALUE" \
    --repo "$REPO" 2>&1)

if echo "$OUTPUT" | grep -q "✓"; then
    echo -e "${GREEN}✓ Secret '${SECRET_NAME}' set successfully${NC}"
else
    echo -e "${RED}❌ Failed to set secret: $OUTPUT${NC}"
    exit 1
fi

# ── Confirm it exists ─────────────────────────────────────────────────────────
echo -e "${YELLOW}▸ Verifying...${NC}"
sleep 1
if gh secret list --repo "$REPO" 2>/dev/null | grep -q "$SECRET_NAME"; then
    echo -e "${GREEN}✓ Verified: ${SECRET_NAME} is present in GitHub Actions Secrets${NC}"
else
    echo -e "${RED}❌ Secret set but not visible — investigate${NC}"
    exit 1
fi

# ── Log (name only, never value) ─────────────────────────────────────────────
TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
echo "[${TIMESTAMP}] SECRET_ADDED repo=${REPO} name=${SECRET_NAME}" >> /home/team/shared/secret_rotation.log

echo -e "${GREEN}✓ Done. Use \${{ secrets.${SECRET_NAME} }} in workflow YAML.${NC}"
echo -e "${YELLOW}⚠️  Delete any chat messages, .env files, or shell history containing this value${NC}"