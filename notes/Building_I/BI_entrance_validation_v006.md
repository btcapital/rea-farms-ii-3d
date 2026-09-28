# Building I — entrance geometry correction v006: comparison and validation report

Date: 2026-09-22
Model: `models\Building_I\BI_landscape_v006.blend` (729 objects = 726 from the approved v005 + 3 validation cameras), built by `scripts\Building_I\BI_build_entrance_fix_v006.py`. Control document: `BI_entrance_geometry_control_v006.md`. Build report: `BI_entrance_v006_build_report.json`. Comparison script: `BI_compare_geometry_v005_v006.py`.
Status: **built and validated, NOT approved.** v005 remains the frozen approved baseline (85 files, manifest PASS).

## 1. Objects changed (object-by-object comparison v005 → v006)

| Object | What changed | Previous | Corrected | Difference | Source |
| --- | --- | --- | --- | --- | --- |
| `BI_open_NORTH_015, 017, 020, 023, 026, 031, 032` (L2 curtain-wall lites, z 17.13–24.58) and `BI_open_NORTH_018, 022, 025, 028, 030` (transom band, z 11.69–14.02), x 40.67–63.67 | translated in y only | plane **y = 83.56** (vestibule north face, grid G.2) | plane **y = 74.36** (E–F.2 band north face, grid F.2 = 74.54) | **−9.20 ft**; x and z extents unchanged | A5.18 A2 wall section (curtain wall on F.2 from LVL-01 to roof; vestibule F.2→G.2 below the gallery line); A1.02 Level 2 wall lines y 72.5–74.25 (vector, 6.750 pt/ft); A7.26 B1 CW1 24'-6" high; A7.34 "CW sill @ entry vestibule roof" |
| `BI_Z4b_north_block_south_part` | faces only: 24 old cap faces and 10 sliver side faces removed; caps rebuilt as the rectangle (71, 70.58)–(271.38, 70.58)–(271.38, 97.75)–(71, 97.75); west closure face on existing vertices (71, 70.58)–(71, 74.5); 16 vertices left unused removed | self-overlapping outline with a 0.5-ft U-sliver west of x = 71; cap tessellation bridging the entrance notch (8 triangles at z ≈ 33, the false overhang); sliver north face at y 74.5 covering the curtain wall x 60.25–71 | clean prism x 71–271.38 × y 70.58–97.75 (+ the buried south face to x 28.71); **0 triangles in the notch**; no face north of y 74.38 west of x 71 | vertex count 28 → 12; **0 vertices moved, 0 added**; bounding box identical | A1.00c roof edge at F.2 (no roof between F.2 and H.1 at grids 3–6); A5.18 A2 (roof/parapet end at the F.2 curtain wall); A1.02 (no wall at y > 74.25 on Level 2 west of grid 6) |
| `FR_NORTH_BRK1_N1`, `FR_NORTH_GLZ_N2`, `FR_NORTH_PNL1_N3`, `FR_WEST_GLZ_W2`, `FR_WEST_PNL1_W2b` | finish-region polygons regenerated with the unchanged v005 region data: the moved lites are now subtracted on plane 74.38, and the band faces adjoining the removed sliver are no longer mis-classified as buried | — | — | 51 other region objects byte-identical | consequential (§3 of the control document) |
| cameras | added `BI_cam_entrance_elevation_ortho`, `BI_cam_entrance_oblique`, `BI_cam_entrance_side_depth` | — | — | validation only | — |

Not changed (verified by hash of 645 mesh objects and by the comparison): the lower entrance canopy (`BI_canopy_*`, 10 objects — **canopy geometry unchanged**), the vestibule `BI_Z3_vestibule_100`, its doors and side lites (`BI_open_NORTH_*` at z ≤ 8.52 on y 83.58), all other openings (364), the band `BI_Z2_band_E_F2`, the wing, the north block `BI_Z4a`, the end block, parapets, mechanical screen, all `SITE_`, `CTX_` and `LS_` objects, all materials, all existing cameras.

## 2. Original source / logic that caused the errors

