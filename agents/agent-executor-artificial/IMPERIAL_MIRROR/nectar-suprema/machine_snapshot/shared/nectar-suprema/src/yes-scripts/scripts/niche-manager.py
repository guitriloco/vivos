import json
import argparse
import os

def main():
    parser = argparse.ArgumentParser(description='Manage niche-specific content for Landing Pages.')
    parser.add_argument('--niche', type=str, help='Niche name (e.g., energia-solar)')
    parser.add_argument('--project-path', type=str, default='.', help='Path to the Landing Page project')
    parser.add_argument('--apply', action='store_true', help='Apply changes to the project')

    args = parser.parse_args()

    # Use relative path to niches.json
    script_dir = os.path.dirname(os.path.abspath(__file__))
    niches_file = os.path.join(script_dir, 'niches.json')
    if not os.path.exists(niches_file):
        print(f"Error: {niches_file} not found.")
        return

    with open(niches_file, 'r') as f:
        niches = json.load(f)

    if args.niche not in niches:
        print(f"Error: Niche '{args.niche}' not found in {niches_file}.")
        print(f"Available niches: {', '.join(niches.keys())}")
        return

    niche_data = niches[args.niche]
    print(f"Loaded data for niche: {args.niche}")

    if args.apply:
        config_dir = os.path.join(args.project_path, 'src/config')
        os.makedirs(config_dir, exist_ok=True)
        config_file = os.path.join(config_dir, 'content.json')
        
        with open(config_file, 'w') as f:
            json.dump(niche_data, f, indent=2)
        
        print(f"Applied niche configuration to {config_file}")
    else:
        print("Dry run. Use --apply to save changes.")
        print(json.dumps(niche_data, indent=2))

if __name__ == "__main__":
    main()
