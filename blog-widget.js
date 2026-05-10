/* Conen Digital — Blog ajánló widget · auto-inject */
(function(){
  const POSTS = [
    {t:'Az IKER konfigurátor: hogyan tervezz weboldalt két verzióban',u:'/blog/iker-konfigurator-bemutatasa',c:'CENTAUR',d:'2026.05.10'},
    {t:'Weboldal készítés árak 2026: mennyibe kerül egy céges weboldal?',u:'/blog/weboldal-keszites-arak-2026',c:'Site Factory',d:'2026.05.08'},
    {t:'WCAG 2.2 AA checklist: 12 pont amit most ellenőrizz',u:'/blog/wcag-checklist-kkv',c:'EAA',d:'2026.05.07'},
    {t:'EAA megfelelés 2026: érint-e a céged?',u:'/blog/eaa-megfeleles-2026',c:'EAA',d:'2026.05.06'},
    {t:'Mi az a CENTAUR-modell?',u:'/blog/centaur-modell',c:'CENTAUR',d:'2026.05.05'},
    {t:'99-es PageSpeed mobilon: a Motyán case study',u:'/blog/99-pagespeed-motyan-case-study',c:'Case Study',d:'2026.05.04'},
  ];
  const html = `
<section id="blogWidget" style="border-top:1px solid rgba(255,255,255,.04);padding:4rem 0 3rem;background:rgba(0,0,0,.3);margin-top:3rem">
  <div style="max-width:1200px;margin:0 auto;padding:0 2rem">
    <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:2rem;flex-wrap:wrap;gap:1rem">
      <div>
        <div style="font-family:'JetBrains Mono',monospace;font-size:.7rem;color:#00f0ff;letter-spacing:.18em;text-transform:uppercase;margin-bottom:.5rem">[ Blog ]</div>
        <div style="font-size:1.5rem;font-weight:700">Legfrissebb cikkek</div>
      </div>
      <a href="/blog/" style="font-family:'JetBrains Mono',monospace;font-size:.72rem;letter-spacing:.1em;text-transform:uppercase;padding:.6rem 1.2rem;border:1px solid #00f0ff;color:#00f0ff;text-decoration:none;transition:all .3s">Összes cikk →</a>
    </div>
    <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:1.5rem">
      ${POSTS.slice(0,3).map(p => `
      <a href="${p.u}" style="background:rgba(255,255,255,.02);border:1px solid rgba(255,255,255,.05);padding:1.5rem;text-decoration:none;color:inherit;transition:all .35s;display:flex;flex-direction:column;gap:.75rem">
        <div style="font-family:'JetBrains Mono',monospace;font-size:.62rem;color:rgba(255,255,255,.35);text-transform:uppercase;letter-spacing:.1em;display:flex;gap:.5rem"><span style="color:#00f0ff">${p.c}</span><span>·</span><span>${p.d}</span></div>
        <div style="font-size:1rem;font-weight:600;line-height:1.3">${p.t}</div>
        <div style="font-family:'JetBrains Mono',monospace;font-size:.65rem;color:#00f0ff;margin-top:auto;letter-spacing:.08em">Olvasás →</div>
      </a>`).join('')}
    </div>
  </div>
</section>
<style>
#blogWidget a:hover{border-color:rgba(0,240,255,.2) !important;transform:translateY(-2px);box-shadow:0 12px 40px -10px rgba(0,240,255,.08)}
@media(max-width:768px){#blogWidget div[style*="grid-template-columns"]{grid-template-columns:1fr !important}}
</style>`;
  const footer = document.querySelector('footer') || document.querySelector('.footer');
  if (footer) footer.insertAdjacentHTML('beforebegin', html);
  else document.body.insertAdjacentHTML('beforeend', html);
})();
