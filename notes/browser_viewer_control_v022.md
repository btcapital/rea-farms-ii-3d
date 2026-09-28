# Browser viewer control document v022 — Lobby Concept A Pass 1 + Pass 2 (model v021)

Date: 2026-09-22 · **Viewer version v022** (`viewer_v022/`, port **8022**) shows **model version v021** (`models/building_shell_v021.blend` = approved v019 lobby + Pass 2). v022 is the approved v020 viewer **unchanged** (same page, controls, walk grids, Stair 1 navigation surface, viewpoints); only the version labels and the data / GLB file names differ. v020 (8020) and all earlier viewers are untouched.

## Files
| File | Content |
| --- | --- |
| `exports/building_II_model_v021_viewer_v022.glb` | **10,022,696 bytes** (v020: 8,932,392). 761 nodes, 177 meshes, 124 materials, 4 images (walnut grain, art A1, art A2, directory graphic) |
| `viewer_v022/models/…v022.glb` | identical copy |
| `viewer_v022/assets/viewer_data_v022.json` | as v020 + `navigation_note`; `lobby_concept` metadata says model v021, Pass 1 + Pass 2 |
| `scripts/export_viewer_v022.py` | v020 export script with: v021 source, Pass 2 material overrides, image textures kept for the art / directory materials, Pass 2 objects excluded from collision, and an **assertion that all three walk grids and the Stair 1 surfaces are identical to viewer v020's** |
| `renders/viewer_v022_lobby_01…05.png` | headless-browser verification screenshots (05 = directory graphic and DP-01 wall) |

## Lobby group in the GLB (verified by parsing, then in the browser)
12 mesh nodes (the three formerly empty Pass 2 nodes now carry geometry), 33 primitives, **10,748 triangles** (v020: 6,048), 28 lobby materials. Pass 2 nodes: FF&E_SEATING (banquettes + 4 chairs, 864 tri), FF&E_TABLES (456), FF&E_PLANTERS (3,128: sphere foliage), ART_DECOR (48), SIGNAGE_DIRECTORY (+ graphic plane), FINISH_WALL (+ 19 DP-01 panels + trim).

## Viewer-only material treatment added for Pass 2
Chair frame with the walnut grain texture; cushions warm off-white; tables dark bronze metallic; SP-01 grey; foliage matte green; art frames near-black; **art canvases and the directory graphic keep their generated images from the v021 master** (directory emissive so it reads as switched on); DP-01 pale-blue glossy; TR-05 brushed stainless.

## Navigation
Unchanged from v020 by construction: Pass 2 objects (`LOB_A_P2_*`) are not collision blockers, and the export asserts the grid rows and stair surfaces equal v020's. Consequence: the loose chairs, tables and planters can be walked through (they are review props); adding them as blockers is a collision change that needs approval.

## Validation (2026-09-22)
Page loads, no console errors · lobby group present with 12 mesh nodes, 6 textured meshes · the four saved lobby views place the camera as in v020 · scripted Stair 1 walkthrough (entrance → run 1 → landing → run 2 → Level 2 → guard stop → back down to Level 1) gives the same positions and heights as the v020 test (largest step 0.44 ft, never below floor) · chair cell (119.9, 89.7) open in the lobby grid · frozen files: all 333 Building II files of v001–v020 (models, scripts, notes, renders, exports, viewers, tenant PDF, concept PowerPoint) SHA-256 identical.

## How to open v022
As v020, but the folder is **`viewer_v022`** and the address is `http://127.0.0.1:8022/`. Click the brown **Lobby** button, walk with W A S D, drag to look; Stair 1 leads to Level 2.
