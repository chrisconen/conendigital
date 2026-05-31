import os

workspace_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
blog_src_dir = os.path.join(workspace_dir, "conen-blog", "src", "content", "blog")

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
            print(f"  Replaced in {os.path.basename(file_path)}: '{old_str.strip()[:60]}...' -> '{new_str.strip()[:60]}...'")
    
    if modified:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"  Saved modified file: {file_path}")
    else:
        print(f"  No replacements matched in: {file_path}")

# 1. ai-chatbot-weboldalra.md
chatbot_replacements = [
    ("**Build**: a chatbot integrálása a weboldalra: 150-300k Ft (a komplexitástól függ).",
     "**Build**: a chatbot integrálása a weboldalra: egyedi scope alapján."),
    ("**Havi díj**: 250.000 Ft/hó-tól (#service-ai-ops).",
     "**Havi díj**: egyedi ajánlat szerint (#service-ai-ops).")
]

# 2. eaa-megfeleles-2026.md
eaa_replacements = [
    ("Az AX-audit (120.000 Ft) 100%-ban beszámít a projekt költségébe.",
     "Az AX-audit (díjmentes beszámítással) 100%-ban beszámít a projekt költségébe.")
]

# 3. mcp-endpoint.md
mcp_replacements = [
    ("Az alap: 250.000 Ft/hó-tól, ami tartalmazza a hosting-ot, monitoringot, és a frissítéseket.",
     "Egyedi havi díj alapján, ami tartalmazza a hosting-ot, monitoringot, és a frissítéseket.")
]

# 4. weboldal-karbantartas.md
karbantartas_replacements = [
    ("| Tartalom-frissítés | Igény szerint | 15k Ft/alkalom |",
     "| Tartalom-frissítés | Igény szerint | Egyedi megállapodás |"),
    ("| Éves felülvizsgálat | Éves | 50k Ft |",
     "| Éves felülvizsgálat | Éves | Egyedi megállapodás |"),
    ("| Plugin frissítés | Havi | 25k Ft/hó |",
     "| Plugin frissítés | Havi | Egyedi megállapodás |"),
]

# 5. weboldal-keszites-vagy-sablon.md
sablon_replacements = [
    ("| Induló költség | 0-50k Ft | 400k+ Ft |",
     "| Induló költség | Minimális | Érték- és scope alapú |")
]

# 6. wordpress-vs-egyedi-2026.md
wordpress_replacements = [
    ("- **Rövid távú budget**: egy sablonos WordPress oldal 150-250k Ft-ból megvan",
     "- **Rövid távú budget**: egy egyszerű sablonos WordPress oldal alacsony induló költséggel is megoldható")
]

# Run replacements
print("=== Cleaning Source Markdown Blog Posts ===")
process_file(os.path.join(blog_src_dir, "ai-chatbot-weboldalra.md"), chatbot_replacements)
process_file(os.path.join(blog_src_dir, "eaa-megfeleles-2026.md"), eaa_replacements)
process_file(os.path.join(blog_src_dir, "mcp-endpoint.md"), mcp_replacements)
process_file(os.path.join(blog_src_dir, "weboldal-karbantartas.md"), karbantartas_replacements)
process_file(os.path.join(blog_src_dir, "weboldal-keszites-vagy-sablon.md"), sablon_replacements)
process_file(os.path.join(blog_src_dir, "wordpress-vs-egyedi-2026.md"), wordpress_replacements)

