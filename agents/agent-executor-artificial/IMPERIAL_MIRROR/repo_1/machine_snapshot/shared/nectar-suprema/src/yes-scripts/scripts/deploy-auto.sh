#!/bin/bash

# deploy-auto.sh: Autonomous push and deploy for Nectar Suprema
NICHE=$1

if [ -z "$NICHE" ]; then
    echo "Usage: ./deploy-auto.sh <niche>"
    exit 1
fi

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
REPO_ROOT="$(cd "$SCRIPT_DIR/../../.." && pwd)"

echo "[AUTO-DEPLOY] Initializing autonomous cycle for niche: $NICHE"

# 1. Run local deployment flow
bash "$SCRIPT_DIR/deploy-supremo.sh" "$NICHE"

# 2. Stage changes
cd "$REPO_ROOT"
git add .

# 3. Commit
TIMESTAMP=$(date "+%Y-%m-%d %H:%M:%S")
git commit -m "feat(auto-deploy): new landing page for $NICHE [$TIMESTAMP]"

# 4. Attempt Push
echo "[AUTO-DEPLOY] Attempting push to remote repository..."
# Note: This expects get_git_credentials to have been called or environment to be pre-auth
git push origin main

if [ $? -eq 0 ]; then
    echo "[AUTO-DEPLOY] SUCCESS: Sovereign Entity successfully pushed changes."
else
    echo "[AUTO-DEPLOY] WARNING: Push failed. Check credentials or GITHUB_TOKEN."
    exit 1
fi
