import re
import os

workspace_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

pages = ["szolgaltatasok.html", "rolunk.html", "webaruhaz-keszites.html", "weboldal-keszites.html"]

for page in pages:
    path = os.path.join(workspace_dir, page)
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        headings = re.findall(r'<(h1|h2|h3)[^>]*>(.*?)</\1>', content, re.IGNORECASE | re.DOTALL)
        print(f"\n==========================================")
        print(f"PAGE: {page}")
        print(f"==========================================")
        for tag, text in headings[:15]:  # show top 15 headings
            cleaned_text = re.sub(r'<[^>]+>', '', text).strip()
            # Replace common Hungarian accents to display correctly in typical non-UTF-8 console
            cleaned_text = cleaned_text.replace('\u00e1', 'a').replace('\u00e9', 'e').replace('\u00ed', 'i')
            cleaned_text = cleaned_text.replace('\u00f3', 'o').replace('\u00f6', 'o').replace('\u00f5', 'o')
            cleaned_text = cleaned_text.replace('\u00fa', 'u').replace('\u00fc', 'u').replace('\u00fb', 'u')
            cleaned_text = cleaned_text.replace('\u0151', 'o').replace('\u0171', 'u')
            cleaned_text = cleaned_text.replace('\u00c1', 'A').replace('\u00c9', 'E').replace('\u00cd', 'I')
            cleaned_text = cleaned_text.replace('\u00d3', 'O').replace('\u00d6', 'O')
            cleaned_text = cleaned_text.replace('\u00da', 'U').replace('\u00dc', 'U')
            cleaned_text = cleaned_text.replace('\u0150', 'O').replace('\u0170', 'U')
            cleaned_text = re.sub(r'\s+', ' ', cleaned_text)
            print(f"<{tag.upper()}> {cleaned_text}")
