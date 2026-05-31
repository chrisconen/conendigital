import os

workspace_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
index_path = os.path.join(workspace_dir, "index.html")

with open(index_path, "r", encoding="utf-8") as f:
    content = f.read()

lines = content.splitlines()
for i, line in enumerate(lines, 1):
    if "budget" in line.lower() or "option" in line.lower():
        print(f"Line {i}: {line.strip()}")
