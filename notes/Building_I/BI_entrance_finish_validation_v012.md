# Building I — lobby-tower finish correction v012: validation and completion report

Date: 2026-09-23
Model: `models\Building_I\BI_entrance_finish_v012.blend` (v011 + 2 finish-region objects + 1 validation camera), built by `scripts\Building_I\BI_build_entrance_finish_fix_v012.py` on top of `BI_entrance_facade_v011.blend`. Audit: `BI_entrance_finish_audit_v012.md`. Build report: `BI_entrance_finish_v012_build_report.json`. Comparison: `BI_compare_geometry_v011_v012.py` → `BI_compare_v011_v012.json`. Composites: `BI_entrance_finish_composites_v012.py`.
Status: **built and validated, NOT approved.** v001–v011 frozen (`manifests\BI_freeze_BuildingI_v011_pending_approval.json`, 202 files, PASS after this pass). v010 (entrance site) and v011 (tower west-face regions) are carried unchanged and are themselves awaiting approval.

## 1. What was wrong and what changed

| | |
| --- | --- |
| Face changed | the **lobby tower's north (front) face** on the band plane y 74.38 between its west corner x 28.5 and grid 3.7 (x 40.0), full height, plus the 0.7-ft slivers x 40.0–40.7 below the curtain-wall head |
| Previous material | BRK1 Endicott Manganese Ironspot utility brick (`FR_NORTH_BRK1_N1`, 12 faces, 344.3 sq ft) and PNL1 on the slivers (`FR_NORTH_PNL1_N3`, 3 faces, 17.1 sq ft) |
| Corrected material | **PNL1 Alucobond PLUS Bone White** on the face above the curtain-wall head (x 28.5–40.0, z 24.08–40.0, 176.9 sq ft → new object `FR_NORTH_PNL1_N3b`); **curtain-wall backdrop placeholder** (`GLZ_Viracon_VZE1-42_in_EFCO_framing_placeholder`, the same as `FR_NORTH_GLZ_N2` uses for x 40.7–70.3) on the 14 pier / spandrel faces below the head (x 28.5–40.7, z 0–24.6, 184.4 sq ft → new object `FR_NORTH_GLZ_N2b`) |
| Source | A4.02 Building North Elevation, Rev 14: the tower's north face is one element from x 28.5 to x 71 — CW1 from grade to the head and the white PNL1 panel with the sloping top above it, tagged "PNL1"; the two "BRK1" tags beside it sit on the wing north face (y 54.2) drawn in projection (corner zoom in the audit §2). A7.26: CW1 41'-7" wide = x 28.6–70.2. A4.02 West Elevation: PNL1/CW1 tower, PNL1/PNL2 north-block face beyond, BRK1/PNL1 wing face. Legend: PNL1 "shown in white". Closeout: Alucobond PLUS Bone White = PNL1. |
| Photograph | `drone_2026-07-28_a.jpg` (genuine, validation only): the tower front above the canopy is a continuous white ACM box, the lower tower is dark glazing, brick only on the wing (left) and the north block (right). **Agrees.** No new photo was found in the source folders; this frame is the clearest genuine view of the tower front. |
| Geometry | **no vertex moved, added or removed**: the union of the vertex sets of the four region objects after = the union before (build-script assertion); the 15 faces keep their coordinates and only change object and material. Wall, curtain-wall lite placeholders (`BI_open_NORTH_010…014` etc.), canopy, vestibule, doors, roof, site, landscape: identical (hash `467de669…` over the other 783 mesh objects; comparison script: 811 of 813 v011 objects identical, the two region objects that lost faces changed, two region objects and one camera added). |
| Material node trees | 0 changed; no material added or removed (only assignments changed) |

## 2. Adjacent faces that remain brick, and why

| Face | Region | Why it stays BRK1 |
| --- | --- | --- |
| Wing north face y 54.2, x 10.67–28.5, z 0–33.3 (with SF1 windows) | `FR_NORTH_BRK1_N1` (wing part, 38 faces left, 662 sq ft) | A4.02 north elevation: the BRK1 tags, soldier-band note and brick hatch are on this face (corner zoom); it is the brick wall the reviewer sees left of the tower |
| Wing west face x 10.67, z 0–33.3 | `FR_WEST_BRK1_W1` | A4.02 west elevation: BRK1 with SF1 between grids D and A |
| North block west face x 71, y 97.75+ | `FR_WEST_BRK1_W5` | v005 regions, unchanged; not part of this audit |
| North block west face x 71, y 74.38–97.75 (the recess east of the tower) | `FR_WEST_PNL2_W4` (0–15.33) / `FR_WEST_PNL1_W4b` above | A4.02 west elevation: PNL1 over PNL2 between F.2 and H.1 — dark ACM, not brick; unchanged |
| Tower west face x 28.5 | `FR_WEST_PNL1_W2b` / `FR_WEST_GLZ_W2` (v011) | PNL1 above the head, curtain wall below; unchanged |

