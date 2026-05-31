import re
import os

workspace_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
index_path = os.path.join(workspace_dir, "index.html")

with open(index_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Find all headings
headings = re.findall(r'<(h1|h2|h3)[^>]*>(.*?)</\1>', content, re.IGNORECASE | re.DOTALL)

print(f"--- Headings in index.html ---")
for tag, text in headings:
    cleaned_text = re.sub(r'<[^>]+>', '', text).strip()
    print(f"<{tag.upper()}> {cleaned_text}")

# Find sections by id
sections = re.findall(r'<section[^>]*id="([^"]+)"[^>]*>', content)
print(f"\n--- Sections in index.html ---")
for s in sections:
    print(f"Section ID: {s}")
