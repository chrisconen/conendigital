---
name: portfolio-slider-clone-infinite-loop
description: Seamless infinite slider using clone technique on 13 pages
created: 2026-06-01T13:35:07.818Z
updated: 2026-06-01T13:35:07.818Z
metadata:
  type: project
---

# Portfolio slider — clone-based seamless infinite loop

Previous attempt used `goTo()` wrapping that animated the full distance back to 0 — looked broken.

**Fix:** Clone first slide → append to end, clone last slide → prepend to start. `transitionend` handler (`snapToReal()`) instantly snaps to the real slide with `transition: none` when reaching a clone.

**13 pages updated** with full rewrite (clone + `snapToReal` + `computeOffset` + `moving` guard):
- `index.html`, budapest, debrecen, eger, kaposvar, kecskemet, miskolc
- szeged, székesfehérvár, szolnok, szombathely, veszprem, zalaegerszeg

**3 pages unchanged** (already had simpler modulo-based infinite loop): nyiregyhaza, pécs, sopron

**Key details:**
- `getVisibleCount()` uses `realCount` (not with clones)
- `goTo(index, instant)` — second param `true` = no transition
- `moving` flag prevents double-fire during active animation
- Touch swipe → if not enough drag, `snapToReal()` ensures on-track
- Resize → `snapToReal()` instead of `goTo(current)`
