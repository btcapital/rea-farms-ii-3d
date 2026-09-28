# Building I — footprint correction v008: comparison and validation report

Date: 2026-09-23
Model: `models\Building_I\BI_footprint_v008.blend` (798 objects = 779 in v007 − 19 replaced/removed + 38 built, incl. 5 validation cameras), built by `scripts\Building_I\BI_build_footprint_fix_v008.py` from `BI_footprint_data_v008.json` and `BI_facade_regions_v008.json`. Audit: `BI_footprint_audit_v008.md`. Build report: `BI_footprint_v008_build_report.json`. Comparison: `BI_compare_geometry_v007_v008.py`.
Status: **built and validated, NOT approved.** v001–v006 remain the frozen approved baseline; v007 is frozen pre-v008 (`manifests\BI_freeze_BuildingI_v007_pre_v008.json`, 114 files, PASS).

## 1. What changed (object-by-object comparison v007 → v008)

| Class | Changed | Added | Removed | Detail |
| --- | --- | --- | --- | --- |
| Shell prisms | 4 (`BI_Z2_band_E_F2` 28.5–71 × 54.2–74.38; `BI_Z5_end_block_13_14` 271.29–281.62 × 44.21–97.75; `BI_Z4b_north_block_south_part` rebuilt as a clean prism, same bounding box 71–271.38 × 70.58–97.75; `BI_L2_floor_slab` on the Level 2 outline) | 6 (`BI_Z1_south_wing_L1` 0–13.5, `BI_Z1_south_wing_L2` 13.5–33.3, `BI_Z1_L2_storefront_projection_bay` 172.01–228.01 × −4.15…−1.46 × 12.58–27.33, `BI_Z4a_north_block_L1` 0–9.0, `_mid` 9.0–14.83, `_L2` 14.83–top) | 2 (`BI_Z1_south_wing`, `BI_Z4a_north_block`) | every new cap triangulation verified: cap area = polygon area for all nine prisms (v001 had +8 % overlapping cap triangles on the south wing) |
| Openings (376) | 290 re-placed | 0 | 0 | SOUTH 149 moved: +2.89 ft (91, brick face), +7.23/+7.26 (31, recesses), +0.2 (21, storefront box), −16.31 (6, rear-vestibule south face); EAST 71: +0.65 (18, brick face 281.62), −2.36 (14, gallery 284.62), +10.27 (11, rear vestibule), −5.36 (2, Level 1 under the gallery), +6.42 (2, stair landing), ≤0.1 (24); NORTH 26: −6.89 (9, wing north wall), −1.96 / −0.57 / +0.17 (17, clerestory on the Level 2 north face); WEST 44: +3.76 (17, x 10.67), 8 rotated onto the canted storefront, others on the recessed door / TWS projection / lobby west face; 86 unchanged |
| Parapet screens | 5 | 10 | 4 | 15 strips on the Level 2 south faces, recess returns, east face y 8.6–44.21 and west face y 2–54.2 (same R profiles) |
| Finish regions | 52 | 2 (`FR_EAST_UNRES_E0`, `FR_WEST_UNRES_W0`: 1.9 sq ft of 0.03-ft slivers) | 1 | 58 regions regenerated on the new faces: BRK1 8,820 sq ft, PNL1 13,769, PNL2 5,198 (+S7/N6 extents), TWS1 4,963, GLZ 787, PNL3 338, UNRES ≈ 60 sq ft (slivers at region joints) |
| Foundation skirts | 2 | 4 | 1 | one skirt per Level 1 zone polygon (depth 4.0, A) |
| Landscape | 19 (14 plant groups + their mulch discs + the unresolved-symbol object) | 0 | 0 | **84 plants returned to their documented LP-100/LP-101 positions; 0 plants and 0 of the 117 unresolved symbols need pushing** against the corrected footprint; 225 other landscape objects byte-identical; quantities unchanged (608 placed + 117 unresolved) |
| Cameras | — | 5 | — | `BI_cam_plan_top`, `_plan_G8_south`, `_plan_G9_wing_north`, `_plan_G10_northeast` (orthographic top), `BI_cam_oblique_southeast` |
| Everything else | 0 | 0 | 0 | canopy (10), vestibule, mechanical screen, grid, all `SITE_` surfaces/walls/streets/context, 225 landscape objects, materials: identical (hash of 285 kept mesh objects `f0a4c049…d9ee` before/after; comparison script confirms) |

## 2. Footprint change (Level 1, outside face of wall)

| Method | v007 (v001 footprint) | v008 | Change |
| --- | --- | --- | --- |
| Zone polygons (exact) | 47,092 sq ft (footprint_union 46,345 + lobby band 530 + vestibule 217) | **45,091 sq ft** | **−2,001 sq ft (−4.2 %)** |
| Raster of the shell solids at z = 1 ft, 0.5-ft cells (`BI_compare_geometry_v007_v008.py`) | 47,910 (≈ 820 sq ft inflated by the v001 overlapping cap triangles, which the ray-parity test reads as solid) | 45,091 | −2,820 (3,004 removed, 184 added) |

