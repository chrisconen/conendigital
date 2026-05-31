import os

# Dynamically find workspace directory (parent of scratch folder)
workspace_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def process_file(file_path, replacements):
    if not os.path.exists(file_path):
        print(f"WARNING: File does not exist: {file_path}")
        return
        
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    modified = False
    for old_str, new_str in replacements:
        if old_str in content:
            content = content.replace(old_str, new_str)
            modified = True
            print(f"  Replaced: '{old_str.strip()[:60]}...' -> '{new_str.strip()[:60]}...'")
    
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
    
    # Meta / Description
    ('"description": "Audit utáni egyedi árazás, havi modell. Tipikus: 250.000 Ft-tól / hó."',
     '"description": "Audit-alapú egyedi árazás és havi támogatás az éles növekedésért."'),
     
    # Schema Offers
    ('''          "offers": {
            "@type": "AggregateOffer",
            "priceCurrency": "HUF",
            "lowPrice": "600000",
            "highPrice": "1500000",
            "description": "Audit utáni egyedi árazás, tipikus tartomány."
          }''',
     '''          "offers": {
            "@type": "Offer",
            "description": "Audit-alapú egyedi árazás."
          }'''),
          
    ('''          "offers": {
            "@type": "AggregateOffer",
            "priceCurrency": "HUF",
            "lowPrice": "450000",
            "highPrice": "1200000",
            "description": "Audit utáni egyedi árazás, tipikus tartomány."
          }''',
     '''          "offers": {
            "@type": "Offer",
            "description": "Audit-alapú egyedi árazás."
          }'''),
          
    ('''          "offers": {
            "@type": "Offer",
            "priceCurrency": "HUF",
            "description": "Audit utáni egyedi árazás, havi modell. Tipikus: 250.000 Ft-tól / hó."
          }''',
     '''          "offers": {
            "@type": "Offer",
            "description": "Audit-alapú egyedi árazás és havi támogatás."
          }'''),
    
    # Hero Title lines
    ('<span class="hero-title-gradient">havi 5 ezer Ft-tól</span>',
     '<span class="hero-title-gradient">Egyedi fejlesztés</span>'),
    ('<span class="hero-title-subline">bérelhető weboldalak és webáruházak',
     '<span class="hero-title-subline">& AI automatizáció'),
    
    # Prices in services section (Pillar 1, 2, 3 pricing text)
    ('tipikus tartomány: 100.000 – 300.000 Ft',
     'személyre szabott scope szerint'),
    ('tipikus tartomány: 250.000 – 600.000 Ft',
     'személyre szabott scope szerint'),
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
    ('"description": "Audit utáni egyedi árazás. Tipikus: 250.000 Ft-tól / hó."',
     '"description": "Audit-alapú egyedi árazás."'),

    # Visual service prices
    ('<div class="service-price-value" style="font-size: 1.4rem;">600k – 1.5M Ft</div>',
     '<div class="service-price-value" style="font-size: 1.4rem;">Audit-alapú</div>'),
    ('<div class="service-price-value" style="font-size: 1.4rem;">450k – 1.2M Ft</div>',
     '<div class="service-price-value" style="font-size: 1.4rem;">Audit-alapú</div>'),
    ('<div class="service-price-value" style="font-size: 1.4rem;">800k Ft-tól</div>',
     '<div class="service-price-value" style="font-size: 1.4rem;">Audit-alapú</div>'),
    ('<div class="service-price-value" style="font-size: 1.4rem;">120k Ft</div>',
     '<div class="service-price-value" style="font-size: 1.4rem;">Egyedi ajánlat</div>'),
    ('<div class="service-price-value" style="font-size: 1.4rem;">150k Ft-tól</div>',
     '<div class="service-price-value" style="font-size: 1.4rem;">Audit-alapú</div>'),
     
    ('<div class="service-price-note">tipikus tartomány</div>',
     '<div class="service-price-note">egyedi scope szerint</div>'),
    ('<div class="service-price-label">Audit utáni egyedi</div>',
     '<div class="service-price-label">Árazási modell</div>'),
    ('<div class="service-price-label">Audit utáni egyedi, havi</div>',
     '<div class="service-price-label">Árazási modell</div>'),
    ('<div class="service-price-note">tipikus belépési szint</div>',
     '<div class="service-price-note">egyedi havi díj</div>'),
    ('<div class="service-price-label">Fix-árú diagnosztika</div>',
     '<div class="service-price-label">Diagnosztika</div>'),
    ('<div class="service-price-note">~2 hét, írásos riport</div>',
     '<div class="service-price-note">~2 hét, írásos riport</div>'),
    ('<div class="service-price-note">scope-tól függően</div>',
     '<div class="service-price-note">scope-tól függően</div>'),

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
    ('"description": "Audit utáni egyedi árazás. Tipikus belépési szint: 800.000 Ft-tól."',
     '"description": "Audit utáni egyedi árazás."'),
    ('"text": "Audit-alapú. Nem termékszám, hanem a checkout komplexitása (fizetés, futár, számlázás), integrációk mélysége, MCP-endpoint igény, jogi követelmények, többnyelvűség és platformválasztás. Tipikus belépési szint: 800.000 Ft-tól. AX-audit önállóan választható: fix 120k Ft / ~2 hét."',
     '"text": "Audit-alapú. Nem termékszám, hanem a checkout komplexitása, integrációk mélysége, MCP-endpoint igény, jogi követelmények, többnyelvűség és platformválasztás. Egyedi árazás. AX-audit önállóan is kérhető."'),
    ('opcionális AX-audit (120k Ft / ~2 hét)',
     'opcionális AX-audit'),
    ('<h3>AX-audit (opcionális, 120k Ft / ~2 hét)</h3>',
     '<h3>AX-audit (opcionális)</h3>'),
    ('<p style="font-size: 1.4rem; color: var(--cyan); font-weight: 700;">800.000 Ft-tól</p>',
     '<p style="font-size: 1.4rem; color: var(--cyan); font-weight: 700;">Egyedi ajánlat</p>'),
    ('ott 600k–1.5M Ft a tipikus tartomány',
     'ott egyedi árazással dolgozunk'),
    ('<strong>Audit-alapú</strong>, nem csomag. Tipikus belépés: <strong>800.000 Ft-tól</strong>.',
     '<strong>Audit-alapú</strong>, nem csomag. Tipikus belépés: <strong>Egyedi ajánlat alapján</strong>.'),
    ('AX-audit önállóan: fix 120k Ft / ~2 hét.',
     'AX-audit önállóan is kérhető.'),
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
    ('Audit-alapú árazás 450k-1.2M Ft tipikus tartomány. CENTAUR-ügynökség.',
     'Audit-alapú egyedi árazás. CENTAUR-ügynökség.'),
    ('"text": "Audit-alapú. A meglévő oldal komplexitása (oldalszám, plugin-szám, egyedi kód, tartalom-mennyiség), az EAA-állapot kiindulása, az integrációk (űrlap, e-mail, CRM) és a migrációs scope együtt. Tipikus tartomány: 450.000 – 1.200.000 Ft. AX-audit önállóan: fix 120k Ft / ~2 hét. A pontos árajánlat a 30-perces díjmentes diagnosztika után."',
     '"text": "Audit-alapú. A meglévő oldal komplexitása (oldalszám, plugin-szám, egyedi kód, tartalom-mennyiség), az EAA-állapot kiindulása, az integrációk és a migrációs scope együtt. Egyedi árazás. AX-audit önállóan is kérhető. A pontos árajánlat a 30-perces díjmentes diagnosztika után."'),
    ('<p style="font-size: 1.4rem; color: var(--cyan); font-weight: 700;">450.000 – 1.200.000 Ft</p>',
     '<p style="font-size: 1.4rem; color: var(--cyan); font-weight: 700;">Egyedi ajánlat</p>'),
    ('fix 120.000 Ft / ~2 hét',
     'egyedi ajánlat alapján / ~2 hét'),
    ('<strong>450.000 – 1.200.000 Ft</strong>. AX-audit önállóan: 120k Ft / ~2 hét.',
     '<strong>Egyedi ajánlat alapján</strong>. AX-audit önállóan is kérhető.'),
]

