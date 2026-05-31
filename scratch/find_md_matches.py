import os
import re

workspace_dir = r"g:\CONEN DIGITAL"
blog_src_dir = os.path.join(workspace_dir, "conen-blog", "src", "content", "blog")
patterns = [
    re.compile(r'\b\d+(?:k|M|\.000)?\s*(?:-|–)?\s*\d*(?:k|M|\.000)?\s*Ft\b', re.IGNORECASE),
    re.compile(r'\b\d+\s*k\s*Ft-tól\b', re.IGNORECASE),
    re.compile(r'\b\d+\s*Ft-tól\b', re.IGNORECASE),
    re.compile(r'\b\d+(?:\.\d{3})*\s*(?:Ft-tól|Ft/hó|Ft)\b', re.IGNORECASE),
]

output_file = os.path.join(workspace_dir, "scratch", "md_matches.txt")

with open(output_file, "w", encoding="utf-8") as out:
    if not os.path.exists(blog_src_dir):
        out.write(f"Source directory not found: {blog_src_dir}\n")
    else:
        for file in os.listdir(blog_src_dir):
            if file.endswith(".md"):
                path = os.path.join(blog_src_dir, file)
                try:
                    with open(path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    matches = []
                    for i, line in enumerate(content.splitlines(), 1):
                        for pat in patterns:
                            m = pat.search(line)
                            if m:
                                matches.append((i, line.strip(), m.group()))
                                break
                    if matches:
                        out.write(f"File: {file} ({len(matches)} matches)\n")
                        for idx, line, val in matches:
                            out.write(f"  Line {idx}: {line} (Matched: {val})\n")
                except Exception as e:
                    out.write(f"Error reading {file}: {e}\n")

print("Done. Saved to scratch\\md_matches.txt")
