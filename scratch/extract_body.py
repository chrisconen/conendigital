import re
import os

workspace_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
index_path = os.path.join(workspace_dir, "index.html")
out_path = os.path.join(workspace_dir, "scratch", "body_start.html")

with open(index_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Let's find body start
match = re.search(r'<body', content, re.IGNORECASE)
if match:
    start_pos = match.start()
    end_pos = min(len(content), start_pos + 6000)
    with open(out_path, 'w', encoding='utf-8') as out:
        out.write(content[start_pos:end_pos])
    print(f"Body context written to {out_path}")
else:
    print("<body> tag not found")
