import re
import os

workspace_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
index_path = os.path.join(workspace_dir, "index.html")

with open(index_path, 'r', encoding='utf-8') as f:
    content = f.read()

fonts_links = re.findall(r'<link[^>]*href="[^"]*fonts\.googleapis\.com[^"]*"[^>]*>', content)
print("Google Fonts Links:")
for link in fonts_links:
    print(link)
