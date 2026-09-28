# Lobby Concept A — Pass 2 control document v021 (loose FF&E, planters, artwork, directory graphic, DP-01 cladding, polish)

Date: 2026-09-22 · Applies to: `scripts/build_shell_v021.py` → `models/building_shell_v021.blend` · Baseline: **v019 approved** (architectural lobby) and **viewer v020 approved** (navigation). v021 = v019 rebuilt by the identical code **plus** objects named `LOB_A_P2_*` placed in the existing sub-collections of `Building_II > INT_LOBBY_CONCEPT_A`. The only change to a v019 value is the render intensity of the 64 wall cylinders (light energy 0.9 → 0.7 W, emitter strength 0.55 → 0.40; a lighting-polish item, no geometry). Stair 1, the wood wall, the pendants, the directory massing and the viewer collision are untouched.

Codes: **W** written · **M** measured from the sealed drawings · **C** concept (`Rea_Farms_2_Lobby.pptx`, aesthetic reference only) · **A** assumption / design choice.

## 1. Document check for Pass 2 items (what the permit set actually says)

| Item | Finding | Effect on v021 |
| --- | --- | --- |
| Lounge furniture | **ID101 Level 01 finish plan draws four lounge chairs in two facing pairs with two small round tables between them**, east of Stair 1 run 1 on the entry axis (1/8" plan; positions M ±0.5 ft). ID801 has no furniture line item; chair / table type is not specified | chairs and tables modeled at the drawn positions; form and finish from the concept (wood-frame lounge chair, light cushions, small dark round tables) |
| SP-01 planter | ID801 **SP-01 Florence Gray Silver Speck 4C06D-05, 17" × 23¼" × 17½"** (W); **ID201 A2 east elevation draws one SP-01 at the north end of the east wall** (M ±1 ft) | planter 1 at the north end of the east wall (x 141.55, y 100.6); planter 2 by the wood-wall end / door 101D (C, the concept shows a planter by the door); plants = simplified massing (A) |
| Artwork | not documented; the concept shows a canvas on the balcony back wall and one beside the right-hand door | A1 6 × 4 ft on the Level 2 west wall north of the wood wall (seen across the void from the entry); A2 2 × 3.5 ft on the east wall north of door 101B; generated neutral abstract images (no text) |
| Directory | ID301 C2 "TV inset detail" + **ID201 B1 south elevation: a 55" TV inset, centred (EQ / EQ), on the elevator block's north face behind the DP-01 glass**; XL Media quote (8/10/2026, approved) upgrades the display to a 75" Panasonic portrait monitor | **the approved v019 location (east wall south of door 101B) is kept**; a neutral graphic (header band, accent rule, blank rows; no tenant names, no building name) is added on the approved screen. **Relocation to the documented elevator-block face is a decision for the owner** (section 5) |
| DP-01 | ID801 **DP-01 Clarus wall-to-wall CBC-201** (W); **ID101 tags DP-01 on the elevator block's lobby faces; ID201 B1 / A2 tag it; ID301 B4 "East elevator wall Clarus system" shows 6'-0" tiers with TR-05 trims** | modeled on the elevator block's west face (x 135.75, both levels, around the elevator doors) and north face (y 82.58), 6 ft tiers (W), ⅛" reveals (A), ½" glass proud of the face (A), pale blue back-painted colour (C, consistent with the concept's pale-blue pier), TR-05 brushed stainless corner trim (W) |
| Walk-off mat | ID101 draws WOM-01 about 20 × 5 ft across the entry; v019 modeled 14 × 8 ft (A) | **not changed** (approved architecture); recorded for a later revision |
| South step platform | ID303 B3 two-step tile platform | still not modeled (location ambiguous) |

## 2. Objects added (91, all `LOB_A_P2_*`, custom property `pass = 2`)

| Sub-collection | Added | Content |
| --- | --- | --- |
| FF&E_SEATING | 4 chairs × 12 parts | wood frame (legs, rails, posts, arms) + seat and back cushions; centres (119.9, 89.7) facing E, (124.4, 89.7) facing W, (119.9, 83.4) E, (124.4, 83.4) W; 2.2 × 2.3 ft, seat 1'-4", arm 2'-0¾", back 2'-9" |
| FF&E_TABLES | 2 × 3 parts | round side tables Ø 1'-4", 1'-6" high at (122.1, 89.7) and (122.1, 83.4) |
| FF&E_PLANTERS | 2 × (planter, soil, trunk, 6 foliage spheres) | SP-01 size (W), tapered (A); plants about 3½ ft above the pot (A) |
| ART_DECOR | 2 × (frame, canvas) | A1 Level 2 west wall y 95.5–101.5, z 19–23; A2 Level 1 east wall y 95–97, z 4.5–8 |
| SIGNAGE_DIRECTORY | 1 | neutral graphic plane 1 mm in front of the approved 75" screen (emissive, "screen on") |
| FINISH_WALL | 19 DP-01 panels + 1 TR-05 trim | elevator block west face (3 columns, door openings kept clear at both levels) and north face, tiers 0.5–6.5–12.5–18.5–24.5–28.95 ft |

## 3. Clearances (from the build report)
Chairs 5.63 ft clear of the run 1 guard line · 4.29 ft clear of the walk-off mat · 7.58 ft clear of the south banquette · 2.2 ft between facing chairs (table between) · east chairs cross the door 101A axis by 0.97 ft (as drawn on ID101) · planter 1: 5.13 ft from the door 101B jamb, 1.76 ft from the north wall · planter 2: 1.36 ft from the wood-wall end, 1.88 ft from door 101D · A2 0.26 / 0.29 ft from the door head and the east return · DP-01 projects 0.054 ft (⅝") from the block faces.

## 4. Materials / lighting polish (render)
WLC cylinders dimmed (see top) so they read as warm points instead of white rectangles · new materials: chair frame walnut (A, relates to PL-01), cushion fabric warm off-white (C/A), table dark bronze (C/A), SP-01 grey speck (W tone A), soil, trunk, foliage (A), art frame black (A), generated art images (A), neutral directory graphic (A), DP-01 pale-blue back-painted glass (C/A), TR-05 brushed stainless (W). No v019 material was edited.

## 5. Decisions for the owner
1. **Display location.** The permit set (ID201 B1, ID301 C2 / B4) puts the lobby display centred on the elevator block's north face, behind the DP-01 glass, facing the entrance. v019 (approved) has it on the east wall south of door 101B. Recommendation: relocate the 75" display to the documented elevator-block face (a v023 change if approved). v021 keeps the approved location and adds the neutral graphic there.
2. **Chair / table product and finish** are not specified in the documents; the concept's wood-frame armchairs with light cushions were used.
3. **Second planter and both artworks** are concept-derived placements.
4. **Walk-off mat extent** on ID101 differs from the v019 assumption (about 20 × 5 ft vs 14 × 8 ft).

## 6. Viewer
Viewer **v022** (`viewer_v022/`, port 8022) = the approved v020 viewer unchanged, showing the v021 export `exports/building_II_model_v021_viewer_v022.glb`. Pass 2 objects are **not** collision blockers; the export asserts that all three walk grids and the Stair 1 navigation surface are byte-identical to viewer v020's. See `notes/browser_viewer_control_v022.md`.
