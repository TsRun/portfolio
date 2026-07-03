# Prototype design recuperation — pixel-faithful replicas

Date: 2026-07-03 · Status: approved by user (approach B, full design)

## Goal

The three interactive prototypes in `project/Portfolio.dc.html` (Savana, Foreman, FdF) are styled
in the portfolio's own cream aesthetic and don't resemble the real applications. Rebuild each mock
window as a **pixel-faithful, real-scale replica** of the actual app, shrunk to fit with CSS `zoom`,
while keeping (and upgrading) the live interactivity.

Design sources (extracted 2026-07-03):
- Savana: `TsRun/Savana@master` — `src/style.css`, `src/App.vue`, `src/components/SmurfCard.vue`.
- Foreman: local `/Users/apple/Projects/foreman` — `src/index.css` + `src/components/**` (inline styles).
- FdF: `TsRun/Fil-de-Fers` is README-only → authentic look is a plain macOS MiniLibX window.

## Scaling mechanism (approach B)

Author each replica at true app dimensions inside a `zoom`-frame:
- Replica root has fixed real width (Savana ≈ 1100px, Foreman ≈ 1060px).
- A `ResizeObserver` on the wrapper sets `el.style.zoom = min(1, wrapperWidth / realWidth)`.
- `zoom` participates in layout + hit-testing, so clicks work untransformed.
- Fallback if the DC renderer rejects `zoom`: `transform: scale(z)` + `transform-origin: 0 0` +
  wrapper `height = realHeight * z` compensation.
- FdF needs no zoom (canvas is fluid).

## Language rule

Replica internals are fixed to the real app's language (Savana: EN labels, FR tooltips;
Foreman: EN). They do NOT flip with the portfolio EN/FR toggle. Surrounding portfolio copy stays
bilingual; mock captions updated ("hit Load", "press ↵ Delegate").

---

## 1. Savana replica

Real-scale ≈ 1100 × 740. All values below are ground truth from the repo.

### Tokens (`src/style.css :root`, verbatim)

```css
--bg-primary:#0a0a0f; --bg-secondary:#12121a; --bg-tertiary:#1a1a25;
--bg-card:#16161f; --bg-card-hover:#1e1e2a;
--accent-primary:#6366f1; --accent-secondary:#8b5cf6;
--accent-gradient:linear-gradient(135deg,#6366f1 0%,#8b5cf6 100%);
--accent-glow:rgba(99,102,241,0.4);
--success:#22c55e; --warning:#f59e0b; --error:#ef4444; --info:#3b82f6;
--text-primary:#f8fafc; --text-secondary:#94a3b8; --text-muted:#64748b;
--border-subtle:rgba(255,255,255,0.04); --border-active:rgba(99,102,241,0.4);
/* radius: sm 6 / md 10 / lg 16 / xl 24 / full 9999 · font: Inter 400/500/600/700, base 14px/1.5 */
```

Card base: `linear-gradient(145deg, rgba(22,22,31,.9), rgba(18,18,26,.95))`, 1px `--border-subtle`,
radius 16, `backdrop-filter: blur(10px)`; hover: lighter gradient, indigo border-glow,
`translateY(-2px)`, `0 12px 40px rgba(0,0,0,.25), 0 0 0 1px rgba(99,102,241,.3)`.

### Shell

- **Titlebar 32px**: `--bg-secondary`, bottom border subtle, padding-left 16. Left: 20×20 logo
  (radius 4) + "Savana" 0.75rem `--text-secondary`. Right: three 46px buttons (— ▢ ✕), hover
  `--bg-tertiary`, close hover `#ef4444` + white.
- **Sidebar 260px**: `--bg-secondary`, right border. Header pad 24: 40×40 logo radius 10 +
  "Savana" (700, 1rem) over "v2.0" (0.75rem muted). Nav pad 16: items gap 16, pad 8/16, radius 10;
  active = `--accent-gradient` + white ("Accounts" active; "Friends" idle). Footer pad 16:
  profile pill on `--bg-tertiary` radius 10 — 36px gradient initial avatar, username over
  "Online" (`--success`), 32px logout icon btn (hover error/white).
- **Content header** pad 24/32 on `--bg-secondary`: "My Accounts" 1.5rem/700 + "4 accounts"
  0.875rem muted; right: search input 220px (`--bg-tertiary`, radius 10, placeholder "Search...");
  select "SoloQ" 120px; "+ Add Account" green ghost (`rgba(16,185,129,.15)` grad bg, `#10b981`,
  border `rgba(16,185,129,.4)`); "Resave All" = `--accent-gradient` white; buttons pad 8/16
  radius 8 weight 600 0.875rem.
