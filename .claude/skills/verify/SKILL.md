---
name: verify
description: Verify portfolio page changes by serving project/ and driving the real page in Playwright at the viewports the change targets
---

# Verify the portfolio page

The site is a single self-booting HTML file (`project/Portfolio.dc.html`, mirrored to `project/index.html`). No build step.

## Launch

```sh
cd project && python3 -m http.server 8931 --bind 127.0.0.1   # background
```

Open `http://127.0.0.1:8931/` with the Playwright MCP tools. This serves `index.html` — run `cp project/Portfolio.dc.html project/index.html` first or you'll test stale markup.

## Drive

- Resize to the target viewports: 390×844 (phone), 320×568 (SE), 768/1024 (tablet), 1280+ (desktop regression).
- Overflow check at each width: `document.documentElement.scrollWidth <= innerWidth`.
- Mobile-specific state to assert: `.sav-app` / `.fm-app` have `style.zoom === '1'` at ≤720px and a fractional zoom above; `.nav-burger` visible / `.nav-links` hidden at ≤720px.
- `(pointer: coarse)` rules (e.g. `.fdf-canvas` `touch-action: pan-y`) need a real mobile-emulated context: `browser.newContext({ isMobile: true, hasTouch: true })` — a bare viewport resize keeps a fine pointer.
- Interactions worth exercising: burger open → link click closes menu and scrolls; EN/FR toggle (also inside the menu); Savana card flip; Foreman goal → Delegate adds a task.
- Console must stay free of errors (info logs from `[dc-runtime] x-import` are normal).

## Gotchas

- `html{scroll-behavior:smooth}` makes `scrollIntoView()` async — use `scrollTo({behavior:'instant'})` before screenshots.
- Screenshots save to the repo root by default; move them into `.playwright-mcp/` (gitignored) when done.
- The mobile layer lives in the helmet `<style>` as `.class{…!important}` overrides (breakpoints: 720px phone, 721–1099px tablet) because all element styles are inline.
