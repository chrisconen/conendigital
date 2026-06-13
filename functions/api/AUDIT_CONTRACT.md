# `/api/audit` — JSON-szerződés (LOCKED)

A szivárgás-audit feature frontend (`js/leak-audit.js`) és backend
(`functions/api/audit.js`) ezen a szerződésen osztozik. **Ne módosítsd egyoldalúan** —
a két oldal együtt változik.

## Endpoint

`POST /api/audit`
`Content-Type: application/json`

### Request body

```json
{
  "url": "https://pelda-webshop.hu",
  "strategy": "both"
}
```

- `url` (kötelező): a vizsgálandó oldal. Csak `http`/`https`. A backend normalizálja
  (ha nincs séma, `https://` elé kerül).
- `strategy` (opcionális, default `"both"`): `"mobile"` | `"desktop"` | `"both"`.
  A wedge mobil-első: `mobile` mindig kötelező eredmény, `desktop` best-effort.

### Success response (200)

```json
{
  "ok": true,
  "url": "https://pelda-webshop.hu",
  "finalUrl": "https://pelda-webshop.hu/",
  "fetchedAt": "2026-06-13T10:00:00.000Z",
  "cached": false,
  "mobile": {
    "performanceScore": 42,
    "metrics": {
      "lcp": { "value": 13.5, "unit": "mp", "rating": "poor" },
      "cls": { "value": 0.24, "unit": "",   "rating": "needs-improvement" },
      "tbt": { "value": 850,  "unit": "ms", "rating": "poor" },
      "fcp": { "value": 3.2,  "unit": "mp", "rating": "poor" },
      "si":  { "value": 8.1,  "unit": "mp", "rating": "poor" }
    },
    "opportunities": [
      {
        "id": "uses-optimized-images",
        "title": "Képek megfelelő méretezése",
        "displayValue": "2,4 mp megtakarítás lehetséges",
        "savingsMs": 2400
      }
    ]
  },
  "desktop": { "...": "ugyanaz a forma, vagy null, ha best-effort elhasalt" },
  "estimate": null
}
```

**Fontos (integritás-szabály):** a backend **soha nem** ad vissza Ft-veszteség-számot.
Az `estimate` mindig `null` a szerver felől. A pénzbecslés **kizárólag kliensoldalon**
készül, a látogató által beírt havi forgalomból és átlagos kosárértékből, és
egyértelműen „becslés a te adataidból" címkével jelenik meg. Input nélkül csak az
általános iparági elv mutatható (~1 mp késés ≈ ~7% konverzióvesztés), konkrét Ft nélkül.

`rating` lehetséges értékei (Core Web Vitals küszöbök): `"good"` | `"needs-improvement"` | `"poor"`.

### Error response (200, `ok:false` — a frontend mindig a body-ból olvas)

```json
{
  "ok": false,
  "error": "TIMEOUT",
  "message": "A mérés most túl sokáig tartott. Próbáld újra pár perc múlva."
}
```

`error` kódok: `INVALID_URL` | `TIMEOUT` | `PSI_ERROR` | `RATE_LIMITED` | `SERVER_ERROR`.
A `message` mindig barátságos, magyar, a látogatónak megmutatható.

## Backend env

- `PAGESPEED_API_KEY` — Google PageSpeed Insights API kulcs (Cloudflare Pages →
  Settings → Environment variables). Lokális teszthez: `functions/.dev.vars`
  (gitignore-olt), `PAGESPEED_API_KEY=...`.

## Lead capture

Az eredmény után az emailbekérés a meglévő Formspree-re megy a frontendből
(`https://formspree.io/f/movgkdoz`), az audit-eredmény rövid snapshotjával együtt —
nincs új backend infra.