# 6. kapcsolat.html replacements
kapcsolat_replacements = [
    # Schema FAQs
    ('"text": "Először egy ingyenes diagnosztikai videohívás (~30 perc). Ott eldől, hogy van-e értelme tovább menni. Ha igen, opcionális AX-audit (120k Ft, ~2 hét) vagy közvetlenül scope + ajánlat (~1 hét). Az árak audit-alapúak, nem fix csomagok."',
     '"text": "Először egy ingyenes diagnosztikai videohívás (~30 perc). Ott eldől, hogy van-e értelme tovább menni. Ha igen, opcionális AX-audit (egyedi ajánlat alapján, ~2 hét) vagy közvetlenül scope + ajánlat (~1 hét). Az árak audit-alapúak, nem fix csomagok."'),
    ('"text": "Az Agent Experience audit egy önálló diagnosztikai termék: megnézzük a meglévő oldal AI-asszisztens-kompatibilitását. JSON-LD lefedettség, /llms.txt, MCP-feasibility, versenytárs-benchmark. Eredmény: számozott akcióterv. 120k Ft, ~2 hét."',
     '"text": "Az Agent Experience audit egy önálló diagnosztikai termék: megnézzük a meglévő oldal AI-asszisztens-kompatibilitását. JSON-LD lefedettség, /llms.txt, MCP-feasibility, versenytárs-benchmark. Eredmény: számozott akcióterv. Egyedi ajánlat alapján, ~2 hét."'),
    
    # Dropdown Options
    ('<option value="small">Alap weboldal, 5 ezer Ft/hó</option>',
     '<option value="small">Fókuszált céges honlap / landing</option>'),
    ('<option value="medium">Starter weboldal 15 ezer F/hó</option>',
     '<option value="medium">Komplett üzleti honlap (blog, aloldalak)</option>'),
    ('<option value="large">Profi weboldal 25 ezer Ft/hó</option>',
     '<option value="large">Webáruház / E-commerce rendszer</option>'),
     
    # Text FAQs
    ('<strong>2. AX-audit (opcionális)</strong> — 120k Ft, ~2 hét, írásos riport és számozott',
     '<strong>2. AX-audit (opcionális)</strong> — Egyedi ajánlat alapján, ~2 hét, írásos riport és számozott'),
    ('Fix ár: 120k Ft, ~2 hét.',
     'Egyedi ajánlat alapján, ~2 hét.'),
]

