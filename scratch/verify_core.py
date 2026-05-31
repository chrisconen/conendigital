import os
import re

workspace_dir = r"g:\CONEN DIGITAL"
core_files = [
    "index.html",
    "szolgaltatasok.html",
    "webaruhaz-keszites.html",
    "weboldal-keszites.html"
]

patterns = [
    re.compile(r'\b\d+(?:k|M|\.000)?\s*(?:-|–)?\s*\d*(?:k|M|\.000)?\s*Ft\b', re.IGNORECASE),
    re.compile(r'\b\d+\s*k\s*Ft-tól\b', re.IGNORECASE),
    re.compile(r'\b\d+\s*Ft-tól\b', re.IGNORECASE),
    re.compile(r'\b\d+(?:\.\d{3})*\s*(?:Ft-tól|Ft/hó|Ft)\b', re.IGNORECASE),
]

for file in core_files:
    path = os.path.join(workspace_dir, file)
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        matches = []
        for i, line in enumerate(content.splitlines(), 1):
            for pat in patterns:
                m = pat.search(line)
                if m:
                    # Skip if it is about "0 Ft" because we replaced it in some places, 
                    # but let's check what exactly is matched
                    matches.append((i, line.strip(), m.group()))
                    break
        if matches:
            print(f"File: {file} ({len(matches)} matches)")
            for idx, line, val in matches:
                print(f"  Line {idx}: {line} (Matched: {val})")
        else:
            print(f"File: {file} - 100% Clean.")
