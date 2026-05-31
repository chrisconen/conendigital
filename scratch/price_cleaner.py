import os

workspace_dir = r"g:\CONEN DIGITAL"

def process_file(file_path, replacements):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    modified = False
    for old_str, new_str in replacements:
        if old_str in content:
            content = content.replace(old_str, new_str)
            modified = True
            print(f"  Replaced: '{old_str.strip()}' -> '{new_str.strip()}'")
    
    if modified:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"  Saved modified file: {file_path}")
    else:
        print(f"  No replacements matched in: {file_path}")

# 1. index.html replacements
index_replacements = [
    # Title
    ("<title>WEBáruház & WEBoldal készítés Győr | havi 5 ezer Ft-tól bérelhető weboldalak</title>",
     "<title>WEBáruház & WEBoldal készítés Győr | Egyedi fejlesztés & AI automatizáció | Conen Digital</title>"),
    
    # Meta
    ('"description": "Audit utáni egyedi árazás, havi modell. Tipikus: 250.000 Ft-tól / hó."',
     '"description": "Audit-alapú egyedi árazás és havi támogatás az éles növekedésért."'),
    
    # Hero Title lines
    ('<span class="hero-title-line"><span class="hero-title-gradient">havi 5 ezer Ft-tól</span></span>',
     '<span class="hero-title-line"><span class="hero-title-gradient">Egyedi fejlesztés</span></span>'),
    ('<span>bérelhető weboldalak</span>',
     '<span>& AI automatizáció</span>'),
    
    # Hero Stat
    ('<div class="hero-stat-number"><span style="color: var(--magenta)">0</span> Ft</div>',
     '<div class="hero-stat-number"><span style="color: var(--magenta)">Díjmentes</span></div>'),
    
    # Pillar 01 Price
    ('tipikus tartomány: 100.000 – 300.000 Ft',
     'személyre szabott scope szerint'),
    
    # Pillar 02 Price
    ('tipikus tartomány: 250.000 – 600.000 Ft',
     'személyre szabott scope szerint'),
    
    # Pillar 03 Price
    ('tipikus: 50.000 Ft-tól / hó',
     'személyre szabott scope szerint'),
    
    # Dropdown Options
    ('<option value="small">Alap weboldal, 5 ezer Ft/hó</option>',
     '<option value="small">Fókuszált céges honlap / landing</option>'),
    ('<option value="medium">Starter weboldal 15 ezer F/hó</option>',
     '<option value="medium">Komplett üzleti honlap (blog, aloldalak)</option>'),
    ('<option value="large">Profi weboldal 25 ezer Ft/hó</option>',
     '<option value="large">Webáruház / E-commerce rendszer</option>'),
]