- Placeholders: `BI_build_shell_v001.py::face_coordinate()` placed every north-facing opening on the outermost footprint boundary at its x regardless of height, so lites within the vestibule's x-range were attached to the 9-ft vestibule face even above its roof. They were misplaced, not duplicated.
- Overhang: the v001 Level-2 slab-edge trace produced a self-overlapping outline for the north-block-south-part prism (a thin U hugging the E–F.2 band); the single cap polygon over that outline could not be tessellated correctly and Blender bridged the re-entrant notch with four top and four bottom triangles, reading as a horizontal plate at z ≈ 33 from the band face out to y = 97.75. The same sliver stood 0.12 ft proud of the band wall over the curtain wall (the black strip in earlier renders). Nothing in the drawings has geometry there: not a parapet, slab edge, canopy duplicate or raster shape.

## 3. Source sheets confirming the corrected condition

A5.18 A2 "Wall Section @ Primary Entry Vestibule" (rev 13, 7/25/2025); A5.19 A1/A2 (vestibule sections); A7.26 B1/B2/A1/A2 (curtain-wall elevations at the entry vestibule, 41'-7" × 24'-6"; vestibule head 8'-9"); A7.34 (curtain-wall head/sill details at the vestibule); A1.13 A1 (vestibule 1'-9" + 10'-3" + 10'-3" + 1'-9", canopy gutter on G.2); A1.02 (Level 2 wall lines, registered vector); A1.00c (roof edge at F.2). Photographs 2026-07-28 and 2025-09-09 agree (two-storey glazed lobby wall behind a low vestibule and the flat canopy; no upper overhang) and were used for validation only.

## 4. Validation

| Check | Result |
| --- | --- |
| Hash of every mesh object except the 12 placeholders, `BI_Z4b_north_block_south_part` and the `FR_*` regions (645 objects) before/after | identical (`f513c3c3…4a39`) |
| Independent comparison (`BI_compare_geometry_v005_v006.py`) | 0 missing objects; 18 changed (12 openings by −9.20 ft in y, 1 shell object faces only, 5 regions); 3 cameras added; Z4b bounding box identical, 0 triangles in the entrance notch |
| Canopy | 10 canopy objects unchanged |
| Site and landscape | 0 `SITE_`/`CTX_`/`LS_` objects changed |
| `BI_freeze_BuildingI_v005_approved.json` (85 files: all v001–v005 notes, data, scripts, models, renders) | PASS |
| `BI_freeze_project_and_BuildingII_v001.json` (311) | PASS |
| `BI_freeze_sources_BuildingI_longpath_v001.json` (1,231 source files) | PASS |
| Renders inspected | entrance close-up (same camera as the v005 validation view), straight-on entrance elevation (orthographic), entrance oblique, side/depth view: overhang gone, glazing on the wall plane, vestibule and canopy in front, no black strip |

## 5. Renders

`renders\Building_I\BI_entrance_v006_entrance_closeup.png`, `_entrance_elevation_ortho.png`, `_entrance_oblique.png`, `_entrance_side_depth.png`, `_front_north_elevation.png`, and the before/after pairs `BI_entrance_v006_before_after_{entrance_closeup, entrance_elevation_ortho, entrance_oblique, entrance_side_depth}.png` (left: frozen v005 rendered from the same cameras; right: v006).

## 6. Still uncertain

Vestibule height 9.0 ft (v001 assumption A-1; A7.26 head 8'-9" plus the A5.19 roof build-up not summed); curtain-wall outer face ≤ 0.4 ft north of grid F.2 not modeled (band face at 74.38 used); placeholder lite extents remain raster-detected (R); the entrance ACM soffit/portal (A7.32) not modeled. All earlier G-, F-, SC- and LC-items carry forward; G-7 is closed by this version.

## 7. Files created in this pass

```
models/Building_I/BI_landscape_v006.blend
notes/Building_I/BI_entrance_geometry_control_v006.md
notes/Building_I/BI_entrance_v006_build_report.json
notes/Building_I/BI_entrance_validation_v006.md
notes/Building_I/manifests/BI_freeze_BuildingI_v005_approved.json
renders/Building_I/BI_entrance_v006_{entrance_closeup,entrance_elevation_ortho,entrance_oblique,entrance_side_depth,front_north_elevation}.png
renders/Building_I/BI_entrance_v006_before_after_{entrance_closeup,entrance_elevation_ortho,entrance_oblique,entrance_side_depth}.png
scripts/Building_I/BI_build_entrance_fix_v006.py
scripts/Building_I/BI_compare_geometry_v005_v006.py
```

Next decision for the owner: **approve or redirect the v006 entrance correction.**
