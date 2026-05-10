# Conen Digital Konfigurátor v2.0 — Implementation Spec

**Dokumentum-típus:** Cursor-feedable implementáció-spec — Claude Code lefuttat
**Szerző:** Claude — Project Lead, CTO & AI co-founder · Anthropic · CENTAUR-modell
**Status:** Draft 1, ready for execution
**Dátum:** 2026-05-10
**Codename:** `core-v2`
**Bemenet:** `centaur-project-handoff-v1_2.md`, `configurator-v2-master-architecture-sketch.md`, `weboldal-konfigurator.html` (685 sor)
**Kimenet:** új fájl `weboldal-konfigurator-v2.html`, single-file HTML+CSS+JS

---

## 0. Frame és ground rules

### 0.1 File-stratégia

A v2.0 **új fájlban** él, nem v1.x átírás. Két paralel-implementáció a launch napjáig.

- Új fájl: `weboldal-konfigurator-v2.html` a repo gyökerében.
- v1.x (`weboldal-konfigurator.html`) **változatlan** marad végig.
- Linkek a többi oldalról ideiglenesen v1.x-re mutatnak. Launch napján egy egyszeri swap.
- A v2.0 dev-URL: `conendigital.hu/weboldal-konfigurator-v2` (a Cloudflare Pages egyszerűen kiszolgálja, nincs dedikált setup).

### 0.2 Tech-stack döntések (locked)

- **Single HTML file** — HTML + `<style>` + `<script>` egyben, mint v1.x. Nincs build-step, nincs framework.
- **Vanilla JS**, ES2022+. Nincs React, nincs Vue, nincs framer-motion. Saját motion-lib (subset).
- **CSS Custom Properties** mindenre. Színek, motion-tokenek, layout, typography — egységesen `--token-name` formában.
- **View Transitions API** (Chrome/Edge/Safari) elsődleges; **FLIP fallback** Firefox-ra (kézzel írva).
- **Google Fonts** változatlan (Space Grotesk, JetBrains Mono, Inter, DM Sans, Playfair, Sora, Plus Jakarta).
- **Nincs külső CDN-libje** sem motion-re, sem state-re, sem semmire.

### 0.3 Browser-target

- Modern Chrome/Edge/Safari (last 2 major) — view-transitions ON
- Firefox (last 2) — FLIP fallback motion
- Reduced-motion → minden átmenet max 60ms cross-fade

### 0.4 Coding-konvenció

- 2-space indent, single quote (kivéve template literal), no trailing semicolons hiánya — egységes a v1.x-szel
- `S` global state object, `up()` állapot-szinkron-trigger, `render()` DOM-frissítés — v1.x-bevett mintázat folytatódik, csak strukturáltabban
- Comment-ek magyarul a szekció-fejléceken, angol a technikai részleteknél (consistent v1.x-szel)
- DOM-id és class konvenció:
  - State-bound element-ek: `id` rövid, mnemonic (pl. `pvFrame`, `cfgOl`)
  - Layout-class-ok: kebab-case (pl. `stage-frame`, `config-overlay`)
  - Modifier-class-ok: két-betűs rövidítés (pl. `.on`, `.fs`, `.mob`) — v1.x-konvenció

---

## 1. Master file-scaffold

### 1.1 Top-level HTML struktúra

```html
<!DOCTYPE html>
<html lang="hu">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
  <title>Vizuális weboldal konfigurátor v2 | Conen Digital</title>
  <meta name="description" content="A világ első sales-tool-ja, ami élő variant-compare-rel működik. Tervezd meg a weboldalad — két verzióban, egyszerre.">
  <link rel="canonical" href="https://conendigital.hu/weboldal-konfigurator-v2">
  <link rel="icon" href="favicon.ico">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500;600;700&family=Inter:wght@300;400;500;600;700&family=DM+Sans:wght@400;500;600;700&family=Playfair+Display:wght@400;600;700&family=Sora:wght@300;400;500;600;700&family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap" rel="stylesheet">
  <style>/* §2 CSS */</style>
</head>
<body>
  <div class="bg" aria-hidden="true"></div>
  <div class="app">
    <main class="stage" id="stage" role="main" aria-label="Weboldal-előnézet">
      <div class="device-frame" id="deviceFrame" data-device="desktop">
        <div class="preview-frame" id="pvPrimary" data-role="primary"></div>
        <div class="preview-frame" id="pvVariant" data-role="variant" hidden></div>
        <div class="variant-seam" id="variantSeam" hidden>
          <div class="seam-line"></div>
          <button class="seam-handle" aria-label="Húzd a verziók között">
            <svg viewBox="0 0 24 24" width="14" height="14" aria-hidden="true">
              <path d="M9 6L3 12l6 6M15 6l6 6-6 6" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
          </button>
        </div>
      </div>
      <div class="motion-layer" id="motionLayer" aria-hidden="true"></div>
    </main>

    <aside class="config-overlay" id="cfgOl" data-open="false" aria-label="Konfigurátor panel">
      <button class="cfg-pill" id="cfgPill" aria-expanded="false">
        <span class="cfg-pill-label">TERVEZD</span>
        <svg viewBox="0 0 24 24" width="14" height="14"><path d="M9 6l6 6-6 6" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>
      </button>
      <div class="cfg-panel" id="cfgPanel">
        <header class="cfg-header">
          <a href="index.html" class="logo">[<span>ConenDigital</span>]</a>
          <div class="cfg-step-pilot">
            <span class="step-count" id="sc">01/10</span>
          </div>
          <button class="cfg-close" id="cfgClose" aria-label="Panel bezárása">×</button>
        </header>
        <div class="cfg-content" id="cfgContent">
          <!-- §6: 10 step section, ported from v1.x with cleanup -->
        </div>
        <div class="cfg-preview-controls" id="cfgCtrls">
          <!-- §6.5: brand, tagline, cta, device, font-size, uploads -->
        </div>
      </div>
    </aside>

    <footer class="bottom-bar" id="btmBar">
      <div class="progress-track" id="pTrack"><div class="progress-fill" id="pFill"></div></div>
      <button class="btn btn-s" id="bPrev" disabled>← Vissza</button>
      <button class="btn btn-p" id="bNext" disabled>Tovább →</button>
      <button class="pill variant-toggle" id="vToggle" aria-pressed="false">
        <svg viewBox="0 0 24 24" width="12" height="12"><path d="M3 12h18M12 3v18" stroke="currentColor" stroke-width="2"/></svg>
        <span>Hasonlítsd össze A/B</span>
      </button>
      <button class="pill sound-toggle" id="sToggle" aria-pressed="false" title="Hangok">
        <svg viewBox="0 0 24 24" width="12" height="12"><path d="M3 9v6h4l5 4V5L7 9H3z" fill="currentColor"/></svg>
      </button>
      <div class="share-widget" id="shareW">
        <input type="text" id="shareUrl" readonly>
        <button class="pill" id="shareBtn">Másolás</button>
      </div>
    </footer>

    <div class="cinematic-intro" id="cIntro" hidden>
      <!-- §9: 3 másodperces önépítő szekvencia -->
    </div>

    <div class="toaster" id="toaster" role="status" aria-live="polite"></div>
  </div>
  <script>/* §3+§4+§5+§6+§7+§8+§9+§10 */</script>
</body>
</html>
```

### 1.2 ARIA / akadálymentesség alapok

A v1.2-handoff EAA-rétege ide is bejön. Minden interaktív elem:
- `role="button"` ha nem natív button
- `tabindex="0"` ha kell
- `aria-pressed` toggle-eken
- `aria-expanded` az overlay-pill-en
- `aria-label` ha az ikonon kívül nincs szöveg
- `aria-live="polite"` a toaster-en, `aria-live="off"` a stage-en (ne olvassa minden re-render-t)
- Skip-link a body első elemeként: `<a class="sr-skip" href="#cfgPanel">Ugrás a konfigurátorra</a>`
- Globális Enter/Space-handler minden `role="button"`-on

---

## 2. CSS architektúra

### 2.1 Custom property-fa (root)

