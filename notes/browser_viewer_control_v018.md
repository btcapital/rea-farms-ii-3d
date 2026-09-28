# Browser viewer control document v018 — tenant-review tool

Date: 2026-09-22
Scope: viewer-only refinement in `viewer_v018/` (port **8018**; v016 on 8016 and v017 on 8017 are untouched and can run at the same time). **No Blender model, GLB geometry, Concept_A_CNSA_ASC geometry, room geometry, viewpoint, room metadata or frozen v001–v017 file was changed.** The only new data is a Level 2 walk grid, derived read-only from the approved v015 model so that Level 2 can be walked.

## Changes from v017

| # | Item | v018 |
| --- | --- | --- |
| 1 | Version label | page title and heading read **"Rea Farms Building II — Review Prototype v018"**; no visible v016 / v017 label remains |
| 2 | Walk speed | unchanged from approved v017: **9.0 ft/s** normal, **18.0 ft/s** with Shift, 0.2 ft collision sub-stepping, mouse-look 0.0032 rad/px |
| 3 | Floor controls | **Level 1 · Level 2 · Both / Exterior** buttons set all layers at once (table below); the old technical checkboxes survive only as overrides under *Advanced layers* |
| 4 | Level 2 walk | new Level 2 walk grid (same 0.25 ft cell size and rules as Level 1, shifted to the 16'-0" slab); eye height 5'-6" above Level 2 (21.5 ft); position remembered per floor; floor buttons move between floors (stairs are not walkable) |
| 5 | Room Labels | checkbox; Concept A labels only; on automatically in Plan mode; **never shown in Walk mode** |
| 6 | Room selection | click a tenant room: yellow floor highlight + orange outline box, room panel top right with name, ID, concept, floor, printed and modeled area; **Clear highlight ×** button and Esc key remove it |
| 7 | Measure | **Measure** button → click two points → distance in feet and inches (nearest ⅛"), plus horizontal, vertical and east-west / north-south components and both points in model coordinates; **Clear Measurement**, **Exit Measure**, Esc |
| 8 | Concept selector | drop-down driven by the `concepts` list in `viewer_data_v018.json` (today: "CNSA ASC — Concept A"); *Show concept* checkbox |
| 9 | Save View Image | downloads the 3D viewport only (no panels) as `BuildingII_v018_<mode>_<floor>_<yyyymmdd-hhmmss>.png` |
| 10 | Presentation Mode | hides Measure, Save View Image, help text, Advanced layers, review note and the status line; keeps Floor, Orbit / Walk / Plan, Reset, concept selector, Show concept, Room Labels, viewpoints; **Exit Presentation Mode** restores everything |
| 11 | Plan mode | Level 1 plan and tenant underlay preserved; plan is framed to the right of the panel; **Level 2 plan** uses the same camera (roof and upper parts hidden, Level 2 slab and walls shown, Level 1 lobby visible through the open-to-below void) |
| 12 | Door warning | preserved in the review note and on every viewpoint jump ("placed here for review; not a documented door connection"); no opening invented |

## Floor button behaviour (what the viewer draws)

| Floor | Orbit | Plan | Walk |
| --- | --- | --- | --- |
| Level 1 | Level 1 interior + concept + envelope; Level 2, roof, solid shell and upper parapets hidden | same, envelope also hidden, north up | Level 1 with Level 2 slab, roof and parapets as ceiling / context |
| Level 2 | Level 1 + Level 2 interior; roof, upper parapets and solid shell hidden | same, north up, slab at 16'-0" | Level 2 with roof lid as ceiling; Level 1 below |
| Both / Exterior | solid exterior with roof, site and landscaping (interiors not drawn inside the solid) | — (plan uses the last floor) | — (Walk switches to Level 1 automatically) |

## Level 2 implementation

`scripts/export_viewer_data_v018.py` opens `models/building_shell_v015.blend` read-only (its SHA-256 is asserted unchanged after the run) and writes `viewer_v018/assets/viewer_data_v018.json` only; the GLB is not re-exported (`viewer_v018/models/building_II_CNSA_ASC_v016.glb` is byte-identical to the approved export). Level 2 grid rule: a 0.25 ft cell is walkable only if it lies under an upward face of the approved Level 2 slab `INT_L2_slab` (223 faces at 16'-0") **and** no base-building or tenant solid stands between 16.5 ft and 22.5 ft (131 blocking objects: Level 2 exterior walls and glazing, lobby / restroom / shaft walls, columns, balcony guards). The lobby open-to-below void, Stair 1 opening, Stair 2 well, elevator hoistway and shafts have no floor and are therefore blocked; the terrace (15'-2", outside the slab) is not walkable. 170,119 open cells (Level 1: 300,753). Documented base-building door openings on Level 2 (200A, 200B, 200C, 210A) are passable because the v014 walls have those gaps; nothing was added.

## Measurement implementation

A ray is cast from the click through the current camera against the visible model groups (helpers, labels, highlight and measurement marks are excluded). The hit point is converted to model feet (`x = X/0.3048`, `y = −Z/0.3048`, `z = Y/0.3048`). Two points give the straight-line distance `√(dx²+dy²+dz²)`, formatted as feet-inches to the nearest ⅛" with the fraction reduced (e.g. `12'-7 1/2"`). Marks are small red spheres joined by a red line. **Spatial review only** — the numbers come from the model, not from a survey.

## Concept-selector architecture

`viewer_data_v018.json → concepts[]`; each entry carries `id`, `label`, `tenant`, `group` (GLB node), `floor`, `rooms`, `viewpoints`, `underlay`, `warning`, `areas`. Selecting an entry hides every other concept's group, rebuilds the viewpoint buttons, labels, underlay and warning, and drives room picking / status text. A future Concept B, Concept C or another tenant is one more entry (and its group in a future GLB export); none was fabricated.

## Controls summary

Floor: Level 1 / Level 2 / Both · Mode: Orbit / Walk / Plan · Reset view · Measure · Save View Image · Presentation Mode / Exit · Tenant concept drop-down · Show concept · Room Labels · Tenant plan underlay · Saved viewpoints (10) · Advanced layers (exterior, base interior, site, landscaping) · Review note · Room panel with Clear highlight · Walk: W A S D / arrows, Shift = fast, drag to look, Esc clears · Address-bar parameters for bookmarks (`?mode= &floor= &vp= &pos=x,y&yaw= &room= &measure=x1,y1,z1,x2,y2,z2&present=1`).

## Validation (2026-09-22)

GLB loads, no console errors · orbit drag / zoom / reset (real mouse) · Level 1 walk W / S / A / D = 9.0 ft/s each, Shift + W = 18.0 ft/s, eye 5.5 ft · Level 2 walk W = 9.0, Shift + W = 18.0, strafe = 9.0 ft/s, eye 21.5 ft · Level 1 wall stop at y 90.65 (wall face 91.5) · Level 2 stops: balcony / void edge y 72.45, south wall y 24.55, restroom east wall x 149.35; documented door 200A passable · floor switching remembers the position on each floor · concept selector and Show concept toggle · all 10 viewpoints · room click by mouse (OFFICE A-045) and by parameter (A-051 / A-052) with highlight and clear · Room Labels on / off, hidden in Walk · measurement: `ftin` unit tests (12'-7 1/2", 10'-0", 0'-6", 3'-0 1/4", 205'-0"), 205 ft grid = 205'-0", 3-4-5 triangle = 5'-0", floor-to-floor = 16'-0", two real clicks 50 ft apart on the plan = 50'-0", OR width 62.05−44.14 = 17'-10 7/8" · plan mode Level 1 and Level 2 · underlay on Level 1 only · Save View Image produces a PNG blob (20.9 KB test frame) · Presentation Mode enters and exits with the right elements hidden / shown · **wall-tunneling sweeps re-run with Shift at the 0.1 s frame cap**: Level 1 OR A-051 16,288 runs and PRE/POST A-002 8,032 runs — 0 escapes; Level 2 restroom 205 5,712 runs — 0 through walls (492 left through the documented door 200C, as expected); Level 2 whole slab 79,848 runs — 0 ended in a solid or off the slab · launcher `viewer_v018\start_viewer.bat` serves the page on 8018 · **frozen files: 273 (v001–v017 incl. both earlier viewers, tenant PDF, exports) SHA-256 identical**.

## Performance

Same 8.4 MB GLB; page ready in 2–4 s; about 0.9–1.0 M triangles with site and planting on; walk and orbit about 7 ms per frame and plan about 33 ms on this computer's integrated Intel graphics (unchanged from v016). The Level 2 grid adds 9 KB to the data file.

## Known limitations

Stairs cannot be climbed; floors are changed with the buttons · terrace not walkable · flat colours, no shadows (review tool, not a rendering) · measurement snaps to whatever surface is under the cursor (walls, floor, glass), not to corners · labels are shown only for rooms with a printed area and only for the active concept · the Level 2 plan has no tenant concept (none exists) · Save View Image relies on the browser's download setting (Edge / Chrome save to Downloads without asking; a browser set to "ask where to save" will prompt) · tested in Microsoft Edge (Chromium); Safari, phones and tablets untested · the local server must be running while the viewer is used.

## How to open v018

1. Open File Explorer and go to the project folder `Rea Farms II 3D`.
2. Open the folder **`viewer_v018`**.
3. Double-click **`start_viewer.bat`** (if Windows shows "Windows protected your PC", click **More info**, then **Run anyway**).
4. A small black window appears and your browser opens `http://127.0.0.1:8018/` a few seconds later. Leave the black window open.
5. When "Loading Building II model…" disappears: choose **Level 1** or **Level 2**, then **Orbit**, **Walk** or **Plan**.
6. When finished, close the browser tab, then the black window.
