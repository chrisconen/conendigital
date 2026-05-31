import os
import re

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

patterns = [
    re.compile(r'\d{3}\s*(?:k|M)'), # e.g. 600k, 150k
    re.compile(r'\d+\s*(?:ezer|millió)\s*Ft'), # e.g. 5 ezer Ft
    re.compile(r'\b\d+(?:\.\d{3})+\s*(?:Ft-tól|Ft/hó|Ft)\b', re.IGNORECASE),
]

for city_file in city_files:
    file_path = os.path.join(workspace_dir, city_file)
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        matches = []
        for i, line in enumerate(content.splitlines(), 1):
            for pat in patterns:
                if pat.search(line):
                    matches.append((i, line.strip()))
                    break
        if matches:
            print(f"File: {city_file} ({len(matches)} matches)")
            for idx, line in matches:
                print(f"  Line {idx}: {line}")
        else:
            print(f"File: {city_file} - No price references found.")