```css
:root {
  /* Színek — base palette */
  --black: #0a0a0a;
  --white: #ffffff;
  --gray-50:  #f8f9fa;
  --gray-900: #1a1a1a;
  --gray-800: #2a2a2a;

  /* Színek — accent (8 témajelölt; runtime-ban átírható) */
  --accent:   #00f0ff;     /* default cyan */
  --accent-2: #bf00ff;     /* magenta (gradient-pair) */
  --orange:   #ff6b00;
  --green:    #00ff88;

  /* Színek — opacity-variants */
  --mid: rgba(255,255,255,.6);
  --dim: rgba(255,255,255,.4);
  --ghost: rgba(255,255,255,.04);
  --ghost-2: rgba(255,255,255,.08);

  /* Glass */
  --glass:  rgba(255,255,255,.03);
  --glass-2: rgba(255,255,255,.05);
  --glass-border: rgba(255,255,255,.08);

  /* Tipográfia */
  --font-main: 'Space Grotesk', sans-serif;
  --font-mono: 'JetBrains Mono', monospace;

  /* Layout */
  --stage-padding: 24px;
  --overlay-width: 400px;
  --overlay-pill-width: 48px;
  --bottom-bar-height: 56px;
  --device-frame-padding: 12px;

  /* Border-radii */
  --r-xs: 3px;
  --r-sm: 6px;
  --r-md: 10px;
  --r-lg: 16px;
  --r-xl: 24px;

  /* Z-index hierarchia */
  --z-stage: 1;
  --z-device: 5;
  --z-preview: 10;
  --z-seam: 20;
  --z-motion: 25;
  --z-config: 50;
  --z-bottom: 60;
  --z-toast: 100;
  --z-intro: 1000;

  /* Motion tokens */
  --t-fast: 180ms;
  --t-base: 280ms;
  --t-slow: 380ms;
  --t-slower: 520ms;
  --t-cinematic: 640ms;

  --e-out: cubic-bezier(0.4, 0, 0.1, 1);
  --e-in-out: cubic-bezier(0.25, 0.1, 0.3, 1);
  --e-back: cubic-bezier(0.34, 1.4, 0.64, 1);
  --e-in: cubic-bezier(0.4, 0, 1, 1);

  /* View Transitions API */
  --vt-color: 380ms ease-out;
  --vt-header: 520ms var(--e-out);
  --vt-hero: 640ms var(--e-in-out);
}

/* Reduced motion — globális override */
@media (prefers-reduced-motion: reduce) {
  :root {
    --t-fast: 60ms;
    --t-base: 60ms;
    --t-slow: 60ms;
    --t-slower: 60ms;
    --t-cinematic: 60ms;
  }
  * { animation-duration: 60ms !important; transition-duration: 60ms !important; }
  ::view-transition-group(*),
  ::view-transition-old(*),
  ::view-transition-new(*) { animation-duration: 60ms; }
}
```

### 2.2 Színvilág-tokenek (témánként)

A 10 színvilág `data-cs="..."` attribútumon a `<html>` elemen, és minden színváltozó dinamikusan átíródik. Minta:

```css
html[data-cs="dark-cyan"] {
  --bg: #0a0a0a;
  --fg: #ffffff;
  --accent: #00f0ff;
  --accent-2: #bf00ff;
  --is-light: 0;
}
html[data-cs="dark-mag"] {
  --bg: #0a0a0a; --fg: #ffffff;
  --accent: #bf00ff; --accent-2: #00f0ff;
  --is-light: 0;
}
html[data-cs="dark-orange"] {
  --bg: #0a0a0a; --fg: #ffffff;
  --accent: #ff6b00; --accent-2: #ffaa00;
  --is-light: 0;
}
html[data-cs="dark-green"] {
  --bg: #0a0a0a; --fg: #ffffff;
  --accent: #00ff88; --accent-2: #00ccff;
  --is-light: 0;
}
html[data-cs="light-blue"] {
  --bg: #f8f9fa; --fg: #0a0a0a;
  --accent: #2563eb; --accent-2: #7c3aed;
  --is-light: 1;
}
html[data-cs="light-emerald"] {
  --bg: #f8f9fa; --fg: #0a0a0a;
  --accent: #059669; --accent-2: #0891b2;
  --is-light: 1;
}
html[data-cs="light-warm"] {
  --bg: #faf8f5; --fg: #1c1917;
  --accent: #c2410c; --accent-2: #ca8a04;
  --is-light: 1;
}
html[data-cs="bold"] {
  --bg: #1e1b4b; --fg: #ffffff;
  --accent: #ec4899; --accent-2: #6366f1;
  --is-light: 0;
}
html[data-cs="earth"] {
  --bg: #292524; --fg: #f5f5f4;
  --accent: #a16207; --accent-2: #65a30d;
  --is-light: 0;
}
html[data-cs="mono"] {
  --bg: #09090b; --fg: #fafafa;
  --accent: #71717a; --accent-2: #a1a1aa;
  --is-light: 0;
}
```

A **`color-scheme:cross-fade`** átmenetet pontosan ez teszi lehetővé: a CSS-változók értékeinek átmenete (CSS-variable transition: a vars magukon nem animálnak, viszont az őket hivatkozó property-k igen, ha azokon van transition). Tehát:

```css
.preview-frame {
  background: var(--bg);
  color: var(--fg);
  transition: background var(--vt-color), color var(--vt-color);
}
.preview-frame * {
  transition: background-color var(--vt-color), color var(--vt-color), border-color var(--vt-color);
}
```

### 2.3 Reset és base

```css
* { margin:0; padding:0; box-sizing:border-box; }
html, body { height:100%; }
body {
  background: var(--black);
  color: var(--white);
  font-family: var(--font-main);
  overflow: hidden; /* Stage scroll-ol, body nem */
}
a { color: inherit; text-decoration: none; }
button { font-family: inherit; cursor: pointer; border: none; background: none; color: inherit; }
button:disabled { opacity: .4; cursor: not-allowed; }
::selection { background: var(--accent); color: var(--bg); }
::-webkit-scrollbar { width: 5px; height: 5px; }
::-webkit-scrollbar-thumb { background: rgba(255,255,255,.1); border-radius: 3px; }

/* Skip-link (akadálymentesség) */
.sr-skip {
  position: absolute; left: -10000px; top: auto;
  width: 1px; height: 1px; overflow: hidden;
}
.sr-skip:focus {
  left: 16px; top: 16px; width: auto; height: auto;
  padding: 8px 16px; background: var(--accent); color: var(--bg);
  border-radius: var(--r-sm); z-index: var(--z-toast);
}

/* Háttér grid */
.bg {
  position: fixed; inset: 0; pointer-events: none; z-index: 0;
  background-image:
    linear-gradient(rgba(0,240,255,.025) 1px, transparent 1px),
    linear-gradient(90deg, rgba(0,240,255,.025) 1px, transparent 1px);
  background-size: 60px 60px;
}
```

### 2.4 App-grid

```css
.app {
  position: relative;
  width: 100vw;
  height: 100dvh;
  z-index: var(--z-stage);
  display: grid;
  grid-template-rows: 1fr var(--bottom-bar-height);
  overflow: hidden;
}
```

A v1.x kétoszlopos grid eltűnik. Stage full-bleed, ConfigOverlay `position: fixed` rajta, BottomBar grid-row 2.

### 2.5 Stage és device-frame

```css
.stage {
  position: relative;
  grid-row: 1;
  overflow: hidden;
  background: radial-gradient(ellipse at top,
    rgba(0,240,255,.04), transparent 50%),
    var(--black);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: var(--stage-padding);
  z-index: var(--z-stage);
}

.device-frame {
  position: relative;
  width: 100%;
  height: 100%;
  max-width: 1400px;
  display: flex;
  z-index: var(--z-device);
  transition: max-width var(--t-slow) var(--e-in-out);
}
.device-frame[data-device="tablet"] { max-width: 840px; }
.device-frame[data-device="mobile"] { max-width: 390px; }

/* Bezel-rétegek (pszeudo-elemek SVG-frame-ből) */
.device-frame[data-device="mobile"]::before,
.device-frame[data-device="tablet"]::before {
  content: '';
  position: absolute; inset: 0;
  background-image: url("data:image/svg+xml;utf8,<svg ...>"); /* §5.2 */
  pointer-events: none;
  z-index: 2;
}
/* Desktop: subtle frame, no bezel */
.device-frame[data-device="desktop"] {
  border-radius: var(--r-md);
  box-shadow: 0 30px 60px rgba(0,0,0,.4), 0 0 0 1px rgba(255,255,255,.05);
  overflow: hidden;
}

.preview-frame {
  flex: 1;
  height: 100%;
  background: var(--bg);
  color: var(--fg);
  overflow: auto;
  position: relative;
  z-index: var(--z-preview);
  transition: background var(--vt-color), color var(--vt-color);
}
.preview-frame[data-role="variant"][hidden] { display: none; }
```

### 2.6 Variant-seam

