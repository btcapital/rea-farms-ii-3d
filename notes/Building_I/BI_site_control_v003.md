# Building I — site / grading control document v003

Date: 2026-09-22
Applies to: `scripts\Building_I\BI_build_site_v003.py` + `notes\Building_I\BI_site_data_v003.json` → `models\Building_I\BI_site_v003.blend`, renders `renders\Building_I\BI_site_v003_*.png`.
Base: **BI_facade_v002 (owner-approved facade/material baseline) on BI_shell_v001 (owner-approved geometry baseline). Both unchanged**; frozen in `manifests\BI_freeze_BuildingI_v002_approved.json` (43 files). v003 adds site/grading only, in collection `08_Site_v003`, every object prefixed `SITE_` or `CTX_`.
Scope: site/grading baseline (skill gate 4). No landscaping, vehicles, people, signage or presentation effects. Nothing beyond this gate.

## 1. Carried-forward items (not resolved here)

Geometry G-1…G-6 (F→G spacing measured; canopy edge J vs H.1; vestibule roof 9'-0" assumed; 271'-0" north total unreconciled; south parapet/mechanical screen inseparable; raster heights lower confidence) and material items (PNL3, frame colour, canopy steel, vestibule enclosure, coping/soffit allocation, raster-derived facade extents ±1 ft) remain open exactly as in `BI_geometry_control_v001.md` §13 and `BI_material_control_v002.md` §7. No site document was allowed to move the approved shell.

## 2. Sources used

| # | Source | Building | File / page | Printed status | Used for |
| --- | --- | --- | --- | --- | --- |
| S-1 | **CG-101 Grading & Drainage Plan, RFI 78 bulletin drawing** (V3 Southeast, project 230959, scale 1" = 20') | Building I (post-Rev-14 civil bulletin, inside PCO 24) | `Contractors\Edifice\PCOs\OCO #6\PCO 24 - RFI 78 …(FMK Reviewed).pdf` p.11 (also p.4; p.15 = RFI 90 version) | date 03.01.24, revision 14 "RFI 78" 07.29.25 | spot elevations (TOC/BOC/SPOT/HP/LP), TW 661.00 landscape wall, FFE labels, storm structure rims |
| S-2 | **CG-101 with canopy grade revision** (Blythe COR 29 "Revised Canopy Grades" 10/15/2025) | Building I (inside PCO 50) | `Contractors\Edifice\PCOs\Rea_Farms_PCO_No_50_-_Grade_Issue_at_Canopy_.pdf` p.4 (1"=20') and p.5 (1"=10" canopy area) | latest grading in hand (12/17/2025 PCO) | **controlling spot elevations: 421 within the block window** (521 on the sheet) |
| S-3 | **CS-101 Dimension Control Plan, RFI 58 site-furnishings revision** (V3, 1"=20') | Building I (inside PCO 17) | `Contractors\Edifice\PCOs\PCO 17 - RFI 58 - Site Furnishing.pdf` p.10 (p.8 clean, p.7/p.9 = CS-100 1"=30') | revision 13 "SITE FURNISHINGS RFI" 07.22.25 | curb linework → walks/drive/plaza regions; dumpster, plaza, paver notes; setback/R/W labels |
| S-4 | CX-104 site details (brick landscape retaining wall detail 13, concrete stairs detail 14) | Building I (inside PCO 24) | PCO 24 p.5 / p.14 | 07.29.25 RFI 78 | wall build-up, riser/tread rule |
| S-5 | RFI 90 South Stair Entrance Drainage, bulletin AD-157 (1"=10') | Building I (inside PCO 24) | PCO 24 p.16 | 07.29.25 | trench/area drain rims at the rear entrance (661.20–661.59) — grades only |
| S-6 | A0.01 Architectural Site Plan (Rev 14) | Building I | Rev 14 record set p.8 | 3/28/2025 (rev 9) | FFE 661.75, "Plaza" label, 30'-1" plaza dimension, 14' front setbacks, "Medical Office (Future Phase)" |
| S-7 | A0.04 Dumpster Enclosure Details (Rev 14) | Building I | Rev 14 p.11 | 6/16/2025 | enclosure 25'-8" × 10'-11 3/8", 6'-8" high, brick veneer on 8" CMU |
| S-8 | A4.01/A4.02 fenestration calcs | Building I | Rev 14 p.64–65 | 6/16/2025 | average grades 660.5 (E), 660 (S), 659.5 (W), 660 (N) |
| S-9 | Topographic survey 3513, Cloninger Bell, 1"=40' | Building I | `Survey\3513 1-11-2024 - Survey.pdf` | January 2, 2024 (pre-construction) | datum reference only (existing contours before grading); not used for geometry |
| S-10 | Blythe storm and water/sewer as-builts (Griffin Surveying preliminary plats) | Building I closeout | closeout binder p.4599–4600 | 2026 | reviewed; no legible elevations in the text layer — not used |
| **S-11** | **CS-101 Dimension Control Plan rev 6** | **Building II — shared-site register entry** | `source_documents\Building II\00 PLANS\Revision 5\Rea Farms 2 - Civil Drawings 03.17.26.pdf` p.7 | rev 6 03.10.26 "Wall Revisions" | Building II outline (context mass), Building II FFE 660.30, confirmation that the V3 sheet base is positioned identically to the Building I civil sheets |
| **S-12** | **CG-101 Grading & Drainage Plan rev 6** | **Building II — shared-site register entry** | same file p.3 | rev 6 03.10.26 | 39 spot elevations on the Building II side (TW/BW of Building II walls) — reviewed for the shared plaza; not used for Building I geometry |
| P-1 | Drone photo 2026-07-28 (`Pics\Drone Photos 7.28.26\dji_fly_20260728_113708_0045…JPEG`) and site overview 2026-08-10 (`Pics\Drone Photos and Videos 8.10.26\Rea Farms Area Photo Overview .JPG`) | genuine photographs | — | — | validation only: north parking lot with islands, entry drop-off loop and plaza pavers, Building II under construction west of the plaza, streets and sidewalks as drawn |

Not found for Building I: an official V3 civil set (CG/CS/CX/LP sheets) outside the PCO bulletins; grading east of Midway Park Dr; utility plans (CU-101) with rims/inverts in text form.

## 3. Registration of the civil sheets

All V3 sheets (S-1, S-2, S-3, S-11, S-12) are 1" = 20' (3.6 pt/ft), north up, and share one base drawing: their border, curb runs and R/W labels sit at identical PDF coordinates. Registration to Building I feet was fitted on the three 94-ft basketball-court sidelines that are drawn on both A1.01 (Rev 14) and CG-101:

`x = 141.00 + (X − 1859.0) / 3.6`, `y = 173.53 − (Y − 1211.1) / 3.6` (X, Y in PDF points).

Checks: court widths 50.0 ft on both; the FFE 661.75 door spots land on the approved south face within 0.2 ft; Building II outline on S-11 at x −249.3 → −44.5, y 0.6 → 105.3 versus the Building II model's 205'-0" × 105'-10" box transformed through the same relation (−249.0 → −44.0, 0.09 → 105.92): residual ≤ 0.6 ft. **No site document conflicts with the approved Building I placement.** Relationship of the two building coordinate systems: `x_BI = x_BII − 249.0`, `y_BI = y_BII + 0.09` (from the shared sheet base; ±0.6 ft).

## 4. Vertical datum and exact grades

| Item | Value | Code | Source |
| --- | --- | --- | --- |
| Building I FFE | **661.75** | W | S-1/S-2/S-6/S-11 |
| Building II FFE | 660.30 | W | S-11/S-12 |
| Average grade by elevation | E 660.5, S 660.0, W 659.5, N 660.0 | W | S-8 |
| Spot elevations | **421 written spots** (169 TOC, 170 BOC, 174 SPOT, 2 HP, 1 LP, 2 FFE, 2 RIM) in the block window x −320…340, y −60…340; range 653.74 – 662.49 | W (position V ±0.3 ft) | S-2 |
| Curb height | TOC − BOC = **0.50 ft** at 121 paired spots (6" curb) | W | S-2 |
| High points | HP 660.93 at (39.7, 141.8) — drop-off lane; HP 655.83 at (−263.3, 240.5) | W | S-2 |
| Low point | LP 659.72 at (12.4, 235.7) | W | S-2 |
| Grades at the south face | 659.36–659.51 at x 14–98 (y −7/−4), 660.45 at x 111, 661.71 at x 248 (door) | W | S-2 |
| Grades at the west wing face | 660.59 (y 3.6), 661.23 (17.5), 661.29 (28.8), 661.42 (42.8) at x ≈ 5 | W | S-2 |
| Entry drop-off | 661.36 / 660.86 TOC/BOC at (9.3, 125.3); 661.14 / 660.64 at (41.5, 126.9); pavers 661.47–661.57 at y 92–96 | W | S-2 |
| Storm rims | AD 656.49 at (53.7, 134.5); 657.25 at (−16.1, 133.8); RFI 90 rims 661.20–661.59 at the rear entrance | W | S-2, S-5 |
| Brick landscape retaining wall | **TW 661.00** (two labels, x 13.7 and 61.0, y ≈ −9.5); grade south of the wall 659.36–659.39; planting bed north 661.29 | W | S-1, S-4 |

Slopes (derived, I): parking lot falls from ≈ 661 at the building to ≈ 657 at the Golf Links Dr edge (~1.3 %); the south front falls west from 661.7 at the door (x 248) to 659.4 at x 14; west side falls from 661.4 at y 43 to 660.6 at y 4. No slope percentages are printed except "2 % max" notes at accessible spaces and pads.

Contours: CG-101 draws 1-ft contours but their labels are not tied to the linework in the text layer; the terrain is interpolated from the spots only (contours not modeled separately).

## 5. What is modeled (collection `08_Site_v003`)

| Object(s) | Geometry | Code |
| --- | --- | --- |
| `SITE_terrain_IDW_INTERPOLATED` | 4-ft grid over x −370…400, y −120…520; z = inverse-distance interpolation (weight 1/d³) through the 421 spots; the building footprint, corridor band, vestibule and every cell lying entirely under an asphalt surface are cut out (9,452 faces). **Entire surface is INTERPOLATED** except at the spots; outside the spot cloud (beyond the streets) it extrapolates flat; small bumps appear at TOC/BOC pairs (0.5 ft difference within ~1 ft). | INT |
| `SITE_asphalt_west_drive_dropoff` | drive loop from the drop-off lane north into the two nearest parking aisles, polygon flood-filled from the CS-101 curb lines. All asphalt slabs (and street bands) are subdivided to ≤ 6 ft so they follow the terrain and sit 0.10–0.13 ft above it (render offset only, staggered per slab; asphalt is documented AT grade) | M ±1 ft (partial: fill stopped at stall stripes) |
| `SITE_asphalt_parking_north_APPROX` | rectangle x −190…300, y 215…425 at terrain level; islands and stripes omitted | **A** ±5 ft |
| `SITE_walk_south_concrete`, `…walk_west_of_wing…`, `…walk_east…`, `…walk_east_end_block…`, `…walk_ne_courts…`, `…walk_north_courts…` | polygons flood-filled from the CS-101 curb lines and the approved footprint; top = terrain + 0.5 ft (6" curb) | M ±1 ft (partial coverage) |
| `SITE_entry_plaza_pavers_Westmount_Onyx` | region north of the wing / west of the vestibule; product per CS-101 note (Techo-Bloc Westmount, Onyx; header Blu 60 Greyed Nickel; pathways Linea Shale Gray) — colours not modeled | M |
| `SITE_plaza_between_buildings_APPROX` | strip x −44.5…−29 between the Building II east face and the west walk | **A** |
| `SITE_brick_landscape_retaining_wall_RFI78` | x 3.2 → 119.2, y −8.4 → −6.4 (2 ft incl. veneer), top **661.00**, bottom 658.5 (below grade) | W top / M extent ±2 ft / A bottom |
| `SITE_dumpster_enclosure_APPROX` | 25.7 × 12.7 ft box, 6.2 ft above local grade, at the CS-101 label (272–298, 368–381) | W size / M position ±3 ft / A orientation |
| `SITE_foundation_skirt_*` | approved footprint, band and vestibule extruded 4 ft below FFE so the interpolated terrain never shows inside the shell | A |
| `CTX_N_Rea_Park_Ln_88ft_ROW`, `CTX_Golf_Links_Dr_80ft_ROW`, `CTX_N_Old_Springs_Rd_61ft_ROW`, `CTX_Midway_Park_Dr_69ft_ROW` | flat asphalt bands at the right-of-way positions (R/W widths from CS-101 labels: 88', 80', 61', 69'; property lines 14 ft outside the printed setback lines) | I ±5 ft |
| `CTX_Building_II_mass_from_BII_CS-101_rev6` | plain box x −249.3…−44.5, y 0.6…105.3 (S-11, V), FFE 660.30 (W), 43.83 ft high (Building II model high parapet; context only) | shared-site register |
| `BI_grade_plane_660` (v002) | hidden, superseded by the terrain | — |
| `05_Grid_control` (v001 collection) | render-hidden at collection level only (the 39 grid-line objects are untouched): the lines sit just below the old flat 660 plane and would show through wherever grade < 659.75 | — |
| `BI_cam_site_elevated` | new camera in `90_Cameras` at (560, −390, 320) ft looking at (80, 160, 0), 28 mm | — |

Not modeled (documented but out of this pass or not extractable): parking islands and striping, curb-and-gutter profiles, storm structures, bollards, benches, bike lockers, light poles, street sidewalks, the Building II site walls/stairs (Building II scope), planting beds, the plaza "concrete band with stamped concrete" pattern, accessible ramps.

## 6. Conflicts

| # | Conflict | Handling |
| --- | --- | --- |
| SC-1 | A0.04 dumpster enclosure specifies Roman brick; PCO 14 changed the building brick to utility size | enclosure modeled as a plain masonry box; finish undecided |
| SC-2 | CS-101 note "Building II: future medical office building, future FFE 660.30" vs Building II built at FFE 660.30 (S-11) | consistent; no action |
| SC-3 | The parking lot could not be traced automatically (stall stripes and curbs share the same line weight); the north lot is an approximate rectangle | flagged A; islands to be added in a later pass or from the Building II CS-101 island geometry |
| SC-4 | The RFI 78 landscape wall label says "Utility brick this would be 28"" (wall height query) while the detail shows TW 661.00 over an 8" CMU wall; no BW written | wall bottom assumed 658.5 (below the 659.4 grade) |
| SC-5 | The Building I civil exists only as PCO bulletin sheets (RFI 58 / 78 / 90 and the Blythe canopy revision); no sealed record civil set | documented; these are the latest dated civil sheets in hand and post-date Rev 14 |

## 7. Assumptions

A-S1 6" curb at every walk/asphalt edge (from the TOC/BOC pairs); A-S2 walks planar on the interpolated terrain; A-S3 north parking lot rectangle; A-S4 plaza strip between the buildings; A-S5 foundation skirt 4 ft; A-S6 street bands flat; A-S7 dumpster orientation (long side east–west); A-S8 landscape wall bottom.

## 8. Photo discrepancies

None concluded. The 2026-07-28 and 2026-08-10 drone photographs show the north parking lot with landscaped islands, the drop-off loop with pavers, the plaza between the buildings and Building II under construction — consistent with the modeled surfaces; they were not used to change any dimension (decision 5). AI-generated images listed in `BI_revision_review_v002.md` §5 were excluded.

## 9. Planned outputs and validation

`models\Building_I\BI_site_v003.blend`; renders `BI_site_v003_front_north.png`, `_rear_south.png`, `_left_west.png` (Building II context mass render-hidden for this view only, because it stands between the camera and Building I), `_right_east.png`, `_oblique_northwest.png`, `_site_elevated.png`; `BI_site_v003_build_report.json`; `BI_site_validation_v003.md`. Validation: v002 vertex+material hash inside the build; independent v002→v003 object comparison; manifests `BI_freeze_BuildingI_v002_approved.json`, `BI_freeze_project_and_BuildingII_v001.json`, `BI_freeze_sources_BuildingI_longpath_v001.json`.
