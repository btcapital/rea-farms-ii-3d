# Comparison — building_shell_v015 → building_shell_v019 (main lobby Concept A, Pass 1 architectural)

Date: 2026-09-22 · Basis: `notes/lobby_concept_control_v019.md` (written before modeling) and the owner-approved `notes/lobby_concept_fit_analysis_2026-09-22.md`. Pass 2 (loose FF&E, artwork, planters, directory detailing, final tuning) is **not** included and awaits approval of these renders.

## Validation

| Check | Result |
| --- | --- |
| Frozen files (350: v001–v018 models, scripts, notes, renders, exports, three viewers, tenant PDF, the concept PowerPoint) | SHA-256 identical before and after: **0 changed** |
| `models/building_shell_v015.blend` | unchanged (in the frozen set); no approved model overwritten; v019 is a new file |
| `source_documents` | `Building II` 360 files unchanged; `Building I` not opened (aggregate 1,231 files / 6,929,037,544 bytes unchanged); `concept_design\Rea_Farms_2_Lobby.pptx` hash unchanged |
| v015 objects inside v019 | **2,109 of 2,109 identical** (geometry, collection, materials, visibility flags); none removed; no v015 collection changed its object count |
| Stair 1 geometry (56 v014 tread / landing / guard objects) | **56 / 56 identical — the stair did not move** |
| Exterior (673 objects: masses, parapets, openings, inside shell, glass, canopies, sun-shade, facade detail) | **673 / 673 identical** |
| Structure / core (130 objects: columns, core walls, elevator, shafts, slabs, ceilings, terrace) | **130 / 130 identical** |
| Approved cameras | all identical; 3 new `Cam_lobby_A_*` cameras added |
| New objects | **571**, every one named `LOB_A_…` (or `Cam_lobby_A_…`) and inside `Building_II > INT_LOBBY_CONCEPT_A`: 504 meshes, 64 point lights, 3 cameras |

