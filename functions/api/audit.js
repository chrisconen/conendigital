/**
 * POST /api/audit — Szivárgás-audit backend (Cloudflare Pages Function)
 *
 * Lekéri a Google PageSpeed Insights v5 valós Lighthouse-adatait (mobil + asztali),
 * kivonatolja a Core Web Vitals metrikákat és a legnagyobb javítási lehetőségeket,
 * és a LOCKED /api/audit szerződés szerinti JSON-t ad vissza.
 *
 * Integritás: a backend SOHA nem ad Ft-veszteség-becslést — az `estimate` mindig null.
 * A pénzbecslés kizárólag kliensoldalon, a látogató saját számaiból készül.
 *
 * Szerződés: functions/api/AUDIT_CONTRACT.md
 */

const PSI_ENDPOINT = 'https://www.googleapis.com/pagespeedonline/v5/runPagespeed';
const PSI_TIMEOUT_MS = 45000;
const CACHE_TTL_S = 6 * 60 * 60; // 6 óra URL-enként

const CORS = {
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Methods': 'POST, OPTIONS',
  'Access-Control-Allow-Headers': 'Content-Type',
};

function json(body, status = 200) {
  return new Response(JSON.stringify(body), {
    status,
    headers: { 'Content-Type': 'application/json; charset=utf-8', ...CORS },
  });
}

function fail(error, message) {
  return json({ ok: false, error, message });
}

// Origin-allowlist: böngészőből csak a saját oldalunkról indítható (CORS-abuse ellen).
// Origin nélküli kérés (pl. curl) átmegy, de a rate-limit fékezi.
const ALLOWED_ORIGINS = [
  'https://conendigital.hu',
  'https://www.conendigital.hu',
  'http://localhost:8788',
  'http://127.0.0.1:8788',
];
function originAllowed(origin) {
  return !origin || ALLOWED_ORIGINS.includes(origin);
}

