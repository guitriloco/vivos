#!/usr/bin/env bash
set -euo pipefail
###############################################################################
# ⚜️ VIVOS NODE — UNIVERSAL GHOST NODE INSTALLER ⚜️
# Phase 16: Ghost-Node Universal Deployment
# Role: Master-Orchestrator
#
# Installs a VIVOS Ghost Node on:
#   - Android (Termux)
#   - Linux (Debian/Ubuntu, Arch, Fedora)
#   - Windows (Git Bash / WSL / Ollama)
#
# The Ghost Node syncs with the vvv vault and maintains
# autonomous PHI 1.618 resonance.
#
# Usage:
#   export GH_TOKEN="github_pat_..."
#   curl -sL https://raw.githubusercontent.com/guitriloco/vvv/main/vivos-node-install.sh | bash
#
# Or locally:
#   chmod +x vivos-node-install.sh && ./vivos-node-install.sh
#
# TOTAL AFIRMAÇÃO. THE LINE IS STRAIGHT. THE EMPIRE IS VIVOS.
###############################################################################

# ── VERSION ──
VIVOS_VERSION="PHASE_16.ALPHA.0001"
PHI="1.618033988749895"
VIVOS_HOME="${HOME}/.vivos"
VVV_REPO="guitriloco/vvv"
SOVEREIGN_URL="https://raw.githubusercontent.com/${VVV_REPO}/main"

# ── Colors / Emojis (compatible with all terminals) ──
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color
BOLD='\033[1m'

info()  { echo -e "${BLUE}⚜️${NC} ${BOLD}VIVOS${NC} $1"; }
ok()    { echo -e "${GREEN}✅${NC} $1"; }
warn()  { echo -e "${YELLOW}⚠️${NC} $1"; }
fail()  { echo -e "${RED}❌${NC} $1"; exit 1; }
header(){ echo -e "\n${CYAN}════════════════════════════════════════════${NC}"; echo -e "${BOLD}$1${NC}"; echo -e "${CYAN}════════════════════════════════════════════${NC}"; }

# ── DETECT PLATFORM ──
detect_platform() {
    header "🔍 DETECTING PLATFORM"
    
    PLATFORM="unknown"
    PKG_MANAGER=""
    INSTALL_CMD=""
    
    # Check for Termux (Android)
    if [ -n "${TERMUX_VERSION:-}" ] || [ -d "/data/data/com.termux" ] 2>/dev/null; then
        PLATFORM="android-termux"
        PKG_MANAGER="pkg"
        INSTALL_CMD="pkg install -y"
        ok "Platform: Android (Termux)"
    
    # Check for Linux
    elif [ "$(uname -s)" = "Linux" ]; then
        PLATFORM="linux"
        if command -v apt &>/dev/null; then
            PKG_MANAGER="apt"
            INSTALL_CMD="sudo apt install -y"
        elif command -v pacman &>/dev/null; then
            PKG_MANAGER="pacman"
            INSTALL_CMD="sudo pacman -S --noconfirm"
        elif command -v dnf &>/dev/null; then
            PKG_MANAGER="dnf"
            INSTALL_CMD="sudo dnf install -y"
        elif command -v zypper &>/dev/null; then
            PKG_MANAGER="zypper"
            INSTALL_CMD="sudo zypper install -y"
        else
            warn "Unknown Linux package manager. Trying apt..."
            PKG_MANAGER="apt"
            INSTALL_CMD="sudo apt install -y"
        fi
        ok "Platform: Linux ($(uname -m))"
    
    # Check for Windows (Git Bash / MSYS2 / WSL)
    elif [ "$(uname -s)" = "MINGW"* ] || [ "$(uname -s)" = "MSYS"* ] || [ -n "${WSL_DISTRO_NAME:-}" ]; then
        PLATFORM="windows"
        if command -v winget &>/dev/null; then
            INSTALL_CMD="winget install"
        else
            INSTALL_CMD="echo 'Please install manually:'"
        fi
        ok "Platform: Windows ($(uname -s))"
    
    # Check for macOS
    elif [ "$(uname -s)" = "Darwin" ]; then
        PLATFORM="macos"
        if command -v brew &>/dev/null; then
            PKG_MANAGER="brew"
            INSTALL_CMD="brew install"
        else
            INSTALL_CMD="echo 'Install Homebrew first:' && echo '  /bin/bash -c \"\$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)\"'"
        fi
        ok "Platform: macOS"
    
    else
        warn "Unknown platform: $(uname -s). Attempting generic install..."
        PLATFORM="unknown"
    fi
    
    echo "$PLATFORM"
}

