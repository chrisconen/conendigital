---
title: "99-es PageSpeed mobilon: hogyan értük el a Motyán Árnyékolásnál"
summary: "13.5 másodperces betöltési időből 1.8 lett. PageSpeed score 57-ről 99-re. Ez a cikk dokumentálja, mit változtattunk meg az Astro-migráció során — mérhető lépésenként."
publishedAt: 2026-05-04
category: "Case Study"
tags:
  - "PageSpeed"
  - "Astro"
  - "WordPress"
  - "performance"
author: "Chris Conen"
readingTime: 4
draft: false
---

A Motyán László árnyékolástechnika cég weboldala WordPress + Elementor stacken futott — ami a 2018-as évek standard megoldása a magyar KKV-piacon. 2026-ban viszont már nem áll meg.

A migráció előtti mérési alapadatok:

| Metrika | Érték |
|---|---|
| Mobil PageSpeed score | 57 |
| LCP (Largest Contentful Paint) | 13.5 másodperc |
| TBT (Total Blocking Time) | 890 ms |
| Bundle méret | 4.2 MB |

Ezek a számok azt jelentik, hogy egy mobil látogató **13 és fél másodpercig** nézi a fehér képernyőt, mielőtt megjelenik a hero. A Google Core Web Vitals küszöbe LCP-re 2.5 másodperc — háromszorosát sem értük el.

## Az új stack

A migráció után:

| Metrika | Érték |
|---|---|
| Mobil PageSpeed score | **99** |
| LCP | **1.8 másodperc** |
| TBT | **40 ms** |
| Bundle méret | **180 KB** (gzip) |

Stack: **Astro 5.x** statikus generálás, **Cloudflare Pages** hosting, **WebP képek** lazy loading-gal, **kritikus CSS** inline-olva, fontok `font-display: swap`-pel.

## Ami a leginkább számított

Három változtatás adta a fő nyereséget. WordPress lecserélése Astro-ra önmagában 30+ pontot vitt fel a score-on — a WordPress + Elementor jQuery-t, jQuery Migrate-et, Elementor runtime-ot, és féltucat plugin scriptet tölt be minden oldalon, minden látogatónak. Az Astro statikus HTML-t generál; a látogató csak a tényleg szükséges JS-t kapja.

A képek WebP-re konvertálása + lazy loading szintén jelentős nyereség volt. A korábbi PNG/JPG hero-képek 800-1200 KB-osak voltak. WebP-vel ugyanaz vizuális minőségben 80-150 KB. A `loading="lazy"` attribute pedig a fold alatti képeket csak akkor tölti be, ha közelednek a viewport-hoz.

A kritikus CSS inline-olása a `<head>`-be került, így a böngésző nem vár external stylesheet letöltésre, mielőtt elkezdi renderelni az oldalt. Ez egyedül 2-3 másodpercet vitt le az LCP-ről.

> Ez a cikk később bővül a teljes implementációs részlettel, kódminta-mintákkal, és a tényleges Lighthouse audit screenshotokkal.

## A tanulság

Ha a PageSpeed score-od 70 alatt van mobilon 2026-ban, az nem optimalizálási kérdés — az **stack-választási kérdés**. Egy WordPress + Elementor oldal néhány pluginnel is csak ritkán éri el a 90-et mobilon, hiába rakunk rá cache-pluginokat.

Astro vagy hasonló SSG (Static Site Generator) stack mellett a 95+ az alapértelmezett, nem a kivétel.
