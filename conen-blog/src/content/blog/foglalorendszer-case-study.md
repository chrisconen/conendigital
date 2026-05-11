---
title: "Foglalórendszer integráció: hogyan automatizáltuk egy klinika időpontfoglalását"
summary: "Heti 40 telefonhívás → heti 5. A többi online jön, automatikusan, SMS-emlékeztetővel. Egy fogászati klinika digitális átállásának története."
publishedAt: 2026-03-22
category: "Case Study"
tags: ["foglalórendszer", "automatizáció", "klinika", "case study"]
author: "Chris Conen"
readingTime: 4
draft: false
---

## A probléma

Egy budapesti fogászati klinika (3 orvos, 2 asszisztens) heti 60-80 telefonhívást kapott időpont-foglalásra. Az asszisztens idejének 60%-a telefonálásra ment, nem betegek fogadására.

## A megoldás

### Online foglalás

Egyedi foglalórendszer a weboldalon: a páciens kiválasztja az orvost, a kezelés típusát, és a szabad időpontok közül választ. A rendszer **valós időben szinkronizál** a klinika naptárával.

### SMS-emlékeztető

Automatikus SMS 24 órával a foglalás előtt + 1 órával előtte. A no-show ráta **35%-ról 8%-ra csökkent**.

### Admin felület

Az orvosok egyszerű felületen kezelik a naptárukat: szabadság, egyedi időpontok, kezelés-típusonkénti időtartam.

## Az eredmény

| Metrika | Előtte | Utána |
|---|---|---|
| Heti telefonhívás | 60-80 | 12-15 |
| Online foglalás aránya | 0% | 78% |
| No-show ráta | 35% | 8% |
| Asszisztens terhelés | 60% telefonra | 15% adminra |

**A befektetés 4 hónap alatt megtérült** — az asszisztens időmegtakarítása és a csökkent no-show önmagában fedezi.

## A tech stack

- Astro frontend, EAA-konform
- Cloudflare Workers API (foglalás-kezelés)
- Google Calendar szinkronizáció
- Twilio SMS (emlékeztető)
- Formspree fallback (ha az online rendszer nem elérhető)