- **Accounts grid**: `repeat(auto-fill, 380px)` centered, gap 24, pad 32, scrollable.

### SmurfCard (380px, min-height 400, pad 24, column gap 16)

a. Header: name 1.25rem/700 over `#TAG` 0.875rem muted (gap 2); right gradient LVL badge
   (pad 8/16, radius 10, level 1.125rem/700 white over "LVL" 0.625rem/500 rgba(255,255,255,.7)
   uppercase ls .5px).
b. Rank row (pad 16, `rgba(255,255,255,.03)`, radius 10, subtle border): rank emblem img
   96×96 contain, `drop-shadow(0 4px 8px rgba(0,0,0,.4))`, `scale(1.1)`; "GOLD II" 1rem/600 +
   "{lp} LP" 0.875rem `--text-secondary`; right two stat stacks (value 1.125rem/700 over label
   0.7rem muted): WR% (≥60 `#22c55e`, ≥50 `#f59e0b`, else muted) and Games.
c. Stats row (gap 8): role pill (`#1a1a25`, radius 10, pad 6/10: 20px role SVG white-filtered +
   "{pct}%" 0.75rem/600); KDA pill ("7.2 / 4.1 / 6.8" — K `#22c55e` / D `#ef4444` / A `#3b82f6`,
   sep muted; ratio chip `rgba(0,0,0,.2)` radius 4 — ≥4 `#ffd700`, ≥3 `#22c55e`, ≥2 `#94a3b8`);
   champions right-aligned (`margin-left:auto`): 3 × (32px icon radius 4 border 2px subtle +
   WR% 0.6rem/600 colored).
d. Actions footer (top border `rgba(255,255,255,.1)`, pad-top 16, gap 8): `.action-btn` column
   pill (pad 10/8, `rgba(30,30,42,.8)`, radius 8, `#a1a1aa`, label 0.65rem/600 uppercase):
   "User", "Pass", session-save (has-token = green tint `rgba(34,197,94,.25)`/`#22c55e`),
   **"Load"** `flex:2`, `--accent-gradient`, white — hover lift + `0 4px 16px rgba(99,102,241,.4)`.
e. Card back (3D flip on card click, `perspective:1000px`, rotateY .5s
   `cubic-bezier(.23,1,.32,1)`): name+tag header; inset `rgba(0,0,0,.2)` panel with uppercase
   0.7rem labels Username/Password over dark inputs (`#1a1a25`, radius 6, masked dummies);
   footer "Delete Session" red ghost + "Save" gradient.

### Interactions

- Card hover: real glow/lift. Card click: 3D flip front↔back.
- **Load click** (stopPropagation): toast sequence top-right of replica window, real style
  (`#16161f`, radius 10, pad 16/24, 3px colored left border, slideInRight): "Recovering session…"
  (info) → "League is starting" (success) → account becomes connected (Load shows ✓ state).
- Search box + queue select: visual only. Drag-to-reorder: skipped.

### Data (4 accounts, from previous data pass — real model shape)

Midlane Diff#EUW (Diamond III, 63 LP, 148W/129L, WR 54, Lv 214, MID 76%, KDA 3.6,
Ahri 19g 63% / Syndra 12g 58% / Hwei 7g 52%) · Kayn Enjoyer#KAYN (Emerald II, 74 LP,
96W/71L, WR 61, Lv 88, JUNGLE 83%, KDA 4.1, Kayn 41g 66% / Viego 15g 60% / Briar 9g 55%) ·
ward diff#0000 (Platinum IV, 31 LP, 52W/49L, WR 51, Lv 143, SUPPORT 71%, KDA 3.0,
Thresh 22g 55% / Rakan 14g 57% / Renata 6g 50%) · ADC Andy#EUW (Gold I, 12 LP, 38W/41L,
WR 48, Lv 67, BOTTOM 68%, KDA 2.7, Jinx 17g 53% / Caitlyn 13g 46% / Smolder 8g 50%).

### Assets (hotlinked, with fallback)

Base `https://raw.githubusercontent.com/TsRun/Savana/master/public/`:
- `SavanaLogo.jpg` (titlebar + sidebar)
- `assets/ranks/{diamond|emerald|platinum|gold}.png`
- `assets/roles/{middle|jungle|support|bottom}.svg` (filter `brightness(0) invert(1)`)
- `assets/champions/{Ahri|Syndra|Hwei|Kayn|Viego|Briar|Thresh|Rakan|Renata|Jinx|Caitlyn|Smolder}.png`

