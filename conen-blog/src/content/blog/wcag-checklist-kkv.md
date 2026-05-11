---
title: "WCAG 2.2 AA checklist: 12 pont amit most ellenőrizz a weboldaladon"
summary: "Nem kell akadálymentesítési szakértőnek lenned. Ez a 12 pontos vizuális checklist megmutatja, hol állsz — böngészőből, 10 perc alatt."
publishedAt: 2026-05-07
category: "EAA"
tags: ["WCAG", "checklist", "akadálymentesítés", "önaudit"]
author: "Chris Conen"
readingTime: 7
draft: false
---

A WCAG 2.2 AA szint az EAA jogszabályi minimum. Mielőtt szakértőt hívnál, nézd végig ezt a 12 pontot.

## 1. Kontraszt-arány

Nyisd meg a Chrome DevTools-t (F12), válaszd az Elements panelt, kattints egy szövegre. A Styles szekcióban a `color` mellett megjelenik a kontraszt-arány. **Min. 4.5:1 kell normál szövegre, 3:1 nagy szövegre.**

## 2. Tab-navigáció

Nyomj Tab-ot az oldalon. Minden gombot, linket, űrlapmezőt el tudsz érni? A fókusz-jelölés látható? Ha nem — probléma.

## 3. Alt szövegek

Jobb klikk → Vizsgálat minden képen. Van `alt` attribútum? Értelmes-e? A dekoratív képeknél `alt=""` kell (üres, de létezik).

## 4. Heading hierarchia

Nincs h1 → h3 ugrás. A struktúra: h1 → h2 → h3. Egy oldalon egy h1. A DevTools-ban `document.querySelectorAll('h1,h2,h3,h4')` megmutatja.

## 5. Űrlap-hibák

Töltsd ki rosszul a kontakt formot. A hibajelzés **szöveges**? Vagy csak a mező pirosra vált? A szín önmagában nem elég — szöveg kell.

## 6. Link-szövegek

Van „kattints ide" link? Az nem jó. A link szövege önmagában értelmes kell legyen: „Szolgáltatásaink megtekintése" > „kattints ide".

## 7. Mobil zoom

Csíptet zoom-mal 200%-ra nagyítod. Minden olvasható? Semmi nem vágódik le? A `maximum-scale=1` meta tag tiltja a zoom-ot — az EAA-ban nem megengedett.

## 8. Videó feliratok

Ha van videó az oldalon: van felirat? Ha nincs — az EAA-ban kötelező.

## 9. Animációk

Gyors villogás (3/s felett) epilepszia-kockázat. A `prefers-reduced-motion` CSS media query-t támogatod?

## 10. Nyelv-attribútum

Az `<html lang="hu">` tag van? Ez alapvető — a képernyőolvasó ebből tudja, milyen nyelven olvassa.

## 11. Aria-live régiók

Dinamikus tartalom (toast üzenetek, AJAX-frissítések) `aria-live="polite"` attribútummal kell jelölni.

## 12. Skip-link

Az oldal tetején van rejtett „Ugrás a fő tartalomra" link? Keyboard-user-eknek ez az első dolog.

---

**Hány pontot teljesítesz?** Ha 8 alatti: sürgős az audit. Ha 8-10: néhány javítás kell. 11-12: jó úton jársz.
