#!/bin/bash

SKELETON_DIR="/home/agent-engineer/vivos_skeleton/.vivos"
TARGET_REPOS=(
    "/home/team/shared/cto.new"
    "/home/agent-engineer/Sovereign-Intelligence-SDK"
    "/home/agent-engineer/oi"
    "/home/agent-engineer/olocoo"
    "/home/agent-engineer/projets"
    "/home/agent-engineer/Nov"
    "/home/agent-engineer/vvv"
    "/home/agent-engineer/Yes"
    "/home/agent-engineer/Auto"
)

for REPO in "${TARGET_REPOS[@]}"; do
    if [ -d "$REPO" ]; then
        echo "[VIVOS] Injecting skeleton into $REPO..."
        mkdir -p "$REPO/.vivos"
        cp -r "$SKELETON_DIR"/* "$REPO/.vivos/"
        
        # SDK Interlace Hook (Special case for Python files in repo root or src)
        # We add an import check if applicable, but for now the skeleton files are enough.
        
        echo "[VIVOS] Injection complete for $REPO."
    else
        echo "[VIVOS] WARNING: Repo $REPO not found. Skipping."
    fi
done
