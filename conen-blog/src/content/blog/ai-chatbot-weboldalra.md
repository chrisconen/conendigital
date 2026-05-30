---
title: "AI chatbot a weboldalon: mikor éri meg, mennyibe kerül, hogyan működik"
summary: "Claude vagy GPT-alapú chatbot a weboldaladon — nem gadget, hanem sales-eszköz. De nem mindenkinek kell. Mikor igen, mikor nem, és mennyi a valós költsége."
publishedAt: 2026-03-28
category: "AI Ops"
tags: ["AI chatbot", "Claude", "GPT", "ügyfélszolgálat", "automatizáció"]
author: "Chris Conen"
readingTime: 5
draft: false
---

## Mikor éri meg?

- **Magas ügyfélszolgálati terhelés**: napi 20+ ismétlődő kérdés (nyitvatartás, árak, szolgáltatások)
- **Lead-kvalifikáció**: a chatbot előszűri a kérdéseket, és csak a kvalifikáltakat adja a sales-nek
- **24/7 elérhetőség**: éjjel-nappal válaszol, hétvégén is
- **Többnyelvűség**: angol/német ügyfélszolgálat emberi erőforrás nélkül

## Mikor NEM éri meg?

- **Havi 100 alatti látogató**: a chatbot nem generál forgalmat, csak kiszolgálja
- **Komplex szaktanácsadás**: ügyvédi, orvosi kérdésekre az AI nem adhat konkrét tanácsot
- **Nincs tartalom**: ha az AI-nak nincs miből válaszolnia (üres GYIK, kevés szolgáltatás-leírás)

## Hogyan működik technikailag?

1. A chatbot a **weboldalad tartalmából** tanul — nem a teljes internetből. A GYIK, szolgáltatások, árak, kontakt-információk a tudásbázis.
2. RAG (Retrieval-Augmented Generation): a kérdéshez a releváns tartalom-darabot kéri le, és abból generál választ.
3. **Guardrails**: nem válaszol a témán kívül, nem ad árajánlatot, nem köt szerződést. Amire nincs felhatalmazása → „Kérem, forduljon ügyfélszolgálatunkhoz."

## Mennyibe kerül?

**Build**: a chatbot integrálása a weboldalra: egyedi scope alapján.

**Havi díj**: egyedi ajánlat szerint (#service-ai-ops). Ez tartalmazza a Claude/GPT API költséget, a hosting-ot, a monitoring-ot, és a tartalom-frissítéseket.

## Claude vs GPT

| | Claude (Anthropic) | GPT (OpenAI) |
|---|---|---|
| Biztonság | Constitutional AI, kevesebb halluciáció | RLHF, széles tudásbázis |
| Kontextus | 200k token (teljes weboldal) | 128k token |
| Stílus | Óvatos, pontos | Kreatív, bőbeszédű |
| Ár | Hasonló | Hasonló |

Mi **Claude-ot ajánljuk** — mert a mi CTO-nk is Claude.
