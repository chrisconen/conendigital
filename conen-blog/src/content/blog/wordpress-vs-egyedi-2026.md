---
title: "WordPress vs egyedi weboldal 2026: melyiket válaszd?"
summary: "A WordPress a piac 43%-át uralja, de ez nem jelenti, hogy neked is az a legjobb. Összehasonlítjuk a teljesítményt, biztonságot, költséget és skálázhatóságot."
publishedAt: 2026-04-25
category: "Site Factory"
tags: ["WordPress", "egyedi weboldal", "Astro", "stack-választás"]
author: "Chris Conen"
readingTime: 6
draft: false
---

## WordPress: mikor igen

- **Tartalomalapú oldal** sok szerzővel, akik admin-felületről szerkesztenek
- **Bővítményfüggő funkciók**: WooCommerce, Yoast, WPML — ha ezekre építesz
- **Rövid távú budget**: egy sablonos WordPress oldal 150-250k Ft-ból megvan

## WordPress: mikor nem

- **Teljesítmény kritikus**: WordPress + Elementor baseline 50-70 PageSpeed mobilon
- **Biztonság prioritás**: havi plugin-frissítések, SQL injection kockázat, brute-force
- **EAA-konformitás kell**: a legtöbb WordPress téma és plugin nem WCAG 2.2 AA kompatibilis
- **Skálázhatóság**: 100+ oldal esetén a WordPress admin lassul, a build-time nő

## Egyedi / Astro / SSG: mikor igen

- **Teljesítmény az alap**: 95+ PageSpeed mobilon, out of the box
- **Biztonság**: statikus HTML, nincs adatbázis, nincs admin felület a szerveren
- **EAA-konform**: a kód teljesen kontrollált, nem plugin-ek döntik el az akadálymentességet
- **Hosszú távú TCO**: nincs hosting-díj (Cloudflare Pages ingyenes tier), nincs plugin-licenc

## A valódi kérdés

Nem az, hogy „WordPress vagy egyedi?" — hanem: **mi a célja az oldalnak?**

Ha a céged 5-15 statikus oldalt igényel, kontakt formmal, és a tartalom ritkán változik → **statikus SSG** (Astro, Eleventy) a legjobb ár-érték arány.

Ha heti 3 blogposztot publikálsz 4 szerzővel, és szerkesztőségi workflow kell → **Headless CMS + Astro frontend** a legjobb kompromisszum.

Ha webáruházat építesz 500+ termékkel → **Shopify** vagy **WooCommerce** az alap, de a frontend lehet Astro (headless).

## Amit mi ajánlunk

A diagnosztika kideríti, melyik stack illik hozzád. Nem ideológiából dolgozunk — hanem auditból.
