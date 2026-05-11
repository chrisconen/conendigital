---
title: "JSON-LD és strukturált adatok: az AI-keresők nyelve"
summary: "A strukturált adatok nem csak a Google rich snippet-ekhez kellenek. 2026-ban az AI-keresők (ChatGPT, Perplexity, Claude) is ebből dolgoznak. Ha nincs JSON-LD az oldaladon, láthatatlan vagy az MI számára."
publishedAt: 2026-04-18
category: "AX-readiness"
tags: ["JSON-LD", "schema.org", "strukturált adatok", "SEO", "AI"]
author: "Chris Conen"
readingTime: 5
draft: false
---

## Mi az a JSON-LD?

JavaScript Object Notation for Linked Data. Egy `<script type="application/ld+json">` blokk a HTML `<head>`-ben, ami gépi olvasható formátumban írja le az oldal tartalmát.

```json
{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": "JSON-LD és strukturált adatok",
  "author": { "@type": "Person", "name": "Chris Conen" },
  "publisher": { "@type": "Organization", "name": "Conen Digital" }
}
```

## Miért fontos 2026-ban?

**Google**: rich snippet-ek (FAQ, HowTo, Article, Product) → magasabb CTR a keresési eredményekben.

**AI-keresők**: ChatGPT, Perplexity, Claude mind **JSON-LD-t olvasnak először**, mielőtt a szöveges tartalmat értelmezik. Ha nincs schema markup, az AI nem tudja strukturáltan feldolgozni az oldaladat.

**Voice search**: „Hey Google, melyik cég csinálja a legjobb weboldalt Győrben?" → a `LocalBusiness` schema válaszol.

## Milyen típusokat érdemes használni?

- **Organization / LocalBusiness**: cégadatok, elérhetőség, nyitvatartás
- **Article / BlogPosting**: cikkek — headline, author, datePublished
- **Product**: termékek — ár, elérhetőség, értékelés
- **FAQ**: gyakori kérdések — közvetlenül a keresési eredményben jelennek meg
- **BreadcrumbList**: navigációs útvonal
- **HowTo**: lépésről lépésre útmutatók

## Hogyan implementáljuk?

Minden projektünkben a JSON-LD alapból benne van. A blog-posztokban Article schema, a szolgáltatás-oldalakon Service schema, a főoldalon Organization + LocalBusiness.

Nem plugin — hanem a kódban, build-time generálva, validálva a Google Rich Results Test-tel.
