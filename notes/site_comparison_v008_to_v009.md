# Site comparison — building_shell_v008 → building_shell_v009

Date: 2026-09-21
Basis: `notes/site_landscape_coordination_v009.md` (written before the build).

## Validation

| Check | Result |
| --- | --- |
| Frozen v001–v008 files (85 files: models, scripts, all notes, build reports, all 44 renders) | SHA-256 identical before and after: **0 changed** |
| `source_documents` | 360 files, **0 modified** |
| Objects | v008 924 → v009 925 mesh objects |
| Identical to v008 (same vertex coordinates) | **892** — the whole building, facade detail, yard, terrain, every other walk / stair / slab / fill / skirt, and all planting except the west seasonal group |
| Terrain | identical (v007 interpolation inputs and under-slab outlines kept on purpose) |
| Building moved | no |

## Exactly which objects changed

| Object | Change | Source |
| --- | --- | --- |
| `Site_Walk_north_transition_west` | **removed** (straight-edged wedge, a v006 simplification) | — |
| `Site_Walk_entrance_curve_west` | **new** — walk follows the documented S-curve: outer edge (61.6, 123.4) → (69.5, 119.1) → (78.3, 114.4); inner R10.50' edge (63.7, 115.2) → (70.0, 109.4) → (78.3, 107.4) | CS-101 rev 6 03.10.26 and LP-101 (approved 1/9/2026) vector linework, agreeing within 0.5 ft; R10.50' written |
| `Site_Dropoff_band_west` | **reshaped** — was a rectangle x 62 → 108.3 against the building; now x 78.3 → 108.3 with its building-side edge at y = 107.35 (8.50 ft band, written) and the door-100A landing (x 80.1 → 88.3) running to the building. North edge and the joint with the unchanged entry plaza are as before | same |
| `Site_Entrance_bed_fill_west` | **new** — ground (mulch surface) for the documented planting bed between the curve and the building | LP-101 bed; CS-101 |
| `Site_Building_base_strip_UNRES` | **new** — 1.05 ft strip against the building east of door 100A, at walk level, **neutral placeholder** (surface not labelled on any sheet) | CS-101 edge line at y = 107.35 |
| `LAND_Bed_mulch_seasonal_west_OVER_V007_PAVING` | **removed** (superseded by the bed fill) | — |
| `LAND_SEAS_…` — the **29 west seasonal annuals** | **re-packed** inside the documented bed, clear of the corrected walk and of the camellia. Quantity (29) and 12" spacing unchanged. Their positions were and remain interpreted | LP-101 "(29) SEAS" |

Not changed: the camellia at (63.5, 109.5) (already inside the documented bed), the east seasonal group (34), every other plant, the entry plaza, the east band, the parking-lot walk, the curb treatment, the CW2-bay planter patch.

New-surface elevations come from the unchanged v007 interpolation, so the new shapes meet their unchanged neighbours without a step.

## Remaining simplifications at the entrance (not guessed)

- A sliver of lawn-colored terrain shows along the outside of the new curve, because the asphalt area on the (unchanged) terrain still follows the old straight chord; up to about 0.5 ft wide. Left alone to keep the terrain identical.
- The 1.5 ft flush-curb strip is still part of the paving band, as in v007.
- Strip material and CW2-bay planter height are unresolved; the Rev 5 "pavers at entrance" landscape clarification sheet is not in the folder.

## Renders

`renders/building_shell_v009_front_north.png`, `…_landscape_oblique_north.png`, `…_site_oblique_northwest.png` (the three views requested; cameras and neutral daylight unchanged).