# 2. szolgaltatasok.html replacements
szolgaltatasok_replacements = [
    # Meta / Descriptions
    ('content="Három pillér audit-alapú árazással: Ajánlatgeneráló weboldalak (600k-1.5M Ft tipikus), Felújítás + EAA-megfelelés (450k-1.2M Ft tipikus), AI Ops (250k Ft-tól / hó). CENTAUR-ügynökség, Győr + DACH."',
     'content="Három pillér audit-alapú egyedi árazással: Ajánlatgeneráló weboldalak, Felújítás + EAA-megfelelés és AI Ops automatizáció. Conen Digital, Győr."'),
    ('content="Három pillér audit-alapú árazással: Ajánlatgeneráló weboldalak (600k-1.5M Ft tipikus), Felújítás + EAA-megfelelés (450k-1.2M Ft tipikus), AI Ops (250k Ft-tól / hó)."',
     'content="Három pillér audit-alapú egyedi árazással: Ajánlatgeneráló weboldalak, Felújítás + EAA-megfelelés és AI Ops automatizáció."'),
    ('"description": "Három pillér audit-alapú árazással: Ajánlatgeneráló weboldalak (600k-1.5M Ft tipikus), Felújítás + EAA-megfelelés (450k-1.2M Ft tipikus), AI Ops (250k Ft-tól / hó)."',
     '"description": "Három pillér audit-alapú egyedi árazással: Ajánlatgeneráló weboldalak, Felújítás + EAA-megfelelés és AI Ops automatizáció."'),
    ('"description": "Audit utáni egyedi árazás. Tipikus: 250.000 Ft-tól / hó."',
     '"description": "Audit-alapú egyedi árazás."'),

    # Service Price Value 01
    ('<div class="service-price-value" style="font-size: 1.4rem;">600k – 1.5M Ft</div>',
     '<div class="service-price-value" style="font-size: 1.4rem;">Audit-alapú</div>'),
    ('<div class="service-price-label">Audit utáni egyedi</div>\n                        <div class="service-price-value" style="font-size: 1.4rem;">600k – 1.5M Ft</div>\n                        <div class="service-price-note">tipikus tartomány</div>',
     '<div class="service-price-label">Árazási modell</div>\n                        <div class="service-price-value" style="font-size: 1.4rem;">Audit-alapú</div>\n                        <div class="service-price-note">egyedi scope szerint</div>'),

    # Service Price Value 02
    ('<div class="service-price-value" style="font-size: 1.4rem;">450k – 1.2M Ft</div>',
     '<div class="service-price-value" style="font-size: 1.4rem;">Audit-alapú</div>'),
    ('<div class="service-price-label">Audit utáni egyedi</div>\n                        <div class="service-price-value" style="font-size: 1.4rem;">450k – 1.2M Ft</div>\n                        <div class="service-price-note">tipikus tartomány</div>',
     '<div class="service-price-label">Árazási modell</div>\n                        <div class="service-price-value" style="font-size: 1.4rem;">Audit-alapú</div>\n                        <div class="service-price-note">egyedi scope szerint</div>'),

    # Service Price Value 03
    ('<div class="service-price-value" style="font-size: 1.4rem;">250k+ Ft / hó</div>',
     '<div class="service-price-value" style="font-size: 1.4rem;">Audit-alapú</div>'),
    ('<div class="service-price-label">Audit utáni egyedi, havi</div>\n                        <div class="service-price-value" style="font-size: 1.4rem;">250k+ Ft / hó</div>\n                        <div class="service-price-note">tipikus belépési szint</div>',
     '<div class="service-price-label">Árazási modell</div>\n                        <div class="service-price-value" style="font-size: 1.4rem;">Audit-alapú</div>\n                        <div class="service-price-note">egyedi havi díj</div>'),

    # Service Price Value 04
    ('<div class="service-price-value" style="font-size: 1.4rem;">800k Ft-tól</div>',
     '<div class="service-price-value" style="font-size: 1.4rem;">Audit-alapú</div>'),
    ('<div class="service-price-label">Audit utáni egyedi</div>\n                        <div class="service-price-value" style="font-size: 1.4rem;">800k Ft-tól</div>\n                        <div class="service-price-note">platformtól függően</div>',
     '<div class="service-price-label">Árazási modell</div>\n                        <div class="service-price-value" style="font-size: 1.4rem;">Audit-alapú</div>\n                        <div class="service-price-note">platformtól függően</div>'),

    # Service Price Value 05
    ('<div class="service-price-value" style="font-size: 1.4rem;">120k Ft</div>',
     '<div class="service-price-value" style="font-size: 1.4rem;">Egyedi ajánlat</div>'),
    ('<div class="service-price-label">Fix-árú diagnosztika</div>\n                        <div class="service-price-value" style="font-size: 1.4rem;">120k Ft</div>\n                        <div class="service-price-note">~2 hét, írásos riport</div>',
     '<div class="service-price-label">Diagnosztika</div>\n                        <div class="service-price-value" style="font-size: 1.4rem;">Egyedi ajánlat</div>\n                        <div class="service-price-note">~2 hét, írásos riport</div>'),

    # Service Price Value 06
    ('<div class="service-price-value" style="font-size: 1.4rem;">150k Ft-tól</div>',
     '<div class="service-price-value" style="font-size: 1.4rem;">Audit-alapú</div>'),
    ('<div class="service-price-label">Audit utáni egyedi</div>\n                        <div class="service-price-value" style="font-size: 1.4rem;">150k Ft-tól</div>\n                        <div class="service-price-note">scope-tól függően</div>',
     '<div class="service-price-label">Árazási modell</div>\n                        <div class="service-price-value" style="font-size: 1.4rem;">Audit-alapú</div>\n                        <div class="service-price-note">scope-tól függően</div>'),

    # Pricing Grid Cards
    ('<div class="pricing-price"><span style="color: var(--cyan)">0 Ft</span> <span>~30 perc</span></div>',
     '<div class="pricing-price"><span style="color: var(--cyan)">Díjmentes</span> <span>~30 perc</span></div>'),
    ('<div class="pricing-price"><span style="color: var(--magenta)">120k Ft</span> <span>~2 hét</span></div>',
     '<div class="pricing-price"><span style="color: var(--magenta)">Egyedi ajánlat</span> <span>~2 hét</span></div>'),
]

