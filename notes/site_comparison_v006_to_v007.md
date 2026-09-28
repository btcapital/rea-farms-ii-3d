# Site comparison — building_shell_v006 → building_shell_v007

Date: 2026-09-21
Basis: `notes/site_coordination_review_v007.md`.

## Validation

| Check | Result |
| --- | --- |
| Frozen v001–v006 files (62 files: models, scripts, all notes, build reports, all 31 renders) | SHA-256 identical before and after: **0 changed** |
| `source_documents` | 360 files, **0 modified** |
| Objects | v006 576 → v007 577 mesh objects; none removed |
| Identical to v006 (same vertex coordinates) | **574** — the entire building, facade detail, yard walls, canopies, every walk, stair, slab, island and foundation skirt |
| Changed | **2**: `Site_Transformer_pad`, `Site_Terrain_INTERPOLATED` |
| Added | **1**: `Site_Retained_fill_southwest` |
| Terrain | 5,152 vertices; **30 changed**, all within x −26 → −10, y 72 → 92 (the enclosure footprint). Every other terrain vertex is identical to v006 |
| Building moved / enclosure walls moved | No |
| Cameras, lighting, materials | unchanged; same six views |

## What changed and why

| Object | v006 | v007 | Source |
| --- | --- | --- | --- |
| `Site_Transformer_pad` | top at 659.94 (−0.36 ft) | top at **655.32** (−4.98 ft) | CG-101 rev 6 spot 655.32 at the gate; S141 Rev 5 elevation CMU-5: 9'-4" walls and full-height gate from −6'-0"; A302. The 659.94 spot belongs to the walk east of the wall (v006 misreading) |
| `Site_Terrain_INTERPOLATED` | ground inside the enclosure at about −0.8 ft | 12 interior vertices set to the pad level; 24 vertices on the four bounding grid lines shifted horizontally by up to 3 ft so the step in the ground falls **inside the wall thickness** and is hidden by the frozen walls and their skirts | same |
| `Site_Retained_fill_southwest` (new) | — (ground inside the low wall had been interpolated down to street level) | retained fill, top at **659.71** (−0.59 ft), in the triangle between the diagonal low wall, the generator enclosure and the south-west walk | A012 Rev 5 section B2 (retaining condition); CG-101 "TW 659.71" = high-side grade |

The interpolation control set was deliberately kept exactly as in v006, so that nothing outside the enclosure footprint moved. (A first attempt that re-interpolated the terrain changed 419 vertices across the west side and the parking islands; I discarded that draft and rebuilt. No approved file was involved.)

## Not changed

Transformer enclosure position (Target 1: architectural/structural position confirmed). South-west low wall height (Target 2: +2'-8" confirmed). No gate, steps, ramp or landing added (Target 3: none are documented or needed).

## Remaining measured / assumed values in these two changes

Pad modeled flat at the single written gate elevation (final pad by Duke Energy) · retained fill modeled flat at 659.71 (the civil shows 659.71 at the wall and 659.90 at the generator enclosure; the slight fall between them is not modeled) · fill outline from the v005 wall positions.
