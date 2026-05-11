---
title: "PWA 2026: kell-e progresszív webalkalmazás a cégednek?"
summary: "A PWA telepíthető app-élményt ad natív app költsége nélkül. De nem mindenkinek éri meg. Mikor igen, mikor nem, és mi a valós fejlesztési költség."
publishedAt: 2026-03-15
category: "AI Ops"
tags: ["PWA", "progresszív webalkalmazás", "mobil", "app"]
author: "Chris Conen"
readingTime: 4
draft: false
---

## Mi az a PWA?

Progressive Web App: egy weboldal, ami **telepíthető** a telefon kezdőképernyőjére, offline is működik (részben), és push-értesítéseket küldhet. Kinézetre és viselkedésre natív app, technikailag weboldal.

## Mikor éri meg?

- **Visszatérő felhasználók**: ha az ügyfelek hetente többször látogatják az oldalt
- **Offline elérés kell**: katalógus, árjegyzék, dokumentáció
- **Push-értesítés**: akciók, foglalás-emlékeztető, tartalom-frissítés
- **Nincs app-store budget**: a PWA nem igényel Apple/Google fejlesztői fiókot

## Mikor NEM éri meg?

- **Egyszeri látogatók**: ha az ügyfél egyszer jön, egyszer rendel → nem fogja telepíteni
- **Egyszerű bemutatkozó oldal**: 5 oldal kontakt formmal nem igényel PWA-t
- **Hardver-hozzáférés kell**: kamera, Bluetooth, NFC → natív app kell

## A technikai minimum

1. **Service Worker**: a cache-stratégia és offline működés motorja
2. **Web App Manifest**: ikon, név, téma-szín, megjelenítési mód
3. **HTTPS**: kötelező (Cloudflare Pages automatikusan biztosítja)

## Költség

A PWA-funkcionalitás hozzáadása egy meglévő weboldalhoz: **+12% a projekt-költséghez**. Nem külön app — a meglévő oldal bővítése.

## Az alternatíva

Ha nem kell PWA, de az app-élmény fontos: a **„Hozzáadás a kezdőképernyőhöz"** prompt (Add to Home Screen) egyszerűbb megoldás. Nincs offline, nincs push — de az ikon ott van a telefonon.
