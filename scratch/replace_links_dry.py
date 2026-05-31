import os
import re

workspace_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
pattern = re.compile(r'/?weboldal-konfigurator-v2\.html', re.IGNORECASE)

print(f"Workspace: {workspace_dir}")
for root, dirs, files in os.walk(workspace_dir):
    if any(ignored in root for ignored in [".git", "__pycache__", "node_modules", "sablonok", "conen-blog\\node_modules", "conen-blog\\dist"]):
        continue
    for file in files:
        if file.endswith((".html", ".md", ".js", ".astro", ".json", ".ts", ".mjs")):
            path = os.path.join(root, file)
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                matches = pattern.findall(content)
                if matches:
                    rel_path = os.path.relpath(path, workspace_dir)
                    print(f"File: {rel_path} - Matches: {len(matches)}")
                    for m in set(matches):
                        print(f"  Pattern matched: {m}")
            except Exception as e:
                print(f"Error reading {file}: {e}")
