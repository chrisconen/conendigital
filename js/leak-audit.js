/**
 * Szivárgás-audit — frontend modul (vanilla, progresszív bővítés).
 *
 * Mountol: #leak-audit-app konténerbe.
 * Backend: POST /api/audit (lásd functions/api/AUDIT_CONTRACT.md).
 * Lead: Formspree (a meglévő űrlap-endpoint), az eredmény snapshotjával.
 *
 * INTEGRITÁS: a "havi veszteség" Ft-szám SOHA nem kitalált. Csak akkor jelenik meg,
 * ha a látogató maga adja meg a havi forgalmát és átlagos kosárértékét — és akkor is
 * "becslés a TE adataidból" címkével, a feltevésekkel együtt. Input nélkül csak az
 * általános iparági elv látszik (~1 mp késés ≈ ~7% konverzióvesztés), Ft nélkül.
 */
(function () {
  'use strict';

  var FORMSPREE = 'https://formspree.io/f/movgkdoz';
  var PHONE = '+36305696550';
  // Önkiszolgáló időpontfoglaló (Cal.com/Calendly). Üresen a telefonra esik vissza.
  // Chris: ide jöhet a valódi naptár-link, és máris self-serve booking lesz.
  var BOOKING_URL = '';
  var CONV_PER_SECOND = 0.07; // iparági heurisztika: ~7% konverzióvesztés / +1 mp
  var DRAG_CAP = 0.35; // hihetőségi plafon
  var ASSUMED_CONV = 0.015; // ha a látogató nem ad konverziót: óvatos 1,5% feltevés
  var GOOD_LCP = 2.5;

  var root = document.getElementById('leak-audit-app');
  if (!root) return;

  injectStyles();
  renderInput();

  // Globális indító — a hero-ba épített input innen tudja elindítani az auditot.
  window.startLeakAudit = function (url) {
    var sec = document.getElementById('szivargas-audit');
    if (sec) sec.scrollIntoView({ behavior: 'smooth', block: 'start' });
    if (url && url.trim()) runAudit(url.trim());
  };

  // Hero-ba épített audit-form bekötése (ha van).
  var heroForm = document.getElementById('heroAuditForm');
  if (heroForm) {
    heroForm.addEventListener('submit', function (e) {
      e.preventDefault();
      var u = (document.getElementById('heroAuditUrl') || {}).value || '';
      window.startLeakAudit(u);
    });
  }

  // Megosztott link: ?audit=<url> → automatikus audit (pl. Chris elküldi az ügyfélnek a saját szivárgását).
  var sharedAudit = null;
  try {
    sharedAudit = new URLSearchParams(window.location.search).get('audit');
  } catch (e) {
    /* no URLSearchParams */
  }
  if (sharedAudit) {
    window.__laShared = true;
    setTimeout(function () {
      window.startLeakAudit(sharedAudit);
    }, 500);
  }

  // ---- állapot ----
  var lastResult = null;

  function renderInput(prefillError) {
    root.innerHTML =
      '<form class="la-inputbar" id="la-form" novalidate>' +
      '  <label class="la-sronly" for="la-url">Webshop címe</label>' +
      '  <input class="la-url" id="la-url" type="text" inputmode="url" autocomplete="url" ' +
      '         placeholder="pl. pelda-webshop.hu" aria-label="Webshop címe" />' +
      '  <button class="la-btn" id="la-go" type="submit">Megnézem, hol szivárog →</button>' +
      '</form>' +
      '<p class="la-hint">Valós mérés a Google PageSpeed Insights motorjával — nincs regisztráció, ~20–40 mp.</p>' +
      (prefillError ? '<p class="la-error" role="alert">' + esc(prefillError) + '</p>' : '');

    document.getElementById('la-form').addEventListener('submit', function (e) {
      e.preventDefault();
      var url = document.getElementById('la-url').value.trim();
      if (!url) {
        renderInput('Adj meg egy webcímet, és megnézzük, hol szivárog.');
        return;
      }
      runAudit(url);
    });
  }

  function renderLoading(url) {
    root.innerHTML =
      '<div class="la-loading">' +
      '  <div class="la-spinner" aria-hidden="true"></div>' +
      '  <div class="la-loading-text">' +
      '    <strong>Mérjük: ' + esc(stripScheme(url)) + '</strong>' +
      '    <span id="la-load-step">Valós Lighthouse-mérés indul…</span>' +
      '  </div>' +
      '</div>';
    var steps = [
      'Mobil nézet betöltése…',
      'Core Web Vitals számítása (LCP, CLS)…',
      'A legnagyobb szivárgások keresése…',
      'Asztali nézet ellenőrzése…',
      'Eredmény összeállítása…',
    ];
    var i = 0;
    var el = document.getElementById('la-load-step');
    var iv = setInterval(function () {
      if (!document.getElementById('la-load-step')) {
        clearInterval(iv);
        return;
      }
      el.textContent = steps[i % steps.length];
      i++;
    }, 4500);
  }

  function runAudit(url) {
    renderLoading(url);
    track('leak_audit_start');
    fetch('/api/audit', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ url: url, strategy: 'both' }),
    })
      .then(function (r) {
        return r.json();
      })
      .then(function (data) {
        if (!data || !data.ok) {
          var msg = (data && data.message) || 'Ezt az oldalt most nem sikerült lemérni. Próbáld újra.';
          track('leak_audit_fail', { error: data && data.error });
          renderInput(msg);
          return;
        }
        lastResult = data;
        track('leak_audit_success', { score: data.mobile && data.mobile.performanceScore });
        renderResult(data);
      })
      .catch(function () {
        renderInput('Hálózati hiba a mérés közben. Ellenőrizd a kapcsolatot, és próbáld újra.');
      });
  }

  // ---- eredmény ----
  function renderResult(data) {
    var m = data.mobile;
    var d = data.desktop;
    var verdict = verdictFor(m);

    var html =
      '<div class="la-result">' +
      (window.__laShared
        ? '  <div class="la-shared-banner">Ezt a szivárgás-auditot megosztották veled. Lentebb a saját oldalad mért eredménye — a Conen Digitaltól.</div>'
        : '') +
      '  <div class="la-result-head">' +
      '    <div>' +
      '      <div class="la-result-label">Szivárgás-audit eredménye</div>' +
      '      <h3 class="la-result-url">' + esc(stripScheme(data.finalUrl || data.url)) + '</h3>' +
      '    </div>' +
      '    <div class="la-result-actions">' +
      '      <button class="la-share" id="la-share" type="button">🔗 Megosztható link</button>' +
      '      <button class="la-again" id="la-again" type="button">Másik oldal →</button>' +
      '    </div>' +
      '  </div>' +
      '  <div class="la-verdict la-verdict--' + verdict.tone + '">' + esc(verdict.text) + '</div>' +
      '  <div class="la-scores">' +
      scoreCard('Mobil', m.performanceScore) +
      (d ? scoreCard('Asztali', d.performanceScore) : '') +
      '  </div>' +
      '  <div class="la-metrics">' + metricsRow(m.metrics) + '</div>';

    if (m.opportunities && m.opportunities.length) {
      html += '<div class="la-ops"><div class="la-ops-title">A legnagyobb szivárgások — ezek lassítják a leginkább:</div><ul class="la-ops-list">';
      m.opportunities.forEach(function (op) {
        html +=
          '<li class="la-op"><span class="la-op-name">' + esc(op.title) + '</span>' +
          (op.displayValue ? '<span class="la-op-save">' + esc(op.displayValue) + '</span>' : '') +
          '</li>';
      });
      html += '</ul></div>';
    }

    // Becslés-blokk (kliensoldali, őszinte)
    html += estimateBlock(m);

    // Másodlagos biztonsági jel — ugyanaz a plugin-bloat: lassít ÉS kitesz.
    if (data.security) html += securityStrip(data.security);

    if (data.partial) {
      html += '<p class="la-note">Megjegyzés: az egyik nézet mérése most nem sikerült, a mobil eredményt mutatjuk.</p>';
    }

    // Booking/hívás CTA — a leggyorsabb út a beszélgetésig (audit→konzultáció rés zárása)
    var bookHref = BOOKING_URL || ('tel:' + PHONE);
    var bookExternal = BOOKING_URL ? ' target="_blank" rel="noopener"' : '';
    var bookLabel = BOOKING_URL ? 'Foglalj egy ingyenes 15 perces konzultációt →' : 'Beszéljünk a javításról — hívj most: +36 30 569 6550';
    html +=
      '  <div class="la-book">' +
      '    <div class="la-book-title">Találtunk szivárgást? Állítsuk el — beszéljünk.</div>' +
      '    <a class="la-book-btn" href="' + esc(bookHref) + '"' + bookExternal + ' onclick="try{window.gtag&&gtag(\'event\',\'leak_audit_book\')}catch(e){}">' + esc(bookLabel) + '</a>' +
      '    <span class="la-book-or">vagy kérd e-mailben a részletes tervet ↓</span>' +
      '  </div>' +
      '  <div class="la-lead" id="la-lead">' +
      '    <div class="la-lead-title">Kérd a konkrét javítási tervet</div>' +
      '    <p class="la-lead-sub">Átküldöm e-mailben, mit és milyen sorrendben érdemes javítani ezen az oldalon — és mennyi időt/sebességet nyersz vele. Nincs kötelezettség.</p>' +
      '    <form class="la-lead-form" id="la-lead-form" novalidate>' +
      '      <input class="la-lead-input" id="la-lead-email" type="email" required placeholder="email@ceged.hu" aria-label="E-mail cím" />' +
      '      <input class="la-lead-input" id="la-lead-name" type="text" placeholder="Neved (opcionális)" aria-label="Neved" />' +
      '      <button class="la-btn" type="submit">Kérem a javítási tervet →</button>' +
      '    </form>' +
      '    <label class="la-consent"><input type="checkbox" id="la-consent" required /> ' +
      '      <span>Elfogadom az <a href="/adatvedelem.html" target="_blank" rel="noopener">Adatvédelmi tájékoztatót</a>. Az adataimat kizárólag a kapcsolatfelvételhez használjátok.</span></label>' +
      '  </div>' +
      '</div>';

    root.innerHTML = html;
    window.__laShared = false; // a banner csak a megosztott audit első renderénél jelenjen meg

    document.getElementById('la-again').addEventListener('click', function () {
      renderInput();
    });
    var shareBtn = document.getElementById('la-share');
    if (shareBtn) {
      shareBtn.addEventListener('click', function () {
        var shareUrl = window.location.origin + '/?audit=' + encodeURIComponent(stripScheme(data.finalUrl || data.url));
        var done = function () {
          shareBtn.textContent = '✓ Link másolva';
          track('leak_audit_share');
          setTimeout(function () { shareBtn.textContent = '🔗 Megosztható link'; }, 2500);
        };
        if (navigator.clipboard && navigator.clipboard.writeText) {
          navigator.clipboard.writeText(shareUrl).then(done, function () { window.prompt('Másold ki a megosztható linket:', shareUrl); });
        } else {
          window.prompt('Másold ki a megosztható linket:', shareUrl);
        }
      });
    }
    wireEstimate(m);
    document.getElementById('la-lead-form').addEventListener('submit', submitLead);
  }

  // Másodlagos biztonsági csík — NEM a fő eredmény. Könnyű, a sebesség-szivárgás alatt.
  function securityStrip(sec) {
    var grade = sec.grade || 'F';
    var tone = grade === 'A' || grade === 'B' ? 'good' : grade === 'C' ? 'mid' : 'bad';
    var html =
      '<div class="la-sec">' +
      '  <div class="la-sec-head">' +
      '    <span class="la-sec-grade la-sec-grade--' + tone + '">' + esc(grade) + '</span>' +
      '    <div><div class="la-sec-title">Biztonsági jelek <span>· másodlagos</span></div>' +
      '    <div class="la-sec-sub">Ugyanaz a plugin-bloat, ami lassít, támadási felületet is nyit — egy gyökér, két sebzés.</div></div>' +
      '  </div>';
    if (sec.wordpress) {
      html += '<p class="la-sec-wp">WordPress + plugin-réteg észlelve — ez lassít ÉS bővíti a támadási felületet (elavult pluginek, ismert sérülékenységek).</p>';
    }
    if (sec.findings && sec.findings.length) {
      html += '<ul class="la-sec-list">';
      sec.findings.forEach(function (f) {
        html += '<li>' + esc(f) + '</li>';
      });
      html += '</ul>';
    } else {
      html += '<p class="la-sec-ok">A vizsgált alap-headerek rendben — ez ritka és jó jel.</p>';
    }
    html += '<p class="la-sec-foot">' + sec.passed + '/' + sec.total + ' alap biztonsági header rendben. A teljes vizsgálat (függőségek, konfiguráció) a javítási tervben.</p>';
    return html + '</div>';
  }

  function scoreCard(label, score) {
    var tone = score >= 90 ? 'good' : score >= 50 ? 'mid' : 'bad';
    return (
      '<div class="la-score la-score--' + tone + '">' +
      '  <div class="la-score-num">' + score + '</div>' +
      '  <div class="la-score-cap">' + esc(label) + ' sebesség<br><span>0–100</span></div>' +
      '</div>'
    );
  }

  function metricsRow(metrics) {
    var labels = {
      lcp: ['Legnagyobb tartalom betöltése (LCP)', 'mp'],
      cls: ['Ugráló elrendezés (CLS)', ''],
      tbt: ['Kattintásra fagyás (TBT)', 'ms'],
      fcp: ['Első tartalom (FCP)', 'mp'],
      si: ['Vizuális készre töltés (SI)', 'mp'],
    };
    var order = ['lcp', 'tbt', 'cls', 'fcp', 'si'];
    var out = '';
    order.forEach(function (k) {
      var mm = metrics[k];
      if (!mm) return;
      var L = labels[k];
      var val = hu(mm.value);
      out +=
        '<div class="la-metric la-metric--' + mm.rating + '">' +
        '  <div class="la-metric-val">' + val + (mm.unit ? ' ' + mm.unit : '') + '</div>' +
        '  <div class="la-metric-lab">' + esc(L[0]) + '</div>' +
        '</div>';
    });
    return out;
  }

  // Minden metrika sima nyelven + következmény. A `speed` jelzi a sebesség-tengelyt.
  var METRIC_INFO = {
    lcp: { speed: true,  plain: function (v) { return 'lassan tölt be a fő tartalom (LCP ' + hu(v) + ' mp)'; }, cons: 'a vásárló elmegy, mielőtt betöltene' },
    fcp: { speed: true,  plain: function (v) { return 'sokáig üres marad a képernyő (FCP ' + hu(v) + ' mp)'; }, cons: 'a látogató azt hiszi, nem tölt, és kilép' },
    si:  { speed: true,  plain: function (v) { return 'lassan áll össze a kép (SI ' + hu(v) + ' mp)'; }, cons: 'a használható oldalra sokat kell várni' },
    tbt: { speed: false, plain: function (v) { return 'akad és fagy a kattintásra (TBT ' + v + ' ms)'; }, cons: 'a vásárló frusztrálódik és elkattint' },
    cls: { speed: false, plain: function (v) { return 'ugrál az elrendezés (CLS ' + hu(v) + ')'; }, cons: 'félrekattintás és bizalomvesztés' },
  };

  // A ténylegesen legrosszabb metrikát adja vissza (poor előbb, mint needs-improvement),
  // prioritási sorrenddel a holtversenyre. Ez vezeti az összegzést — nem a nyers pontszám.
  function worstLeak(metrics) {
    var order = ['lcp', 'cls', 'tbt', 'fcp', 'si'];
    var poor = null, ni = null;
    order.forEach(function (k) {
      var mm = metrics[k];
      if (!mm) return;
      if (mm.rating === 'poor' && !poor) poor = { key: k, m: mm };
      if (mm.rating === 'needs-improvement' && !ni) ni = { key: k, m: mm };
    });
    return poor || ni || null;
  }

  // Az összegzés a valódi legrosszabb szivárgást nevezi meg sima nyelven (nem a pontszámot).
  function verdictFor(m) {
    var w = worstLeak(m.metrics);
    if (!w) {
      return { tone: 'good', text: 'Ez az oldal gyors és stabil — a nagy, mérhető szivárgások itt nincsenek. Ha mégis kevés a vásárlás, az a checkout-flow vagy a tartalom; azt nézzük meg együtt.' };
    }
    var info = METRIC_INFO[w.key];
    var plain = info.plain(w.m.value);
    if (w.m.rating === 'poor') {
      if (info.speed) {
        return { tone: 'bad', text: 'Itt komoly, néma szivárgás van: ' + plain + ' — ' + info.cons + '. Ezen a sebességen a mobil vásárlók jelentős része kilép.' };
      }
      // Sebesség rendben, de nem-sebesség metrika a baj (pl. CLS): ezt KI KELL mondani.
      return { tone: 'bad', text: 'A sebesség rendben — DE ' + plain + ', ami ' + info.cons + '. Itt a szivárgás, nem a töltésnél.' };
    }
    // needs-improvement: enyhébb
    return { tone: 'mid', text: 'Van mit behozni: ' + plain + ' — ' + info.cons + '. Még nem kritikus, de már némán visz vásárlót.' };
  }

  // ---- őszinte becslés ----
  function estimateBlock(m) {
    var lcp = m.metrics.lcp ? m.metrics.lcp.value : null;
    var excess = lcp != null ? Math.max(0, lcp - GOOD_LCP) : 0;
    var dragPct = Math.round(Math.min(excess * CONV_PER_SECOND, DRAG_CAP) * 100);

    var principle;
    if (excess > 0) {
      // A sebesség a (számszerűsíthető) szivárgás — ~7%/mp heurisztika + kalkulátor.
      principle =
        'A te oldaladnál a mobil LCP <strong>' + hu(lcp) + ' mp</strong>, ami <strong>' +
        hu(round1(excess)) + ' mp-cel</strong> van a jó tartomány (2,5 mp) felett. Az iparági kutatások szerint nagyjából minden plusz másodperc ~7% konverzióvesztéssel jár.';
    } else {
      // A sebesség rendben — ha más metrika a baj (pl. CLS), AZT nevezzük meg, nem siklunk át fölötte.
      var w = worstLeak(m.metrics);
      if (w && (w.m.rating === 'poor' || w.m.rating === 'needs-improvement') && !METRIC_INFO[w.key].speed) {
        var info = METRIC_INFO[w.key];
        principle =
          'A sebesség rendben' + (lcp != null ? ' (LCP <strong>' + hu(lcp) + ' mp</strong>)' : '') +
          ' — a szivárgás itt nem a töltés, hanem hogy <strong>' + info.plain(w.m.value) + '</strong>: ' + info.cons +
          '. Forintban ezt nem találgatjuk: a te számaidon, közös méréssel mutatjuk meg, mennyit ér a javítása.';
      } else if (w) {
        principle =
          'A sebesség a jó tartományban van, de van mit csiszolni (' + METRIC_INFO[w.key].plain(w.m.value) + '). ' +
          'A nagy, mérhető szivárgás itt nem a töltés.';
      } else {
        principle = 'A mért értékek a jó tartományban vannak — a sebesség itt nem szivárog. Ha mégis kevés a vásárlás, a checkout-flow-t és a tartalmat érdemes nézni.';
      }
    }

    return (
      '<div class="la-est">' +
      '  <div class="la-est-principle">' + principle + '</div>' +
      (excess > 0
        ? '  <div class="la-est-calc">' +
          '    <div class="la-est-calc-title">Mennyit ér ez forintban? Számold ki a <strong>saját</strong> számaiddal:</div>' +
          '    <div class="la-est-inputs">' +
          '      <label>Havi látogató<input id="la-visitors" type="number" min="0" inputmode="numeric" placeholder="pl. 8000" /></label>' +
          '      <label>Átlagos kosárérték (Ft)<input id="la-cart" type="number" min="0" inputmode="numeric" placeholder="pl. 18000" /></label>' +
          '      <label>Konverzió % <span class="la-opt">(ha tudod)</span><input id="la-conv" type="number" min="0" step="0.1" inputmode="decimal" placeholder="opcionális" /></label>' +
          '    </div>' +
          '    <button class="la-est-btn" id="la-est-go" type="button">Becslés a saját adataimból →</button>' +
          '    <div class="la-est-out" id="la-est-out" data-drag="' + dragPct + '"></div>' +
          '  </div>'
        : '') +
      '</div>'
    );
  }

  function wireEstimate(m) {
    var btn = document.getElementById('la-est-go');
    if (!btn) return;
    btn.addEventListener('click', function () {
      var V = num(document.getElementById('la-visitors').value);
      var C = num(document.getElementById('la-cart').value);
      var convRaw = num(document.getElementById('la-conv').value);
      var out = document.getElementById('la-est-out');
      var dragPct = parseInt(out.getAttribute('data-drag'), 10) || 0;
      var drag = dragPct / 100;

      if (!V || !C) {
        out.className = 'la-est-out la-est-out--warn';
        out.innerHTML = 'A becsléshez add meg legalább a <strong>havi látogatót</strong> és az <strong>átlagos kosárértéket</strong> — a számot a TE adataidból építjük, nem találjuk ki.';
        return;
      }

      var conv = convRaw ? convRaw / 100 : ASSUMED_CONV;
      var assumed = !convRaw;
      var monthlyOrders = V * conv;
      var recoverableOrders = monthlyOrders * drag;
      var recoverable = Math.round(recoverableOrders * C);

      out.className = 'la-est-out la-est-out--show';
      out.innerHTML =
        '<div class="la-est-big">~' + huFt(recoverable) + ' Ft / hó</div>' +
        '<div class="la-est-cap">becslés a TE adataidból — nem mért tény</div>' +
        '<div class="la-est-detail">' +
        huFt(V) + ' látogató × ' + (assumed ? '<u>1,5% feltételezett</u>' : hu(convRaw) + '%') + ' konverzió × ' +
        dragPct + '% sebesség-veszteség × ' + huFt(C) + ' Ft kosár.' +
        (assumed ? ' <em>(Konverziót nem adtál meg — óvatos 1,5%-kal számoltunk; a sajáttal pontosabb.)</em>' : '') +
        '</div>';
      track('leak_audit_estimate', { recoverable: recoverable });
    });
  }

  // ---- lead ----
  function submitLead(e) {
    e.preventDefault();
    var email = document.getElementById('la-lead-email').value.trim();
    var name = document.getElementById('la-lead-name').value.trim();
    var consent = document.getElementById('la-consent').checked;
    var lead = document.getElementById('la-lead');
    if (!email || !/.+@.+\..+/.test(email)) {
      flash(lead, 'Adj meg egy érvényes e-mail címet.');
      return;
    }
    if (!consent) {
      flash(lead, 'Az adatvédelmi tájékoztató elfogadása kötelező.');
      return;
    }

    var snapshot = lastResult
      ? {
          url: lastResult.finalUrl || lastResult.url,
          mobil_pont: lastResult.mobile && lastResult.mobile.performanceScore,
          asztali_pont: lastResult.desktop && lastResult.desktop.performanceScore,
          mobil_lcp: lastResult.mobile && lastResult.mobile.metrics.lcp ? lastResult.mobile.metrics.lcp.value + ' mp' : '—',
        }
      : {};

    var body = {
      _subject: 'Szivárgás-audit lead — ' + (snapshot.url || ''),
      email: email,
      name: name || '(nincs megadva)',
      forras: 'leak-audit',
      audit_url: snapshot.url || '',
      audit_mobil_pont: snapshot.mobil_pont,
      audit_asztali_pont: snapshot.asztali_pont,
      audit_mobil_lcp: snapshot.mobil_lcp,
    };

    var btn = lead.querySelector('button[type="submit"]');
    if (btn) {
      btn.disabled = true;
      btn.textContent = 'Küldés…';
    }

    fetch(FORMSPREE, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', Accept: 'application/json' },
      body: JSON.stringify(body),
    })
      .then(function (r) {
        if (r.ok) {
          track('leak_audit_lead');
          lead.innerHTML =
            '<div class="la-lead-done"><strong>Megkaptam — köszönöm! ✅</strong>' +
            '<p>Hamarosan küldöm a konkrét javítási tervet erre az oldalra. Ha sürgős: <a href="tel:+36305696550">+36 30 569 6550</a>.</p></div>';
        } else {
          if (btn) {
            btn.disabled = false;
            btn.textContent = 'Kérem a javítási tervet →';
          }
          flash(lead, 'Most nem sikerült elküldeni. Próbáld újra, vagy hívj: +36 30 569 6550.');
        }
      })
      .catch(function () {
        if (btn) {
          btn.disabled = false;
          btn.textContent = 'Kérem a javítási tervet →';
        }
        flash(lead, 'Hálózati hiba. Próbáld újra, vagy hívj: +36 30 569 6550.');
      });
  }

  // ---- segédek ----
  function num(v) {
    var n = parseFloat(String(v).replace(/\s/g, '').replace(',', '.'));
    return isFinite(n) && n > 0 ? n : 0;
  }
  function round1(n) {
    return Math.round(n * 10) / 10;
  }
  function hu(n) {
    return String(n).replace('.', ',');
  }
  function huFt(n) {
    return Math.round(n).toLocaleString('hu-HU');
  }
  function stripScheme(u) {
    return String(u || '').replace(/^https?:\/\//i, '').replace(/\/$/, '');
  }
  function esc(s) {
    return String(s == null ? '' : s).replace(/[&<>"']/g, function (c) {
      return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c];
    });
  }
  function flash(container, msg) {
    var existing = container.querySelector('.la-flash');
    if (existing) existing.remove();
    var p = document.createElement('p');
    p.className = 'la-flash';
    p.setAttribute('role', 'alert');
    p.textContent = msg;
    container.appendChild(p);
  }
  function track(name, params) {
    try {
      if (typeof window.gtag === 'function') window.gtag('event', name, params || {});
    } catch (e) {
      /* no-op */
    }
  }

  function injectStyles() {
    if (document.getElementById('la-styles')) return;
    var css =
      '#leak-audit-app{--la-gold:#C9A962;--la-good:#4ade80;--la-mid:#fbbf24;--la-bad:#f87171;font-family:var(--font-body,sans-serif);max-width:920px;margin:0 auto}' +
      '.la-sronly{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0,0,0,0)}' +
      '.la-inputbar{display:flex;gap:.6rem;flex-wrap:wrap}' +
      '.la-url{flex:1;min-width:220px;padding:1rem 1.1rem;background:var(--surface-2,#18181b);border:1px solid var(--border,#27272a);border-radius:var(--radius-md,12px);color:var(--text,#fafafa);font-size:1rem;font-family:var(--font-mono,monospace)}' +
      '.la-url:focus{outline:none;border-color:var(--la-gold);box-shadow:0 0 0 3px rgba(201,169,98,.15)}' +
      '.la-btn{padding:1rem 1.5rem;background:var(--la-gold);color:#0b0b0d;border:none;border-radius:var(--radius-md,12px);font-weight:700;font-family:var(--font-main,sans-serif);font-size:1rem;cursor:pointer;white-space:nowrap;transition:transform .15s,filter .15s}' +
      '.la-btn:hover{filter:brightness(1.08);transform:translateY(-1px)}.la-btn:disabled{opacity:.6;cursor:default}' +
      '.la-hint{margin:.8rem 0 0;font-size:.82rem;color:var(--text-tertiary,#71717a);font-family:var(--font-mono,monospace)}' +
      '.la-error,.la-flash{margin:.9rem 0 0;color:var(--la-bad);font-size:.9rem}' +
      '.la-loading{display:flex;align-items:center;gap:1.2rem;padding:2rem 0}' +
      '.la-spinner{width:42px;height:42px;border:3px solid var(--border,#27272a);border-top-color:var(--la-gold);border-radius:50%;animation:la-spin 1s linear infinite;flex-shrink:0}' +
      '@keyframes la-spin{to{transform:rotate(360deg)}}' +
      '.la-loading-text strong{display:block;color:var(--text,#fafafa);font-family:var(--font-mono,monospace);font-size:.95rem}' +
      '.la-loading-text span{display:block;margin-top:.3rem;color:var(--text-secondary,#a1a1aa);font-size:.85rem}' +
      '.la-result-head{display:flex;justify-content:space-between;align-items:flex-start;gap:1rem;flex-wrap:wrap}' +
      '.la-result-label{font-family:var(--font-mono,monospace);font-size:.72rem;text-transform:uppercase;letter-spacing:.08em;color:var(--la-gold)}' +
      '.la-result-url{margin:.2rem 0 0;font-size:1.25rem;color:var(--text,#fafafa);word-break:break-all}' +
      '.la-again,.la-est-btn{background:transparent;border:1px solid var(--border-hover,#3f3f46);color:var(--text-secondary,#a1a1aa);padding:.5rem .9rem;border-radius:var(--radius-full,9999px);font-size:.82rem;cursor:pointer;font-family:var(--font-mono,monospace)}' +
      '.la-result-actions{display:flex;gap:.5rem;flex-wrap:wrap}' +
      '.la-share{background:rgba(201,169,98,.1);border:1px solid var(--la-gold);color:var(--la-gold);padding:.5rem .9rem;border-radius:var(--radius-full,9999px);font-size:.82rem;cursor:pointer;font-family:var(--font-mono,monospace);white-space:nowrap}' +
      '.la-share:hover{background:rgba(201,169,98,.18)}' +
      '.la-shared-banner{margin-bottom:1.1rem;padding:.8rem 1.1rem;border:1px solid var(--la-gold);border-left-width:3px;border-radius:var(--radius-sm,6px);background:rgba(201,169,98,.06);color:var(--text,#fafafa);font-size:.9rem;line-height:1.5}' +
      '.la-again:hover,.la-est-btn:hover{border-color:var(--la-gold);color:var(--la-gold)}' +
      '.la-verdict{margin:1.3rem 0;padding:1rem 1.2rem;border-radius:var(--radius-md,12px);font-size:1.02rem;line-height:1.5;border-left:3px solid}' +
      '.la-verdict--good{background:rgba(74,222,128,.08);border-color:var(--la-good)}' +
      '.la-verdict--mid{background:rgba(251,191,36,.08);border-color:var(--la-mid)}' +
      '.la-verdict--bad{background:rgba(248,113,113,.08);border-color:var(--la-bad)}' +
      '.la-scores{display:flex;gap:1rem;flex-wrap:wrap;margin-bottom:1.3rem}' +
      '.la-score{display:flex;align-items:center;gap:.8rem;padding:1rem 1.4rem;border:1px solid var(--border,#27272a);border-radius:var(--radius-md,12px);background:var(--surface-2,#18181b);flex:1;min-width:150px}' +
      '.la-score-num{font-size:2.4rem;font-weight:800;font-family:var(--font-main,sans-serif);line-height:1}' +
      '.la-score--good .la-score-num{color:var(--la-good)}.la-score--mid .la-score-num{color:var(--la-mid)}.la-score--bad .la-score-num{color:var(--la-bad)}' +
      '.la-score-cap{font-size:.85rem;color:var(--text-secondary,#a1a1aa);line-height:1.3}.la-score-cap span{font-size:.7rem;color:var(--text-tertiary,#71717a)}' +
      '.la-metrics{display:grid;grid-template-columns:repeat(auto-fit,minmax(140px,1fr));gap:.7rem;margin-bottom:1.5rem}' +
      '.la-metric{padding:.85rem 1rem;border:1px solid var(--border,#27272a);border-radius:var(--radius-sm,6px);background:var(--surface,#111113);border-left:3px solid}' +
      '.la-metric--good{border-left-color:var(--la-good)}.la-metric--needs-improvement{border-left-color:var(--la-mid)}.la-metric--poor{border-left-color:var(--la-bad)}' +
      '.la-metric-val{font-size:1.25rem;font-weight:700;font-family:var(--font-mono,monospace);color:var(--text,#fafafa)}' +
      '.la-metric-lab{font-size:.74rem;color:var(--text-tertiary,#71717a);margin-top:.2rem;line-height:1.3}' +
      '.la-ops{margin-bottom:1.5rem}.la-ops-title{font-size:.9rem;color:var(--text-secondary,#a1a1aa);margin-bottom:.7rem}' +
      '.la-ops-list{list-style:none;padding:0;margin:0}' +
      '.la-op{display:flex;justify-content:space-between;gap:1rem;padding:.7rem 0;border-bottom:1px solid var(--border,#27272a);flex-wrap:wrap}' +
      '.la-op-name{color:var(--text,#fafafa);font-size:.92rem}.la-op-save{color:var(--la-gold);font-family:var(--font-mono,monospace);font-size:.82rem;white-space:nowrap}' +
      '.la-est{margin:1.5rem 0;padding:1.3rem;border:1px solid var(--border,#27272a);border-radius:var(--radius-md,12px);background:rgba(201,169,98,.04)}' +
      '.la-est-principle{font-size:.95rem;line-height:1.6;color:var(--text-secondary,#a1a1aa)}.la-est-principle strong{color:var(--text,#fafafa)}' +
      '.la-est-calc{margin-top:1.1rem;padding-top:1.1rem;border-top:1px solid var(--border,#27272a)}' +
      '.la-est-calc-title{font-size:.9rem;color:var(--text,#fafafa);margin-bottom:.8rem}' +
      '.la-est-inputs{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:.7rem;margin-bottom:.9rem}' +
      '.la-est-inputs label{display:flex;flex-direction:column;gap:.3rem;font-size:.78rem;color:var(--text-tertiary,#71717a)}' +
      '.la-est-inputs input{padding:.7rem;background:var(--surface-2,#18181b);border:1px solid var(--border,#27272a);border-radius:var(--radius-sm,6px);color:var(--text,#fafafa);font-family:var(--font-mono,monospace)}' +
      '.la-est-inputs input:focus{outline:none;border-color:var(--la-gold)}.la-opt{opacity:.6}' +
      '.la-est-out{margin-top:1rem}' +
      '.la-est-out--warn{color:var(--la-mid);font-size:.88rem;line-height:1.5}' +
      '.la-est-out--show .la-est-big{font-size:2rem;font-weight:800;color:var(--la-gold);font-family:var(--font-main,sans-serif)}' +
      '.la-est-cap{font-family:var(--font-mono,monospace);font-size:.72rem;text-transform:uppercase;letter-spacing:.06em;color:var(--text-tertiary,#71717a);margin-top:.2rem}' +
      '.la-est-detail{font-size:.82rem;color:var(--text-secondary,#a1a1aa);margin-top:.6rem;line-height:1.5}' +
      '.la-note{font-size:.8rem;color:var(--text-tertiary,#71717a);margin:0 0 1rem}' +
      '.la-sec{margin:1.3rem 0;padding:1.1rem 1.3rem;border:1px solid var(--border,#27272a);border-radius:var(--radius-md,12px);background:var(--surface,#111113)}' +
      '.la-sec-head{display:flex;gap:.9rem;align-items:center}' +
      '.la-sec-grade{flex-shrink:0;width:44px;height:44px;display:flex;align-items:center;justify-content:center;border-radius:var(--radius-sm,6px);font-family:var(--font-main,sans-serif);font-weight:800;font-size:1.4rem;border:1px solid}' +
      '.la-sec-grade--good{color:var(--la-good);border-color:var(--la-good);background:rgba(74,222,128,.08)}' +
      '.la-sec-grade--mid{color:var(--la-mid);border-color:var(--la-mid);background:rgba(251,191,36,.08)}' +
      '.la-sec-grade--bad{color:var(--la-bad);border-color:var(--la-bad);background:rgba(248,113,113,.08)}' +
      '.la-sec-title{font-size:.95rem;font-weight:700;color:var(--text,#fafafa)}.la-sec-title span{font-family:var(--font-mono,monospace);font-size:.68rem;color:var(--text-tertiary,#8a8a94);font-weight:400;text-transform:uppercase;letter-spacing:.06em}' +
      '.la-sec-sub{font-size:.8rem;color:var(--text-secondary,#a1a1aa);margin-top:.15rem;line-height:1.4}' +
      '.la-sec-wp{font-size:.85rem;color:var(--la-mid);margin:.9rem 0 0;line-height:1.5}' +
      '.la-sec-list{list-style:none;padding:0;margin:.8rem 0 0}.la-sec-list li{font-size:.84rem;color:var(--text-secondary,#a1a1aa);padding:.35rem 0 .35rem 1.1rem;position:relative;line-height:1.4}.la-sec-list li:before{content:"›";position:absolute;left:0;color:var(--la-bad)}' +
      '.la-sec-ok{font-size:.85rem;color:var(--la-good);margin:.8rem 0 0}' +
      '.la-sec-foot{font-size:.72rem;color:var(--text-tertiary,#8a8a94);margin:.9rem 0 0;font-family:var(--font-mono,monospace)}' +
      '.la-book{margin-top:1.5rem;padding:1.4rem;border-radius:var(--radius-md,12px);background:linear-gradient(135deg,rgba(201,169,98,.16),rgba(201,169,98,.05));border:1px solid var(--la-gold);text-align:center}' +
      '.la-book-title{font-size:1.15rem;font-weight:700;color:var(--text,#fafafa);font-family:var(--font-main,sans-serif);margin-bottom:.9rem}' +
      '.la-book-btn{display:inline-block;background:var(--la-gold);color:#0b0b0d;padding:.95rem 1.6rem;border-radius:var(--radius-full,9999px);font-weight:700;font-family:var(--font-main,sans-serif);font-size:1.02rem;text-decoration:none;transition:transform .15s,filter .15s}' +
      '.la-book-btn:hover{filter:brightness(1.08);transform:translateY(-1px)}' +
      '.la-book-or{display:block;margin-top:.8rem;font-size:.8rem;color:var(--text-tertiary,#8a8a94);font-family:var(--font-mono,monospace)}' +
      '.la-lead{margin-top:1rem;padding:1.4rem;border:1px solid var(--la-gold);border-radius:var(--radius-md,12px);background:var(--surface-2,#18181b)}' +
      '.la-lead-title{font-size:1.1rem;font-weight:700;color:var(--text,#fafafa);font-family:var(--font-main,sans-serif)}' +
      '.la-lead-sub{font-size:.88rem;color:var(--text-secondary,#a1a1aa);margin:.4rem 0 1rem;line-height:1.5}' +
      '.la-lead-form{display:flex;gap:.6rem;flex-wrap:wrap}.la-lead-input{flex:1;min-width:160px;padding:.85rem 1rem;background:var(--surface,#111113);border:1px solid var(--border,#27272a);border-radius:var(--radius-sm,6px);color:var(--text,#fafafa)}' +
      '.la-lead-input:focus{outline:none;border-color:var(--la-gold)}' +
      '.la-consent{display:flex;gap:.6rem;align-items:flex-start;margin-top:.9rem;font-size:.78rem;color:var(--text-secondary,#a1a1aa);line-height:1.5}.la-consent a{color:var(--gold-text,#e5d4a1)}' +
      '.la-lead-done strong{color:var(--la-good);font-size:1.05rem}.la-lead-done p{margin:.5rem 0 0;color:var(--text-secondary,#a1a1aa);font-size:.9rem}.la-lead-done a{color:var(--la-gold)}' +
      '@media(max-width:560px){.la-score-num{font-size:2rem}.la-est-out--show .la-est-big{font-size:1.6rem}}';
    var style = document.createElement('style');
    style.id = 'la-styles';
    style.textContent = css;
    document.head.appendChild(style);
  }
})();
