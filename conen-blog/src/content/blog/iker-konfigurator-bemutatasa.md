---
title: "Az IKER konfigurátor: hogyan tervezz weboldalt két verzióban, egyszerre"
summary: "10 lépés, élő preview, variant-compare, three-axis scoring. Az IKER nem űrlap — hanem sales-tool, amit a CENTAUR-modell épített. Bemutatjuk, hogyan működik."
publishedAt: 2026-05-10
category: "CENTAUR"
tags: ["IKER", "konfigurátor", "variant-compare", "weboldal tervezés"]
image: "/blog/blog-images/weboldal-tervezo-webaruhaz-keszito.webp"
imageAlt: "weboldal tervező és webáruház készítő alkalmazás"
author: "Chris Conen"
readingTime: 5
draft: false
---

## Nem űrlap. Sales-tool.

A legtöbb webfejlesztő cég weboldalán ugyanaz a flow vár.

„Kérjen ajánlatot.”

Név. Email. Telefonszám. Rövid leírás.

Aztán csend.

1-2 nap múlva érkezik egy PDF, gyakran egyetlen összeggel, pár technikai bulletpointtal és egy homályos időbecsléssel. A folyamat mögött szinte mindig ugyanaz a logika működik: az ügyfél próbálja szavakban elmagyarázni azt, amit valójában vizuálisan és interaktívan szeretne megérteni.

A probléma nem az, hogy ez lassú.

Hanem az, hogy 2026-ban még mindig úgy tervezünk digitális élményeket, mintha statikus nyomdai anyagokat gyártanánk.

A weboldal azonban nem PDF.

Nem screenshot.

Nem mockup.

Hanem élő rendszer.

Az IKER pontosan ezt próbálja újragondolni.

## Az IKER nem konfigurátor. Hanem döntési rendszer.

Az IKER-t sokan első pillantásra weboldal-konfigurátornak nevezik.

Technikailag valóban az.

De a valóságban sokkal közelebb áll egy interaktív sales-operációs rendszerhez.

Mert nem egyszerűen opciókat listáz.

Hanem döntési helyzeteket teremt.

A legtöbb configurator úgy működik, mint egy webshop:

* checkboxok
* dropdownok
* opciók
* összegzés

Az IKER más filozófiára épül.

A cél nem az, hogy a felhasználó „kitöltse”.

Hanem az, hogy:

> lássa, összehasonlítsa és megértse a saját jövőjét.

Ezért született meg a variant-compare rendszer.

És ezért lett az egész platform preview-first architektúrára építve.

## A weboldal-tervezés legnagyobb problémája

A legtöbb ügyfél nem tud wireframe-ben gondolkodni.

Nem tudja elképzelni, hogy:

* milyen lesz a spacing
* hogyan mozog majd a navigáció
* milyen érzés lesz a hero-szekció
* hogyan változik a hangulat egy másik typography-val
* mennyit számít egy sticky header
* milyen UX-érzetet ad egy split layout

És ez teljesen természetes.

A legtöbb ember nem frontendes.

Nem designer.

Nem UX researcher.

Ezért az iparág évtizedeken át mockupokra épített.

A gond az, hogy a mockup nem viselkedik.

Nem mozog.

Nem reagál.

Nem él.

A web viszont igen.

Az IKER ebből a felismerésből született.

## A 10 lépés — de valójában nem form flow

Papíron az IKER egy 10 lépéses rendszer.

Valójában azonban ez nem wizard.

Hanem fokozatos scope-building engine.

Minden döntés vizuális következménnyel jár.

Minden interakció azonnali preview-változást okoz.

És minden választás közelebb visz egy valódi, technikailag értelmezhető projektscope-hoz.

## 1. Típus

Az első lépés nem template-választás.

Hanem üzleti modell választás.

Bemutatkozó oldal?

Leadgeneráló rendszer?

Foglalós platform?

SaaS?

Webáruház?

A választás nem csak layoutot változtat.

Hanem teljes komponenslogikát.

Egy webáruház-preview automatikusan:

* termékrácsot
* testimonialokat
* checkout-flow elemeket
* kategória-szekciókat

kap.

Míg egy SaaS oldal:

* pricing-táblát
* statisztikákat
* comparison blockokat
* onboarding CTA-kat

jelenít meg.

Ez nem skin-csere.

Hanem struktúra-váltás.

## 2. Stílus

A legtöbb builder itt megáll a „válassz színt” szinten.

Az IKER-ben a stílus-layer teljes preview-rendszert vezérel.

10 színvilág.

6 tipográfia.

Lekerekítés-intenzitás.

És minden hover valós idejű morph-transitionnel jelenik meg.

Nem kell alkalmazni a stílust ahhoz, hogy lásd.

Egyszerűen föléviszed az egeret.

És a teljes site átalakul.

Ez fontos UX-különbség.

Mert a döntés így nem absztrakt.

Hanem érzékszervi.

## 3–4. Navigáció és Hero

Itt válik igazán láthatóvá az IKER cinematic engine-je.

A legtöbb configurator egyszerűen reloadolja a preview-t.

Az IKER viszont View Transitions API-ra és animációs state-managementre épül.

Ha sticky header-ről transparent header-re váltasz:

* a navigáció kimorf-ol
* a layout újrapozicionálódik
* a spacing alkalmazkodik
* a hero új ritmust kap

Ez nem UI gimmick.

Hanem sales-pszichológia.

Az ügyfél nem „beállítást” lát.

Hanem élményt.

## A killer feature: variant-compare

Ez az a pont, ahol az IKER teljesen kilép a klasszikus website builder kategóriából.

A variant-compare mód lényege:

> két élő verzió egyszerre.

Bal oldalon sticky header + centered hero.