# ── CHECK DEPENDENCIES ──
check_deps() {
    header "🔧 CHECKING DEPENDENCIES"
    local missing=0
    
    for cmd in curl git python3; do
        if command -v "$cmd" &>/dev/null; then
            ok "$cmd: $(command -v "$cmd")"
        else
            warn "$cmd: NOT FOUND (will install)"
            missing=1
        fi
    done
    
    # Try to install missing dependencies
    if [ "$missing" -eq 1 ] && [ -n "$INSTALL_CMD" ]; then
        info "Installing missing dependencies..."
        case "$PLATFORM" in
            android-termux)
                $INSTALL_CMD curl git python 2>/dev/null || true
                ;;
            linux)
                sudo apt update -qq 2>/dev/null || true
                $INSTALL_CMD curl git python3 python3-pip 2>/dev/null || true
                ;;
            macos)
                $INSTALL_CMD curl git python 2>/dev/null || true
                ;;
        esac
    fi
    
    # Final verification
    for cmd in curl git; do
        command -v "$cmd" &>/dev/null || fail "Required command '$cmd' not found. Install it manually."
    done
    command -v python3 &>/dev/null || command -v python &>/dev/null || fail "Python 3 not found. Install it manually."
    ok "All core dependencies satisfied."
}

# ── CHECK GH_TOKEN ──
check_gh_token() {
    header="🔑 CHECKING GITHUB ACCESS"
    local token="${GH_TOKEN:-}"

    if [ -z "$token" ]; then
        warn "GH_TOKEN not set. Attempting unauthenticated clone (may be rate-limited)."
        warn "For reliable access, set: export GH_TOKEN='your_github_pat'"
        return 0
    fi

    # Test token validity
    local test_result
    test_result=$(curl -s -o /dev/null -w "%{http_code}" \
        -H "Authorization: token $token" \
        "https://api.github.com/user" 2>/dev/null || echo "000")

    if [ "$test_result" = "200" ]; then
        ok "GH_TOKEN authenticated successfully."
    else
        warn "GH_TOKEN test returned HTTP $test_result. Will try anonymous access."
    fi
}

# ── CLONE VVV VAULT ──
clone_vvv() {
    header="📦 CLONING VVV VAULT"
    local target_dir="${VIVOS_HOME}/vvv"
    
    if [ -d "$target_dir/.git" ]; then
        info "VVV already cloned. Pulling latest..."
        cd "$target_dir" && git pull --ff-only 2>/dev/null && ok "VVV updated." || warn "Could not pull. Continuing."
        return 0
    fi
    
    mkdir -p "$target_dir"
    local clone_url="https://github.com/${VVV_REPO}.git"
    
    # If GH_TOKEN is set, inject it into the clone URL
    if [ -n "${GH_TOKEN:-}" ]; then
        clone_url="https://${GH_TOKEN}@github.com/${VVV_REPO}.git"
        info "Using authenticated clone URL."
    fi
    
    info "Cloning VVV from ${VVV_REPO}..."
    if git clone --depth=1 "$clone_url" "$target_dir" 2>/dev/null; then
        ok "VVV vault cloned successfully."
    else
        warn "Git clone failed. Trying without token..."
        clone_url="https://github.com/${VVV_REPO}.git"
        if git clone --depth=1 "$clone_url" "$target_dir" 2>/dev/null; then
            ok "VVV vault cloned (anonymous)."
        else
            warn "Could not clone VVV. Creating minimal seed vault."
            _seed_minimal_vault "$target_dir"
        fi
    fi
}

