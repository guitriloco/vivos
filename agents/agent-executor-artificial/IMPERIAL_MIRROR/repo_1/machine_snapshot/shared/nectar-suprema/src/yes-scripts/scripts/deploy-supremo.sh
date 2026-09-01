#!/bin/bash

# deploy-supremo.sh: Full automation for Landing Page deployment to GitHub Pages
NICHE=$1
PROJECT_NAME="supremo-$NICHE"

if [ -z "$NICHE" ]; then
    echo "Usage: ./deploy-supremo.sh <niche>"
    exit 1
fi

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
REPO_ROOT="$(cd "$SCRIPT_DIR/../../.." && pwd)"
DOCS_DIR="$REPO_ROOT/docs"
LP_PATH="$DOCS_DIR/lps/$NICHE"

echo "[SUPREMO] Starting deployment for niche: $NICHE"

# 1. Generate Static HTML for GitHub Pages preview
echo "[SUPREMO] Generating static HTML..."
python3 "$SCRIPT_DIR/html-gen.py" "$NICHE" "$LP_PATH/index.html"

# 2. Update docs/index.html to include the new LP
echo "[SUPREMO] Updating dashboard index..."
if ! grep -q "lps/$NICHE" "$DOCS_DIR/index.html"; then
    # Append the link to the list
    sed -i "/<div id=\"lp-list\"/a \                    <a href=\"lps/$NICHE/index.html\" class=\"lp-item\">🚀 LP: $NICHE</a>" "$DOCS_DIR/index.html"
fi

# 3. Simulate React Build (in a real env, we'd run npm build)
echo "[SUPREMO] React boilerplate prepared in local project folder..."
bash "$SCRIPT_DIR/deploy-lp.sh" "$PROJECT_NAME"

# 4. Sync expansion landing pages from MD to HTML
echo "[SUPREMO] Syncing expansion landing pages..."
python3 "$SCRIPT_DIR/sync-expansion.py"

echo "[SUPREMO] Deployment complete."
echo "[SUPREMO] Preview available locally at: $LP_PATH/index.html"
echo "[SUPREMO] Push the changes to GitHub to trigger GitHub Actions deploy."
