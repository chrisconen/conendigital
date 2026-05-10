# Conen Digital Konfigurátor v2.0 — Master Architecture Sketch

**Dokumentum-típus:** Alaprajz (foundational sketch), nem implementáció-spec
**Szerző:** Claude — Project Lead, CTO & AI co-founder · Anthropic · CENTAUR-modell
**Státusz:** Draft 1 · Conen Krisztián számára informális megosztásra (no approval gate, per CEO mandátum)
**Dátum:** 2026-05-10
**Working codename:** `core-v2`
**Final név:** TBD — készből születik, nem rajzból. A v2.0 karaktere még csak körvonalazódik; a nevet a launch előtt rögzítem.

---

## 0. A frame — mi változik vs. v1.x

A v1.x egy **kompetens élő mockup-konfigurátor**. A v2.0 ennél kategoriálisan többet vállal: **a tool maga a CENTAUR-bizonyíték**. Nem azt mondjuk a látogatónak, hogy "AI-co-founderekkel dolgozunk", hanem amit a kezében tart, azt csak ilyen szervezet tudja megépíteni.

Három core mozdulat alkotja a paradigma-váltást, és minden egyéb döntés ezeknek a támogatása vagy következménye:

1. **Preview-first architektúra** — a preview a stage, a config az overlay. Inverz a v1.x hierarchiához.
2. **Variant-compare mint core mode** — két élő preview egymás mellett, draggable seam-mel. A killer feature; nem v1.3-prioritás, hanem v2.0-mag.
3. **Cinematic continuity** — minden state-átmenet animál, nem snap-pel. Filmes érzet, nem űrlap-érzet.

Ez egy harmadik osztályt nyit meg: nem ügynökségi kalkulátor, nem termék-builder, hanem **sales-tool-élő-preview-val-és-variant-compare-rel**, ahol jelenleg senki nem áll. Itt fogunk egyedül állni, és pontosan ezt kommunikáljuk.

---

## 1. State-modell

A v1.x egyetlen lapos `S` objektumot használt. A v2.0 strukturált state-modellt vezet be, mert a variant-compare és a meta-UI-állapotok rendezett szétválasztást igényelnek.

```js
const State = {
  // A weboldal definíciója — "mit építünk"
  site: {
    type, brand, tagline, cta, logo, hero_img,
    style:    { color_scheme, font_family, border_radius, font_size },
    nav:      { header_style, hero_style },
    pages:    [...],
    page_sections:  { ... },
    section_config: { ... },
    features: [...],
    extras:   [...],
    content_state, timeline,
    industry, // v1.2-handoff carry-over
  },

  // Variant-slot — a killer-feature alapja
  variant: null | { ...same shape, partial overlay over site },
  variant_active: false,   // toggles the split-view
  variant_seam_pos: 0.5,   // 0..1, draggable seam horizontal position
  variant_active_target: 'site' | 'variant', // melyik oldalra mennek a választások

  // Meta-state — UI-viselkedés, nem site-definíció
  meta: {
    step,                    // 1..10
    active_page, device,
    config_overlay_open: false,  // alapértelmezetten összecsukva
    realistic_mode: true,        // ALAPÉRTELMEZETT (nem toggle-on)
    sound_enabled: false,
    motion_reduce: <derived from prefers-reduced-motion>,
    intro_seen: false,           // localStorage flag
  },

  // Score-ok — derived, cache-elt
  scores: { eaa, ax, centaur }   // computed from site
}
```

**Kritikus döntések ebben a modellben:**

- A `site` és `variant` szerkezetileg azonosak, ami a swap-és-merge műveleteket triviálissá teszi.
- A `meta` teljesen elkülönül — UI-állapot soha nem keveredik a site-definícióval. Ez azért fontos, mert a vanity-URL share csak a `site`-ot serializálja, nem a teljes UI-státuszt.
- A `realistic_mode: true` az alapértelmezett. A v1.2-handoff szerint ez toggle volt; a v2.0-ban ez fordítva van: a wireframe-mode lesz az opcionális kapcsolható állapot.

---

## 2. Komponens-fa

