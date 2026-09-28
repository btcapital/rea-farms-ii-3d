# Tenant test-fit control document v015 — Concept_A_CNSA_ASC

Date: 2026-09-21
Applies to: `scripts/build_shell_v015.py` → `models/building_shell_v015.blend`
Baseline: **v014, frozen.** Every v001–v014 object is rebuilt by the identical code and is not edited. v015 only **adds** tenant objects (named `TEN_A_…`) inside `Building_II > TENANT_CONCEPTS > Concept_A_CNSA_ASC`. Written before any tenant geometry was built.

This is the first real prospective-tenant plan. **It is modeled as drawn, not redesigned.** Building I was not touched; `source_documents` was not modified.

Codes: **W** written on the tenant plan · **M** measured from the tenant plan's exact vector linework after registration · **A** assumed, with the reason.

## 1. Source

| Item | Value |
| --- | --- |
| File | `tenant_testfits\CNSA_ASC\ASC Rea Farms PRESENTATION PLAN v3 20260915.pdf` (read-only; SHA-256 `440e03c8…dff7d3`, 233,607 bytes) |
| Author | McCulloch England Architects (logo on sheet) |
| Title on sheet | CNSA REA FARMS ASC — "1 / A1 FLOOR PLAN - LEVEL 1" |
| Date on sheet | 9-15-2026 (PDF created 2026-09-15 17:17 by Bluebeam) |
| Scale on sheet | 1/8" = 1'-0" |
| Printed areas | **ASC - 12,503 SQ. FT** · **SHELL - 5,716 SQ. FT.** |
| Content type | one 42" × 30" page, **vector linework + live text** (not a scan); rooms are colored filled rectangles with name and SF labels |
| Floor | **Building II, Level 1.** Confirmed: the background of the tenant sheet is the architect's Level 1 plan (A112) — exterior walls, Lobby 101 with Stair 1 and elevator, Stair 2, Elect. Room, Em. Elect. Room, Riser Room, column symbols, drop-off canopy and site walks all coincide with the v014 Level 1 model |

## 2. Registration

Method: every line segment of the tenant PDF was compared with every line segment of the Level 1 Dimension Plan A112 Rev 5 (the sheet the v001–v014 model was built from, already registered to the model at 9 pt = 1 ft). Segments of identical length and direction vote for a translation; the winning translation was then refined by least squares, first as a full similarity transform (free scale and rotation) and then as a pure translation.

| Item | Value |
| --- | --- |
| Matched points | **2,875 segment endpoints** on base-building linework common to both drawings |
| Fitted scale factor | **1.0000158** (i.e. the PDF really is 1/8" = 1'-0": 9.000 PDF points per foot; **no scaling applied**) |
| Fitted rotation | **0.0006°** (none applied; plan north = model +Y) |
| Transformation used | uniform, translation only: **x_ft = (X_pdf − 651.395) / 9**, **y_ft = (1571.795 − Y_pdf) / 9** (PDF Y runs downward). Relative to the A112 sheet the tenant sheet is shifted +139.495 pt in X and −57.705 pt in Y |
| Residual, all anchors | **RMS 0.027 ft (⅓"), maximum 0.070 ft (⅞")** — the same size as the rounding of coordinates inside the two PDFs |

Residuals by anchor group (translation only):

| Anchor group | Points | RMS (ft) | Max (ft) |
| --- | --- | --- | --- |
| West exterior wall and Stair 2 | 371 | 0.024 | 0.070 |
| North exterior wall (CW3, door 100A bay, CW2) | 915 | 0.026 | 0.070 |
| South exterior wall (SF1 windows, recess) | 861 | 0.026 | 0.070 |
| East exterior wall | 539 | 0.029 | 0.065 |
| Lobby 101 and Stair 1 | 222 | 0.019 | 0.065 |
| Elevator shaft | 64 | 0.031 | 0.065 |
| Elec. 102 / Riser 104 rooms | 55 | 0.031 | 0.070 |

Because anchors on all four exterior walls (205 ft and 106 ft apart) agree to under an inch with scale 1.00002, the registration does not depend on any single point and no non-uniform scaling was used.

## 3. Area reasonableness check (before modeling)

| Quantity | Printed | From registered geometry | Difference |
| --- | --- | --- | --- |
| ASC | 12,503 SF | 12,444 SF = union of all colored room and circulation fills | −0.5 % |
| Shell | 5,716 SF | about 5,698 SF = v014 Level 1 interior (inside face of exterior wall lining) east of the ASC boundary line and east of the lobby | −0.3 % |
| 45 walled rooms | printed SF | fill rectangle minus the drawn walls | **within 1.5 SF for 35 of the 45 walled rooms**; the other ten differ by 2–15 SF where a room borders a base-building wall or overlaps another room (e.g. OR 350.9 vs 350, PROCEDURE 210.9 vs 210, PRE/POST 152.1 vs 152) |

