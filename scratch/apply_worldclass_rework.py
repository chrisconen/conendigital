import os
import re

workspace_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

print(f"Applying World-Class Rework to Conen Digital under: {workspace_dir}")

# Define the font injection block
google_fonts_link = """    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&family=Inter+Tight:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500;600;700&display=swap" rel="stylesheet">"""

# Define stylesheet variables override to inject into the style tag
style_override = """
        :root {
            --black: #09090b;          /* Pure obsidian black */
            --white: #ffffff;
            --gray: #141416;           /* Premium charcoal */
            --gray-light: #222225;
            --cyan: #C9A962;           /* Champagne Gold */
            --magenta: #8A8A8F;        /* Muted gold-glow/silver */
            --orange: #C99566;         /* Warm copper */
            --font-main: 'Space Grotesk', sans-serif;
            --font-body: 'Inter Tight', -apple-system, sans-serif;
            --font-mono: 'JetBrains Mono', monospace;
        }
        body, p, li, a, td, th, input, textarea, select {
            font-family: var(--font-body) !important;
        }
        h1, h2, h3, h4, h5, h6, .glitch, .nav-logo, .nav-logo-text, .hero-title-line, .hero-title-gradient, .hero-title-subline {
            font-family: var(--font-main) !important;
        }
        .cursor, .cursor-trail, #cursorTrailContainer, .scanlines {
            display: none !important;
        }
        body {
            cursor: auto !important;
        }
"""

def apply_global_system_overrides(path):
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Replace Google Fonts loading
    font_pattern = re.compile(r'<link[^>]*fonts\.googleapis\.com[^>]*family=Space\+Grotesk[^>]*>')
    if font_pattern.search(content):
        content = font_pattern.sub(google_fonts_link, content)
    else:
        # Fallback to general replacement of fonts.googleapis
        general_font_pattern = re.compile(r'<link[^>]*href="[^"]*fonts\.googleapis\.com[^"]*"[^>]*>(?:\s*<link[^>]*href="[^"]*fonts\.gstatic\.com[^"]*"[^>]*>)?(?:\s*<link[^>]*href="[^"]*fonts\.googleapis\.com/css2[^"]*"[^>]*>)?')
        if general_font_pattern.search(content):
            content = general_font_pattern.sub(google_fonts_link, content)

    # Inject variables override in first <style> tag
    style_match = re.search(r'<style[^>]*>', content, re.IGNORECASE)
    if style_match:
        pos = style_match.end()
        content = content[:pos] + style_override + content[pos:]

    return content

