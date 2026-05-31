import os

workspace_dir = r"g:\CONEN DIGITAL"

# 1. City pages replacements (all 15 city pages)
city_files = [
    "weboldal-keszites-budapest.html",
    "weboldal-keszites-debrecen.html",
    "weboldal-keszites-eger.html",
    "weboldal-keszites-kaposvar.html",
    "weboldal-keszites-kecskemet.html",
    "weboldal-keszites-miskolc.html",
    "weboldal-keszites-nyiregyhaza.html",
    "weboldal-keszites-pecs.html",
    "weboldal-keszites-sopron.html",
    "weboldal-keszites-szeged.html",
    "weboldal-keszites-szekesfehervar.html",
    "weboldal-keszites-szolnok.html",
    "weboldal-keszites-szombathely.html",
    "weboldal-keszites-veszprem.html",
    "weboldal-keszites-zalaegerszeg.html"
]

city_extra_replacements = [
    ('<div class="hero-stat-label">Első hívás 0 Ft</div>',
     '<div class="hero-stat-label">Díjmentes első hívás</div>'),
    ('<div class="hero-stat-number"><span style="color: var(--magenta)">0</span> Ft</div>',
     '<div class="hero-stat-number"><span style="color: var(--magenta)">Díjmentes</span></div>'),
]

# 2. kapcsolat.html replacements
kapcsolat_replacements = [
    ('(120k Ft, ~2 hét)', '(opcionális, egyedi ajánlat alapján)'),
    ('120k Ft, ~2 hét.', 'Egyedi ajánlat alapján.'),
    ('– 120k Ft, ~2 hét', '– Egyedi ajánlat alapján'),
    ('Fix ár: 120k Ft, ~2 hét.', 'Egyedi ajánlat alapján.'),
]

# 3. portfolio.html replacements
portfolio_replacements = [
    ('AX-audit (120k Ft / ~2 hét) közbeiktatva',
     'AX-audit (egyedi ajánlat alapján) közbeiktatva'),
]

# 4. weboldal-konfigurator-v2.html replacements
konfigurator_replacements = [
    ('AX-audit (120k Ft) 100%-ban beszámít',
     'AX-audit 100%-ban beszámít'),
    ('250.000 Ft / hó-tól',
     'Egyedi havi díj'),
    ("+ AI OPS HAVI: 250.000 Ft/hó-tól (' + aiOps.join(', ') + ') – külön szerződés",
     "+ AI OPS HAVI: Egyedi havi díj (' + aiOps.join(', ') + ') – külön szerződés"),
    ("p1.push('AX-audit (120k Ft) – 100%-ban beszámít');",
     "p1.push('AX-audit – 100%-ban beszámít');"),
    ('AX-audit (120k Ft) 100%-ban beszámít a végösszegbe',
     'AX-audit 100%-ban beszámít a végösszegbe'),
    ("külön havi szerződés keretében működnek, 250.000 Ft/hó-tól.",
     "külön havi szerződés keretében működnek, egyedi díj alapján."),
]

def apply_replacements(file_name, reps):
    file_path = os.path.join(workspace_dir, file_name)
    if not os.path.exists(file_path):
        print(f"WARNING: File {file_name} does not exist!")
        return
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    modified = False
    for old_str, new_str in reps:
        if old_str in content:
            content = content.replace(old_str, new_str)
            modified = True
            print(f"  Replaced: '{old_str.strip()}' -> '{new_str.strip()}'")
            
    if modified:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"  Saved: {file_name}")
    else:
        print(f"  No replacements matched in: {file_name}")

print("=== Cleaning City Pages ===")
for city_file in city_files:
    apply_replacements(city_file, city_extra_replacements)

print("\n=== Cleaning kapcsolat.html ===")
apply_replacements("kapcsolat.html", kapcsolat_replacements)

print("\n=== Cleaning portfolio.html ===")
apply_replacements("portfolio.html", portfolio_replacements)

print("\n=== Cleaning weboldal-konfigurator-v2.html ===")
apply_replacements("weboldal-konfigurator-v2.html", konfigurator_replacements)

print("\n=== Final clean completed! ===")