Every `<img>` gets an `onError` fallback → hide img, show initial-letter tile. Verify each URL
with `curl -sI` during implementation; swap any 404 champion for one that exists.

Font: add Inter (400/500/600/700) to the Google Fonts link in the helmet.

---

## 2. Foreman replica

Real-scale ≈ 1060 × 620. Ground truth from local source (inline styles + `index.css`).

### Tokens (light theme)

```css
--bg:#f5f4ed; --panel:#faf9f5; --panel-2:#efece1; --ink:#141413; --ink-2:#3d3d3a;
--muted:#5e5d59; --faint:#87867f; --line:#f0eee6; --line-2:#e8e6dc; --line-strong:#d1cfc5;
--sel:#ece7d8; --accent:#c96442; --accent-hover:#b5573a; --accent-ink:#faf9f5;
--success:#6e8d45; --warn:#b58238; --danger:#aa4434;
/* fonts: Newsreader serif display / system sans 13px / Iosevka mono */
```

### Layout tree

```
TopBar h54 --panel, border-bottom --line
grid: 312px | minmax(0,1fr) | 318px
  TaskListPane  --panel-2, border-right --line
  RoomTimeline  --bg
  TaskDetailPane --panel, border-left --line
StatusStrip h32 --panel, border-top --line
```

### TopBar

Brand mark 25×25 SVG (1024 viewBox: rect rx 229 fill `#f1eee4` stroke `#1f1e1c`@.09; three bars
x300 rx59 h118: y290 w424 `#c96442`, then w340 `#211f1b`, then w262 `#211f1b`) + "Foreman"
serif 16/500 · "/" faint · project switcher btn (`--bg`, border `--line-2`, radius 8, pad 5/11:
"portfolio-site" serif 14/500 + branch chip "⎇ main" (border `--line-2`, radius 5, 10.5px muted)
+ "▾" faint) · spacer · Tasks/Map seg (border `--line-2` radius 8; active = ink bg +
`--accent-ink`, inactive = `--bg` + muted, 11px pad 5/12) · "Accounts" btn (11.5px muted) ·
"⚙" 30×30.

### TaskListPane (312px)

Header pad 13/15/11 border-bottom: "Tasks" serif 16/500 + mono count faint 11 + filter seg
All/Active/Done. List pad 11 gap 7. **TaskCard**: radius 9, `--bg`, pad 10/11, border 1px
(`selected: --ink` / `waiting: --accent` / else `--line`), border-left 2px (same or transparent),
selected bg `--sel`. Row 1: ComplexityBadge + title 12.5/1.4 (+ 7px accent dotpulse dot if
waiting). Row 2 (mt 11): 18px avatar chip (radius 5, tint bg, brand-color mono letter 8px/600) +
agent name 11 muted + spacer + StatusPill.

Badges (verbatim `.badge`): 10px/600 uppercase ls .06em pad 2/7 radius 5, 1px border;
low `--success`, medium `--warn`, high `--danger` — each `color-mix` 12-13% bg / 40-42% border.
Pills (verbatim `.pill`): 10.5px/600 pad 2/8 radius 11 border `--line-strong` bg `--panel`
muted; running = ink bg + `--accent-ink` + 9px spinning ring; done = success tinted;
classified renders "ready"; icons: pending ●, waiting ?, done ✓, failed ✕.

Composer (border-top, `--panel`, pad 11/12/12): textarea rows 2 (`--bg`, border `--line-2`,
radius 9, 12.5px, placeholder **"Give Foreman a goal — it picks the agent…"**, Enter submits) +
right ink btn **"Delegate ↵"** (12px pad 7/14 radius 8) + transient "✓ routed to {name}"
`--success` 11px.

### RoomTimeline (center, --bg)

Header pad 12/22: "Room" serif 16/500 over "agents coordinating" 11 faint; right overlapping
avatar stack (25px chips, ml -6, `box-shadow 0 0 0 2px var(--bg)`). Body pad 18/22, inner
max-width 760 centered, vertical rail 2px `--line-2` at left 14. Message: 30px avatar
(radius 8, ring 3px `--bg`) + header (name bold 13 + kind chip 10/600 pad 1.5/8 radius 6,
color k / bg k@13% + recipient 12/500 muted + mono time 9.5 faint right) + body 13/1.58
`--ink-2` max 640. Kinds: delegate "delegates to" `#c96442` · ask "asks" `#b58238` ·
answer "answers" `#6e8d45` · report "reports to" `#5e5d59` · blocked "is blocked by" `#aa4434`.

### TaskDetailPane (318px)