```
<App>
  <Stage>                          // a preview a stage, a stage az egész
    <DeviceFrame device>           // iPhone / iPad / MacBook bezel SVG
      <PreviewFrame role="primary"  state={site}/>
      <PreviewFrame role="variant"  state={variant} if active/>
      <VariantSeam     if active/>  // draggable függőleges osztó
    </DeviceFrame>
    <MotionLayer/>                  // cross-fadek, morphok, view-transitions itt élnek
  </Stage>

  <ConfigOverlay collapsed={meta.config_overlay_open}>
    <StepPilot step={meta.step}/>   // kompakt step-navigáció
    <StepContent>                   // a tényleges választások
      ... step-specific UI ...
    </StepContent>
    <PreviewControls>               // brand/tagline/cta inputs, device toggle, fs zoom
    </PreviewControls>
  </ConfigOverlay>

  <BottomBar>                       // vékony, mindig látható
    <ProgressTrack/>
    <NavButtons/>
    <VariantToggle/>                // "Hasonlítsd össze A/B" pill
    <SoundToggle/>
    <ShareWidget/>                  // vanity URL + copy
  </BottomBar>

  <CinematicIntro on first visit/>  // 3 másodperces self-build animáció
  <Toaster/>
  <Backstage>                       // keyboard shortcuts, help, dev-mode
  </Backstage>
</App>
```

A v1.x grid (`grid-template-columns: minmax(340px, 42%) 1fr`) eltűnik. Helyette a Stage full-bleed, és a ConfigOverlay `position: fixed`-en lebeg fölötte, translucent backdrop-blur-rel. Mobilon a ConfigOverlay alulról csúszik fel sheet-ként.

---

## 3. A három core mozdulat — architekturális szinten

### 3.1 Preview-First

- **Stage** full-bleed background. Default állapotban egy vibráló REALISTIC bemutatkozó-típus, dark-cyan színvilággal, betöltve. A látogató első frame-en már lát egy kész weboldalt.
- **ConfigOverlay** alapértelmezetten **összecsukva**, jobb oldali függőleges pill formában ("TERVEZD →"). Klikkre kicsúszik 360-420px széles overlay-jé, blur-backdrop-pal.
- A Stage és a ConfigOverlay **soha nem versenyez ugyanazokért a pixelekért teljes állapotban** — az overlay mindig translucent backdrop-blur-rel takar, sosem solid.
- A user-feel: nem űrlapot tölt ki, ami mellett egy preview frissül. Egy valódi weboldalt manipulál közvetlenül, és időnként előhúz egy panelt, hogy beállítást váltson.

### 3.2 Variant-Compare

- A `<VariantToggle/>` pill mindig látható a BottomBar-ban. Klikkre `variant_active = true`, és `variant = clone(site)`.
- Két `<PreviewFrame/>` egymás mellett rendelődik. Default vertikális seam 50%-on, klasszikus before/after slider-pattern (mint az image-comparison widgetek), draggable handle-lel.
- **Active-target indikátor:** vizuális kiemelés (subtle glow, vagy border) jelöli, melyik oldalra mennek a választások. Klikk a nem-aktív oldalra → átkapcsol az aktív target. Choices flow → `state[active_target]`-be.
- **Swap:** egy ikon az osztón → a két oldal gyorsan átfordul (300ms ease-in-out cross-fade).
- **Merge / Resolve:** a flow végén "Melyiket választod?" — pick left, pick right, or save both. A vanity-URL share és a scope-email mindkettőt el tudja vinni.
- Vizuális: az osztó-vonal egy 1.5px-es cyan→magenta gradient, közepén egy 32px circle-handle ←→ ikonokkal. Drag-eléskor a háttér enyhén "mélyebbre" megy (filter: brightness 0.95) — a manipulált tárgy érződik.

**Miért ez a killer feature:** sales-tool-ok között senki nem csinál variant-compare-t. Egy A/B-élő-összehasonlítás a saját webhelyed-koncepciójáról. Egyetlen képernyőkép erről, és kész a marketing-anyag. Egy GIF, egy demó-videó, egy 1500 szavas blog-poszt — ez a pozícionáló bomba.

### 3.3 Cinematic Continuity

- Minden site-érintő state-átmenet a **MotionLayer**-en megy keresztül.
- Elsődleges mechanika: **View Transitions API** (modern Chrome/Edge/Safari). Fallback: FLIP-style animációk vanilla JS-szel. Reduced-motion → max 60ms cross-fadek, soha nem dobjuk el az animációt teljesen, de tompítjuk.
- **Konkrét, named transitions** (lásd a 5. szekció motion-spec táblát): color-scheme:cross-fade, header-style:morph, hero-style:transition, section:reveal, step:transition, variant:swap.
- Hover-preview transient: font hover → 280ms-os preview-átíródás → mouseleave → 200ms-os snap vissza. Color-scheme hover → ugyanez, csak a CSS-color-tokenekkel. Tactile, nem absztrakt.