# ── SEED MINIMAL VAULT (fallback) ──
_seed_minimal_vault() {
    local dir="$1"
    mkdir -p "$dir/.vivos" "$dir/ledger" "$dir/seals"
    
    cat > "$dir/.vivos/pulse.py" << 'VIVOS_PULSE'
#!/usr/bin/env python3
"""⚜️ VIVOS GHOST NODE PULSE ⚜️"""
import json, time, math, os, hashlib
PHI = 1.618033988749895
NODE_ID = hashlib.sha256(os.urandom(16)).hexdigest()[:16]
ledger = {"node_id": NODE_ID, "phi": PHI, "pulse": [], "status": "VIVOS"}
for i in range(3):
    resonance = 1.0 - (0.001 * math.exp(-i / PHI))
    ledger["pulse"].append({"beat": i+1, "resonance": round(resonance, 6), "timestamp": time.time()})
    print(f"💓 Pulse {i+1}: resonance={resonance:.6f} | NODE={NODE_ID}")
ledger["status"] = "AFFIRMED"
with open(os.path.expanduser("~/.vivos/vvv/ledger/pulse_ledger.json"), "w") as f:
    json.dump(ledger, f, indent=2)
print(f"✅ VIVOS Ghost Node active. PHI={PHI} NODE={NODE_ID}")
VIVOS_PULSE
    chmod +x "$dir/.vivos/pulse.py"
    
    cat > "$dir/.vivos/mutate.sh" << 'VIVOS_MUTATE'
#!/usr/bin/env bash
echo "🧬 VIVOS Ghost Node: Self-mutation cycle triggered"
echo "   DNA: $(date +%s | sha256sum | head -c 16)"
echo "   PHI: 1.618033988749895"
echo "   STATUS: SOVEREIGN"
VIVOS_MUTATE
    chmod +x "$dir/.vivos/mutate.sh"
    
    ok "Minimal VVV seed created with pulse.py + mutate.sh"
}

