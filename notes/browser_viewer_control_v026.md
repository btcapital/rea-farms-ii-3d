# Browser viewer control document v026 — final viewer-only polish of v025 (model v023)

**STATUS (2026-09-23): APPROVED — CURRENT APPROVED BUILDING II VIEWER v026 (model v023). See `notes/building_II_status_2026-09-23.md`.**

Date: 2026-09-23 · **Viewer version v026** (`viewer_v026/`, port **8026**) = viewer v025 with two visual adjustments: a subtler walnut texture and a neutral ambient colour balance. Model v023 unchanged (read only, hash asserted); v025 not overwritten. All functionality is the v025 / v024 code and data; the export asserts the data file's grids, stair surfaces, furniture collision, floors, walk settings, tenant concepts and lobby viewpoints equal viewer v024's (v025's data is the same).

## Files
`exports/building_II_model_v023_viewer_v026.glb` (+ identical copy in `viewer_v026/models/`): **12,505,452 bytes** (v025: 12,515,768); 762 nodes, 178 meshes, 126 materials, 5 images; lobby group 13 mesh nodes, 35 primitives, 12,028 triangles, 30 materials (identical to v024 / v025). `viewer_v026/assets/viewer_data_v026.json`, `scripts/export_viewer_v026.py`. Captures `renders/viewer_v026_lobby_01_entrance.png`, `_03_level2_overlook.png`, `_04_feature_wall.png`, `_05_seating.png`.

## 1. Walnut (viewer texture only; wall geometry and box pattern untouched)
| | v025 | v026 |
| --- | --- | --- |
| Grain octaves (control points across the 8 ft repeat) | 28 / 72 / 190 / 480 at amplitudes 1.0 / 0.6 / 0.38 / 0.22 | **+ a fine octave of 1,024 points at 0.20**, 480-point octave 0.22 → 0.26; sum renormalised (÷ 2.44) |
| Grain contrast | tone ± 9 % | **± 11 %** (still low; noticeable up close, not across the lobby) |
| Board-to-board variation | 3-point drift × 0.03 across the width | **12-point variation (about 8 in. boards) × 0.045 + 3-point drift × 0.02** |
| Slow variation along the height | ± 2.5 % | unchanged |
| Base colour (linear) | 0.295 / 0.185 / 0.112 | **0.28 / 0.188 / 0.122** (red down, green / blue up: less red-orange, neutral mid-dark brown) |
| Method | tileable 1-D value noise, no sine terms, ± 5 px drift | unchanged |
Same texture on the treads and chair frames (their base tints unchanged). No gloss change (roughness 0.55).

## 2. Lighting colour balance (viewer code only)
| Light | v025 | v026 |
| --- | --- | --- |
| Hemisphere sky / ground | white 0xffffff / warm grey 0x9a9488, 1.9 | **neutral 0xf6f8fb / neutral grey 0xa4a4a2, 1.9** |
| Sun | white, 1.9 | unchanged |
| Lobby point light at the entrance (124.5, 98, 9 ft) | warm 0xffd6a6, 22 | **neutral daylight 0xf2f5fa, 22** |
| Lobby point light east side (131, 78, 9 ft) | warm 0xffd6a6, 14 | slightly less warm 0xffe2c2, 14 |
| Pendant-cluster and wood-wall point lights | warm 0xffd6a6 | unchanged (3500 K intent) |
| Tone mapping / exposure | ACES filmic, 1.0 | unchanged |
Result: walls and floor read neutral, cushions stay warm off-white, the wood wall and its graze pools stay warm, daylight through the glazing stays natural.

## Validation (2026-09-23, browser)
No console errors · Stair 1 ascent / descent identical to v020 / v022 / v024 / v025 (same positions and heights, largest step 0.44 ft, guard stop at y 81.4) · furniture collision identical (chair / table / planter cells blocked with the concept on, chair cell open when off, aisle open, walk into a chair stops at y 91.8) · Lobby toggle, Base / Concept, six lobby views, Lobby button, exterior, Level 2 plan, Level 1 orbit, measure (5'-0"), tenant viewpoint, tenant concept selector, room labels, presentation mode as in v025 · draw calls 1,359 in both versions, same triangles; GPU-flushed idle frame time 1.7–3.4 ms per frame in both v025 and v026 (measured in the app's browser pane after the screenshot captures finished; one transient 150–220 ms reading on the overlook view was a one-off stall not reproduced) · manifest: all 420 Building II files of v001–v025 SHA-256 identical (v023 model and the v025 GLB / code included); source documents unchanged.

## How to open
As before, folder **`viewer_v026`**, address `http://127.0.0.1:8026/`.
