# Building I — interactive browser viewer v015: control document

Date: 2026-09-25
Gate: BUILDING I INTERACTIVE BROWSER VIEWER (skill gate 6). Not authorised: tenant concepts A/B/C (gate 7).
Controlling model: `models\Building_I\BI_interior_base_v014.blend` — owner-approved 2026-09-25 as the INTERIOR BASE-BUILDING BASELINE; opened read-only, never saved (`blend_saved: false` in the export report; sha256 recorded). Frozen: `manifests\BI_freeze_BuildingI_v014_approved.json` (263 files, PASS).
Starting structured data: `BI_interior_base_viewer_v014.json` (unchanged) + `BI_interior_base_data_v014.json` (unchanged, read for the wall / CNSA / slab rectangles, columns and doors).

## 1. Outputs of this pass

| Output | Path |
| --- | --- |
| GLB export (new) | `exports\Building_I\BI_model_v014_viewer_v015.glb` — 12,999,464 bytes (13.0 MB), sha256 in the export report |
| Export report | `notes\Building_I\BI_viewer_glb_v015_export_report.json` (groups, per-object tris/bbox verification, materials, extracted collision primitives) |
| Viewer data (new, versioned) | `notes\Building_I\BI_viewer_data_v015.json` (copy in `viewer_BI_v015\data\`) |
| Viewer folder | `viewer_BI_v015\` — 18.7 MB: `index.html`, `src\app.js`, `src\style.css`, `model\` (GLB copy), `data\`, `plans\` (2 underlays), `vendor\three\` (three.js 0.186.1 MIT, offline), `server.py`, `server.js`, `server_fallback.ps1`, `start_viewer.bat`, `README_LAUNCH.txt` |
| Scripts | `scripts\Building_I\BI_export_viewer_glb_v015.py` (Blender, headless), `BI_make_viewer_data_v015.py` (system python + Pillow) |
| Validation captures | `renders\Building_I\viewer_v015_*.png` (25) |
| Notes | this file; `BI_browser_viewer_validation_v015.md` |

Port: `127.0.0.1:8115` (local only; falls back to 8116…8125 if busy and prints the URL). No publishing, no cloud, no installation. Building II viewers (`viewer_v017`…`viewer_v026`) were not opened or modified.

## 2. Sources used

| Source | Used for |
| --- | --- |
| v014 model (read-only) | all geometry (824 objects exported: every render-visible v014 object except the two v001 reference planes and the cameras/sun) |
| v014 viewer / data JSON | levels, columns (84, S601), hoistway, stairs, fixed-room zones (20), tenant zones (3), constraints, areas, wall rectangles (617 L1 / 532 L2), CNSA rectangles (519 / 169), L2 slab rectangles + gallery polygon, door schedule |
| Rev 14 A1.01 (p.26) / A1.02 (p.27), text layer (`pdftotext -bbox-layout`) | documented room tags: 56 room number + name pairs (33 L1, 22 L2, 1 mezzanine) with their printed positions, registered with the v008 grid-bubble fits |
| Rev 14 A1.01 / A1.02 page renders at 150 dpi (`pdftocairo`) | plan underlays, cropped to the registered building window only (no rescale, no distortion) |
| v013 presentation data | flat viewer colours (base colours of the v013 shaders; procedural shaders cannot be exported) |
| CNSA A100 rev 8 | via the v014 CNSA rectangles only |
| Building II viewer standard (as stated by the owner) | 9.0 / 18.0 ft/s, eye 5'-6", WASD + mouse look, two-click measurement — implemented from the owner's description, the Building II viewer code was not read |

## 3. Coordinates and units

Building I feet, origin grid 1 × A at FFE 661.75, +X east, +Y north, z above LVL-01 (v001). The GLB is glTF Y-up in metres (Blender scene units); the viewer scales the scene by 1/0.3048 so three.js (x, y, z) = (X ft, Z ft, −Y ft). Every JSON datum, the status line, the measurement readout and the room extents are Building I feet. Plan mode is north-up.

## 4. GLB export method (`BI_export_viewer_glb_v015.py`)

- Opened `BI_interior_base_v014.blend` headless; all edits below are in memory only, the file is never saved (verified: v014 approved manifest PASS after the export).
- Groups (glTF node extras `bi_group`, `bi_level`, `bi_collection`; also listed per object in the viewer data):

| Group | Source collections | Objects / tris |
| --- | --- | --- |
| EXTERIOR_SHELL | 01_Shell (wall faces), 07_Facade_regions_v005, 03_Canopy | 87 / 3,848 |
| EXTERIOR_GLAZING | 04_Openings (376 lite placeholders) | 376 / 4,512 |
| ROOF | ROOF_* faces split from the 01_Shell prisms (8 objects), 02_Parapet_screens, BI_Z6_mech_screen | 16 / 192 |
| SITE | 08_Site terrain, hardscape, walls/structures | 26 / 107,403 |
| LANDSCAPE | 09_Landscape trees, shrubs, groundcover, beds, context trees | 244 / 64,610 |
| CONTEXT | 08_Site context (roads, Building II mass) | 5 / 97,548 |
| GRID | 05_Grid_control (default off) | 39 / 468 |
| BASE_L1 | BB_L1_slab_on_grade, BB_core_walls_L1, BB_fmk_program_partitions_L1 | 3 / 3,832 |
| BASE_L2 | BB_L2_composite_slab, BB_mezzanine_slab_233, BB_core_walls_L2, BB_fmk_program_partitions_L2 | 4 / 3,328 |
| BASE_ENVELOPE | BB_extwall_inner_faces, _TWS1_translucent, BB_extwall_window_reveals | 3 / 5,239 |
| BASE_VERTICAL | 5 stairs + 5 guards, hoistway walls, pit slab | 12 / 1,604 |
| STRUCTURE | BB_columns_S601, BB_roof_deck_underside_TOS | 2 / 1,100 |
| CNSA | CNSA_partitions_L1/L2, CNSA_tenant_zone_L1/L2 | 4 / 8,280 |
| CONCEPT_A / B / C | empty collections → one empty node each | 0 tris |

- Roof split: the v008 shell prisms carry their roof faces (ROOF_JM_TPO material) as top faces of the same object; those faces were moved to new `ROOF_<prism>` objects (vertex positions untouched; walls + roof triangle counts add up to the source count, asserted) so the roof can be toggled.
- Materials: every Cycles node tree replaced (in memory) by a flat Principled BSDF — base colour from the v013 data base colour, else a palette for procedural/placeholder materials (brick tone, PNL3 grey, pavers charcoal, glazing blue-grey α 0.45, TWS1 white α 0.85, canopy glass α 0.30, CNSA zone plate α 0.35). No textures. Colour source recorded per material in the export report.
- Export options: GLB, Y-up, modifiers applied (none exist), extras on, materials exported, no images, no Draco, full collection hierarchy as nodes, cameras/lights off.
- Verification (in the script): every exported object present in the GLB by name, triangle count identical, world bounding box identical within 0.01 ft (0 mismatches over 824 objects, 301,964 triangles); the 8 split prisms untouched in the scene.

## 5. Viewer architecture (data-driven)

`src\app.js` reads `data\BI_viewer_data_v015.json` — floors, groups, concepts, objects→group map, materials, spaces, viewpoints, underlays, collision, levels/columns/stairs/areas/constraints (copied from v014). Nothing building-specific is hard-coded except the default camera positions; a second building or a new concept is a data change:

- Modes: ORBIT (three.js OrbitControls), WALK (own controller), PLAN (orthographic, north up, own pan/zoom).
- Floors: L1 / L2 / Mezzanine / Both-Exterior. In Orbit and Plan a floor sets a global clip plane (L1 cut at 10.0 ft, Mezzanine 20.5 ft, L2 26.0 ft) and hides the CONTEXT group; Both/Exterior removes the clip. In Walk a floor sets the walker's floor elevation (0 / 13.021 / 15.333) and remembers the last position per floor. Entering Walk from Both/Exterior goes to Level 1.
- Concept selector (data list): None / Base Building → no tenant group; Existing CNSA → group CNSA; Concept A / B / C → groups CONCEPT_A/B/C, flagged `empty: true` so they are listed but disabled. The "Existing CNSA ON/OFF" button and the selector are the same state. Adding a tenant concept later = model it in FUTURE_CONCEPTS/Concept_X, re-run the export (the group node already exists), set `empty: false` and, if wanted, add its spaces/viewpoints/collision rectangles to the data file. No viewer code change is needed.
- Layers: one checkbox per group (advanced panel).
- Spaces (clickable, pick planes on a separate raycast layer so they never block navigation): 20 core bounding zones (BASE BUILDING, "interpreted (v014 core bounding zone)"), 3 tenant/shell zones (CNSA L1 boundary documented per A1.01; CNSA L2 east limit interpreted ±2 ft; MOB Shell 2300 remaining), 56 documented room tags (label position only, "boundary not extracted"). Info panel: name, number, level, category (BASE BUILDING / EXISTING CNSA / FUTURE CONCEPT), area when available, boundary status, source. No room data was fabricated: rooms without a documented number show "(not documented)"; tags with no area show "(not available)".
- Labels: CSS2D DOM labels with `pointer-events: none`; auto-on in Plan, off in Walk, user toggle in Orbit; filtered by floor (Level 2 view shows L2 + mezzanine); CNSA labels only when CNSA is on.
- Measurement: two raycast clicks on visible geometry (respecting the clip plane) → total, horizontal, vertical, both points, feet-inches (nearest 1/8 in) + decimal feet; labelled SPATIAL REVIEW ONLY; also drawn into saved images.
- Save View Image: renders the frame, composites the visible labels and a footer (model/viewer version, mode, floor, concept, timestamp), downloads `BuildingI_v015_<mode>_<floor>_<timestamp>.png`.
- Presentation mode: hides tools, layers, notes, status; keeps mode, floor, CNSA/concept, viewpoints, Exit.
- Plan underlays: `plans\BI_underlay_L1_A1.01_rev14_150dpi.jpg`, `..._L2_A1.02_...jpg` placed as textured planes at floor + 0.06 ft with the exact registered extents (A1.01: x −25.0…305.0 ft window → pixels 65–4707 × 577–4094; A1.02 likewise; registration = the v008 fits `x_pt = 199.81 + 6.7500x, y_pt = 1795.91 − 6.7502y` (A1.01) and `197.71 / 1796.00` (A1.02), RMS 0.027 ft). Crop only; the x/y scale difference of the fit itself (6.7500 vs 6.7502 pt/ft, 0.003 %) is preserved, nothing is rescaled to force a match. Mezzanine uses the A1.02 sheet (the lab 233 is drawn on it).

## 6. Collision (documented solid geometry only)

Walker: radius 1.0 ft, eye 5'-6", body band floor + 0.5…6.5 ft, 9.0 ft/s, Shift 18.0 ft/s, WASD / arrows, pointer-lock mouse look (drag fallback). Movement is sub-stepped at ≤ 0.2 ft per step (a frame at 18 ft/s and 1 fps = 90 sub-steps), each step tested, with axis-separated sliding.

Blocking primitives (all from v014 data or the v014 meshes, none invented):

| Primitive | Source | Count |
| --- | --- | --- |
| interior walls (rated core to deck, program partitions 10 ft) | v014 `walls_L1` / `walls_L2` rectangles (the A1.01/A1.02 wall pairs) | 617 / 532 |
| CNSA partitions (only while CNSA is on) | v014 `cnsa.rects_L1/L2` | 519 / 169 |
| columns | v014 columns, d × bf boxes (web ∥ y, the v014 assumption) | 84 |
| elevator hoistway | inside + 8 in shaft wall, pit −5 to 33 ft | 1 |
| stairs (footprints, both landings' floors) | bounding boxes of the 5 v014 stair meshes | 5 |
| exterior wall inner faces (closed, incl. TWS1) | vertical faces of `BB_extwall_inner_faces` / `_TWS1_translucent` (segments) | 752 |
| exterior lites (glass = closed; exterior doors are inside the storefront lites and are treated as closed) | 04_Openings bounding boxes | 376 |
| slab edges / floor openings (walkable region) | L1: outline of `BB_L1_slab_on_grade` top face (74 + 4 vertex loops); L2: the 30 A1.00b slab rectangles + gallery polygon; mezzanine: the mezzanine slab extent | — |

Doors and openings: the gaps between the v014 wall rectangles ARE the openings as drawn (the door swing interrupts the wall pair on A1.01/A1.02); nothing was cut for walking convenience. Where the CNSA drawing does not show an opening none exists in the viewer.

Documented-route classification: at load the viewer flood-fills a 0.5 ft grid per floor from a route origin — L1: inside the entry vestibule 100 (main entrance); L2: corridor 202 at the elevator (documented vertical circulation); mezzanine: between the two mezzanine stairs — and marks every walk viewpoint DOCUMENTED WALKABLE ROUTE or VIEWPOINT TELEPORT. The status line shows the same for the walker's current position. Stairs are not climbable in v015 (blocked footprints); Level 2 is reached with the floor buttons / viewpoints.

## 7. Viewpoints (eye 5'-6" above the floor)

| # | Viewpoint | Floor | Eye (x, y) | Route |
| --- | --- | --- | --- | --- |
| 1 | Main entrance lobby | L1 | 33, 67 | walkable |
| 2 | Level 1 core — corridor 102 at the elevator | L1 | 84, 66 | walkable |
| 3 | Existing CNSA Level 1 (MOB Shell 150-S) | L1 | 140, 30 | walkable |
| 4 | Training courts 121 | L1 | 196, 128 | walkable |
| 5 | Level 2 office area (Taylor Capital suite) | L2 | 86, 140 | walkable |
| 6 | Existing CNSA Level 2 | L2 | 100, 30 | walkable |
| 7 | Mezzanine — Sports Science Lab 233 | MEZZ | 195, 194 | walkable |
| 8 | Base-building shell — MOB Shell 250-S east ("SHELL 2300") | L2 | 230, 30 | walkable |
| 9 | Gallery 234 | L2 | 266, 104 | **TELEPORT** — the gallery is reached only by the gallery stair 126 / south stair 231 (stairs not walkable in v015) |
| 10–11 | Exterior porte cochère (v013 hero camera), north-west aerial | orbit | | |
| 12–13 | Plan Level 1, Plan Level 2 | plan | | |

If a viewpoint's eye falls inside a wall it is moved to the nearest free spot (≤ 8 ft, reported); if its look direction is blocked within 8 ft the view turns to the longest free run (reported per viewpoint in the test API). Neither happened for the final list.

## 8. Assumptions, limits and open items (none resolved silently)

- Viewer colours are flat (v013 shaders are procedural); lighting is a non-physical hemisphere + sun for readability (walk mode brighter). Not a rendering baseline — v013 remains the presentation baseline.
- Stairs not climbable; exterior doors closed; walking stays inside the building. The slab on grade has no hoistway opening in v014 (the pit is below the slab), so a plan-mode measurement inside the hoistway hits z = 0.
- Room 101 (lobby) has no numeric tag in the A1.01 text layer → not listed; 119's tag reads "Sports Training Area" (the full name is Architech Sports Training Area, 3-line tag). Room names come from the tag text only.
- Space areas are only given where v014 published them (tenant zones); core bounding zones show the bounding-box area of the zone, labelled as such.
- Route classification depends on the extracted wall gaps; a missing door gap would show as TELEPORT, never as a fabricated opening.
- `THREE.Clock` deprecation warning printed by the three.js 0.186.1 vendor build (console warning, not an error).
- Carried unchanged: I-1…I-4 (v014) and all exterior/site items (G-1…G-6, G-15, F-1…F-9, SC-1, SC-3, LC-2).

## 9. Regeneration

```
blender --background models/Building_I/BI_interior_base_v014.blend --python scripts/Building_I/BI_export_viewer_glb_v015.py
pdftotext -bbox-layout -f 26 -l 27 <Rev14.pdf> words.html ; pdftocairo -png -r 150 -f 26 -l 27 <Rev14.pdf> plans/p
python scripts/Building_I/BI_make_viewer_data_v015.py words.html plans/
```
(both scripts refuse to overwrite existing outputs)