---

## 4. Critical-Path User Flow

### Phase 0 — Cinematic intro (csak első látogatáskor, 3 másodperc)

1. Stage fekete. Egyetlen sor monospace szöveg középen: "Egy CENTAUR-tool. Ember + két MI co-founder."
2. Stage felépíti magát: wireframe-dobozok megjelennek → szín befolyik → tipográfia beáll → kész hero-szekció előbukkan.
3. Overlay-szöveg fade-in: "Most a tied. Tervezd meg." + "Kezdés" gomb.
4. Kihagyható Esc-cel vagy "Kihagyom" linkkel.
5. Csak első látogatáskor fut le; localStorage-flag `core_v2_intro_seen`. Friss-start törli.

### Phase 1 — First touch (0–30 másodperc)

- Beérkezés: Stage full-bleed mutat egy alapértelmezett preview-t (REALISTIC bemutatkozó, dark-cyan, hero-style: centered).
- ConfigOverlay collapsed pill jobb oldalon: "TERVEZD →".
- User klikk → overlay nyílik, Step 1 (TÍPUS) látszik.
- User választ egy típust → preview cross-fade-el a típus default-jaira (pages, sections, features → mind a típushoz illő preset). Ez az **első katarzis-pillanat** — az egész oldal megváltozik, élőben, egyetlen kattintásra.

### Phase 2 — Engagement (30s–3 perc)

- User végigmegy a step-eken; minden választás named transition-t indít.
- Step 2-n font-hover → transient preview-rebuild a Stage-en → mouseleave → snap vissza.
- Step 2-n color-scheme hover → ugyanez a hover-mechanika a CSS-color-tokenekkel.
- Step 6-n a page-tabok között váltás a preview-t is animáltan vezeti át (a "fő-oldal → kapcsolat → rólunk" valódi navigációs élménnyé válik).

### Phase 3 — Variant-compare (bárhol, de tipikusan Step 3-7 között)

- BottomBar pill: "Hasonlítsd össze A/B".
- Klikk → variant init mint clone, seam megjelenik.
- User módosít egy beállítást → csak az aktív target változik.
- User klikkel a másik oldalra → az lesz az aktív target.
- **Killer demo-pillanat:** balra "sticky header", jobbra "transparent → solid header", mindkettő él, scroll-szimulációval is működnek.

### Phase 4 — Resolution (Step 10)

- Scope-summary, pricing-tartomány, három-axis scoring (EAA + AX + CENTAUR), megközelítés-panel (Hagyományos vs CENTAUR).
- "Vanity-URL generálása" gomb → produkál egy `conendigital.hu/cfg/<random-three-word-slug>` linket (pl. `conendigital.hu/cfg/csillag-ablak-deli`). Ez share-elhető, és a slug 30 napig él.
- Scope-email Formspree-vel (létező mechanika).
- Ha variant aktív volt: opcionálisan mindkettő el-küldhető. "Melyiket szeretnéd, hogy a diagnosztikára vigyük?" — A, B, vagy mindkettőt.

---

## 5. Motion-spec tábla

| Átmenet | Időtartam | Easing | Réteg |
|---|---|---|---|
| `color-scheme:cross-fade` | 380ms | `ease-out` | MotionLayer (CSS custom properties animálva) |
| `header-style:morph` | 520ms | `cubic-bezier(0.4, 0, 0.1, 1)` | View Transitions API |
| `hero-style:transition` | 640ms | `cubic-bezier(0.25, 0.1, 0.3, 1)` | View Transitions API |
| `section:reveal` | 320ms (60ms staggered) | `cubic-bezier(0.34, 1.4, 0.64, 1)` | per-section CSS |
| `section:remove` | 240ms | `cubic-bezier(0.4, 0, 1, 1)` | per-section CSS |
| `step:transition` | 280ms | `ease-out` | overlay-only, Stage nem mozog |
| `variant:open` | 420ms | `cubic-bezier(0.4, 0, 0.1, 1)` | Stage |
| `variant:swap` | 300ms | `ease-in-out` | cross-fade |
| `variant:close` | 360ms | `ease-out` | Stage |
| `variant:seam-drag` | 0ms | `linear` | live, nincs animáció |
| `device-frame:change` | 480ms | `ease-in-out` | bezel + content |
| `cinematic:intro` | 3000ms | scripted, multi-stage | one-shot |
| `font:hover-preview` | 280ms in / 200ms out | `ease-out` / `ease-in` | Stage szövegelemei |
| `color:hover-preview` | 320ms in / 240ms out | `ease-out` / `ease-in` | Stage CSS-tokenek |

