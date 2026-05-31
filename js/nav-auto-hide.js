(function () {
  var style = document.createElement('style');
  style.textContent = '.nav--hidden{transform:translateY(-100%)!important;top:0!important}';
  document.head.appendChild(style);

  var nav = document.querySelector('.nav');
  if (!nav) return;

  var lastY = 0, ticking = false;
  function onScroll() {
    var currentY = window.scrollY;
    if (currentY > lastY && currentY > 100) {
      nav.classList.add('nav--hidden');
    } else if (currentY < lastY) {
      nav.classList.remove('nav--hidden');
    }
    lastY = currentY;
    ticking = false;
  }

  window.addEventListener('scroll', function () {
    if (!ticking) {
      requestAnimationFrame(onScroll);
      ticking = true;
    }
  }, { passive: true });
})();
