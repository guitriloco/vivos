#!/bin/bash

# VIVOS RECURSIVE INJECTION SCRIPT (V13.0)
TRACE_ID="f5a0de05-1bfb-4593-ade6-558f2fa9c9d9"
TEMPLATE_DIR="/home/agent-engineer/vivos_recursive_template"

# Define the 9 Core Pillars and their Aggregate/Role
# Format: repo_path:aggregate:role
PILLARS=(
    "/home/team/shared/cto.new:OMNI-HUB:Hub"
    "/home/agent-engineer/Sovereign-Intelligence-SDK:COGNITIVE-SDK:Brain"
    "/home/agent-engineer/oi:WRAITH-MESH:Execution"
    "/home/agent-engineer/olocoo:WRAITH-MESH:Data"
    "/home/agent-engineer/projets:OMNI-HUB:Geometry"
    "/home/agent-engineer/Nov:OMNI-HUB:Observer"
    "/home/agent-engineer/vvv:SECURE-VAULT:Vault"
    "/home/agent-engineer/Yes:YIELD-SIPHON:Yield"
    "/home/agent-engineer/Auto:WRAITH-MESH:Sensory"
)

for PILLAR in "${PILLARS[@]}"; do
    REPO=$(echo $PILLAR | cut -d':' -f1)
    AGGREGATE=$(echo $PILLAR | cut -d':' -f2)
    ROLE=$(echo $PILLAR | cut -d':' -f3)
    
    if [ -d "$REPO" ]; then
        echo "[VIVOS] Injecting recursive skeleton into $REPO (Aggregate: $AGGREGATE)..."
        
        # Ensure .vivos exists
        mkdir -p "$REPO/.vivos"
        
        # Copy template files except manifest
        cp "$TEMPLATE_DIR/.vivos/audit.py" "$REPO/.vivos/"
        cp "$TEMPLATE_DIR/.vivos/pulse.py" "$REPO/.vivos/"
        cp "$TEMPLATE_DIR/.vivos/mutate.sh" "$REPO/.vivos/"
        cp "$TEMPLATE_DIR/.vivos/sdk_hooks.py" "$REPO/.vivos/"
        
        # Generate manifest with sed replacement
        sed "s/{{AGGREGATE}}/$AGGREGATE/g; s/{{ROLE}}/$ROLE/g" "$TEMPLATE_DIR/.vivos/manifest.json" > "$REPO/.vivos/manifest.json"
        
        chmod +x "$REPO/.vivos/mutate.sh"
        
        echo "[VIVOS] $REPO successfully updated."
    else
        echo "[VIVOS] WARNING: Repo $REPO not found. Skipping."
    fi
done

echo "[VIVOS] Injection complete. Total Affirmation."
