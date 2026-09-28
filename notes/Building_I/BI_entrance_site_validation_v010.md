# Building I — entrance / porte-cochere site correction v010: validation and completion report

Date: 2026-09-23
Model: `models\Building_I\BI_entrance_site_v010.blend` (810 objects = 800 of v009 + 7 site objects + 3 cameras), built by `scripts\Building_I\BI_build_entrance_site_v010.py` from `BI_entrance_site_data_v010.json` on top of `BI_presentation_v009.blend`. Audit: `BI_entrance_site_audit_v010.md` (§1–8 before any change, §9 trial findings). Build report: `BI_entrance_site_v010_build_report.json`. Comparison: `BI_compare_geometry_v009_v010.py` → `BI_compare_v009_v010.json`. Composites: `BI_entrance_site_composites_v010.py`.
Status: **built and validated, NOT approved.** v001–v009 frozen (`manifests\BI_freeze_BuildingI_v009_pre_v010.json`, 155 files, PASS; `BI_freeze_BuildingI_v008_approved.json`, 142 files, PASS). v009 was not approved by the owner (missing entrance site condition); its shader / sky / camera work is carried into v010 unchanged.

## 1. What was wrong (root causes, all v003 site artifacts)

1. The v003 asphalt polygon was flood-filled from the CS-101 heavy linework and stopped wherever it hit a line: no drop-off loop east of x 22, no median island, the plaza in front of the canopy covered by asphalt up to y 90.4, 137 jagged vertices along leaders and hatch.
2. 42 values of the two STORM DRAINAGE CHART tables printed over the entrance area of CG-101 (rectangles x −29.5…37 / 39…80.5, y 111…143; values 655.40–660.12) had been harvested as spot elevations → a 3–5 ft inverse-distance pit right in front of the porte cochere, which the asphalt slab and the plants followed.
3. Three roof-drain pipe labels of the PCO 50 CG-101 bulletin ("656.00 (WYE-100)", "659.80 (BEND-43)", "659.80 (BEND-101)") had been harvested as TOC/BOC spots → a 4-ft cone in the paved nose in the first v010 trial.

## 2. Documented configuration modeled (CS-101 rev 13 07.22.25 in PCO 17 p.10, vector curb chains + written dimensions; grades CG-101 PCO 24 p.11 / PCO 50 p.4–5)

| Element | Documented | v010 model | Code |
| --- | --- | --- | --- |
| Drop-off lane at the porte cochere | face of curb y 88.37, back 89.87; **14.50'** wide to the nose; (6) bollards | asphalt to the face of curb; plaza from the back of curb; bollards not modeled (site furnishing) | V / W |
| Entry drive west of the island | **24.00'** (end-island curb x −8.4 → island outer curb 15.63) | 24.03 measured on the chains | W / V |
| Lane → return-lane curve | **R26.50'** from (26.7, 88.37) to (53.2, 114.87) | 16-chord polyline of the chain | W / V |
| Return lane east of the island | island outer curb x 29.70 → east face of curb **x 53.2** (12.50' lane + 11.00') | 23.5 total | W / V |
| Loading zone / north end of the loop | face of curb x 53.2 to y 182.5 then the curve to (17.1, 207.0) | as chained; the curb ring fades over the last 8 ft of the window (y 202–210) | V |
| Drive aisle from the north lot / diagonal approach | aisle south face of curb y 123.44; R9.50'; 45° diagonal (−46.3, 117.7)→(−18.2, 89.6); R12.50' / R4.00' | as chained (v003 had y 126.6) | V / W |
| **Median island, planted oval** | outer curb x 15.63–29.70, y 112.37–168.0 (55.6 ft), inner width **11.08'** (11.07 measured), **R5.50'** ends | mulch slab at curb-top level, 739.9 sq ft, 11 EMRA re-seated on it | W / V |
| **Median island, paved nose** | concave **R31.00'** (centre (−15.4, 156.0)) from the oval to (−4.52, 126.92), **R7.50'** nose (circumradius 7.51) to (−1.88, 112.37), straight south edge y 112.37 | concrete slab at curb-top level, 513.2 sq ft | W / V |
| Parking end island | **12.20'** wide, x −41.1…−6.4, y 146.9–162.1 | mulch slab, 437.9 sq ft | W / V |
| Canopy plaza | pavers from the back of curb (89.87) to the vestibule / lobby faces and the west entry plaza (y 74); **8.50'** east walk (x 51.7–60.5) north to the loading zone; planting bed x 60.5–71 from y 100 (LP-101 rows) | 2,241.1 sq ft paver slab at curb-top level | V / W |
| Diagonal walk | **7.00'** pavers south-west of the diagonal back of curb | 278.8 sq ft | W / V |
| Aisle walk | **8.00' / 8.50'** concrete south of the aisle back of curb, x −95.07 … −45.23 | 480.7 sq ft | W / V |
| **Curb** | double line 1.5 ft apart on CS-101; TOC − BOC = **0.50** at every CG-101 pair | `SITE_curb_entrance_drive_CS101`: 1.5-ft concrete ring along the whole drive polygon inside the window, top at the curb-top field, 992 sq ft | V / W |
| Crossings | none drawn at the loop | none | — |