No dark ACM (PNL2) occurs on the tower; PNL2 occurs only on the north-block recess face and (per the drawing note) on the canopy column wraps, which are not modeled (F-1).

## 3. Mesh / assignment validation (from the build report)

| Check | Result |
| --- | --- |
| Faces moved | 15 (12 from `FR_NORTH_BRK1_N1`, 3 from `FR_NORTH_PNL1_N3`), 361.4 sq ft, listed face-by-face with x, z, old and new material |
| Vertex multiset of the four region objects | identical before / after |
| Coplanar overlaps between the north-face region objects on the band plane | 0 |
| Coverage of the band north face (x 28.5–71, 0–40) by regions + lite placeholders | 1,666 sq ft union vs the wall face's 1,615 sq ft (the union exceeds the face because the lite placeholders include their frames; no gap) |
| Normals | all +y (unchanged faces) |
| Unrelated geometry (783 other mesh objects) | identical (hash) |
| Cameras | `BI_cam_photo_match_drone_2026-07-28a` added (−235, 265, 62) → (35, 85, 14), lens 32; all other cameras untouched |

## 4. Renders (`renders\Building_I\`)

`BI_entrance_finish_v012_1_photo_match_drone.png` (approximate vantage of the 2026-07-28 drone photograph; the Building II context mass is hidden in this view only because the photo predates it), `_2_entrance_oblique.png` (v009 entrance camera), `_3_tower_closeup.png`, `_4_tower_corner_side.png` (the tower's north-west corner: PNL1 wrapping the corner above the head, curtain wall below, the brick wing face beyond), `_before_*` (same four cameras through the untouched v011 scene), `_before_after_{2_entrance_oblique,3_tower_closeup,4_tower_corner_side}.png`, and `_photo_vs_render.png` (photo | v011 | v012 side by side). Settings = v009 (Cycles OptiX, 256 samples, AgX, exposure −4.3); 16–33 s per view.

## 5. Confirmations

| Check | Result |
| --- | --- |
| `BI_freeze_BuildingI_v011_pending_approval.json` (202 files: all v001–v011) | PASS |
| `BI_freeze_BuildingI_v010_pending_approval.json` (182), `BI_freeze_BuildingI_v009_pre_v010.json` (155), `BI_freeze_BuildingI_v008_approved.json` (142) | PASS |
| `BI_freeze_sources_BuildingI_longpath_v001.json` (1,231) | PASS — `source_documents` unchanged |
| Geometry identical to v011 | yes (no vertex changed anywhere; comparison script: only the two region objects that lost faces differ, two region objects and one camera added) |
| Site / landscape / roof / openings / canopy / vestibule / doors | identical |
| Only supported material-region assignments changed | yes (§1) |

## 6. Files created in this pass

```
notes/Building_I/BI_entrance_finish_audit_v012.md
notes/Building_I/BI_entrance_finish_v012_build_report.json
notes/Building_I/BI_entrance_finish_validation_v012.md
notes/Building_I/BI_compare_v011_v012.json
notes/Building_I/manifests/BI_freeze_BuildingI_v012_pending_approval.json
scripts/Building_I/BI_build_entrance_finish_fix_v012.py
scripts/Building_I/BI_compare_geometry_v011_v012.py
scripts/Building_I/BI_entrance_finish_composites_v012.py
models/Building_I/BI_entrance_finish_v012.blend
renders/Building_I/BI_entrance_finish_v012_{1_photo_match_drone,2_entrance_oblique,3_tower_closeup,4_tower_corner_side}.png
renders/Building_I/BI_entrance_finish_v012_before_{1_photo_match_drone,2_entrance_oblique,3_tower_closeup,4_tower_corner_side}.png
renders/Building_I/BI_entrance_finish_v012_before_after_{2_entrance_oblique,3_tower_closeup,4_tower_corner_side}.png
renders/Building_I/BI_entrance_finish_v012_photo_vs_render.png
```

Next decision for the owner: **approve or redirect v010 + v011 + v012 together** (entrance site, tower west-face regions, tower front finish), then freeze v001–v012. Not started: presentation realism continuation, interiors, signage, people, vehicles, viewer work. Carried: F-1 (column wraps), F-9 (parapet-return duplicate strips), all earlier open items.
