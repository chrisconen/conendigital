---
title: "Headless CMS 2026: mi ez, és miért jobb mint a WordPress admin"
summary: "A tartalom és a megjelenés szétválasztása. A headless CMS-ben a szerkesztő ír, a frontend-fejlesztő designol — egymástól függetlenül. Ez a jövő."
publishedAt: 2026-03-30
category: "Site Factory"
tags: ["headless CMS", "Strapi", "Contentful", "tartalom-kezelés"]
author: "Chris Conen"
readingTime: 5
draft: false
---

## A probléma a hagyományos CMS-sel

WordPress: a tartalom, a design, és a funkcionális logika **egy rendszerben** él. Ha a szerkesztő elront egy shortcode-ot → az egész oldal összeomlik. Ha a fejlesztő frissít egy témát → a szerkesztő tartalma felülíródhat.

## A headless megoldás

A tartalom egy **API-n** keresztül érhető el. A frontend (Astro, Next.js, bármi) lekéri a tartalmat, és megjeleníti. A szerkesztő a CMS admin-felületén dolgozik, a fejlesztő a frontend-kódon — **egymástól függetlenül**.

## Népszerű headless CMS-ek

**Strapi**: nyílt forráskódú, self-hosted, teljesen testreszabható. Magyar nyelv támogatott. Ideális: ha kontrollod akarod a hosting felett.

**Contentful**: SaaS, felhő-hosted, kiváló API. Ideális: ha nem akarsz szervert karbantartani.

**Sanity**: valós idejű szerkesztés, erős fejlesztői eszközök. Ideális: komplex tartalom-struktúrák.

**Decap CMS (volt Netlify CMS)**: Git-alapú, fájl-szintű. Ideális: statikus oldalak mellé, minimális overhead.

## Mikor éri meg?

- **Több csatorna**: ugyanaz a tartalom weboldalon, mobilappon, és digital signage-en
- **Több szerkesztő**: szerkesztőségi workflow, jóváhagyási rendszer
- **Teljesítmény**: a frontend statikus HTML, a CMS csak szerkesztéskor aktív
- **Biztonság**: nincs admin felület a publikus szerveren

## Mikor NEM éri meg?

- **1-2 fős csapat**: ha te vagy az egyetlen szerkesztő, egy Markdown fájl egyszerűbb
- **Egyszerű oldal**: 5 statikus oldal nem igényel CMS-t
- **Alacsony budget**: a headless CMS integráció plusz fejlesztési idő

## A mi ajánlásunk

Astro + Decap CMS a legtöbb magyar KKV-nak. Zero hosting költség, Git-alapú tartalom-kezelés, és a frontend teljesen kontrollált.
