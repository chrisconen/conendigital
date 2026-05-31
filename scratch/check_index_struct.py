import os

workspace_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
index_path = os.path.join(workspace_dir, "index.html")

with open(index_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Let's search for some elements
for elem in ["<div class=\"scanlines\"", "scanlines", "cursor", "Cinzel", "Cormorant", "Georgia", "Space Mono"]:
    count = content.count(elem)
    print(f"Occurrence of '{elem}': {count}")
