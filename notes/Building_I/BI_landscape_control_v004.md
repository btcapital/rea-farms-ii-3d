# Building I — landscape / immediate-context control document v004

Date: 2026-09-22
Applies to: `scripts\Building_I\BI_build_landscape_v004.py` + `notes\Building_I\BI_landscape_data_v004.json` → `models\Building_I\BI_landscape_v004.blend`, renders `renders\Building_I\BI_landscape_v004_*.png`.
Base: **BI_site_v003 (owner-approved site/grading baseline) on BI_facade_v002 / BI_shell_v001, all unchanged**; frozen in `manifests\BI_freeze_BuildingI_v003_approved.json` (56 files). v004 adds vegetation and immediate context only, in collection `09_Landscape_v004`; every object is prefixed `LS_` (documented planting) or `CTX_` (existing street trees).
Scope: landscape + immediate-context baseline (skill gate 4, second pass). No signage, vehicles, people, lighting fixtures or presentation effects. Nothing beyond this gate.

## 1. Carried-forward items (not resolved here)

Geometry G-1…G-6, the v002 material placeholders, and the v003 site items SC-1…SC-5 (dumpster brick; simplified north parking-lot rectangle without islands — islands are now added as **landscape** objects on top of it, the asphalt rectangle itself is untouched; landscape-wall height query; no sealed Building I civil set; contours not modeled) remain open exactly as recorded in the earlier control documents.

## 2. Sources

