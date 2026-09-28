# Landscape control document v008

Date: 2026-09-21
Applies to: `scripts/build_shell_v008.py` → `models/building_shell_v008.blend`
Baseline: **v007, frozen** — building and site rebuilt identically; nothing moved to make planting fit.
Written before the final v008 build.

Codes: **W** written in the plant schedule or a plan callout · **M** symbol position measured from the LP-101 vector linework (sheet registered to the building ±0.7 ft) · **INT** interpreted (explained) · **A** assumption.

## 1. Controlling landscape sources

| Sheet | File, PDF page | Printed revision / status | Use |
| --- | --- | --- | --- |
| **LP-101 Landscape Plan – Building** (with "Plant Schedule BLDG II") | `00 PLANS\Approved Civil\APPROVED-LDCP-2025-00715.pdf` p.13 | rev 1 11.06.25 "City comments"; landscape architect's seal 09.08.2025; **City of Charlotte Land Development FINAL APPROVAL 1/9/2026** (LDCP-2025-00715) | **Controlling.** Plant schedule, callouts, symbol positions, bed and lawn shapes |
| LP-100 Overall Landscape Plan | same file p.12 | rev 1 11.06.25, rev 2 12.12.25 | Legend, planting notes, tree-mitigation and urban-forestry notes for the whole site (LP-101 refers to it). Not needed for positions at the building |
| LP-100 / LP-101 earlier issues | `Approved Set\APPROVED-COS-001319.pdf` p.8–9; `Permit_Pricing CDs…\02 CIVIL & LANDSCAPE…` p.13–14 | no revisions listed (09.23.25 / 09.29.25) | Superseded by the approved-civil issue |
| Revision 5 log | `Revision 5\_00 REVISION LOG…pdf` | 02.27.2026 | Says "Landscape: 1. Clarification to pavers at entrance" — **but no revised LP sheet is in the folder** (the Rev 5 civil/landscape PDF contains only CO-100 and CS-101; the 03.17.26 civil package has no LP sheets). See conflict L-1 |
| CS-101 / CG-101 rev 6, A012 Rev 5 | as in `site_control_v006.md` | 03.10.26; 02/27/2026 | Site geometry the planting must fit |

No separate planting details sheet or landscape specification section was found in `source_documents` (specification Division 32 says "see civil drawings").

## 2. Plant Schedule BLDG II (LP-101) — all W

| Symbol on plan | Code | Qty | Botanical / common name | Size | Cal. | Height | Spacing |
| --- | --- | ---: | --- | --- | --- | --- | --- |
| tree circle | SANJ | 1 | Osmanthus × fortunei 'San Jose' — San Jose Fortune Osmanthus | B&B | 1.5" min | 8' min | as indicated |
| tree circle | LACE | 1 | Ulmus parvifolia 'Allee' — Allee Lacebark Elm | B&B | 2.5" min | 8' min | as indicated |
| shrub circle, dot | DAZA | 28 | Azalea × 'Roblen' — Autumn Sunset Encore Azalea | 7 gal | – | 15" min | 3' o.c. |
| large shrub circle | GATE | 2 | Camellia japonica 'White by the Gate' | 7 gal | – | 36" min | 6' o.c. |
| toothed circle | JEWL | 8 | Distylium × 'BLDY01' — Jewel Box Distylium | 3 gal | – | 15" min | 3' o.c. |
| shrub circle, dot | JADE | 17 | Distylium × 'Vintage Jade' | 3 gal | – | 18" min | 4' o.c. |
| scalloped circle | FOAR | 8 | Forsythia × 'Arnold's Dwarf' | 3 gal | – | 12" min | 7' o.c. |
| irregular outline | ILST | 6 | Ilex crenata 'Steeds' — Steeds Japanese Holly | 15 gal | – | 36" min | as indicated |
| circle with "+" | RHCO | 10 | Rhododendron × 'Conlea' — Autumn Rouge Encore Azalea | 7 gal | – | 15" min | 5' o.c. |
| hatch | SEAS | 63 | Seasonal annuals | 6" pot | – | – | 12" o.c. |
| hatch | CARE | 69 | Carex oshimensis 'Evergold' — Evergold Sedge | 1 gal | – | – | 18" o.c. |
| hatch | COZA | 27 | Coreopsis verticillata 'Zagreb' — Zagreb Tickseed | 1 gal | – | – | 18" o.c. |
| hatch | CORA | 33 | Heuchera × 'Electric Plum' — Coral Bells | 1 gal | – | – | 24" o.c. |
| hatch | JUNE | 28 | Hosta × 'June' | 1 gal | – | – | 24" o.c. |
| hatch | CATM | 57 | Nepeta × faassenii 'Walker's Low' — Catmint | 1 gal | – | – | 24" o.c. |
| hatch | OSOR | 11 | Rosa × 'Chewnicebell' — Oso Easy Italian Ice Rose | 3 gal | – | – | 24" o.c. |

