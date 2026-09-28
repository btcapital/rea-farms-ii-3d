# Context control document v011

Date: 2026-09-21
Applies to: `scripts/build_shell_v011.py` → `models/building_shell_v011.blend`
Baseline: **v010, frozen.** Building II, its site, landscape, materials, lighting, exposure and the six cameras are rebuilt identically. v011 adds **context only**, all in the new collection `14_Context_v011`, every object named `CTX_…` with its confidence in the name. Written before the build.

No signage, tenant names, people, vehicles, interiors, street furniture or speculative architecture. Nothing about Building II was changed from photos.

## Confidence classes

- **Exact** — written dimension or elevation.
- **Measured** — outline scaled from the civil vector linework (CS-101 rev 6, 1" = 20'), ±2–3 ft.
- **Simplified** — a real, documented element reduced to a plain shape (flat, constant width).
- **Approximate** — existence supported by the site photos or plan labels, but size, height or position estimated.

## Sources

| Source | Use |
| --- | --- |
| CS-101 Dimension Control Plan, rev 6 03.10.26 (`Revision 5\Rea Farms 2 - Civil Drawings 03.17.26.pdf` p.7) | Building I footprint and label ("Existing two-level mixed use building 'Building I', FFE 661.75"), block right-of-way lines, parking islands, street names and R/W widths, "existing sidewalk", "existing on-street parking" |
| CG-101 rev 6 (same file p.3) | Building I FFE 661.75; existing grades at the block edges |
| LP-101 (approved civil p.13) | positions of the street trees along North Rea Park Ln and the three existing parking-island trees |
| Drone photos 8.29.26 (`Photos\8.29.26 Drone Photos\dji_fly_…_photo.JPG`, `image*.jpg`) and ground photos 08.04.26 | what surrounds the site: Building I's general character, multi-storey apartment buildings beyond an open lawn to the south, houses to the west, a continuous wooded horizon, young street trees |

No architectural drawings of Building I, and no survey of anything outside the block, are in `source_documents`.

## Context elements

| Element (object name prefix) | Source | Class | Notes |
| --- | --- | --- | --- |
| `CTX_BuildingI_mass…` | CS-101 footprint; CG-101 FFE | footprint **Measured** (corners squared off, bays and canopies omitted); FFE 661.75 **Exact**; height 34 ft **Approximate** (photos: two levels, about as tall as Building II's low roof) | Plain mass. Dark masonry-tone material and a lighter upper band are **Approximate** from photos — not a reconstruction |
| `CTX_Parking_island_…` (18) | CS-101 | **Measured** ±3 ft, all drawn the same size | 6" curb height as CX-101 |
| `CTX_Parking_east_half…` | CS-101 | **Simplified** (one flat surface, no striping) | |
| `CTX_Ground_east_of_site…` | CS-101 (walks and plaza around Building I) | **Simplified** to one paved surface | |
| `CTX_Lawn_band_north…`, `CTX_Sidewalk_north…`, `CTX_Sidewalk_south…` | CS-101 ("existing sidewalk", perimeter landscape strip) | **Simplified**, widths scaled | |
| `CTX_Street_Golf_Links_Dr…`, `…N_Rea_Park_Ln…`, `…Terminus_Rd…`, `…Midway_Park_Dr…` | CS-101 street labels and R/W widths (60 ft / 61 ft) | **Simplified**: flat asphalt bands at the right-of-way position, no curbs, markings or on-street parking bays | Terminus Rd and N Rea Park Ln are "proposed … by others" on the civil sheets |
| `CTX_Street_tree_south_…` (14) | LP-101 symbols along North Rea Park Ln (first 7 **Measured**; the rest continue the same 40 ft spacing along the block) | position Measured / continued; size **Approximate** (young trees about 12 ft, as in the photos) | species unknown (by others) |
| `CTX_Island_tree_…` (3) | LP-101 existing-tree symbols in the three nearest islands | position **Measured**; size **Approximate** | |
| `CTX_Park_lawn_south…`, `CTX_Lawn_beyond_Golf_Links…` | drone photos | **Approximate** extent | flat lawn-colored ground |
| `CTX_Distant_building_…` (6, with dark roofs) | drone photos: apartment blocks to the south, houses to the west and east | **Approximate** size, height (48 ft / 30 ft) and position | plain boxes, only to give the horizon scale |
| `CTX_Horizon_tree_…` (280) | drone photos: wooded horizon all round | **Approximate** | large low-detail canopies about 900–1,000 ft away |

All context ground sits on the v010 backdrop slabs, so it is **flat** at the mean height of each site edge; real grades outside the modeled site are not documented in the folder.

## Not added

Vehicles, people, signage, light poles, bollards, bike racks, dumpster enclosures, striping, on-street parking bays, Building I's canopies, storefronts or plaza features, the row of shrubs along the west street, anything not visible in the documents or photos.

## Open items carried

Project north = plan north (A-1) · architectural revisions 6–10 not in hand · unresolved finishes remain grey placeholders · interiors not modeled.
