---
title: "WordPress → Astro migráció: teljes útmutató magyar KKV-knak"
summary: "Lépésről lépésre: hogyan vidd át a WordPress oldaladat Astro-ra anélkül, hogy elveszítenéd a SEO-pozícióidat, a tartalmadat, vagy az eszed."
publishedAt: 2026-04-05
category: "Site Factory"
tags: ["WordPress", "Astro", "migráció", "SSG", "teljesítmény"]
author: "Chris Conen"
readingTime: 7
draft: false
---

## Miért migrálsz?

Ha a WordPress oldaladon:
- A PageSpeed mobilon 70 alatt van
- Havonta plugin-frissítéssel és biztonsági patchekkel foglalkozol
- Az EAA-megfelelés plugin-ektől függ (és nem működik)
- A hosting 20-50 EUR/hó, és lassú

...akkor ideje váltani.

## A migráció 5 lépése

### 1. Tartalom export

WordPress → Tools → Export → All content. Ez XML-t ad. Az Astro-nak Markdown kell. Konvertáló eszközök: `wordpress-export-to-markdown` (npm), vagy kézi átalakítás.

**Fontos**: a képeket külön kell letölteni és optimalizálni (WebP konverzió).

### 2. URL-struktúra megtervezése

A régi WordPress URL-ek (`/2024/03/cikk-cim/`) és az új Astro URL-ek (`/blog/cikk-cim/`) különbözhetnek. **301 redirect-ek kellenek** — Cloudflare Pages `_redirects` fájllal.

Ha az URL-struktúra változik redirect nélkül → SEO-pozíció elvész.

### 3. Design átültetés

Nem kell 1:1 másolat. Az Astro komponens-alapú — Header, Footer, PostCard, Layout. A CSS custom property-k a design-tokenek.

A tipikus idő: 2-3 nap egy átlagos KKV oldal designjának átültetésére.

### 4. Funkciók átgondolása

Kontakt form: Formspree vagy Cloudflare Workers. Analytics: GA4 (script tag). Keresés: Pagefind (build-time index). Kommentek: általában nem kell.

Ami nem kell: Yoast (a meta tagek kézzel jobbak), cache plugin (statikus oldalnak nincs cachje), security plugin (nincs mit védeni).

### 5. DNS átállás

Cloudflare DNS → Cloudflare Pages. A TTFB 800ms-ről 20ms-re csökken, mert az edge-network szolgálja ki a statikus fájlokat.

## Az eredmény

Egy átlagos WordPress → Astro migráció után:
- PageSpeed: 50-70 → **95-100**
- Hosting: 20-50 EUR/hó → **0 EUR/hó** (Cloudflare Pages free tier)
- Betöltés: 3-8 mp → **0.5-1.5 mp**
- Karbantartás: heti 1-2 óra → **havi 30 perc**

## Mikor NE migrálj?

Ha a WordPress admin felületet napi szinten használják nem-technikai szerzők, és nincs budget headless CMS-re. Ilyenkor a WordPress marad — de a frontend lehet Astro (headless WordPress).
