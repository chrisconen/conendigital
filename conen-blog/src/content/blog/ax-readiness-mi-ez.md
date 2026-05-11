---
title: "AX-readiness: miért fontos, hogy az AI is olvassa a weboldalad"
summary: "2026-ban nem elég, ha a Google indexeli az oldaladat. Claude, ChatGPT, Perplexity is keresnek — és ha a weboldalad nem AX-ready, nem fognak téged idézni."
publishedAt: 2026-05-03
category: "AX-readiness"
tags: ["AX-readiness", "JSON-LD", "llms.txt", "semantic HTML", "AI"]
author: "Chris Conen"
readingTime: 5
draft: false
---

AX = AI Experience. Ahogy a UX a felhasználói élmény, az AX az **AI-asszisztensek élménye** a weboldaladon. Ha egy AI-keresőmotor (ChatGPT, Perplexity, Claude, Google AI Overview) nem tudja hatékonyan olvasni az oldaladat — nem fog téged ajánlani.

## A három pillér

**1. JSON-LD strukturált adatok**

A `<script type="application/ld+json">` blokkban a schema.org markup mondja el az AI-nek, hogy mi van az oldalon: Article, Organization, Product, FAQ, HowTo. Ez az egyetlen formátum, amit **minden AI-motor natívan ért**.

**2. llms.txt**

Egy egyszerű szöveges fájl a gyökérben (`/llms.txt`), ami elmondja az AI-nak: ki vagy, mit csinálsz, milyen szolgáltatásaid vannak. Mint a `robots.txt`, de AI-asszisztenseknek.

**3. Szemantikus HTML**

Nem div-spam. `<article>`, `<nav>`, `<header>`, `<main>`, `<aside>` — ezek a tagek mondják meg a struktúrát. Ha az AI egy `<div class="content-wrapper-inner-2">` halmazt lát — nem fogja érteni a hierarchiát.

## Miért számít ez üzletileg?

Mert a keresési forgalom egyre nagyobb része **AI-generált válaszokból** jön. Amikor valaki megkérdezi a ChatGPT-t: „melyik magyar webfejlesztő cég ért az EAA-hoz?", és a válaszban a te céged neve jelenik meg — az az új SEO.

## Mit csinálunk?

Minden projektünkben alapból benne van az AX-readiness:
- JSON-LD Article, Organization, LocalBusiness schema
- `llms.txt` a domainre
- Szemantikus HTML struktúra
- Open Graph és Twitter Card meta tagek

Ez nem extra csomag. Ez az alap.