# 7. portfolio.html replacements
portfolio_replacements = [
    ('AX-audit (120k Ft / ~2 hét) közbeiktatva',
     'AX-audit (egyedi ajánlat alapján, ~2 hét) közbeiktatva')
]

# 8. weboldal-konfigurator-v2.html replacements
konfigurator_replacements = [
    ('AX-audit (120k Ft) 100%-ban beszámít.',
     'AX-audit (díjmentes beszámítással) 100%-ban beszámít.'),
    ('250.000 Ft / hó-tól',
     'Egyedi havi díj'),
    ('600k – 1.2M Ft',
     'Egyedi ajánlat'),
    ("lines.push('+ AI OPS HAVI: 250.000 Ft/hó-tól (' + aiOps.join(', ') + ') — külön szerződés');",
     "lines.push('+ AI OPS HAVI: egyedi ajánlat szerint (' + aiOps.join(', ') + ') — külön szerződés');"),
    ("p1.push('AX-audit (120k Ft) — 100%-ban beszámít');",
     "p1.push('AX-audit (díjmentes beszámítással) — 100%-ban beszámít');"),
    ("p1.push('Scope-dokumentum + fix árajánlat');",
     "p1.push('Scope-dokumentum + egyedi ajánlat');"),
    ("<p>Audit-alapú árazás. AX-audit (120k Ft) 100%-ban beszámít a végösszegbe.${aiOps.length ? ' Az AI-funkciók ('+aiOps.join(', ')+') külön havi szerződés keretében működnek, 250.000 Ft/hó-tól.' : ''}</p>",
     "<p>Audit-alapú árazás. AX-audit (díjmentes beszámítással) 100%-ban beszámít a végösszegbe.${aiOps.length ? ' Az AI-funkciók ('+aiOps.join(', ')+') külön havi szerződés keretében működnek, egyedi havi díj alapján.' : ''}</p>"),
    ("document.getElementById('rAmt').textContent = fmtHUF(r.l) + ' – ' + fmtHUF(r.h);",
     "document.getElementById('rAmt').textContent = 'Egyedi scope alapján';"),
    ('<div class="pdf-price">${fmtHUF(r.l)} – ${fmtHUF(r.h)}</div>',
     '<div class="pdf-price">Egyedi ajánlat</div>'),
    ("lines.push('', 'NAGYSÁGRENDI TARTOMÁNY (build): ' + fmtHUF(r.l) + ' – ' + fmtHUF(r.h));",
     "lines.push('', 'NAGYSÁGRENDI TARTOMÁNY (build): Audit-alapú egyedi ajánlat');")
]

# 9. City pages replacements (all 15 files)
city_replacements = [
    ('<option value="small">200.000 - 500.000 Ft</option>',
     '<option value="small">Fókuszált céges honlap / landing</option>'),
    ('<option value="medium">500.000 - 1.000.000 Ft</option>',
     '<option value="medium">Komplett üzleti honlap (blog, aloldalak)</option>'),
    ('<option value="large">1.000.000 - 2.500.000 Ft</option>',
     '<option value="large">Webáruház / E-commerce rendszer</option>'),
    ('<option value="enterprise">2.500.000 Ft +</option>',
     '<option value="enterprise">Bespoke AI-integráció & egyedi platform</option>'),
]

# Run replacements
print("=== Cleaning Core Pages ===")
process_file(os.path.join(workspace_dir, "index.html"), index_replacements)
process_file(os.path.join(workspace_dir, "szolgaltatasok.html"), szolgaltatasok_replacements)
process_file(os.path.join(workspace_dir, "webaruhaz-keszites.html"), webaruhaz_replacements)
process_file(os.path.join(workspace_dir, "weboldal-keszites.html"), weboldal_replacements)
process_file(os.path.join(workspace_dir, "wordpress-weboldal-modernizalas.html"), modernizalas_replacements)
process_file(os.path.join(workspace_dir, "kapcsolat.html"), kapcsolat_replacements)
process_file(os.path.join(workspace_dir, "portfolio.html"), portfolio_replacements)
process_file(os.path.join(workspace_dir, "weboldal-konfigurator-v2.html"), konfigurator_replacements)

# Run replacements for City Pages
print("\n=== Cleaning City Pages ===")
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
    print(f"Processing: {city_file}")
    process_file(file_path, city_replacements)

print("\n=== All price cleanups completed successfully! ===")