Jobb oldalon hamburger navigation + split hero.

Középen egy draggable elválasztó.

És az ügyfél valós időben hasonlíthatja össze a két irányt.

Ez elképesztően fontos különbség.

A legtöbb rendszer időben egymás után mutat alternatívákat.

Az IKER térben mutatja őket.

Ez sokkal gyorsabb emberi döntéshozatalt tesz lehetővé.

Az agy ugyanis összehasonlításban gondolkodik.

Nem memóriából rekonstruál.

## Nem A/B teszt. Hanem pre-decision architecture.

A variant-compare nem marketing gimmick.

Hanem egy teljesen új sales-modell alapja.

A klasszikus A/B tesztelés:

* utólagos
* adat-alapú
* lassú
* production környezetet igényel

Az IKER ezzel szemben:

* döntés előtti
* vizuális
* azonnali
* konverzáció-alapú

A user nem statisztikát néz.

Hanem jövőket hasonlít össze.

És ez pszichológiailag sokkal erősebb.

## Oldalak és szekciók — a modularitás új szintje

Az IKER nem page-builder.

Hanem komponens-orchestrator.

A rendszer jelenleg:

* 11 szekciótípust
* per-page konfigurációt
* inline finomhangolást
* layout-axis kontrollt

támogat.

Például egy galéria-szekciónál:

* oszlopszám
* spacing
* shadow
* hover-intenzitás
* border radius
* képarány
* caption-stílus

mind valós időben módosítható.

A cél nem a pixel-perfect design editor.

Hanem a gyors scope-kristályosítás.

## Funkciók és extrák — transzparens scope

A legtöbb ügynökségi ajánlat legnagyobb problémája:

az ügyfél nem tudja pontosan, mi miért kerül pénzbe.

Az IKER egyik legfontosabb filozófiája ezért a transzparencia.

Minden funkció explicit.

Például:

* többnyelvűség
* EAA-megfelelés
* CRM-integráció
* AI chatbot
* analytics
* PWA
* Core Web Vitals optimization
* MCP endpoint
* AX readiness

mind külön scope-elemként jelenik meg.

Nem rejtett költségként.

Ez két dolgot változtat meg:

1. Az ügyfél jobban érti a projektet
2. A sales-beszélgetés sokkal magasabb szintre kerül

## Three-axis scoring

A legtöbb configurator végén egy ár jelenik meg.

Az IKER végén három stratégiai scoring-rendszer jelenik meg.

## EAA Score

Mennyire akadálymentes a scope?

Mennyire áll közel a WCAG és EAA megfeleléshez?

## AX Score

Mennyire AI-kompatibilis a rendszer?

Támogatja-e a machine-readable struktúrát?

Agent-friendly flowkat?

Structured contentot?

## CENTAUR Score

Mennyire alkalmas AI-human collaborative operationre?

Mennyire automatizálható?

Mennyire jövőálló?

Ez a három scoring-rendszer már nem egyszerű weboldal-logika.

Hanem digitális infrastruktúra-logika.

## Nem quote generator. Hanem sales acceleration engine.

Az IKER egyik legérdekesebb hatása nem technológiai.

Hanem operációs.

A legtöbb ügynökségi sales-flow rendkívül lassú.

* discovery call
* brief
* utánkövetés
* ajánlat
* módosítás
* új ajánlat

Az IKER ezt a folyamatot radikálisan lerövidíti.

Mert az ügyfél már úgy érkezik diagnosztikára, hogy:

* látott alternatívákat
* hozott döntéseket
* megértette a scope-ot
* érzékeli a technikai komplexitást

A beszélgetés így nem nulláról indul.

Hanem egy közösen látható vászonról.

## CENTAUR-modell — ember + AI co-founder architektúra

Az IKER maga is a CENTAUR-modell terméke.

A fejlesztés során:

* stratégiai layer
* implementációs layer
* AI orchestration layer
* human review layer

egyszerre működött.

A rendszer architektúráját AI-assisted planning támogatta.

A positioning AI-human collaborative iterációban alakult.

A UX-flowkat több modell validálta.

Ez fontos.

Mert az IKER nem csak egy AI-val készült projekt.

Hanem egy AI-native működési modell demonstrációja.

## A jövő: MCP és AI-to-business interfészek

Az IKER roadmapjének legfontosabb eleme a saját MCP endpoint.

Ez gyakorlatilag azt jelenti majd, hogy:

egy AI-asszisztens közvetlenül tud weboldal-scope-ot generálni.

Például:

* ChatGPT
* Claude
* Gemini
* Perplexity

vagy bármilyen agentic rendszer.

Ez a scope pedig közvetlenül beérkezhet diagnosztikára.

Ez nem egyszerű integráció.

Hanem egy teljesen új internetes interaction model.

A jövőben ugyanis nem csak emberek fognak weboldalakat rendelni.

Hanem AI-agentek is.

Az IKER erre készül.

## Nem a jövő. Hanem a következő logikus lépés.

A weboldal-iparág hosszú ideig statikus prezentációs logikára épült.

Mockupok.

PDF-ek.

Screenshotok.

Lassú ajánlatkérések.

Az IKER ebből próbál kilépni.

Nem azért, mert „AI”.

Nem azért, mert „cinematic”.

Hanem mert a modern web már nem statikus objektum.

Hanem élő rendszer.

És élő rendszereket élő módon kell tervezni.

Az IKER ezért nem űrlap.

Nem quote builder.

Nem page editor.

Hanem egy új típusú sales-tool.

Egy rendszer, amelyben a döntés nem egy PDF végén történik meg.

Hanem valós időben.

A saját szemed előtt.

És valószínűleg ez az irány, amerre a teljes digitális sales-iparág el fog indulni a következő években.

