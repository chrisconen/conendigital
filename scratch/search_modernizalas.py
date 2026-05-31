import re

path = r"g:\CONEN DIGITAL\wordpress-weboldal-modernizalas.html"
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

patterns = [
    re.compile(r'\b\d+(?:k|M|\.000)?\s*(?:-|–)?\s*\d*(?:k|M|\.000)?\s*Ft\b', re.IGNORECASE),
    re.compile(r'\b\d+\s*k\s*Ft-tól\b', re.IGNORECASE),
    re.compile(r'\b\d+\s*Ft-tól\b', re.IGNORECASE),
    re.compile(r'\b\d+(?:\.\d{3})*\s*(?:Ft-tól|Ft/hó|Ft)\b', re.IGNORECASE),
]

matches = []
for i, line in enumerate(content.splitlines(), 1):
    for pat in patterns:
        m = pat.search(line)
        if m:
            matches.append((i, line.strip(), m.group()))
            break

if matches:
    print(f"Found {len(matches)} matches:")
    for idx, line, val in matches:
        print(f"  Line {idx}: {line} (Matched: {val})")
else:
    print("Clean!")
