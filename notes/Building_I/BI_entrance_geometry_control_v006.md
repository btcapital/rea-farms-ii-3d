# Building I — entrance geometry correction control document v006

Date: 2026-09-22
Applies to: `scripts\Building_I\BI_build_entrance_fix_v006.py` → `models\Building_I\BI_landscape_v006.blend`, renders `renders\Building_I\BI_entrance_v006_*.png`.
Base: **BI_landscape_v005.blend (owner-approved facade-cleanup baseline, frozen in `manifests\BI_freeze_BuildingI_v005_approved.json`, 85 files)**.
Scope: two targeted geometry corrections at the main entrance only — (A) the upper-level curtain-wall placeholders floating in front of the wall, (B) the false horizontal overhang above the entrance. Nothing else changes.

## 1. Issue A — curtain-wall placeholders above the vestibule

### 1.1 Current condition (measured in v005)
12 opening placeholders `BI_open_NORTH_*` with x 40.67–63.67 and z 11.69–14.02 (5) / 17.13–24.58 (7) sit on the plane **y = 83.58** (the vestibule north face, grid G.2) although the vestibule (`BI_Z3_vestibule_100`) is only 9.0 ft tall. The neighbouring placeholders at x 64.0–70.28 sit on **y = 74.38** (the E–F.2 band north face, grid F.2 = 74.54). Cause (v001 build rule, `BI_build_shell_v001.py::face_coordinate`): every north-facing opening was placed on the *outermost* footprint boundary at its x, ignoring z, so all openings within the vestibule's x-range went to the vestibule plane, including the ones above its roof. They are not duplicated (no second copy exists on y = 74.38); they are misplaced by **9.20 ft** north.

