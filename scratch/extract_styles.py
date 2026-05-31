import re
import os

workspace_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
index_path = os.path.join(workspace_dir, "index.html")

with open(index_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Extract all font-family declarations in styles
font_declarations = re.findall(r'font-family:\s*([^;}]+);', content)
print("Unique Font-Family declarations in index.html:")
for font in set(font_declarations):
    print(f"  {font.strip()}")