`build_shell_v019.py` = `build_shell_v015.py` + one `LOBBY_A` parameter block, the documented box list, and `build_lobby_concept_a()`; hiding or deleting `INT_LOBBY_CONCEPT_A` removes the whole concept. The tenant room schedule is re-written as `…_v019.json` (byte-identical to the v015 file, required by the script's no-overwrite rule).

## What was modeled (Pass 1) and what controlled it

| Collection | Objects | Content | Controlling source |
| --- | --- | --- | --- |
| ARCH_WOOD_WALL | 51 | laminate field 19.45 ft × 28.95 ft on the west wall (y 73.41–92.86) + **50 protruding box pieces** exactly as drawn on ID302 A6 (6 / 8 / 6 / 4 / 4 / 8" widths in a 36.5" group, staggered lengths, 2.4" deep) | ID201 B2 extent (W/M), ID302 A6 pieces (M ±⅛"), ID302 B4 depth (M), ID801 PL-01 walnut vertical grain (W) |
| LIGHT_FEATURE_WALL | 192 | **64 BEGA 33590 wall cylinders** (3" × 5⅛" × 3¾") with a warm lens and a 3500 K point light each, at the elevation's positions (10 per group) | E003 / RV-001319-001 WLC × 64 3500 K (W); ID801 LT-04 size (W); positions ID302 A6 (M ±3") |
| ARCH_STAIR_FINISH | 59 | walnut tread caps with 1" nosing on all 26 treads and the landing; dark risers; dark 1" × 14" stringer plates on the open sides; dark soffit wedges; landing fascia and soffit | A500 wood treads, painted risers / stringers, metal-panel soffit (W); WD-01 walnut (W); **dark charcoal colour = design choice (C)**, supported by the 2025 concept note "stair framing gunmetal" |
| ARCH_GUARDRAIL | 11 | black glass shoes on both runs and on the three Level 2 guard lines, 1½" handrails at 36" (glass side and wall side), Level 2 guard caps | A500 shoe glass guardrail, 1½" O.D. handrail (W); profiles A |
| LIGHT_DECORATIVE | 127 | ceiling coffer (12'-6" step and 12'-0" inner panel), black LT-02 track with a warm slot on the coffer edges, **7 SH1 ring pendants** (3'-6" to 6'-0", 1.5" × 2" black tube, warm inner emitters, cables, canopies) at bottoms 21–26 ft | A212 Rev 5 coffer (W/M); E003 / RV SH1 Lightnet Caleo Inverse × 7 3500 K (W); ID801 LT-02 (W); sizes, stagger, black frame **C/A** |
| FINISH_FLOOR | 90 | 88 POR-01 47" × 47" tiles with ⅛" warm-gray grout on the entry axis, grout bed, WOM-01 walk-off 14 × 8 ft inside door 101A | ID801 POR-01 (W), ID101 WOM-01 (W); grout / origin / walk-off extent A |
| FF&E_SEATING | 4 | POR-02 plinths (1'-1¾" × 1'-10") and FAB-01 leather seats: west banquette 8'-7⅞" under run 1, south banquette 9'-3" | ID303 (W); cushion 4" A |
| FINISH_WALL | 30 | PT-01 overlays on all lobby gypsum (both levels), PT-02 metallic on the Level 2 balcony fascia, RB-01 base at the directory wall, coffer planes | ID801 PT-01 / PT-02 / RB-01 (W), ID201 tags (W); RGB values A |
| SIGNAGE_DIRECTORY | 4 | 75" portrait display massing (38.4" × 66.3" × 2.8"), Chief mount, bezel, PT-02 accent panel; screen blank | XL Media approved quote 8/10/2026 (W); location owner-approved; height A |
| CAMERAS_LOBBY | 3 | entrance (inside door 101A looking SW), east wall by door 101B looking W, Level 2 balcony looking NW | owner-approved viewpoints |

## Design assumptions (all in the `LOBBY_A` block)
Stair dark-metal colour, roughness and metallic value · 1" nosing · walnut tone · 4" cushion · ring sizes / heights / black frame · WLC and ring render intensities · LT-02 slot emission · ⅛" grout, tile origin on the entry axis, walk-off extent · directory bottom at 2'-6" · PT-01 / PT-02 RGB · FAB-01 colour · **soffit drawn as a solid wedge** and the stringer reading about 18" deep, because the frozen v014 tread blocks are 10.8" thick simplifications (the documented plates are 14") · handrail brackets omitted · the ID303 two-step tile platform omitted (location ambiguous) · the PT-02 rectangle that ID201 draws behind the landing is **not** applied over the wood boxes (ID302 draws boxes there; conflict recorded).

## Dimensional checks (from the build report)
Wood wall 19.45 × 28.95 ft, boxes project 3.15" from the gypsum · wood wall ends 4.70 ft south of door 101D · all 7 rings inside the documented 11'-6" × 6'-6¾" panel; clearance above the stair top 5.0–9.0 ft, above the Level 2 guard top 1.5–6.5 ft; none over Level 2 floor · directory projects 5.8", 1.11 ft clear of door 101B, within the 5.58 ft wall segment · south banquette ends 10.8 ft west of the door 101C path · 3.1 ft headroom over the west banquette under run 1 · 101A → 101C path unobstructed.

## Collisions / interferences found
None between new objects and the frozen stair, guards, columns, elevator, doors or glazing. Overlay shells intentionally overlap the frozen tread blocks and wall faces by ≤ ⅛" (additive finishes). Two documentation conflicts are recorded, not resolved: the ID201 PT-02 panel vs the ID302 boxes behind the landing; and the Modern Forms "Chaos" cut sheet (6/5/2026) vs the permit revision's SH1 × 7 (6/18/2026, controlling).

## Renders (`renders/`, 256 samples, 2400 × 1350, RTX A1000)
`building_shell_v019_lobby_A_01_entrance.png` (165 s) · `building_shell_v019_lobby_A_02_level1_corner.png` (155 s) · `building_shell_v019_lobby_A_03_level2_overlook.png` (157 s). Model file 2.8 MB → 3.1 MB.
