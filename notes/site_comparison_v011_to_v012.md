# Comparison — building_shell_v011 → building_shell_v012 (vegetation realism pass)

Date: 2026-09-21
Basis: `notes/vegetation_control_v012.md` (written before the build).

## Validation

| Check | Result |
| --- | --- |
| Frozen v001–v011 files (118 files: models, scripts, all notes, build reports, all 59 renders) | SHA-256 identical before and after: **0 changed** |
| `source_documents` | 360 files, **0 modified** |
| Object set | identical — 1,286 mesh objects in both; none added, none removed |
| Non-vegetation objects (building, facade detail, site, walks, walls, terrain, beds, lawn patches, context buildings, streets, islands…) | **632 of 632 identical** vertex for vertex |
| Vegetation objects (340 Building II plants + osmanthus trunk, 17 context trees + 17 trunks, 280 horizon trees) | **654 of 654 at exactly the same location**; mesh and material replaced |
| Plant quantities | unchanged: DAZA 28, RHCO 10, JEWL 8, JADE 17, FOAR 8, ILST 6, GATE 2, SANJ 1, CARE 69, COZA 27, CORA 24, JUNE 28, CATM 37, OSOR 11, SEAS 63 |
| Cameras, sun, sky, exposure | the six v010/v011 cameras and all light settings identical; one camera added (`Cam_landscape_entrance_oblique`) |
| Missing schedule plants, vehicles, people, signage, interiors | none added |

`build_shell_v012.py` = `build_shell_v011.py` + the vegetation block, one call to it, and the seventh view. (Two low-resolution trials were run in a scratch folder; my first full v012 build was deleted and rebuilt once to slim the inner core of the upright plants, which was showing through. No approved file was involved.)

## What changed

- **Building II planting:** every smooth proxy replaced by a procedurally generated plant — leaf-card mounds for azaleas, distylium (layered habit), forsythia (with arching canes), roses, coreopsis, catmint and annuals; upright pyramidal holly; upright oval glossy camellia; osmanthus as a small evergreen tree on its trunk; arching blades for sedge; leaf rosettes for hosta and coral bells. Four variants per species, per-plant brightness shift, per-plant size factor 1.00–1.10 (never below the scheduled minimum), rotation about the vertical axis only.
- **Context trees:** street and island trees now have irregular multi-lobe leaf canopies and tapered round trunks; the 280 horizon trees use four irregular canopy variants with per-tree tone variation.
- **Ground:** lawn gets two scales of tonal variation, fine bump and a slightly duller green; mulch and beds get a chip-scale cellular pattern.

## What remains approximate

Spread of every plant, all groundcover heights, leaf shape/size/density and every vegetation color (cultivar-typical, not from the drawings) · annuals' flower color (undocumented) · RHCO, OSOR, CORA, CATM positions and all groundcover region shapes (interpreted in v008/v009, unchanged) · context tree species, sizes and the horizon (approximate in v011, unchanged) · lawn and mulch are still flat surfaces with shader detail, not blades or chips · no branches are modeled inside canopies · newly installed 15–18" shrubs at 3–5 ft spacing look sparse — that is what the schedule specifies.

Honest assessment: planting now reads as vegetation rather than spheres, and the sedge and small trees are convincing at render distance, but close views (the landscape oblique) still look computer-generated — leaf cards are generic, and the reflected horizon trees read as dark clumps in the glass.

## Performance

| | v011 | v012 |
| --- | --- | --- |
| Faces in scene (instances counted) | 60,267 | about 1.13 million |
| Saved model size | 0.74 MB | 2.4 MB |
| Render time per view (256 samples, RTX A1000, OptiX) | 21–72 s | 22–74 s (+1 to +4 s); new landscape view 50 s |

Instancing keeps the cost low: only 60 plant meshes and 7 canopy meshes are stored.

## Renders (`renders/`)

`building_shell_v012_hero_front_north.png` · `…_entrance_oblique_northeast.png` · `…_rear_oblique_southeast.png` · `…_elevated_site_oblique_northwest.png` · `…_facade_material_closeup.png` · `…_corner_northwest_eye_level.png` · `…_landscape_entrance_oblique.png`