| # | Source | Building | File / page | Printed status | Used for |
| --- | --- | --- | --- | --- | --- |
| L-1 | **LP-101 Landscape Plan – Building** (V3 Southeast project 230959, 1" = 20') | Building I landscape plan (bound only inside PCO 24) | `Contractors\Edifice\PCOs\OCO #6\PCO 24 - RFI 78 …(FMK Reviewed).pdf` p.13 | date 03.01.24; revisions 8 11.11.24 RTAP → 13 07.22.25 "Site Furnishings RFI"; stamped "RFI 78 – Bulletin Drawing" | **controlling** for foundation beds, plaza and entry planting: plant schedule "Main Building Landscape" (2 tree, 14 shrub, 12 ground-cover species), 61 quantity callouts, plant symbols, lighting schedule (20 Van Gogh path lights) |
| L-2 | **LP-100 Overall Landscape Plan** (1" = 30') | Building I (inside PCO 24) | same file p.12 | rev 13 07.22.25 | **controlling** for the north parking lot and perimeter beds: schedule "Parking Lot" (WILO 22, LACE 10, ABFR 114, ABKA 7, BLON 22, EMRA 37, LOJA 95, VIBL 96, SEAS 170, OSOR 42), 36 callouts, 17 island ovals, "13 existing trees along Golf Links Dr to remain", "7 existing trees along Midway Park Dr to remain", SOD labels, planting notes (mulch 1.5–2" double-hammered hardwood, islands mounded 6" above back of curb) |
| L-3 | Rev 14 cover sheet index | Building I | Rev 14 record set p.1 | 9/25/2025 | lists C-LP-100 / C-LP-101 as part of the permit set; **the sheets are not bound in either combined set** — only the PCO 24 bulletin copies exist in the folder |
| L-4 | PCO 34 Landscape Lighting per Rev 13 R1 | Building I | `PCOs\OCO #9\PCO 34 …_signed.pdf` (2 p.) | 10/28/2025, signed 11/3/2025 | $9,500 allowance, 20 bronze Pro Trade path lights (UG Landscape) — lighting not modeled |
| L-5 | CS-101 Dimension Control (RFI 58) | Building I (PCO 17 p.10) | see v003 S-3 | rev 13 07.22.25 | curb/walk geometry already in v003; bike lockers/racks (RFI 78 p.5) not modeled |
| L-6 | A0.04 dumpster, CX-104 landscape wall | Building I | see v003 | — | unchanged from v003 |
| **L-7** | **LP-100 Overall Landscape Plan rev 2 (Carolina Sports MOB)** | **Building II — shared-site register entry** | `source_documents\Building II\00 PLANS\Approved Civil\APPROVED-LDCP-2025-00715.pdf` p.12 (final approval 1/9/2026) | rev 2 12.12.25 "2nd city comments" | shared parking lot and street frontage only: compared with L-2 (see LC-2); note "REFER TO LDCP-2025-00064 FOR BUILDING 1 LANDSCAPING"; existing-tree counts on Golf Links Dr and Midway Park Dr; NOT used for any Building I planting position |
| **L-8** | **LP-101 Landscape Plan – Building (Bldg II)** | **Building II — shared-site register entry** | same file p.13 | rev 1 11.06.25 | reviewed for the plaza strip between the buildings; Building II beds are Building II scope and were not modeled |
| L-9 | Rea Farms 2 civil set 03.17.26 p.5 (cover, sheet index) | Building II — register (already S-11/S-12 file) | `…Revision 5\Rea Farms 2 - Civil Drawings 03.17.26.pdf` | rev 6 03.10.26 | confirms LP-100 rev 2 / LP-101 rev 1 are the latest Building II landscape issues; no landscape sheet bound in that set |
| L-10 | APPROVED Bulletin Rea Farms Infrastructure Extension 2026-5-14 | Building II folder — shared streets | `Building II\00 PLANS\APPROVED Bulletin_…2026-5-14.pdf` (6 p., C-2.x/C-4.0/C-5.x grading) | 5/14/2026 | checked for the N Rea Park Ln / N Old Springs Rd street-tree plan: **grading sheets only, no planting plan bound** |
| P-1 | Drone photos 2026-07-28 (`dji_fly_20260728_113708_0045`, `…114046_0053`) and 2026-08-10 `Rea Farms Area Photo Overview .JPG` | genuine photographs | — | — | validation only (§8) |

Not found for Building I: LDCP-2025-00064 (Building I land development approval), the Rea Farms Major Infrastructure Plans Phase 2 (street trees on N Rea Park Ln / N Old Springs Rd are "per city project", not drawn on LP-100), an irrigation plan (design-build per note 11), planting details sheet CX-102 (referenced, inside PCO 24 p.10 only as drainage details).

## 3. Registration of the landscape sheets

Both sheets share the V3 civil base of CS-101/CG-101. Offsets were found by correlating their curb/edge lines with the CS-101 lines registered in v003 (court-sideline fit):

- LP-101 (3.6 pt/ft): `x = −87.6 + X/3.6`, `y = 504.8 − Y/3.6` — 137 of 235 candidate lines match within 0.4 ft.
- LP-100 (2.4 pt/ft): `x = −395.2 + X/2.4`, `y = 699.3 − Y/2.4` — 156 of 306 lines match.
- Cross-check: the parking-island centres read from LP-100 (92.0, 263.7), (153.1, 263.7), (214.0, 263.7) coincide with the island-tree symbols on LP-101 at (91.9, 265.1), (152.9, 265.2), (214.0, 265.2): agreement 1.5 ft between two independently registered sheets. Expected positional accuracy of plant symbols: **±1.5 ft** (V).

## 4. Plant schedules (written, W)

LP-101 "Plant Schedule Main Building Landscape" and LP-100 "Plant Schedule Parking Lot" are transcribed in full in `BI_landscape_data_v004.json → schedule` (code, botanical/common name, quantity, container size, caliper/height minimum, spacing, canopy). Summary:

| Sheet | Trees | Shrubs | Ground covers / annuals | Total |
| --- | --- | --- | --- | --- |
| LP-101 | BUTT 2 (Ginkgo 'Jade Butterfly' 1.5" B&B), STAR 2 (Star Magnolia 1.5" B&B) | ABKA 46, DAZA 12, BLON 28, GATE 19, CASL 4, COFA 10, JEWL 88, JADE 18, FOAR 8, DOUB 16, ILST 4, LOPE 13, BUNN 42, RHCO 7 = 315 | CARZ 108, CARE 109, COZA 28, SNOW 9, CORA 47, JUNE 17, MUHL 37, CATM 61, OSOR 61, RUSS 9, LAMB 29, VANG 25 = 540 | 859 |
| LP-100 | WILO 22 (Hightower Willow Oak 2.5" B&B, 30' canopy), LACE 10 (Allee Lacebark Elm 2.5" B&B, 35') | ABFR 114, ABKA 7, BLON 22, EMRA 37, LOJA 95, VIBL 96 = 371 | SEAS 170 (annuals), OSOR 42 | 615 |

Callout sums equal the schedule quantities where checked (JEWL 13+16+26+33 = 88; CORA 6+6+5+11+19 = 47; CATM 13+48 = 61; GATE 3+3+13 = 19; ABFR 7+9+13+14+14+21+36 = 114).

## 5. Placement method and what is exact vs interpreted

1. **Symbol positions (V):** every drawn plant symbol carries a centre mark made of tiny (< 2.5 pt) strokes; clustering those marks gives 393 symbols within the LP-101 viewport and 687 on LP-100 — the LP-100 count equals the two schedules' 686 individually-drawn plants (ground covers are hatched, not symbolised). Symbols are exact to the drawing (±1.5 ft registration).
2. **Species (V / V-I / I):** each "(n) CODE" callout was linked to its leader line (12-pt black, 18-pt landing then a diagonal) and the nearest free symbol of the matching kind at the leader tip seeded a nearest-neighbour growth of n symbols (link ≤ 9.5 ft). Result codes: **V** = full group found at the leader (383 plants); **V-I** = symbols exact but the group is short of n (143); **I** = second pass with a wider link (41). Plants: **567 placed** (35 trees, 393 shrubs, 139 individually-drawn ground-cover plants).
3. **Species-unresolved symbols (U):** 121 documented symbols (92 on LP-100, 29 on LP-101) were not reached by a leader; they are modeled as neutral grey-green shrubs in `LS_shrub_UNRESOLVED_species_documented_symbol` at their drawn positions. They account for most of the shortfalls in ABFR (77/114), VIBL (36/96), JEWL (40/88), BUNN (3/42), BLON (3/28), DOUB (5/16), COFA (5/10), LACE (9/10) and all of EMRA (0/37, whose 20-pt circle symbol was not isolated).
4. **Hatched ground covers (I):** CARZ, CARE, COZA, MUHL, CATM, OSOR, SEAS and parts of CORA/VANG/LAMB/SNOW are hatched areas. Automatic hatch tracing was unreliable (patterns share strokes with adjacent beds), so each shortfall is represented by an **interpreted disc** of area = missing quantity × spacing², centred 0.6 radius beyond the leader tip along the leader direction. Discs whose centre falls on a v003 hardscape surface are not modeled and are listed in the build report. Bed outlines ("proposed mulch bed line") are **not** modeled; a mulch disc (r 1.6 ft) is placed under every documented plant instead.
5. **Parking islands (V):** 17 curb ovals 37 × 10 ft read from LP-100 at x ∈ {−204.5, −143.5, −82.5, 92.0, 153.1, 214.0}, y ∈ {152.7, 230.5, 263.7, 354.2}; modeled as 6-in raised mulch islands over the v003 asphalt rectangle (asphalt untouched). One WILO per island per the plan.
6. **Existing street trees (context, V position / I size):** 14 grey tree symbols along Golf Links Dr (y ≈ 421–443, labelled "13 existing trees … to remain") and 8 along Midway Park Dr (x ≈ 311, "7 existing … to remain"); modeled as `CTX_existing_street_tree_*`, 22 ft tall, 14 ft canopy (photo-based size).
7. **Lawn:** SOD labels on LP-100 cover all remaining pervious areas; the v003 terrain (lawn material) already represents them; no lawn object added.
8. **Sizes (I):** new trees 12 ft / 7 ft canopy / 3 in trunk (schedule: 8 ft, 2.5 in at planting 2025; 2026 photos show ≈12 ft); shrubs at the schedule minimum height with width = min(spacing, 1.3 × height); ground-cover plants 0.6–0.8 ft; simple spheres/ellipsoids on cylinders, no photorealism.

## 6. Conflicts

| # | Conflict | Handling |
| --- | --- | --- |
| **LC-1** | **Building outline on the civil/landscape sheets vs approved v001 footprint.** On CS-101, LP-100 and LP-101 the long south building line sits at y ≈ −1.2 ft and the east line at x ≈ 281 (y 60–200), whereas the approved v001 slab-edge polygon (A1.00a/b clip) has the south edge at −4.38 (x 6.9–48.5 and 118.3–271.4) and a 287.0 strip (y 97.9–160.4). Foundation plants drawn against the civil outline therefore fall up to 3.4 ft **inside** the approved shell. | Building NOT moved. 84 plants (ABKA 12, JADE 18, CORA 14, DAZA 8, FOAR 8, COFA 5, GATE 4, CATM 4, JUNE 4, RUSS 4, BUNN 3) were pushed outward across the nearest footprint edge to 1.2 ft (trees 3 ft) clearance, max shift 9.9 ft at the wing/vestibule re-entrant corner; each shift is listed in the build report. **Owner/architect question:** is the A1.00 slab edge at −4.38 a slab projection beyond the wall face at −1.17 (grid A minus 1'-2")? If so, v001 geometry G-item to be opened. |
| LC-2 | Shared parking-lot schedule: Building I LP-100 rev 13 (07.22.25) shows WILO 22 / LACE 10 / ABFR 114 / LOJA 95 / VIBL 96; Building II LP-100 rev 2 (12.12.25, approved 1/9/2026) shows WILO 23 / LACE 9 / ABFR 78 / LOJA 75 / VIBL 85 with "2 relocated proposed street trees" and revised lot layout. | Building I sheet used (source priority 1–2); Building II sheet logged as shared-site context only; the difference is unresolved (the later Building II revision may reflect what was built in the lot). |
| LC-3 | LP-100/LP-101 quantities vs callouts resolved: EMRA 0/37 placed, VIBL 36/96, ABFR 77/114, JEWL 40/88, BUNN 3/42, BLON 3/28, DOUB 5/16 — symbols exist (121 unresolved) but their species could not be tied to leaders automatically. | Modeled at documented positions as species-unresolved shrubs (U); no plants invented. |
| LC-4 | Street trees on N Rea Park Ln and N Old Springs Rd are visible in the 2026 photos but are "per Rea Farms Major Infrastructure Plans – Phase 2 (city project)", not drawn on any sheet in the folder. | Not modeled (photos are validation only). Gap recorded. |
| LC-5 | Ground-cover bed extents (hatches) not extractable. | Interpreted discs (§5.4), clearly named `_INTERPRETED`; discs on hardscape omitted. |
| LC-6 | LP-101 is a bulletin copy (RFI 78, 07.29.25) and LP-100 rev 13 predates the Blythe canopy-grade change (PCO 50, 10/2025) and PCO 34 lighting (11/2025); no landscape as-built or closeout planting record was found. | Documented; treat plantings as design intent (Rev 13), photo-validated in July–August 2026. |
| LC-7 | Plaza strip between the buildings: LP-101 shows only Building I-side beds; Building II LP-101 rev 1 shows its own beds (not modeled). | Strip remains the v003 APPROX plaza surface. |

## 7. Assumptions

A-L1 plant sizes (§5.8); A-L2 mulch discs instead of bed polygons; A-L3 island height 0.5 ft over asphalt (planting note 8: mound 6" above back of curb); A-L4 existing street-tree size; A-L5 leader-disc placement for hatched ground covers; A-L6 push-out of plants inside the approved footprint (LC-1); A-L7 unresolved-species symbols rendered as 1.5-ft grey-green shrubs.

## 8. Photo validation notes

- 2026-07-28 photo 0045 (north lot looking south-east): parking islands are planted with single young trees and lawn/mulch; the drop-off loop island carries shrubs and small trees; foundation beds along the north face are mulched with shrubs; street trees along Golf Links Dr are present. Consistent with LP-100.
- 2026-07-28 photo 0053 (south front): continuous mulched foundation beds with low shrubs and grasses along the south face, lawn strip, sidewalk, and a row of street trees in the N Rea Park Ln verge (LC-4). Consistent with LP-101 bed layout; tree row not on any sheet.
- 2026-08-10 overview: parking islands with trees, Midway Park Dr street trees, plaza between the buildings still under construction (Building II site). No dimension was taken from photographs.

## 9. Planned outputs and validation

`models\Building_I\BI_landscape_v004.blend`; renders `BI_landscape_v004_front_north.png`, `_rear_south.png`, `_left_west.png` (Building II context mass hidden), `_right_east.png`, `_oblique_northwest.png`, `_site_elevated.png`, `_landscape_entry.png` (new camera `BI_cam_landscape_entry` at (−48, 205, 26) ft looking at the entry beds); `BI_landscape_v004_build_report.json`; `BI_landscape_validation_v004.md`. Validation: v003 vertex + material hash inside the build; independent `BI_compare_geometry_v003_v004.py`; manifests `BI_freeze_BuildingI_v003_approved.json` (56), `BI_freeze_project_and_BuildingII_v001.json` (311), `BI_freeze_sources_BuildingI_longpath_v001.json` (1,231).
