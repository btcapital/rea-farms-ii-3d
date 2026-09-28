# Site comparison — building_shell_v007 → building_shell_v008

Date: 2026-09-21
v008 = landscape pass on the frozen v007 baseline. Sources, schedule, interpretation flags and conflicts: `notes/landscape_control_v008.md` (written before the final build).

## Validation

| Check | Result |
| --- | --- |
| Frozen v001–v007 files (73 files: models, scripts, all notes, build reports, all 37 renders) | SHA-256 identical before and after: **0 changed** |
| `source_documents` | 360 files, **0 modified** |
| v007 objects in v008 | **577 of 577 identical** (same vertex coordinates) — building, facade detail, yard walls, terrain, walks, stairs, slabs, fill, skirts |
| Removed / changed | none |
| Added | **347 mesh objects, all in the new collection `12_Landscape_v008`**, all named `LAND_…`. Deleting that collection returns exactly v007 |
| Nothing moved to make planting fit | confirmed — curbs, walks, walls, grades, utility areas and building untouched |
| Cameras / lighting | the six v007 cameras unchanged; one added (`Cam_landscape_oblique_N`); same neutral daylight |

`build_shell_v008.py` was generated from `build_shell_v007.py` by text patch: header and version, the landscape data/function block, one call to it at the end of the site function, and the seventh camera. (One earlier draft of the script failed on a too-small interpreted groundcover region and was regenerated; no approved file was involved.)

## What was added

| Group | Count | Basis |
| --- | ---: | --- |
| DAZA azalea | 28 | positions measured from LP-101 symbols |
| ILST holly | 6 | 4 measured from symbols, 2 measured from the raster (±1 ft) |
| GATE camellia | 2 | measured |
| JEWL distylium | 8 | measured |
| JADE distylium | 17 | measured |
| FOAR forsythia | 8 | measured |
| SANJ osmanthus (tree form) + trunk | 1 (+1 trunk object) | measured |
| RHCO azalea | 10 | **interpreted** positions (5' o.c. in the documented gaps) |
| OSOR rose | 11 | **interpreted** rows (3 in the CW2 planter, 8 in the north-east bed) |
| CORA coral bells | 24 | **interpreted** front row, south strip |
| CATM catmint | 37 | **interpreted** front row, south strip |
| COZA 27, CARE 69, SEAS 63, JUNE 28 | 187 | quantities and spacing written; **regions interpreted** from the LP-101 hatches |
| Mulch bed patches | 5 | interpreted outlines |
| Lawn patches | 2 | interpreted outlines |

Quantities match the LP-101 **plan callouts** exactly. Installed heights follow the schedule where given (15", 18", 12", 36", 8 ft).

## Directly documented vs. interpreted

- **Written (schedule / callouts):** every species, quantity per callout, container size, caliper, minimum height, on-centre spacing.
- **Measured from the drawing:** positions of 70 individually drawn shrubs and the tree.
- **Interpreted:** positions of RHCO, OSOR, CORA, CATM; all groundcover region shapes; bed and lawn patch outlines; every proxy's spread, groundcover heights, and all colors (representational only).
- **Not given anywhere:** mulch type, edging, sod type, mature sizes.

## Conflicts / unresolved (nothing moved)

1. **L-1** Schedule totals exceed located callouts: CATM 57 vs 37, CORA 33 vs 24; **LACE elm (1) scheduled but not found on the plan** → not modeled. Rev 5 log mentions a landscape/paver clarification with no revised LP sheet in the folder.
2. **L-2** The seasonal bed and camellia west of the entrance sit where v007 has paving (`Site_Dropoff_band_west` was digitized too simply). Planting shown on a thin patch over the paving; walk outline should be corrected in a later site revision if approved.
3. **L-3** Planter at the CW2 bay: raised or flush not stated; modeled flush.
4. **L-4** FOAR drawn at about 6 ft, scheduled at 7' o.c.
5. **L-5** South strip planting follows the interpolated v007 ground, which falls toward the street.
6. **L-6** Shown on LP-101 but outside the BLDG II schedule, not modeled: existing island trees, west-street shrub row, south street trees (by others), everything east of the enlargement limit line. **L-7** rooftop terrace planting not reviewed.

## Questions for the design team

1. Where are the remaining 20 CATM, 9 CORA and the LACE elm? Is there a later LP-101 (the Rev 5 log refers to a landscape clarification)?
2. Is the CW2-bay planter raised, and if so how high?
