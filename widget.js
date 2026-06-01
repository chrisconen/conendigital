(function () {
  "use strict"
  if (window.__conenChatLoaded) return
  window.__conenChatLoaded = true

  var WIDGET_HOST = 'https://nexus.conendigital.hu';

  var COLORS = ["#00f0ff", "#bf00ff", "#ff6b00", "#00ff88", "#ff3366", "#4488ff", "#ffcc00", "#00ffcc", "#ff00aa"]

  function injectStyles() {
    var css = [
      "@keyframes conen-pulse{0%,100%{opacity:1;transform:scale(1)}50%{opacity:.55;transform:scale(.95)}}",
      "@keyframes conen-drift{0%{transform:translateY(0) scale(1);opacity:.9}100%{transform:translateY(-120px) scale(0);opacity:0}}",
      ".conen-chat-fab{position:fixed;bottom:28px;right:28px;display:flex;align-items:center;justify-content:center;width:76px;height:76px;border-radius:38px;background:#0a0a0a;color:#fff;border:1px solid rgba(0,240,255,.5);cursor:pointer;box-shadow:0 8px 32px rgba(0,0,0,.5),0 0 28px -4px rgba(0,240,255,.55);z-index:2147483646;transition:transform .2s,box-shadow .25s,border-color .25s;font-family:'JetBrains Mono',ui-monospace,monospace;font-size:13px;font-weight:600;letter-spacing:.15em;text-transform:uppercase;padding:0}",
      ".conen-chat-fab::before{content:'';width:10px;height:10px;border-radius:50%;background:#00f0ff;box-shadow:0 0 12px #00f0ff;margin-right:6px;animation:conen-pulse 1.6s ease-in-out infinite}",
      ".conen-chat-fab:hover{transform:translateY(-2px);border-color:#00f0ff;box-shadow:0 12px 44px rgba(0,0,0,.6),0 0 36px -2px rgba(0,240,255,.85)}",
      ".conen-chat-fab:focus-visible{outline:2px solid #00f0ff;outline-offset:3px}",
      ".conen-chat-fab[data-open='true']::before{display:none}",
      ".conen-chat-fab[data-open='true']{padding-left:0;padding-right:0}",
      ".conen-chat-particle{position:fixed;pointer-events:none;z-index:2147483645;border-radius:50%;animation:conen-drift 1.8s ease-out forwards}",
      ".conen-chat-frame-wrap{position:fixed;bottom:116px;right:28px;width:420px;height:660px;max-height:calc(100vh - 150px);border-radius:18px;overflow:hidden;box-shadow:0 30px 60px rgba(0,0,0,.7),0 0 0 1px rgba(0,240,255,.18);z-index:2147483647;display:none;background:#0a0a0a;transform:translateY(8px);opacity:0;transition:transform .25s ease,opacity .25s ease}",
      ".conen-chat-frame-wrap.open{display:block;transform:translateY(0);opacity:1}",
      ".conen-chat-frame{width:100%;height:100%;border:0;display:block;background:#0a0a0a}",
      "@media (max-width:500px){.conen-chat-frame-wrap{right:0;bottom:0;width:100vw;height:100vh;max-height:100vh;border-radius:0}.conen-chat-fab{bottom:16px;right:16px;width:64px;height:64px;font-size:11px}}",
      "@media (prefers-reduced-motion:reduce){.conen-chat-fab::before{animation:none}.conen-chat-frame-wrap{transition:none}.conen-chat-particle{display:none}}",
    ].join("")
    var style = document.createElement("style")
    style.textContent = css
    document.head.appendChild(style)
  }

  function spawnParticle(btn) {
    var rect = btn.getBoundingClientRect()
    var cx = rect.left + rect.width / 2
    var cy = rect.top + rect.height / 2
    var el = document.createElement("div")
    el.className = "conen-chat-particle"
    var size = 3 + Math.random() * 5
    var color = COLORS[Math.floor(Math.random() * COLORS.length)]
    var dx = (Math.random() - 0.5) * 60
    el.style.cssText =
      "width:" + size + "px;height:" + size + "px;background:" + color + ";" +
      "left:" + (cx - size / 2) + "px;bottom:" + (window.innerHeight - cy) + "px;" +
      "box-shadow:0 0 " + (size * 2) + "px " + color + ";" +
      "animation:conen-drift 1.8s ease-out forwards;" +
      "--dx:" + dx + "px"
    el.style.translate = "var(--dx,0px) 0px"
    document.body.appendChild(el)
    setTimeout(function () { el.remove() }, 2000)
  }

  function mount() {
    injectStyles()

    var wrap = document.createElement("div")
    wrap.className = "conen-chat-frame-wrap"

    var iframe = document.createElement("iframe")
    iframe.className = "conen-chat-frame"
    iframe.title = "NEXUS AI — Conen Digital"
    iframe.setAttribute("loading", "lazy")
    wrap.appendChild(iframe)

    var btn = document.createElement("button")
    btn.className = "conen-chat-fab"
    btn.type = "button"
    btn.setAttribute("aria-label", "NEXUS AI megnyitása")
    btn.setAttribute("aria-expanded", "false")
    btn.textContent = "NEXUS"

    var particleTimer

    function startParticles() {
      if (particleTimer) return
      spawnParticle(btn)
      particleTimer = setInterval(function () { spawnParticle(btn) }, 1200)
    }

    function stopParticles() {
      if (particleTimer) {
        clearInterval(particleTimer)
        particleTimer = null
      }
    }

    function closeWidget() {
      wrap.classList.remove("open")
      btn.setAttribute("aria-expanded", "false")
      btn.setAttribute("data-open", "false")
      btn.textContent = "NEXUS"
      startParticles()
    }

    btn.addEventListener("click", function () {
      if (!iframe.src) iframe.src = WIDGET_HOST + "/"
      var isOpen = wrap.classList.toggle("open")
      btn.setAttribute("aria-expanded", isOpen ? "true" : "false")
      btn.setAttribute("data-open", isOpen ? "true" : "false")
      btn.textContent = isOpen ? "×" : "NEXUS"
      if (isOpen) { stopParticles() } else { startParticles() }
    })

    window.addEventListener("message", function (event) {
      if (event.data && event.data.type === "close-chat") {
        closeWidget()
      }
    })

    document.body.appendChild(wrap)
    document.body.appendChild(btn)

    startParticles()
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", mount)
  } else {
    mount()
  }
})()