# 1. REWORK INDEX.HTML
index_path = os.path.join(workspace_dir, "index.html")
if os.path.exists(index_path):
    print("Reworking index.html...")
    content = apply_global_system_overrides(index_path)

    # Rework Hero Title & Description
    old_title_pattern = re.compile(r'<h1 class="hero-title">.*?</h1>', re.DOTALL)
    new_title = """<h1 class="hero-title">
                    <span class="hero-title-line">Prémium webáruház & egyedi weboldal készítés Győr szívében -
                    <span class="hero-title-gradient">Valódi vevőket szerző rendszerek</span> 
                    <span class="hero-title-subline">& Önműködő folyamatok
                    </span></span>
                </h1>"""
    content = old_title_pattern.sub(new_title, content)

    old_desc_pattern = re.compile(r'<p class="hero-description">.*?</p>', re.DOTALL)
    new_desc = """<p class="hero-description">
                    Egy weboldal vagy webáruház akkor ér igazán valamit, ha nemcsak szép, hanem új ügyfeleket és vásárlókat szerez neked – teljesen önműködően. Nem sablonokat másolunk: teljesen egyedi tervezésű, villámgyors és mesterséges intelligenciával támogatott megoldásokat adunk át, amelyek bizonyíthatóan behozzák az árukat. 
                    Ráadásul a keresők és a legújabb AI-asszisztensek is látják és ajánlják a vállalkozásodat az ügyfeleknek – a nap 24 órájában, Győrtől az egész országig.
                </p>"""
    content = old_desc_pattern.sub(new_desc, content)

    # Inject NEXUS Proof Section right after Hero Section
    hero_end_pattern = re.compile(r'</section>\s*<!--\s*Hogyan működik', re.IGNORECASE)
    nexus_section = """</section>

    <!-- NEXUS AI PROOF SECTION -->
    <section class="nexus-proof-section" style="padding: 80px 20px; background: rgba(255, 255, 255, 0.02); border-top: 1px solid var(--glass-border); border-bottom: 1px solid var(--glass-border); position: relative; overflow: hidden;">
        <div style="position: absolute; inset: 0; background: radial-gradient(circle at center, rgba(201, 169, 98, 0.05) 0%, transparent 70%); pointer-events: none;"></div>
        <div class="centaur-section-inner" style="max-width: 1000px; margin: 0 auto; text-align: center; position: relative; z-index: 1;">
            <div style="display: inline-flex; align-items: center; gap: 8px; background: rgba(201, 169, 98, 0.1); border: 1px solid rgba(201, 169, 98, 0.3); border-radius: 30px; padding: 6px 16px; margin-bottom: 24px;">
                <span style="font-family: var(--font-mono); font-size: 0.7rem; letter-spacing: 0.15em; text-transform: uppercase; color: var(--cyan); font-weight: 600;">NEXUS · AZ ÉLŐ BIZONYÍTÉK</span>
            </div>
            <h2 style="font-size: clamp(1.8rem, 4vw, 2.8rem); font-weight: 700; margin-bottom: 20px; color: var(--white); font-family: var(--font-main); line-height: 1.2;">Az Ember és a Mesterséges Intelligencia közös ereje működés közben</h2>
            <p style="font-size: 1.15rem; color: var(--silver); max-width: 800px; margin: 0 auto 32px; line-height: 1.7; font-family: var(--font-body);">
                Mi nemcsak beszélünk a modern, intelligens megoldásokról – megépítettük a <strong>NEXUS</strong>-t, a Conen Digital saját, intelligens tervező és specifikációs rendszerét. A NEXUS a kézzelfogható bizonyítéka annak, hogyan képes a technológia és az emberi tapasztalat fúziója a töredékére csökkenteni a tervezési időt, miközben 100%-os precizitást nyújt. Próbáld ki a NEXUS-t élőben, és tervezd meg a saját projektedet mindössze 10 perc alatt!
            </p>
            <a href="https://app.conendigital.hu" class="nav-konfigurator-btn" style="display: inline-flex; align-items: center; gap: 0.5rem; padding: 1.1rem 2.2rem; background: var(--cyan); color: var(--black); font-family: var(--font-mono); font-size: 0.9rem; font-weight: 700; border-radius: 4px; letter-spacing: 0.05em; transition: all 0.2s; text-decoration: none; box-shadow: 0 4px 24px rgba(201,169,98,0.25);" onmouseover="this.style.background='transparent';this.style.color='var(--cyan)';this.style.boxShadow='inset 0 0 0 1px var(--cyan), 0 0 24px rgba(201,169,98,0.4)'" onmouseout="this.style.background='var(--cyan)';this.style.color='var(--black)';this.style.boxShadow='0 4px 24px rgba(201,169,98,0.25)'">Elindítom a NEXUS Tervezőt →</a>
        </div>
    </section>

    <!-- Hogyan működik"""
    content = hero_end_pattern.sub(nexus_section, content)

    # Rework "Three Situations" headlines & texts
    content = content.replace("Három helyzet, ahol egy \"szebb weboldal\" már nem segít", "Három helyzet, ahol a hagyományos weboldal már nem elég")
    content = content.replace("Az adminisztráció felemészti a napot", "Elveszel a napi papírmunkában és adminisztrációban?")
    content = content.replace("Az érdeklődő nem ér rá várni", "Vevőket veszítesz azért, mert túl lassan adsz árajánlatot?")
    content = content.replace("A meglévő oldal csak viszi a pénzt", "A weboldalad csak egy digitális névjegykártya, ami nem hoz vevőt?")

    # Save index.html
    with open(index_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("index.html completed.")

# 2. REWORK SZOLGALTATASOK.HTML
szolg_path = os.path.join(workspace_dir, "szolgaltatasok.html")
if os.path.exists(szolg_path):
    print("Reworking szolgaltatasok.html...")
    content = apply_global_system_overrides(szolg_path)

    # Rework text and headlines
    content = content.replace("Három pillér, audit-alapú árazás", "Három pillérünk a vállalkozásod digitális növekedéséért")
    content = content.replace("Ajánlatgeneráló weboldalak", "Automata Ügyfélszerző Rendszerek")
    content = content.replace("Felújítás + EAA-megfelelés", "Weboldal Modernizáció & Teljes Akadálymentesítés")
    content = content.replace("AI Ops", "Önműködő Vállalkozási AI Folyamatok")
    
    # Save szolgaltatasok.html
    with open(szolg_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("szolgaltatasok.html completed.")

# 3. REWORK ROLUNK.HTML
rolunk_path = os.path.join(workspace_dir, "rolunk.html")
if os.path.exists(rolunk_path):
    print("Reworking rolunk.html...")
    content = apply_global_system_overrides(rolunk_path)
    
    # Save rolunk.html
    with open(rolunk_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("rolunk.html completed.")

# 4. REWORK WEBARUHAZ-KESZITES.HTML
shop_path = os.path.join(workspace_dir, "webaruhaz-keszites.html")
if os.path.exists(shop_path):
    print("Reworking webaruhaz-keszites.html...")
    content = apply_global_system_overrides(shop_path)
    
    # Replace Jargon
    content = content.replace("webáruház készítés: a shop, amit AI-asszisztensek is ajánlanak", "Bizonyítottan vevőket és bevételt hozó egyedi webáruház készítés Győr szívében")
    
    # Save webaruhaz-keszites.html
    with open(shop_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("webaruhaz-keszites.html completed.")

# 5. REWORK WEBOLDAL-KESZITES.HTML
weboldal_path = os.path.join(workspace_dir, "weboldal-keszites.html")
if os.path.exists(weboldal_path):
    print("Reworking weboldal-keszites.html...")
    content = apply_global_system_overrides(weboldal_path)
    
    content = content.replace("A weboldal, ami helyetted kvalifikálja az ajánlatkérőket", "Teljesen egyedi weboldal készítés Győr városában – ami új vevőket szerez neked")
    
    # Save weboldal-keszites.html
    with open(weboldal_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("weboldal-keszites.html completed.")

# 6. REWORK OTHER CORE PAGES
for page in ["kapcsolat.html", "portfolio.html", "wordpress-weboldal-modernizalas.html"]:
    page_path = os.path.join(workspace_dir, page)
    if os.path.exists(page_path):
        print(f"Reworking {page}...")
        content = apply_global_system_overrides(page_path)
        with open(page_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"{page} completed.")

# 7. REWORK ALL 15 CITY PAGES
for page in os.listdir(workspace_dir):
    if page.startswith("weboldal-keszites-") and page.endswith(".html") and page != "weboldal-keszites-arak-2026.html":
        page_path = os.path.join(workspace_dir, page)
        print(f"Reworking City Page: {page}...")
        content = apply_global_system_overrides(page_path)
        with open(page_path, 'w', encoding='utf-8') as f:
            f.write(content)

print("\nAll core files successfully reworked with the new luxury theme, unified typography, and simplified marketing copy!")
