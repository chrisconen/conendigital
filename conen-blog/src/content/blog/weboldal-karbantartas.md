---
title: "Weboldal karbantartás: mennyibe kerül, és mit tartalmaz 2026-ban"
summary: "A weboldal nem egyszeri projekt — élő rendszer. A biztonsági frissítések, a tartalom-aktualizálás, és a teljesítmény-monitoring mind folyamatos karbantartást igényel."
publishedAt: 2026-03-18
category: "Site Factory"
tags: ["weboldal karbantartás", "biztonság", "frissítések", "monitoring"]
author: "Chris Conen"
readingTime: 4
draft: false
---

## Miért kell karbantartás?

### Biztonság
WordPress: havonta 3-5 plugin-frissítés, amelyek biztonsági javításokat tartalmaznak. Ha nem frissítesz → az oldal sebezhető. A 2025-ös évben a WordPress oldalak **43%-át érte biztonsági incidens** elavult pluginek miatt.

### Teljesítmény
Az oldalsebesség idővel romlik: új tartalom, nagyobb képek, elavuló cache-beállítások. Negyedéves PageSpeed-audit kell a szinten tartáshoz.

### Tartalom
Elavult információk (régi árak, megszűnt szolgáltatások, rossz telefonszám) rombolják a hitelességet. Havi tartalom-ellenőrzés minimum.

### Jogi megfelelés
Az EAA-konformitás nem egyszeri feladat — új tartalom hozzáadásakor az akadálymentességet is ellenőrizni kell.

## A mi karbantartási modellek

### Statikus oldal (Astro/Cloudflare)

| Tétel | Gyakoriság | Ár |
|---|---|---|
| Tartalom-frissítés | Igény szerint | 15k Ft/alkalom |
| PageSpeed audit | Negyedéves | Díjmentes |
| SSL/DNS monitoring | Folyamatos | Díjmentes |
| Éves felülvizsgálat | Éves | 50k Ft |

**Miért olcsó?** Mert nincs plugin, nincs adatbázis, nincs szerver-frissítés. A statikus oldal karbantartási igénye minimális.

### WordPress oldal

| Tétel | Gyakoriság | Ár |
|---|---|---|
| Plugin frissítés | Havi | 25k Ft/hó |
| Biztonsági monitoring | Folyamatos | Benne |
| Backup | Heti | Benne |
| Tartalom-frissítés | Igény szerint | 15k Ft/alkalom |

## A tanulság

A stack-választás a karbantartási költséget is meghatározza. Egy Astro oldal éves karbantartása **töredéke** egy WordPress oldalénak.
