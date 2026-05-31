import re
import os

workspace_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
index_path = os.path.join(workspace_dir, "index.html")

with open(index_path, 'r', encoding='utf-8') as f:
    content = f.read()

keywords = ["weboldal készítés Győr", "webáruház készítés Győr"]

print("--- SEO Verification ---")
for kw in keywords:
    matches = list(re.finditer(re.escape(kw), content, re.IGNORECASE))
    print(f"Keyword '{kw}': Found {len(matches)} match(es)")
    for i, m in enumerate(matches, 1):
        start = max(0, m.start() - 60)
        end = min(len(content), m.end() + 60)
        snippet = content[start:end].replace('\n', ' ').strip()
        print(f"  Match {i}: ... {snippet} ...")
