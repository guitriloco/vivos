#!/bin/bash

TRACE_ID="f5a0de05-1bfb-4593-ade6-558f2fa9c9d9"
BRANCH_NAME="feat/vivos-skeleton-f5a0de05"
COMMIT_MSG="feat: inject VIVOS self-authoring skeleton

Trace ID: $TRACE_ID"

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
        echo "[VIVOS] Committing to $REPO..."
        cd "$REPO" || continue
        
        # Checkout new branch
        git checkout -b "$BRANCH_NAME"
        
        # Add files
        git add .vivos/
        
        # Commit
        git commit -m "$COMMIT_MSG"
        
        echo "[VIVOS] Commit complete for $REPO."
    else
        echo "[VIVOS] WARNING: Repo $REPO not found. Skipping."
    fi
done
