import os
import sys
import glob

sys.path.insert(0, '/Users/dmoisa/Documents/sun/smi/suds-tools')
from src.drw_parser import parse_drw_file

octal_dir = '/Users/dmoisa/Documents/sun/smi/smi/octal/'
prev_dir = '/Users/dmoisa/Documents/sun/smi/smi/prev/'

files = []
files.extend(glob.glob(os.path.join(octal_dir, '*.drw.O')))
files.extend(glob.glob(os.path.join(prev_dir, '*.drw.*.O')))

results = {}

for path in files:
    filename = os.path.basename(path)
    # Extract base name
    # e.g., q1.drw.O -> q1
    # q1.drw.5.O -> q1
    if filename.endswith('.drw.O'):
        base = filename[:-6]
    else:
        # e.g., q1.drw.5.O
        parts = filename.split('.drw.')
        base = parts[0]
    
    try:
        drw = parse_drw_file(path)
        bodies = len(drw.body_placements)
        points = len(drw.points)
        
        if base not in results:
            results[base] = []
        results[base].append((path, bodies, points))
    except Exception as e:
        print(f"Error parsing {path}: {e}", file=sys.stderr)

best_versions = {}
for base, versions in results.items():
    # Sort by bodies descending, then points descending
    versions.sort(key=lambda x: (x[1], x[2]), reverse=True)
    best_versions[base] = versions[0]

summary_lines = []
summary_lines.append("| Base Name | Best Source Path | Body Count | Point Count |")
summary_lines.append("|---|---|---|---|")

for base in sorted(best_versions.keys()):
    path, bodies, points = best_versions[base]
    summary_lines.append(f"| {base} | {path} | {bodies} | {points} |")

summary_text = "\n".join(summary_lines)
with open('/Users/dmoisa/Documents/sun/smi/suds-tools/scripts/summary.md', 'w') as f:
    f.write(summary_text)

script_lines = []
script_lines.append("#!/bin/bash")
script_lines.append("mkdir -p /Users/dmoisa/Documents/sun/smi/suds-tools/best_drw/")
for base in sorted(best_versions.keys()):
    path = best_versions[base][0]
    script_lines.append(f"cp '{path}' '/Users/dmoisa/Documents/sun/smi/suds-tools/best_drw/{base}.drw.O'")

with open('/Users/dmoisa/Documents/sun/smi/suds-tools/scripts/copy_best_versions.sh', 'w') as f:
    f.write("\n".join(script_lines))

os.chmod('/Users/dmoisa/Documents/sun/smi/suds-tools/scripts/copy_best_versions.sh', 0o755)
