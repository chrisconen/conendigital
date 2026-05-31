import os
import re

workspace_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
pattern = re.compile(r'/?weboldal-konfigurator-v2\.html', re.IGNORECASE)
replacement = "https://app.conendigital.hu"

print(f"Starting replacement process under: {workspace_dir}")
modified_files_count = 0
total_replacements_count = 0

for root, dirs, files in os.walk(workspace_dir):
    if any(ignored in root for ignored in [".git", "__pycache__", "node_modules", "sablonok", "conen-blog\\node_modules", "conen-blog\\dist"]):
        continue
    for file in files:
        if file.endswith((".html", ".md", ".js", ".astro", ".json", ".ts", ".mjs")):
            path = os.path.join(root, file)
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Check if matches exist
                matches = pattern.findall(content)
                if matches:
                    new_content = pattern.sub(replacement, content)
                    with open(path, 'w', encoding='utf-8') as f:
                        f.write(new_content)
                    
                    rel_path = os.path.relpath(path, workspace_dir)
                    print(f"Updated {rel_path}: {len(matches)} replacement(s) made.")
                    modified_files_count += 1
                    total_replacements_count += len(matches)
            except Exception as e:
                print(f"Error processing {file}: {e}")

print(f"\nReplacement completed. Modified {modified_files_count} file(s) with {total_replacements_count} total replacements.")
