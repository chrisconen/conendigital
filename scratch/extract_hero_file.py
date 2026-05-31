import re
import os

workspace_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
index_path = os.path.join(workspace_dir, "index.html")
out_path = os.path.join(workspace_dir, "scratch", "hero_context.html")

with open(index_path, 'r', encoding='utf-8') as f:
    content = f.read()

match = re.search(r'weboldal készítés Győr', content, re.IGNORECASE)
if match:
    start_pos = max(0, match.start() - 1500)
    end_pos = min(len(content), match.end() + 1500)
    with open(out_path, 'w', encoding='utf-8') as out:
        out.write(content[start_pos:end_pos])
    print(f"Context written to {out_path}")
else:
    print("Keyword not found")