Header pad 13/16: badge + serif title 15/500 + meta row (18px avatar + name 11 muted + pill);
action row mt 12: ink "▶ Run" / outline "↻ Retry" (11.5px pad 6/13 radius 7). Tabs pad 9/14/0:
Changes n / Run / Files — 12px pad 7/11, active = 2px ink underline + 600. Content pad 12/14/18.
- Run tab = ConversationThread (verbatim CSS): `.who` 10px uppercase ls .12em faint ("YOU" /
  "CLAUDE"); user bubble ink bg white 12.5px radius 9 pad 9/13 max 80%; claude log `--panel-2`,
  border `--line`, border-left 2px `--line-strong`, radius 9, pad 11/14, mono 11.5/1.8;
  line colors: tool = ink 600, dim/cmd = faint, ok = `--ink-2`, done = ink 600 + dashed top
  border; live cursor 7×12 ink block blinking.
- Changes tab: bordered card (`--panel-2`, radius 9) of git rows — mono 11.5, 20px status code
  column (M/A/?? — ?? faint) + path `--ink-2`. Empty: dashed "No file changes yet."
- Files tab: mono 11.5 tree, `▸` dirs / `·` files faint, indent 16/depth.

### StatusStrip

h 32, pad 0/16, gap 16, 11px muted: 6px accent dot + "{n} working" · "·" · "{n} tasks · {n} done"
· "·" · mono "⎇ main" · spacer · mono faint "${x} today" · "·" · mono faint "foreman v2".

### Provider identity (hard-coded)

claude C `#c96442`/`#f3e3db` · codex X `#46443f`/`#e7e5dd` · gemini G `#5b6ea8`/`#e2e6f1` ·
aider A `#6e8d45`/`#e6eed8` · foreman F `#c96442`/`#f3e3db` · you Y `#141413`/`#ece7d8`.
Avatar chip = square, radius 28% of size, tint bg, mono letter 600 at 42% size.

### Interaction remapping (existing state machine, new skin)

- Goal input → composer textarea; Enter → classify() → new TaskCard (badge word LOW/MEDIUM/HIGH,
  avatar per provider, pill "ready"/running) + transient "✓ routed to {agent}".
- Run → pill flips to running (ink + spinner), detail pane switches to Run tab, log pool lines
  stream into the CLAUDE mono log with blinking cursor; YOU bubble = the task title/goal.
- Room: seeded coordination messages; on delegate/run, append Foreman "delegates to" {agent}
  message (+ one ask/answer pair for flavor).
- Done → pill done, Changes tab count updates (static plausible git rows per agent pool).
- StatusStrip counts + cost live-update (existing cents logic).
- Seed tasks: keep 3 current tasks (Backend/Frontend/Tests) mapped to real statuses
  (running / waiting→"ready" / done).

---

## 3. FdF window

Keep canvas + projection + `pyra.fdf` data (previous pass). Frame → authentic macOS window:
- Titlebar ~28px flat `#ececec`, bottom border `#d0d0d0`, radius-top 10, centered
  title "fdf" 13px `#4a4a4a` system-ui 500; traffic lights left (12px circles gap 8:
  `#ff5f57`, `#febc2e`, `#28c840`).
- Canvas: pure black `#000` (MiniLibX default), keep height-gradient wireframe.
- Controls (zoom/relief/reset) move BELOW the window, restyled as portfolio mono captions
  (Iosevka 10px uppercase, cream-on-paper) — the real binary has no in-window UI.
- Window: radius 10, `box-shadow 0 24px 60px rgba(0,0,0,.35)`, 1px `rgba(0,0,0,.2)` border.

---

## 4. Cross-cutting implementation notes

- All three replicas live in `project/Portfolio.dc.html` (DC prototype; inline styles;
  bindings via `{{ }}` / `sc-for` / `sc-if`; logic in the single `Component` class).
- New keyframes needed: `spin360`, `dotpulse`, `blink`, `slideInRight` (+ existing pulse).
- New Component state: savFlipped (id|null), savToasts[], savConnected (id), foreman room
  messages, detail tab. Reuse existing timers/tick machinery.
- Captions under each mock updated to match new interactions; captions stay bilingual.
- Verification: node syntax-check of the DC script block; template-binding cross-check
  (every `{{ root }}` resolves); `curl -sI` every hotlinked asset URL (expect 200);
  grep for leftover old-mock classes/labels.

## Risks

- Hotlinked GitHub assets may fail under strict CSP → onError fallback tiles (initial letters).
- ~8–9px effective text at 0.6 zoom — accepted (approach B choice).
- DC renderer must tolerate `zoom` → transform-scale fallback documented above.
- `color-mix()` needs a modern browser — fine for a design prototype (DC host is Chromium).