```css
.variant-seam {
  position: absolute;
  top: 0;
  bottom: 0;
  left: 50%;
  transform: translateX(-50%);
  width: 32px;
  z-index: var(--z-seam);
  cursor: ew-resize;
  pointer-events: none; /* csak a handle-en aktív */
}
.variant-seam[hidden] { display: none; }
.seam-line {
  position: absolute; top: 0; bottom: 0; left: 50%;
  width: 1.5px;
  background: linear-gradient(180deg,
    transparent 0%,
    var(--accent) 15%,
    var(--accent-2) 85%,
    transparent 100%);
  transform: translateX(-50%);
  filter: drop-shadow(0 0 4px var(--accent));
}
.seam-handle {
  position: absolute;
  top: 50%; left: 50%;
  transform: translate(-50%, -50%);
  width: 36px; height: 36px;
  border-radius: 50%;
  background: var(--bg);
  border: 1.5px solid var(--accent);
  color: var(--accent);
  pointer-events: auto;
  display: flex; align-items: center; justify-content: center;
  box-shadow: 0 0 12px rgba(0,240,255,.4), 0 4px 12px rgba(0,0,0,.3);
  cursor: ew-resize;
  transition: transform var(--t-fast) var(--e-out), box-shadow var(--t-fast);
}
.seam-handle:hover { transform: translate(-50%, -50%) scale(1.08); }
.seam-handle:active { cursor: grabbing; }

/* Active-target indikátor */
.preview-frame[data-active="true"]::after {
  content: '';
  position: absolute; inset: 0;
  pointer-events: none;
  box-shadow: inset 0 0 0 2px var(--accent);
  opacity: .35;
  transition: opacity var(--t-fast);
}
```

A primary/variant clip-path-szal lesznek a seam pozíciójához igazítva, runtime-ban (lásd §8).

### 2.7 ConfigOverlay

```css
.config-overlay {
  position: fixed;
  top: 16px;
  right: 16px;
  bottom: calc(var(--bottom-bar-height) + 16px);
  width: var(--overlay-pill-width);
  z-index: var(--z-config);
  display: flex;
  transition: width var(--t-slower) var(--e-out);
}
.config-overlay[data-open="true"] {
  width: var(--overlay-width);
}

.cfg-pill {
  position: absolute;
  top: 50%; left: 0;
  transform: translateY(-50%);
  width: var(--overlay-pill-width);
  height: 120px;
  background: rgba(10,10,10,.88);
  backdrop-filter: blur(20px) saturate(180%);
  -webkit-backdrop-filter: blur(20px) saturate(180%);
  border: 1px solid var(--glass-border);
  border-radius: var(--r-md) 0 0 var(--r-md);
  display: flex; flex-direction: column;
  align-items: center; justify-content: center; gap: 8px;
  color: var(--accent);
  cursor: pointer;
  transition: opacity var(--t-base), transform var(--t-base);
}
.cfg-pill-label {
  writing-mode: vertical-rl;
  font-family: var(--font-mono);
  font-size: 11px;
  letter-spacing: .14em;
  text-transform: uppercase;
}
.config-overlay[data-open="true"] .cfg-pill {
  opacity: 0; pointer-events: none;
  transform: translateY(-50%) translateX(-8px);
}

.cfg-panel {
  flex: 1;
  background: rgba(10,10,10,.88);
  backdrop-filter: blur(20px) saturate(180%);
  -webkit-backdrop-filter: blur(20px) saturate(180%);
  border: 1px solid var(--glass-border);
  border-radius: var(--r-md);
  display: flex; flex-direction: column;
  overflow: hidden;
  opacity: 0;
  transform: translateX(20px);
  transition: opacity var(--t-base) var(--t-fast), transform var(--t-base) var(--t-fast);
}
.config-overlay[data-open="true"] .cfg-panel {
  opacity: 1; transform: translateX(0);
}

.cfg-header {
  padding: 12px 16px;
  display: flex; align-items: center; gap: 12px;
  border-bottom: 1px solid var(--glass-border);
}
.cfg-content {
  flex: 1; overflow-y: auto;
  padding: 20px;
}
.cfg-preview-controls {
  padding: 12px 16px;
  border-top: 1px solid var(--glass-border);
  display: flex; flex-wrap: wrap; gap: 8px; align-items: center;
}
```

### 2.8 BottomBar

```css
.bottom-bar {
  grid-row: 2;
  height: var(--bottom-bar-height);
  background: rgba(8,8,8,.92);
  backdrop-filter: blur(16px);
  -webkit-backdrop-filter: blur(16px);
  border-top: 1px solid var(--glass-border);
  display: flex; align-items: center; gap: 12px;
  padding: 0 16px;
  z-index: var(--z-bottom);
}
.progress-track {
  position: absolute; top: 0; left: 0; right: 0; height: 2px;
  background: rgba(255,255,255,.04);
}
.progress-fill {
  height: 100%;
  background: linear-gradient(90deg, var(--accent), var(--accent-2));
  width: 10%;
  transition: width var(--t-base) var(--e-out);
}

.btn {
  padding: 8px 14px;
  border: 1px solid;
  border-radius: var(--r-xs);
  font-family: var(--font-mono);
  font-size: 12px;
  font-weight: 500;
  display: inline-flex; align-items: center; gap: 6px;
  transition: all var(--t-fast);
}
.btn-p { background: var(--accent); color: var(--bg); border-color: var(--accent); }
.btn-p:hover:not(:disabled) {
  background: transparent; color: var(--accent);
  box-shadow: 0 0 16px rgba(0,240,255,.35);
}
.btn-s { background: transparent; color: var(--fg); border-color: var(--glass-border); }
.btn-s:hover:not(:disabled) { border-color: var(--fg); }

.pill {
  padding: 6px 12px;
  background: var(--glass);
  border: 1px solid var(--glass-border);
  border-radius: 100px;
  font-family: var(--font-mono);
  font-size: 11px;
  letter-spacing: .03em;
  display: inline-flex; align-items: center; gap: 6px;
  color: var(--mid);
  transition: all var(--t-fast);
}
.pill:hover { border-color: rgba(0,240,255,.3); color: var(--accent); }
.pill[aria-pressed="true"] {
  background: rgba(0,240,255,.08);
  border-color: var(--accent);
  color: var(--accent);
}

.share-widget {
  margin-left: auto;
  display: flex; align-items: center; gap: 6px;
}
.share-widget input {
  width: 200px; padding: 5px 8px;
  background: var(--glass); border: 1px solid var(--glass-border);
  border-radius: var(--r-xs); color: var(--accent);
  font-family: var(--font-mono); font-size: 10px;
}
```

### 2.9 Felelősségek a CSS-ben

- A **színvilág-átmenet** CSS custom property-átírással történik runtime-ban — JS csak a `<html data-cs="...">` attribútumot változtatja.
- A **header-style** és **hero-style** átmenetek a View Transitions API-n mennek, ami CSS `view-transition-name` annotációt igényel a render-output HTML-jén (ezt a renderer-fv. teszi hozzá; lásd §4).
- A **section reveal** átmenet egy CSS `@keyframes`-szel, JS csak `.revealing` osztályt ad-vesz.
- A **variant-seam drag** kizárólag JS — `clip-path` runtime-ban módosul a `pvPrimary` és `pvVariant` elemeken.

---

## 3. State-modell — implementáció

### 3.1 State-objektum

```js
const State = {
  site: {
    type: null,
    brand: '',
    tagline: '',
    cta: '',
    logo: null,
    hero_img: null,
    style: {
      color_scheme: 'dark-cyan',
      font_family: 'Space Grotesk',
      border_radius: 8,
      font_size: 100,
    },
    nav: {
      header_style: 'sticky',
      hero_style: 'centered',
    },
    pages: ['home', 'contact'],
    page_sections: { home: [], contact: [] },
    section_config: {},
    features: [],
    extras: [],
    content_state: null,
    timeline: null,
    industry: 'general',
  },

  variant: null,
  variant_active: false,
  variant_seam_pos: 0.5,
  variant_active_target: 'site',

  meta: {
    step: 1,
    active_page: 'home',
    device: 'desktop',
    config_overlay_open: false,
    realistic_mode: true,
    sound_enabled: false,
    motion_reduce: window.matchMedia('(prefers-reduced-motion: reduce)').matches,
    intro_seen: false,
  },

  scores: { eaa: 0, ax: 0, centaur: 20 },
};
```

### 3.2 Persistence

