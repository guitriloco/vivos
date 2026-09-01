#!/usr/bin/env python3
"""
Precise fixer: read each damaged file, find the except block damage,
and restore correct indentation. Only fixes the exact pattern of damage.
"""
import os, re, subprocess

ROOT = "/home/team/shared"

files = [
    "expansion_code/SUPRA/intelligence_fusion_v3.py",
    "interlace_matrix/src/interlace/OI_Master.py",
    "cto.new/src/interlace/OI_Master.py",
    "imperial_defense/SOVEREIGN_PERIMETER_PROTOCOL.py",
    "fusion/OMNI-HUB/src/interlace/OI_Master.py",
    "fusion/WRAITH-MESH/run_supra_master.py",
    "fusion/WRAITH-MESH/V9_OMNI_REALIZATION/intelligence_fusion_v3.py",
    "fusion/WRAITH-MESH/src/interlace/olocoo/V9_OMNI_REALIZATION/intelligence_fusion_v3.py",
    "fusion/WRAITH-MESH/src/interlace/auto/V9_OMNI_REALIZATION/intelligence_fusion_v3.py",
    "fusion/WRAITH-MESH/src/interlace/auto/VELOCITY_OPTIMIZATION/arbitrage_engine_v2_1_FIXED.py",
    "fusion/SECURE-VAULT/V9_OMNI_REALIZATION/intelligence_fusion_v3.py",
    "fusion/YIELD-SIPHON/core/printer/webui/Main.py",
    "fusion/MUTANT-NECTAR/core/local_brain_bridge.py",
    "fusion/MUTANT-NECTAR/core/telemetry.py",
    "fusion/MUTANT-NECTAR/imperial_state/powers/EVOLUTION_ENGINE_V1.py",
    "fusion/MUTANT-NECTAR/imperial_state/powers/SUPRA_COMMAND_V1.py",
    "v15_1_master_logic/V15_1_SOVEREIGN_LOOP.py",
    "run_audit.py",
    "vivos_auto_repair.py",
]

def fix_indentation(content):
    """
    Fix the pattern where print(f"WARNING: {e}") is followed by a
    dedented line (the regex ate the indentation).
    """
    lines = content.split('\n')
    new_lines = []
    i = 0
    while i < len(lines):
        line = lines[i]
        # Detect if this line has the print statement and the next line is at column 0
        if 'print(f"WARNING:' in line and i + 1 < len(lines):
            next_line = lines[i + 1]
            if next_line.strip() and not next_line.startswith(' ') and not next_line.startswith('\t'):
                # The next line lost its indentation
                # Get the current indentation of the print line
                indent = len(line) - len(line.lstrip())
                if indent >= 4:
                    # Restore the indentation of the next line to match the print's indent level
                    lines[i + 1] = ' ' * indent + next_line.lstrip()
        new_lines.append(line)
        i += 1
    
    return '\n'.join(lines)

fixed = 0
for relpath in files:
    fpath = os.path.join(ROOT, relpath)
    if not os.path.exists(fpath):
        continue
    
    with open(fpath, 'r') as f:
        content = f.read()
    
    original = content
    
    # Fix 1: Restore indentation of lines after print statements
    content = fix_indentation(content)
    
    # Fix 2: Also fix the pattern where the print line itself is at wrong indentation
    # This happens when the except block was at some indentation but the print lost it
    # Find except Exception as e: followed by blank line then print
    content = re.sub(
        r'(\n)([ \t]*)except Exception as e:\s*\n\s*\n([ \t]*)print\(f"WARNING:',
        lambda m: m.group(1) + m.group(2) + 'except Exception as e:\n' + m.group(2) + '    print(f"WARNING:',
        content
    )
    
    # Fix 3: Remove duplicate blank lines
    while '\n\n\n' in content:
        content = content.replace('\n\n\n', '\n\n')
    
    if content != original:
        with open(fpath, 'w') as f:
            f.write(content)
        fixed += 1
        print(f"Fixed: {relpath}")

print(f"\nFixed {fixed} files")

# Verify
print("\n=== SYNTAX CHECK ===")
pass_count = 0
fail_count = 0
for relpath in files:
    fpath = os.path.join(ROOT, relpath)
    if not os.path.exists(fpath):
        continue
    result = subprocess.run(['python3', '-m', 'py_compile', fpath], capture_output=True, text=True)
    if result.returncode == 0:
        print(f"  PASS: {relpath}")
        pass_count += 1
    else:
        err = result.stderr.split('\n')[0] if result.stderr else 'unknown'
        print(f"  FAIL: {relpath}")
        fail_count += 1

print(f"\nResult: {pass_count} pass, {fail_count} fail")