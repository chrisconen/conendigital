# Conen Digital Blog

Astro 5.x static site, ami a `conendigital.hu/blog/` alatt fut. A főoldal érintetlen marad — ez egy különálló projekt, ami a `/blog/` subpath-ot szolgálja ki.

## Stack

- **Astro 5.x** — static site generator, build-time HTML generálás
- **Markdown content** — `src/content/blog/` mappában `.md` fájlok
- **Content Collections** — type-safe schema, automata routing
- **Cloudflare Pages** (vagy bármi static host) — deploy target
- **GitHub** — source-of-truth, commit-driven publish

Nincs adatbázis. Nincs admin felület. Nincs PHP. Cikket írni = `.md` fájl commit a `src/content/blog/`-ba.

## Helyi fejlesztés

```bash
# Egyszer, install
npm install

# Dev server (http://localhost:4321/blog/)
npm run dev

# Production build (output: dist/)
npm run build

# Build előnézet
npm run preview
```

Node.js 20+ kell.

## Új cikk írása

1. Hozz létre egy új `.md` fájlt itt: `src/content/blog/cikk-slug.md`
2. A fájlnév lesz az URL slug (pl. `cikk-slug.md` → `/blog/cikk-slug`)
3. Frontmatter (a `---` blokk a fájl tetején) **kötelező mezői**:

```yaml
---
title: "A cikk címe"
summary: "1-2 mondatos összefoglaló (meta description és card preview)"
publishedAt: 2026-05-06
category: "EAA"  # EAA | AX-readiness | AI Ops | Site Factory | MCP-Commerce | Case Study | CENTAUR
tags:
  - "tag1"
  - "tag2"
author: "Chris Conen"
draft: false  # true = nem jelenik meg
---
```

4. A `---` után jön a markdown tartalom. Standard markdown: `## H2`, `**bold**`, `[link](url)`, kód blokk három backtickkel, stb.
5. Commit + push → Cloudflare Pages 30 másodperc alatt deployolja.

A schema validációt a `src/content/config.ts` fájl végzi. Ha hibás frontmatter van, a build elhasal érthető hibaüzenettel.

## Mappastruktúra

```
src/
├── content/
│   ├── config.ts              # Content collection schema
│   └── blog/
│       └── *.md               # Cikkek
├── layouts/
│   ├── BaseLayout.astro       # HTML váz, header + footer
│   └── PostLayout.astro       # Cikk template, markdown stylek
├── components/
│   ├── Header.astro           # Sticky nav
│   ├── Footer.astro
│   ├── PostCard.astro         # Cikk lista item
│   └── SEO.astro              # Meta tags + JSON-LD Article schema
├── pages/
│   ├── index.astro            # /blog/ — cikk lista
│   ├── [...slug].astro        # /blog/cikk-slug
│   ├── category/[category].astro  # /blog/category/eaa
│   ├── rss.xml.ts             # /blog/rss.xml
│   └── 404.astro
└── styles/
    └── global.css             # Conen Digital design tokenek
```

## Deploy — Cloudflare Pages

A blog külön projektként fut a Cloudflare Pages-en, és a `conendigital.hu/blog/*` path-routinggal csatlakozik a fő domain-hez.

### 1. GitHub repo

Hozz létre egy új repót `conen-digital-blog` néven. Push:

```bash
git init
git add .
git commit -m "Initial commit: Astro blog setup"
git branch -M main
git remote add origin git@github.com:USERNAME/conen-digital-blog.git
git push -u origin main
```

### 2. Cloudflare Pages projekt

1. Cloudflare dashboard → Workers & Pages → Create application → Pages → Connect to Git
2. Válaszd a `conen-digital-blog` repót
3. Build settings:
   - **Framework preset:** Astro
   - **Build command:** `npm run build`
   - **Build output directory:** `dist`
   - **Root directory:** `/` (üresen)
   - **Environment variables:** semmi
4. Save and Deploy. Az első build kb. 1-2 perc.

### 3. Path-routing a fő domain alá

A blog két módon csatlakozhat a `conendigital.hu`-hoz:

#### Opció A: ugyanaz a Cloudflare Pages projekt mint a főoldal

Ha a `conendigital.hu` is Cloudflare Pages-en fut:

1. A főoldali Pages projektben add hozzá a `conendigital.hu` custom domain-t
2. A blog Pages projektben add hozzá ugyanezt a custom domain-t — Cloudflare Pages kezeli a subpath-ot az `astro.config.mjs` `base: '/blog'` beállítása alapján
3. Cloudflare automatikusan a megfelelő projektre routol a path alapján

#### Opció B: külön subdomain (`blog.conendigital.hu`)

Ha a főoldal máshol fut és nem akarod a path-routingot bonyolítani:

1. A blog Pages projektben add hozzá custom domain-ként a `blog.conendigital.hu`-t
2. Az `astro.config.mjs`-ben módosítsd: `site: 'https://blog.conendigital.hu'` és vedd ki a `base` sort

A subpath verzió (`conendigital.hu/blog/`) **SEO szempontból jobb** — ugyanaz a domain authority, AI engines is egységes brand-ként látják. Az alap setup (a jelenlegi `astro.config.mjs`) ezt feltételezi.

### 4. Sitemap a Search Console-hoz

Build után a sitemap automatikusan generálódik ide: `/blog/sitemap-index.xml`.

Adj hozzá egy `<Sitemap: https://conendigital.hu/blog/sitemap-index.xml>` sort a fő `robots.txt`-hez.

## Mit ad ez 2026 SEO-jában?

Minden cikk automatikusan kap:

- **Schema.org Article markup** (JSON-LD) → AI engines (Google AI Overviews, ChatGPT, Perplexity, Claude) ezt olvassák first-line. Ez a legerősebb single signal arra, hogy a cikkedet idézzék válaszaikban.
- **Open Graph + Twitter Card** → social sharing rendben renderelődik
- **Static HTML** → 99-es PageSpeed alapértelmezetten, mert nincs server-side rendering, nincs JS framework runtime
- **Sitemap** → Google Search Console azonnal indexelhet
- **RSS feed** → távoli olvasók, AI scrapers, hírlevél automatizációk

## A nyelvi/stílus iránymutatás

A `src/content/blog/eaa-megfeleles-2026.md` és `99-pagespeed-motyan-case-study.md` fájlok jelenleg `draft: true` — placeholder cikkek. Amikor készen állnak a teljes szöveggel, csak a `draft: true` sort kell `false`-ra állítani (vagy törölni).

A Quick Check PDF magnethez már megírt 12 pontos önaudit szövege egy az egyben átemelhető az EAA cikkbe — pillar content és lead magnet ugyanabból az alapból.

---

## Hibaelhárítás

**A build elhasal "InvalidContentEntryFrontmatterError" hibával:**
A `.md` fájl frontmatterje nem felel meg a `src/content/config.ts` schema-nak. Az error message megmondja melyik mező a hibás.

**A `/blog/` 404-et ad lokálisan:**
Az `astro.config.mjs`-ben `base: '/blog'` van beállítva, ezért a dev server a `http://localhost:4321/blog/`-on válaszol, nem a gyökéren.

**Cloudflare Pages "deployment failed" log:**
Általában `npm run build` hibát ad lokálisan is — futtasd először helyben, és a hibaüzenet megmondja mit kell javítani.
