import os
import re

workspace_dir = r"g:\CONEN DIGITAL"
html_files = []

# Walk through the workspace directory to find all HTML files
for root, dirs, files in os.walk(workspace_dir):
    # Skip .git, __pycache__, node_modules
    if any(ignored in root for ignored in [".git", "__pycache__", "node_modules"]):
        continue
    for file in files:
        if file.endswith(".html"):
            html_files.append(os.path.join(root, file))

# We'll search for things like digits followed by Ft, HUF, k Ft, M Ft, or prices in text
# e.g., "600k", "1.5M Ft", "250.000 Ft", "120k Ft"
price_patterns = [
    re.compile(r'\b\d+(?:\.\d{3})*(?:\s*-\s*\d+(?:\.\d{3})*)?\s*(?:k|M)?\s*(?:Ft|HUF)\b', re.IGNORECASE),
    re.compile(r'\b\d+\s*k\s*Ft-tól\b', re.IGNORECASE),
    re.compile(r'\b\d+\s*Ft-tól\b', re.IGNORECASE),
    re.compile(r'\b\d+(?:\.\d{3})*\s*(?:Ft-tól|Ft/hó)\b', re.IGNORECASE),
    re.compile(r'\b\d+\s*hó\b', re.IGNORECASE), # might be too generic, let's keep it safe
    re.compile(r'árak|árazás|díj', re.IGNORECASE)
]

print(f"Found {len(html_files)} HTML files. Scanning for price references...")

for file_path in html_files:
    rel_path = os.path.relpath(file_path, workspace_dir)
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        lines = content.splitlines()
        matches = []
        for i, line in enumerate(lines, 1):
            # Check for pattern matches
            found = False
            for pattern in price_patterns:
                match = pattern.search(line)
                if match:
                    found = True
                    break
            if found:
                matches.append((i, line.strip()))
        
        if matches:
            print(f"\nFile: {rel_path} ({len(matches)} potential matches)")
            for idx, line in matches[:15]: # limit output per file
                print(f"  Line {idx}: {line}")
            if len(matches) > 15:
                print(f"  ... and {len(matches) - 15} more")
    except Exception as e:
        print(f"Error reading {rel_path}: {e}")
