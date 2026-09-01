import re
import os
import unicodedata

def slugify(value):
    """
    Normalizes string, converts to lowercase, removes non-alpha characters,
    and converts spaces to hyphens.
    """
    value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore').decode('ascii')
    value = re.sub(r'[^\w\s-]', '', value).strip().lower()
    return re.sub(r'[-\s]+', '-', value)

def extract_niches(file_path):
    if not os.path.exists(file_path):
        return []
    
    with open(file_path, 'r') as f:
        content = f.read()
    
    niches = []
    
    # Pattern 1: ### 1. NICHO NAME (used in Top 10)
    top_patterns = re.findall(r'### \d+\.\s+([^\n(]+)', content)
    for name in top_patterns:
        name = name.strip().split('|')[0].strip() # Clean potential trailing info
        slug = slugify(name)
        if name and slug:
            niches.append({"name": name, "slug": slug, "potential": 0.9})

    # Pattern 2: Table rows | # | Nicho | (used in 11-30 and 31-50)
    # Filter out header rows and extract the name
    table_lines = re.findall(r'\|\s*\d+\s*\|\s*([^|]+)\|', content)
    for name in table_lines:
        name = name.strip()
        if "**" in name:
            name = name.replace("**", "")
        if name.lower() == "nicho":
            continue
        slug = slugify(name)
        if name and slug and not any(n['slug'] == slug for n in niches):
            niches.append({"name": name, "slug": slug, "potential": 0.7})

    # Pattern 3: Legacy pattern from research_results.md
    legacy_patterns = re.findall(r'\|\s*\*\*([^*]+)\*\*', content)
    for name in legacy_patterns:
        name = name.strip()
        if name.lower() == "nicho":
            continue
        slug = slugify(name)
        if name and slug and not any(n['slug'] == slug for n in niches):
            niches.append({"name": name, "slug": slug, "potential": 0.8})

    return niches

if __name__ == "__main__":
    # Test with both files
    files = ["/home/team/shared/research_results.md", "/home/team/shared/50_niches_roi.md"]
    all_niches = []
    for f in files:
        if os.path.exists(f):
            print(f"Parsing {f}...")
            found = extract_niches(f)
            print(f"  Found {len(found)} niches.")
            for n in found:
                if not any(x['slug'] == n['slug'] for x in all_niches):
                    all_niches.append(n)
    
    print(f"\nTotal unique niches extracted: {len(all_niches)}")
    for n in all_niches[:10]:
        print(f"- {n['name']} ({n['slug']})")