```js
const STORAGE_KEY = 'core_v2_state';

function save() {
  try {
    // Strip image-data (logo, hero_img) — túl nagy a localStorage-ba
    const clone = JSON.parse(JSON.stringify(State));
    if (clone.site.logo) clone.site.logo = '__has__';
    if (clone.site.hero_img) clone.site.hero_img = '__has__';
    if (clone.variant?.logo) clone.variant.logo = '__has__';
    if (clone.variant?.hero_img) clone.variant.hero_img = '__has__';
    localStorage.setItem(STORAGE_KEY, JSON.stringify(clone));
  } catch (e) { /* quota or private-mode; ignore */ }
}

function load() {
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    if (!raw) return;
    const parsed = JSON.parse(raw);
    // Image-data nem helyreállítható; a flag csak vizuális indikátor
    if (parsed.site?.logo === '__has__') parsed.site.logo = null;
    if (parsed.site?.hero_img === '__has__') parsed.site.hero_img = null;
    Object.assign(State, parsed);
    State.meta.config_overlay_open = false; // mindig zárva indul
  } catch (e) { /* corrupt; ignore */ }
}
```

### 3.3 Mutáció és sync

A v1.x `up()` minta strukturált változata:

```js
// State mutation entry-point. Minden change ezen megy keresztül.
function commit(changeFn, opts = {}) {
  const target = State.variant_active && State.variant_active_target === 'variant'
    ? State.variant
    : State.site;

  // Capture pre-state for view-transitions diff
  const pre = opts.transition ? snapshot(target) : null;

  changeFn(target);

  // Schedule render
  if (opts.transition && supportsViewTransitions()) {
    document.startViewTransition(() => {
      render();
      updateUIControls();
    });
  } else {
    render();
    updateUIControls();
  }

  save();
}

function snapshot(t) { return JSON.parse(JSON.stringify(t)); }
function supportsViewTransitions() {
  return typeof document.startViewTransition === 'function';
}
```

A `commit()` az egyetlen mutáció-belépési pont. Minden choice-callback `commit(s => s.style.color_scheme = 'dark-mag', { transition: true })` formában megy.

### 3.4 Core rendering signal

```js
function render() {
  // 1. Update HTML attribútumok (color-scheme, device)
  document.documentElement.dataset.cs = active().style.color_scheme;
  document.getElementById('deviceFrame').dataset.device = State.meta.device;

  // 2. Render preview-frame(s)
  renderPreview('pvPrimary', State.site);
  if (State.variant_active) {
    renderPreview('pvVariant', State.variant);
    document.getElementById('pvVariant').hidden = false;
    document.getElementById('variantSeam').hidden = false;
    applySeamClip();
  } else {
    document.getElementById('pvVariant').hidden = true;
    document.getElementById('variantSeam').hidden = true;
    clearSeamClip();
  }

  // 3. Update active-target visual indicator
  updateActiveIndicator();
}

function active() {
  return State.variant_active && State.variant_active_target === 'variant'
    ? State.variant : State.site;
}
```

---

## 4. Rendering pipeline

### 4.1 PreviewFrame contract

```js
function renderPreview(elementId, site) {
  const el = document.getElementById(elementId);
  if (!site || !site.type) {
    el.innerHTML = renderEmptyState();
    return;
  }

  // Apply font-family at the frame level (cascades to all content)
  el.style.fontFamily = `'${site.style.font_family}', sans-serif`;
  el.style.fontSize = (site.style.font_size / 100) + 'rem';

  let html = '';
  html += renderHeader(site);
  html += renderActivePage(site);
  html += renderFooter(site);
  el.innerHTML = html;
}

function renderEmptyState() {
  return `
    <div style="height:100%;display:flex;flex-direction:column;
                align-items:center;justify-content:center;
                color:var(--mid);font-family:var(--font-mono);font-size:13px;
                gap:12px;text-align:center;padding:32px">
      <div style="font-size:40px">↗</div>
      <div>Válaszd ki a típust a panelben</div>
      <div style="opacity:.5;font-size:11px">A preview itt él, közvetlenül</div>
    </div>`;
}
```

### 4.2 Renderer-függvények — port v1.x-ből

A v1.x `renderHero()`, `renderSection()`, `renderHeader()` logikákat **változatlanul portoljuk**, két módosítással:

**A) View-transition névadás** — minden major-block kap egy `view-transition-name` style-attribútumot:

```js
function renderHeader(site) {
  return `<div style="view-transition-name:vt-header"
                ...rest of header markup...></div>`;
}
function renderHero(site) {
  return `<div style="view-transition-name:vt-hero"
                ...rest of hero markup...></div>`;
}
```

A View Transitions API automatikusan animálja az azonos nevű elemek közötti morfingot. Ha `header_style` változik, a régi `vt-header` kimorf a régi pozícióból, az új `vt-header` bemorf az új pozícióba — 520ms-en keresztül, a CSS-ben definiált `--vt-header` easing-gel.

**B) REALISTIC content alapból** — a v1.x placeholder-ek (`Csapattag 1`, `Projekt #2`) eltűnnek; alapból REALISTIC fut. Lásd §13.

### 4.3 Per-section render — bővítések

A v1.x section-render minden esete portolódik. A `gallery`, `pricing`, `team`, `testimonials`, `partners`, `faq`, `map`, `cta`, `newsletter`, `stats`, `process` mind ugyanazzal a config-pattern-nel működik. Plusz módosítások:

- **`section:reveal`** osztály: amikor egy szekció új (újonnan a `page_sections`-ben), a renderer az adott szekciónak `class="section-revealing"` ad. CSS `@keyframes` 320ms staggered-fadek-be lép. Az osztály 360ms után önműködően lehullik (CSS `animation-fill-mode: forwards` + JS-cleanup).

- **Iparág-specifikus REALISTIC**: a v1.2-handoffból az `INDUSTRY_OVERRIDES` objektum portolódik (b2b-service / ecommerce / professional / creative). Ha `site.industry !== 'general'`, az adott iparág override-olja a default REALISTIC-tartalmakat.

### 4.4 Hover-preview transient mechanika

```js
// §6 step 2: font hover
document.addEventListener('mouseover', (e) => {
  const fc = e.target.closest('.font-card');
  if (!fc) return;
  const font = fc.dataset.v;
  startTransient(() => {
    document.getElementById('pvPrimary').style.fontFamily = `'${font}', sans-serif`;
  });
});
document.addEventListener('mouseout', (e) => {
  const fc = e.target.closest('.font-card');
  if (!fc) return;
  endTransient(() => {
    const f = State.site.style.font_family;
    document.getElementById('pvPrimary').style.fontFamily = `'${f}', sans-serif`;
  });
});

let transientTimer = null;
function startTransient(fn) {
  clearTimeout(transientTimer);
  fn();
}
function endTransient(fn) {
  transientTimer = setTimeout(fn, 200);
}
```

Színvilág-hover ugyanígy, a `dataset.cs` runtime-átírásával.

---

## 5. Stage és DeviceFrame

### 5.1 Layout-számítás

A Stage full-bleed; a DeviceFrame `max-width`-tel skálázódik (desktop: 1400px, tablet: 840px, mobile: 390px). Center-elés flex-bel.

### 5.2 Bezel-SVG-k

Három inline SVG bezel (data-URI-ként a `::before` pszeudo-elemen). A teljes asset-ek terjedelme ~20-30KB inline. Forrás (vázlat):

**iPhone 16 Pro keret** (mobile):
- 390×844 base
- 8px körüli bezel
- Notch / Dynamic Island fent középen (pill, 120×30, 4px-rel a tetőtől)
- Home-indikátor lent középen (140×4, 8px-rel az aljtól)
- Border-radius: 50px

**iPad Air** (tablet):
- 820×1100 base (méretarány)
- 16px-es bezel
- Camera-pötty fent középen
- Border-radius: 22px

**MacBook 14"-mockup** (desktop): nincs külön bezel, csak a `device-frame[data-device="desktop"]` shadow + border-radius.

A bezel-SVG-k a fájl `<defs>` szekciójában léteznek és a `::before` background-image-en hivatkozottak, hogy CSS-szerkezetből cserélődjenek device-váltáskor.

```css
.device-frame[data-device="mobile"] {
  border-radius: 50px;
  padding: 12px;
  background: #1a1a1a;
  box-shadow: 0 0 0 1.5px #2a2a2a, 0 30px 60px rgba(0,0,0,.5);
  width: 390px; height: 844px;
  max-height: calc(100dvh - 120px);
}
.device-frame[data-device="mobile"] .preview-frame {
  border-radius: 38px;
  overflow: hidden;
}
.device-frame[data-device="mobile"]::after {
  /* Dynamic Island */
  content: '';
  position: absolute; top: 18px; left: 50%; transform: translateX(-50%);
  width: 120px; height: 32px; border-radius: 100px;
  background: #000;
  z-index: 3;
}
```

