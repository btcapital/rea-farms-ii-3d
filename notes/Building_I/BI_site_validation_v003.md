# Building I — site / grading baseline v003: validation and completion report

Date: 2026-09-22
Model: `models\Building_I\BI_site_v003.blend` (2,052 objects = 2,030 from the approved v002 file + 22 new), built by `scripts\Building_I\BI_build_site_v003.py` from `BI_site_data_v003.json` on top of the approved `BI_facade_v002.blend`. Control document: `BI_site_control_v003.md`. Build report: `BI_site_v003_build_report.json`.
Status: **built and validated, NOT approved.** Stopped at the site/grading approval gate (skill gate 4).

## 1. What was created

| Output | Content |
| --- | --- |
| `models\Building_I\BI_site_v003.blend` | v002 building unchanged + collection `08_Site_v003` (terrain 1, hardscape 10, walls/structures 5, context 5) + camera `BI_cam_site_elevated` |
| `renders\Building_I\BI_site_v003_front_north.png`, `_rear_south.png`, `_left_west.png`, `_right_east.png`, `_oblique_northwest.png`, `_site_elevated.png` | six views, neutral lighting; the Building II context mass is render-hidden in `_left_west` only (it stands between that camera and Building I) |
| `notes\Building_I\BI_site_control_v003.md`, `BI_site_data_v003.json`, `BI_site_v003_build_report.json` | control, data, report |
| `scripts\Building_I\BI_build_site_v003.py`, `BI_compare_geometry_v002_v003.py` | build, independent object comparison |

## 2. Site geometry added (all objects `SITE_` or `CTX_`, inside `08_Site_v003`)

