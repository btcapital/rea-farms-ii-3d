# Comparison — building_shell_v012 → building_shell_v013 (small-scale site-detail pass)

Date: 2026-09-21
Basis: `notes/site_detail_control_v013.md` (written before the build; amended once during the pass — see "Process note").

## Validation

| Check | Result |
| --- | --- |
| Frozen v001–v012 files (130 files: models, scripts, all earlier notes, build reports, all 66 renders) | SHA-256 identical before and after: **0 changed** |
| `source_documents\Building I` | **Not opened, listed by name, read or used.** Only the aggregate was compared: 1,231 files / 6,929,037,544 bytes / newest modification time — identical to the figures recorded at the start of the pass |
| `source_documents\Building II` | 360 files; path, size and modification time of every file identical to the start-of-pass baseline: **0 differences**. Nothing else exists at the top level of `source_documents` |
| v012 objects | **1,286 of 1,286 identical** vertex for vertex (building, facade, site, terrain, landscape, vegetation, context — including the approximate Building I context mass); none changed, none removed |
| New objects | **61**, all named `DET_…`, all in the new collection `15_Site_Detail_v013` and nowhere else (list below) |
| Cameras, sun, sky, exposure | all seven cameras and all light / exposure settings identical to v012 |
| People, vehicles, signage, interiors, furniture | none added |

`build_shell_v013.py` = `build_shell_v012.py` + the site-detail block and one call to it.

## Objects added (61)

| Objects | Count | Basis |
| --- | --- | --- |
| `DET_Striping_stalls` | 1 (269 lines) | CS-101 rev 6 linework, positions and lengths measured; 4" white assumed |
| `DET_Striping_hatch` | 1 (66 lines) | CS-101 rev 6 hatching at the accessible aisles / no-parking areas; 4" white assumed |
| `DET_Curb_walk_west`, `DET_Curb_walk_east` | 2 | CS-101 curb-and-gutter note, CX-101 6" curb; only where the curb is not flush |
| `DET_Curb_island_site_1…3` | 3 | around the v006 islands; 6" high written, 6" wide assumed |
| `DET_Curb_island_ctx_…` | 18 | around the v011 context islands (±3 ft, as the islands themselves) |
| `DET_Bollard_steel_1…6` | 6 | CS-101 "(6) … @ 6'-6" o.c."; CX-101 detail 9: 3'-0" high, black; 6" diameter assumed |
| `DET_Bollard_light_1…4` + `…_lens` | 8 | CS-101 "(4) … Light Column Bollard Series 600 by Forms+Surfaces"; size assumed; finish is a neutral `UNRES_` placeholder |
| `DET_Light_pole_1…4` + `…_base` + `…_luminaire` | 12 | LP-101 symbols (positions measured); height, section, base and black color approximate from the 8.29.26 photo |
| `DET_Area_drain_AD-208, -209, -213, -214` | 4 | CG-101 rev 6 structure labels; position ±3 ft, 12" grate assumed |
| `DET_Door_pull_100A_1, _2` | 2 | A800 / A815 door 100A pair; pull shape and height assumed |
| `DET_Door_lever_110B, _102, _104` | 3 | A800 hardware sets; lever shape, side and height assumed |
| `DET_Joint_concrete_control_joints_APPROX_5ft` | 1 (20 lines) | spacing not written on the sheets reviewed — 5 ft assumed; name carries the flag |

Total new geometry: 1,594 faces.

## What remains approximate

Stripe width and color · curb width (gutter pan not modeled) · steel bollard diameter · everything about the light bollards except their position and count · light-pole height, section, base size and luminaire shape · area-drain positions (±3 ft) and grate size · all door-hardware shapes, heights and handing · concrete joint spacing · the 18 context island curbs (as approximate as the v011 context islands they follow).

Not added because not supported: paver joints (unit size and header-band location not dimensioned), painted wheelchair symbols, wheel stops, bike racks/lockers (furniture is excluded from this pass), stair handrails, other storm structures.

## Unresolved site-detail conflicts

1. **Bollards on the flush-curb band.** CS-101 places all ten bollards on the 1'-6" flush-curb strip, which v007–v012 model as part of the paver band. Bollards are placed on the existing surface; no v012 geometry changed.
2. **Light-pole symbols.** LP-101 shows four pole symbols along the walk edge with no schedule in the landscape sheet; their meaning is confirmed only by the 8.29.26 drone photo. One pole (x = 62.0) stands at the edge of a planting bed. The electrical site-lighting sheet was not used for positions in this pass.
3. **Island outline.** CS-101 draws the islands with rounded ends; v006–v012 model them with chamfered corners. The v013 curbs follow the frozen v012 outline, not the rounded one.
4. **Product data missing** for the Forms+Surfaces light bollard (size, finish) and the steel bollard diameter.
5. Carried from earlier phases: sun-shade drawings-vs-spec conflict, unresolved finishes, CATM / CORA / LACE shortfall, architectural revisions 6–10 not in hand.

## Render-time impact

| View | v012 | v013 |
| --- | --- | --- |
| hero_front_north | 21.6 s | 22.8 s |
| entrance_oblique_northeast | 34.9 s | 34.9 s |
| rear_oblique_southeast | 29.4 s | 29.3 s |
| elevated_site_oblique_northwest | 40.0 s | 41.1 s |
| facade_material_closeup | 73.8 s | 75.4 s |
| corner_northwest_eye_level | 29.1 s | 29.4 s |
| landscape_entrance_oblique | 50.2 s | 50.5 s |

Negligible: +0 to +1.6 s per view (256 samples, RTX A1000, OptiX). Model file 2.4 MB → 2.5 MB.

## Process note

Two things were corrected after the first full v013 build, which was my own unapproved draft and was deleted and rebuilt (no approved file involved): (a) 48 isolated diagonal lines that were drawing leaders, not pavement hatching, were filtered out (114 → 66 hatch lines); (b) a check against the CS-101 sheet image showed the first extraction had missed the three double stall rows directly north of the Building II islands, because each pair of stalls is drawn there as one 37 ft line — 21 such lines and 8 row centre lines were added (240 → 269 stall lines). The control document was amended accordingly.

## Renders (`renders/`)

`building_shell_v013_hero_front_north.png` · `…_entrance_oblique_northeast.png` · `…_rear_oblique_southeast.png` · `…_elevated_site_oblique_northwest.png` · `…_facade_material_closeup.png` · `…_corner_northwest_eye_level.png` · `…_landscape_entrance_oblique.png`
