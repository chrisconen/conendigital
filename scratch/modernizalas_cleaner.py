import os

path = r"g:\CONEN DIGITAL\wordpress-weboldal-modernizalas.html"

replacements = [
    # Line 9
    ("Audit-alapú árazás 450k-1.2M Ft tipikus tartomány.",
     "Audit-alapú egyedi árazás."),
    
    # Line 114
    ("Tipikus tartomány: 450.000 – 1.200.000 Ft. AX-audit önállóan: fix 120k Ft / ~2 hét. A pontos árajánlat a 30-perces",
     "Egyedi scope-alapú ajánlat. AX-audit önállóan is kérhető. A pontos árajánlat a 30-perces"),
    
    # Line 1164
    ('<p style="font-size: 1.4rem; color: var(--cyan); font-weight: 700;">450.000 – 1.200.000 Ft</p>',
     '<p style="font-size: 1.4rem; color: var(--cyan); font-weight: 700;">Egyedi ajánlat</p>'),
    
    # Line 1182
    ("Az AX-audit önállóan is választható, ha nem akarsz azonnal projektet: <strong>fix 120.000 Ft / ~2 hét</strong>,",
     "Az AX-audit önállóan is kérhető, ha nem akarsz azonnal projektet: <strong>Egyedi ajánlat alapján</strong>,"),
    
    # Line 1277
    ("<strong>450.000 – 1.200.000 Ft</strong>. AX-audit önállóan: 120k Ft / ~2 hét.",
     "<strong>Egyedi ajánlat alapján</strong>. AX-audit önállóan is kérhető."),
]

with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

modified = False
for old_str, new_str in replacements:
    if old_str in content:
        content = content.replace(old_str, new_str)
        modified = True
        print(f"Replaced successfully: '{old_str.strip()}'")
    else:
        # Try finding with potential character encoding variants if any en-dashes are different
        print(f"WARNING: Pattern not found: '{old_str.strip()}'")

if modified:
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("WordPress modernizálás page cleaned successfully!")
else:
    print("No modifications made to WordPress modernizálás page.")
