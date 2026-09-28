# Comparison note — building_shell_v005 → building_shell_v006

Date: 2026-09-21
v006 = site and grading pass on the frozen v005 building. Sources, registration, grades and conflicts: `notes/site_control_v006.md` (written before the build).

## 1. Validation

| Check | Result |
| --- | --- |
| Frozen v001–v005 files (51 files: models, scripts, control and comparison notes, build reports, drawing review, photo log, all 25 renders) | SHA-256 identical before and after the v006 build: **0 changed** |
| `source_documents` | 360 files, **0 modified** |
| v005 building objects in v006 | **526 of 526 identical** — same vertex coordinates, same faces, same per-face materials (masses, parapets, openings, canopies, sun-shade, railings, yard walls, facade detail, hidden cutters) |
| Building moved? | **No.** Civil registration shows the building where the model has it, within ±0.5 ft; no placement discrepancy found |
| Removed | `Ground_flat_at_average_grade` (the flat-ground assumption) and the old `North_arrow`; the three text labels (not mesh objects) are also gone |
| Added | **50 objects, all named `Site_…`**, all in collection `09_Site_context` |
| Script control checks (205'-0" × 105'-10" face of stud, finish extents, top of parapet) | pass |
| Terrain range | 654.64 → 660.30 (−5.66 → 0.00 ft relative to FFE) |

`build_shell_v006.py` was generated from `build_shell_v005.py` by text patch: header and version, the flat-ground block removed, the site block added, one call to it, and a sixth camera. No building data or function changed. (During this pass I regenerated my own draft of `build_shell_v006.py` once before the final run; no approved file was involved.)

## 2. Site geometry added

| Object(s) | What |
| --- | --- |
| `Site_Terrain_INTERPOLATED` | 4-ft grid terrain, solid block to −10 ft; lawn, existing asphalt and landscape-bed areas shown as materials on it |
| `Site_Walk_north_west`, `…_transition_west`, `Site_Dropoff_band_west/east`, `Site_Walk_north_east`, `Site_Walk_to_BuildingI_plaza` | paver walk along the parking lot edge, dropping to the flush drop-off band in front of the entrance |
| `Site_Entry_plaza` | entry plaza between the lobby piers out to the flush curb |
| `Site_Walk_west`, `Site_Landing_door_110B`, `Site_Stair_west_9_risers_tread01–08`, `Site_Landing_west_stair_bottom` | west walk, door landing, the documented 9-riser stair down to the west street level |
| `Site_Transformer_pad`, `Site_Generator_yard_slab` | yard slabs at their documented elevations, on retained fill |
| `Site_Walk_southwest`, `Site_Landing_sw_stair_top`, `Site_Stair_southwest_7_risers_ASSUMED_tread01–06` | walk and stair at the south-west corner |
| `Site_Walk_east_door_100B`, `Site_Walk_east_door_100C`, `Site_Existing_plaza_between_buildings` | east door walks to the existing plaza |
| `Site_Parking_island_1–3` | the three nearest existing parking islands, as raised ground shapes |
| `Site_Foundation_skirt_podium` + 13 `Site_Foundation_skirt_<yard wall>` | carry the podium and yard walls below the real grade so nothing floats on the low (south, west) sides |
| `Site_North_arrow` | on the parking lot |

Sixth camera `Cam_site_oblique_NW` added; the five earlier cameras are unchanged.

## 3. Directly documented grades (W, CG-101 rev 6)

FFE 660.30 · door thresholds 660.30 · north walk 659.80, 660.08, 659.40 · entry plaza 660.27 · lobby east return 660.09 · NE corner 659.79 · NW walk 659.31, 659.09, 659.59, 659.80 · transformer pad 659.94 and 655.32 outside it · generator yard 660.18 / 659.90 · south face 657.49, 658.47, 658.50 · west stair TS 660.10 / BS 655.60, 9 risers at 6", 8 treads at 12" · south-west stair TS 660.19 / BS 656.88 · wall elevations TW 659.87 / BW 655.53, BW 656.28, TW 659.71 / BW 656.98, BW 656.44, retaining wall top 663.63 · 6" curb, flush along the 97.16-ft drop-off transition.
Read visually from the sheet (V): the "EX:" spots (658.81, 658.70, 659.80, 660.14 ×3, 659.77, 659.72, 660.04, 655.47, 656.37 and the west-street gutter 654.60–655.11).

## 4. Interpolated — not exact

- **The whole terrain surface** between the spots (inverse-distance interpolation through the spots, contour label positions and walk edges). Contours were used only at their label positions, not traced.
- Parking lot and drive surface; street edges to the west and south; lawn slopes on the south and west sides.
- Walk surfaces between written spots (straight-line between them); walk-slope percentages quoted in the control document are derived, not printed.
- Asphalt edge set 6" below the walk where the curb is not flush.
- All plan outlines are digitized from CS-101 (±1 ft) on a ±0.5 ft registration; the asphalt/lawn boundary is stepped at the 4-ft grid.

## 5. Assumptions

South-west stair riser count (7) · island height 6" · foundation-skirt depth · retained-fill slabs carried down to −8 ft · plain steps without cheek walls or handrails · representational colors for asphalt, lawn, beds and concrete; paver colors approximate the names on CS-101 (Techo-Bloc Linea "Shale Gray", Westmount "Onyx").

## 6. Unresolved civil / architectural conflicts

1. **C-1 Transformer enclosure is 2.2 ft further west on civil rev 6 (03.10.26) than on A112/A012 Rev 5 (02/27/26).** Kept at the architectural (frozen) position.
2. **C-2 South-west low wall height:** A012 +2'-8" (662.97) vs CG-101 TW 659.71. Kept at the architectural height.
3. **C-3 Drop-off canopy outline** on CS-101 (about 88 × 24 ft, further north-west) vs A700/S132 (65'-7 1/4" × 23'-3"). Architectural kept.
4. **C-6 Transformer gate vs. grade:** about 4.6 ft drop at the west (gate) side of the enclosure on CG-101.
5. C-4 civil building outline 0.3–0.6 ft smaller than the architectural finish face (inside tolerance); U-6 CS-101 revision-label inconsistency; V-1 architectural revisions 6–10 not in hand.

Not modeled: planting, trees, signage, bollards, bike racks, lights, handrails, cheek walls, striping, accessible-ramp detail, curb-and-gutter profile, storm structures, Building I, streets' curbs and on-street parking (by others).