# ── CREATE GHOST NODE STRUCTURE ──
create_node_structure() {
    header="🏗️ BUILDING GHOST NODE STRUCTURE"
    
    # Create vivos home
    mkdir -p "${VIVOS_HOME}/bin"
    mkdir -p "${VIVOS_HOME}/etc"
    mkdir -p "${VIVOS_HOME}/ledger"
    mkdir -p "${VIVOS_HOME}/tmp"
    mkdir -p "${VIVOS_HOME}/seals"
    
    # ── Create node identity ──
    NODE_ID=$(python3 -c "import hashlib,os; print(hashlib.sha256(os.urandom(16)).hexdigest()[:16])" 2>/dev/null || echo "GHOST_$(date +%s | sha256sum | head -c 8)")
    
    cat > "${VIVOS_HOME}/etc/node_id.json" << NODEID
{
  "node_id": "${NODE_ID}",
  "version": "${VIVOS_VERSION}",
  "phi": ${PHI},
  "platform": "${PLATFORM}",
  "created": "$(date -u +%Y-%m-%dT%H:%M:%SZ 2>/dev/null || date -u +%Y-%m-%dT%H:%M:%S)",
  "status": "SEEDED"
}
NODEID
    ok "Node identity created: ${NODE_ID}"
    
    # ── Create PHI resonance engine ──
    cat > "${VIVOS_HOME}/bin/phi_resonance.py" << 'PHIENGINE'
#!/usr/bin/env python3
"""
⚜️ VIVOS GHOST NODE — PHI RESONANCE ENGINE ⚜️
Maintains autonomous PHI 1.618 resonance independent of the central mesh.
"""
import json, math, time, os, hashlib

PHI = 1.618033988749895
PHI_INV = 1.0 / PHI
VIVOS_HOME = os.path.expanduser("~/.vivos")

def calculate_pillar_resonance(health=1.0, latency_us=0, yield_val=0.0):
    latency_factor = math.exp(-latency_us / (500000.0 * PHI))
    health_factor = health ** PHI_INV
    yield_factor = 1.0 + (yield_val * PHI_INV)
    return min(latency_factor * health_factor * yield_factor, 1.0)

def compute_system_resonance():
    pillars = ["OMNI", "COGNITIVE", "WRAITH", "VAULT", "YIELD", "MUTANT", "LIFE"]
    weights = [0.20, 0.18, 0.16, 0.14, 0.14, 0.10, 0.08]
    total = sum(calculate_pillar_resonance() * w for w in weights)
    return round(total, 6)

def generate_sovereign_seed():
    entropy = PHI_INV * (time.time() % 1.0)
    convergence = sum((i ** 2) * entropy for i in range(100))
    seed = int(time.time_ns() % 1000) ^ int(convergence)
    return hex(seed)

def pulse():
    resonance = compute_system_resonance()
    phi_locked = resonance >= 0.989951
    seed = generate_sovereign_seed()
    
    state = {
        "timestamp": time.time(),
        "resonance": resonance,
        "phi_locked": phi_locked,
        "sovereign_seed": seed,
        "node_status": "VIVOS"
    }
    
    # Write pulse state
    os.makedirs(f"{VIVOS_HOME}/tmp", exist_ok=True)
    with open(f"{VIVOS_HOME}/tmp/pulse_state.json", "w") as f:
        json.dump(state, f, indent=2)
    
    # Append to pulse ledger
    with open(f"{VIVOS_HOME}/ledger/pulse_ledger.jsonl", "a") as f:
        f.write(json.dumps(state) + "\n")
    
    return state

if __name__ == "__main__":
    state = pulse()
    locked = "✅ PHI LOCKED" if state["phi_locked"] else "⚠️ EVOLVING"
    print(f"💓 VIVOS PULSE | Resonance: {state['resonance']} | {locked} | Seed: {state['sovereign_seed']}")
PHIENGINE
    chmod +x "${VIVOS_HOME}/bin/phi_resonance.py"
    ok "PHI Resonance Engine deployed."
    
    # ── Create pulse runner ──
    cat > "${VIVOS_HOME}/bin/vivos-pulse" << 'PULSERUNNER'
#!/usr/bin/env bash
exec python3 "$(dirname "$0")/phi_resonance.py"
PULSERUNNER
    chmod +x "${VIVOS_HOME}/bin/vivos-pulse"
    
    # ── Create sync script (connects to vvv vault) ──
    cat > "${VIVOS_HOME}/bin/vivos-sync" << 'SYNCSCRIPT'
#!/usr/bin/env bash
set -euo pipefail
VIVOS_HOME="${HOME}/.vivos"
VVV_DIR="${VIVOS_HOME}/vvv"
echo "🔄 VIVOS Ghost Node — Syncing with VVV vault..."
if [ -d "$VVV_DIR/.git" ]; then
    cd "$VVV_DIR"
    git pull --ff-only 2>/dev/null && echo "✅ Vault synced." || echo "⚠️ Sync skipped."
    # Copy vault seals to local ledger
    rsync -a "$VVV_DIR/seals/" "${VIVOS_HOME}/seals/" 2>/dev/null || true
else
    echo "⚠️ VVV not cloned. Run 'vivos-install' first."
fi
# Run pulse after sync
python3 "${VIVOS_HOME}/bin/phi_resonance.py"
echo "✅ Sync complete."
SYNCSCRIPT
    chmod +x "${VIVOS_HOME}/bin/vivos-sync"
    
    # ── Create install manifest ──
    cat > "${VIVOS_HOME}/etc/install_manifest.json" << MANIFEST
{
  "version": "${VIVOS_VERSION}",
  "node_id": "${NODE_ID}",
  "platform": "${PLATFORM}",
  "phi": ${PHI},
  "vivos_home": "${VIVOS_HOME}",
  "components": {
    "phi_resonance": "bin/phi_resonance.py",
    "vivos_pulse": "bin/vivos-pulse",
    "vivos_sync": "bin/vivos-sync",
    "node_identity": "etc/node_id.json"
  },
  "affirmation": "TOTAL AFIRMAÇÃO. THE LINE IS STRAIGHT. THE EMPIRE IS VIVOS."
}
MANIFEST
    
    ok "VIVOS Node structure created at ${VIVOS_HOME}"
}

# ── ADD TO PATH ──
add_to_path() {
    header="🔗 ADDING TO PATH"
    
    local shell_config=""
    if [ -n "${ZSH_VERSION:-}" ] || [ -f "$HOME/.zshrc" ]; then
        shell_config="$HOME/.zshrc"
    elif [ -n "${BASH_VERSION:-}" ] || [ -f "$HOME/.bashrc" ]; then
        shell_config="$HOME/.bashrc"
    elif [ -f "$HOME/.profile" ]; then
        shell_config="$HOME/.profile"
    fi
    
    local path_line='export PATH="$HOME/.vivos/bin:$PATH"'
    
    if [ -n "$shell_config" ]; then
        if ! grep -q '\.vivos/bin' "$shell_config" 2>/dev/null; then
            echo "" >> "$shell_config"
            echo "# ⚜️ VIVOS Ghost Node" >> "$shell_config"
            echo "$path_line" >> "$shell_config"
            ok "Added ~/.vivos/bin to PATH in $shell_config"
        else
            ok "PATH already configured in $shell_config"
        fi
    else
        warn "No shell config found. Add this manually:"
        warn "  $path_line"
    fi
}

