/* Conen Digital — Blog ajánló widget · dinamikus, RSS-ből */
(function(){
  var FALLBACK = [
    {t:'Az IKER konfigurátor: hogyan tervezz weboldalt két verzióban',u:'/blog/iker-konfigurator-bemutatasa',c:'CENTAUR',d:'2026.05.10',img:''},
    {t:'Weboldal készítés árak 2026',u:'/blog/weboldal-keszites-arak-2026',c:'Site Factory',d:'2026.05.08',img:''},
    {t:'WCAG 2.2 AA checklist: 12 pont amit most ellenőrizz',u:'/blog/wcag-checklist-kkv',c:'EAA',d:'2026.05.07',img:''}
  ];

  function render(posts) {
    var cards = posts.slice(0, 3).map(function(p) {
      var imgHtml = p.img
        ? '<div style="overflow:hidden;border-bottom:1px solid rgba(255,255,255,.04)"><img src="' + p.img + '" alt="" loading="lazy" style="width:100%;aspect-ratio:3/2;object-fit:cover;display:block"></div>'
        : '';
      return '<a href="' + p.u + '" style="background:rgba(255,255,255,.02);border:1px solid rgba(255,255,255,.05);text-decoration:none;color:inherit;transition:all .35s;display:flex;flex-direction:column;overflow:hidden">'
        + imgHtml
        + '<div style="padding:1.25rem;display:flex;flex-direction:column;gap:.65rem;flex:1">'
        + '<div style="font-family:\'JetBrains Mono\',monospace;font-size:.62rem;color:rgba(255,255,255,.35);text-transform:uppercase;letter-spacing:.1em;display:flex;gap:.5rem"><span style="color:#C9A962">' + p.c + '</span><span>&middot;</span><span>' + p.d + '</span></div>'
        + '<div style="font-size:1rem;font-weight:600;line-height:1.3">' + p.t + '</div>'
        + '<div style="font-family:\'JetBrains Mono\',monospace;font-size:.65rem;color:#C9A962;margin-top:auto;letter-spacing:.08em">Olvasás &rarr;</div>'
        + '</div></a>';
    }).join('');

    var html = '<section id="blogWidget" style="border-top:1px solid rgba(255,255,255,.04);padding:4rem 0 3rem;background:rgba(0,0,0,.3);margin-top:3rem">'
      + '<div style="max-width:1200px;margin:0 auto;padding:0 2rem">'
      + '<div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:2rem;flex-wrap:wrap;gap:1rem">'
      + '<div>'
      + '<div style="font-family:\'JetBrains Mono\',monospace;font-size:.7rem;color:#C9A962;letter-spacing:.18em;text-transform:uppercase;margin-bottom:.5rem">[ Blog ]</div>'
      + '<div style="font-size:1.5rem;font-weight:700">Legfrissebb cikkek</div>'
      + '</div>'
      + '<a href="/blog/" style="font-family:\'JetBrains Mono\',monospace;font-size:.72rem;letter-spacing:.1em;text-transform:uppercase;padding:.6rem 1.2rem;border:1px solid #C9A962;color:#C9A962;text-decoration:none;transition:all .3s">Összes cikk &rarr;</a>'
      + '</div>'
      + '<div style="display:grid;grid-template-columns:repeat(3,1fr);gap:1.5rem">' + cards + '</div>'
      + '</div></section>'
      + '<style>'
      + '#blogWidget a:hover{border-color:rgba(201,169,98,.2) !important;transform:translateY(-2px);box-shadow:0 12px 40px -10px rgba(201,169,98,.08)}'
      + '#blogWidget a img{transition:transform .4s}#blogWidget a:hover img{transform:scale(1.03)}'
      + '@media(max-width:768px){#blogWidget div[style*="grid-template-columns"]{grid-template-columns:1fr !important}}'
      + '</style>';

    var footer = document.querySelector('footer') || document.querySelector('.footer');
    if (footer) footer.insertAdjacentHTML('beforebegin', html);
    else document.body.insertAdjacentHTML('beforeend', html);
  }

  // RSS-ből friss posztok kinyerése
  fetch('/blog/rss.xml')
    .then(function(r) { return r.text(); })
    .then(function(xml) {
      var parser = new DOMParser();
      var doc = parser.parseFromString(xml, 'text/xml');
      var items = doc.querySelectorAll('item');
      var posts = [];
      for (var i = 0; i < Math.min(items.length, 3); i++) {
        var item = items[i];
        var title = item.querySelector('title') ? item.querySelector('title').textContent : '';
        var link = item.querySelector('link') ? item.querySelector('link').textContent : '';
        var pubDate = item.querySelector('pubDate') ? item.querySelector('pubDate').textContent : '';
        var category = item.querySelector('category') ? item.querySelector('category').textContent : '';

        // Dátum formázás
        var d = new Date(pubDate);
        var dateStr = d.getFullYear() + '.' + String(d.getMonth()+1).padStart(2,'0') + '.' + String(d.getDate()).padStart(2,'0');

        // Kép: enclosure-ból vagy media:content-ből, fallback slug-alapú
        var enclosure = item.querySelector('enclosure');
        var img = enclosure ? enclosure.getAttribute('url') : '';
        if (!img) {
          var slug = link.replace(/\/$/, '').split('/').pop();
          if (slug) img = '/blog/blog-images/' + slug + '.png';
        }

        // Link relatívvá
        var u = link;
        try { u = new URL(link).pathname; } catch(e) {}

        posts.push({ t: title, u: u, c: category, d: dateStr, img: img });
      }
      render(posts.length > 0 ? posts : FALLBACK);
    })
    .catch(function() {
      render(FALLBACK);
    });
})();
