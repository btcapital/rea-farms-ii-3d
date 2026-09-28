# Building I — main entrance / porte-cochere site audit v010

Date: 2026-09-23
Baseline audited: `models\Building_I\BI_presentation_v009.blend` (site geometry = v003, unchanged through v009; building = v008 approved; materials = v009).
Frozen before any change: `manifests\BI_freeze_BuildingI_v009_pre_v010.json` (155 files: every v001–v009 note, data file, script, model and render; PASS). v008 and v009 are not overwritten; v010 is built on top of v009 so the v009 material and shader work is carried unchanged.
Status: **audit complete — the entrance drive, drop-off loop, median island and canopy plaza are fully documented on the civil sheets; the v003 site model has (a) an incorrect flood-filled asphalt polygon and (b) 42 storm-chart table values harvested as spot elevations, which together produce the undefined asphalt/terrain mass in front of the porte cochere. Building I v010 is created (§8).**

## 1. Sources reviewed (priority order)

| # | Source | File / page | Printed status | Used for |
| --- | --- | --- | --- | --- |
| 1 | **CS-101 Dimension Control Plan** (V3 Southeast 230959) | `Contractors\Edifice\PCOs\PCO 17 - RFI 58 - Site Furnishing.pdf` p.10 | rev 13 "SITE FURNISHINGS RFI" 07.22.25 | curb lines (vector), written widths and radii, walk/plaza hatches, bollards, loading zone |
| 2 | **CG-101 Grading & Drainage Plan** | PCO 24 (RFI 78) p.11; **PCO 50 (Blythe COR 29 "Revised Canopy Grades" 10/15/2025) p.4 (1"=20') and p.5 EXHIBIT 1 (1"=10')** | 07.29.25 / 10.10.25 | TOC/BOC/HP spot elevations at the loop, canopy plaza grades, storm structures and drainage direction |
| 3 | LP-100 / LP-101 Landscape Plans | PCO 24 p.12–13 | rev 13 07.22.25 | island planting (oval planted, nose unplanted), bed lines along the walks |
| 4 | PCO / bulletin civil | same bulletins (no other civil bulletin touches the entrance) | — | — |
| 5 | Survey / closeout | topographic survey 3513 (pre-construction), Blythe storm as-built plats (closeout p.4599–4600) | 2024 / 2026 | reviewed; no legible geometry — not used |
| 6 | Building II shared-site civil (CS-101 rev 6, 03.10.26) | `Building II\00 PLANS\Revision 5\Rea Farms 2 - Civil Drawings 03.17.26.pdf` p.7 | register entry S-11 | the shared plaza west of the wing only; the loop is entirely on the Building I sheet — not needed |
| 7 | A0.01 Architectural Site Plan (Rev 14 p.8), A1.13 Entry Canopy Plans (p.29) | Rev 14 record set | 3/28/2025 / 7/25/2025 | secondary check of the loop/island/plaza layout; canopy extent (unchanged) |
| 8 | Photographs 2026-07-28 drone a/b, 2026-08-10 overview | genuine | — | validation only: loop, planted oval island, paved nose, canopy over the drop-off lane |

No AI-generated or retouched image was used (list in `BI_revision_review_v002.md` §5).

## 2. Registration

CS-101, CG-101 and the PCO 50 CG-101 share one drawing base (1" = 20', 3.6 pt/ft): `x_BI = 141.0 + (X − 1859.0)/3.6`, `y_BI = 173.53 − (Y − 1211.1)/3.6` (v003 fit on the three 94-ft court sidelines drawn on A1.01 and CG-101; building faces within 0.3 ft). Check on this pass: the vestibule outline on CS-101 lands at x 39–62, y 74–85 (model 38.25–62.25 × 74.54–83.58) and the north-block west face at x 71 — within 0.4 ft.

## 3. Documented entrance configuration (CS-101, vector curb lines + written dimensions)

Curb linework is drawn as two parallel 6-pt lines 1.5 ft apart (face of curb on the pavement side, back of curb on the walk side); the chained polylines (`scratchpad …/v10/cs101_chains.json`) give:

| Element | Documented geometry (Building I ft) | Written | Vector-measured | Conf. |
| --- | --- | --- | --- | --- |
| Drive aisle from the north parking lot | south face of curb y = 123.44 from x −95 to −60, then R9.50' into the diagonal | 25.00' / 24.50' aisle, R9.50' | y 123.44 (v003 had 126.6) | V |
| Diagonal approach | face of curb from (−46.3, 117.7) to (−18.2, 89.6) at 45°, R12.50' upper curve, R4.00' lower curve | R12.50', R4.00' | 39.8 ft long | V |
| **Drop-off lane at the porte cochere** | face of curb **y = 88.37** (back of curb 89.87) from x −15.3 to 26.7, with (6) bollards @ 6'-6" o.c.; lane **14.50'** wide to the median nose (y ≈ 102.9–105) | 14.50', 5.63' (walk between curb and canopy line on the civil base) | 88.37 / 89.87 | V / W |
| Entry drive (west of the island) | between the parking end-island curb (x ≈ −8.4) and the island outer curb (x 15.63): **24.00'** | 24.00' | 24.03 | W / V |
| Lane-to-return-lane curve | **R26.50'** face of curb from (26.7, 88.37) to (53.2, 114.87) | R26.50' | polyline of 16 chords | W / V |
| Return lane (east of the island) | pavement from the island outer curb (x 29.7) to the east face of curb **x = 53.2**, y 114.9–182.5; **12.50'** lane + **11.00'** strip | 12.50', 11.00' | 23.5 total | W / V |
| Loading zone / north end | face of curb x 53.2 to y 182.5, then the curve to (17.1, 207.0) into the courts-vestibule drive; loading-zone hatch 24' × 12' | 24.00', 7.00' | — | V |
| **Median island — planted oval** | outer curb x 15.63–29.70, y 112.37–168.0 (**55.6 ft long**), inner curb x 17.1–28.2 (**11.07 ft**, written **11.08'**), semicircular ends **R5.50'** | 11.08', R5.50' | 11.07 / 55.6 | W / V |
| **Median island — paved nose** (hatched, unplanted) | from the oval's west curb at (15.63, 155.95) a concave **R31.00'** edge (centre (−15.4, 156.0)) to (−4.52, 126.92), then the **R7.50'** nose (three drawn points, circumradius 7.51) round to (−1.88, 112.37), then the straight south edge y 112.37 back to the oval | R31.00', R7.50' | 7.51 / 31.0 | W / V |
| Parking end island (12.20') | rounded rectangle x −41.1…−6.4, y 146.9–162.1 | 12.20' | 34.7 × 15.2 outer | W / V |
| Canopy plaza (pavers) | from the back of curb (y 89.87) south to the vestibule (y 83.58 / 74.54), the lobby north face (74.38) and west to the entry plaza (y 74); east to the north-block west face (x 71) and north along the east walk to the loading zone (y 181); Techo-Bloc Westmount pavers, header Blu 60 Greyed Nickel (CS-101 notes) | 14.05', 7.00', 16.50', 11.00' | — | V / W product |
| Diagonal walk | **7.00'** paver band south-west of the diagonal back of curb | 7.00' | — | W / V |
| Aisle walk | **8.00' / 8.50'** concrete walk south of the aisle back of curb (y 124.94 → 116.4), x −111.8 to the diagonal | 8.00', 8.50' | — | W / V |
| Pedestrian crossing | none drawn at the loop (the heavy dashed line along the lane and up the return lane is the fire/accessible route, not a curb) | — | — | — |
| Landscape beds | LP-101: 11 EMRA in the oval (v007 data, x 22.6, y 120–160), beds along the east walk (x 61–70) and the walk to the west plaza; the nose is unplanted | — | — | V (positions) |
| Connection to the parking lot | via the 25' aisle (x < −45) and via the 24' drive north of the island to the courts vestibule drive / loading zone | — | — | V |

## 4. Documented grades (CG-101 / PCO 50, written; positions ±0.3 ft)

| Location | TOC / BOC or spot | Reading |
| --- | --- | --- |
| Drop-off lane, west end of the curb (PCO 50 p.5) | TOC 660.11 / BOC 659.61 at (−17.8, 99.5) [leader to the curb] | lane gutter 659.6 at the west end |
| Drop-off lane, canopy (PCO 24 p.11) | TOC 660.32 / BOC 659.82 at (−0.5, 96.8/94.1) | gutter 659.8 at the canopy west columns |
| Median nose | TOC 661.36 / BOC 660.86 at (9.3, 125.2 / 122.6) | gutter 660.86 at the nose |
| Return lane, island east side | TOC 661.14 / BOC 660.64 at (41.5, 126.9 / 124.2); **HP 660.93 at (39.7, 141.8)** | lane crown/high point in the return lane |
| Island north end | TOC 660.74 / BOC 660.24 at (9.3, 166.8 / 164.1); TOC 661.12 / BOC 660.62 at (41.4, 170.2 / 167.5) | |
| Entry drive north | TOC 660.50 / BOC 660.00 at (10.4, 176.3 / 173.6); TOC 661.72 / BOC 661.22 at (31.5, 178.5 / 175.8) | |
| Parking end island | TOC 659.74 / BOC 659.24 at (−1.7, 143.2 / 140.5); TOC 659.07 / BOC 658.57 at (−19.0, 143.1 / 140.4); TOC 660.24 / BOC 659.74 at (6.2, 150.6 / 147.8) | |
| Diagonal curb | TOC 659.48 / BOC 658.98 at (−33.9, 125.0 / 122.3) | |
| Canopy plaza pavers | 661.47 (20.1 / 21.9, 91.6), 661.57 (30.2 / 32.0, 96.0), 661.69 (PCO 50 p.5), FFE 661.75 at the doors, 661.36 at (40.4, 107.7), 661.42 at (44.9, 117.7) | plaza 661.4–661.7 falling west to 660.67 / 660.83 at x ≈ −13/−7 |
| West walk | 660.30 / 660.39 / 660.48 / 660.64, 659.72 / 659.79 (drive) | |
| Storm | area drains AD-105CM (rim 660.12) and AD-204 (659.50) at the west end of the canopy walk; the canopy roof drains by 4"/6"/8" HDPE to WYE-105CH (PCO 50 "±96 LF of 8" HDPE for canopy drainage") | drainage direction: lane gutter falls **west** from the nose (660.86) to the canopy west end (659.6–659.8), about 1.1 % over 100 ft; return lane crowns at HP 660.93 and falls north to 660.00–660.24 |
| Curb height | TOC − BOC = 0.50 ft everywhere (6" curb) | |
| Pavement slopes | lane 1.0–1.3 % longitudinal (from the spots), plaza ≈ 0.6 % toward the curb; no cross-slope written | derived from the spots (I) |

## 5. Current v009 geometry at the entrance and why it does not match

| Item | Current (v003 site, unchanged to v009) | Finding |
| --- | --- | --- |
| `SITE_asphalt_west_drive_dropoff` | one 380-vertex polygon flood-filled from the CS-101 heavy linework, x −143…22, y 90.4…310 | **Incorrect**: the fill stopped at the curb lines it happened to hit — it ends at x = 22 (east half of the loop, the return lane, the loading-zone drive missing), runs south to y 90.4 (covers the plaza in front of the canopy up to 2 ft from the vestibule instead of stopping at the curb face 88.37 … it actually crosses it), zig-zags around the island area (the oval was partly filled, partly not) and follows leader lines and hatch (137 jagged vertices between y 85 and 175). Its edge does not coincide with any documented curb east of x −45. |
| Median island (oval + nose) | **missing** | the 11 EMRA shrubs of the island sit on asphalt/terrain |
| Drop-off lane, return lane, loading-zone drive | **missing** east of x 22 | lawn terrain there |
| Canopy plaza / walk in front of the vestibule (y 74–90) | **missing** (the v003 `entry_plaza` polygon stops at y 74) | asphalt to y 90.4, then terrain to the vestibule |
| Diagonal walk, aisle walk, 12.20' end island | **missing** (v003 only built walks south/east of the building) | |
| `SITE_terrain_IDW_INTERPOLATED` | IDW (1/d³) through 421 "spots" | **42 of the spots are not grades**: the two STORM DRAINAGE CHART tables are printed over the entrance area of CG-101 (x −29…37 / 39…80, y 111…143) and their Rim/Invert columns (655.40–660.12) were harvested as bare `SPOT` values at (−16.1, 112–130), (−10…−9.6, 112–135), (5.4–6.8, 112–134), (53.7–60.4, 115–135), (75–77, 115–135). They pull the interpolated surface down 3–5 ft in a 40 × 25 ft pocket right in front of the porte cochere and at the return lane → the large irregular faceted mound/pit, the asphalt slab (which follows the same IDW) dipping with it, and the plants of the island standing 2–3 ft below the real grade (EMRA n11 base z −3.0). This is **incorrect terrain interpolation from misread text**, not a documented grade. |
| Overlap / z-fight | the asphalt (dz 0.1) and the terrain share the pocket; terrain faces were removed only under the wrong polygon, so lawn shows where the drive should be and asphalt where the plaza should be | missing curb containment: no curbs east of the fill |
| Canopy (`BI_canopy_*`, A1.13) | 78 × 23.4 ft, gutter on G.2, north edge y 99.96 | preserved; the civil base draws a shallower canopy (north edge ≈ 92) — the documented lane curb at 88.37 therefore lies **under** the canopy (a porte cochere: the canopy spans the lane); carried as item G-2 (canopy depth, plan J vs section H.1) — unchanged |
| Landscape | EMRA n11 (11 plants at x 22.6, y 120.1–160.1), SEAS annual disc (interpreted, centre (20.7, 132.5)), the plants along the east walk (DOUB, LAMB, SNOW, VANG, ILST, BLON at x 61–70) and the unresolved-symbol row at (−57…−37, 96–114) all have documented x,y that agree with the CS-101 beds; only their z is wrong (old terrain) | no plant needs to move in plan |

## 6. Missing / incorrect objects → v010 scope

Add: drive asphalt loop (corrected polygon), median oval planting bed, paved nose, 12.20' parking end island, canopy plaza pavers, diagonal 7-ft walk, aisle 8/8.5-ft walk. Correct: `SITE_asphalt_west_drive_dropoff` (replaced by the union of its correct western/northern part with the documented loop), the terrain in the window x −130…90, y 60…215 regenerated from the cleaned spot set. Re-seat (z only) the landscape objects that intersect the window. Nothing else.

## 7. Confidence and assumptions

- Curb lines V (±0.3 ft registration); widths and radii W where written (24.00', 14.50', 12.50', 11.08', R5.50', R7.50', R31.00', R26.50', R9.50', R4.00', R12.50', 12.20', 7.00', 8.00'/8.50') and reproduced within 0.05 ft by the vector measurement.
- Grades W at the spots; the pavement surface between spots is interpolated (I) with the v003 inverse-distance method on the cleaned set; asphalt uses gutter grades (TOC lowered 0.5 ft), curbs are implied by the raised walk/island slabs (+0.5 ft, v003 convention) — no curb-and-gutter profile modeled (A).
- The oval's planting surface is set at curb-top level (A; LP-101 note "mound 6 in" applies to the parking-lot islands, not stated for the median).
- Plaza materials per the CS-101 notes (Techo-Bloc Westmount Onyx placeholder colour, v003/v009); the nose is concrete (hatch); the aisle walk concrete (dotted hatch).
- The 1/3 of the loop north of y 162 (courts-vestibule drive, loading zone) is taken from the v003 polygon where it was correct and from the documented face of curb elsewhere.
- Unchanged and carried: canopy depth G-2, parking-lot outline SC-3, dumpster SC-1, landscape wall, all v008/v009 open items.

## 8. Decision

The entrance geometry is sufficiently documented (§3–4): Building I v010 is created, correcting only the entrance site area (`scripts\Building_I\BI_build_entrance_site_v010.py`, data `BI_entrance_site_data_v010.json`, validation `BI_entrance_site_validation_v010.md`).

## 9. Addendum — findings from the v010 trial builds (before the final build)

| Finding | Evidence | Action |
| --- | --- | --- |
| A second class of false spot elevations | the first trial render showed a 4-ft cone in the paved nose; the "TOC 656.00" spot at (6.44, 125.92) is the roof-drain pipe label **656.00 (WYE-100)** printed on the PCO 50 CG-101 bulletin next to the real TOC 661.36 / BOC 660.86 pair. Every harvested value immediately followed by a "(STRUCTURE)" word is a pipe invert / connection elevation (656.00 (BEND-105CL), 656.00 (AD-105CM), 655.70 (WYE-62) …). | 3 such values were inside the kept set → dropped (`spots_dropped_pipe_inverts`); the other 39 had already been removed with the chart rectangles. Leave-one-out check of the remaining 376 spots: no residual outlier inside the entrance window (the 11 remaining >1.2 ft deviations are all at x < −245 or y < 0 or retaining-wall TW values, outside the window). |
| Terrain rising through the pavement edges | the 4-ft terrain cells straddling a curb kept their lawn height inside the pavement (v003 method) | the window terrain is now cut exactly at the face of curb / slab outlines with the exact boolean (§ data JSON `objects.SITE_terrain_IDW_INTERPOLATED`); the terrain grade field is the curb-top field T, the pavement the gutter field G = T − 0.50 (CG-101: TOC − BOC = 0.50 at every pair) |
| Curb | §7 assumed "curbs implied by the raised slabs" | CS-101 draws the curb as two lines 1.5 ft apart; a concrete curb ring (`SITE_curb_entrance_drive_CS101`, top = TOC, 1.5 ft wide) is modeled along the whole drive polygon inside the window. Island / plaza / walk slabs keep their +0.50 ft edges as their curbs. |
| Plaza extent | the first trial ran the pavers from the east walk to the north-block face (x 60.5–71) up to y 181, over the LP-101 bed rows DOUB / LAMB / SNOW / VANG / ILST / BLON | the plaza polygon now stops at the 8.5-ft east walk (x 51.7–60.5); the bed x 60.5–71 starts at y 100 (LP-101 positions), so those plants are seated on the terrain, not skipped as "on hardscape" |
| Regrade window | §6: x −130…90, y 60…215 | final: x −130…110 (the east edge lies inside the building for y 74–203 so the second storm chart leaves no step at the window edge), y 60…210 (the two LP-100 parking-lot islands at y 213–228 are untouched) |
| Long thin fan triangles | the ear-clip triangulation of the 248-vertex drive polygon produced dark shading streaks across the asphalt | all new slabs are regular grids clipped to their outline (exact boolean), then lifted onto the grade field |
