# Browser viewer control document v020 — Lobby Concept A review (model v019)

Date: 2026-09-22
**Viewer version v020** (`viewer_v020/`, port **8020**) shows **model version v019** (`models/building_shell_v019.blend`, the Pass 1 architectural lobby). v016–v018 were viewer-only versions of the v015 model; v019 is the first real model update since v015, so the version numbers are kept distinct: the page reads "Review Prototype v020 · Model v019 · Lobby Concept A (Pass 1)". Earlier viewers (`viewer/` 8016, `viewer_v017/` 8017, `viewer_v018/` 8018) and their GLB are untouched and still run.

**Nothing in the Blender master was changed.** `scripts/export_viewer_v020.py` opens `building_shell_v019.blend` read-only (its SHA-256 is asserted unchanged after the run), regroups / joins / re-materials objects in memory only, exports the GLB and writes the data file. No lobby design work was done: the viewer shows exactly the v019 Pass 1 objects (no chairs, tables, planters, artwork, signage or tenant names were added; the reserved Pass 2 sub-collections are exported as empty nodes).

## Files

| File | Content |
| --- | --- |
| `exports/building_II_model_v019_viewer_v020.glb` | new export, **8,932,392 bytes** (v016 GLB: 8,409,512). 761 nodes, 174 meshes, 111 materials, 1 image (generated walnut grain) |
| `viewer_v020/models/building_II_model_v019_viewer_v020.glb` | identical copy used at run time |
| `viewer_v020/assets/viewer_data_v020.json` | groups, floors, three walk grids, Stair 1 navigation surface, tenant concept (rooms, 10 viewpoints, underlay), lobby concept (4 viewpoints, orbit target, metadata) |
| `viewer_v020/index.html`, `src/main.js`, `src/style.css`, `serve.py`, `serve.js`, `start_viewer.bat`, `vendor/` | the viewer (from v018, extended) |
| `renders/viewer_v020_lobby_01_entrance.png` … `_04_feature_wall.png` | browser verification screenshots (headless Edge, 1920 × 1080) |

## What the GLB contains for the lobby (verified by parsing the GLB, then in the browser)

`GRP_Lobby_Concept_A` (extras: building = Building II, level = Lobby / Level 1 / Level 2, category = Interior Concept, concept = Lobby Concept A, model_version = v019, source_collection = Building_II > INT_LOBBY_CONCEPT_A) with one child node per v019 sub-collection:

| Node | v019 source objects | Exported | Triangles |
| --- | --- | --- | --- |
| LOBBY_A__ARCH_WOOD_WALL | 51 | 1 mesh | 612 |
| LOBBY_A__LIGHT_FEATURE_WALL | 192 (128 meshes + 64 point lights) | 1 mesh, 2 materials | 1,536 |
| LOBBY_A__ARCH_STAIR_FINISH | 59 | 1 mesh, 2 materials | 708 |
| LOBBY_A__ARCH_GUARDRAIL | 11 | 1 mesh | 132 |
| LOBBY_A__LIGHT_DECORATIVE | 127 | 1 mesh, 3 materials (7 pendants, coffer, track) | 1,524 |
| LOBBY_A__FINISH_FLOOR | 90 | 1 mesh, 3 materials | 1,080 |
| LOBBY_A__FINISH_WALL | 30 | 1 mesh, 3 materials | 360 |
| LOBBY_A__FF&E_SEATING | 4 | 1 mesh, 2 materials | 48 |
| LOBBY_A__SIGNAGE_DIRECTORY | 4 | 1 mesh, 3 materials | 48 |
| LOBBY_A__FF&E_TABLES, FF&E_PLANTERS, ART_DECOR | 0 | empty nodes (reserved, Pass 2 not authorized) | 0 |

Totals: 504 source meshes → 9 mesh nodes, 20 draw primitives, **6,048 triangles**, **15 lobby materials**. The 64 Blender point lights and the 3 lobby cameras are not exported (cameras become data viewpoints).

## Viewer-only optimizations and material treatment (export pipeline, master untouched)