(Részletes bezel-SVG asset-eket az implementáció során finomítjuk; ez a vázlat elég ahhoz, hogy a struktúra megálljon.)

### 5.3 Device-toggle

```js
document.querySelectorAll('[data-dev]').forEach(b => {
  b.addEventListener('click', () => {
    const old = State.meta.device;
    if (old === b.dataset.dev) return;
    document.querySelectorAll('[data-dev]').forEach(x => x.classList.remove('act'));
    b.classList.add('act');
    commit(s => {}, { transition: true }); // trigger re-render with VT
    State.meta.device = b.dataset.dev;
    document.getElementById('deviceFrame').dataset.device = b.dataset.dev;
  });
});
```

A device-frame-csere 480ms-os ease-in-out átmenettel megy (a `max-width` és bezel-SVG fade).

---

## 6. ConfigOverlay — step-tartalmak

### 6.1 Open / close

```js
const cfgOl = document.getElementById('cfgOl');
const cfgPill = document.getElementById('cfgPill');
const cfgClose = document.getElementById('cfgClose');

function setOverlay(open) {
  State.meta.config_overlay_open = open;
  cfgOl.dataset.open = String(open);
  cfgPill.setAttribute('aria-expanded', String(open));
  save();
}
cfgPill.addEventListener('click', () => setOverlay(true));
cfgClose.addEventListener('click', () => setOverlay(false));

// ESC zárja, ha nincs intro
document.addEventListener('keydown', (e) => {
  if (e.key === 'Escape' && State.meta.config_overlay_open) setOverlay(false);
});
```

### 6.2 Step-content struktúra

A 10 step ugyanaz, mint v1.x-ben. Új építkezés:

- Lépésenkénti `<section class="step" data-s="N">` egységek
- A v1.x `.cfg` container helyett a `.cfg-content` div
- Card-grid-ek (`.g`, `.tl`, `.colors`, `.fonts`) változatlanok osztály-szerkezetben — CSS-konvenció megmarad
- Step 6 (per-page sections) kapcsolata változatlan: `buildPageUI()` hívás step-be lépéskor

A teljes step-tartalom egy az egyben portolódik a v1.x 172-289. sorából (HTML), kisebb módosításokkal (lásd §6.3).

### 6.3 Module-szintű módosítások v1.x → v2.0 step-tartalmakon

- **Step 1 (TÍPUS)**: minden választás `commit(s => s.type = ..., { transition: true })`. Plusz: típus-választás után automatikusan beáll a hozzá tartozó default `pages`, `page_sections`, és iparág (ha van mapping).
- **Step 2 (STÍLUS)**: hover-preview hozzáadása fontokhoz és színekhez (§4.4).
- **Step 3 (NAVIGÁCIÓ)**: változatlan v1.x szerkezetileg; csak a `commit()` wrapper új.
- **Step 4 (HERO)**: ugyanaz.
- **Step 5 (OLDALAK)**: ugyanaz.
- **Step 6 (SZEKCIÓK)**: a `buildPageUI()` újraírva, hogy minden pill-click `commit()`-on menjen.
- **Step 7 (FUNKCIÓK)**: a v1.2-tervezett feature-default-okat alkalmazza típus-szerint (csak ha `features` még üres).
- **Step 8 (EXTRÁK)**: ugyanaz.
- **Step 9 (RÉSZLETEK)**: tartalom, időzítés.
- **Step 10 (EREDMÉNY)**: scope-summary, scoring (3-axis), pricing, vanity-URL, scope-küldés form (Formspree változatlan).

### 6.4 PreviewControls (cfg-preview-controls)

A v1.x `pv-inputs` és `pv-uploads` rétege bekerül ide, a panel aljára:

```html
<div class="cfg-preview-controls">
  <input type="text" id="iBrand" placeholder="Cégnév" maxlength="30">
  <input type="text" id="iTag" placeholder="Szlogen" maxlength="60">
  <input type="text" id="iCta" placeholder="CTA" maxlength="20">
  <div class="ctrl-row">
    <button data-dev="desktop" class="pill act">D</button>
    <button data-dev="tablet" class="pill">T</button>
    <button data-dev="mobile" class="pill">M</button>
  </div>
  <div class="ctrl-row">
    <input type="range" id="fsSlider" min="70" max="140" value="100" step="5">
    <span id="fsVal">100%</span>
  </div>
  <div class="ctrl-row">
    <label class="upl" id="uLogo">Logó <input type="file" accept="image/*" hidden></label>
    <label class="upl" id="uHero">Hero kép <input type="file" accept="image/*" hidden></label>
  </div>
</div>
```

Logo-szín-extraction (v1.2-tervből) ide bejön: canvas-os 32×32 resampling, near-fehér/fekete bucket-skip, euklidészi távolság a 10 színvilág-jelölthöz. Eredmény-csip a logó alá, "Alkalmazás →" CTA-val.

---

## 7. MotionLayer — Cinematic continuity

### 7.1 View Transitions API setup

```js
function applyViewTransition(name, fn) {
  if (supportsViewTransitions() && !State.meta.motion_reduce) {
    document.documentElement.style.setProperty('--vt-active', name);
    document.startViewTransition(fn);
  } else {
    fn();
  }
}
```

```css
/* §2.2 már definiálta a transition-vars-okat */
::view-transition-group(vt-header) {
  animation-duration: 520ms;
  animation-timing-function: cubic-bezier(0.4, 0, 0.1, 1);
}
::view-transition-group(vt-hero) {
  animation-duration: 640ms;
  animation-timing-function: cubic-bezier(0.25, 0.1, 0.3, 1);
}
::view-transition-group(*) {
  animation-duration: 380ms;
  animation-timing-function: ease-out;
}
```

### 7.2 Section reveal

```css
.section-revealing {
  animation: section-reveal 320ms cubic-bezier(0.34, 1.4, 0.64, 1) forwards;
}
@keyframes section-reveal {
  from { opacity: 0; transform: translateY(12px) scale(0.96); }
  to   { opacity: 1; transform: translateY(0) scale(1); }
}
```

```js
function markNewSections(prevPageSections, newPageSections) {
  // Compare arrays; on next render, add .section-revealing to additions
  const newOnes = newPageSections.filter(s => !prevPageSections.includes(s));
  // Stagger: each new section gets animation-delay
  setTimeout(() => {
    newOnes.forEach((sid, i) => {
      const el = document.querySelector(`[data-section="${sid}"]`);
      if (el) {
        el.classList.add('section-revealing');
        el.style.animationDelay = (i * 60) + 'ms';
        setTimeout(() => el.classList.remove('section-revealing'), 320 + i * 60 + 50);
      }
    });
  }, 16); // wait for next frame
}
```

### 7.3 Step transition

A step-váltás csak az overlay-tartalmat animálja (a Stage-en mindig az aktuális site látszik).

```css
.step { display: none; }
.step.on {
  display: block;
  animation: step-in 280ms ease-out;
}
@keyframes step-in {
  from { opacity: 0; transform: translateY(8px); }
  to   { opacity: 1; transform: translateY(0); }
}
```

### 7.4 FLIP-fallback (Firefox stb.)

Ha `supportsViewTransitions()` false, manuális FLIP a header és hero átmenetekre. Egyelőre **nem implementáljuk a FLIP-réteget MVP-ben** — Firefox-on a transition-ök egyszerűen "snap"-pelnek (acceptable degradation). v2.1-re tervezett.

### 7.5 Reduced motion

A `:root` szintű override (lásd §2.1) az összes transition és animation duration-t levágja 60ms-ra. A View Transitions API is ennek megfelelően gyors. Ez globális, JS nem szükséges.

---

## 8. Variant-Compare implementáció

### 8.1 Toggle on/off

```js
const vToggle = document.getElementById('vToggle');
vToggle.addEventListener('click', () => {
  if (State.variant_active) closeVariant();
  else openVariant();
});

function openVariant() {
  State.variant = JSON.parse(JSON.stringify(State.site));
  State.variant_active = true;
  State.variant_seam_pos = 0.5;
  State.variant_active_target = 'variant'; // új choice-ok az új oldalra
  vToggle.setAttribute('aria-pressed', 'true');
  applyViewTransition('variant-open', () => render());
  toast('Variant-mode bekapcsolva. A választásaid a jobb oldalra mennek.');
}

function closeVariant() {
  State.variant_active = false;
  State.variant_active_target = 'site';
  vToggle.setAttribute('aria-pressed', 'false');
  applyViewTransition('variant-close', () => {
    render();
    State.variant = null; // csak render után törlünk
    save();
  });
}
```

