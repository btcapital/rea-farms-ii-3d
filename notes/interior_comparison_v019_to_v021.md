# Comparison — building_shell_v019 → building_shell_v021 (Lobby Concept A, Pass 2)

Date: 2026-09-22 · Basis: `notes/lobby_pass2_control_v021.md`. v021 = v019 rebuilt by the identical code + Pass 2 additions.

## Object-level diff (Blender fingerprints: world-space vertices, faces, collections, materials, flags, properties)

| Check | Result |
| --- | --- |
| v019 objects | 2,680; **2,616 identical** in v021, 0 removed |
| Changed v019 objects | **64**, all `LOB_A_WLC_nn_point` lights: energy 0.9 → 0.7 W (lighting polish; colour unchanged). No mesh, camera or empty changed |
| Changed v019 materials | **1**: `LOB_A_WLC_lens_3500K` emission strength 0.55 → 0.40. No other material changed |
| Stair 1 (frozen v014 + v019 finishes), wood wall, pendants, guards, directory massing | **identical** |
| New objects | **117**, all `LOB_A_P2_*`: FF&E_SEATING 68 (4 chairs × 17 parts), FINISH_WALL 20 (19 DP-01 panels + TR-05 trim), FF&E_PLANTERS 18, FF&E_TABLES 6, ART_DECOR 4, SIGNAGE_DIRECTORY 1 |
| New materials | 13 `LOB_A_P2_*` |
| Collections | only the six lobby sub-collections above gained objects; no collection added or removed |
| Tenant room schedule v021 | byte-identical to v015 |
| Frozen files | all 333 Building II files of v001–v020 SHA-256 identical (the `Building_I` folders belong to a separate session and were not touched) |
| Source documents | not modified (read-only inspection of ID101, ID201, ID301, ID303, ID801, concept PowerPoint) |

## Renders (`renders/`, 256 samples, 2400 × 1350)
`building_shell_v021_lobby_A_01_entrance.png` · `_02_level1_corner.png` · `_03_level2_overlook.png` — same three approved cameras as v019; render times about 3.9 / 2.9 / 3.4 min. Model file 3.10 MB → 4.05 MB.

## What to look for versus v019
Wall cylinders now read as warm points · four wood-frame lounge chairs and two round tables on the entry axis (as drawn on ID101) · SP-01 planters at the north end of the east wall and by door 101D · abstract canvases on the Level 2 west wall and by door 101B · the elevator block's lobby faces clad in pale-blue DP-01 glass with a stainless corner trim · the 75-inch display shows a neutral directory graphic (no names).
