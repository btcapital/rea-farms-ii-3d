# Building I — interactive browser viewer v015: validation and completion report

Date: 2026-09-25. Status: **built and validated, NOT approved.** Control: `BI_browser_viewer_control_v015.md`.
Test environment: the Claude desktop built-in browser (Chromium) at 1600 × 1000, served by `server.py --capture` (capture endpoint on only for this validation; off in the shipped launcher), NVIDIA RTX A1000. Every screenshot below was written by the viewer's own capture routine and visually inspected.

## 1. Load

| Check | Result |
| --- | --- |
| Page load, console | loads; no errors. One console **warning** from the three.js vendor build (`THREE.Clock` deprecation) — not from the viewer code |
| GLB | 13.0 MB, 824 nodes with meshes (920 three.js meshes after multi-material splits), 301,964 triangles |
| Frame rate (1600 × 1000, everything on, exterior aerial) | 58 fps, ≈ 950 draw calls, 278 k triangles |
| Load time | ≈ 3 s on this machine |

## 2. Layer / floor / concept tests (test API `window.BI`, triangles rendered)

| Toggle | Triangles | Note |
| --- | --- | --- |
| all default layers, aerial | 290,697 | |
| SITE off | 183,294 | site is the heaviest group (terrain + hardscape) |
| CONTEXT off | 193,149 | |
| LANDSCAPE off | 241,785 | independent vegetation toggle |
| EXTERIOR_SHELL / GLAZING / ROOF / BASE_* / STRUCTURE / CNSA off | each reduces the count by its group | all 16 groups toggle |
| GRID on | +468 | default off |
| CONCEPT_A/B/C on | +0 | empty groups (listed, disabled in the selector) |
| CNSA OFF (selector "None / Base Building") | −8,280 | CNSA partitions + zone plates disappear; collision rectangles drop from 1,344 to 825 on L1 |
| Floors L1 / L2 / Mezzanine / Both | clip at 10.0 / 26.0 / 20.5 ft / none | captures 03–06 |

Captures: `viewer_v015_03_L1_orbit_cutaway_cnsa_on.png`, `_04_..._cnsa_off.png`, `_05_L2_orbit_cutaway.png`, `_06_mezzanine_orbit.png`, `_01/_02` exterior.

## 3. Walk mode (deterministic simulation through the test API; fixed time step)

| Test | Setting | Result |
| --- | --- | --- |
| forward, normal, 1 s @ 60 fps (open courts) | 9.0 ft/s | displacement **9.000 ft** |
| forward, Shift, 1 s @ 60 fps | 18.0 ft/s | **18.000 ft** |
| backward / strafe right / strafe left (arrow) / diagonal, 1 s | 9.0 ft/s | 9.000 / 9.000 / 9.000 / 9.000 ft (diagonal normalised) |
| wall: corridor 102 heading south into the corridor south wall, 2 s | | stopped at y = 62.55 (wall face 61.55 + 1.0 ft radius), reason "core_corridor_102_south_wall" |
| column: heading north into column C-10 (180, 30) W10X77, 2 s | | stopped at y = 28.50, reason "column C-10"; Shift @ 2 fps: stopped at 28.40 |
| elevator hoistway (L2, corridor 204 heading south), 2 s | | stopped at y = 80.60 (hoistway outer face 79.58 + radius), reason "elevator hoistway (8 in shaft wall)"; L1 approach stops at the elec 103/104 core wall first (documented) |
| stair void / stair: lobby heading south into the lobby stair, 3 s | | stopped at y = 61.65, reason "BB_stair_lobby_stair_A6.11" |
| slab edge: L2 heading west from (80, 66) toward the lobby double-height void (slab edge x 71.01), 3 s | | stopped at x = 72.05, reason "slab edge / floor opening" |
| anti-tunnelling worst case: Shift (18 ft/s) at 5 fps, 2 fps and **1 fps** (18 ft per frame) into a 0.5 ft wall | | stopped at y = 62.60 every time (sub-steps ≤ 0.2 ft) — no tunnelling |
| documented door passage: door 102b (A7.01, tag at 164.95, 57.35) through the corridor 102 south wall, normal speed | | passes: y 66 → 48 in 2 s (18 ft, uninterrupted); with Shift @ 3 fps passes the door and stops 6 ft later at a **CNSA partition** (CNSA on) |
| CNSA collision toggle | | CNSA on: 1,344 rectangles; off: 825 |
| per-floor position memory | | switching floors and back returns to the stored position (state API) |
| mezzanine walk | | floor 13.021 ft, walkable region = mezzanine slab; capture `viewer_v015_walk_vp_mezz.png` |