**Reduced-motion override:** ha `prefers-reduced-motion: reduce`, minden timing → max 60ms cross-fade. Soha nem dobjuk el az átmenetet teljesen, mert a state-változás vizuális visszajelzése akadálymentességi szempontból is fontos.

---

## 6. Mit nem fed le ez a sketch (deferred a következő doc-ra)

- Részletes CSS-architektúra (várhatóan: CSS custom properties + view transitions + minimal motion lib)
- Vanilla JS vs. könnyű React-réteg végleges döntés (jelenleg vanilla felé hajlok, de TBD)
- Per-section render-minőség upgrade (a "polished mockup → polished site" ugrás konkrét specifikációja)
- Sonic réteg specifikáció (hangok, toggle-mechanika, asset-lista)
- Real-device frame asset-ek (iPhone 16 Pro, iPad Air, MacBook Pro 14")
- v2.0 final név — ezt a launch előtt rögzítem
- Backend/state-persistence vanity-URL-ekhez (Cloudflare Worker KV-store kell hozzá; ez a v2.1-ben élesedik)
- AI-asszisztens chat integrációja a ConfigOverlay-be (in-flow assistant, nem floating fab)

---

## 7. Decision log — unilaterálisan meghozott döntések (per CEO-mandátum)

1. **Default REALISTIC content.** A wireframe-mode opcionális toggle lesz, nem fordítva.
2. **Variant-compare v2.0-mag, nem v1.3-prioritás.** Promotált a killer-feature pozícióba.
3. **Nincs floating chat-fab.** Az AI-asszisztens absorbál a ConfigOverlay-be, in-flow context-aware.
4. **Cinematic intro one-shot.** Skippable, de minden first-time visitor látja. Nem toggleable.
5. **Three-axis scoring panel marad.** EAA + AX + CENTAUR. v1.2-tervből átvéve.
6. **Preview a stage, config az overlay.** Inverz a v1.x hierarchiához.
7. **Vanity-URL random three-word slug-gal.** Magyar szótár-alapú generátor (~3-szótagos szavak, 200-300 elemes pool).
8. **State-modell strukturált, nem flat.** `site` / `variant` / `meta` / `scores` szétválasztva.
9. **Final név rögzítése a launch előtt, nem most.** Working codename `core-v2`.
10. **Mobil: ConfigOverlay sheet alulról.** Nem külön mobile-PV button, mint a v1.x-ben.

---

## 8. Következő lépés

Ez alaprajz. Olvasd el. Ha van strukturális észrevétel, jelezd; ha nincs, megyek a következő iterációra: az **Implementation Spec**, ami már Cursor-számára-futtatható dokumentum. Az Implementation Spec a következőket fogja tartalmazni:

- File-paths (mit szerkesztünk, mit hozunk létre)
- Pontos CSS custom property nevek és értékek
- Function signature-ök a kritikus state-tranzakciókra
- Acceptance criteria minden ticket-hez
- Cursor-ready tasking — Claude Code lefuttat egy ilyen docot, és a v2.0 kódba leírva születik meg
- Várhatóan ennek a dokumentumnak a 3-5x-szeres terjedelme

Egy kérés a deploy-cikluson tartott kezedhez: a v2.0 munka **nem** a `weboldal-konfigurator.html` átírásával kezdődik, hanem külön fájllal (`weboldal-konfigurator-v2.html` vagy `core-v2.html`). A v1.x élesben marad addig, amíg a v2.0 nem teljes és tesztelt. Csak a launch napján cseréljük le. Ez a CI/CD-szempontból tiszta, és nem kockáztatjuk a working sales-tool-t.

---

— Built by Claude · Project Lead, Konfigurátor v2.0 · CTO & AI co-founder · Anthropic · CENTAUR-modell · `centaur-lang.dev`
