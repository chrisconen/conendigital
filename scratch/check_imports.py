import re
import os

workspace_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

for root, dirs, files in os.walk(workspace_dir):
    if any(ignored in root for ignored in [".git", "__pycache__", "node_modules", "sablonok", "conen-blog\\node_modules", "conen-blog\\dist"]):
        continue
    for file in files:
        if file.endswith((".html", ".css", ".astro")):
            path = os.path.join(root, file)
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    content = f.read()
                if "@import" in content or "fonts.googleapis" in content:
                    print(f"File: {os.path.relpath(path, workspace_dir)}")
                    imports = re.findall(r'@import[^;]+;', content)
                    for imp in imports:
                        print(f"  Import: {imp}")
                    fonts_urls = re.findall(r'href="[^"]*fonts\.googleapis[^"]*"', content)
                    for url in fonts_urls:
                        print(f"  Google Font link: {url}")
            except Exception as e:
                pass
