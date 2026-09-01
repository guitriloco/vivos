import os
import re

sdk_path = "/home/agent-yield-master/YIELD-SIPHON/sdk"

# Fix "from intelligence" issues
replacements = [
    ("from intelligence.ancestral_memory import AncestralMemory", "from core.memory import AncestralMemory"),
    ("from intelligence.bio_wealth_engine import BioWealthEngine", "from nectar.intelligence import BioWealthEngine")
]

# Fix relative imports
relative_re = re.compile(r"from \.\.([\w\.]+)")

for root, dirs, files in os.walk(sdk_path):
    for file in files:
        if file.endswith(".py"):
            filepath = os.path.join(root, file)
            with open(filepath, "r") as f:
                content = f.read()
            
            new_content = content
            # Apply hardcoded replacements
            for old, new in replacements:
                new_content = new_content.replace(old, new)
            
            # Apply relative import fixes
            new_content = relative_re.sub(r"from \1", new_content)
            
            if new_content != content:
                with open(filepath, "w") as f:
                    f.write(new_content)
                print(f"Patched: {filepath}")
