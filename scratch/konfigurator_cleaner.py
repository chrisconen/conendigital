import os

path = r"g:\CONEN DIGITAL\weboldal-konfigurator-v2.html"

with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

old_str = "600k – 1.2M Ft"
new_str = "Egyedi ajánlat"

if old_str in content:
    content = content.replace(old_str, new_str)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Successfully replaced mock price in weboldal-konfigurator-v2.html!")
else:
    print("Mock price not found in weboldal-konfigurator-v2.html.")
