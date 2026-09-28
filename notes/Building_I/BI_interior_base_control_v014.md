# Building I — interior base-building framework v014: control document

Date: 2026-09-25
Controlling exterior: `models\Building_I\BI_presentation_v013.blend` — owner-approved 2026-09-25 as the FINAL EXTERIOR PRESENTATION BASELINE, used read-only. Frozen: `manifests\BI_freeze_BuildingI_v013_approved.json` (244 files, PASS).
Authorised gate: BUILDING I INTERIOR BASE-BUILDING MODEL (skill gate 5). Not authorised: tenant concepts, browser viewer.
Data: `BI_interior_base_data_v014.json` (every level, slab, column, wall rectangle, stair, elevator, door, tenant zone, camera). Script: `scripts\Building_I\BI_build_interior_base_v014.py`. Output: `models\Building_I\BI_interior_base_v014.blend`, renders `BI_interior_base_v014_*.png`, viewer data `BI_interior_base_viewer_v014.json`. Validation: `BI_interior_base_validation_v014.md`.

## 1. Coordinates, units, datums

Building I feet; origin grid 1 × grid A at FFE 661.75; +X east, +Y north; z above LVL-01. Blender units metres (× 0.3048). Grid table as v001 (X: 1=0, 2=12.33, 3=30, 3.7=40, 4=45, 5=60, 6=72, 7=90, 8=120, 9=150, 10=180, 11=210, 12=240, 12.9=268, 13=270, 14=280; Y: A=0, B=4, B.7=22.0, C=30, C.6=42, C.9=50.5, D=52.33, E=61.5, F=70.583, F.2=74.54, G=80.53, G.2=83.58, H/H.1=98.695, J=102.03, K=119.28, K.1=124.78, K.7=133.78, L=138.53, L.6=154.53, M=168.53, M.7=187.11, N=198.53). B.7 / C.6 / C.9 were added this pass from the A1.00b bubble registration (V).

