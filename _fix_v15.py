#!/usr/bin/env python3
"""Fix V15_1_SOVEREIGN_LOOP.py - add indentation to dedented methods."""
filepath = "/home/team/shared/v15_1_master_logic/V15_1_SOVEREIGN_LOOP.py"

with open(filepath, 'r') as f:
    lines = f.readlines()

# Fix methods at column 0 that take 'self' (they should be inside classes)
fixes = {
    372: '    ',  # def analyze_telemetry
    493: '    ',  # def compute_system_yield
    985: '    ',  # def _print_affirmation
    1007: '    ',  # def _print_consolidated_report
}

# Apply fixes
for line_num, indent in sorted(fixes.items(), reverse=True):
    idx = line_num - 1  # 0-based
    if idx < len(lines) and lines[idx].startswith('def ') and not lines[idx].startswith(indent):
        lines[idx] = indent + lines[idx]
        print(f"Fixed line {line_num}: {lines[idx].strip()[:60]}")

with open(filepath, 'w') as f:
    f.writelines(lines)

print("Done")