Walk captures (eye 5'-6"): `viewer_v015_walk_vp_lobby / core_L1 / cnsa_L1 / cnsa_L1_cnsa_off / courts / L2_office / cnsa_L2 / mezz / shell_L2 / gallery.png`.

## 4. Viewpoints

13 viewpoints; the 9 walk viewpoints classified at load: 8 DOCUMENTED WALKABLE ROUTE (green), 1 VIEWPOINT TELEPORT (gallery 234 — reachable only by stairs, which are not walkable in v015). No viewpoint needed a position or orientation adjustment in the final data. The status line reports "on DOCUMENTED WALKABLE ROUTE" / "TELEPORTED" for the walker's current position.

## 5. Rooms, highlight, labels

| Test | Result |
| --- | --- |
| click on the "121 Training Courts" tag in Plan L1 (real mouse click) | info panel: Training Courts, 121, L1, BASE BUILDING, area (not available), boundary "not extracted (documented tag position only)", source A1.01 |
| click in the CNSA Level 1 zone (real mouse click) | zone highlighted (blue fill + outline), panel: 16,216 sq ft, boundary documented (A1.01 MOB Shell 150-S extent), status existing tenant (rev 8, 2/18/2026) |
| Esc / Clear Highlight | selection and highlight cleared |
| labels | 79 spaces (56 tags, 23 zones); Plan mode auto-on (44 visible on L1), Walk off by default, toggle works; labels are DOM elements with pointer-events none (navigation unaffected) |

Captures: `viewer_v015_room_highlight_plan_L1.png`, `_07_plan_L1_underlay_labels.png`, `_08_plan_L1_labels.png`, `_09_plan_L2_underlay_labels.png`, `_10_plan_L2_cnsa_off.png`, `_11_plan_L2_core_zoom.png`.

## 6. Measurement (known model dimensions)

| Test | Expected | Measured |
| --- | --- | --- |
| Level 1 slab top → Level 2 slab top at (100, 40), same screen point with BASE_L2 toggled | 15'-4" (15.333 ft) | total 15'-4" (15.33 ft), horizontal 0'-0", vertical 15'-4" |
| hoistway inside width, plan L1 clicks 0.05 ft inside each inner face (91.30 → 99.87) | 8.57 ft (inside 8'-8" = 8.67 documented) | 8'-6 7/8" (8.57 ft) horizontal, 0 vertical |

Readout shows feet-inches and decimal feet, both points' coordinates and "SPATIAL REVIEW ONLY". Captures `viewer_v015_measure_floor_to_floor.png`, `_measure_hoistway.png`.

## 7. Plan mode, underlays, presentation, save image, launcher

| Test | Result |
| --- | --- |
| Plan mode north-up, pan / wheel zoom | works; L1 and L2 plan viewpoints |
| underlay toggle | A1.01 under L1, A1.02 under L2 / mezzanine; the model walls and columns sit on the drawn walls (captures 07, 09) |
| Presentation Mode | tools, layers, notes, status hidden; mode / floor / CNSA / concept / viewpoints / Exit kept (checked by computed style) |
| Save View Image button (real click) | wrote `BuildingI_v015_plan_L1_20260925_151318.png` (copy in renders as `viewer_v015_save_view_image_button_output_...png`); saved images carry labels, measurement readout and a footer |
| `start_viewer.bat` | started with port 8115 already in use → server fell back to **8116**, served `index.html` (200), the GLB as `model/gltf-binary` (12,999,464 bytes), `app.js` as `text/javascript`, capture endpoint disabled (`{"capture": false}`), wrote `viewer_url.txt`, opened the default browser. A first attempt exposed a Windows port-reuse bug (SO_REUSEADDR) — fixed in `server.py` before this test |
| Node and PowerShell fallbacks | present in the launcher chain (`server.js`, `server_fallback.ps1`); not exercised on this machine because Python is installed |

## 8. Integrity

| Check | Result |
| --- | --- |
| `BI_freeze_BuildingI_v014_approved.json` (263 files, v001–v014) | PASS after the export and at the end of the pass |
| `BI_freeze_sources_BuildingI_longpath_v001.json` (1,231 source files) | PASS |
| v014 Blender model | not saved (script never calls save; sha256 `…` recorded in the export report equals the frozen hash) |
| exported geometry vs v014 | 824/824 objects: names, triangle counts and bounding boxes identical (0 mismatches); split roof faces add up |
| CNSA separate | 4 objects in group CNSA / node `EXISTING_TENANT/CNSA`; not in any BASE group; toggled independently |
| Future Concept A/B/C | empty nodes, 0 triangles |
| no undocumented openings | collision built only from the v014 rectangles/faces; no primitive removed or cut |
| Building II viewers | not opened, not modified (project/Building II manifest unchanged apart from the 17 files somebody moved earlier — reported at v010, untouched by this work) |

## 9. What did not work / limits

- Walk mode cannot climb stairs (blocked footprints); Level 2 and the mezzanine are entered by floor button or viewpoint. Gallery 234 is therefore a teleport.
- Exterior doors are closed (the lites are solid); the walker cannot go outside.
- Interior lighting is a readability setting, not the v013 render look.
- The pane's animation loop pauses while the test harness runs scripts, so captures are taken with an explicit render call — no effect on normal use.

## 10. Files created in this pass

```
exports/Building_I/BI_model_v014_viewer_v015.glb
viewer_BI_v015/  (index.html, src/app.js, src/style.css, model/, data/, plans/, vendor/three/, server.py, server.js, server_fallback.ps1, start_viewer.bat, README_LAUNCH.txt)
notes/Building_I/BI_browser_viewer_control_v015.md
notes/Building_I/BI_browser_viewer_validation_v015.md
notes/Building_I/BI_viewer_data_v015.json
notes/Building_I/BI_viewer_glb_v015_export_report.json
notes/Building_I/manifests/BI_freeze_BuildingI_v014_approved.json
notes/Building_I/manifests/BI_freeze_BuildingI_v015_pending_approval.json
scripts/Building_I/BI_export_viewer_glb_v015.py
scripts/Building_I/BI_make_viewer_data_v015.py
renders/Building_I/viewer_v015_*.png (25)
```

Next decision for the owner: **approve or redirect v015** (then freeze v001–v015). Not started: Concept A / B / C.