The full room-by-room table is at the end of this document and in `notes/tenant_concept_A_CNSA_ASC_room_schedule_v015.json`.

## 4. Tenant boundary

West, north and south: the Building II exterior walls. East: a single heavy line at **x = 144.13 ft** (0.6 ft east of column line 9) from the south wall to the lobby (y 0.5 → 72.6) (**M**). North-east: the Lobby 101 south wall. The base-building rooms Elect. Room 102, Em. Elect. Room 103, Riser Room 104, Stair 2, Lobby 101, Stair 1 and the elevator are shown white (not part of the ASC). Tenant entry: lobby door pair **101C** into WAIT. Exterior door **100A** serves the DISCHARGE VESTIBULE.

## 5. What the drawing contains, and how each element is modeled

| Drawn element | Found | Modeled as |
| --- | --- | --- |
| Partitions drawn as **double lines** | 148 wall rectangles; thickness 0.41–0.43 ft (= 4⅞", a 3⅝" stud wall) for 136 of them, a few 0.38–0.63 ft (**M**) | **120** are interior partitions: solid, at the drawn position and thickness, **height 10'-0" A**. The other **28** are room-outline lines that run along the inside of the exterior wall (see §7): kept in the file in a hidden sub-collection, **not shown**, because they would cover the exterior glazing |
| **Single lines** between PACU bays and between the three 64 SF PRE/POST bays | 5 lines (**M**) | thin 2" dividers, **7'-0" high, type unknown (A)** — could be curtains or partitions |
| Single lines at the open fronts of PACU / PRE-POST bays, CONTROL and NURSE (19 SF) | 5 lines (**M**) | floor marker lines only (no geometry above the floor) |
| Heavy single line on the east ASC boundary | x = 144.13 (**M**) | demising partition 4⅞" thick, 10'-0" high (**A**: thickness and height not given) |
| "RED LINE" dashed line and tags | between DECONTAM / CONTROL / the two PROCEDURE rooms (**M**) | red floor marker |
| Tables drawn as 3'-0" × 7'-0" rectangles | 3 OR tables, 2 procedure tables (**M**) | plain boxes 3'-0" high (**A** height) |
| Dashed rectangles in ORs and procedure rooms | zones, not objects | not modeled |
| Room fills and labels | 57 named rooms/bays, 19 circulation pieces | one thin floor plate per room carrying its name, ID, printed SF and modeled SF; flat text labels in a separate sub-collection |
| **Doors** | **none — the presentation plan does not draw a single tenant door, door swing or opening** | **no tenant doors or openings are modeled** (see §7) |
| Casework, reception desk, nurse-station counters, lockers, plumbing fixtures | none drawn | not modeled |

## 6. Base-building conflicts and coordination items (base building preserved in every case)