- Repeated pieces (50 wood boxes, 64 wall fixtures + lenses, 88 tiles, 7 pendants, overlays) are **joined per sub-collection in memory** — one node per sub-collection instead of 504 objects; the group stays toggleable as a whole.
- No real-time lights for the 64 wall cylinders: the lens, the pendant emitters and the track slot use **emissive glTF materials** (warm 3500 K tint); **4 browser point lights** (pendant cluster, wood wall, entrance, east side) add warmth and are shown only while the concept is on.
- Procedural Cycles materials are flattened to plain colours. Viewer overrides (in `VIEWER_MATERIALS`): walnut laminate and treads get a **generated vertical wood-grain texture** with box-projected UVs (4 ft repeat, in memory) so they read as walnut rather than flat orange; dark metal / gunmetal 0.115 grey with metallic 0.5 (not pure black); PT-02 metallic; PT-01 light warm neutral; POR-01 light grey 0.64 with roughness 0.55 (not glossy white); walk-off dark grey; leather warm brown; screen off dark; guard glass keeps the v016 translucent treatment (alpha 0.28).
- Subtle edge lines on the built lobby elements (wood wall, stair finishes, rails, banquettes, directory) as a display aid; none on the floor, lights or paint overlays.

## Controls added (existing v018 UI and design language kept)