| Datum | ft above LVL-01 | Code | Source |
| --- | --- | --- | --- |
| LVL-01 | 0.000 (FFE 661.75) | W | A0.01 / A5.01 |
| Gallery (structural datum) | 11.000 | W | A4.01 / A5.01 — the gallery cantilever's soffit datum; Gallery 234 itself is a Level 2 room and the gallery stair rises to LVL-02 (A6.14) |
| Mezzanine (Sports Science Lab 233) | 13.021 | W | A5.01 / A6.13 (23 risers × 6 13/16" = 13.06) |
| LVL-02 | 15.333 | W | A5.01 |
| T.O.S. col 14 / A / F / N | 28.0 / 30.0 / 31.5 / 37.292 | W | A4.01, A5.01 |
| Elevator pit / footing | −5.0 / −2.0 | W | A6.01 |

## 2. Source hierarchy for this gate

| Rank | Source | Used for |
| --- | --- | --- |
| 1 | Rev 14 A1.01 / A1.02 building plans (p.26–27), vector | room layout, every interior wall pair (stroke classes 3 = partitions, 10 = exterior / shaft walls), stair and elevator positions, door tags; registration = v008 grid-bubble fit (RMS 0.027 ft) |
| 2 | A1.00b Level 2 edge of slab (p.24), vector clip regions | Level 2 and mezzanine slab extents (30 rectangles + the gallery polygon) |
| 3 | A5.01 building sections; A6.01/A6.02 elevator; A6.11–A6.14 stairs; A0.21/A0.22 wall types; A7.01 door schedule; A3.01/A3.02 RCPs | levels, slab build-up, hoistway, treads/risers/landings, wall thicknesses, doors, ceiling heights (recorded) |
| 4 | S101 / S102 / S103 / S104 / S601 / S401–S403 | 4" slab on grade, framing member sizes, column marks and sizes (84), braced-frame members |
| 5 | G0.01 code summary; Jays Cleaning SF plans (owner derivative 10/2/2025) | published area figures for the check only |
| 6 | CNSA A100 rev 8 (McCulloch England, 2/18/2026) | existing tenant partitions and extent ONLY (black lines = new tenant walls; the FMK background is grey and excluded by construction) |
| — | photographs | not used for interiors (no hidden geometry inferred from photos) |

## 3. What is BASE_BUILDING, what is EXISTING_TENANT, what is left out

**BASE_BUILDING** (collection `Building_I/BASE_BUILDING`, 24 objects):
- `BB_L1_slab_on_grade` — 4 in (W), footprint = the union of the approved v008 shell prisms at z 0 (45,091 sq ft).
- `BB_L2_composite_slab` — 6 1/2 in composite (W, A6.01), extent from A1.00b (24,095 sq ft), exact-boolean union of the hatch rectangles and the gallery polygon; `BB_mezzanine_slab_233` (1,423 sq ft at 13.02).
- `BB_columns_S601` — 84 columns at their grid intersections, sizes from S601 (W10X33…W16X100, HSS6/8/10), box placeholders d × bf, top at the roof T.O.S. formula; orientation assumed (web ∥ y).
- `BB_extwall_inner_faces` / `_TWS1_translucent` / `BB_extwall_window_reveals` — the inside face of every exterior wall = the v008 outside face offset inward by the A0.21 wall-type thickness (BRK1 1'-2 1/8", PNL1 10 5/8", PNL2 9 5/8", PNL3 10 1/2", curtain wall 6", TWS1 7"), material from the v008 finish regions, apertures cut where the v001 lite placeholders are, with jamb/head/sill reveals; 99 faces.
- `BB_core_walls_L1` / `_L2` — wall rectangles inside the core zones (elevator/elec 103-104/203, restrooms 105-108 / 111-112 / 127-130 / 207-208, tele 145/245, riser 129, corridor 102/202 rated walls, south stair 131/231, gallery stair 126, courts vestibule 123, sports-science-lab end walls), height to the deck.
- `BB_fmk_program_partitions_L1` / `_L2` — the remaining FMK-documented partitions of the sports-medicine program (offices, training, PT, lockers, storage, Taylor Capital suite 210-226), 10 ft high. They are in the base set of drawings but are not structure or core; kept as a separate object so a test fit can treat them as movable.
- `BB_stair_*` (5) with guards — lobby stair (A6.11), south stair 131/231 (A6.12), gallery stair 126 (A6.14), mezzanine stairs east and west (A6.13, west = mirror note): risers 6 13/16", treads 11", counts and landings as written; run directions of the south and gallery return flights interpreted (I).
- `BB_elevator_hoistway_walls` / `BB_elevator_pit_slab` — inside 7'-0" × 8'-8" (W; vector 7.04 × 8.67), 8 in shaft wall, pit −5.0, top 33.0.
- `BB_roof_deck_underside_TOS` — plates at the written top-of-steel datums (linear between); joists/trusses not modeled.

**EXISTING_TENANT / CNSA** (4 objects): `CNSA_partitions_L1` (519 rectangles), `CNSA_partitions_L2` (169), and the two zone plates (L1 16,216 sq ft = the whole MOB Shell 150-S; L2 10,846 sq ft, x 11.3–185, the west part of MOB Shell 250-S). Nothing from the CNSA set went into BASE_BUILDING. Demising = the corridor 102/202 south walls (base building).

**FUTURE_CONCEPTS / Concept_A / B / C**: empty (asserted).

**Not modeled**: furniture, casework, equipment, ceilings (heights recorded), doors as leaves (schedule recorded with tag positions), MEP, joists/trusses/braces as members, stair stringers, guard details, the ADA lift (A6.02), the storefront/curtain-wall framing, the CNSA ceilings/millwork/equipment, the tenant doors.

## 4. Extraction method (so it can be repeated)

- Wall pairs: parallel black lines of the wall stroke classes 1.8–9.5 pt apart (0.27–1.4 ft) sharing ≥ 5 pt of overlap → boxes; unioned on a 0.125 ft raster into axis-aligned rectangles (617 L1, 532 L2); rectangles on the exterior wall line (within 1.6 ft of a v008 outside face) or inside the hoistway are dropped (they are the shell / the elevator object). Core vs program by zone table (data file).
- CNSA: the same detector on the black lines of A100 (p.11); registration by the wing outside faces and the corridor wall (I, ±0.5 ft L1 / ±1 ft L2).
- Column schedule: S601 words — each mark takes the size word directly above it in its column band.
- Overlay check: `renders\Building_I\BI_interior_base_v014_overlay_L1_A1.01.png` / `_L2_A1.02.png` (cutaway render at 55 % over the registered plan).

## 5. Interior heights (W written / I interpreted / M measured / A assumed)

| Item | Value | Code |
| --- | --- | --- |
| Floor-to-floor L1→L2 | 15.333 | W |
| L2 slab underside | 14.79 | I (15.333 − 6.5 in) |
| L1 under structure (wing / west block) | 13.5–13.6 | I (W16X26/31 15.7–15.9 in; W14X22 bays) |
| L1 ceilings | 9'-0" (Type 2/3, west block rooms), 9'-6" (lobby at grid 6), 10'-2" (Type 6, north entrances), 8'-9" (entry vestibule), 10'-6" GWB (elevator lobby), 11'-8" (west storefront soffit); MOB Shell 150-S none | W (A3.01, A6.01) |
| L2 ceilings | 8'-0"/8'-2" (offices 212–216, 225, corridor 204), 9'-0" (209/210/224 zone), 10'-6" baffles (210), 10'-0" GWB (elevator lobby); MOB Shell 250-S none | W (A3.02, A6.01) |
| L2 under roof structure | 12.7–14.2 above LVL-02 | I (T.O.S. 30.0→31.5 minus W18–W24 roof beams) |
| Courts clear (to truss bottom chord) | ≈ 27 (F) → 31 (N) | M (A5.01 D1, truss depth 4.5→6.5 ft scaled) |
| Training 119/120 clear | ≈ 30 | M (double-height, roof formula minus joists) |
| Gallery cantilever soffit | 9.0 | M (v008) |
| Slabs | SOG 4 in (W); L2 6 1/2 in composite (W); mezzanine = L2 (A) |

## 6. Structural / tenant constraints recorded (viewer JSON `constraints`)

Columns (84, S601); elevator hoistway (x 91.25–99.92, y 71.87–78.91, pit −5 to top 33); five stairs; restroom cores 105–112 / 127–130 / 207–208; elec 103/104/203/225; tele 145/245; riser 129; corridor 102/202 rated walls; floor openings — lobby band x 28.5–71 y 53.5–74.4 (double-height, no L2 slab), courts x 121–271 y 71.5–186 open to the roof, training 119/120 x 71–121 y 170–198 open to the roof, south-stair well x 275–281 y 79.7–96, gallery stair; braced frames — A5.01 shows X-braced bays between grids 9–10 and 11–12 on the wing/courts grid-line walls (members HSS8X8, HSS20X8, HSS4X4, HSS14X6 per S401–S403); the S401–S403 elevation titles could not be text-parsed so the exact grid lines are recorded from the sections (M) and not modeled as members; low-clearance zones as §5.

## 7. Assumptions and unresolved items (none resolved silently)

- Partition heights (10 ft program / to deck for core) — not in the plans (A).
- Column orientation (web ∥ y) and box placeholders for the W-shapes (A); splices ignored.
- Mezzanine slab thickness = L2 (A); roof deck modeled as T.O.S. plates only.
- Stair run directions of the south and gallery return flights (I); the mezzanine east stair's 8-tread flight is drawn 6'-5" (= 7 treads) but written 8 treads — the written count is used and the discrepancy is recorded (**I-1**).
- CNSA registration (I, ±0.5–1 ft); CNSA L2 east limit x ≈ 185 read from the plan (I).
- Exterior wall inner faces use the full A0.21 type thickness; the MOB-shell inner gypsum board is "by tenant at time of upfit" (A0.21) — the base face is 5/8 in outboard of the finished tenant face (**I-2**).
- Gallery datum 11'-0" vs Gallery 234 on the Level 2 plan: modeled per A1.00b (the gallery slab is part of the Level 2 slab at 15.33; the 11.0 datum is the cantilever soffit) (**I-3**, to be confirmed with A5.15 A2 when the interior of the gallery is detailed).
- Braced-frame grid lines by section reading only (**I-4**).
- Carried unchanged: every exterior/site/landscape open item (G-1…G-6, G-15, F-1…F-9, SC-1, SC-3, LC-2, etc.).
