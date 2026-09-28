# Building I — entrance-facade correction v011: validation and completion report

Date: 2026-09-23
Model: `models\Building_I\BI_entrance_facade_v011.blend` (813 objects = 810 of v010 + 3 validation cameras), built by `scripts\Building_I\BI_build_entrance_facade_fix_v011.py` on top of `BI_entrance_site_v010.blend`. Audit: `BI_entrance_facade_audit_v011.md`. Build report: `BI_entrance_facade_v011_build_report.json`. Comparison: `BI_compare_geometry_v010_v011.py` → `BI_compare_v010_v011.json`. Composites: `BI_entrance_facade_composites_v011.py`.
Status: **built and validated, NOT approved.** v001–v010 frozen (`manifests\BI_freeze_BuildingI_v010_pending_approval.json`, 182 files, PASS after this pass). The v010 entrance site correction is carried unchanged and is itself still awaiting approval.

## 1. Exact cause

The black rectangle above the porte cochere is on the **west face of the lobby tower** (plane x 28.5, y 54.2–74.38, z 24.6–40). `FR_WEST_PNL1_W2b` (the PNL1 finish region of that face) contained **two coplanar overlapping faces**: face 0 (y 54.2–70.58 × z 24.6–33.3, 142.5 sq ft) lying entirely inside face 1 (y 54.2–74.38 × z 24.6–40, 310.8 sq ft), 0.03 ft in front of the wall. Cycles offsets a shading point only against the triangle it hit, so every shadow and bounce ray from one face was blocked by the other coincident face and the pixels went black — independent of material (proved with a white material override) and of the wall behind (proved by hiding the wall). Neither a recess, an opening, a missing wall, a reversed normal nor a material assignment was involved: **geometry (mesh) of the finish region was wrong; the wall and the material assignment were right.** Full diagnosis chain in the audit §1.

Origin: the **v008** finish-region regeneration emitted one panel per exterior zone face; on this plane the lobby-band face and the south-wing Level 2 face coincide (both at x 28.5 for y 54.2–70.58), so the region was emitted twice, and the north block's x 71 face for y 70.58–74.38 (inside the band) was emitted as well. v005/v006 had a single face (no coincidence: the wing north wall then sat at y 61.12). The patch is visible in the v008, v009 and v010 renders. v009 (materials) and v010 (site) did not introduce it.

## 2. Source sheets used (Rev 14 record set; photos validation only)

A1.01 Level 1 plan, A1.02 Level 2 plan, A1.00c / A1.03 roof plans (lobby west wall straight at x 28.50 from y 54.22 to 74.13–74.54 on both levels), A4.02 West Elevation (CW1 below, PNL1 above continuously to the tower top; no opening, no material change), A7.26 Curtain Wall Elevations (CW1 head 24.6), A5.18 A2 Wall Section @ entry and A5.24 A3 parapet detail (one wall plane past the roof deck to the coping), closeout material record (Alucobond PLUS Bone White = PNL1), drone photographs 2026-07-28 / 2026-08-10 (continuous white ACM face — validation only).

| Item | Documented | Model |
| --- | --- | --- |
| Recess depth in this face | none (single plane) | none |
| Step the eye reads as a "recess" | wing west face x 10.67 → tower face x 28.5 = **17.8 ft** at y 54.2 (A1.01/A1.02, v008 G-9/G-11); tower top 40.0 vs wing roof edge 33.3 = 6.7 ft | unchanged v008 geometry |
| Surface / finish | PNL1 Bone White ACM from the CW1 head (24.6) to the top (40.0 at x 30, R, sloping to 36.0 at x 71); CW1 curtain wall 0–24.6 | `FR_WEST_PNL1_W2b` one face 24.6–40; `FR_WEST_GLZ_W2` backdrop below with the 16 CW1 opening placeholders |
| Vertical / horizontal limits | z 24.6–40.0; y 54.2–74.38 (20.18 ft) | identical |
| Openings above 24.6 | none | none |

## 3. Objects changed (from `BI_compare_v010_v011.json`: 808 of 810 v010 objects identical)

| Object | Before | After | Faces dropped |
| --- | --- | --- | --- |
| `FR_WEST_PNL1_W2b` | 3 faces, 484.1 sq ft, 1 coplanar overlap | **1 face, 310.8 sq ft**, 0 overlaps; union coverage on x 28.47 = 310.8 = band face above 24.6 (20.18 × 15.4) | face 0 duplicate (142.5), face 2 buried at x 70.97 inside the band (30.8) |
| `FR_WEST_GLZ_W2` | 59 faces, 298.0 sq ft, 20 coplanar overlaps | **38 faces, 159.3 sq ft**, 0 overlaps; union coverage = 159.3 vs expected 159.5 (face below 24.6 minus the 16 openings on the plane; the 0.2 sq ft is the 0.03-ft rounding of opening strips) | 20 duplicate strips (0.2–10.3 sq ft) + 1 buried face at x 70.97 (93.4) |
| Everything else | 808 objects | identical (vertices, transforms, material indices, slots, collections, visibility) | — |
| Added | — | cameras `BI_cam_tower_closeup` (−52,122,14)→(28.5,64,27) lens 55, `BI_cam_tower_side_depth` (−30,140,24)→(22,58,20) lens 40, `BI_cam_tower_west_elevation_ortho` (−42,64.3,20) looking +x, ortho 60 ft | — |
| Materials / world / view / samples | — | 0 node trees changed, world and view identical, 256 samples | — |