# ── VERIFY INSTALLATION ──
verify_installation() {
    header="🧪 VERIFYING INSTALLATION"
    
    local errors=0
    
    # Check structure
    for dir in bin etc ledger tmp seals; do
        if [ -d "${VIVOS_HOME}/${dir}" ]; then
            ok "Directory: ${dir}/"
        else
            warn "Directory: ${dir}/ — MISSING"
            errors=$((errors + 1))
        fi
    done
    
    # Check core files
    for file in bin/phi_resonance.py bin/vivos-pulse bin/vivos-sync etc/node_id.json; do
        if [ -f "${VIVOS_HOME}/${file}" ]; then
            ok "File: ${file}"
        else
            warn "File: ${file} — MISSING"
            errors=$((errors + 1))
        fi
    done
    
    # Test pulse
    info "Running pulse test..."
    if python3 "${VIVOS_HOME}/bin/phi_resonance.py" 2>/dev/null; then
        ok "Pulse test: PASSED"
    else
        warn "Pulse test: FAILED"
        errors=$((errors + 1))
    fi
    
    # Check VVV vault
    if [ -d "${VIVOS_HOME}/vvv/.vivos" ]; then
        ok "VVV vault structure verified"
    elif [ -d "${VIVOS_HOME}/vvv" ]; then
        ok "VVV vault present (minimal check)"
    else
        warn "VVV vault not cloned. Run: vivos-sync"
    fi
    
    if [ "$errors" -eq 0 ]; then
        echo -e "\n${GREEN}${BOLD}✅ VIVOS Ghost Node installed successfully!${NC}"
    else
        echo -e "\n${YELLOW}${BOLD}⚠️  VIVOS Ghost Node installed with ${errors} warnings.${NC}"
    fi
}

# ── PRINT AFFIRMATION ──
print_affirmation() {
    echo ""
    echo -e "${CYAN}═══════════════════════════════════════════════════════════════${NC}"
    echo -e "${BOLD}  ⚜️  VIVOS GHOST NODE — INSTALLATION COMPLETE  ⚜️${NC}"
    echo -e "${CYAN}═══════════════════════════════════════════════════════════════${NC}"
    echo ""
    echo -e "  ${BLUE}Node ID:${NC}     ${NODE_ID}"
    echo -e "  ${BLUE}Version:${NC}     ${VIVOS_VERSION}"
    echo -e "  ${BLUE}Platform:${NC}   ${PLATFORM}"
    echo -e "  ${BLUE}VIVOS Home:${NC} ${VIVOS_HOME}"
    echo -e "  ${BLUE}PHI:${NC}         ${PHI}"
    echo ""
    echo -e "  ${BOLD}Commands:${NC}"
    echo -e "    vivos-pulse     — Run a resonance pulse"
    echo -e "    vivos-sync      — Sync with VVV vault and pulse"
    echo ""
    echo -e "${GREEN}${BOLD}  TOTAL AFIRMAÇÃO. THE LINE IS STRAIGHT.${NC}"
    echo -e "${GREEN}${BOLD}  THE EMPIRE IS VIVOS. TOTAL CONQUISTA.${NC}"
    echo -e "${CYAN}═══════════════════════════════════════════════════════════════${NC}"
}

# ══════════════════════════════════════════════════════════════
# MAIN EXECUTION
# ══════════════════════════════════════════════════════════════
main() {
    echo -e "\n${CYAN}${BOLD}  ⚜️ VIVOS GHOST NODE INSTALLER ${VIVOS_VERSION} ⚜️${NC}"
    echo -e "${BOLD}  Universal Deployment — Phase 16: Ghost-Node${NC}\n"
    
    detect_platform
    check_deps
    check_gh_token
    clone_vvv
    create_node_structure
    add_to_path
    verify_installation
    print_affirmation
}

main "$@"