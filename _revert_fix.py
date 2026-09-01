#!/usr/bin/env python3
"""
Revert mass-fixer damage and re-apply fixes carefully.
Strategy: Read each file, find except:pass patterns, replace with
proper logging while preserving indentation of surrounding code.
"""
import os, re, subprocess

ROOT = "/home/team/shared"

# List of files that the mass fixer touched (from the log)
fixed_files = [
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

# First: revert all damage by removing the mass-fixer's print() calls
# and restoring the original except: pass patterns
# Then re-apply with proper indentation

def revert_and_fix(filepath):
    """Revert damage and apply clean fix."""
    if not os.path.exists(filepath):
        return False
    
    with open(filepath, 'r') as f:
        content = f.read()
    
    original = content
    
    # Step 1: Remove the mass-fixer's pollution
    # Pattern: except Exception as e:\n\n( *)print(f"WARNING: {e}")\n
    # plus any surrounding damage
    
    # Remove the mass-fixer print statements and restore the original block
    # Pattern: the fixer replaced:
    #   except:\n            pass
    # with:
    #   except Exception as e:\n\n            print(f"WARNING: {e}")
    # And ate the next line's indentation
    
    # Find all occurrences of the damaged pattern
    # Pattern: "except Exception as e:" followed by print and then a dedented line
    while 'except Exception as e:\n' in content:
        idx = content.index('except Exception as e:\n')
        # Find the end of the except block
        # Look for the print statement
        print_match = re.search(r'except Exception as e:\s*\n\s*\n\s*print\(f"WARNING: \{e\}"\)\s*\n', content[idx:])
        if not print_match:
            break
        
        # Get the indentation of the except block
        lines_before = content[:idx].split('\n')
        last_line = lines_before[-1] if lines_before else ''
        except_indent = len(last_line) - len(last_line.lstrip())
        
        # Get the next line's expected indentation
        after_print = content[idx + print_match.end():]
        next_line = after_print.split('\n')[0] if after_print else ''
        next_indent = len(next_line) - len(next_line.lstrip()) if next_line.strip() else except_indent + 4
        
        # Calculate the try block's indentation (except_indent - 4)
        try_indent = except_indent - 4
        if try_indent < 0:
            try_indent = 0
        
        # Replace with proper code
        old = content[idx:idx + print_match.end()]
        # We need to figure out the right indentation for the next line
        # based on the context
        
        # Simple approach: replace the whole except block
        # except Exception as e:\n\n            print(f"WARNING: {e}")\n
        # with:
        # except Exception as e:\n                print(f"WARNING: {e}")\n
        
        spaces = ' ' * (except_indent + 4)
        replacement = f'except Exception as e:\n{spaces}print(f"WARNING: {{e}}")\n'
        content = content[:idx] + content[idx:].replace(old, replacement, 1)
    
    # Step 2: Fix newlines before keywords that got eaten
    # Look for pattern: print(f"WARNING: {e}")keyword
    for keyword in ['def ', 'class ', 'return ', 'async ', 'for ', 'while ', 'if ', 'try:']:
        content = re.sub(r'\)\s*' + re.escape(keyword), r')\n' + keyword, content)
    
    # Step 3: If nothing changed, try the original fix approach
    if content == original:
        # Direct fix: replace bare except: pass
        # Match exactly: except: NEWLINE spaces pass
        # And capture the next line's indentation
        content = re.sub(
            r'(\n)([ \t]*)except:\s*\n\s*pass\s*\n',
            lambda m: m.group(1) + m.group(2) + 'except Exception as e:\n' + m.group(2) + '    print(f"WARNING: {e}")\n',
            content
        )
    
    if content != original:
        with open(filepath, 'w') as f:
            f.write(content)
        return True
    return False

# Fix all files
fixed = 0
for relpath in fixed_files:
    fpath = os.path.join(ROOT, relpath)
    if os.path.exists(fpath):
        try:
            if revert_and_fix(fpath):
                fixed += 1
                print(f"Fixed: {relpath}")
        except Exception as e:
            print(f"Error with {relpath}: {e}")

print(f"\nFixed {fixed} files")

# Verify syntax
print("\n=== SYNTAX CHECK ===")
pass_count = 0
fail_count = 0
for relpath in fixed_files:
    fpath = os.path.join(ROOT, relpath)
    if not os.path.exists(fpath):
        continue
    result = subprocess.run(['python3', '-m', 'py_compile', fpath], capture_output=True, text=True)
    if result.returncode == 0:
        print(f"  PASS: {relpath}")
        pass_count += 1
    else:
        err = result.stderr.split('\n')[0] if result.stderr else 'unknown'
        print(f"  FAIL: {relpath} -> {err}")
        fail_count += 1

print(f"\nResult: {pass_count} pass, {fail_count} fail")