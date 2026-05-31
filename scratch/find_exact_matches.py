import os
import re

# Dynamically find workspace directory (parent of scratch folder)
workspace_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
patterns = [
    re.compile(r'\b\d+(?:k|M|\.000)?\s*(?:-|–)?\s*\d*(?:k|M|\.000)?\s*Ft\b', re.IGNORECASE),
    re.compile(r'\b\d+\s*k\s*Ft-tól\b', re.IGNORECASE),
    re.compile(r'\b\d+\s*Ft-tól\b', re.IGNORECASE),
    re.compile(r'\b\d+(?:\.\d{3})*\s*(?:Ft-tól|Ft/hó|Ft)\b', re.IGNORECASE),
]

output_file = os.path.join(workspace_dir, "scratch", "remaining_matches.txt")

with open(output_file, "w", encoding="utf-8") as out:
    for root, dirs, files in os.walk(workspace_dir):
        if any(ignored in root for ignored in [".git", "__pycache__", "node_modules", "sablonok", "conen-blog\\dist"]):
            continue
        for file in files:
            if file.endswith(".html"):
                path = os.path.join(root, file)
                try:
                    with open(path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    matches = []
                    for i, line in enumerate(content.splitlines(), 1):
                        for pat in patterns:
                            m = pat.search(line)
                            if m:
                                matches.append((i, line.strip(), m.group()))
                                break
                    if matches:
                        out.write(f"File: {os.path.relpath(path, workspace_dir)} ({len(matches)} matches)\n")
                        for idx, line, val in matches:
                            out.write(f"  Line {idx}: {line} (Matched: {val})\n")
                except Exception as e:
                    out.write(f"Error reading {os.path.relpath(path, workspace_dir)}: {e}\n")

print(f"Done. Saved to {output_file}")
