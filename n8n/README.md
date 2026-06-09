# Pragmatic Engineer → Conen Blog automatizáció (n8n)

Ez a workflow figyeli a [The Pragmatic Engineer](https://blog.pragmaticengineer.com/) blog RSS feedjét, és amikor új poszt jelenik meg, **egy AI-modellel magyar nyelvű, eredeti feldolgozást** készít belőle (forrásmegjelöléssel, belső linkekkel, SEO-frontmatterrel), draftként commitolja, majd **Telegramon jóváhagyásra küldi**. A te döntésed alapján:
- **Jóváhagyás** → a poszt `draft: false`-ra vált és kimegy az élő blogra,
- **Elutasítás** → a draft fájl törlődik a repóból.

A publikálás `git commit` egy `.md` fájllal a `conen-blog/src/content/blog/` mappába → Cloudflare Pages buildeli.

### Folyamat-áttekintés

```
RSS → új poszt? → AI magyar feldolgozás → GitHub draft commit
   → 📱 Telegram jóváhagyás (Jóváhagyom / Elutasítom)
        ├─ Jóváhagyom → GitHub edit (draft:false) → 📱 "Publikálva" → blog élő
        └─ Elutasítom → GitHub delete (draft törlése) → 📱 "Elutasítva"
```

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

### 3. Jóváhagyás-alapú publikálás (human-in-the-loop)
A workflow **nem** publikál automatikusan. Minden cikk először `draft: true`-ként commitolódik, és **Telegramon kapsz egy üzenetet két gombbal** (Jóváhagyom / Elutasítom). Csak a Te jóváhagyásod után vált `draft: false`-ra és kerül ki élesben. Elutasításnál a draft fájl törlődik. Így a Groq+Llama kimenetét mindig ellenőrzöd, mielőtt bármi élesedik.

---

## Telepítés

### Előfeltételek
- Self-hosted n8n (Docker) **vagy** n8n Cloud — nálad mindkettő szinkronban (hub.centaur-lang.dev).
- Egy LLM API kulcs. Alapból **Groq + Llama 3.3 70B** (`api.groq.com`, `llama-3.3-70b-versatile` – ingyenes tier, OpenAI-kompatibilis). Bármilyen OpenAI-kompatibilis végpontra átállítható (lásd lent).
- Egy **GitHub Personal Access Token** a `chrisconen/conendigital` repóhoz (`repo` / `Contents: Read and write` jog).
- Egy **Telegram bot token** (@BotFather) és a saját **chat ID**-d a jóváhagyó üzenetekhez.

### 1. Workflow importálása
n8n UI → bal felső menü → **Import from File** → válaszd a
`n8n/pragmatic-engineer-to-conen.workflow.json` fájlt.

### 2. GitHub credential
1. n8n → **Credentials** → **New** → *GitHub API*.
2. Server: `https://api.github.com` (vagy a GitHub Enterprise URL-ed).
3. Access Token: a PAT-od.
4. Mentsd `GitHub – conendigital` néven.
5. A workflow **négy** GitHub node-jánál (`Meglévő posztok`, `GitHub commit`, `GitHub publikálás`, `GitHub draft törlése`) válaszd ki ezt a credentialt.

> A JSON-ben `REPLACE_GITHUB_CRED_ID` helyőrző van — import után egyszerűen kattints minden GitHub node-ra és válaszd ki a credentialt a legördülőből.

### 2/b. Telegram credential
1. **Bot létrehozása:** Telegramban írj a [@BotFather](https://t.me/BotFather)-nek → `/newbot` → kapsz egy **bot tokent** (`123456:ABC...`).
2. **Chat ID megszerzése:** írj egy üzenetet a saját botodnak, majd nyisd meg böngészőben:
   `https://api.telegram.org/bot<BOT_TOKEN>/getUpdates` → a `chat.id` mező a te chat ID-d (pozitív szám privát chatnél).
3. n8n → **Credentials** → **New** → *Telegram API* → illeszd be a bot tokent → mentsd `Telegram – Conen bot` néven.
4. A három Telegram node-on (`Telegram jóváhagyás`, `Telegram: publikálva`, `Telegram: elutasítva`) válaszd ki ezt a credentialt, és a **`chatId` mezőbe** írd be a saját chat ID-d (a JSON-ben `REPLACE_CHAT_ID` helyőrző van mindháromban).

> **⚠️ WEBHOOK_URL (self-hosted!):** a „Telegram jóváhagyás" (Send and Wait) node a folyamatot megállítja, és egy webhook-linken keresztül folytatja, amikor a gombra kattintasz. Ehhez a self-hosted n8n-nek tudnia kell a **publikus URL-jét**. Állítsd be a Docker környezeti változót:
> ```
> WEBHOOK_URL=https://hub.centaur-lang.dev/
> ```
> Enélkül a gombok „Invalid token" hibát adnak, vagy a workflow nem folytatódik.

### 3. LLM credential (Groq + Llama 3.3 alapból)
1. n8n → **Credentials** → **New** → *Header Auth*.
2. **Name:** `Authorization`
3. **Value:** `Bearer gsk_A_TE_GROQ_KULCSOD`
4. Mentsd `Groq API key` néven, és rendeld az `AI – magyar feldolgozás` node-hoz.

> Groq ingyenes kulcsot a [console.groq.com](https://console.groq.com) → API Keys alatt kapsz.

#### Másik szolgáltató (DeepSeek / OpenAI / Anthropic)?
Az `AI – magyar feldolgozás` HTTP node-ban cseréld:

| Szolgáltató | URL | `model` mező |
|---|---|---|
| **Groq** (alap) | `https://api.groq.com/openai/v1/chat/completions` | `llama-3.3-70b-versatile` |
| DeepSeek | `https://api.deepseek.com/chat/completions` | `deepseek-chat` |
| OpenAI | `https://api.openai.com/v1/chat/completions` | `gpt-4o` |

A Header Auth mindegyiknél `Authorization: Bearer <kulcs>`.
(Anthropic Claude esetén más a body-séma — szólj, és átírom Claude-ra.)

### 4. Tesztelés (élesítés ELŐTT)
1. Nyisd meg a workflow-t, kattints **Execute Workflow**.
2. Nézd végig node-ról node-ra a kimenetet:
   - `RSS feed letöltése` → kapsz-e 200-at? (Ha 403: lásd Hibaelhárítás.)
   - `Új poszt szűrés` → kijön-e 1 elem?
   - `AI – magyar feldolgozás` → valid JSON-e a `choices[0].message.content`?
   - `.md fájl összeállítás` → nézd meg a `fileContent`-et, hogy jó-e a frontmatter.
   - `GitHub commit` → létrejön a draft `.md`.
   - `Telegram jóváhagyás` → megkapod-e az üzenetet a két gombbal? Kattints **Jóváhagyom** → a `GitHub publikálás` átírja `draft: false`-ra és jön a „Publikálva" üzenet. Vagy **Elutasítom** → a draft törlődik.
3. Ellenőrizd a repóban / az élő blogon (`https://conendigital.hu/blog/<slug>`) az eredményt.

### 5. Élesítés
Ha jó a minőség: kapcsold be a workflow-t (jobb fent **Active** kapcsoló). Ettől kezdve **óránként** fut. Futásonként **egy** új posztot dolgoz fel (hogy az első indításkor ne posztoljon be 10 cikket egyszerre). Minden poszt a Telegram-jóváhagyáson megy keresztül, mielőtt élesedne.

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
| 8 | **.md fájl összeállítás** | Validálja a kategóriát, slugot képez, összerakja a frontmattert + body markdownt. Két verziót gyárt: `fileContent` (draft:true) és `fileContentPublished` (draft:false). |
| 9 | **GitHub commit (draft .md)** | Létrehozza a draft `.md` fájlt a repóban (main branch). |
| 10 | **Telegram jóváhagyás** | „Send and Wait": elküldi a cím/kategória/összefoglaló + GitHub-link üzenetet két gombbal, és **megállítja a workflow-t**, amíg nem döntesz. |
| 11 | **Jóváhagyva?** | IF node: `{{ $json.data.approved }}` alapján ágazik. |
| 12 | **GitHub publikálás (draft:false)** | (Jóváhagyás ág) felülírja a fájlt `draft: false`-ra → a poszt élesedik. |
| 13 | **Telegram: publikálva** | Visszajelzés a live URL-lel. |
| 14 | **GitHub draft törlése** | (Elutasítás ág) törli a draft fájlt a repóból. |
| 15 | **Telegram: elutasítva** | Visszajelzés az elutasításról. |
| 16 | **Guid mentése** | A feldolgozott posztot megjelöli (mindkét ág után), hogy ne ismétlődjön. |

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
- **Hangnem / hossz / belső linkek száma:** az `AI – magyar feldolgozás` node `system` promptjában szerkeszthető (a `Slug lista összeállítás` Code node-ban).
- **Jóváhagyás kihagyása (full-auto):** ha mégis automata publikálást akarsz, töröld a `Telegram jóváhagyás` + `Jóváhagyva?` node-okat, és a `GitHub commit`-ban a `fileContent` helyett a `fileContentPublished` mezőt használd (vagy kösd közvetlenül a `GitHub publikálás`-t). **Nem ajánlott**, amíg a minőség nem stabil.
- **Featured kép:** a séma `image` mezője opcionális; bővíthető egy kép-generáló/-kereső lépéssel.

---

## Hibaelhárítás

**`RSS feed letöltése` 403 Forbidden** — a Ghost blog néha botokat blokkol. Próbáld:
- másik `User-Agent` (valódi böngésző stringje),
- vagy a Substack feed: `https://newsletter.pragmaticengineer.com/feed`.

**Az AI válasza nem JSON** — a `.md fájl összeállítás` node hibát dob. A node tartalmaz egy fallbacket (kivágja a `{...}` részt), de ha makacs, emeld a prompt szigorát vagy válts erősebb modellre.

**Groq rate limit (429)** — az ingyenes tieren van perc-/napi tokenkorlát. Mivel a workflow futásonként csak 1 posztot dolgoz fel, ez ritkán üt be; ha mégis, ritkítsd az ütemezést, vagy tedd be egy „Wait" node-ot retmyval. A `llama-3.3-70b-versatile` támogatja a JSON módot, és a prompt tartalmazza a „JSON" szót (ezt a Groq megköveteli a `response_format`-hoz).

**A build elhasal a commit után** (`InvalidContentEntryFrontmatterError`) — szinte mindig rossz `category` érték. Ezért van a node-ban kategória-validáció `AI Ops` fallbackkel; ha bővíted az enumot, frissítsd a `VALID_CATEGORIES` listát a Code node-ban is.

**Duplikált posztok** — a dedup a workflow *static data*-ra épül. Ha újraimportálod a workflow-t, a static data nullázódhat; ekkor egyszer lefuthat egy már látott posztra.

**Telegram gombok nem működnek / „Invalid token" / a workflow nem folytatódik** — szinte mindig a `WEBHOOK_URL` hiányzik vagy rossz a self-hosted n8n-en. Állítsd be: `WEBHOOK_URL=https://hub.centaur-lang.dev/` és indítsd újra a konténert. Ellenőrizd azt is, hogy a `chatId` mindhárom Telegram node-on a saját chat ID-d.

**Nem jön a Telegram üzenet** — a botnak előbb írnod kell egyszer (a bot nem tud elsőként üzenetet küldeni ismeretlen chatnek), és a `chatId`-nak helyesnek kell lennie (lásd `getUpdates`).

**`GitHub publikálás` hibázik** — az `edit` művelet meglévő fájlt frissít; ha a draft commit valamiért nem jött létre, nincs mit szerkeszteni. Előbb a `GitHub commit`-nak le kell futnia.