1. **Lobby door 101D** (3'-0", 45-min, west wall of Lobby 101) opens directly against the east wall of PRE/POST A-009; the plan shows no route from that door.
2. **Partitions landing on exterior glass.** All PRE/POST and toilet partitions on the north side end on the continuous **CW3 curtain wall**, and two partitions plus the TLT A-010 room end on the **CW4** glazed corner; mullion alignment is not shown. On the south wall, partitions end inside storefront windows **SF1**: x = 44.14 (STERILE INSTRUMENTS / OR), x = 62.05 (OR / OR), x = 110.59 (CLEAN / LOCKER), x = 122.59 (TLT), x = 128.00 (LOCKER / LOUNGE, 0.5 ft from the opening edge).
3. **Glazed rooms.** The three ORs, STERILE INSTRUMENTS, CLEAN, both LOCKER rooms, LOUNGE and MECH. PUMP have existing storefront windows in their exterior wall; toilet A-010 sits against the CW4 curtain wall. Recorded only; no judgment made.
4. **Columns in circulation** (pinch points): **H-7.2** stands 1.2 ft north of the OR A-050 wall in the sterile corridor; **H-5** stands 3.2 ft north of the OR wall in the same corridor; **F-3** stands at the south edge of the 6.7 ft corridor outside Stair 2 door 110A, leaving about 5.6 ft.
5. **Columns inside rooms:** H-3 free-standing in STERILE PROCESSING (5.4 ft from the nearest wall), H-8.3 free-standing in LOCKER A-043, E.1-2.8 inside JAN A-025, G-9 inside WAIT at the demising line, A-3 in SHARED TLT A-004, K-3.1 in STERILE INSTRUMENTS, K-5 in OR A-052, K-8.3 in LOCKER A-053. Columns F-4, F-7, G-8, K-6, A-1, A-5, A-7, C-1, K-2 fall within or against drawn partitions.
6. **Level 1 slab.** Almost the whole ASC stands on the area where the base building provides **no slab on grade** ("future slab, not in scope", v014).
7. **Stairs, elevator, shafts, core walls:** no tenant element overlaps Stair 1, Stair 2, the elevator, the lobby walls or the electrical / riser rooms. Stair 2 door 110A opens into a tenant corridor. There are no base-building shafts on Level 1.
8. **Em. Elect. Room.** The tenant plan shows "EM. ELECT. ROOM" as an existing white room; in the base building it is only a future room (v014 shows its outline). MED GAS abuts it.

## 7. Ambiguous elements

- **Room outlines along the exterior wall.** Every room is drawn as a closed rectangle, so 28 outline segments run along the inside of the exterior walls, in front of the CW3 curtain wall and the SF1 windows. Whether these are intended furring walls (plausible at the ORs) or just the block-plan outline cannot be determined. They are kept as hidden objects (`…_ambiguous_perimeter_outline_walls`) and the base-building glazing is left visible. The partition drawn on column line 1, about 1.4 ft inside the CW4 curtain wall (west side of PRE/POST A-002, A-013), is farther from the wall and is modeled as drawn.
- **No doors anywhere.** Every walled room is a closed box on the drawing. Door positions, widths and swings cannot be derived and were **not invented**; consequently rooms cannot be walked between in the model, and door-position error cannot be measured.
- PACU (65 SF) and the 64–65 SF PRE/POST bays: the printed areas equal the fill rectangle reduced by a wall thickness on every side, yet the bays are drawn with single lines and open fronts — curtain bays or walled rooms is not determinable.
- RECEPTION and NURSE STATION are drawn as fully walled rectangles with no counter or opening.
- "NURSE 19 SF" and "CONTROL 41 SF": labels sit outside small fills; treated as open alcoves.
- The two LOCKER rooms' printed areas (319 / 320 SF) include the toilet drawn inside them.
- WAIT: printed 591 SF is one rectangle; an unlabeled arm of the same color (62 SF) connects it west to the corridor.
- A thin line 0.9 ft south of the lobby south wall (y = 71.4) along WAIT: meaning unknown, not modeled.

## 8. Assumptions

Partition height 10'-0" for every tenant partition including the demising line · bay dividers 7'-0" × 2" · table height 3'-0" · wall thickness as drawn · no ceilings (open to the Level 2 deck at 15'-5½") · neutral materials, lightly tinted by the plan's own room color groups so rooms can be told apart · **review lighting only**: two soft overhead area lights inside the concept collection so windowless rooms can be seen; they are not a lighting design.

## 9. Intentionally excluded

Doors and hardware · casework, counters, lockers, fixtures, furniture, medical equipment other than the five drawn tables · wall assemblies, ratings, shielding, acoustic construction · ceilings, lighting design, medical gas, plumbing, electrical, HVAC · finishes · signage, people · any change to the base building.

## 10. Registered underlay

A 150 dpi image of the tenant sheet is saved as `exports/tenant_underlay_Concept_A_CNSA_ASC_v015.png` (made with `pdftoppm -r 150 -png -singlefile`, Poppler, already installed) and placed in the model as a flat plane at the registered position (page corners x −72.377 → 263.623 ft, y −65.355 → 174.644 ft). It is hidden except in the registration-overlay render.

## 11. Reusable workflow (for Concept_B, Concept_C, revised plans)

1. Put the tenant file in `tenant_testfits\<TENANT>\` (read-only). 2. Convert to vector segments; vote-and-fit the transform against A112 (Level 1) or A122 (Level 2); report scale, rotation and residuals by anchor group. 3. Extract room fills and labels, double-line walls, single lines, equipment outlines, doors if drawn. 4. Check areas and conflicts against the v014 base. 5. Write the control document. 6. Add one data block per concept to the build script; the generic builder creates `Concept_X_<NAME>` with sub-collections for labels, viewpoints, underlay and review lighting. Hiding or deleting that one collection removes the concept.

## 12. Room schedule (printed vs modeled)

| ID | Room (as labeled) | Printed SF | Modeled SF | Net of rooms drawn inside | Enclosure as drawn | Fill rectangle x0, y0 → x1, y1 (ft) |
| --- | --- | --- | --- | --- | --- | --- |
| A-001 | DISCHARGE VESTIBULE | 105 | 104.7 |  | walled (double lines), no door drawn | 78.7, 96.0 → 92.6, 104.8 |
| A-002 | PRE/POST | 152 | 152.1 |  | walled (double lines), no door drawn | 1.4, 91.5 → 14.9, 104.4 |
| A-003 | PRE/POST | 152 | 152.1 |  | walled (double lines), no door drawn | 14.5, 91.5 → 28.0, 104.4 |
| A-004 | SHARED TLT | 55 | 55.0 |  | walled (double lines), no door drawn | 27.6, 93.5 → 33.9, 104.4 |
| A-005 | PRE/POST | 152 | 152.1 |  | walled (double lines), no door drawn | 33.5, 91.5 → 47.0, 104.4 |
| A-006 | PRE/POST | 152 | 152.1 |  | walled (double lines), no door drawn | 46.6, 91.5 → 60.1, 104.4 |
| A-007 | SHARED TLT | 55 | 54.9 |  | walled (double lines), no door drawn | 59.7, 93.5 → 66.0, 104.4 |
| A-008 | PRE/POST | 152 | 152.3 |  | walled (double lines), no door drawn | 65.6, 91.5 → 79.1, 104.4 |
| A-009 | PRE/POST | 155 | 160.6 |  | walled (double lines), no door drawn | 92.2, 90.6 → 105.0, 104.3 |
| A-010 | TLT | 52 | 52.3 |  | walled (double lines), no door drawn | 0.5, 83.1 → 7.9, 92.0 |
| A-011 | SHARED TLT | 54 | 55.9 |  | walled (double lines), no door drawn | 94.2, 84.8 → 105.0, 91.0 |
| A-012 | PRE/POST | 155 | 161.1 |  | walled (double lines), no door drawn | 92.2, 71.4 → 105.0, 85.2 |
| A-013 | PRE/POST | 164 | 169.3 |  | walled (double lines), no door drawn | 1.8, 69.8 → 15.3, 83.5 |
| A-014 | MEDS | 96 | 98.8 |  | walled (double lines), no door drawn | 14.9, 69.8 → 23.2, 83.5 |
| A-015 | NURSE STATION | 216 | 230.7 | 213.1 | walled (double lines), no door drawn | 22.7, 69.8 → 41.3, 83.5 |
| A-016 | CLEAN | 135 | 135.6 |  | walled (double lines), no door drawn | 58.8, 67.3 → 68.4, 83.5 |
| A-017 | NOURISH | 90 | 90.6 |  | walled (double lines), no door drawn | 68.0, 76.8 → 84.2, 83.5 |
| A-018 | PACU | 65 | 79.2 |  | open bay / alcove (single lines) | 49.3, 74.8 → 58.8, 83.2 |
| A-019 | TLT | 60 | 60.1 |  | walled (double lines), no door drawn | 68.0, 67.3 → 75.4, 77.2 |
| A-020 | PRE/POST | 65 | 79.2 |  | open bay / alcove (single lines) | 75.4, 67.3 → 83.8, 76.8 |
| A-021 | PACU | 65 | 79.2 |  | open bay / alcove (single lines) | 49.3, 66.5 → 58.8, 74.8 |
| A-022 | TLT | 54 | 54.9 |  | walled (double lines), no door drawn | 32.2, 64.9 → 41.3, 72.2 |
| A-023 | WAIT (west arm, same fill colour, no separate label) | — | 61.7 |  | open area | 105.4, 64.1 → 113.8, 71.4 |
| A-024 | WAIT | 591 | 632.2 |  | open area | 113.8, 50.2 → 143.7, 71.4 |
| A-025 | JAN | 22 | 24.6 |  | walled (double lines), no door drawn | 26.8, 64.9 → 32.6, 70.2 |
| A-026 | NURSE | 19 | 28.4 |  | open bay / alcove (single lines) | 59.2, 59.3 → 62.8, 67.3 |
| A-027 | PACU | 65 | 79.2 |  | open bay / alcove (single lines) | 49.3, 58.2 → 58.8, 66.5 |
| A-028 | OFFICE | 147 | 147.1 |  | walled (double lines), no door drawn | 92.2, 51.4 → 105.4, 64.1 |
| A-029 | TLT | 52 | 52.2 |  | walled (double lines), no door drawn | 105.0, 56.7 → 113.8, 64.1 |
| A-030 | PRE/POST | 64 | 77.6 |  | open bay / alcove (single lines) | 59.2, 49.8 → 67.4, 59.3 |
| A-031 | PRE/POST | 64 | 77.5 |  | open bay / alcove (single lines) | 67.4, 49.8 → 75.6, 59.3 |
| A-032 | PRE/POST | 64 | 77.6 |  | open bay / alcove (single lines) | 75.6, 49.8 → 83.8, 59.3 |
| A-033 | MED GAS | 120 | 126.1 |  | walled (double lines), no door drawn | 17.7, 44.3 → 27.7, 58.2 |
| A-034 | BREAK DOWN | 171 | 171.1 |  | walled (double lines), no door drawn | 27.3, 44.3 → 41.3, 58.2 |
| A-035 | PACU | 65 | 79.2 |  | open bay / alcove (single lines) | 49.3, 49.8 → 58.8, 58.2 |
| A-036 | TLT | 52 | 52.1 |  | walled (double lines), no door drawn | 105.0, 49.8 → 113.8, 57.2 |
| A-037 | PROCEDURE | 210 | 210.9 |  | walled (double lines), no door drawn | 92.2, 34.0 → 105.4, 51.8 |
| A-038 | ANESTHESIA OFFICE | 101 | 100.8 |  | walled (double lines), no door drawn | 105.0, 38.5 → 115.0, 50.2 |
| A-039 | RECEPTION | 254 | 254.8 |  | walled (double lines), no door drawn | 114.6, 38.5 → 138.7, 50.2 |
| A-040 | SOILED | 219 | 219.2 |  | walled (double lines), no door drawn | 49.3, 37.8 → 69.8, 49.8 |
| A-041 | PROCEDURE | 210 | 210.6 |  | walled (double lines), no door drawn | 69.3, 34.0 → 84.2, 49.8 |
| A-042 | DECONTAM | 226 | 230.3 |  | walled (double lines), no door drawn | 17.7, 34.0 → 41.3, 44.7 |
| A-043 | LOCKER | 319 | 311.8 | 246.1 | walled (double lines), no door drawn | 110.4, 19.3 → 128.2, 38.9 |
| A-044 | TLT | 65 | 65.7 |  | walled (double lines), no door drawn | 122.4, 25.1 → 128.2, 38.9 |
| A-045 | OFFICE | 132 | 132.5 |  | walled (double lines), no door drawn | 127.8, 25.0 → 138.7, 38.9 |
| A-046 | CONTROL | 41 | 55.0 |  | open bay / alcove (single lines) | 49.7, 34.0 → 64.0, 37.8 |
| A-047 | STERILE PROCESSING | 440 | 448.1 |  | walled (double lines), no door drawn | 17.7, 10.9 → 37.9, 34.4 |
| A-048 | JAN | 77 | 78.0 |  | walled (double lines), no door drawn | 97.7, 13.9 → 105.4, 26.0 |
| A-049 | LOUNGE | 380 | 380.8 |  | walled (double lines), no door drawn | 127.8, 0.1 → 144.1, 25.4 |
| A-050 | OR | 350 | 350.9 |  | walled (double lines), no door drawn | 79.8, 2.5 → 98.1, 23.3 |
| A-051 | OR | 350 | 350.4 |  | walled (double lines), no door drawn | 43.9, 0.5 → 62.3, 21.3 |
| A-052 | OR | 350 | 350.6 |  | walled (double lines), no door drawn | 61.8, 0.5 → 80.2, 21.3 |
| A-053 | LOCKER | 320 | 313.0 | 247.3 | walled (double lines), no door drawn | 110.4, 0.1 → 128.2, 19.7 |
| A-054 | MECH. PUMP | 178 | 183.7 |  | walled (double lines), no door drawn | 5.1, 0.5 → 18.2, 15.8 |
| A-055 | CLEAN | 165 | 165.4 |  | walled (double lines), no door drawn | 97.7, 0.1 → 110.8, 14.3 |
| A-056 | TLT | 65 | 65.7 |  | walled (double lines), no door drawn | 122.4, 0.1 → 128.2, 13.9 |
| A-057 | STERILE INSTRUMENTS | 257 | 257.5 |  | walled (double lines), no door drawn | 17.8, 0.5 → 44.3, 11.3 |

"Modeled SF" = the room's colored fill rectangle minus the partitions extracted from the drawing. Sum of printed room areas: 8,606 SF; circulation fills: 3,028 SF; union of all fills: 12,444 SF (printed ASC 12,503 SF).

