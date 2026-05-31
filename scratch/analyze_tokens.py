import re
import os

workspace_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

tokens = {}

for root, dirs, files in os.walk(workspace_dir):
    if any(ignored in root for ignored in [".git", "__pycache__", "node_modules", "sablonok", "conen-blog\\node_modules", "conen-blog\\dist"]):
        continue
    for file in files:
        if file.endswith(".html"):
            path = os.path.join(root, file)
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Extract root declarations
                roots = re.findall(r':root\s*{(.*?)}', content, re.DOTALL)
                for r in roots:
                    declarations = re.findall(r'(--[a-zA-Z0-9-]+)\s*:\s*([^;]+);', r)
                    for k, v in declarations:
                        tokens[k.strip()] = v.strip()
            except Exception as e:
                pass

print("Custom Property Tokens found in :root:")
for k in sorted(tokens.keys()):
    print(f"  {k}: {tokens[k]}")