Plan callouts found on LP-101 (W): north-west bed (33) CARE, (27) COZA, (15) DAZA, (2) ILST; west strip (2) ILST, (8) JEWL; drop-off flanks (29) SEAS + (1) GATE west, (34) SEAS + (1) GATE east, (3) OSOR; north-east bed (8) OSOR, (28) JUNE, (36) CARE, (13) DAZA, (2) ILST; south strip (17) JADE, (37) CATM, (24) CORA, (10) RHCO, (1) SANJ, (8) FOAR.

## 3. What is modeled, and how each item is known

| Item | Qty modeled | Position | Size of proxy |
| --- | ---: | --- | --- |
| DAZA | 28 | **M** — each symbol's centre dot: 15 in the row along the north face west of the entrance, 13 along the north face of the east wing | height 15" **W**; spread 2.4 ft **INT** |
| ILST | 6 | 4 **M** from centre dots (row ends); the 2 on the west strip **M from the raster, ±1 ft** | height 36" **W**; spread **INT** |
| GATE | 2 | **M** | height 36" **W**; spread **INT** |
| JEWL | 8 | **M** (west strip, 3 ft apart) | 15" **W**; spread **INT** |
| JADE | 17 | **M** (four groups along the south face, 4 ft apart) | 18" **W** |
| FOAR | 8 | **M** (south-east, 6 ft apart as drawn; schedule says 7' o.c.) | 12" **W** |
| SANJ | 1 | **M** (in front of the south recess) | 8 ft tall **W**; 4 ft canopy and trunk proportions **INT** |
| RHCO | 10 | **INT** — the "+" symbols could not be extracted; placed 5' o.c. (W) in the two gaps between JADE groups where the plan shows them | 15" **W** |
| OSOR | 11 | **INT** — (3) in the planter in front of the CW2 bay, (8) in a row in front of the north-east DAZA row, 24" o.c. (W) | 1.2 ft **INT** (no height scheduled) |
| CORA | 24 | **INT** — front row of the south strip at the two RHCO gaps, 24" o.c. (W) | **INT** |
| CATM | 37 | **INT** — front row of the south strip at the JADE groups, 24" o.c. (W) | **INT** |
| COZA 27, CARE 33 (17+16), CARE 36, SEAS 29, SEAS 34, JUNE 28 | as called out | **INT** — hatch areas read from LP-101 and approximated as simple regions; plants set at the scheduled spacing (W), packed about the centre of each region | heights **INT** (none scheduled) |
| Mulch bed surfaces, lawn patches | 7 patches | **INT** outlines; 0.05–0.08 ft above the v007 ground | — |

All proxy **colors are representational** category colors, not documented. Plants are shown at about **installed** size (heights W where scheduled), not mature size. Mulch type, bed edging and sod type are **not given** on LP-101: the orange bed-edge arcs are used only as the lawn/bed boundary; no edging object is modeled.

Lawn: v007 ground is already lawn-colored wherever it is not paving or bed. v008 adds two lawn patches where LP-101 shows turf *inside* the v007 bed shapes (the middle of the north-west bed behind the arc, and part of the north-east bed).

## 4. Conflicts and open items (flagged, nothing moved)

| # | Item |
| --- | --- |
| **L-1** | **Schedule totals vs. plan callouts.** CATM: schedule 57, callouts total 37 (20 not located). CORA: schedule 33, callouts 24 (9 not located). **LACE** tree: scheduled (1) but no callout or symbol found inside the BLDG II limit line. Not modeled rather than guessed. Also the Rev 5 log mentions a landscape clarification "to pavers at entrance" with no revised LP sheet in the folder. |
| **L-2** | **Seasonal bed west of the entrance vs. v007 paving.** LP-101 (and CS-101) show a planting bed between the building and the curved walk from about x = 61 to 80 ft. v007's `Site_Dropoff_band_west` slab was digitized as one simple shape and covers that area. The (29) SEAS and (1) GATE are placed where LP-101 puts them, on a thin mulch patch named `…_OVER_V007_PAVING`. Recommend correcting the walk outline in a later site revision. |
| **L-3** | **Planter at the CW2 bay.** LP-101 shows a small stippled rectangle with (3) OSOR in front of the narrow curtain-wall bay, inside v007's paved band. Whether it is a raised planter or a flush bed is not stated; modeled flush. |
| **L-4** | FOAR drawn at about 6 ft spacing; schedule says 7' o.c. Drawn positions used. |
| **L-5** | South strip: LP-101 shows the bed between the building and the right-of-way line; v007's interpolated ground falls away there, so the plants step down with the terrain. No grading was changed. |
| L-6 | Shown on LP-101 but **not in the BLDG II schedule and not modeled**: existing parking-island trees, the row of shrubs along the west street, street trees along the south street (by others), and all planting east of the heavy "see enlargement" limit line (Building I / plaza). |
| L-7 | Rooftop terrace planting, if any, is on civil rooftop sheets CS-301 / CX-201, not reviewed in this pass. |
| V-1 | Architectural revisions 6–10 not in hand (carried). |