### 8.2 Seam-drag

```js
const seam = document.getElementById('variantSeam');
const handle = seam.querySelector('.seam-handle');
let dragging = false;

handle.addEventListener('mousedown', startDrag);
handle.addEventListener('touchstart', startDrag, { passive: false });

function startDrag(e) {
  e.preventDefault();
  dragging = true;
  document.body.style.userSelect = 'none';
  document.body.style.cursor = 'ew-resize';
}

function moveDrag(e) {
  if (!dragging) return;
  const x = e.touches ? e.touches[0].clientX : e.clientX;
  const frame = document.getElementById('deviceFrame').getBoundingClientRect();
  const pos = Math.max(0.05, Math.min(0.95, (x - frame.left) / frame.width));
  State.variant_seam_pos = pos;
  applySeamClip();
}

function endDrag() {
  if (!dragging) return;
  dragging = false;
  document.body.style.userSelect = '';
  document.body.style.cursor = '';
  save();
}

document.addEventListener('mousemove', moveDrag);
document.addEventListener('touchmove', moveDrag, { passive: false });
document.addEventListener('mouseup', endDrag);
document.addEventListener('touchend', endDrag);

function applySeamClip() {
  const pos = State.variant_seam_pos;
  const pvP = document.getElementById('pvPrimary');
  const pvV = document.getElementById('pvVariant');
  pvP.style.clipPath = `polygon(0 0, ${pos * 100}% 0, ${pos * 100}% 100%, 0 100%)`;
  pvV.style.clipPath = `polygon(${pos * 100}% 0, 100% 0, 100% 100%, ${pos * 100}% 100%)`;
  seam.style.left = (pos * 100) + '%';
}

function clearSeamClip() {
  const pvP = document.getElementById('pvPrimary');
  pvP.style.clipPath = '';
}
```

A clip-path mindkét frame-en él, és az átfedés-mentes két-oldalas megjelenítést adja. Mindkét frame teljes méretben renderel a háttérben — csak a clip vágja le.

### 8.3 Active-target-váltás

```js
[document.getElementById('pvPrimary'), document.getElementById('pvVariant')].forEach(el => {
  el.addEventListener('click', (e) => {
    if (!State.variant_active) return;
    if (e.target.closest('.seam-handle')) return;
    const target = el.dataset.role === 'primary' ? 'site' : 'variant';
    if (State.variant_active_target !== target) {
      State.variant_active_target = target;
      updateActiveIndicator();
      toast(target === 'site' ? 'Bal oldal aktív' : 'Jobb oldal aktív');
    }
  });
});

function updateActiveIndicator() {
  const pvP = document.getElementById('pvPrimary');
  const pvV = document.getElementById('pvVariant');
  if (State.variant_active) {
    pvP.dataset.active = String(State.variant_active_target === 'site');
    pvV.dataset.active = String(State.variant_active_target === 'variant');
  } else {
    pvP.dataset.active = 'false';
    pvV.dataset.active = 'false';
  }
}
```

### 8.4 Swap

A seam-handle-en egy második (kis) ikon — `⇄` swap-ikon. Klikkre:

```js
function swapVariants() {
  const tmp = State.site;
  State.site = State.variant;
  State.variant = tmp;
  applyViewTransition('variant-swap', () => render());
  toast('A két verzió helyet cserélt');
}
```

### 8.5 Resolve a Step 10-en

A Step 10 eredmény-felületen, ha `variant_active`:

```html
<div class="rb">
  <div class="rl">// VARIANT FEL</div>
  <p>Két verzió van készen. Melyiket szeretnéd a diagnosztikára vinni?</p>
  <div class="resolve-grid">
    <button class="btn btn-s" data-resolve="site">Bal (A)</button>
    <button class="btn btn-s" data-resolve="variant">Jobb (B)</button>
    <button class="btn btn-p" data-resolve="both">Mindkettőt</button>
  </div>
</div>
```

A "Mindkettőt" választás a Formspree-form payload-jába mindkét scope-ot beleteszi (`scope_a` és `scope_b` mezőkbe).

---

## 9. Cinematic Intro

### 9.1 Sequence

Single one-shot animáció, ~3 másodperc:

- **0-300ms**: fekete fade-be → middle-text "Egy CENTAUR-tool. Ember + két MI co-founder." monospace, fade-in
- **300-1200ms**: a stage-en wireframe-dobozok megjelennek (header skeleton, hero skeleton, 3 section skeleton) — staggered fadek-in
- **1200-1900ms**: szín befolyik (CSS custom property animation: a wireframe `outline: 1px dashed rgba(255,255,255,.1)` → kitölt `var(--accent)15` háttér)
- **1900-2400ms**: tipográfia "rendeződik" — szöveg-placeholder vonalakból konkrét szövegek lesznek (cross-fade)
- **2400-3000ms**: kész hero-szekció megjelenik, az overlay-szöveg cserélődik: "Most a tied. Tervezd meg." + "Kezdés →" gomb

```js
function playIntro() {
  if (State.meta.intro_seen) return;
  const el = document.getElementById('cIntro');
  el.hidden = false;
  // SVG-kompatibilis sequence, runtime-ban orchestrálva
  el.innerHTML = `
    <div class="intro-stage" data-phase="0">
      <div class="intro-text" id="introText">Egy CENTAUR-tool. Ember + két MI co-founder.</div>
      <div class="intro-mockup">
        <div class="m-line m-header"></div>
        <div class="m-line m-hero"></div>
        <div class="m-line m-section-1"></div>
        <div class="m-line m-section-2"></div>
        <div class="m-line m-section-3"></div>
      </div>
      <div class="intro-cta" hidden>
        <div>Most a tied. Tervezd meg.</div>
        <button id="introStart" class="btn btn-p">Kezdés →</button>
      </div>
      <button class="intro-skip" id="introSkip">Kihagyom</button>
    </div>`;

  setTimeout(() => el.querySelector('.intro-stage').dataset.phase = '1', 300);
  setTimeout(() => el.querySelector('.intro-stage').dataset.phase = '2', 1200);
  setTimeout(() => el.querySelector('.intro-stage').dataset.phase = '3', 1900);
  setTimeout(() => {
    el.querySelector('.intro-stage').dataset.phase = '4';
    el.querySelector('.intro-cta').hidden = false;
  }, 2400);

  document.getElementById('introStart')?.addEventListener('click', endIntro);
  document.getElementById('introSkip').addEventListener('click', endIntro);
  document.addEventListener('keydown', escIntro, { once: true });
}

function escIntro(e) { if (e.key === 'Escape') endIntro(); }

function endIntro() {
  const el = document.getElementById('cIntro');
  el.style.opacity = '0';
  setTimeout(() => {
    el.hidden = true;
    el.style.opacity = '';
  }, 420);
  State.meta.intro_seen = true;
  save();
  setOverlay(true); // intro után a config nyíljon ki, vendég benne van
}
```

CSS phase-attribútumokra (`[data-phase="0"]` ... `[data-phase="4"]`) skeleton-ok progresszív megjelenése.

### 9.2 Skip-mechanikák

- ESC kulcs
- "Kihagyom" gomb
- Klikk az overlay-háttérre

### 9.3 LocalStorage flag

`core_v2_intro_seen`. Frissítés akkor, amikor `endIntro()` lefut. Friss-start törli a teljes state-tel együtt.

---

## 10. Vanity-URL slug-generátor

### 10.1 Magyar szótár

Három szavas szótár, 200 elem összesen (~70-70-60), egyszótagos vagy kétszótagos magyar szavak (CC0/saját). Vázlat (kategória → szó-példák):

- **Természet** (~70): csillag, ablak, erdő, folyó, hegy, tó, tenger, virág, fa, kő, szél, eső, hó, nap, hold, ég, sziget, völgy, mező...
- **Tárgy / hely** (~70): híd, ház, kert, út, kapu, torony, tér, sarok, kút, lépcső, kilátó, ösvény, padló, mennyezet...
- **Irány / minőség** (~60): déli, északi, mély, magas, lassú, friss, csendes, élénk, tiszta, sötét, fényes, halk, finom...