### 1.2 Sources reviewed
| Sheet | Page | Printed status | What it shows |
| --- | --- | --- | --- |
| **A5.18 A2 "Wall Section @ Primary Entry Vestibule"** (1/2" = 1'-0") | 78 | rev 13 7/25/2025 | The two-storey curtain wall stands on grid **F.2** from LVL-01 to the roof (T.O.S. 30'-0") with the parapet (6'-11 99/256" above the deck) directly above it; the Level 2 slab sits behind it; the vestibule is a low glazed box from F.2 to **G.2** with its roof just below the 11'-0" gallery line; beyond it only the canopy (G–G.2 column). **No wall or glazing at G.2 above the vestibule roof.** |
| A5.19 A2 "Section @ Entry Vestibule", A1 "Wall Section @ Entry Vestibule Side", B1/B2 roof details | 79 | rev 6 11/15/2024 | Vestibule sliders 100b/100c between grids 3.7 and 5 with its own TPO roof and coping; the curtain wall behind rises past LVL-02 |
| A7.26 B1 "Curtain Wall North Elevation @ Entry Vestibule", B2 West, A1 "CW Inside Vestibule", A2 "CW Side Vestibule" | 106 | rev 6 11/15/2024 | CW1 north elevation **41'-7" wide × 24'-6" high** (7'-10 3/4" + 9'-10" + 6'-9 1/4"), vestibule front 8'-9" high with 3'-7 3/4" side lites and the 100b sliders in front of it; vestibule side and inside curtain-wall elevations 9'-0" wide |
| A7.34 details | 112 | 3/28/2025 | "Curtain Wall Head @ Entry Vestibule Front/Side", "Curtain Wall Sill @ Entry Vestibule Roof" — the main curtain wall continues down to the vestibule roof where the vestibule meets it |
| A1.13 A1 "Enlarged Plan at Entry Canopy" | 29 | rev 13 7/25/2025 | vestibule 1'-9" + 10'-3" + 10'-3" + 1'-9" between F.2 and G.2 (as in v001) |
| A1.02 Level 2 plan (registered vector, 6.750 pt/ft, residual ≤ 0.07 ft in x) | 27 | rev 13 7/25/2025 | Level 2 exterior wall lines at **y 72.5–74.25, x 28.8–70.9** (F.2 wall); no wall line at y ≈ 83.6 on Level 2 |
| A1.00c Roof Edge of Slab Plan (registered vector) | 25 | rev 7 1/20/2025 | roof edge along **y 74.5–75.25 from x 28.5 to 90.8**; no roof between F.2 and H.1 at grids 3–6 |
| Photographs 2026-07-28 (0045), 2025-09-09 progress | — | — | glazed two-storey lobby wall behind a low vestibule and the flat canopy; validation only |

### 1.3 Determination
- Correct wall / glazing plane: the E–F.2 band north face, **y = 74.38 in the approved v001 geometry** (grid F.2 = 74.54; the curtain-wall outer face in A5.18 sits within 0.4 ft north of the grid line, inside v001's tolerance). Written source A5.18 A2; supported by A1.02 and A1.00c vector lines and A7.26/A7.34.
- Horizontal position and vertical extent of the placeholders: unchanged (x 40.67–63.67, z 11.69–24.58 as detected in v001; A7.26 gives the CW1 total height 24'-6" = 24.5 ft, consistent with the top at 24.58).
- Relationship to the vestibule: the vestibule (F.2 → G.2, 9.0 ft in v001; A7.26 head 8'-9", roof per A5.19) stands in front of the curtain wall; only the sliders and side lites (z ≤ 8.52) belong on y = 83.58.
- Relationship to the canopy: the canopy (gutter on G.2 at 13'-0 1/4", A1.13) is independent; unchanged.
- Correction: translate the 12 placeholders by **Δy = −9.20 ft** (83.58 → 74.38). No other opening moves.

## 2. Issue B — false upper overhang

### 2.1 Current condition
Ray-casting the entrance camera shows the white plate above the entrance is the **top face of `BI_Z4b_north_block_south_part`** hit at (52.6, 79.6, 33.1) — a location outside that object's footprint (its west part is only the strip y 70.58–74.5). The mesh's cap faces were built as one polygon over the whole concave outline and Blender's tessellation bridged the re-entrant notch: **4 triangles (573 sq ft) lie inside x 30–71, y 74.6–97.7 at z ≈ 33.2**, forming a plate from the band face to y = 97.75 over the entrance. Vertices are correct (all 28 within the intended outline); only the cap faces are wrong. Not a parapet, slab edge, canopy duplicate or raster shape: a **cap-face tessellation artifact of the v001 prism build**.

### 2.2 Documents confirming no overhang
A1.00c roof edge plan (roof edge at F.2, nothing between F.2 and H.1 at grids 3–6); A5.18 A2 (roof and parapet end at the F.2 curtain wall; only the canopy projects); A4.02 north elevation (sloped PNL1 wall above CW1, no soffit line); A1.13 (canopy is the only projecting element, gutter at 13'-0 1/4"). Photographs 2026-07-28 / 2025-09-09 show no upper overhang.

### 2.3 Root cause found during the correction: a self-overlapping v001 outline
Ordering the prism's top vertices through its side faces shows the v001 Level-2 trace produced a **self-overlapping outline west of x = 71**: (271.38, 97.75) → (271.38, 70.58) → (28.71, 70.58) → (28.75, 74.38) → (39.62, 74.38) → (39.62, 73.88) → (29.25, 73.75) → (29.28, 70.58) → (71, 70.58) → (71, 73.75) → (60.25, 73.88) → (60.25, 74.38) → (71, 74.5) → (71, 97.75). West of x = 71 this is a 0.5-ft-wide "U" sliver hugging the E–F.2 band, lying inside `BI_Z2_band_E_F2`, except that its north face at **y = 74.5 (x 60.25–71) stands 0.12 ft proud of the band wall and covers the curtain wall there** (the black strip beside the glazing in every entrance render, confirmed by ray-cast: first hit `BI_Z4b_north_block_south_part` at y 74.49 in front of the placeholders at 74.43). No such wall exists on A1.02 (Level 2 wall lines at y 72.5–74.25 only) or A5.18 (single curtain-wall plane at F.2). A polygon of this shape cannot be ear-clipped, which is why v001's cap tessellation bridged the notch.

### 2.4 Correction
`BI_Z4b_north_block_south_part`: delete the sliver side faces (every face whose vertices all lie at x ≤ 71.01, y ≤ 74.51, except the long south face), close the prism's west side on its existing vertices (71, 70.58)–(71, 74.5), rebuild the top and bottom caps as the simple rectangle (71, 70.58)–(271.38, 70.58)–(271.38, 97.75)–(71, 97.75) on existing vertices, and drop the vertices left unused (the sliver vertices, all inside the band prism). **No vertex is moved and no vertex is added**; the visible result is the removal of the false overhang and of the 0.12-ft strip over the curtain wall. The band prism `BI_Z2_band_E_F2` (which carries the real F.2 wall) is untouched.

## 3. Consequential facade regions
The v005 finish regions are regenerated with the identical `BI_facade_regions_v005.json` and algorithm; because the moved placeholders now lie on plane y = 74.38, the N2 curtain-wall backdrop and N3 PNL1 regions on that plane lose the polygons under the moved glazing. All other region polygons are byte-identical (checked by the comparison script).

## 4. Unchanged / not resolved
Lower entrance canopy, entrance doors and side lites (z ≤ 8.52 on y = 83.58), glazing sizes, all other openings, shell, parapets, site, landscape, materials, existing cameras. Vestibule height stays 9.0 ft (v001 A-1; A7.26 head 8'-9" + roof build-up per A5.19 not summed here). Curtain-wall outer face vs grid F.2 offset (≤ 0.4 ft) not modeled. Carried forward: G-1…G-6, F-1…F-8, SC-, LC-items. Item G-7 (this issue) is resolved by v006 for the plane; the placeholder extents remain R (raster-detected).

## 5. Validation planned
Hash of every mesh object except the 12 placeholders, Z4b and the FR regions, before/after; `BI_compare_geometry_v005_v006.py` reporting every changed object with previous and new plane/location; Z4b vertex set identical and no cap triangle inside the notch; freeze manifests v005 (85), project/Building II (311), Building I sources (1,231). Renders: entrance close-up (same camera as the v005 validation view), straight-on entrance elevation (orthographic), entrance oblique, side/depth view along the north face; before/after composites for each.
