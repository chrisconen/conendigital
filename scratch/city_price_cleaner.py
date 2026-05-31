import os

workspace_dir = r"g:\CONEN DIGITAL"

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

city_replacements = [
    ('<option value="small">200.000 - 500.000 Ft</option>',
     '<option value="small">Fókuszált céges honlap / landing</option>'),
    ('<option value="medium">500.000 - 1.000.000 Ft</option>',
     '<option value="medium">Komplett üzleti honlap (blog, aloldalak)</option>'),
    ('<option value="large">1.000.000 - 2.500.000 Ft</option>',
     '<option value="large">Webáruház / E-commerce rendszer</option>'),
    ('<option value="enterprise">2.500.000 Ft +</option>',
     '<option value="enterprise">Egyedi fejlesztés & AI automatizáció</option>'),
]

for city_file in city_files:
    file_path = os.path.join(workspace_dir, city_file)
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        modified = False
        for old_str, new_str in city_replacements:
            if old_str in content:
                content = content.replace(old_str, new_str)
                modified = True
        
        if modified:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Successfully cleaned prices in: {city_file}")
        else:
            print(f"No replacements matched in: {city_file}")
    else:
        print(f"WARNING: File {city_file} does not exist!")

print("\n=== City pages pricing cleanup completed! ===")