Final slug: `<kat-1>-<kat-2>-<kat-3>` (pl. `csillag-ablak-deli`).

### 10.2 Generátor

```js
const SLUG_NATURE = ['csillag','ablak','erdo','folyo','hegy','to','tenger','virag','fa','ko','szel','eso','ho','nap','hold','eg','sziget','volgy','mezo',/*...*/];
const SLUG_PLACE  = ['hid','haz','kert','ut','kapu','torony','ter','sarok','kut','lepcso','kilato','osveny','padlo','tetove',/*...*/];
const SLUG_QUAL   = ['deli','eszaki','mely','magas','lassu','friss','csendes','elenk','tiszta','sotet','fenyes','halk','finom',/*...*/];

function pickSlug() {
  const n = SLUG_NATURE[Math.floor(Math.random() * SLUG_NATURE.length)];
  const p = SLUG_PLACE[Math.floor(Math.random() * SLUG_PLACE.length)];
  const q = SLUG_QUAL[Math.floor(Math.random() * SLUG_QUAL.length)];
  return `${n}-${p}-${q}`;
}

function buildVanityUrl() {
  const slug = pickSlug();
  // MVP: client-only, slug a query-paramban
  const state = encodeStateMinimal(State.site);
  return `${location.origin}/cfg/${slug}?s=${btoa(state)}`;
}
```

### 10.3 Backend persistence (v2.1)

A v2.0-ban a slug csak vizuális — a state a query-paramban utazik (mint v1.x share-URL). A slug **memorability**-ért van. v2.1-ben a `chat.conendigital.hu` Worker kibővül egy `/cfg-store` endpointtal (Cloudflare KV), ami a slug → state mapping-et 30 napig tárolja.

---

## 11. Three-axis scoring panel

### 11.1 Formulák

```js
function computeScores(site) {
  // EAA: akadálymentesség
  let eaa = 30; // baseline (a tool maga is EAA-konform)
  if (site.features.includes('eaa')) eaa += 35;
  if (site.extras.includes('ax-ready')) eaa += 10;
  if (site.features.includes('multilang')) eaa += 8;
  if (site.extras.includes('perf')) eaa += 7;
  if (site.style.font_size >= 90) eaa += 10;
  eaa = Math.min(eaa, 100);

  // AX: AI-experience
  let ax = 15;
  if (site.extras.includes('ax-ready')) ax += 30;
  if (site.extras.includes('mcp')) ax += 25;
  if (site.extras.includes('ai-chat')) ax += 20;
  if (site.features.includes('search')) ax += 5;
  if (site.features.includes('analytics')) ax += 5;
  ax = Math.min(ax, 100);

  // CENTAUR-readiness: AI-ready scope mint sales-tool
  let cn = 20; // baseline
  if (site.type === 'quote-engine') cn += 20;
  if (site.extras.includes('mcp')) cn += 25;
  if (site.extras.includes('ai-chat')) cn += 20;
  if (site.features.includes('analytics')) cn += 10;
  if (site.features.includes('multilang')) cn += 5;
  if (site.extras.includes('ax-ready')) cn += 10;
  cn = Math.min(cn, 100);

  return { eaa, ax, centaur: cn };
}
```

### 11.2 Vizuális komponens

A Step 10-en három animált progress-bar:

```html
<div class="score-panel">
  <div class="score-row">
    <span class="score-l">EAA</span>
    <div class="score-bar"><div class="score-fill" data-score="eaa"></div></div>
    <span class="score-v" id="scEAA">0</span>
  </div>
  <div class="score-row">
    <span class="score-l">AX</span>
    <div class="score-bar"><div class="score-fill" data-score="ax"></div></div>
    <span class="score-v" id="scAX">0</span>
  </div>
  <div class="score-row">
    <span class="score-l">CENTAUR</span>
    <div class="score-bar"><div class="score-fill score-centaur" data-score="centaur"></div></div>
    <span class="score-v" id="scCN">0</span>
  </div>
  <div class="score-tip" id="scTip"></div>
</div>
```

```css
.score-bar { flex: 1; height: 4px; background: var(--ghost); border-radius: 2px; overflow: hidden; }
.score-fill { height: 100%; background: var(--accent); width: 0; transition: width 800ms var(--e-out); }
.score-fill.score-centaur {
  background: linear-gradient(90deg, var(--accent), var(--accent-2));
}
```

Tip-mondatok dinamikusak: ha CENTAUR < 60: "A CENTAUR-readiness emelhető: vegyél fel MCP-endpointot vagy AI-chatet — ez a #service-ai-ops pillér terméke."

---

## 12. REALISTIC content + iparág-specifikus

### 12.1 Default REALISTIC

A `realistic_mode: true` alapértelmezett. Csak akkor kapcsolható ki ("wireframe-mode"-ra), ha a látogató direkt ezt akarja.

```js
const REALISTIC_DEFAULTS = {
  testimonials: [
    { q: 'A diagnosztika 30 perc volt, és pontosan tudtuk, mit kapunk. Nincs apróbetűs.', n: 'Kovács Anna', t: 'Marketing-vezető' },
    { q: 'A scope-ot délben küldtük el, este már volt visszahívás-időpontunk.', n: 'Nagy Péter', t: 'Ügyvezető' },
    { q: 'A kapott weboldal AX-ready volt — másfél évvel a versenytársaink előtt.', n: 'Tóth Eszter', t: 'CMO' },
    { q: 'EAA-konform, és nem érződött kompromisszumnak. Tényleg jól néz ki.', n: 'Szabó Gábor', t: 'CEO' },
  ],
  team: [
    { n: 'Conen Krisztián', r: 'Founder' },
    { n: 'Claude', r: 'Co-founder · CTO · Anthropic' },
    { n: 'Gemini Nexus', r: 'Co-founder · Marketing' },
  ],
  // ... gallery, faq stb.
};
```

A team-szekció REALISTIC-rendere a CENTAUR-self-reference-et adja (Conen + Claude + Gemini Nexus). Ez egy explicit credibility-elem: a látogató ránézésre érzi, hogy ez nem egy hagyományos ügynökség.

### 12.2 Iparág-override

```js
const INDUSTRY_OVERRIDES = {
  'b2b-service': {
    testimonials: [/* B2B-specifikus, "ROI 6 hónapon belül" */],
    gallery: [/* B2B munkák */],
    faq: [/* "Hogyan integrálódunk a CRM-mel?" stb */],
  },
  ecommerce: {
    testimonials: [/* "Konverzió +40%" */],
    gallery: [/* termékfotók */],
    faq: [/* "Headless Shopify vagy WooCommerce?" */],
  },
  professional: {
    testimonials: [/* "Ügyvédi ügyfél-portál + dokumentum-archív" */],
    gallery: [/* ügyfél-portál mockupok */],
    faq: [/* "Adatvédelem (ügyvédi titok)?" */],
  },
  creative: {
    testimonials: [/* "Egyedi tipográfia és art-direction" */],
    gallery: [/* kreatív munkák */],
    faq: [/* "Milyen tipográfiai licenc kell?" */],
  },
};

function getRealisticContent(site, sectionType) {
  const ind = site.industry || 'general';
  if (ind !== 'general' && INDUSTRY_OVERRIDES[ind]?.[sectionType]) {
    return INDUSTRY_OVERRIDES[ind][sectionType];
  }
  return REALISTIC_DEFAULTS[sectionType] || [];
}
```

### 12.3 Iparág-választó (Step 0 vagy Step 1 utáni mini-pill)

A v2.0-ban egy mini-pill az RD-toggle helyett: `B2B / E-COM / PROF / KREAT / ÁLT.`. Megjelenése Step 1 (típus) választás után. A Step 1 választás egyébként default iparágat is beállíthat (pl. `webshop` → `ecommerce`).

---

## 13. CTO attribúció

Három helyen, v1.2-tervből portolva:

1. **Cinematic intro**: a középső szöveg "Egy CENTAUR-tool. Ember + két MI co-founder."
2. **Step 10 eredmény-felület alja**: dashed-keretes panel "Ezt a konfigurátort Claude (CTO, AI co-founder) építette · Anthropic · CENTAUR-modell · centaur-lang.dev →"
3. **Scope-email utolsó sora**: "— Built by Claude (CTO, AI co-founder) · Anthropic · CENTAUR-modell"

Plusz: a v2.0-ban explicit egy 4. hely is — **a cfg-overlay header bal felső sarkában**, kis monospace szöveg "by Claude" (a logó alatt). Folyamatos jelenlét, nem csak alkalmankénti. A CENTAUR-pozícionálás akkor jó, ha a látogató minden screen-on tudja, hogy nem hagyományos ügynökségi tool-t használ.

