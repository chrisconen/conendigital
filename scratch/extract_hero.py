import re
import os

workspace_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
index_path = os.path.join(workspace_dir, "index.html")

with open(index_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Let's find the hero section
# Look for something like id="hero" or class="hero" or similar
# Let's search for the text "Webáruház & weboldal" in index.html and print 50 lines before and after it
match = re.search(r'weboldal készítés Győr', content, re.IGNORECASE)
if match:
    start_pos = max(0, match.start() - 2000)
    end_pos = min(len(content), match.end() + 2000)
    print("--- Context around 'weboldal készítés Győr' ---")
    print(content[start_pos:end_pos])
else:
    print("Keyword not found")
