# Comparison — building_shell_v021 → building_shell_v023 (lobby visual-refinement pass)

Date: 2026-09-23 · Basis: `notes/lobby_refinement_control_v023.md`. v023 = v021 rebuilt by the identical code + the v023 refinement layer (materials, lights, Pass 2 object forms, fill lights, temporary camera). Blender fingerprints compared: world-space vertices and faces, location, collections, materials, visibility, custom properties, light and camera data.

## Architecture check (v019 geometry)
| Check | Result |
| --- | --- |
| Non-lobby v019 objects (shell, structure, core, stairs, slabs, glazing, site, landscape, tenant concept) | **2,109 of 2,109 identical** |
| Frozen lobby list: Stair 1 (v014 treads / landing / guards + v019 finishes), wood wall field + 50 boxes, Level 2 guards and shoes, banquettes and plinths, POR-01 tiles, coffer and track, directory massing and graphic, DP-01 panels | **311 of 311 identical** |
| Pendant ring tubes (28) | geometry identical (a 4 mm bevel modifier was added; material assignment unchanged) |
| Wall-fixture bodies (64 `LOB_A_WLC_nn_BEGA_33590`) | geometry identical |
| v019 mesh objects with changed geometry | 92 = 64 WLC lens emitters (re-shaped to a ⅜ in. base slot) + 28 pendant cables (0.19 in. → 1⁄16 in.). Nothing else |

## Everything v023 modified relative to v021
| Kind | Count | Change |
| --- | --- | --- |
| WLC lights | 64 | POINT 0.7 W → SPOT 1.8 W, 105°, blend 0.95; moved 0.08 ft to the fixture base and aimed down the wall |
| WLC lens emitters | 64 | geometry (base slot) and strength 0.40 → 1.4 |
| Pendant cables | 28 | thinner; new material `LOB_A_V23_cable_dark` |
| Pendant ring tubes | 28 | bevel modifier only |
| Lounge chairs | 4 chairs: 44 v021 parts removed, 32 new parts, 24 parts re-shaped | refined form; centres and 2.2 × 2.3 ft footprint unchanged (the raked back-rest top leans 1.4 in. beyond the rear edge at 2'-9" height) |
| Tables | 6 | thinner top, slimmer pedestal, smaller base (positions unchanged) |
| Plants | 14 v021 objects removed (2 trunks + 12 spheres), 4 new (2 branch meshes + 2 leaf meshes) | planters, soil unchanged |
| Materials changed (11) | `LOB_A_black_fixture`, `LOB_A_dark_metal_PT-02_gunmetal`, `LOB_A_FAB-01_leather`, `LOB_A_P2_chair_cushion_fabric`, `LOB_A_P2_plant_foliage`, `LOB_A_PL-01_walnut_laminate`, `LOB_A_POR-01_Santorini_Gray_47in`, `LOB_A_PT-01_SW7646_First_Star`, `LOB_A_PT-02_Scuffmaster_metal`, `LOB_A_SH1_ring_emitter_3500K`, `LOB_A_WLC_lens_3500K` | values in the control note; finish identities unchanged |
| Materials new (1) | `LOB_A_V23_cable_dark` | |
| Art images | 2 regenerated (landscape-inspired) | canvas objects unchanged |
| Objects added (3) | `LOB_A_V23_fill_daylight_CW1`, `LOB_A_V23_fill_ceiling_soft` (area lights, hidden in the saved file), `Cam_lobby_A_04_seating` (temporary) | |
| Totals | v021 2,797 objects → v023 2,778 (2,553 identical, 186 changed, 58 removed, 39 new) | |

## Before / after lighting values
WLC light 0.7 W omni → 1.8 W spot (105°) · WLC emitter 0.40 (full face) → 1.4 (⅜ in. slot) · SH1 ring emitter 9.0 → 4.2, colour 1.0/0.84/0.66 → 1.0/0.86/0.68 · exposure 0.45 → 0.55 · fill lights added: 115 W cool daylight panel inside the curtain wall, 90 W warm-neutral panel under the coffer · sun 7.0 and sky 0.16 unchanged · view transform AgX unchanged.

## Circulation
Unchanged from v021: chairs 5.63 ft from the run 1 guard line, 4.29 ft from the walk-off, 7.58 ft from the south banquette, 2.2 ft between facing chairs, east chairs 0.97 ft over the entry axis as drawn; planter 1 5.13 ft from door 101B, planter 2 1.88 ft from door 101D and 1.36 ft from the wood-wall end; elevator approach 10.2 ft clear; directory 1.11 ft from door 101B. Viewer navigation files (v020, v022) untouched.

## Manifest
All 365 Building II files of v001–v022 (models, scripts, notes, renders, exports, viewers v016–v022, tenant PDF, concept PowerPoint) SHA-256 identical before and after the build; source documents: Building II 360 files identical, Building I aggregate identical (not opened), PowerPoint hash unchanged. v019, v020, v021 and v022 hashes match the snapshot.

## Renders
`renders/building_shell_v023_lobby_A_01_entrance.png`, `_02_level1_corner.png`, `_03_level2_overlook.png`, `_04_seating.png` (256 samples, 2400 × 1350; 181 / 174 / 172 / 172 s). Model file 4.05 MB → 6.51 MB (packed art images and plant meshes).
