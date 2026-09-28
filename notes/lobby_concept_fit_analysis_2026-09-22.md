# Building II main lobby — existing conditions and concept-fit analysis

Date: 2026-09-22 · Phase: **inspection only — nothing modeled, no file changed**
Concept source: `source_documents\concept_design\Rea_Farms_2_Lobby.pptx` (read-only; SHA-256 `b74469ee6e25…`; byte-identical to the copy in `source_documents\Building II\Photos\`; created 2026-06-26 by Brandon Taylor; 2 slides, each one image, no text or notes).

Labels used below: **DOCUMENTED** (Building II model or permit documents) · **CONCEPT** (read from the PowerPoint images) · **PROPOSED** (recommended adaptation) · **ASSUMPTION** (design choice needed, not documented).

## 1. Approved baseline and controls

| Item | Status |
| --- | --- |
| Latest approved Blender model | **`models/building_shell_v015.blend`** (approved as the Concept_A_CNSA_ASC baseline). v016–v018 are viewer-only versions built from v015; there is no newer .blend. Next model version would be **v019** (`scripts/build_shell_v019.py`, `models/building_shell_v019.blend`), created only after approval. |
| Freeze | SHA-256 snapshot of all 350 project files (models, scripts, notes, renders, exports, three viewers, tenant PDF) taken before this inspection; **0 changed** at the end of it. |
| `source_documents` | read-only; `Building II` 360 files unchanged; `Building I` not opened (aggregate 1,231 files / 6,929,037,544 bytes unchanged); the new `concept_design` folder holds only the PowerPoint. |
| Lobby coordinate system | unchanged: decimal feet, origin grid 1' × K', X east, Y north, Z up; Level 1 = 0.0, Level 2 = 16.0. |

## 2. The most important finding

**The approved permit set already contains a full interior design for this lobby, and the PowerPoint is a rendering of essentially that design.** Sheets (all in `Building II\00 PLANS\Approved Set\APPROVED-COS-001319.pdf`, issue E 09/29/2025, county-approved 1/30/2026; not reissued in Revision 5 except ID101/ID102):

| Sheet | Content (DOCUMENTED) |
| --- | --- |
| **ID201** Interior Elevations (p.156) | Lobby west / south / east / north elevations. **West elevation = full-height "WOOD WALL PATTERN" behind Stair 1**, PT-02 metallic on the Level 2 balcony fascia, PT-01 elsewhere, LT-01 / LT-02 tags, banquette and stair on the south elevation. |
| **ID302** Interior Details (p.159) | "A4 Enlarged wood feature wall elevation", "A5 / A6 Wood feature wall with lights elevation", "A1–A3 Panel A / B / C", "B4 Wood wall plan section": vertical plastic-laminate-wrapped plywood boxes of **varying width and length**, "sconce behind the box", small wall luminaires set into the field, "all lights applied to surface"; panel-top heights 21'-10⅝", 18'-6", 17'-5⅜", 16'-9¼", 13'-1½". Also "B2 Drop-down ceiling with inset lighting" and "B4 East elevator wall Clarus system". |
| **ID303** Banquette sections / details (p.160) | Built-in banquette at the stair foot: **south banquette 9'-3"** and **west banquette + stair 8'-7⅞"**, upholstered seat FAB-01, POR-02 tile plinth, TR-04 USB outlets, two tiled steps (11" treads) at the stair base. |
| **ID801** Finish schedule (p.161) | POR-01 **Porcelanosa Santorini Gray Nature 47" × 47"**, custom #643 warm-gray grout · WOM-01 Mohawk walk-off 24" × 24" · PL-01 **Wilsonart Uptown Walnut Softgrain, grain vertical** (the wood wall) · WD-01 **Grothouse walnut treads, Bianca oil, match PL-01** · PT-01 SW 7646 First Star satin (warm off-white) · PT-02 Scuffmaster SM9500 Metal · RB-01 Johnsonite 6" base · SS-01 MSI Acura White polished slab · FAB-01 Green Hide Lena Mystic leather · SP-01 Florence gray silver-speck planter 17" × 23¼" · DP-01 Clarus wall-to-wall glass panel · LT-01 **Lightnet Caleo Inverse suspended ring system, 1.5" profile** · LT-02 Coronet Magneto recessed track, black, mitered corners · LT-03 Startek Med Beam black linear · LT-04 BEGA 33 590 black wall luminaires 3" × 5⅛" × 3¾" |
| **A212** Rev 5 RCP (p.7) | Level 2 lobby: gypsum ceiling CA-1 at **12'-11⅜" AFF (z 28.95)**, a 23'-6" × 18'-7" coffer stepping to 12'-6" and an inner 11'-6" × 6'-6¾" panel at 12'-0" AFF (z 28.0) that carries the **LT-01 pendant cluster (six nested rounded squares drawn)**; LT-02 track at the coffer edges; LT-03 linear at the south. Level 1 lobby: open to Level 2 ceiling; LT-01/02 tags along the west wall (wood wall lighting). |
| **A500 / A501** Stair 1 (p.43–44) | Steel stair, (2) 1" × 14" stringer plates, **wood treads**, riser and stringer painted to match, **glass shoe guardrail with metal-panel finish wrap**, 1½" handrail, metal panel ceiling between stringers, 42" guard / 36" handrail, "stair support columns within furr-out wall only". |
| **E003 / E120** (p.119, 125) | **SH1 "pendant square hollow LED", 3,570 lm, 3500 K, 47 W × 7** at the lobby (E120 shows the cluster; pendant lengths "as directed by the architect"); WL1 indirect/direct wall linear 3500 K × 4; lobby on a low-voltage dimmer + timer. |

So the design language the owner listed — warm vertical walnut feature wall with integrated lights, dark stair expression with glass rail and walnut treads, square ring pendants at varied heights, large-format light porcelain floor, warm-white walls, black metal accents — is **documented design intent, not only concept**. The PowerPoint adds: a specific dark/black stair colour, black rectangular ring fixtures, lounge chairs and tables, a vertical digital directory, planters and artwork (CONCEPT). Recommendation: **model the documented ID design as the base, and use the PowerPoint to resolve the items the drawings leave open** (colours, fixture form, furniture, directory).

## 3. What the PowerPoint shows (CONCEPT)

Slide 1: two views — (a) lobby seen from the entrance: full-height vertical walnut slat wall behind an L-shaped black stair with slender black rail; six black rectangular ring pendants at staggered heights; large light-grey tile; warm-white walls; lounge grouping (two-seat bench + four wood-frame armchairs + low tables); portrait digital directory on a pale-blue clad pier at the left; glazed doors to adjacent rooms; planter and artwork by the right door; entry walk-off mat. (b) view from the lobby floor toward the Level 2 balcony: black balcony fascia with glass guard, high exterior windows on the left, the pendant cluster, elevator door, artwork on the balcony wall. Slide 2: a cleaner version of (a) with the black fascia soffit carrying a continuous warm light line, black ring fixtures in three sizes, and the wood wall reaching the ceiling. Both are staged visualizations (people, props); **not** dimensional evidence.

## 4. Existing Building II lobby (DOCUMENTED, from `building_shell_v015.blend` and the notes it was built from)

**Collections / objects.** Lobby walls: `BASE_Core` (`INT_Core_L1_lobby_west_SA3.1_*`, `…south_SA6.1_*`, `…east_SA6.1_*`, `INT_Core_L2_lobby_*`); exterior walls and glass: `BASE_Exterior` (`INT_ExtWall_L1_P1_e14_*` = CW1 bay, `INT_Glass_L1_P1_e14_108.66_00.00` / `_11.70`, `INT_ExtWall_L2_lobby_head_above_CW1`, `INT_Glass_L2_LobbyBlock_e01_083.51_19.00` = SF7); slabs: `BASE_Level_1` (`INT_L1_slab_poured_ribbon_and_core`), `BASE_Level_2` (`INT_L2_slab`, `INT_Ceiling_L2_lobby_CA-1_a/b`); stair: `BASE_Vertical_Circulation` (`INT_Stair1_run1_tread_01…14`, `INT_Stair1_landing`, `INT_Stair1_run2_tread_01…12`, `INT_Stair1_run1_guard_*`, `INT_Stair1_run2_guard_*`, `INT_Guard_L2_balcony_east_of_stair`, `INT_Guard_L2_balcony_north`, `INT_Guard_L2_south_of_stair`); elevator: `INT_Elevator_shaft_L1_*`, `INT_Elevator_shaft_L2_*`, `INT_Elevator_pit_floor`; columns: `BASE_Structure` (`INT_Column_A-8/A-9/E-8/E-8.4/E-9_*`); exterior masses `01_Masses` (`L1_Podium`, `L2_LobbyBlock`) and opening panels `03_Opening_panels` (`Opening_04/05_N_CW1`, `Opening_17_E_SF7`). Tenant plates `Concept_A_CNSA_ASC_rooms` touch the lobby only at doors 101C / 101D.

**Dimensions (feet, model coordinates; gypsum face to gypsum face / glass).**

| Item | Value |
| --- | --- |
| Level 1 lobby 101, E–W | x 106.59 → 142.45 = **35.86 ft** (35'-10") |
| Level 1 lobby 101, N–S | y 72.89 (south wall) → 103.09 (CW1 glass) = **30.2 ft** (30'-2½") |
| Level 1 elevation / Level 2 elevation / floor-to-floor | **0.0 / 16.0 / 16'-0"** |
| Two-storey clear height | floor 0.0 → gypsum ceiling CA-1 at **28.95 (28'-11⅜")**; roof deck underside 31.75 |
| Level 2 lobby 204 (walls) | west x 106.59 (same plane as Level 1), south y 64.61, east: exterior wall x 143.95 (SF7 window y 83.5–96.9, z 19–28.9) / elevator face x 135.75 (y 72.6–82.6), north CW1 head 28.91 |
| Level 2 floor around the void | south strip x 106.54–124.52 × y 64.61–73.44 (18.0 × 8.8 ft) and balcony x 124.52–135.75 × y 64.61–82.52 (11.2 × 17.9 ft); floor also x 135.75–143.5 south of the elevator (y 64.6–72.6) |
| Level 2 opening (open to below) | west part x 106.54–124.52 × y 73.44–103.3 (**18.0 × 29.9 ft**, contains Stair 1) + east part x 124.52–143.5 × y 82.52–103.3 (**19.0 × 20.8 ft**) ≈ 933 SF incl. the stair |
| Level 1 ceiling where Level 2 floor exists | slab underside **15.46 (15'-5½")** over the south strip and balcony |
| Ceiling coffer over the void (A212) | 23'-6" × 18'-7" at 12'-6" AFF L2 (z 28.5), inner 11'-6" × 6'-6¾" at 12'-0" AFF (z 28.0) → in model terms about x 112.9–136.4 × y 79.9–98.4, inner x 119.0–130.5 × y 85.9–92.4 (positions **M ±0.5 ft** from the RCP strings) |

**Stair 1 (DOCUMENTED, A500/A501; modeled exactly).** L-shaped open stair: **run 1** along the west wall, x 107.08–113.02 (**width 5.94 ft**), 14 treads × 11" = 12'-10", rising south from the first riser at y 92.20 to the landing at y 79.37; **15 risers** to the landing at **8.571 (8'-6⅞")**; **landing** x 107.08–113.52 × y 73.44–79.37 (6.44 × 5.93 ft); **run 2** eastward, y 73.44–79.37 (width 5.93 ft), 12 treads × 11" = 11'-0", x 113.52–124.52, **13 risers** to Level 2 at 16.0; all 28 risers 6.857"; total rise 16'-0". Bounding box x 107.08–124.52, y 73.44–92.20, z 0–16. Orientation: starts at the north end of the west wall next to door 101D, rises south past the wood wall, turns east under the balcony guard and lands on the Level 2 balcony at x 124.52. Modeled guards: stepped 42" glass panels on the open sides (run 1 east side at x 113.02, run 2 north side at y 79.37) and 42" glass along the three Level 2 void edges (y 73.39 south of the stair, x 124.52 and y 82.47 at the balcony). Not yet modeled: stringers, handrails, shoe, nosing, the documented walnut treads and banquette.

**Exterior glazing affecting the lobby.** North wall: **CW1** curtain wall x 108.66–140.49 (31.8 ft) between two 3'-8" piers, lower lite 0–9.97, door canopy zone 9.97–11.7, upper lite 11.7–28.91 (head 28'-10⅞"); **door 101A** 14'-0" × 10'-0" automatic bi-parting entry in the lower lite (centred about x 124.6, position from A815); glass plane at y 103.09–103.17; the piers project north so only 6–7" of pier return shows inside. East, Level 2 only: **SF7** x 144.3, y 83.5–96.9, z 19–28.9 (this is the high window seen at the left of the concept's balcony view). Daylight: north (front, drop-off side) and east (morning). No glazing on the west or south lobby walls.

**Other fixed conditions.** Columns A-8 (105.5, 103.33) and A-9 (143.5, 103.33) sit inside the piers; E-8 (105.5, 71.83), E-8.4 (125.38, 71.83, Level 1 only) and E-9 (143.5, 71.83) sit inside the south wall — **no free-standing column in the lobby**. Elevator: CMU shaft x 135.75–143.08 × y 72.58–82.58, 3'-6" door in its west face at y 77.6–81.1 (opens into the lobby, both levels), pit −5.0. Doors: 101B 6'-0" pair east wall y 88.16–94.74 (tenant east); 101C 6'-0" pair south wall x 126.66–133.2 (tenant WAIT); 101D 3'-0" west wall y 97.56–101.12 (tenant north-west); Level 2: 200A west wall y 64.76–71.4, 200B south wall x 126.46–132.88, 200C restroom. Mechanical shaft on Level 2 west of the lobby wall (x 100.8–106.2, y 73.3–100.7) — the lobby west wall is a 3⅝" rated wall with the shaft behind it: **wood-wall boxes must be surface-applied (as ID302 says), not recessed**. Beams not modeled (clear about 12'-11" under the deepest Level 2 girders elsewhere; the lobby is open to the roof deck at 31.75 with the gypsum ceiling at 28.95). Circulation to keep clear: 101A → 101C (straight south, x 124.6–130), 101A → 101B and the elevator (south-east), 101A → 101D and the stair foot (west), stair landing zone at y 92.2 + 5 ft.

## 5. Concept → real lobby mapping and fit

| Concept element | Fits the real lobby? | Where (PROPOSED) |
| --- | --- | --- |
| Full-height wood feature wall behind the stair | **Yes — it is documented** on the west wall | west wall x 106.59, **y 73.5 → 97.5 (24 ft)** between the south-west corner and door 101D, **z 0 → 28.95**, continuous past the Level 2 floor line (the wall plane is continuous on both levels) |
| Black monumental stair with glass rail | Yes; the real stair is an L (run along the wood wall, landing, return run along the south wall) — the concept's L is similar but its wood wall sits behind the upper run; here the wood wall is behind the **lower** run and the upper run crosses the wood wall's end at the landing | finishes only, on the frozen geometry |
| Ring pendants at varied heights through the void | **Yes — documented cluster** over the void, north of the balcony | inner coffer panel, about x 119–130.5 × y 86–92.4 |
| Large light-neutral porcelain floor | **Documented** POR-01 47" × 47" | whole lobby floor |
| Warm-white walls, black metal accents, black balcony fascia with light line | PT-01 documented; PT-02 metallic on the fascia documented; concept's continuous light line = LT-02 track / LT-03 linear | balcony fascia and coffer edges |
| Lounge chairs / bench / tables | Documented **banquette** (south wall 9'-3", under-stair 8'-7⅞"); loose chairs are CONCEPT | clear zone x 114–124, y 80–96 (between the stair and the 101A→101C path) |
| Directory on a wide pier by the entry | **Cannot** be placed as drawn: the entry piers show only 6–7" inside the lobby; the west wall north of the wood wall has only 2 ft beside door 101D | **east wall y 82.58–88.16 (5.6 ft) south of door 101B**, facing the entry axis and the elevator |
| Artwork, planters | SP-01 planter is documented (location not); artwork CONCEPT | planters at the stair foot / by 101B; artwork on the Level 2 balcony north wall face (seen from below) and the east wall by 101B |
| Digital screen content, branding | out of scope for now (owner instruction: no branding) | — |
| Staged people, props, sky views | not modeled | — |

**Items that cannot be recreated faithfully**: the wide directory pier at the entry (no such pier inside); the concept's stair proportions (the real runs are 5'-11" wide, 15 + 13 risers, landing at 8'-6⅞" — kept as documented); the concept's black balcony soffit spanning the whole lobby width (the real balcony is 11.2 ft wide east of the stair plus the 8.8 ft south strip); the concept's very tall wall-to-ceiling glazing on the right (the real north wall is the CW1 curtain wall with the door canopy band at 10–11.7 ft).

## 6. Proposed design strategy (PROPOSED unless marked)

**A. Wood feature wall** — west wall, 24 ft × 28'-11⅜" (documented position and extent within ±1 ft). Module: **surface-applied vertical boxes** (ID302) in four widths **4" / 6" / 8" / 12"** and three depths **¾" / 1¾" / 3"** (ASSUMPTION — ID302 shows varying widths and a plan section but the text extract gives no depths; measure the ¾" = 1'-0" plan section before building), lengths staggered so the top edge steps between 13'-1½" and 21'-10⅝" with the tallest boxes continuing to the ceiling (documented heights); a ½" reveal between boxes (ASSUMPTION). Material: PL-01 Uptown Walnut laminate, grain vertical (documented); in the render a warm mid-tone walnut, roughness 0.45–0.55, no gloss. Lighting: the documented small black wall luminaires (LT-04 BEGA, about 14 on the elevation, in two bands roughly 4–6 ft and 12–14 ft AFF — positions to be measured from ID302) plus, from the concept, warm 2700–3000 K grazing strips in the deeper reveals (ASSUMPTION; adds to, does not replace, the documented fixtures). Base: the wall lands on the ID303 west banquette / POR-02 plinth under run 1 and on the RB-01 base elsewhere; top: boxes die into the CA-1 ceiling with the LT-02 black track at the edge of the coffer. Composition: densest and tallest boxes behind run 1 where the stair rises, thinning toward door 101D so the door reads as a break.

**B. Stair treatment (finishes only on the frozen geometry)** — stringer plates, risers, stair soffit panels and the balcony fascia painted **charcoal-black** (CONCEPT; documented only as "painted to match" — colour is an ASSUMPTION, propose a low-sheen near-black, e.g. the PT-02 family or a custom black); **WD-01 walnut treads** with a 1" nosing (documented species; nosing ASSUMPTION); closed painted risers (documented); 42" glass shoe guard with the documented metal-panel shoe wrap in black and a 1½" round black handrail at 36" (documented sizes, colour ASSUMPTION); the ID303 tiled two-step plinth and banquette at the foot; a continuous warm light line in the balcony fascia (LT-03 documented position on the south, extended per the concept — ASSUMPTION). Implementation: thin overlay shells offset 1/16" from the frozen treads / guards, in the concept collection; the v015 objects stay untouched.

**C. Suspended light feature** — **seven** fixtures (E003 count; A212 draws six overlapping) of the LT-01 Caleo Inverse family, rendered as black rectangular rings with a 1.5" × 3" profile and an inner warm-white diffuser (form per CONCEPT; documented finish text is ambiguous — verify): sizes **3'-6", 4'-6", 5'-6" squares and 3' × 6' rectangles**, bottoms at **z 22, 23.5, 25, 26, 21, 24.5, 22.5** (all above the 19.5 balcony guard top and well clear of the stair, whose highest point is 16.0), suspended 3–7 ft from the 12'-0" panel at z 28.0, laid out in a loose overlapping cluster within x 119–130.5 × y 86–92.4 (documented panel) with the largest ring centred over the void; 3500 K documented (concept looks 3000 K — keep 3500 K unless the owner prefers warmer; ASSUMPTION either way).

**D. Flooring** — POR-01 47" × 47" (documented), joints running parallel to the grid with a full tile centred on the entry axis x ≈ 124.6 (ASSUMPTION), ⅛" warm-grey grout (width ASSUMPTION), matte "Nature" finish; WOM-01 24" × 24" walk-off inside door 101A for the full CW1 bay width × 8 ft deep (extent ASSUMPTION — ID101 shows a mat, size to be measured); POR-02 at the stair plinth and banquette base (documented); tile continues to the thresholds of 101B/101C/101D. Slab untouched.

**E. Walls / ceiling** — PT-01 First Star satin on all gypsum (documented), PT-02 metallic on the Level 2 balcony fascia and the drop soffit (documented tags); black LT-02 track at the coffer edges and black LT-04 boxes (documented); CA-1 ceiling painted PT-01; north, east and south walls kept plain so the wood wall dominates; the Clarus DP-01 glass panel on the east elevator wall (documented; treat as a plain glass panel).

**F. Lounge / FF&E** — keep the documented banquettes (south 9'-3" along the south wall west of door 101C; west 8'-7⅞" under run 1) with FAB-01 leather; add **four lounge chairs and two low tables** (CONCEPT) in the zone x 114–124 × y 80–96, leaving ≥ 6 ft clear on the 101A → 101C line (x 124.6–130) and ≥ 5 ft around the stair foot; no rug (hard floor, healthcare); **two SP-01 planters** (documented item) at the stair foot corner (x 114, y 94) and beside door 101B; artwork: one large piece on the Level 2 balcony north face (visible from below and the entry) and one by 101B (CONCEPT). No furniture in the elevator / 101B / 101C approach.

**G. Directory** — one 55" portrait display (27" × 48" active, ASSUMPTION) on the east wall at y 82.58–88.16, centred y 85.4, bottom 3'-0" AFF, in a slim black metal surround on a PT-02 accent panel 4 ft wide × 9 ft high (PROPOSED); content and branding left blank.

## 7. Conflicts, uncertainties, assumptions

1. **Are ID201–ID303 (09/29/2025) still the intent?** Revision 5 reissued ID101/ID102 only; the PowerPoint (2026-06-26) differs in details (black stair, black rectangular rings, loose furniture, directory). Owner to confirm the documented design is the base and the concept governs where the two differ.
2. **Stair colour** is not documented ("painted to match"); black is a concept-derived assumption.
3. **Wood-wall box depths, exact widths and light positions** must be measured from ID302 (¾" and 3/8" scale) before modeling; the elevation confirms the pattern, not the numbers.
4. **LT-01 finish**: the schedule row text is garbled in extraction; the fixture family (Caleo Inverse, 1.5" ring system) is clear, colour is not.
5. **Pendant hanging lengths** are "as directed by the architect" — heights above are an assumption.
6. **Walk-off mat extent, tile start point, grout width, banquette top material (SS-01 slab?)** — to measure / assume.
7. **Directory**: the concept location does not exist; the east-wall location is a proposal.
8. **Level 2 balcony north face / artwork, planter locations**: not documented.
9. The lobby floor is part of the poured core slab (A191) — no slab conflict.
10. No exterior, structural, stair, slab, glazing, door, shaft or camera change is proposed or needed.

## 8. Review viewpoints (to be added as NEW cameras later; approved cameras untouched)

| # | Purpose | Eye (x, y, z ft) | Target (x, y, z) | Lens |
| --- | --- | --- | --- | --- |
| 1 | Entrance: inside door 101A looking south-west at the stair and wood wall | (125.5, 101.5, 5.5) | (112, 80, 9) | 20 mm |
| 2 | Opposite corner: south-east corner of Level 1 looking north-west across the lounge to the stair / wall | (140.5, 75.0, 5.5) | (111, 92, 10) | 20 mm |
| 3 | Level 2 balcony looking west / down into the lobby and at the pendants | (131.0, 77.5, 21.5) | (112, 92, 8) | 20 mm |

## 9. Future model organization (not created yet)

`Building_II > INT_LOBBY_CONCEPT_A` with `ARCH_WOOD_WALL`, `ARCH_STAIR_FINISH` (overlay shells only), `ARCH_GUARDRAIL` (shoe, handrail, panel overlays), `LIGHT_DECORATIVE` (LT-01 rings), `LIGHT_FEATURE_WALL` (LT-04 boxes, reveal strips), `FINISH_FLOOR` (POR-01 plane with joints, WOM-01, POR-02 plinth), `FINISH_WALL` (PT-01/PT-02 overlays, Clarus panel), `FF&E_SEATING` (banquettes, chairs), `FF&E_TABLES`, `FF&E_PLANTERS`, `SIGNAGE_DIRECTORY` (screen hardware only), `ART_DECOR`, `CAMERAS_LOBBY` (three review cameras). Every object named `LOB_A_…`; all base-building objects stay in their frozen collections; finishes are additive shells that never edit base meshes; the build stays procedural (`build_shell_v019.py` = v015 code + one lobby block driven by a `LOBBY_CONCEPT_A` parameter dictionary: panel widths / depths / spacing / colour, light spacing / intensity / temperature, ring sizes / profile / heights, stair finish thickness, tile size / grout, furniture coordinates). Hiding `INT_LOBBY_CONCEPT_A` removes the whole concept.

## 10. Requested approvals

1. Use the documented ID design (ID201/302/303/801, A212, A500, E003) as the base and the PowerPoint as the reference that decides open items.
2. Wood wall: west wall, y 73.5–97.5, full height; box module 4/6/8/12" × ¾/1¾/3" depths (to be refined from ID302 measurements); walnut PL-01 tone; documented LT-04 boxes + concept reveal lighting.
3. Stair: charcoal-black stringers / risers / soffit / fascia, walnut treads, black shoe + 1½" black handrail, glass guards, fascia light line.
4. Seven black rectangular LT-01 rings, sizes and heights as in section 6C, 3500 K.
5. POR-01 47" tile square to grid, ⅛" grout, WOM-01 walk-off at 101A.
6. Four chairs + two tables in the zone stated, documented banquettes kept, two planters, two artworks.
7. Directory: 55" portrait on the east wall south of door 101B.
8. Three new lobby review cameras (section 8).
9. Collection plan and naming in section 9; next version = **v019**.