# 7. Completely rewrite weboldal-keszites-arak-2026.md
arak_post_path = os.path.join(blog_src_dir, "weboldal-keszites-arak-2026.md")
new_arak_post_content = """---
title: "Weboldal készítés árazás 2026: Miért csapda a fix árajánlat, és hogyan működik a prémium árazás?"
summary: "A hagyományos fix csomagok és a 400.000 Ft-os sablonok látszólag kiszámíthatóak, de hosszú távon versenyhátrányt okoznak. Bemutatjuk a valódi értékalapú árazást és a CENTAUR-megközelítést."
publishedAt: 2026-05-08
category: "Site Factory"
tags: ["weboldal készítés", "árak", "KKV", "költségvetés"]
author: "Chris Conen"
readingTime: 5
draft: false
---

A „mennyibe kerül egy weboldal?" a leggyakoribb kérdés, amit kapunk. A válasz: **attól függ** — de nem azért, mert kitérünk, hanem mert a scope és az üzleti érték határozza meg a fejlesztés mértékét.

## A fix áras csapdák

Sok vállalkozás fix csomagok közül választ (pl. „Alap weboldal”, „Profi webshop”), abban a hiszemben, hogy ezzel minimalizálja a kockázatot. Ez azonban a legtöbbször kétféleképpen végződik:
1. **Alulárazott kivitelezés**: A fejlesztő menet közben szembesül a valós igényekkel, csúszni kezd a projekt, elhanyagolja a minőséget (pl. a PageSpeed és az EAA-megfelelés elmarad), végül egy használhatatlan oldalt kapsz.
2. **Túlbiztosított árazás**: A fejlesztő hatalmas puffereket épít be az árba, így sokkal többet fizetsz, mint amit a valódi scope indokolna.

Mi nem árulunk előre csomagolt sablonokat, mert minden sikeres vállalkozás egyedi folyamatokat követ.

## Hogyan határozzuk meg az értéket?

A mi megközelítésünk a **valós cost-driverekre** és a megtérülésre fókuszál. Egy weboldal nem dekoráció — hanem a sales és a mérések központi belső pontja. Ezek a tényezők alakítják a scope-ot:

- **Ügyfélút komplexitása**: Milyen automatizált lépések történnek az űrlap kitöltése után? (CRM-integráció, e-mail szekvenciák, automata ajánlatkészítés)
- **Funkcionális igények**: Szükséges-e egyedi kalkulátor, konfigurátor, vagy naptár-integráció?
- **Akadálymentesítés**: EAA (European Accessibility Act) WCAG 2.2 AA szintű natív megfelelés biztosítása.
- **AX-readiness**: Strukturált JSON-LD adatok és MCP-endpointok kiépítése az AI-asszisztensek (ChatGPT, Perplexity, Claude) kiszolgálására.

## Az audit-alapú árazás előnye

Nálunk nincs találgatás. A projekt minden esetben egy **30 perces díjmentes diagnosztikai videohívással** indul, ahol megnézzük a jelenlegi rendszeredet.

Ezt követi az opcionális **AX-audit (Agent Experience)**, amely egy önálló diagnosztikai termék. Az audit során feltérképezzük az oldal jelenlegi AI-olvashatóságát, sebességét, EAA-állapotát és egy számozott prioritás-riportot adunk.

> [!IMPORTANT]
> Az AX-audit költsége 100%-ban jóváírásra és beszámításra kerül a későbbi egyedi fejlesztési díjból, így ez a fázis nem jelent extra kiadást a teljes projekt szintjén.

## Hol térül meg a befektetés?

Egy professzionálisan összerakott, egyedi Astro 5 frontenddel épített oldal hosszú távon lényegesen olcsóbb, mint a folyamatosan foltozott sablonos rendszerek:
- **Sebesség**: A zöld Core Web Vitals jobb Google helyezést és alacsonyabb hirdetési költséget (CPC) eredményez.
- **Automatizáció**: Ha a weboldalad naponta több órát takarít meg az adminisztráción, az a leggyorsabban megtérülő fejlesztés.
- **AI-láthatóság**: Az AX-ready oldalak bekerülnek az AI-asszisztensek ajánlásaiba, új, prémium leadeket hozva.
"""

with open(arak_post_path, 'w', encoding='utf-8') as f:
    f.write(new_arak_post_content.strip())
print(f"  Successfully rewrote {arak_post_path} into a premium positioning article.")

print("\n=== Blog posts cleanups completed! ===")
