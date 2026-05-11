---
title: "Core Web Vitals 2026: a Google rangsorolás új szabályai"
summary: "Az LCP, INP és CLS hármas határozza meg, hogy a Google hová sorolja az oldaladat. Nem elég jó tartalmat írni — gyorsnak is kell lenni."
publishedAt: 2026-04-28
category: "Site Factory"
tags: ["Core Web Vitals", "LCP", "INP", "CLS", "Google", "SEO"]
author: "Chris Conen"
readingTime: 6
draft: false
---

A Google 2021-ben vezette be a Core Web Vitals-t rangsorolási jelként. 2026-ra ez **az egyik legfontosabb technikai SEO-faktor** lett.

## A három metrika

**LCP (Largest Contentful Paint)**: mennyi idő alatt jelenik meg a legnagyobb vizuális elem. **Cél: 2.5 mp alatt.** A hero kép vagy a főcím betöltése — ez az LCP.

**INP (Interaction to Next Paint)**: mennyi idő telik el egy klikk és a vizuális válasz között. **Cél: 200ms alatt.** Ez váltotta le az FID-et 2024-ben.

**CLS (Cumulative Layout Shift)**: mennyit „ugrik" az oldal betöltés közben. **Cél: 0.1 alatt.** Ha a szöveg betöltődik, aztán beugrik egy kép és letolja — az CLS.

## Mi rontja el?

- **WordPress + Elementor**: jQuery, Elementor runtime, 6-8 plugin script → LCP 4-8 mp
- **Nem optimalizált képek**: PNG/JPG 1-2 MB → WebP-vel 80-150 KB
- **Külső fontok render-block nélkül**: `font-display: swap` hiánya
- **Third-party scriptek**: analytics, chat widget, reklám → INP romlás
- **Hiányzó méretezés**: `<img>` width/height nélkül → CLS

## A mi stackünk miért gyors?

**Astro 5.x**: statikus HTML generálás, zero JS by default. Amit nem használsz, nem töltődik be.

**Cloudflare Pages**: edge-network, globális CDN, ~20ms TTFB Európában.

**Képoptimalizáció**: build-time WebP konverzió, responsive `srcset`, lazy loading.

Az eredmény: **95+ PageSpeed score alapból**, nem optimalizálás után.

## Hogyan mérd?

1. [PageSpeed Insights](https://pagespeed.web.dev) — a Google hivatalos eszköze
2. Chrome DevTools → Lighthouse tab
3. Search Console → Core Web Vitals report (valós felhasználói adatok)

Ha a mobilos score-od 70 alatt van — az nem optimalizálási kérdés. Az **stack-választási kérdés**.
