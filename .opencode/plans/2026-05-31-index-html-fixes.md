# index.html Critical Fixes Implementation Plan

> **For agentic workers:** Inline execution — batching edits to `index.html` with verification after each batch.

**Goal:** Fix all CRITICAL, HIGH, and key MEDIUM issues found in the senior-level analysis of `index.html` — CSP, WCAG/EAA compliance, AX infrastructure, form errors, and CSS/JS quality.

**Architecture:** Single-file HTML page — all changes go to `index.html` except two new AX files. Edits batched by logical groups to minimize read/edit cycles.

**Tech Stack:** Vanilla HTML, CSS, JS. No build step.

---

### Task 1: Critical Security + Legal + Font Fixes (C1, C2, M7, M8)

**Files:** Modify `index.html` (head section, form section, footer)

**Changes:**
- Add CSP meta tag
- Add `&display=swap` to Google Fonts URL
- Add `<noscript>` fallback for fonts
- Add privacy notice checkbox to contact form + data-processing disclosure in footer

### Task 2: Critical WCAG — Skip Link + `<main>` Landmark (C3, H1)

**Files:** Modify `index.html`

**Changes:**
- Add skip-to-content link as first focusable element
- Add `.skip-link` CSS
- Wrap all content between `<nav>` and `<footer>` in `<main id="main-content">`

### Task 3: AX Infrastructure — Create Missing Files (H2)

**Files:** Create `/.well-known/llms.txt`, `/.well-known/agents.txt`

**Changes:**
- Create `llms.txt` with site summary (Hungarian)
- Create `agents.txt` with basic agent configuration

### Task 4: Form Error Handling — Replace `alert()` (H3)

**Files:** Modify `index.html` (script section)

**Changes:**
- Replace `alert()` in form error handler with inline `role="alert"` error message

### Task 5: Modal Hidden Buttons — Fix Keyboard Focus (H4)

**Files:** Modify `index.html` (CSS + JS)

**Changes:**
- Change `.cert-modal-nav.hidden` CSS to use `visibility: hidden`
- Set `tabindex="-1"` on hidden buttons via JS

### Task 6: Marquee Pause + Canvas Transcript Link (H7, H8)

**Files:** Modify `index.html`

**Changes:**
- Add `prefers-reduced-motion: reduce` to stop marquee
- Add `aria-describedby` to canvas linking to transcript
- Add `id="narrationTranscript"` to the `<details>` element

### Task 7: Portfolio Heading Structure Fix (M5)

**Files:** Modify `index.html` (portfolio section)

**Changes:**
- Change `<a><h3>` pattern to `<h3><a>` in all portfolio items

### Task 8: Other Quality Fixes (M3, M11, M12, M2)

**Files:** Modify `index.html`

**Changes:**
- Remove dead CSS `.nav-links a::before { content: '' }`
- Add `:focus-visible` to `.portfolio-item`
- Remove `will-change` from `.screenshot-window img`
- Remove or guard console.error/warn calls
