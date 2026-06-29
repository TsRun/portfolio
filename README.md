# THE BASEMENT — Sector 00 // Archive

A first-person, retro-horror **portfolio hub**. You wake in a concrete basement
lit only by a hand-held lantern. Three doors line the far wall — each a project.
Walk through one to enter its room.

> Built in three.js with a CRT look: pixelated low-res render, animated film
> grain, scanlines, vignette, flickering fluorescent + neon signage, and a
> procedural Web Audio drone (sub-bass hum, breath, footsteps, ballast buzz).

![The hub](design/screenshots/hub.png)

## Controls

| Action | Input |
| --- | --- |
| Enter / capture mouse | **Click** |
| Look | **Mouse** (drag, or move while pointer is captured) |
| Move | **W A S D** |
| Mute / unmute | **M** |
| Release the mouse | **Esc** |

Walk into a door to travel to a project room; walk through the **EXIT** to come
back to the hub.

## Run it

It's a single static file with no build step. Three.js loads from a CDN, so you
need a network connection and any static server (browsers block pointer-lock and
some fetches on `file://`):

```bash
# from the repo root — pick whichever you have
python3 -m http.server 8000
# or
npx serve .
```

Then open <http://localhost:8000/>.

## Layout

```
index.html              ← the site (standalone three.js, no dependencies bundled)
design/                 ← source-of-truth design export, kept for re-sync
  The Basement.dc.html  ← original Claude Design Component (<x-dc> + logic class)
  support.js            ← the Design Component runtime that mounts a .dc.html
  screenshots/          ← reference captures
README.md
```

## About the implementation

The design was authored in [claude.ai/design](https://claude.ai/design) as a
**Design Component** (`design/The Basement.dc.html`): an `<x-dc>` template plus a
`<script data-dc-script>` logic class (`class Component extends DCLogic`). That
runtime (`design/support.js`) loads React, parses the template, evaluates the
logic class, and mounts it.

`index.html` is a faithful **standalone port** of that component. The game logic
was already pure three.js + imperative DOM — React/`DCLogic` were only a thin
mount shell — so the port keeps the entire tuned game verbatim and replaces only
the shell:

- design-editor props (`atmosphere`, `lanternColor`, `neonColor`, `pixelation`,
  `grain`) become their defaults,
- the `ref`-bound template nodes become real DOM elements, and
- the React lifecycle becomes a single boot call.

The result runs with **no React, no Design Component runtime, and no build** —
just three.js from a CDN. The original export is kept under `design/` so the
component can still be edited in claude.ai/design and re-synced later.

## Project rooms

The three doors lead to `NAUTICHESS`, `MINISHELL`, and `FOREMAN`. Each room is
currently a stub (`// WORK IN PROGRESS`) with a glowing artifact on a pedestal —
ready to be filled in with real project content.
