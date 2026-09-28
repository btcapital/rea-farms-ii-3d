# Site detail control document v013

Date: 2026-09-21
Applies to: `scripts/build_shell_v013.py` → `models/building_shell_v013.blend`
Baseline: **v012, frozen.** Everything in v012 is rebuilt identically; v013 only **adds** small-scale objects, all in the new collection `15_Site_Detail_v013`, all named `DET_…`. The approximate Building I context mass is not touched. Written before the build.

**Source folder note.** `source_documents` now contains two subfolders. All Building II documents (the same 360 files) are under `source_documents\Building II\`, so every source path quoted in the earlier notes now begins with `Building II\`. The **`Building I` folder was not opened, listed, read or used**; only its file count, total size and newest modification time were recorded so that "untouched" can be verified.

Codes: **W** written on a sheet · **M** position or outline measured from the exact-scale civil vector linework (CS-101 rev 6, ±0.5–1 ft) · **A** approximate / assumed, with the reason.

## Elements

| Element (object prefix) | Source | Dimensions | Location | Confidence |
| --- | --- | --- | --- | --- |
| **Parking stall striping** `DET_Striping_stalls` | CS-101 rev 6 linework (`Building II\00 PLANS\Revision 5\Rea Farms 2 - Civil Drawings 03.17.26.pdf` p.7) | 269 lines, lengths **M** (17.5 ft and 18.5 ft single stalls; 37 ft lines across the three double rows north of the Building II islands; 8 row centre lines); line width 4" and white color **A** (standard practice; not stated on the sheets reviewed) | whole lot, positions **M** | lines high; width/color approximate |
| **Accessible-aisle / no-parking hatching** `DET_Striping_hatch` | CS-101 rev 6 hatch linework | diagonal hatch lines **M** (isolated diagonals, which are drawing leaders, filtered out); 4" white **A** | at the HC stalls on the west side of the lot, the aisle ends and the loading zones, as drawn | medium-high. The painted wheelchair symbol is **not** added (its size/color are not documented) |
| **Curb at the north walk** `DET_Curb_walk_…` | CS-101 "parking lot barrier to be 1'-6" curb and gutter, typ."; CX-101 detail 1 (6" high curb) | 6" high **W**; modeled as a 6" wide concrete curb top only (gutter pan not modeled) **A** | along the asphalt side of the paver walk, only where the curb is not flush (x −17 → 56.8 and 160 → 189.6) **M** | medium |
| **Island curbs** `DET_Curb_island_…` | CS-101 island outlines; CX-101 6" curb | 6" high **W**, 6" wide **A** | around the 3 site islands and the 18 context islands **M** (context ones ±3 ft) | medium |
| **Steel bollards** `DET_Bollard_steel_…` (6) | CS-101 note "(6) proposed steel bollard, typ. spaced @ 6'-6" o.c."; CX-101 detail 9 "Steel bollard": 3'-0" above grade, concrete-filled steel pipe, painted two field coats black | height 3'-0" **W**; spacing 6'-6" **W**; diameter 6" **A** (not legible in the detail text) | on the flush-curb band at y = 115.1, x = 87.4, 93.9, 106.9, 113.4, 126.4, 132.9 — the "B" symbols between the light bollards **M** | high |
| **Light bollards** `DET_Bollard_light_…` (4) | CS-101 note "(4) proposed decorative bollard … Light Column Bollard Series 600 by Forms+Surfaces"; E010 rev 10 shows four "BL1" at the same places | height 3.3 ft and 6" diameter **A** (product dimensions not in the folder); finish not given → **neutral placeholder** | y = 115.1, x = 80.9, 100.4, 119.9, 139.4 **M** | position high, size approximate |
| **Light poles** `DET_Light_pole_…` (4) | LP-101 pole symbols along the walk edge (positions **M**); drone photo 8.29.26 shows black poles at about these places | about 20 ft tall, 5" square pole with a 2 ft luminaire **A** (from the photo); black | (4.0, 114.9), (62.0, 114.9), (158.9, 115.2), (194.9, 114.0) | medium — symbol meaning inferred and confirmed only by the photo |
| **Area drain grates** `DET_Area_drain_…` (4) | CG-101 rev 6 structure labels AD-213, AD-214 (north beds), AD-208, AD-209 (generator yard) | 12" round grate **A** | at the leader arrowheads, ±3 ft **A** | low-medium |
| **Door pulls** `DET_Door_pull_100A_…` (2) | A800: door 100A is a 6'-0" × 8'-0" pair of aluminum doors in CW3; A815 layout gives the meeting stile | 1" × 12" vertical pulls at 42" **A** | both sides of the meeting stile of door 100A (x = 84.87) **W/M** | position high, hardware shape approximate |
| **HM door levers** `DET_Door_lever_…` (3) | A800 hardware sets for doors 110B, 102, 104 (lever / panic hardware) | small lever 5" long at 40" **A** | on the v004 door leaves, latch side assumed **A** | low |
| **Concrete control joints** `DET_Joint_…` | CX-102 note "2" sealed expansion joint required at … joints, see dimension control plan"; CG-101 concrete hatch areas | 5 ft spacing **A** (spacing not written on the sheets reviewed) | south-west walk, door-110B landing, stair landings, generator yard slab | low — spacing approximate |

## Not added (not supported or not dimensioned)

Paver joints (Techo-Bloc "Linea" unit size is not given; only the 6" × 13" header size is written, and the header band's location is not dimensioned) · painted wheelchair symbols and any signs · wheel stops (none drawn) · bike racks and bike lockers (shown on CS-101 but this pass excludes furniture) · dumpster enclosures in the far corners of the lot · street curbs and markings outside the block · handrails and cheek walls at the stairs · storm structures other than the four area drains · people, vehicles, interiors.

## Conflicts / open items

1. **Flush curb band vs. bollards.** The bollards stand on the 1.5 ft flush-curb strip (y 114.35 → 115.85), which v007–v012 model as part of the paver band. No geometry changed; bollards are placed on the existing surface.
2. **Light bollard product data** and **steel bollard diameter** are not in the project folder.
3. Light-pole symbol meaning is inferred; the electrical site-lighting sheet (E0.02 in the approved civil set) was not used for pole positions in this pass.
4. Carried: sun-shade drawings-vs-spec conflict, unresolved finishes, CATM / CORA / LACE shortfall, architectural revisions 6–10.
