# Browser viewer control document v024 — approved lobby baseline (model v023)

Date: 2026-09-23 · **Viewer version v024** (`viewer_v024/`, port **8024**) shows **model version v023** (`models/building_shell_v023.blend`, the approved lobby baseline). v024 = the v022 viewer code (v020 navigation framework) with a new export. v020 and v022 and all earlier viewers are untouched. The v023 Blender master was only read (its SHA-256 is asserted unchanged by the export).

## Files
| File | Content |
| --- | --- |
| `exports/building_II_model_v023_viewer_v024.glb` (+ identical copy in `viewer_v024/models/`) | **12,585,740 bytes**. 762 nodes, 178 meshes, 126 materials, 5 images (walnut grain, art A1, art A2, directory graphic, graze pool) |
| `viewer_v024/assets/viewer_data_v024.json` | groups, floors, walk grids (with furniture footprints), Stair 1 surfaces, tenant concept, lobby concept with **five** viewpoints, `furniture_collision` record |
| `scripts/export_viewer_v024.py` | v022 export script + v023 source, furniture footprints, baked graze pools, refreshed material overrides, seating viewpoint, navigation assertions |
| `renders/viewer_v024_lobby_01…05.png` | headless-browser verification captures |

## Lobby group in the GLB (parsed, then checked in the browser)
13 mesh nodes, 35 primitives, **12,028 triangles**, 30 lobby materials. Nodes: ARCH_WOOD_WALL 612 tri · LIGHT_FEATURE_WALL 1,536 (64 bodies + 64 exit slots) · **LIGHT_FEATURE_WALL_graze 128 (viewer-only pools)** · ARCH_STAIR_FINISH 708 · ARCH_GUARDRAIL 132 · LIGHT_DECORATIVE 1,524 (coffer, track, 7 pendants, cables) · FINISH_FLOOR 1,080 · FINISH_WALL 600 (paint, fascia, DP-01) · FF&E_SEATING 720 (banquettes + 4 refined chairs) · FF&E_TABLES 1,896 (bevelled tops) · FF&E_PLANTERS 2,984 (pots + branching plants with leaf polygons) · ART_DECOR 48 · SIGNAGE_DIRECTORY 60 (75" massing + neutral graphic). All v023 content is the actual exported geometry; nothing was substituted.

## Wall-light treatment (viewer only)
The 64 Cycles spot lights are not exported. Each fixture keeps its dark body (0.06 charcoal, metallic 0.3) and its ⅜-inch warm emissive exit slot (1.0 / 0.78 / 0.50, strength 1.6). Below each fixture the export adds one trapezoid quad (0.55 ft wide at the top, 1.5 ft at the bottom, 2.6 ft tall, 0.012 ft in front of the box faces) carrying a generated RGBA pool image (warm colour, alpha fading downward and sideways), alpha-blended and slightly emissive: **64 quads, 128 triangles, one material**. Result in the browser: dark fixtures, warm downward pools, walnut dominant. The viewer's warm point light at the wood wall was reduced from 22 to 12 (the pools now carry the warmth); the entrance daylight fill was raised from 14 to 18.

## Material overrides changed for v023 look
Walnut 0.35 / 0.21 / 0.115 with the grain texture · stair / shoe / rail dark metal 0.135 / 0.138 / 0.148, roughness 0.5, metallic 0.4 (charcoal, readable highlights) · fixture and pendant frame black 0.06 · pendant emitter warm 1.0 / 0.86 / 0.68 at 1.8 · cables `LOB_A_V23_cable_dark` 0.05 · cushion fabric 0.86 / 0.83 / 0.77 roughness 0.95 · foliage 0.15 / 0.29 / 0.13 · art and directory keep their generated images from the v023 master · glass unchanged (translucent, not smoked).

## Furniture collision (new in v024)
Simplified invisible footprints, one rectangle per piece from the bounding box of its parts: four chairs about 2.32 × 2.14 ft, two tables 1.35 × 1.35 ft, two planter pots 1.41 × 1.46 ft (exact values in the data file). Plants, art, DP-01 and the directory graphic do not block; banquettes and the directory massing block as before. Applied only to the `level1_lobby_A` grid (concept shown). The export asserts: Stair 1 surfaces identical to v020, `level1` and `level2` grids identical to v020, and every one of the 569 cells that differ in `level1_lobby_A` lies inside a furniture footprint. Circulation stays as validated in v023 (the 4.2 ft aisle between the chair pairs, the entry axis and the door approaches are open).

## Saved lobby viewpoints
Lobby - Entrance · Lobby - Level 1 · Lobby - Level 2 Overlook · Lobby - Feature Wall · **Lobby - Seating** (browser viewpoint read from the v023 review camera `Cam_lobby_A_04_seating`, position 131.8 / 97.2, 28 mm; the Blender camera was not modified) · Free Walk. The one-click **Lobby** button, Base / Concept, orbit lobby state, floor buttons, plan, measure, presentation mode and tenant viewpoints are the v022 behaviours unchanged.

## Validation (2026-09-23, browser)
Loads with no console errors · lobby group with 13 mesh nodes, 7 textured meshes · scripted Stair 1 walkthrough gives the same positions and heights as v020 / v022 (entrance → run 1 → landing → run 2 → Level 2 → guard stop at y 81.4 → back down → Level 1; largest step 0.44 ft, never below floor) · furniture: chair, table, planter, banquette and directory cells blocked with the concept on, chair cell open with it off; walking south into a chair stops 1 ft short of its edge; the aisle between the pairs is walkable · all five viewpoints and Free Walk place the camera correctly · Lobby button sets concept on, both levels, walk at the entrance · orbit lobby framing, Exterior view, Level 1 / Level 2 orbit and plan, measure (3-4-5 = 5'-0"), tenant viewpoint, presentation mode all as in v022 · frozen files: all 375 Building II files of v001–v023 SHA-256 identical; source documents unchanged.

## Known limitations
Graze pools are flat quads 0.2 ft in front of the wall field, so a near-grazing view can show slight parallax against the boxes · foliage is single-sided leaf polygons rendered double-sided (no translucency) · no shadows; the stair underside is lit by the ambient / fill lights rather than true bounce · the two Blender fill lights are not reproduced literally (hemisphere + four point lights instead) · the temporary v023 seating camera is used only as a data viewpoint.

## How to open v024
1. Open File Explorer, go to `Rea Farms II 3D`, open the folder **`viewer_v024`**.
2. Double-click **`start_viewer.bat`** (click "More info" then "Run anyway" if Windows warns).
3. Your browser opens `http://127.0.0.1:8024/`; keep the black window open.
4. Click the brown **Lobby** button, walk with W A S D, drag to look; Stair 1 leads to Level 2. Use the Lobby views buttons to jump, Base / Concept to compare.
5. Close the browser tab, then the black window, when done.