Preserved exactly (hash `367f0bc0…` over the 783 other mesh objects before and after): v010 drive, loop, median island, curbs, plaza, walks, terrain, all landscape, the canopy, the vestibule, every other building and facade object; all materials elsewhere; all cameras except the three added.

## 4. Mesh validation (affected area)

| Check | Result |
| --- | --- |
| Coplanar overlapping faces in the two regions | 0 pairs after (21 before) |
| Zero-area faces | 0 |
| Normals | all faces of both regions face west (−x), 0.03 ft in front of the wall |
| Missing polygons / holes | coverage of the tower face = exact (310.8 / 310.8 above 24.6; 159.3 / 159.5 below, minus openings) |
| Duplicate / coplanar faces elsewhere on the entrance facade | none within the two regions; the lobby-band prism `BI_Z2_band_E_F2` is closed and manifold (8 faces, 0 boundary edges); the south-wing Level 2 prism shares the plane x 28.5 inside the zone union (approved v008 shell, covered by the region, no visual effect — noted, untouched) |
| Cutters / openings | no opening cutter touches this face above 24.6; the 16 CW1 placeholders below are unchanged |
| Facade finish coverage | matches the documented condition (§2) |
| Remaining same-class items outside the entrance scope | 6 pairs of 1-ft parapet-return strips (`FR_SOUTH_PNL1_S8` 3/4, 7/8, 11/12; `FR_EAST_BRK1_E1` 10/11, 18/19; `FR_WEST_PNL1_W1c` 6/7; 3.7–6.2 sq ft) → **F-9**, carried forward, not changed |

## 5. Render validation (`renders\Building_I\`)

`BI_entrance_facade_v011_1_entrance_eye_level.png` (the v010 view in which the void was visible), `_2_tower_closeup.png`, `_3_tower_side_depth.png` (proves the 17.8 ft step and the 6.7 ft tower rise), `_4_tower_west_elevation_ortho.png` (straight-on), `_5_v009_entrance_camera.png`, before/after pairs `_before_after_{1_entrance_eye_level,2_tower_closeup,4_tower_west_elevation_ortho}.png` (the "before" frames were rendered from the untouched v010 scene through the same cameras by the build script before the fix). Settings = v009 (Cycles OptiX, 256 samples, AgX, exposure −4.3); 25–36 s per view. Inspected: the black patch is gone in every view; the tower reads as one continuous plane; the darker lower part of the tower in the west elevation is the sky occlusion of the inside corner with the wing (sun from the east-north-east, west faces in shade), not an artifact.

## 6. Confirmations

| Check | Result |
| --- | --- |
| `BI_freeze_BuildingI_v010_pending_approval.json` (182 files: all v001–v010) | PASS |
| `BI_freeze_BuildingI_v009_pre_v010.json` (155), `BI_freeze_BuildingI_v008_approved.json` (142) | PASS |
| `BI_freeze_sources_BuildingI_longpath_v001.json` (1,231) | PASS — `source_documents` unchanged |
| Building II | not touched (the 17 Building II model files reported by the project manifest remain where someone moved them, `models\Building_II\`, hashes identical — see the v010 report) |
| Building geometry (509 building/facade objects other than the two regions), canopy, vestibule, v010 site, landscape, materials | identical |

## 7. Files created in this pass

```
notes/Building_I/BI_entrance_facade_audit_v011.md
notes/Building_I/BI_entrance_facade_v011_build_report.json
notes/Building_I/BI_entrance_facade_validation_v011.md
notes/Building_I/BI_compare_v010_v011.json
notes/Building_I/manifests/BI_freeze_BuildingI_v011_pending_approval.json
scripts/Building_I/BI_build_entrance_facade_fix_v011.py
scripts/Building_I/BI_compare_geometry_v010_v011.py
scripts/Building_I/BI_entrance_facade_composites_v011.py
models/Building_I/BI_entrance_facade_v011.blend
renders/Building_I/BI_entrance_facade_v011_{1_entrance_eye_level,2_tower_closeup,3_tower_side_depth,4_tower_west_elevation_ortho,5_v009_entrance_camera}.png
renders/Building_I/BI_entrance_facade_v011_before_{1_entrance_eye_level,2_tower_closeup,4_tower_west_elevation_ortho}.png
renders/Building_I/BI_entrance_facade_v011_before_after_{1_entrance_eye_level,2_tower_closeup,4_tower_west_elevation_ortho}.png
```

Next decision for the owner: **approve or redirect v010 + v011 together** (entrance site + entrance facade), then freeze v001–v011. Not started: presentation realism continuation, interiors, signage, people, vehicles, viewer work.
