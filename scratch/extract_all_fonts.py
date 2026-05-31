import re
import os

workspace_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

all_fonts = set()
files_checked = []

for root, dirs, files in os.walk(workspace_dir):
    if any(ignored in root for ignored in [".git", "__pycache__", "node_modules", "sablonok", "conen-blog\\node_modules", "conen-blog\\dist"]):
        continue
    for file in files:
        if file.endswith(".html"):
            path = os.path.join(root, file)
            files_checked.append(os.path.relpath(path, workspace_dir))
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    content = f.read()
                font_declarations = re.findall(r'font-family:\s*([^;}]+);', content)
                for font in font_declarations:
                    all_fonts.add(font.strip())
            except Exception as e:
                pass

print(f"Checked {len(files_checked)} HTML files.")
print("Unique Font-Family declarations across all HTML files:")
for font in sorted(all_fonts):
    print(f"  {font}")
