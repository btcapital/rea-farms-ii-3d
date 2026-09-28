# Vegetation control document v012

Date: 2026-09-21
Applies to: `scripts/build_shell_v012.py` → `models/building_shell_v012.blend`
Baseline: **v011, frozen.** Building, site, context, materials on non-vegetation objects, lighting, exposure and the six cameras are rebuilt identically. v012 changes **only what the vegetation looks like**: the mesh and material of each existing plant / tree object, and the lawn and mulch shaders. Written before the build.

Not changed: any plant location, any quantity, any bed or lawn outline, any site or building geometry. Not added: the unresolved schedule plants (20 CATM, 9 CORA, 1 LACE), rooftop planting, vehicles, people, signage, interiors.

## 1. Method — no external assets

No purchased, downloaded or photo-scanned plant models and no image textures are used (nothing may be downloaded under the project rules, and none exist in `source_documents`). Every plant is **generated procedurally inside the build script** from a fixed random seed, so the result is repeatable:

- **Leaf-card clumps.** A plant is a cloud of small folded leaf shapes (two triangles each, creased along the midrib) distributed through several overlapping lobes, denser toward the outside, around a dark inner core that stops see-through. Leaf size, count, tilt, lobe layout and overall proportions differ by species.
- **Blade and rosette forms** for sedge (arching strips), hosta and coral bells (broad arching leaves from a crown).
- **Accent elements** — small flower discs or spikes — only where the documented cultivar is a flowering plant, kept sparse and muted.
- **Variants.** Four different meshes per species (three for small trees, four for horizon trees), assigned in rotation, plus a per-plant brightness shift and a per-plant size factor of 1.00–1.10 (never below the scheduled minimum). Existing per-object rotation about the vertical axis is kept; no tilting.
- **Trees.** Canopy = leaf-card clumps in 6–8 irregular lobes around a lumpy core; trunk replaced by a tapered round trunk of the same height and position.
- **Leaf shading.** Two-sided leaves with noise mottling, slight translucency, and species-specific roughness (glossy for camellia and holly, matte for catmint and sedge).

## 2. Building II planting — what is documented vs. approximate

Positions and quantities: **exactly as v008/v009** (measured or interpreted as recorded in `landscape_control_v008.md`; unchanged here). Species and installed sizes: **LP-101 Plant Schedule BLDG II**.

| Code | Species (LP-101) | Qty | Installed size from schedule | Modeled height | Modeled spread (assumed) | Form used |
| --- | --- | ---: | --- | --- | --- | --- |
| DAZA | Encore azalea 'Roblen' | 28 | 7 gal, 15" min | 1.25–1.4 ft | 2.4 ft | dense low mound, small leaves, **no blooms** |
| RHCO | Encore azalea 'Conlea' | 10 | 7 gal, 15" min | 1.25–1.4 ft | 3.0 ft | same, slightly looser |
| JEWL | Distylium 'Jewel Box' | 8 | 3 gal, 15" min | 1.25–1.4 ft | 2.4 ft | layered, horizontal small blue-green leaves |
| JADE | Distylium 'Vintage Jade' | 17 | 3 gal, 18" min | 1.5–1.65 ft | 3.2 ft | same, wider and flatter |
| FOAR | Forsythia 'Arnold's Dwarf' | 8 | 3 gal, 12" min | 1.0–1.1 ft | 4.0 ft | low arching canes with sparse light-green leaves, no blooms |
| ILST | Ilex crenata 'Steeds' | 6 | 15 gal, 36" min | 3.0–3.3 ft | 2.5 ft | upright pyramidal, very small dark leaves |
| GATE | Camellia japonica 'White by the Gate' | 2 | 7 gal, 36" min | 3.0–3.3 ft | 3.0 ft | upright oval, larger glossy dark leaves, no blooms |
| SANJ | Osmanthus × fortunei 'San Jose' | 1 | B&B, 1.5" cal, 8' min | 8.0 ft | 4.0 ft | small upright evergreen tree form on the existing trunk |
| CARE | Carex 'Evergold' | 69 | 1 gal | 0.7 ft | 1.2 ft | arching fine blades, cream-green |
| COZA | Coreopsis 'Zagreb' | 27 | 1 gal | 0.8 ft | 1.2 ft | fine thread-leaf mound, a few small muted-yellow flowers |
| CORA | Heuchera 'Electric Plum' | 24 | 1 gal | 0.7 ft | 1.6 ft | rosette of rounded plum-toned leaves, a few thin flower stalks |
| JUNE | Hosta 'June' | 28 | 1 gal | 0.8 ft | 1.7 ft | rosette of broad arching leaves |
| CATM | Nepeta 'Walker's Low' | 37 | 1 gal | 0.9 ft | 1.7 ft | grey-green mound with muted lavender spikes |
| OSOR | Rosa 'Oso Easy Italian Ice' | 11 | 3 gal | 1.2 ft | 1.8 ft | loose mound, a few pale flowers |
| SEAS | Seasonal annuals | 63 | 6" pot | 0.5 ft | 0.8 ft | small leafy mounds with a few muted flowers |

**Exact (from the schedule):** species, quantity, container size, caliper, minimum height.
**Approximate:** spread (the schedule gives spacing, not spread), all groundcover heights (none scheduled), leaf size and density, habit, and every color. Foliage and flower tones follow what the **named cultivar** normally looks like (e.g. 'Electric Plum' foliage is plum, 'Zagreb' flowers are yellow, 'Evergold' is cream-striped, 'Walker's Low' is lavender) — that is horticultural common knowledge about the documented cultivar, **not information from the drawings**. The annuals' flower color is not documented at all; a muted pink/white mix is a visual assumption.

**Substitutions made only for visual realism:** shrubs shown in leaf without seasonal bloom (spring forsythia and azalea flowers would be misleading for a summer view); plants shown at installed size with a 0–10 % size variation; one generic leaf shape per species rather than botanically exact leaves.

## 3. Context trees (positions and approximate sizes exactly as v011)

| Group | Count | Change |
| --- | ---: | --- |
| Street trees, North Rea Park Ln | 14 | rounded canopy → irregular multi-lobe leaf-card canopy (about 12 ft tall, 5.5 ft spread, as v011); tapered round trunk. Species unknown (by others) → generic young deciduous shade tree |
| Existing parking-island trees | 3 | same treatment |
| Wooded horizon | 280 | four irregular multi-lobe canopy variants with per-tree brightness variation; no trunks (as v011) |

All remain **approximate** context, as classed in `context_control_v011.md`.

## 4. Ground surfaces (shader only; outlines unchanged)

- **Lawn:** two scales of tonal variation (broad patchiness and fine mottling), stronger fine bump, slightly duller and less saturated green. No grass-blade geometry.
- **Mulch and planting beds:** chip-scale cellular pattern in color and bump over the v010 variation, so beds read as shredded mulch rather than flat brown. Mulch type is not documented.

## 5. Cameras and light

Identical to v011. One view added: `landscape_entrance_oblique` (low oblique over the north-west bed and the entrance planting).
