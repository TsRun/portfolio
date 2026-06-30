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
assets/projects/        ← in-world exhibit visuals shown on each room's monitor
  notichess.png         ← NotiChess tactics-trainer screenshot
  foreman.png           ← Foreman v2 workspace UI (rendered from its design)
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

- design-editor props (`atmosphere`, `lanternColor`, `neonColor`, `grain`) become
  their defaults,
- the `ref`-bound template nodes become real DOM elements, and
- the React lifecycle becomes a single boot call.

The standalone also **modernises the look**: it renders at full resolution with
antialiasing and anisotropic, smoothly-filtered textures (the original's
low-res `pixelation` pass is dropped), and the retro CRT overlays are toned down
(scanlines removed, grain and vignette eased back).

The render is **fill-bound** (≈800 triangles, ~40 draw calls — geometry is free;
device-pixel count and per-fragment shading are the whole cost), so the scene is
tuned accordingly:

- **Adaptive resolution.** Rendering starts at the crisp cap (`min(devicePixelRatio, 2)`)
  and a governor steps the render scale down a notch only if it can't hold ~60fps,
  then settles. A capable GPU stays at full sharpness; weak / high-DPI / on-battery
  machines stay smooth instead of dropping frames.
- **Cheaper shading.** The large matte surfaces (floor, walls, ceiling, columns,
  wood) use `MeshPhongMaterial` instead of the full PBR `MeshStandardMaterial` —
  visually identical for rough non-metal concrete under these point lights, but a
  much lighter fragment shader where it matters most. Metallic fixtures keep PBR.
- **Shared geometry.** Box/plane sizes recur across the four rooms (door frames,
  walls, exhibit panels), so one `BufferGeometry` is reused per size — roughly
  halves the GPU buffer count (43 → 23 in the hub).
- **Texture hygiene.** UI/screenshot textures skip mipmap generation, and project-
  room textures are uploaded up front so the first door transition doesn't hitch.

The result runs with **no React, no Design Component runtime, and no build** —
just three.js from a CDN. The original export is kept under `design/` so the
component can still be edited in claude.ai/design and re-synced later.

## Project rooms

Each of the three doors opens onto a project room. Inside, a self-lit **monitor**
on one wall shows a visual of the project and a **placard** on the other wall
gives a short write-up (what it is, the stack, and where to find it). The
monitor's glowing bezel matches the door's accent colour.

| Door | Project | Visual | What it is |
| --- | --- | --- | --- |
| `NOTICHESS` | [NotiChess](https://github.com/TsRun) | tactics-trainer screenshot | Desktop chess studio — play/import/organize games + a tactics trainer over ~4.1M real games (Tauri 2 · React · Rust). |
| `MINISHELL` | [minishell](https://github.com/TsRun/minishell) | procedural CRT terminal | École 42 systems project — a Bash-like shell in C (pipes, redirections, env, signals, builtins). |
| `FOREMAN` | [foreman](https://github.com/TsRun) | live workspace UI | macOS task queue for AI coding agents — auto-classifies & routes tasks to role agents that run in parallel and coordinate (Tauri 2 · React · Rust · SQLite). |

The two screenshot visuals live in `assets/projects/`; MINISHELL's terminal is
drawn procedurally at runtime (a C/shell project has no UI screenshot), and every
placard is rendered to a canvas in-engine — so only the two `.png`s are assets.
