# Building I — geometry control document v001 (dimensional / geometry baseline)

Date: 2026-09-22
Applies to: `scripts\Building_I\BI_build_shell_v001.py` → `models\Building_I\BI_shell_v001.blend`, renders `renders\Building_I\BI_shell_v001_*.png`, data `notes\Building_I\BI_geometry_data_v001.json`.
Purpose: record, before geometry is built, where every major dimension comes from, what is measured, what is assumed and what is unresolved. **Geometry validation model only: exterior massing, floor levels, roof and parapet tops, major glazed openings as flush placeholders, entry canopy, rooftop mechanical screen, grid control. No finishes, no site, no interiors.** Neutral clay materials only.

Source-control rules applied: `BI_revision_review_v002.md` section 5 (owner decisions 1–8). Nothing in `source_documents` was modified. No Building II file was opened or modified; no Building II civil sheet was used in this pass (register stays empty, see §11).

---

## 1. Controlling files

| Role | File | Printed sheet / issue |
| --- | --- | --- |
| **Controlling architectural / structural set** | `source_documents\Building I\GC Closeouts\FMK Closeout\CD Record Set\250925_RFSMC_Combined permit set_rev14_RecordSet.pdf` | Rev 14 record set, cover 9/25/2025, FMK Architects project 2329. **Record drawing set, not a field-verified as-built** (decision 4). |
| Audit only | `source_documents\Building I\241115_RFSMC_Combined approved permit set_rev6.pdf` | Rev 6, 11/15/2024. Not used for geometry (decision 2). |
| Post-record change review | `source_documents\Building I\Contractors\Edifice\PCOs\` | See §10. |

Sheets read for this baseline (PDF page → printed sheet, printed sheet revision date):

| Page | Sheet | Title | Sheet date | Used for |
| --- | --- | --- | --- | --- |
| 8 | A0.01 | Architectural Site Plan | 3/28/2025 (rev 9) | FFE 661.75, plan north = true north (per north arrows) |
| 23 | A1.00a | Level 1 Edge of Slab Plan | 1/20/2025 (rev 7) | Level 1 slab-edge polygons (footprint) |
| 24 | A1.00b | Level 2 Edge of Slab Plan | 11/15/2024 (rev 6) | Level 2 slab-edge polygons (footprint of the E–F corridor band and the north projection) |
| 26 | A1.01 | Level 1 Building Plan | 9/25/2025 (rev 14) | Wall lines of the E–F.2 band and vestibule; grid registration; room identities |
| 27 | A1.02 | Level 2 Building Plan | 7/25/2025 (rev 13) | Grid line positions (vector), vestibule roof note |
| 28 | A1.03 | Roof Plan | 6/16/2025 (rev 12) | Rooftop mechanical screen 90'-0" × 40'-7", roof slope note, no-slope zone |
| 29 | A1.13 | Entry Canopy Plans & Details | 7/25/2025 (rev 13) | Canopy 78'-0" × 23'-5", 12'-0" bays, gutter at column line, 1 1/2" / 1'-0" glass slope, levels |
| 64 | A4.01 | Building Elevations (east, south) | 6/16/2025 (rev 12) | Datums T.O.S., LVL-02, Mezzanine, Gallery; overall lengths; raster skylines and glazing |
| 65 | A4.02 | Building Elevations (west, north) | 6/16/2025 (rev 12) | Same |
| 70 | A5.01 | Building Sections | 1/20/2025 (rev 7) | Sloped truss roof F→N, level datums |
| 72–86 | A5.12–A5.27 | Exterior wall sections / details | various | Parapet dimension tags (2'-0", 3'-0", 3'-3", 5'-2", 10'-0" "Metal Panel Parapet Wall") — used only as corroboration |
| 132 | S101 | Foundation Plan | 11/15/2024 (rev 6) | **Written grid dimension strings (X fully written, Y chain)** and exact vector grid lines |

All PDF pages are exact-scale vector exports (checked: 3/32" = 1'-0" sheets give 6.7500 ± 0.0004 pt/ft between grids 2 and 9 on A1.00a, A1.00b, A1.01, S101). **The four building elevations on A4.01/A4.02 are embedded shaded raster images**, only their datum lines, bubbles and text are vector. Values taken from them are therefore raster measurements (code R below).

## 2. Confidence codes

| Code | Meaning |
| --- | --- |
| **W** | Written dimension or datum printed on the controlling sheet. Governs. |
| **V** | Measured from exact-scale vector linework of the controlling sheet (grid lines, slab-edge clip polygons, wall lines), cross-checked against written dimensions; ±0.05 ft. |
| **R** | Measured from the shaded raster elevation at 144 dpi, referenced to the vector datum line LVL-01 and the vector grid bubbles; ±0.15 ft vertically, ±1 ft horizontally (bubble registration). |
| **I** | Interpretation of documented information (e.g. linear interpolation between two written datums). |
| **A** | Assumption, not documented on the sheets reviewed. Listed in §12. |

No dimension was taken from photographs, renderings or AI-generated images.

## 3. Units, coordinate origin, orientation

- Working unit: decimal feet. Blender scene is metric at true scale (1 ft = 0.3048 m), display Imperial.
- **Origin (0, 0, 0) = intersection of grid 1 and grid A at Level 01 finish floor.** FFE = 661.75 (A0.01, W).
- **+X = east** (grids 1 → 14), **+Y = north** (grids A → N), +Z up. Plan north = true north (A0.01 shows both arrows coincident).
- Front of building = **north** face (parking, Golf Links Dr beyond, entry canopy at the north-west). Rear = south (North Rea Park Ln). Building II is to the west.

## 4. Grid table

X positions (ft from grid 1). Source: S101 top/bottom strings (W): 12'-4", 17'-8", 15'-0", 15'-0", 12'-0", 18'-0", 30'-0" ×5, 28'-0", 2'-0", 10'-0". Grid 3.7 = grid 3 + 10'-0" (V, A1.13 bays). Vector grid lines on S101 reproduce every written value within 0.02 ft.

| Grid | X | Grid | X | Grid | X |
| --- | ---: | --- | ---: | --- | ---: |
| 1 (drawn "I") | 0.000 | 5 | 60.000 | 10 | 180.000 |
| 2 | 12.333 | 6 | 72.000 | 11 | 210.000 |
| 3 | 30.000 | 7 | 90.000 | 12 | 240.000 |
| 3.7 | 40.000 | 8 | 120.000 | 12.9 | 268.000 |
| 4 | 45.000 | 9 | 150.000 | 13 | 270.000 |
| | | | | 14 | 280.000 |

Y positions (ft from grid A). Source: S101 right-hand strings (W) A→B 4'-0", B→B.7 17'-8", B.7→C 8'-4", C→C.6 12'-0", C.6→C.9 8'-0", C.9→D 2'-4", D→E 9'-2", E→F 9'-1", G→H.1 18'-2" (via G.1→F.2 7'-6"), H.1→J 3'-4", J→K 17'-3", K→K.7 14'-6", K.7→L 4'-9", L→L.6 16'-0", L.6→M 14'-0", M→M.7 18'-7", M.7→N 11'-5". **F→G is not written on the sheets read: 9.945 ft (V, S101 vector lines).** Minor grids F.2, G.1, G.2, K.1 are V.

| Grid | Y | Grid | Y | Grid | Y |
| --- | ---: | --- | ---: | --- | ---: |
| A | 0.000 | F.2 | 74.540 (V) | K.7 | 133.778 |
| B | 4.000 | G | 80.530 (V) | L | 138.528 |
| B.7 | 21.667 | G.1 | 82.080 (V) | L.6 | 154.528 |
| C | 30.000 | G.2 | 83.580 (V) | M | 168.528 |
| C.6 | 42.000 | H.1 | 98.695 | M.7 | 187.111 |
| C.9 | 50.000 | J | 102.028 | N | 198.528 |
| D | 52.333 | K | 119.278 | | |
| E | 61.500 | K.1 | 124.780 (V) | | |
| F | 70.583 | | | | |

Cross-check: N is 198.51 ft north of A on the S101 vectors (chain gives 198.53). Structural sheet S101 labels the gym south wall grid "H" where the architectural sheets use "H.1"; the architectural label is used.

## 5. Floor, roof and parapet datum table (W unless noted)

| Datum | Printed | Decimal ft | Where printed |
| --- | --- | ---: | --- |
| LVL - 01 (finish floor, FFE 661.75) | 0" | 0.000 | all elevations/sections |
| Gallery | 11' - 0" | 11.000 | A4.01, A5.01, A1.13 |
| Mezzanine | 13' - 0 1/4" | 13.021 | same |
| LVL - 02 | 15' - 4" | 15.333 | same |
| T.O.S. @ Column 14 | 28' - 0" | 28.000 | A4.01 (east end block) |
| T.O.S. @ Column A | 30' - 0" | 30.000 | south wing roof structure at grid A |
| T.O.S. @ Column F | 31' - 6" | 31.500 | roof structure at grid F |
| T.O.S. @ Column N | 37' - 3 1/2" | 37.292 | roof structure at grid N |
| Footing level | -2' - 0" | -2.000 | A1.13, A5.12 (not modeled) |
| Average grade | 659.5 / 660 / 660.5 | -1.25 … -2.25 | A4.01/A4.02 fenestration calcs |
| Maximum building height | 41'-3" / 41'-9" / 42'-3" above avg. grade | **40.00** above FFE on all four elevations (I: 701.75 − 661.75) | fenestration calcs |

Roof planes (I, linear between written datums): south wing T.O.S. z = 30.0 + (y − 0)·(1.5 / 70.583); north block T.O.S. z = 31.5 + (y − 70.583)·(5.792 / 127.945) = 0.04527 ft/ft, i.e. the sloped truss roof of A5.01 rising from F to N. Roof plan note: "roof structure sloped to provide drainage toward plan south exterior facade" (W).

Parapet / top-of-wall values (R, raster elevations; corroborated by wall-section tags):

| Element | Top above FFE | Evidence |
| --- | ---: | --- |
| South wing basic roof-edge parapet (SW corner, west face y<2, south face x<30, east face y<8.6) | 33.3 | R (33.30–33.32 on south, west and east); wall sections A5.12 tag 3'-0"/3'-3" above T.O.S. |
| South wing PNL1 metal-panel parapet screen, south face x 30→40 | 40.0 | R; A5.24 "Metal Panel Parapet Wall" 10'-0" above T.O.S. A (= 40.0 W) |
| same, south face x 40→118 | 40.0 → 37.0 sloping | R (sawtooth-free linear fit) |
| same, south face x 118→134.5 | 37.1 / 39.1 | R |
| same, south face x 134.5→210 | 40.1 | R (mechanical screen behind may contribute) |
| same, south face x 210→270.4 | 38.9 → 40.0 | R |
| South wing east face screen (x = 271.38, y 8.6→60.5) | 40.08 | R |
| South wing west face screen (x = 6.88, y 2→61.12) and E–F.2 band west face | 40.0 | R (40.02–40.08) |
| E–F.2 band north face (y = 74.38, x 28.6→71) | 40.0 at x 30 → 36.0 at x 71 | R (north elevation, bubble registration ±3 ft) |
| 13–14 east end block (x 271.38→281, y 60.5→97.75) | 32.0 | R (south 32.04, north 32.08, east 32.08); T.O.S. col. 14 = 28.0 W |
| North block cornice (courts + training areas, x 71→287, y 70.58→202.9) | 33.15 + (y − 80.5)·0.0535 | R fit on east (33.13 @ G, 37.08 @ L.6) and west (33.36 @ G.2, 39.24 @ N−5) elevations, ≈ T.O.S. + 1.2 … 2.2 ft; north face 39.1–40.2 |
| Sports Science Lab projection north of N (x 148.4→241, y 198.5→202.9) | 40.15 | R (formula gives 39.7; 0.45 ft difference accepted for the baseline) |
| Rooftop mechanical screen | 40.1 | R (south elevation boxes above the parapet) |
| Entry vestibule 100 | 9.0 | R glazing head 8.52 on west and north elevations + 0.5 cap (A) |
| Entry canopy gutter / column top | 13.021 | W (Mezzanine datum on A1.13 section) |

## 6. Footprint controls

Footprint = union of the Level 1 slab-edge clip polygons (A1.00a) and the Level 2 slab-edge clip polygons (A1.00b), registered to grids 2/9 (X) and N (Y), traced at 0.125 ft raster resolution and simplified with 0.25 ft tolerance → 65 vertices (V). Slab edge = outside face of wall assembly per note 2 on A1.01 ("all exterior dimensions are to outside face of wall assembly"); brick-ledge overhangs, if any, are not modeled. Stored verbatim in `BI_geometry_data_v001.json` → `footprint_union`.

Key faces (V):

| Face | Coordinate | Extent |
| --- | --- | --- |
| South wing south face | y = −4.38 (x 6.88→48.5 and 118.3→271.4), y = −1.72 (x 48.5→91.7? see polygon), jogs of 2.7 ft | overall X 6.88 → 271.38 |
| South wing west face | x = 6.88 | y −4.38 → 61.12 |
| South wing north face (west of the band) | y = 61.12 | x 6.88 → 28.62 |
| E–F.2 corridor band (Tele 145 / corridor 102 west part) | x 28.62 → 71.00, y 61.12 → 74.38 | A1.01 wall lines (V); unhatched on A1.00a so added explicitly |
| Entry vestibule 100 | x 38.25 → 62.25 (W: 1'-9" + 10'-3" + 10'-3" + 1'-9" from grid 3.7), y 74.54 (F.2) → 83.58 (G.2) | A1.13 A1 plan |
| Training block west face | x = 71.00 (y 74.4→169.6, jog to 72.88 for y 120.4→132.9) | |
| Courts west face | x = 91.00 with 0.9 ft pilasters | y 169.6 → 197.5 |
| North face | y = 197.5 (x 91→148.4 and 241→281), 198.5 (x 241→281), projection to 202.88 (x 148.4→241) | |
| East faces | x = 281.0 (y 60.6→97.75 and 160.4→198.5), x = 287.0 (gallery/stair strip, y 97.9→160.4), x = 271.38 (wing, y −4.38→60.5) | |
| Overall | X 6.88 → 287.00 = **280.12 ft**; Y −4.38 → 202.88 = **207.25 ft** | |

Written overall checks (A4.01/A4.02 fenestration calcs): south 264'-3 1/2" + 9'-11" = 273'-8 1/2"; north 210'-11 1/2" + 60'-0 1/2" = 271'-0"; east 167'-6" + 30'-7" = 198'-1". These are façade-segment totals, not bounding boxes; they are compared in the validation note.

## 7. Zones built (all prisms from z = 0)

| Zone | Plan region | Top |
| --- | --- | --- |
| Z1 South wing | footprint ∩ y ≤ 70.583, x ≤ 271.38 | 33.3 (R) + parapet screen strips per §5 |
| Z2 E–F.2 band | 28.62–71.00 × 61.12–74.38 | 40.0 → 36.0 west→east (R) |
| Z3 Vestibule 100 | 38.25–62.25 × 74.54–83.58 | 9.0 (R+A) |
| Z4 North block | footprint ∩ y ≥ 70.583 minus Z5 | 33.15 + (y − 80.5)·0.0535 (R) |
| Z5 13–14 end block | 271.38–281 × 60.5–97.75 | 32.0 (R) |
| Z6 Mechanical screen | 120–210 × 30.2–70.7 (A1.03 90'-0" × 40'-7" W; position V) | 31.0 → 40.1 (R) |
| Z7 Entry canopy | x −13.0 → 65.0 (78'-0" W, position V), gutter/column line y = 83.58 (G.2, V), north glass wing 16'-4 1/2" (W), south wing 6'-2 1/4" (W), slope 1 1/2" / 1'-0" (W), 7 columns at x = −10 + 12k (W bays), 8" columns (A1.13 plan detail) | gutter 13.021 (W); glass rises to 15.07 / 13.79 |
| Level 2 floor | Z1 region, 14.83 → 15.33 | LVL-02 15'-4" (W); extent is an approximation (I) |
| Grade plane | flat at −1.75 (avg grade 660, W) | validation reference only |
| Openings | 376 glazing boxes detected on the four shaded elevations (R): south 149, east 71, north 72, west 84 | flush placeholder panels on the face found by ray from that elevation's side |

## 8. Opening controls

Glazing lites were detected by colour on the shaded elevations (teal glass), u-registered to grid bubbles, z-registered to LVL-01. Grouped values: south wing punched windows z 3.3–10.7 (L1) and 17.1–24.6 (L2) in 2.2 ft lites; courts clerestory (north) z 30.24–34.97 in 6.2 ft lites; entry vestibule doors/glass z 0.3–8.5; east lounge/gallery glazing z 10.4–24.6. Storefront system dimensions on A7.21–A7.28 (W, e.g. 4'-0" modules, 8'-0" heads, 55'-4"/32'-0" curtain-wall widths) are not yet cross-referenced lite-by-lite: that belongs to the façade pass. Translucent wall panels (TWS1, grey) are not detected by the colour test and are not modeled.

## 9. Canopy controls (A1.13)

78'-0" long (3'-0" + 6 × 12'-0" + 3'-0"), 23'-5" wide (W); 1" laminated glass on exposed steel; gutter at the column line with 3" downspouts at every other column; glass slopes 1 1/2" / 1'-0" both ways from the gutter (W); column line on G.2 (V, enlarged plan); columns 12'-0" apart starting 3'-0" from the west edge, west edge 13.0 ft west of grid 1 (V). Levels on the section: LVL-02 15'-4" at the high edge, Mezzanine 13'-0 1/4" at the gutter, Gallery 11'-0" (W). The section shows the canopy meeting the building at grid H.1 while the plan shows the north edge at grid J: modeled to the written wing length 16'-4 1/2" from the gutter (reaches y 99.96, between H.1 and J). Column height to the gutter taken as 13.0 ft (I).

## 10. Post-record changes reviewed (decision 3: individual evaluation)

| Document | Content | Applied? |
| --- | --- | --- |
| CONT 8 Rooftop Mechanical Screen (11/17/2025) | Alucopanel FR ACM panels on steel framing "already in place by others"; no dimensions | **Not applied**: no geometry given; the screen extents come from A1.03 (Rev 14). Cladding only, façade pass. |
| PCO 50 Grade Issue at Canopy Footings (12/17/2025) | Storm drain rerouting, grading, paver base at the canopy | **Not applied**: site work, no canopy geometry change stated. |
| PCO 29 / 30 / 54 Lobby stair redesign, railing, Stonhard (11/2025–1/2026) | Interior stair | **Not applied**: interior, out of scope. |
| PCO 24 RFI 78/57 retaining wall, RFI 90 drainage | Site retaining wall/drainage | **Not applied**: site; file name contains characters Poppler cannot open, read via inventory only. Flagged for the site pass. |
| PCO 42/49/65 wall pads, sound panels, Acrovyn; PCO 51/64 J2 panels; PCO 47 turf; PCO 55 goal bracing; CONT 11 partitions; PCO 72/75/76/77 | Interior | **Not applied**: interior. |
| Signage packages (Southwood, Rec Plus) | Exterior signage | **Not applied**: owner decision pending. |

No post-Rev-14 document was found that changes the exterior shell or canopy geometry with a dimensioned final condition.

## 11. Register of Building II civil sheets used as shared-site references (required by v002 §5.1)

| Date | Sheet | File | Revision | Information taken |
| --- | --- | --- | --- | --- |
| — | none | — | — | No Building II document was opened in this pass. Site placement of Building I relative to Building II is deferred to the site gate. |

## 12. Assumptions (A) and interpretations (I)

- A-1 Vestibule 100 roof at 9.0 ft (raster glazing head 8.52 + 0.5). No section of the vestibule roof was found in the sheets read.
- A-2 Canopy column height 13.0 ft to the gutter beam; 8" square columns; gutter beam 1 ft deep.
- A-3 Level 2 floor slab modeled over the whole south-wing region; the true Level 2 slab extent (A1.00b) includes the courts balcony/mezzanine and excludes double-height areas — interior gate.
- A-4 Parapet screen strips 1.0 ft thick; the metal-panel wall build-up is a façade-gate item.
- A-5 Mechanical screen bottom at 31.0 (roof level in that zone), top 40.1 (R).
- I-1 Roof planes interpolated linearly between the written T.O.S. datums (A5.01 shows a single sloped truss F→N).
- I-2 North block cornice height as a linear fit to the raster (±0.3 ft).
- I-3 Maximum building height 40.0 above FFE derived from the fenestration-calc heights and the printed average grades.
- Openings placed as flush placeholder panels; no wall cut-outs (boolean) in this pass.

## 13. Unresolved conflicts / open items

- C-1 Grid F→G spacing not written on any sheet read (V 9.945 ft). Written string on S101 (7'-6") applies to G.1→F.2.
- C-2 Structural "H" vs architectural "H.1" label at the courts south wall.
- C-3 Canopy: section shows the building face at H.1, enlarged plan shows the north edge at J; wing length 16'-4 1/2" used.
- C-4 South-face parapet screen profile between grids 8 and 11 cannot be separated from the mechanical screen behind it on the south elevation raster (both ≈ 40 ft).
- C-5 The E–F.2 band top (36 → 40) and the training block north face (raster 33.9–35.4 at x 71–92) disagree with the north-block cornice formula (37.9 at y 169.6); the formula (consistent on east and west elevations) was kept for the block, the raster for the band.
- C-6 No Building I civil drawings in hand; grade shown as a flat plane at 660.
- C-7 County-stamped permit set not located (documented, not blocking).
- C-8 PCO 24 file could not be opened by Poppler (special characters in the name); content unknown beyond its title.

## 14. Photo discrepancies

None logged yet: no photograph was used in this pass (decision 5). Discrepancy checking against the dated photo folders is scheduled after the geometry baseline is approved.

## 15. Exact vs measured values (summary)

| Item | Exact (W) | Measured (V/R) | Δ |
| --- | ---: | ---: | ---: |
| Grid 1→14 | 280.000 | 280.02 (S101 vectors) | 0.02 |
| Grid A→N | 198.528 (chain incl. V for F→G) | 198.51 (S101 vectors) | 0.02 |
| Canopy length | 78.000 | 77.9 (A1.13 plan) | 0.1 |
| Mechanical screen | 90.000 × 40.583 | 90.0 × 40.5 (A1.03 vectors) | 0.1 |
| Vestibule width | 24.000 | 23.9 (A1.13) | 0.1 |
| Level 2 above LVL-01 | 15.333 | 15.33 (datum line spacing 138.0 pt at 9 pt/ft) | 0.00 |
| T.O.S. N above LVL-01 | 37.292 | 37.30 (datum line) | 0.01 |
| Max height | 40.00 (I) | 40.02–40.19 (R, four elevations) | ≤ 0.2 |

## 16. Planned outputs

- `models\Building_I\BI_shell_v001.blend`
- `renders\Building_I\BI_shell_v001_front_north.png`, `_rear_south.png`, `_left_west.png`, `_right_east.png`, `_oblique_northwest.png`
- `notes\Building_I\BI_shell_v001_build_report.json`
- `notes\Building_I\BI_geometry_validation_v001.md` (after the build)