By item (plan areas, Level 1): G-8 south face −905 (brick face +2.92 ft over 167 ft, recesses +7.3 ft over 56 ft); G-9 wing north wall −150; G-10 north-east notch −367; G-11 west face −176; G-12 east face at grade −375; G-14 north face −278; G-13 rear vestibule +167; east brick face 281.0 → 281.62 +78. Level 2 differs from Level 1 by the storefront box (−41.6 ft × 2.7 ft, one storey), the Level 2 bay (+151 sq ft, z 12.6–27.3), the gallery cantilever (+≈230 sq ft above 9.0 ft) and the north overhang (+≈200 sq ft above 14.83 ft). Overall extent x 7.00…287.39 (280.39 ft), y −4.16…203.03 (207.19 ft), top 40.1 (mechanical screen, unchanged).

## 3. Validation

| Check | Result |
| --- | --- |
| Unrelated geometry (285 kept mesh objects) hash before/after | identical |
| Independent comparison script | changed 4 shell + 290 openings + 5 screens + 52 regions + 19 landscape + 2 skirts; added 6 shell, 10 screens, 2 regions, 4 skirts, 5 cameras; removed 2 shell, 4 screens, 1 region, 1 skirt; canopy / vestibule / mechanical screen / grid / site identical; landscape quantities unchanged |
| Cap tessellation of every rebuilt prism | bottom cap area = polygon area (±0.1 sq ft) for all nine; centroid-in-polygon test passed for every cap triangle |
| Openings | 376 placed, 0 skipped, 8 rotated onto the canted storefront; v006 entrance correction preserved (12 curtain-wall lites still on the y 74.38 plane, vestibule doors on 83.58) |
| Landscape | 84 previously pushed plants now at documented positions, 0 pushed, 0 unresolved symbols pushed |
| `BI_freeze_BuildingI_v007_pre_v008.json` (114 files, all v001–v007) | PASS |
| `BI_freeze_BuildingI_v006_approved.json` (101) | PASS |
| `BI_freeze_project_and_BuildingII_v001.json` (311) | PASS |
| `BI_freeze_sources_BuildingI_longpath_v001.json` (1,231 source files) | PASS |
| Renders inspected | plan top, G-8 / G-9 / G-10 plan comparisons, oblique south-east, oblique north-west, elevated site view, rear south, right east; before/after composites and the three-colour overlay: corrected outline coincides with the documented outside-face lines; the v007 'before' north-east view also shows the v001 cap-tessellation artefact at the corner |

## 4. Renders

`renders\Building_I\BI_footprint_v008_{plan_top, plan_G8_south, plan_G9_wing_north, plan_G10_northeast, oblique_southeast, oblique_northwest, site_elevated, rear_south, right_east}.png`; before/after pairs `BI_footprint_v008_before_after_{plan_G8_south, plan_G9_wing_north, plan_G10_northeast, plan_top, oblique_southeast, oblique_northwest, site_elevated, rear_south, right_east}.png` (left/top: frozen v007 from the same cameras with the documented Level 1 outline in blue; right/bottom: v008); `BI_footprint_v008_overlay_top.png` (red = v007 footprint, blue = controlling Level 1 outside face, green dashed = Level 2 outline, on the v008 top render).

## 5. Still uncertain / assumed in v008

- Gallery cantilever soffit 9.0 ft (M, A5.15 A2 at 1/2" = 1'-0", ±0.3); stair-landing soffit assumed equal (I); north-face Level 2 overhang soffit = slab underside 14.83 (A); Level 1 entry recess (x 10.67–12.30, y 18.42–28.74) soffit at the 13.5 split instead of the slab underside (A, 1.3 ft, hidden).
- Rear vestibule / end block parapet 32.0 (R, v001 raster); all other roof heights unchanged from v001 (R).
- G-15: north-block west face and north face x 91–148 stay at the v001 slab-edge positions (0.5–0.7 ft inside the brick face) to preserve the v006 entrance geometry.
- The canted storefront face (diagonal) has no finish region (clay); the tops of the one-storey projections and the bay show the wall material (no roof tag); the thin roof-edge line at x 287.39 (y 106–166) on A1.02 may be a roof overhang beyond the Level 2 curtain wall — not modeled.
- All earlier open items carry forward unchanged: G-1…G-6, F-1…F-8, SC-1/SC-3, LC-2, 117 species-unresolved symbols, 11 interpreted ground-cover discs, N Old Springs Rd trees not photo-verified, vestibule height (A-1). G-8, G-9, G-10 close with v008; G-11…G-14 are corrected by v008 and G-15 is a documented tolerance.

## 6. Files created in this pass

```
models/Building_I/BI_footprint_v008.blend
notes/Building_I/BI_footprint_audit_v008.md
notes/Building_I/BI_footprint_data_v008.json
notes/Building_I/BI_facade_regions_v008.json
notes/Building_I/BI_footprint_v008_build_report.json
notes/Building_I/BI_footprint_validation_v008.md
notes/Building_I/manifests/BI_freeze_BuildingI_v007_pre_v008.json
renders/Building_I/BI_footprint_v008_*.png (9 views, 9 before/after pairs, 1 overlay)
scripts/Building_I/BI_build_footprint_fix_v008.py
scripts/Building_I/BI_render_footprint_views_v008.py
scripts/Building_I/BI_compare_geometry_v007_v008.py
```

Next decision for the owner: **approve or redirect the v008 footprint correction** (then freeze v001–v008). Not started: presentation realism, interiors, viewer work, further landscape refinement.
