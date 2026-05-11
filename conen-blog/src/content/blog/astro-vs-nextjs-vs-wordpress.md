---
title: "Astro vs Next.js vs WordPress: melyik stack a legjobb KKV-nak?"
summary: "Három technológia, három filozófia. Az Astro a sebességé, a Next.js a rugalmasságé, a WordPress a megszokásé. Összehasonlítás magyar KKV-szemszögből."
publishedAt: 2026-04-10
category: "Site Factory"
tags: ["Astro", "Next.js", "WordPress", "stack", "technológia"]
author: "Chris Conen"
readingTime: 6
draft: false
---

## Astro

**Filozófia**: „küldj kevesebb JavaScript-et a böngészőnek."

Astro statikus HTML-t generál build-időben. A JavaScript csak ott töltődik be, ahol tényleg kell (islands architecture). Az eredmény: **95-100 PageSpeed mobilon** alapból.

| | Astro |
|---|---|
| Sebesség | Kiváló |
| Tanulási görbe | Közepes |
| CMS integráció | Headless (bármilyen) |
| Hosting költség | Ingyenes (Cloudflare Pages) |
| EAA-konformitás | Teljes kontroll |

## Next.js

**Filozófia**: „mindent egy keretrendszerben."

Next.js React-alapú, SSR + SSG + ISR támogatással. Kiváló komplex alkalmazásokhoz (SaaS dashboard, e-commerce), de KKV bemutatkozó oldalhoz overkill.

| | Next.js |
|---|---|
| Sebesség | Jó (de több JS) |
| Tanulási görbe | Magas |
| CMS integráció | Headless |
| Hosting költség | Vercel (ingyenes tier limitált) |
| EAA-konformitás | Kézi munka |

## WordPress

**Filozófia**: „bárki szerkeszthesse."

WordPress a világ 43%-a. Admin felület, plugin-ökoszisztéma, ismerős. De a teljesítmény és a biztonság ára magas.

| | WordPress |
|---|---|
| Sebesség | Gyenge-közepes |
| Tanulási görbe | Alacsony |
| CMS integráció | Beépített |
| Hosting költség | 5-50 EUR/hó |
| EAA-konformitás | Plugin-függő |

## Mikor melyiket?

- **Bemutatkozó oldal, 5-15 oldal**: → **Astro**
- **Blog + hírlevél, több szerző**: → **Astro + Headless CMS** (vagy WordPress headless)
- **SaaS dashboard, komplex app**: → **Next.js**
- **Webáruház**: → **Shopify + Astro frontend** (vagy WooCommerce)
- **Ügyfél maga akar szerkeszteni**: → **WordPress** (ha a teljesítmény nem prioritás)

A mi alapértelmezett stackünk: **Astro + Cloudflare Pages**. Ha más kell — a diagnosztika dönti el.