Registration: `x_BI = 141.0 + (X − 1859.0)/3.6`, `y_BI = 173.53 − (Y − 1211.1)/3.6` (1" = 20'); vestibule and north-block faces check within 0.4 ft. The overlay `renders\Building_I\BI_entrance_site_v010_overlay_plan_top.png` draws the CS-101 curb chains (blue) over the v010 polygons (green) and the replaced v009 outline (red): every v010 edge lies on a documented curb line except the north-west part of the merged polygon, which is the v003 outline kept where it was already on the curb (x < −45 or y > 162).

## 3. Grades (CG-101 / PCO 50; written values, positions ±0.3 ft)

| Location | Spot | v010 surface |
| --- | --- | --- |
| Drop-off lane, west end of the curb | TOC 660.11 / BOC 659.61 (−17.8, 99.5) | gutter 659.6 |
| Canopy west columns | TOC 660.32 / BOC 659.82 (−0.5, 96.8) | gutter 659.8 |
| Median nose | TOC 661.36 / BOC 660.86 (9.3, 125.2 / 122.6) | gutter 660.86, nose top 661.36 |
| Return lane | TOC 661.14 / BOC 660.64 (41.5, 126.9 / 124.2); **HP 660.93 (39.7, 141.8)** | crown in the return lane |
| Island north end | TOC 660.74 / BOC 660.24 (9.3, 166.8 / 164.1); TOC 661.12 / BOC 660.62 (41.4, 170.2 / 167.5) | |
| Entry drive north | TOC 660.50 / BOC 660.00 (10.4, 176.3); TOC 661.72 / BOC 661.22 (31.5, 178.5) | |
| Parking end island | TOC 659.74 / BOC 659.24 (−1.7, 143.2); TOC 659.07 / BOC 658.57 (−19.0, 143.1); TOC 660.24 / BOC 659.74 (6.2, 150.6) | |
| Diagonal curb | TOC 659.48 / BOC 658.98 (−33.9, 125.0) | |
| Canopy plaza | 661.47, 661.57, 661.69, FFE 661.75 at the doors, 661.36 (40.4, 107.7), 661.42 (44.9, 117.7) | plaza 661.4–661.7 falling west |
| Drainage | lane gutter falls **west** from the nose to the canopy west end (~1.1 % over 100 ft); return lane crowns at HP 660.93 and falls north; area drains AD-105CM / AD-204 at the west end of the canopy walk | reproduced by the interpolated fields (I) |

Interpolation (I): gutter field G = inverse-distance (1/d³) of TOC − 0.50 / BOC / pavement spots / ground spots − 0.50 on the 376 cleaned spots; ground / curb-top field T = G + 0.50; asphalt = G + 0.10 (v003 convention), curb top = T + 0.03, island / plaza / walk tops = T, terrain = T. Both fields fade into the plain inverse-distance surface over the outer 8 ft of the regrade window so the untouched v003 terrain is met continuously (boundary vertices keep their v003 heights: max difference 0.323 ft, mean 0.10 ft).

## 4. Objects changed (from `BI_compare_v009_v010.json`; 747 of 800 v009 objects identical)

| Class | Result |
| --- | --- |
| Building, facade regions, openings, canopy (511 `BI_*` / `FR_*` objects) | **identical** (vertices, transforms, material indices, slots, collections) |
| Site objects untouched | all other `SITE_*` / `CTX_*` objects identical (parking lot, walks south/east, streets, walls, skirt, Building II mass) |
| `SITE_asphalt_west_drive_dropoff` | **replaced**: 380-vertex flood fill → 248-vertex documented outline (v003 part kept where correct), 27,075 sq ft, grid slab 4 ft clipped to the outline; bbox x −143.5…53.0, y 88.5…309.75 |
| `SITE_terrain_IDW_INTERPOLATED` | **regraded inside the window only** (x −130…110, y 60…210): 1,379 faces removed, 860 cells rebuilt on the T field as a closed slab, cut by the exact boolean with the pavement solids (drive face-of-curb prism, plaza, diagonal walk, aisle walk, v003 entry plaza), 1,839 faces joined back; every face outside the window verified identical by 40-ft band counts (161/161/1061/950 … 390/517/514) and the v003 winding kept |
| Added | `SITE_curb_entrance_drive_CS101` (992 sq ft), `SITE_entry_island_oval_bed_CS101` (739.9), `SITE_entry_island_nose_paved_CS101` (513.2), `SITE_parking_end_island_12ft_CS101` (437.9), `SITE_walk_canopy_plaza_pavers_CS101` (2,241.1), `SITE_walk_diagonal_pavers_CS101` (278.8), `SITE_walk_aisle_concrete_CS101` (480.7); cameras `BI_cam_entrance_plan_top` (ortho 240 ft), `BI_cam_entrance_eye_level` (−78, 150, 5.5)→(30, 92, 9), `BI_cam_entrance_site_elevated` (−175, 275, 120)→(20, 112, 5) |
| Removed | none |
| Materials | 0 node trees changed, 0 added, 0 removed; new objects use the existing v009 materials (`SITE_asphalt`, `SITE_concrete_walk`, `SITE_pavers_Techo-Bloc_Westmount_Onyx_placeholder`, `LS_mulch`) |
| World, view transform, exposure, samples | identical to v009 |

## 5. Landscape coordination

- 51 landscape objects intersecting the window were rebuilt (`landscape_objects_rebuilt` in the build report): 21 shrub / ground-cover groups with their mulch discs, 8 interpreted ground-cover discs, 5 trees, the unresolved-symbol object. **0 plants moved in x, y**; 246 positions re-seated in z, 143 changed by more than 0.05 ft. Per-plant records (object, x, y, z_old, z_new) are in the build report.
- Largest z corrections (all out of the former pit): LAMB disc n4 at (62.05, 111.99) +5.33 ft; SNOW n9 +1.4…+4.5; DOUB n5 +0.3…+4.0; LAMB n6 +3.2…+3.5; ILST n2 +1.1…+3.4; the 11 EMRA of the median +0.8…+2.1 (now on the island bed); the SEAS annual disc +2.19. Positions outside the window keep their v009 z exactly (10 positions had no surface in v004 either and use v004's own interpolation, unchanged).
- The 8 plants along the east walk (DOUB / LAMB / SNOW / VANG / ILST / BLON, x 61–70) were on the paver slab in the first trial; the plaza was corrected to stop at the documented 8.5-ft walk, so they are seated on the bed, not skipped.
- The SEAS annual disc (LP-100 callout 170, interpreted leader disc at (20.7, 132.5)) now sits on the island bed among the EMRA row; it remains an interpreted item (radius and position by leader only).
- No planting added; the 117 species-unresolved symbols, the 11 interpreted discs and the 7 unmodeled hatched ground covers are carried unchanged.

## 6. Validation renders (`renders\Building_I\`)

`BI_entrance_site_v010_1_entrance_plan_top.png` (ortho, 2400 × 1600, 10 px/ft), `_2_entrance_eye_level.png`, `_3_porte_cochere_oblique.png`, `_4_entrance_site_elevated.png`, `_5_v009_entrance_camera.png`, `_5_before_after_v009_camera.png` (v009 | v010 from the same camera), `_overlay_plan_top.png` (documented curb lines / v009 outline / v010 polygons / regrade window). Render settings = v009 (Cycles OptiX, 256 samples, AgX, exposure −4.3); 28–45 s per view.
Checked in the renders: no terrain through the asphalt or the walks, no pit or cone, no z-fighting between slab and terrain (terrain is cut, curb ring 1 cm above the walks), no faceted mounds (grid slabs), plants seated on their surfaces, the untouched terrain continuous at the window edge.

## 7. Confirmations

| Check | Result |
| --- | --- |
| `BI_freeze_BuildingI_v009_pre_v010.json` (155 files: every v001–v009 note, data, script, model, render) | PASS |
| `BI_freeze_BuildingI_v008_approved.json` (142) | PASS |
| `BI_freeze_sources_BuildingI_longpath_v001.json` (1,231 source files) | PASS — `source_documents` unchanged |
| `BI_freeze_project_and_BuildingII_v001.json` (311) | 294 PASS; **17 Building II model files are reported MISSING at their frozen paths** (`models\blender_test_v001–v002.blend`, `models\building_shell_v001–v015.blend`): they now sit in `models\Building_II\` (folder timestamps 11:51–11:53 today, before this build started) with **identical SHA-256** — moved by someone else, not by this work, which never touches Building II. Not corrected here (Building II is out of bounds); the manifest needs re-pointing by the owner. |
| Building I building geometry (511 objects) | identical (hash `54c6f0fb…` before/after in the build script; comparison script agrees) |
| Unrelated site geometry, plants outside the window, all materials | identical (720 kept mesh objects hash `d5555f9b…`; 0 material node trees changed) |
| Frozen v009 renders / model | untouched (v010 renders carry the `BI_entrance_site_v010_` prefix) |

## 8. Assumptions and items still unresolved

- Pavement surface between spots is interpolated (I); no cross-slope or crown profile is written except HP 660.93; gutter pans, curb-and-gutter profile and the curb's own batter are not modeled (a flat 1.5-ft curb top 0.50 ft above the gutter, A).
- The oval's planting surface at curb-top level (A; the LP-101 "mound 6 in" note applies to the parking-lot islands).
- The curb ring and the fields fade to the v003 condition over the outer 8 ft of the window (y 202–210 at the loading-zone end, x −130…−122 at the west end): the curb height there is not documented differently, it is simply where the correction stops (A).
- Bollards, striping, the accessible-route markings, signage and the loading-zone hatch are not modeled (site furnishing / presentation scope).
- Canopy depth G-2 unchanged: the documented lane curb at y 88.37 lies under the modeled canopy (north edge 99.96); the civil base draws a shallower canopy.
- Paver module / pattern undocumented (placeholder colour); nose and aisle walk concrete by hatch.
- Carried unchanged: G-1…G-6, G-15 brick-ledge tolerance, gallery soffit 9.0 (M), north overhang 14.83 (A), rear vestibule parapet 32.0 (R), F-1…F-8, SC-1 dumpster, SC-3 parking-lot outline, LC-2, 117 unresolved species, interpreted discs, landscape-wall footing, all v009 presentation placeholders.

## 9. Files created in this pass

```
notes/Building_I/BI_entrance_site_audit_v010.md
notes/Building_I/BI_entrance_site_data_v010.json
notes/Building_I/BI_entrance_site_v010_build_report.json
notes/Building_I/BI_entrance_site_validation_v010.md
notes/Building_I/BI_compare_v009_v010.json
notes/Building_I/manifests/BI_freeze_BuildingI_v009_pre_v010.json
notes/Building_I/manifests/BI_freeze_BuildingI_v010_pending_approval.json
scripts/Building_I/BI_build_entrance_site_v010.py
scripts/Building_I/BI_compare_geometry_v009_v010.py
scripts/Building_I/BI_entrance_site_composites_v010.py
models/Building_I/BI_entrance_site_v010.blend
renders/Building_I/BI_entrance_site_v010_{1_entrance_plan_top,2_entrance_eye_level,3_porte_cochere_oblique,4_entrance_site_elevated,5_v009_entrance_camera,5_before_after_v009_camera,overlay_plan_top}.png
```

Next decision for the owner: **approve or redirect the v010 entrance site correction** (then freeze v001–v010 and resume presentation realism on the corrected site). Not started: further presentation realism, interiors, signage, people, vehicles, viewer work.