/** http/https-re normalizál és blokkolja a nyilvánvalóan belső célokat (SSRF/abúzus ellen). */
function normalizeUrl(raw) {
  if (!raw || typeof raw !== 'string') return null;
  let s = raw.trim();
  if (!/^https?:\/\//i.test(s)) s = 'https://' + s;
  let u;
  try {
    u = new URL(s);
  } catch {
    return null;
  }
  if (u.protocol !== 'http:' && u.protocol !== 'https:') return null;
  const host = u.hostname.toLowerCase();
  if (
    host === 'localhost' ||
    host === '127.0.0.1' ||
    host === '0.0.0.0' ||
    host === '::1' ||
    host.endsWith('.local') ||
    host.endsWith('.internal') ||
    /^10\./.test(host) ||
    /^192\.168\./.test(host) ||
    /^172\.(1[6-9]|2\d|3[01])\./.test(host) ||
    /^169\.254\./.test(host)
  ) {
    return null;
  }
  if (!host.includes('.')) return null; // kell legalább egy domain-pont
  return u.toString();
}

function rate(value, good, poor) {
  if (value <= good) return 'good';
  if (value <= poor) return 'needs-improvement';
  return 'poor';
}

/** Egy PSI Lighthouse-eredményt a szerződés szerinti alakra hoz. */
function shapeResult(data) {
  const lh = data && data.lighthouseResult;
  if (!lh || !lh.categories || !lh.categories.performance) return null;
  const audits = lh.audits || {};
  const num = (id) => (audits[id] && typeof audits[id].numericValue === 'number' ? audits[id].numericValue : null);

  const lcpS = num('largest-contentful-paint');
  const clsV = num('cumulative-layout-shift');
  const tbtMs = num('total-blocking-time');
  const fcpS = num('first-contentful-paint');
  const siS = num('speed-index');

  const sec = (ms) => Number((ms / 1000).toFixed(1)); // tiszta kerekítés, lebegőpont-szemét nélkül
  const metrics = {};
  if (lcpS != null) metrics.lcp = { value: sec(lcpS), unit: 'mp', rating: rate(lcpS / 1000, 2.5, 4) };
  if (clsV != null) metrics.cls = { value: Number(clsV.toFixed(3)), unit: '', rating: rate(clsV, 0.1, 0.25) };
  if (tbtMs != null) metrics.tbt = { value: Math.round(tbtMs), unit: 'ms', rating: rate(tbtMs, 200, 600) };
  if (fcpS != null) metrics.fcp = { value: sec(fcpS), unit: 'mp', rating: rate(fcpS / 1000, 1.8, 3) };
  if (siS != null) metrics.si = { value: sec(siS), unit: 'mp', rating: rate(siS / 1000, 3.4, 5.8) };

  const opportunities = Object.keys(audits)
    .map((id) => audits[id])
    .filter((a) => a && a.details && a.details.type === 'opportunity' && typeof a.numericValue === 'number' && a.numericValue > 150)
    .sort((a, b) => b.numericValue - a.numericValue)
    .slice(0, 4)
    .map((a) => ({
      id: a.id,
      title: a.title,
      displayValue: a.displayValue || '',
      savingsMs: Math.round(a.numericValue),
    }));

  const score = Math.round((lh.categories.performance.score || 0) * 100);
  return { performanceScore: score, metrics, opportunities };
}

async function runPSI(url, strategy, key, signal, referer) {
  const qs = new URLSearchParams({
    url,
    strategy,
    category: 'performance',
    locale: 'hu',
    key,
  });
  // A PSI-kulcs HTTP-referer korlátozással van beállítva (böngészős kulcs). A Worker
  // szerveroldalon hívja, ezért explicit Referert küldünk egy engedélyezett origin-nel.
  // Élesben felülírható a PSI_REFERER env változóval.
  const res = await fetch(`${PSI_ENDPOINT}?${qs.toString()}`, {
    signal,
    headers: { Referer: referer },
  });
  if (!res.ok) {
    const status = res.status;
    const err = new Error(`PSI ${status}`);
    err.psiStatus = status;
    throw err;
  }
  const data = await res.json();
  return { shaped: shapeResult(data), finalUrl: data && data.id ? data.id : url };
}

/**
 * MÁSODLAGOS biztonsági jel — NEM a fő eredmény. Ugyanaz az ellenség (plugin-bloat),
 * ami lassít, ki is tesz: egy gyökér, két sebzés. Valós, ellenőrizhető header-higiénia.
 */
async function checkSecurity(url) {
  // Saját, rövid timeout — a fő (PSI) eredménytől függetlenül, gyorsan elenged.
  const ctrl = new AbortController();
  const t = setTimeout(() => ctrl.abort(), 12000);
  let res;
  try {
    res = await fetch(url, { method: 'GET', redirect: 'follow', signal: ctrl.signal, headers: { 'User-Agent': 'Mozilla/5.0 (compatible; ConenDigital-LeakAudit/1.0; +https://conendigital.hu)' } });
  } catch {
    clearTimeout(t);
    return null;
  }
  const h = res.headers;
  const val = (n) => (h.get(n) || '').trim();
  const has = (n) => !!val(n);

  const https = (res.url || url).startsWith('https://');
  const hsts = has('strict-transport-security');
  const csp = has('content-security-policy');
  const xcto = val('x-content-type-options').toLowerCase().includes('nosniff');
  const refpol = has('referrer-policy');
  const permpol = has('permissions-policy') || has('feature-policy');
  const frameProtection = has('x-frame-options') || /frame-ancestors/i.test(val('content-security-policy'));

  const leak = [val('server'), val('x-powered-by')].filter(Boolean).join(' · ');
  const serverLeak = /\d/.test(leak) || val('x-powered-by') ? leak : null;

  let wordpress = false;
  try {
    const body = await res.text();
    wordpress = /wp-content|wp-json|wp-includes|content="WordPress/i.test(body.slice(0, 60000));
  } catch {
    /* ignore body read errors */
  }
  clearTimeout(t);

  const checks = { https, hsts, csp, xContentType: xcto, referrerPolicy: refpol, frameProtection, permissionsPolicy: permpol };
  const passed = Object.values(checks).filter(Boolean).length;
  const total = Object.keys(checks).length;
  const grade = passed >= 7 ? 'A' : passed >= 5 ? 'B' : passed >= 3 ? 'C' : passed >= 1 ? 'D' : 'F';

  const findings = [];
  if (!https) findings.push('Nem mindenhol HTTPS — a kapcsolat lehallgatható.');
  if (!hsts) findings.push('Nincs HSTS — a böngésző http-re is rácsatlakozhat.');
  if (!csp) findings.push('Nincs Content-Security-Policy — gyengébb XSS-védelem.');
  if (!xcto) findings.push('Nincs X-Content-Type-Options — MIME-sniffing kockázat.');
  if (!frameProtection) findings.push('Nincs clickjacking-védelem (X-Frame-Options / frame-ancestors).');
  if (!refpol) findings.push('Nincs Referrer-Policy.');
  if (!permpol) findings.push('Nincs Permissions-Policy.');
  if (serverLeak) findings.push('A szerver kiírja a szoftver/verzió adatát (' + serverLeak + ') — támadónak ingyen infó.');

  return { ok: true, grade, https, wordpress, serverLeak, checks, passed, total, findings: findings.slice(0, 6) };
}

/** Könnyű, best-effort per-IP rate-limit (Cache API, ~6s ablak). Nem bulletproof — a valódi
 *  megoldás Turnstile/KV; ez csak a durva hammering-et fékezi. */
async function rateLimited(ip, cache) {
  if (!ip) return false;
  const key = new Request(`https://rl.audit.local/?ip=${encodeURIComponent(ip)}`);
  if (await cache.match(key)) return true;
  await cache.put(key, new Response('1', { headers: { 'Cache-Control': 'max-age=6' } })).catch(() => {});
  return false;
}

// Friction-mentes napi cap per IP: korlátozza, hány KÜLÖNBÖZŐ oldalt auditálhat egy IP naponta
// (a PSI-kvóta/költség védelme abúzus ellen — captcha NÉLKÜL, hogy a wedge UX ne sérüljön).
const DAILY_CAP = 25;
async function dayCapExceeded(ip, cache) {
  if (!ip) return false;
  const key = new Request(`https://rl.audit.local/day?ip=${encodeURIComponent(ip)}`);
  let count = 0;
  const hit = await cache.match(key);
  if (hit) {
    try { count = (await hit.json()).c || 0; } catch { count = 0; }
  }
  if (count >= DAILY_CAP) return true;
  await cache
    .put(key, new Response(JSON.stringify({ c: count + 1 }), { headers: { 'Cache-Control': 'max-age=86400', 'Content-Type': 'application/json' } }))
    .catch(() => {});
  return false;
}

export async function onRequestOptions() {
  return new Response(null, { status: 204, headers: CORS });
}

export async function onRequestPost({ request, env, waitUntil }) {
  if (!originAllowed(request.headers.get('Origin'))) {
    return fail('FORBIDDEN', 'Ez az audit csak a conendigital.hu-ról indítható.');
  }

  const key = env && env.PAGESPEED_API_KEY;
  if (!key) {
    return fail('SERVER_ERROR', 'Az audit-szolgáltatás épp nem elérhető. Próbáld újra később, vagy hívj minket.');
  }

  let payload;
  try {
    payload = await request.json();
  } catch {
    return fail('INVALID_URL', 'Hibás kérés. Adj meg egy webcímet.');
  }

  const url = normalizeUrl(payload && payload.url);
  if (!url) {
    return fail('INVALID_URL', 'Ez nem tűnik valódi, nyilvános webcímnek. Pl.: pelda-webshop.hu');
  }
  const strategy = ['mobile', 'desktop', 'both'].includes(payload && payload.strategy) ? payload.strategy : 'both';

  // URL-szintű cache (Cloudflare Cache API, KV-binding nélkül).
  const cacheKey = new Request(`https://audit-cache.local/?u=${encodeURIComponent(url)}&s=${strategy}`);
  const cache = caches.default;
  const hit = await cache.match(cacheKey);
  if (hit) {
    const body = await hit.json();
    body.cached = true;
    return json(body);
  }

  // Csak a drága (cache-miss) ágat korlátozzuk; a cache-elt eredmény olcsó és átmegy.
  const ip = request.headers.get('CF-Connecting-IP') || '';
  if (await rateLimited(ip, cache)) {
    return fail('RATE_LIMITED', 'Pillanat — egyszerre egy auditot futtatunk. Próbáld újra pár másodperc múlva.');
  }
  if (await dayCapExceeded(ip, cache)) {
    return fail('RATE_LIMITED', 'Mára elérted az ingyenes auditok számát. Holnap folytathatod, vagy hívj minket: +36 30 569 6550.');
  }

  const referer = (env && env.PSI_REFERER) || 'https://www.conendigital.hu/';
  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), PSI_TIMEOUT_MS);

  try {
    const wantMobile = strategy === 'mobile' || strategy === 'both';
    const wantDesktop = strategy === 'desktop' || strategy === 'both';

    // A biztonsági jel a PSI-vel PÁRHUZAMOSAN fut, és sosem blokkolja a fő eredményt.
    const secPromise = checkSecurity(url).catch(() => null);

    const tasks = [];
    if (wantMobile) tasks.push(runPSI(url, 'mobile', key, controller.signal, referer).then((r) => ['mobile', r]));
    if (wantDesktop) tasks.push(runPSI(url, 'desktop', key, controller.signal, referer).then((r) => ['desktop', r]));

    const settled = await Promise.allSettled(tasks);
    const security = await secPromise;
    clearTimeout(timer);

    let mobile = null;
    let desktop = null;
    let finalUrl = url;
    let anyTimeout = false;
    let anyError = false;

    for (const s of settled) {
      if (s.status === 'fulfilled') {
        const [kind, r] = s.value;
        if (kind === 'mobile') mobile = r.shaped;
        if (kind === 'desktop') desktop = r.shaped;
        if (r.finalUrl) finalUrl = r.finalUrl;
      } else {
        const reason = s.reason || {};
        if (reason.name === 'AbortError') anyTimeout = true;
        else anyError = true;
      }
    }

    // A mobil az elsődleges eredmény. Ha az nincs meg, az audit nem sikerült.
    const primary = wantMobile ? mobile : desktop;
    if (!primary) {
      if (anyTimeout) return fail('TIMEOUT', 'A mérés most túl sokáig tartott. Próbáld újra pár perc múlva.');
      return fail('PSI_ERROR', 'Ezt az oldalt most nem sikerült lemérni. Ellenőrizd a címet, vagy próbáld újra később.');
    }

    const body = {
      ok: true,
      url,
      finalUrl,
      fetchedAt: new Date().toISOString(),
      cached: false,
      mobile,
      desktop,
      security,
      estimate: null,
      partial: anyError || anyTimeout,
    };

    const toCache = json(body);
    toCache.headers.set('Cache-Control', `public, max-age=${CACHE_TTL_S}`);
    const cachePut = cache.put(cacheKey, toCache.clone()).catch(() => {});
    if (typeof waitUntil === 'function') waitUntil(cachePut);
    return toCache;
  } catch (e) {
    clearTimeout(timer);
    if (e && e.name === 'AbortError') {
      return fail('TIMEOUT', 'A mérés most túl sokáig tartott. Próbáld újra pár perc múlva.');
    }
    if (e && e.psiStatus === 429) {
      return fail('RATE_LIMITED', 'Most sokan auditálnak egyszerre. Próbáld újra pár perc múlva.');
    }
    return fail('PSI_ERROR', 'Váratlan hiba a mérés közben. Próbáld újra később.');
  }
}
