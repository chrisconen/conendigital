# Pragmatic Engineer → Conen Blog automatizáció (n8n)

Ez a workflow figyeli a [The Pragmatic Engineer](https://blog.pragmaticengineer.com/) blog RSS feedjét, és amikor új poszt jelenik meg, **egy AI-modellel magyar nyelvű, eredeti feldolgozást** készít belőle (forrásmegjelöléssel, belső linkekkel, SEO-frontmatterrel), majd **draftként commitolja** a `conen-blog` Astro tartalomgyűjteményébe.

A publikálás `git commit` egy új `.md` fájllal a `conen-blog/src/content/blog/` mappába → Cloudflare Pages buildeli.

---

## ⚠️ FONTOS – olvasd el, mielőtt élesíted

### 1. Szerzői jog
A workflow **szándékosan NEM szó szerinti fordítást** készít. Gergely Orosz tartalma szerzői jogvédett (és nagyrészt fizetős). A teljes cikkek lefordítása és újraközlése engedély nélkül **jogsértés**, és SEO-büntetést is hozhat (duplikált/scraped tartalom).

Ezért az AI-prompt **eredeti, magyar nyelvű elemző-összefoglalót** kér, ami:
- a fő gondolatokat ismerteti (parafrazeálva, max 30 egymást követő szó az eredetiből),
- hozzáteszi a **magyar/KKV piaci kontextust** (ez a Google szemében *unique content* → ez hozza a SEO-értéket),
- **kötelezően linkel vissza** az eredeti cikkre.

Ha mégis 1:1 fordítást szeretnél: **előbb szerezz írásos engedélyt** a szerzőtől.

### 2. Paywall
A friss Pragmatic Engineer cikkek nagy része fizetős. Az RSS feed ilyenkor **csak egy teasert** ad, nem a teljes szöveget. A workflow ezzel számol (a teaserből is tud összefoglalót írni), de a minőség jobb a nyilvános cikkeknél.

### 3. Minden poszt `draft: true`-val készül
A workflow **nem** publikál automatikusan élesben. Minden generált cikk `draft: true` frontmatterrel commitolódik → te átnézed, javítod, és csak utána állítod `false`-ra. **Erősen ajánlott így hagyni**, amíg be nem áll a minőség. (Élesítéshez lásd lent.)

---

## Telepítés

### Előfeltételek
- Self-hosted n8n (Docker) **vagy** n8n Cloud — nálad mindkettő szinkronban (hub.centaur-lang.dev).
- Egy LLM API kulcs. Alapból **DeepSeek**-re van állítva (`api.deepseek.com`, `deepseek-chat` modell – olcsó, jó magyar), de bármilyen OpenAI-kompatibilis végpont megy (lásd lent).
- Egy **GitHub Personal Access Token** a `chrisconen/conendigital` repóhoz (`repo` / `Contents: Read and write` jog).

### 1. Workflow importálása
n8n UI → bal felső menü → **Import from File** → válaszd a
`n8n/pragmatic-engineer-to-conen.workflow.json` fájlt.

### 2. GitHub credential
1. n8n → **Credentials** → **New** → *GitHub API*.
2. Server: `https://api.github.com` (vagy a GitHub Enterprise URL-ed).
3. Access Token: a PAT-od.
4. Mentsd `GitHub – conendigital` néven.
5. A workflow két GitHub node-jánál (`Meglévő posztok`, `GitHub commit`) válaszd ki ezt a credentialt.

> A JSON-ben `REPLACE_GITHUB_CRED_ID` helyőrző van — import után egyszerűen kattints a node-ra és válaszd ki a credentialt a legördülőből.

### 3. LLM credential (DeepSeek alapból)
1. n8n → **Credentials** → **New** → *Header Auth*.
2. **Name:** `Authorization`
3. **Value:** `Bearer SK_A_TE_DEEPSEEK_KULCSOD`
4. Mentsd `DeepSeek / OpenAI API key` néven, és rendeld az `AI – magyar feldolgozás` node-hoz.

#### Másik szolgáltató (OpenAI / Anthropic / Gemini)?
Az `AI – magyar feldolgozás` HTTP node-ban cseréld:

| Szolgáltató | URL | `model` mező |
|---|---|---|
| **DeepSeek** (alap) | `https://api.deepseek.com/chat/completions` | `deepseek-chat` |
| **OpenAI** | `https://api.openai.com/v1/chat/completions` | `gpt-4o` |
| OpenAI-kompatibilis egyéb | a szolgáltató végpontja | a saját modellnév |

A Header Auth ugyanúgy `Authorization: Bearer <kulcs>` mindháromnál.
(Anthropic Claude esetén más a body-séma — szólj, és átírom Claude-ra.)

### 4. Tesztelés (élesítés ELŐTT)
1. Nyisd meg a workflow-t, kattints **Execute Workflow**.
2. Nézd végig node-ról node-ra a kimenetet:
   - `RSS feed letöltése` → kapsz-e 200-at? (Ha 403: lásd Hibaelhárítás.)
   - `Új poszt szűrés` → kijön-e 1 elem?
   - `AI – magyar feldolgozás` → valid JSON-e a `choices[0].message.content`?
   - `.md fájl összeállítás` → nézd meg a `fileContent`-et, hogy jó-e a frontmatter.
3. Ha a `GitHub commit` lefut, nézd meg a repóban az új draft `.md`-t, és olvasd át.

### 5. Élesítés
Ha jó a minőség: kapcsold be a workflow-t (jobb fent **Active** kapcsoló). Ettől kezdve **óránként** fut. Futásonként **egy** új posztot dolgoz fel (hogy az első indításkor ne posztoljon be 10 cikket egyszerre).

---

## Hogyan működik (node-ról node-ra)

| # | Node | Mit csinál |
|---|---|---|
| 1 | **Óránkénti ütemezés** | Cron, óránként indít. |
| 2 | **RSS feed letöltése** | HTTP GET a feedre, `User-Agent` headerrel (a Ghost blog botokat blokkol header nélkül). |
| 3 | **XML → JSON** | Az RSS XML-t JSON-ná alakítja. |
| 4 | **Új poszt szűrés (dedup)** | A már látott `guid`-okat a workflow *static data*-ban tárolja; csak az új posztot engedi tovább, futásonként egyet. |
| 5 | **Meglévő posztok** | Lekéri a `conen-blog/src/content/blog/` fájllistát → ezekből lesznek a belső link-jelöltek. |
| 6 | **Slug lista összeállítás** | A meglévő slug-okat átadja az AI-nak. |
| 7 | **AI – magyar feldolgozás** | LLM-hívás: magyar feldolgozás + frontmatter mezők JSON-ban. |
| 8 | **.md fájl összeállítás** | Validálja a kategóriát, slugot képez, összerakja a `---` frontmattert + a body markdownt, `draft: true`. |
| 9 | **GitHub commit** | Létrehozza a `.md` fájlt a repóban (main branch). |
| 10 | **Guid mentése** | A sikeresen feldolgozott posztot megjelöli, hogy ne ismétlődjön. |

---

## Frontmatter, amit a workflow generál

A `conen-blog/src/content/config.ts` sémájához igazítva:

```yaml
---
title: "..."                 # magyar cím
summary: "..."               # max ~155 karakter, meta description
publishedAt: 2026-06-09      # a feldolgozás napja
category: "AI Ops"           # KIZÁRÓLAG: EAA | AX-readiness | AI Ops | Site Factory | MCP-Commerce | Case Study | CENTAUR
tags:
  - "..."
author: "Chris Conen"
readingTime: 6
draft: true                  # te állítod false-ra jóváhagyás után
---
```

> **Kategória-mapping:** a Pragmatic Engineer témái (szoftverfejlesztés, tech karrier, big tech) nem fedik tökéletesen a conen kategóriákat. Az AI alapból az **`AI Ops`** vagy **`CENTAUR`** kategóriát választja. Ha új kategóriát szeretnél (pl. „Engineering Culture"), azt előbb a `config.ts` enumba is fel kell venni, különben a build elhasal.

---

## Finomhangolás

- **Gyakoriság:** `Óránkénti ütemezés` node → állítsd pl. 6 órára vagy napi 1-re.
- **Több poszt egyszerre:** az `Új poszt szűrés` Code node-ban a `freshOnes[0]` helyett `return freshOnes.map(...)`-ra váltva több cikket is feldolgozhat (de a downstream node-ok ekkor több itemmel futnak — teszteld).
- **Hangnem / hossz / belső linkek száma:** az `AI – magyar feldolgozás` node `system` promptjában szerkeszthető.
- **Értesítés:** a `Guid mentése` után fűzhetsz egy e-mail/Slack node-ot („új draft kész: {{ $json.savedGuid }}").
- **Featured kép:** a séma `image` mezője opcionális; bővíthető egy kép-generáló/-kereső lépéssel.

---

## Hibaelhárítás

**`RSS feed letöltése` 403 Forbidden** — a Ghost blog néha botokat blokkol. Próbáld:
- másik `User-Agent` (valódi böngésző stringje),
- vagy a Substack feed: `https://newsletter.pragmaticengineer.com/feed`.

**Az AI válasza nem JSON** — a `.md fájl összeállítás` node hibát dob. A node tartalmaz egy fallbacket (kivágja a `{...}` részt), de ha makacs, emeld a prompt szigorát vagy válts erősebb modellre.

**A build elhasal a commit után** (`InvalidContentEntryFrontmatterError`) — szinte mindig rossz `category` érték. Ezért van a node-ban kategória-validáció `AI Ops` fallbackkel; ha bővíted az enumot, frissítsd a `VALID_CATEGORIES` listát a Code node-ban is.

**Duplikált posztok** — a dedup a workflow *static data*-ra épül. Ha újraimportálod a workflow-t, a static data nullázódhat; ekkor egyszer lefuthat egy már látott posztra.
