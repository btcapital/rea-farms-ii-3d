# Browser viewer control document v025 — visual tuning of the approved v024 viewer (model v023)

Date: 2026-09-23 · **Viewer version v025** (`viewer_v025/`, port **8025**) = viewer v024 with viewer-only visual tuning. Model v023 unchanged (read only, hash asserted). v024 not overwritten. Navigation, collision grids, furniture footprints, Stair 1 surfaces, toggles, viewpoints, tenant controls, measure, plan, orbit, walk, exterior and level controls are the v024 code and data: the export asserts the v025 data file's grids, stair surfaces, furniture collision, floors, walk settings, tenant concepts and lobby viewpoints equal v024's.

## Files
`exports/building_II_model_v023_viewer_v025.glb` (+ identical copy in `viewer_v025/models/`): **12,515,768 bytes** (v024: 12,585,740); 762 nodes, 178 meshes, 126 materials, 5 images; lobby group 13 mesh nodes, 35 primitives, 12,028 triangles, 30 materials (all identical counts to v024). `viewer_v025/assets/viewer_data_v025.json`. `scripts/export_viewer_v025.py`. Captures `renders/viewer_v025_lobby_01_entrance.png`, `_03_level2_overlook.png`, `_04_feature_wall.png`, `_05_seating.png`.

## Exact visual changes (viewer only)
| Area | v024 | v025 |
| --- | --- | --- |
| Walnut texture (wall, treads, chair frames) | 512² tile, sum of 40 sines across the width (periodic, wavy), tone ±28 %, base 0.36 / 0.215 / 0.115 (warm-orange), 4 ft repeat | **1024 × 2048 tile from tileable 1-D value noise (4 octaves, no periodic terms) with ±5 px drift along the grain, tone ±9 % plus slow board-to-board variation, base 0.295 / 0.185 / 0.112 (neutral mid-dark brown), 8 ft repeat**; vertical grain kept |
| Tone mapping / exposure | linear output, no tone mapping | **ACES filmic tone mapping, exposure 1.0**; hemisphere 2.2 → 1.9, sun 2.0 → 1.9; lobby warm point lights 40 / 12 / 18 / 12 → 44 / 12 / 22 / 14 |
| Edge lines | lobby outlines on wood wall, stair finishes, guards, chairs, directory at 0.35 | **outlines only on wood wall, stair finishes, guards at 0.20**; chairs, tables, plants, art and directory have none (base-building edges unchanged) |
| Glass (all interior neutral glass incl. guards) | 0.62 / 0.74 / 0.80, roughness 0.10, alpha 0.28 | **0.76 / 0.83 / 0.87, roughness 0.08, alpha 0.20** (clearer, not milky, no tint) |
| Chair cushions | 0.86 / 0.83 / 0.77, rough 0.95 | 0.84 / 0.81 / 0.75, rough 0.97 (soft off-white, no gloss) |
| Chair frames / treads | grain texture, base 0.34 / 0.21 / 0.12 | new grain texture, base 0.32 / 0.20 / 0.12 and 0.30 / 0.185 / 0.105 |
| Table bronze | 0.14 / 0.11 / 0.09, rough 0.40, metallic 0.70 | 0.13 / 0.105 / 0.09, rough 0.50, metallic 0.60 (softer highlights) |
| Graze pools | 0.55 → 1.5 ft wide, 2.6 ft tall, alpha ≤ 0.80, emissive 0.9 | **0.7 → 1.9 ft wide, 2.8 ft tall, wider Gaussian, alpha ≤ 0.62, emissive 0.75** (softer, less quad-like) |
| Pendant emitters | 1.0 / 0.86 / 0.68 at 1.8 | 1.0 / 0.84 / 0.64 at 1.5 (warm, no clipping under tone mapping) |
| Fixture / frame black | rough 0.55 | rough 0.60 |

## Validation (2026-09-23, browser)
No console errors · lobby group 13 mesh nodes, 4 edge-line sets (wood wall, stair finishes, guardrail) · Stair 1 walkthrough identical to v020 / v022 / v024 (same positions and heights; largest step 0.44 ft; guard stop at y 81.4) · furniture: chair, table, planter cells blocked with the concept on, chair cell open when off, the aisle between pairs open, walking into a chair stops at y 91.8 · Lobby toggle, Base / Concept, six lobby views incl. Free Walk, Lobby button, exterior, Level 2 plan, Level 1 orbit, measure (3-4-5 = 5'-0"), tenant viewpoint VP_A_08, presentation mode all as in v024 · draw calls 1,359 (v024: 1,367), same triangles; GPU-flushed frame times measured in the app's hidden browser pane are noisy for both versions (v024 39–167 ms, v025 31–127 ms in alternating runs) and show no v025 penalty · manifest: all 398 Building II files of v001–v024 SHA-256 identical (v023 model, viewer v024 GLB / data / code included); source documents unchanged.

## Known limitations
The cream cast of the walls under tone mapping comes from the warm hemisphere ground and point lights; a neutral hemisphere would cool it if wanted · pools remain flat quads slightly in front of the wall field · no shadows · frame timing cannot be measured reliably inside the hidden app pane; on a normal desktop browser v024 ran smoothly and v025 has the same geometry, textures (+1.5 MB) and fewer line objects.

## How to open
As v024, but the folder is **`viewer_v025`** and the address `http://127.0.0.1:8025/`.