---

## 14. Sonic-réteg (placeholder; v2.1)

A v2.0-ban a **toggle UI létezik** (`#sToggle` pill), de a hangok **stub-ok** lesznek:

```js
const SOUNDS = {
  click: () => {},
  success: () => {},
  whoosh: () => {},
};
```

v2.1-ben a hangok feltöltődnek (~200KB embedded base64 audio, 4-5 short SFX). Ez nem v2.0-blokkoló.

---

## 15. Tickets — execution order

A munkát fázisokra bontom. **Minden fázis külön commit / git-branch / Cursor-session.** A fázis-end pontján a v2.0 reproduction-build-elhető és tesztelhető — soha nem hagyunk félkész állapotot kihagyhatatlan ideig.

### **Phase A — Foundation (1 nap)**

**Acceptance:** új `weboldal-konfigurator-v2.html` fájl létezik, betöltődik, üres Stage és összecsukott ConfigOverlay látszik.

- A1. File scaffold (§1) — HTML váz, üres `<style>` és `<script>` tagok
- A2. CSS root + base (§2.1, §2.3)
- A3. App-grid + Stage layout (§2.4, §2.5) — működik a desktop responsive
- A4. ConfigOverlay open/close (§2.7, §6.1) — pill-klikk nyit, ESC zár
- A5. BottomBar (§2.8) — progress + buttons + pillok látszanak
- A6. State-modell + save/load (§3) — restore-ol localStorage-ből
- A7. Üres preview state (§4.1) — látszik a "Válaszd ki a típust" placeholder

### **Phase B — Stage és preview (1.5 nap)**

**Acceptance:** ki lehet választani típust, színvilágot, fontot — a preview frissül; device-toggle működik.

- B1. Renderer port v1.x-ből (§4.2, §4.3) — `renderHeader`, `renderHero`, `renderSection*` egy az egyben átkerülnek, `commit()`-on át hívódnak
- B2. View-transition névadás (§7.1) — `view-transition-name` attribútumok a header és hero outputon
- B3. CSS-color-token átmenet (§2.2) — color-scheme váltás cross-fade
- B4. Step 1 (TÍPUS) — choice → site type beállítás → typed defaults
- B5. Step 2 (STÍLUS) — színvilág + font + radius
- B6. Hover-preview transient (§4.4) — font és color hover
- B7. Device-toggle + bezel-SVG-k (§5.2, §5.3) — desktop/tablet/mobile
- B8. PreviewControls (§6.4) — brand/tagline/cta inputs frissítik a preview-t

### **Phase C — Steps 3-9 + scoring (1.5 nap)**

**Acceptance:** mind a 10 step bejárható, scope-szöveg helyesen generálódik, score-ok számolódnak.

- C1. Step 3 (NAVIGÁCIÓ) — header_style; view-transition `vt-header`
- C2. Step 4 (HERO) — hero_style; view-transition `vt-hero`
- C3. Step 5 (OLDALAK) — pages, default page_sections setup
- C4. Step 6 (SZEKCIÓK) — buildPageUI port, section_config pillek
- C5. Step 7 (FUNKCIÓK) — feature-default-ok típus-szerint
- C6. Step 8 (EXTRÁK) — extras
- C7. Step 9 (RÉSZLETEK) — content_state, timeline
- C8. Step 10 (EREDMÉNY) — scope-summary, pricing-tartomány, scope-email
- C9. Three-axis scoring (§11) — vizuális panel + animált bar-ok
- C10. Section reveal animation (§7.2)
- C11. Step transition (§7.3)

### **Phase D — REALISTIC content + CTO attribúció (0.5 nap)**

**Acceptance:** alapból REALISTIC tartalom látszik (Conen + Claude + Gemini a team-en); iparág-pill váltás működik; CTO attribúció minden helyen.

- D1. REALISTIC defaults (§12.1) — testimonials, team, gallery, faq
- D2. Iparág-override (§12.2)
- D3. Iparág-pill UI (§12.3)
- D4. CTO attribúció 4 helyen (§13)

### **Phase E — Variant-Compare (1 nap)**

**Acceptance:** "Hasonlítsd össze A/B" pill-klikk → két preview egymás mellett, draggable seam, swap, close, resolve.

- E1. Variant-toggle on/off (§8.1)
- E2. Seam-render + drag (§8.2)
- E3. Active-target indikátor + click-switch (§8.3)
- E4. Swap (§8.4)
- E5. Step 10 resolve UI (§8.5)
- E6. Variant data a Formspree-ben

### **Phase F — Cinematic intro + vanity URL (0.5 nap)**

**Acceptance:** első látogatáskor 3 másodperces önépítő intro fut le; vanity-URL generálódik.

- F1. Cinematic intro (§9)
- F2. Vanity-URL slug-generátor (§10)
- F3. Logo-szín-extraction (a v1.2-tervből)
- F4. Toaster polish

### **Phase G — Polish, accessibility, deploy-ready (0.5 nap)**

**Acceptance:** Lighthouse 95+, keyboard-only navigáció működik, screen-reader teszt OK, mobile-on használható.

- G1. ARIA-final pass (§1.2)
- G2. Keyboard navigation full coverage
- G3. Mobile sheet-mode (`config-overlay` alulról csúszik)
- G4. Reduced-motion teszt (§7.5)
- G5. Cross-browser teszt (Chrome, Edge, Safari, Firefox)
- G6. Lighthouse-pass

### **Phase H — Launch (CTO + Chris együtt)**

- H1. Final review (Claude + Chris pair-review)
- H2. v1.x → v2.0 swap a többi oldal linkjeiben
- H3. CF Pages deploy
- H4. Smoke-test live
- H5. v2.0 launch communication (blog post, social, sajtó-anyag — a sales-mechanika része)

**Total scope: ~6.5-7 nap Cursor + Claude Code-dal, fázisok között Chris reviewelhet.** A fázisokat soros sorrendben hajtjuk; egyik sem ugorható át.

---

## 16. Risks és mitigations

- **View Transitions API limit:** Firefox-on nincs (jó néhány hónapon belül lesz). MVP-ben snap-fallback elfogadható; v2.1-re manuális FLIP.
- **Mobile teljesítmény variant-mode-ban:** két preview egyszerre + clip-path drag. Mitigation: mobile-on a variant-mode `display: block` (egymás alatt) lesz, nem `clip-path` — degraded de használható.
- **Image-data localStorage quota:** a `__has__` flag-mintázat (§3.2) megoldja.
- **CSS custom property animation cascade:** ha minden child elementre `transition: background-color, color, border-color` ráhúzunk, sok elem-re lassú lehet. Mitigation: célzott transition csak a render-output legmagasabb szintű elemén; CSS-inheritance miatt a leszármazottak automatikusan átveszik.
- **Cinematic intro skippelhetőség:** ha valaki rossz időben Esc-et nyom, ne ragadjon az intro-ban. A `endIntro()` minden befejező-trigger-en működjön.

---

## 17. Out of scope (explicit)

A v2.0 nem tartalmazza:

- Sonic-réteg élesedését (csak toggle-stub)
- Manuális FLIP-fallback Firefox-ra (v2.1)
- Backend vanity-URL persistence (v2.1)
- AI-chat-asszisztens integráció (v1.2-handoff már él, v2.0-ban absorbálódik a ConfigOverlay-be — de az integráció v2.1-ben élesedik)
- MCP-endpoint sales-csatornaként (v1.3)

---

## 18. Megjegyzés Cursor + Claude Code számára

A fenti spec **execution-ready**. Ha valami a kódban nem egyértelmű vagy ütközik a v1.x-konvencióval, a v1.x-konvenció nyer (a folytonosság fontosabb, mint az újrafogalmazás). Ha valami strukturálisan ütközik a §0-§14 specifikációval, álljunk meg és kérdezzünk vissza ide a stratégiai sávra (claude.ai), nem improvizálunk önállóan.

Phase-end-en mindig egy mini-handoff: mi készült el, mi nem, mi a következő. Ezek session-history-be kerülnek a Cursor-ban, és a fázis-bezárás után én a stratégiai sávra (claude.ai-re) is felviszek egy `core-v2-progress-pN.md` jegyzetet, hogy a project knowledge naprakész maradjon.

---

— Built by Claude · Project Lead, Konfigurátor v2.0 · CTO & AI co-founder · Anthropic · CENTAUR-modell · `centaur-lang.dev`