| Object | Basis | Code |
| --- | --- | --- |
| `SITE_terrain_IDW_INTERPOLATED` | 4-ft grid, inverse-distance (1/d³) through 421 written spot elevations from CG-101 (PCO 50 p.4, Blythe canopy grades 10/15/2025); 9,452 faces; footprint, band, vestibule and cells under asphalt removed | interpolated |
| `SITE_asphalt_west_drive_dropoff` | drive loop polygon traced from CS-101 (PCO 17 p.10) curb lines | M ±1 ft, partial |
| `SITE_asphalt_parking_north_APPROX` | rectangle x −190…300, y 215…425; islands/stripes omitted | **A** ±5 ft |
| `SITE_walk_south_concrete`, `SITE_walk_west_of_wing_concrete`, `SITE_walk_east_concrete`, `SITE_walk_east_end_block_concrete`, `SITE_walk_ne_courts_concrete`, `SITE_walk_north_courts_concrete` | traced from CS-101 curb lines + approved footprint, +0.5 ft (6" curb from 121 TOC/BOC pairs) | M ±1 ft |
| `SITE_entry_plaza_pavers_Westmount_Onyx` | plaza north of the wing (CS-101 paver note) | M |
| `SITE_plaza_between_buildings_APPROX` | strip between Building II east face and west walk | **A** |
| `SITE_brick_landscape_retaining_wall_RFI78` | TW 661.00 (W), extent x 3.2…119.2 (M), bottom 658.5 (A) | W/M/A |
| `SITE_dumpster_enclosure_APPROX` | 25'-8" × 10'-11 3/8" × 6'-8" (A0.04, W) at the CS-101 label (M) | W/M/A |
| `SITE_foundation_skirt_A`, `_band_A`, `_vestibule_A` | approved footprint extruded 4 ft below FFE (visual, A) | A |
| `CTX_N_Rea_Park_Ln_88ft_ROW`, `CTX_Golf_Links_Dr_80ft_ROW`, `CTX_N_Old_Springs_Rd_61ft_ROW`, `CTX_Midway_Park_Dr_69ft_ROW` | right-of-way bands from CS-101 R/W labels | I ±5 ft |
| `CTX_Building_II_mass_from_BII_CS-101_rev6` | Building II outline from Building II CS-101 rev 6 (shared-site register), FFE 660.30, 43.83 ft high | shared-site |

Building placement: unchanged. The civil registration (fitted on the 94-ft court sidelines) puts the CG-101 building outline and the FFE 661.75 door spots on the approved v001 footprint within 0.2–0.6 ft, so no site document conflicts with the approved geometry and the building was not moved.

## 3. Exact documented grades vs interpolated

- **Exact (W):** FFE 661.75; Building II FFE 660.30; 421 spot elevations (169 TOC, 170 BOC, 174 SPOT, 2 HP, 1 LP, 2 FFE, 2 RIM), curb height 0.50 ft; TW 661.00 landscape wall; RFI 90 rims 661.20–661.59; average grades 660.5 / 660.0 / 659.5 / 660.0 (E/S/W/N).
- **Interpolated:** every terrain vertex between the spots (the whole `SITE_terrain_IDW_INTERPOLATED` surface), the top of every hardscape slab (terrain + documented offset), the street bands, and the terrain beyond the spot cloud (flat extrapolation). Contours from CG-101 were not used (labels not linked to linework).
- **Assumed (A):** parking-lot rectangle, plaza strip, wall bottom, skirt depth, dumpster orientation, street band positions (I), 0.10–0.13 ft asphalt render offset.

## 4. Building II civil sheets used (shared-site register, per `BI_revision_review_v002.md` §5.1)

| Sheet | File / page | Printed status | Used for |
| --- | --- | --- | --- |
| CS-101 Dimension Control Plan rev 6 | `source_documents\Building II\00 PLANS\Revision 5\Rea Farms 2 - Civil Drawings 03.17.26.pdf` p.7 | rev 6 03.10.26 | Building II outline for the context mass, Building II FFE 660.30, confirmation that the sheet base matches the Building I civil sheets |
| CG-101 Grading & Drainage Plan rev 6 | same file p.3 | rev 6 03.10.26 | 39 Building II-side spots reviewed for the shared plaza; not used for Building I geometry |

No Building II architectural drawing was used. No Building II model, script, note, render or export was opened.

## 5. Unresolved site conflicts and open items

SC-1 dumpster enclosure brick (Roman vs utility); SC-3 parking lot not traceable (stripes share the curb line weight) → APPROX rectangle without islands; SC-4 landscape wall height query in RFI 78, BW not written; SC-5 no sealed Building I civil set — only PCO bulletin sheets (RFI 58/78/90, Blythe canopy revision). Carried forward unchanged: geometry G-1…G-6 and the v002 material placeholders. Not modeled: parking islands/striping, curb-and-gutter profile, storm structures, site furnishings, bollards, light poles, street sidewalks, ramps, Building II site walls/stairs, planting.

## 6. Validation

| Check | Result |
| --- | --- |
| v002 vertex + material-slot hash before/after the site pass (2,023 mesh objects, inside the build) | identical (`72c7a831…ea777`) |
| Independent comparison `BI_facade_v002.blend` vs `BI_site_v003.blend` (`BI_compare_geometry_v002_v003.py`) | 2,023/2,023 mesh objects present, 0 vertex changes, 0 material changes, 0 collection changes; 22 objects added, all `SITE_`/`CTX_` inside `08_Site_v003` except the camera `BI_cam_site_elevated` in `90_Cameras`; only visibility change: `BI_grade_plane_660` hidden (superseded by terrain) |
| `05_Grid_control` | render-hidden at collection level only; its 39 objects unchanged |
| `BI_freeze_BuildingI_v002_approved.json` (43 approved v001–v002 files) | PASS |
| `BI_freeze_project_and_BuildingII_v001.json` (311 pre-existing project + Building II files) | PASS |
| `BI_freeze_sources_BuildingI_longpath_v001.json` (all 1,231 Building I source files) | PASS |
| Renders inspected | six views; terrain and hardscape read correctly; small IDW bumps at curb spot pairs near the drop-off; parking lot shown as a plain rectangle |

## 7. Files created in this pass

```
models/Building_I/BI_site_v003.blend
notes/Building_I/BI_site_control_v003.md
notes/Building_I/BI_site_data_v003.json
notes/Building_I/BI_site_v003_build_report.json
notes/Building_I/BI_site_validation_v003.md
renders/Building_I/BI_site_v003_{front_north,rear_south,left_west,right_east,oblique_northwest,site_elevated}.png
scripts/Building_I/BI_build_site_v003.py
scripts/Building_I/BI_compare_geometry_v002_v003.py
```

## 8. Readiness

The site/grading baseline is ready for the owner's gate-4 decision as a **documented grading context**: every grade that is written on a civil sheet is applied exactly, every surface between spots is labelled interpolated, and every approximate surface carries `_APPROX` in its name. Its limitations are the approximate parking lot (no islands), the absence of curb-and-gutter profiles and storm structures, the PCO-only civil record, and the flat extrapolation beyond the spot cloud. Recommended next step after approval: freeze v003, then either obtain the V3 civil sheet set (CG/CS/CU/LP) from Edifice or FMK to replace the APPROX surfaces, or proceed to the next skill gate the owner names.

Next single decision for the owner: **approve or redirect the v003 site/grading baseline.**
