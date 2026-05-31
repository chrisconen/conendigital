import os
import re

workspace_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
pattern = re.compile(r'weboldal-konfigurator-v2\.html', re.IGNORECASE)

output_file = os.path.join(workspace_dir, "scratch", "configurator_links.txt")

with open(output_file, "w", encoding="utf-8") as out:
    for root, dirs, files in os.walk(workspace_dir):
        if any(ignored in root for ignored in [".git", "__pycache__", "node_modules", "sablonok", "conen-blog\\node_modules", "conen-blog\\dist"]):
            continue
        for file in files:
            if file.endswith((".html", ".md", ".js", ".astro", ".json", ".ts", ".mjs")):
                path = os.path.join(root, file)
                try:
                    with open(path, 'r', encoding='utf-8') as f:
                        lines = f.splitlines() if hasattr(f, 'splitlines') else f.read().splitlines()
                    
                    matches = []
                    for i, line in enumerate(lines, 1):
                        m = pattern.search(line)
                        if m:
                            matches.append((i, line.strip()))
                    if matches:
                        out.write(f"File: {os.path.relpath(path, workspace_dir)} ({len(matches)} matches)\n")
                        for idx, line in matches:
                            out.write(f"  Line {idx}: {line}\n")
                except Exception as e:
                    pass

print(f"Done. Saved to {output_file}")
