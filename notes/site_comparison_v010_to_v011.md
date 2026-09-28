# Comparison — building_shell_v010 → building_shell_v011 (context-only pass)

Date: 2026-09-21
Basis: `notes/context_control_v011.md` (written before the build).

## Validation

| Check | Result |
| --- | --- |
| Frozen v001–v010 files (107 files: models, scripts, all versioned notes, build reports, all 53 renders) | SHA-256 identical before and after: **0 changed** |
| `source_documents` | 360 files, **0 modified** |
| v010 mesh objects in v011 | **929 of 929 with identical vertex coordinates and identical per-face material assignment** |
| Cameras | all identical to v010 (position, rotation, lens, shift) |
| Sun, sky strength, exposure | identical to v010 (sun strength 7, sky 0.16, exposure −0.35) |
| Removed | none |
| Added | **357 objects, all in the new collection `14_Context_v011`**, all named `CTX_…` with their confidence class in the name. Deleting the collection returns exactly v010 |
| Signage, branding, people, vehicles, interiors, street furniture | none |

`build_shell_v011.py` = `build_shell_v010.py` + the context block and one call to it. (One low-resolution trial was run in a scratch folder; the script was regenerated once after reducing the context tree sizes. No approved file was involved.)

## Context added

| Group | Objects | Class |
| --- | ---: | --- |
| Building I plain mass + lighter upper band | 2 | footprint **measured** from CS-101 rev 6 (±2 ft, corners squared, bays/canopies omitted); FFE 661.75 **exact**; 34 ft height and the two material tones **approximate** from photos |
| Parking islands in the north lot (three more rows, both halves) | 18 | **measured** ±3 ft, uniform size |
| East half of the parking lot; paved ground around Building I | 2 | **simplified** to single flat surfaces |
| Perimeter lawn band, north and south sidewalks | 3 | **simplified** |
| Golf Links Dr, North Rea Park Ln, Terminus Rd, Midway Park Dr | 4 | **simplified** flat bands at the documented right-of-way positions and widths; no curbs, markings or parking bays |
| Lawn beyond Golf Links Dr; open park lawn to the south | 2 | **approximate** (photos) |
| Street trees along North Rea Park Ln | 14 (+14 trunks) | first 7 positions **measured** on LP-101, rest continued at the same spacing; size **approximate** (about 12 ft, young, as in the photos) |
| Existing trees in the three nearest islands | 3 (+3 trunks) | position **measured** on LP-101; size **approximate** |
| Distant buildings with roofs (apartments south, houses west/east) | 12 | **approximate** from the drone photos — plain boxes for horizon scale only |
| Wooded horizon | 280 | **approximate** |

All context ground is flat, resting on the v010 backdrop slabs; grades outside the modeled site are not documented.

## Effect on realism

- **Glass: improved.** The curtain walls and storefronts now reflect a tree line, the parking-lot trees and ground instead of a blank horizon; the close-up and north-west corner views show it most clearly.
- **Horizon and scale: improved** — Building I closes the east side, distant buildings and trees break the skyline, the parking islands and young trees give the forecourt scale.
- Reflections are still simple: the reflected trees are low-detail silhouettes and there are no vehicles, light poles or neighbouring facades with detail.

## What remains missing

Vehicles and people (excluded for now) · light poles, bollards, bike racks, striping, curbs on the streets · Building I's real facades, canopies and plaza · real grades outside the site · detailed trees (context trees are rounded canopies on trunks) · interiors · the grey placeholder finishes and approximate named colors on Building II · everything listed under "known realism limits" in `presentation_control_v010.md`.

## Renders (`renders/`)

`building_shell_v011_hero_front_north.png` · `…_entrance_oblique_northeast.png` · `…_rear_oblique_southeast.png` · `…_elevated_site_oblique_northwest.png` · `…_facade_material_closeup.png` · `…_corner_northwest_eye_level.png` — same cameras, light, exposure and render settings as v010 (Cycles, OptiX, 256 samples, denoised).