# 3. webaruhaz-keszites.html replacements
webaruhaz_replacements = [
    ('EAA-megfelelés, audit-alapú árazás 800k+ Ft. CENTAUR-ügynökség Győrből.',
     'EAA-megfelelés, audit-alapú egyedi árazás. CENTAUR-ügynökség Győrből.'),
    ('EAA-megfelelés, audit-alapú árazás 800k+ Ft.',
     'EAA-megfelelés, audit-alapú egyedi árazás.'),
    ('"description": "Audit utáni egyedi árazás. Tipikus belépési szint: 800.000 Ft-tól."',
     '"description": "Audit utáni egyedi árazás."'),
    ('Tipikus belépési szint: 800.000 Ft-tól. AX-audit önállóan választható: fix 120k Ft / ~2 hét.',
     'AX-audit önállóan is kérhető.'),
    ('AX-audit önállóan: fix 120k Ft / ~2 hét. Pontos árajánlat a 30-perces',
     'AX-audit önállóan is kérhető. Pontos árajánlat a 30-perces'),
    ('opcionális AX-audit (120k Ft / ~2 hét)',
     'opcionális AX-audit'),
    ('AX-audit (opcionális, 120k Ft / ~2 hét)',
     'AX-audit (opcionális)'),
    ('<p style="font-size: 1.4rem; color: var(--cyan); font-weight: 700;">800.000 Ft-tól</p>',
     '<p style="font-size: 1.4rem; color: var(--cyan); font-weight: 700;">Egyedi ajánlat</p>'),
    ('ott 600k–1.5M Ft a tipikus tartomány',
     'ott egyedi árazással dolgozunk'),
    ('Tipikus belépés: <strong>800.000 Ft-tól</strong>.',
     'Tipikus belépés: <strong>Egyedi ajánlat alapján</strong>.'),
]

# 4. weboldal-keszites.html replacements
weboldal_replacements = [
    ('szekcióban pedig az induló árak is megvannak.',
     'szekcióban pedig a részletek is megvannak.'),
    ('Fix induló sávokkal indulunk, majd tételes ajánlatot adunk a végleges scope alapján.',
     'Egyedi ajánlatot adunk a végleges scope alapján.'),
    ('Nem „X oldal = Y Ft” fix formula.',
     'Nem „X oldal = Y Ft” fix formula, hanem egyedi scope alapján árazunk.'),
    ('Fix induló sávok a szolgáltatások oldalon, részletes ajánlat a workshop után.',
     'Egyedi ajánlat a workshop után.'),
]

# 5. wordpress-weboldal-modernizalas.html replacements
modernizalas_replacements = [
    ('Fix induló sávok a szolgáltatásoldalon, tételes ajánlat az audit után.',
     'Egyedi ajánlat az audit után.'),
    ('lefedve a szolgáltatások oldalon a WooCommerce / Shopify / egyedi sávokat.',
     'lefedve a szolgáltatások oldalon a WooCommerce / Shopify / egyedi megközelítést.'),
    ('WooCommerce / Shopify / egyedi webshop induló sávokat',
     'WooCommerce / Shopify / egyedi webshop részleteket'),
    ('szekcióban pedig az induló árak is megvannak.',
     'szekcióban pedig a részletek is megvannak.'),
    ('Fix induló sávok a szolgáltatások oldalon, részletes ajánlat a workshop után.',
     'Egyedi ajánlat a workshop után.'),
    ('Nem „X oldal = Y Ft” fix formula.',
     'Nem „X oldal = Y Ft” fix formula, hanem egyedi scope alapján árazunk.'),
]

# 6. Lokális SEO city pages replacements (they all have this grid at lines 1058+)
city_replacements = [
    ('<div style="font-size: clamp(1.2rem, 3vw, 1.8rem); font-weight: 700; margin-bottom: 0.5rem; color: var(--white);">600k – 1.5M Ft</div>',
     '<div style="font-size: clamp(1.2rem, 3vw, 1.8rem); font-weight: 700; margin-bottom: 0.5rem; color: var(--white);">Audit-alapú</div>'),
    ('<div style="font-size: clamp(1.2rem, 3vw, 1.8rem); font-weight: 700; margin-bottom: 0.5rem; color: var(--white);">450k – 1.2M Ft</div>',
     '<div style="font-size: clamp(1.2rem, 3vw, 1.8rem); font-weight: 700; margin-bottom: 0.5rem; color: var(--white);">Audit-alapú</div>'),
    ('<div style="font-size: clamp(1.2rem, 3vw, 1.8rem); font-weight: 700; margin-bottom: 0.5rem; color: var(--white);">250k+ Ft / hó</div>',
     '<div style="font-size: clamp(1.2rem, 3vw, 1.8rem); font-weight: 700; margin-bottom: 0.5rem; color: var(--white);">Audit-alapú</div>'),
]

# Process Core Files
print("=== Processing Core Files ===")
process_file(os.path.join(workspace_dir, "index.html"), index_replacements)
process_file(os.path.join(workspace_dir, "szolgaltatasok.html"), szolgaltatasok_replacements)
process_file(os.path.join(workspace_dir, "webaruhaz-keszites.html"), webaruhaz_replacements)
process_file(os.path.join(workspace_dir, "weboldal-keszites.html"), weboldal_replacements)
process_file(os.path.join(workspace_dir, "wordpress-weboldal-modernizalas.html"), modernizalas_replacements)

# Process City Pages
print("\n=== Processing City Pages ===")
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

for city_file in city_files:
    file_path = os.path.join(workspace_dir, city_file)
    if os.path.exists(file_path):
        print(f"Processing: {city_file}")
        process_file(file_path, city_replacements)
    else:
        print(f"WARNING: File {city_file} does not exist!")

print("\n=== Cleanup finished successfully! ===")