| Control | Behaviour |
| --- | --- |
| **View: Exterior · Lobby · Level 1 · Level 2** | replaces the Floor row. **Lobby** (brown) = one click: Lobby Concept A on, two-storey lobby layers (Level 1 + Level 2 interior, envelope glazing, no roof lid / upper parapets), Walk mode at the entrance looking at the stair and wood wall. Orbit in the Lobby state frames the wood wall + stair + pendant composition from the north-east above the void (orbit target 116, 86, 10 ft; canopies hidden so the void is visible) |
| **Interior concepts: Lobby Concept A** checkbox + **Compare: Base / Concept** | toggles only `GRP_Lobby_Concept_A` (and the browser lobby lights). Base = frozen base building with the v014 stair and shell still visible |
| **Lobby views** | `Lobby - Entrance`, `Lobby - Level 1`, `Lobby - Level 2 Overlook` (the three v019 Blender cameras, read from the model: position, forward vector, lens) and `Lobby - Feature Wall` (viewer-only, chosen in the browser: 137.5, 95.5 ft, eye 5'-6", looking WNW and up at the wood wall, Stair 1, wall lights and pendants; no Blender camera added). **Free Walk** = walk mode at the entrance with the normal walking lens |
| Address-bar parameters | `?lv=LV_01_entrance` … `LV_04_feature_wall`, `?floor=lobby`, `?lobby=0/1`, `?free=1`, plus all v018 parameters |

## Walkable Stair 1 (viewer-only navigation surface)

The viewer has no physics engine; walking is a 0.25 ft grid test with a 0.75 ft body radius (v016–v018). v020 adds a **height** to the surface: three invisible navigation surfaces derived from the frozen v014 tread and landing objects (read, not edited), stored in the data file as `stair_surfaces`:

| Surface | Footprint (ft) | Height rule |
| --- | --- | --- |
| COLLISION_STAIR1_RUN_01 | x 107.08–113.02, y 79.37–92.20 | ramp through the tread centres: z = 0.5714 × (0.5 + d / 0.9167), d = distance south from y 92.20; up to 8.571 |
| COLLISION_STAIR1_LANDING | x 107.08–113.52, y 73.44–79.37 | plane at 8.571 |
| COLLISION_STAIR1_RUN_02 | x 113.52–124.52, y 73.44–79.37 | ramp from 8.571: z = 8.571 + 0.5714 × (0.5 + d / 0.9167), d = distance east from x 113.52; up to 16.0 |

Rules: run 1 lives in the Level 1 grids and the Level 2 grid; landing and run 2 in the Level 2 grid, so the walker hands over from the Level 1 grid to the Level 2 grid at the run 1 / landing line and keeps walking onto the Level 2 slab at x 124.52 (and the reverse coming down). A move is accepted only if the surface under the body centre changes by ≤ 1.0 ft (`step_ft`; a riser is 0.571 ft) and every point of the 0.75 ft body ring is standable within 1.5 ft of that height — this is the fall protection at the open sides of the runs, the landing edge and the Level 2 void, in addition to the frozen glass guards (whose cells are re-applied inside the stair footprint) and the Level 2 balcony guards (blockers at 16.5–22.5 ft). Camera height eases toward the surface (no bounce); walking speed on the ramps is 0.6 × normal (5.4 ft/s). The route is the real L-shape (run 1 → landing → run 2); there is no shortcut. Eye height stays 5'-6"; gravity is implicit (the camera is always on the surface, it cannot fall through the landing or the Level 2 slab).

Grid facts (from the export): Level 1 base grid 315 blockers, 301,826 open cells; Level 1 with lobby concept (banquettes, directory, wood boxes block) 409 blockers, 301,357 open cells; Level 2 240 blockers, 172,952 open cells. The grid follows the Lobby Concept toggle.

## Validation (2026-09-22, Microsoft Edge / built-in browser)

1. v019 Blender master unchanged (SHA-256 asserted by the export; freeze manifest) · 2. previous viewers unchanged · 3. previous GLB unchanged · 4. source documents unchanged (Building II 360 files identical by path / size / time; Building I aggregate 1,231 files / 6,929,037,544 bytes / newest time identical, folder not opened; PowerPoint hash unchanged) · 5. new outputs in `viewer_v020/`, `exports/…v020.glb`, `renders/viewer_v020_*` only · 6. `GRP_Lobby_Concept_A` present in the GLB with the 9 mesh nodes above · 7–13. wood wall, stair finishes (walnut treads, dark stringers / soffit), glass guards with dark shoes and rails, seven pendants, porcelain floor with grout, banquettes, directory massing all visible in the browser screenshots · 14. toggle: off hides only the lobby group and lights, base stair / shell stay; walk grid switches (directory cell open when off, blocked when on) · 15–18. the four saved views place the camera in the lobby (positions 128/101.8, 141.2/88.5, 134.2/69.5 at Level 2, 137.5/95.5) · 19. orbit in the Lobby state frames the void · 20–22. walk at 5'-6"; scripted walkthrough: entrance → foot of run 1 → up run 1 → landing (grid hand-over) → up run 2 → Level 2 floor (z 16) → north stops at the balcony guard (y 81.4 against the guard at 82.47) → east stops at the core wall → back to the stair-top row → down run 2 → landing (to the west wall) → down run 1 → Level 1 (z 0) → lobby. Largest height change per 0.05 s step 0.44 ft, never below 0 ft, no stuck state, no teleport · 23. Exterior view, site and landscaping still draw · 24. v018 functions re-tested: Level 1 / Level 2 orbit and plan, tenant viewpoint VP_A_08 (walk at 45.45, 19.8), measure 3-4-5 = 5'-0", presentation mode (technical controls hidden, lobby views kept), concept selector, room labels.

Performance: about 6.3 ms per frame at the entrance view on this computer (924 k triangles drawn in walk mode with all layers), 1,342 draw calls; page ready in 3–5 s.

## Known limitations

- No section / cutaway: the v018 viewer has no clipping-plane system, so none was built (skipped as instructed). The Lobby orbit state instead hides the roof lid, upper parapets and canopies and looks into the open two-storey void; the CW1 glazing is translucent.
- The stair surface is a smooth ramp through the tread centres, not individual steps: the camera glides up the visible treads (feet up to 0.29 ft above / below a nosing).
- Under Stair 1 the Level 1 floor is walkable only where the frozen treads / landing are above 6.5 ft; the west banquette under run 1 blocks its own footprint when the concept is on.
- Stair 2 (west core) is still not walkable; use the View buttons.
- Flat colours with emissive fixtures, no shadows or bloom: a review tool, not a rendering. The 64 wall cylinders read as small warm rectangles.
- Reserved Pass 2 nodes are empty; nothing was invented.

## How to open v020

1. Open File Explorer and go to the project folder `Rea Farms II 3D`.
2. Open the folder **`viewer_v020`**.
3. Double-click **`start_viewer.bat`** (if Windows shows "Windows protected your PC", click **More info**, then **Run anyway**).
4. A small black window appears and your browser opens `http://127.0.0.1:8020/` a few seconds later. Leave the black window open.
5. When "Loading Building II model…" disappears, click the brown **Lobby** button. You are inside the entrance looking at the stair. Walk with **W A S D** (or the arrow keys), drag the mouse to look around, walk onto the stair to reach Level 2.
6. Use **Base / Concept** to compare, the **Lobby views** buttons to jump, and **Orbit** to rotate around the lobby composition.
7. When finished, close the browser tab, then the black window.
