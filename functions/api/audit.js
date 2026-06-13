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

export async function onRequestOptions() {
  return new Response(null, { status: 204, headers: CORS });
}

// Diagnosztika: GET /api/audit — megmondja, látja-e a Function a kulcsot. Titkot NEM ad ki,
// csak presence + hossz, hogy a Cloudflare env-beállítást ellenőrizni lehessen böngészőből.
export async function onRequestGet({ env }) {
  const k = (env && env.PAGESPEED_API_KEY) || '';
  // Csak NEVEK, értékek nélkül — a rendszer CF_* változókat kiszűrjük.
  const boundVars = Object.keys(env || {}).filter((n) => !n.startsWith('CF_') && typeof env[n] === 'string');
  return json({
    ok: true,
    debug: true,
    keyPresent: !!k,
    keyLength: k.length,
    boundVars,
    referer: (env && env.PSI_REFERER) || 'https://www.conendigital.hu/',
  });
}

export async function onRequestPost({ request, env, waitUntil }) {
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

  const referer = (env && env.PSI_REFERER) || 'https://www.conendigital.hu/';
  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), PSI_TIMEOUT_MS);

  try {
    const wantMobile = strategy === 'mobile' || strategy === 'both';
    const wantDesktop = strategy === 'desktop' || strategy === 'both';

    const tasks = [];
    if (wantMobile) tasks.push(runPSI(url, 'mobile', key, controller.signal, referer).then((r) => ['mobile', r]));
    if (wantDesktop) tasks.push(runPSI(url, 'desktop', key, controller.signal, referer).then((r) => ['desktop', r]));

    const settled = await Promise.allSettled(tasks);
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
