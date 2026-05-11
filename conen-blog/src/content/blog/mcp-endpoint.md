---
title: "MCP endpoint: a következő generációs weboldal-integráció"
summary: "Az MCP (Model Context Protocol) lehetővé teszi, hogy az AI-asszisztensek közvetlenül tranzakciókat hajtsanak végre a weboldaladon. Nem sci-fi — ez 2026 valósága."
publishedAt: 2026-04-15
category: "AI Ops"
tags: ["MCP", "API", "AI integráció", "Claude", "automatizáció"]
author: "Chris Conen"
readingTime: 5
draft: false
---

## Mi az MCP?

Model Context Protocol — az Anthropic által fejlesztett nyílt protokoll, ami lehetővé teszi, hogy AI-modellek (Claude, és más kompatibilis rendszerek) **strukturáltan kommunikáljanak** külső szolgáltatásokkal.

Gyakorlatban: a felhasználó megkérdezi az AI-asszisztenst „Foglalj nekem időpontot a Kovács Klinikára csütörtökre", és az AI az MCP endpoint-on keresztül **ténylegesen lefoglalja** az időpontot.

## Miért fontos ez egy weboldalnak?

Mert az AI-asszisztensek (Claude, ChatGPT, Perplexity) egyre többet „csinálnak", nem csak válaszolnak. Ha a te weboldalad MCP-endpointot kínál:

- **Foglalás**: AI-n keresztül is foglalhatók időpontok
- **Ajánlatkérés**: az AI kitölti és beküldi a formot a felhasználó nevében
- **Termékkereső**: az AI végignézi a katalógusodat és ajánl

## Hogyan működik technikailag?

Egy Cloudflare Worker (vagy más edge-function) kap egy `/mcp` endpointot. Ez JSON-RPC-vel kommunikál:

1. Az AI elküldi a **tool-call kérést** (pl. `create_booking`)
2. A Worker validálja, végrehajtja (API-hívás a foglalórendszerhez)
3. Visszaküldi az eredményt JSON-ben

A biztonság: API key + rate limiting + CORS. Nem nyitott kapu — hanem kontrollált interfész.

## Kinek éri meg?

- **Szolgáltató cégek**: foglalás, ajánlatkérés, konzultáció
- **E-commerce**: termékkereső, rendelés-státusz
- **B2B SaaS**: demo-foglalás, onboarding

## Mi kell hozzá?

Az MCP endpoint havi díjas szolgáltatás (#service-ai-ops). A build-költségen felül, külön szerződéssel. Az alap: 250.000 Ft/hó-tól, ami tartalmazza a hosting-ot, monitoringot, és a frissítéseket.
