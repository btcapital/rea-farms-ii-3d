# Model control document v002 — Building II geometry refinement pass

Date: 2026-09-18
Applies to: `scripts/build_shell_v002.py` → `models/building_shell_v002.blend`
Baseline: `building_shell_v001` (approved by owner as the massing and dimensional-control baseline; **not altered**).
Purpose: still **geometry validation only** — no materials, textures, signage, landscaping, furniture, interiors, MEP or photoreal lighting.

Read together with `notes/model_control_v001.md`. Everything in v001 sections 1–5 (source set, confidence codes, units, origin, datum table, grid table, face-of-stud control lines) is **carried over unchanged** and is not repeated here. Only additions and changes are listed.

Confidence codes: **W** written on the sheet · **G** grid position · **M** measured from exact-scale vector linework or the 200-dpi elevation raster · **A** assumption.

## 1. Preserved from v001 (owner item 11)

- Origin: grid 1' × grid K' at Level 01 FF. +X project east, +Y project north, +Z up. Decimal feet; scene metric at true scale.
- Datums: Average Grade −1'-9 3/4", L1 0'-0", Terrace 15'-2", L2 16'-0", parapets 17'-6", 19'-6", 34'-11", 38'-9 1/2", 42'-0", 43'-10", Roof Structure 32'-0".
- Control box: 205'-0" × 105'-10" to **face of stud**, all primed-grid control lines, Level 2 wall lines, roof zones and parapet heights exactly as v001. The script asserts these.
- Open verification item **V-1** (architectural revisions 6–10 not in hand) still stands.

## 2. Exterior wall build-up — Approved A003 (PDF p.20), all W

A003 General Partition Note A: plan dimensions are to face of stud (FOS). The exterior wall type details dimension the build-up outside FOS:

| Wall type | Layers outside FOS | Total outside FOS |
| --- | --- | --- |
| EW1 (typical) / EW3 — brick veneer | 1/2" sheathing + 1 1/2" insulation + 3 1/2" air gap + 3 5/8" brick | **9 1/8"** (0.760 ft) |
| EW2 / EW4 — "brick insert" | 1/2" + 1 1/2" + 1 1/2" air gap + 3 5/8" brick | **7 1/8"** (0.594 ft) |
| EW5 / EW6 / EW7 — architectural metal panel | 1/2" + 1 1/2" + 2" | **4"** (0.333 ft) |
| EW9 (amenity deck) | 1/2" + 2" | 2 1/2" — not used in v002 |
| EW8 (parapet) | "REF PLAN" | see parapet thickness below |

Where each applies was taken from the EW tags on Rev 5 A112 and Approved A122, and **cross-checked against the wall linework**, which lands on the same offsets (west podium face −0.76 ft, west high-block face −0.60 ft, lobby pier face +0.33 ft, Level 2 east wall +0.33 ft).

| Face | Type used | Basis |
| --- | --- | --- |
| Podium: south K' faces, east 12' face, north B' face, west 1.2' face | EW1 9 1/8" | EW1 tags; linework |
| High block: west, north, south faces and the 7.1' jog; podium recess returns; H' jog | EW2 7 1/8" | EW2/EW4 tags on A112 and A122; linework |
| Lobby block, CW2 bay, all Level 2 low-roof walls, south recess back wall, J' south-east face, 11' face, terrace closet | EW5 4" | EW5/EW7 tags; linework |

Resulting overall **finish-face** size (asserted by the script): X −0.594 → 205.760, Y −0.760 → 106.166. Face of stud remains 0 → 205.0 and 0 → 105.833.

Parapet thickness, finish face to inside face (**M**, A132 linework — replaces v001 assumption A-2): terrace 1.50 ft, high block 1.13 ft, lobby block 1.0 ft, low roof 1.0 ft.

## 3. Openings checked against A811 / A815 / A816 (owner item 9)

| Item | v001 (measured) | v002 | Source |
| --- | --- | --- | --- |
| Level 1 storefronts SF1, SF3: sill / head | 3.09 / 13.77 | **3'-0" / 13'-11 5/8"** | W — A811 (3'-0" + 10'-11 5/8") |
| Level 2 storefronts SF4, SF5B, SF6, SF7: sill / head | 19.81 / 28.77 | **19'-0" / 28'-11 1/4"** | W — A811 (3'-0" AFF + 9'-11 1/4"). The v001 sill was wrong: the 19'-6" terrace parapet hides the bottom of these windows on the building elevations. |
| SF5A (terrace door with transoms) | 24.09 – 28.77 (transom only) | **16'-0" → 28'-11 1/4"**, 3'-4" wide | W — A811 (12'-11 1/4") |
| SF2 (east, under canopy) | 3.14 – 9.78 | sill 3'-0", **head 10'-0"**, 14'-10" wide, with a 3'-3" door to the floor at its south end | W — A811 |
| CW1–CW4 head | 28.77 | **28'-10 7/8"**, bottom at finish floor | W — A815 |
| CW2 | two pieces (canopy hid the middle) | **one opening, floor to 28'-10 7/8"**, 9'-3" wide | W — A815 |
| CW1 (lobby) | 0.21–9.81 and 18.25–28.77 | 0 → **9'-11 5/8"**, opaque "door canopy framing area" to **11'-8 1/2"**, glazing again to 28'-10 7/8"; 31'-10" wide | W — A815 |
| CW3 | one opening | 90'-1" wide incl. corner; **door bay 9'-11 1/2"** at its east end: 9" panel, 1'-2 3/4" + 6'-0" + 1'-5 3/4" glazed door assembly, 6" panel; door head 9'-11 5/8"; canopy framing area 2'-2 3/4" above; glazing above that | W — A815 (sizes); bay position M |
| CW4 | 74.07–104.83 | 30'-11 7/8" wide, run to the glazed NW corner | W — A815 |
| CW5 (south 45'-0") | 3.05 / 13.81 | **3'-0" / 14'-0"** | W — A816 |
| CW6 (east entrance) | 0.10 / 13.82 | **0 / 14'-0"**, 10'-0" wide | W — A816 |
| Widths of SF units | glass extents | frame widths 10'-0", 25'-0", 15'-0", 13'-5", 21'-10", 3'-4", 14'-10" | W — A811; centres M (SF5A/SF5B positions W from A122 string 2'-4 1/2", 3'-4", 1'-5 1/2", 21'-10", 6") |

Glass plane is modeled 2" inside the face of stud (**A**), so reveals now show the real wall thickness.

## 4. New geometry

### 4a. Louvered sun-shade — Approved A702 (p.50), A340, Rev 5 S133
- Plan (**W**): arm depth 13'-7" measured from grids H, 10 and D; south arm 153'-6" overall; east side 80'-0" (13'-7" + 8'-10", 8'-9", 8'-10", 8'-10", 8'-9", 8'-10" + 13'-7"); north arm 40'-10 1/2" (2 1/2", 9'-1", 9'-0", 9'-0", 13'-7"). Bay beams at the written spacings; 45° hips at the two corners.
- Outer edges therefore: X = 185.994, Y = 10.950 and 90.961. These agree with the A132 outline measured in v001 (186.0 / 10.94 / 90.94).
- Top of steel **32'-0"** (**W**, S133 Rev 5 "TOS 32'-0""); beam depth 12" (**W**, A340 detail titles "12" / 10" sun-shade beam" — 12" used throughout).
- Louvers: (12) 1" × 10" at 40°, 11" o.c. (**W**, A702 note). Modeled in the straight runs only; corner bays left open (**A**). Tilt direction and centring within the visible depth are **A**.
- The part of the frame between the grid lines and the wall face is inside the building and not shown. The south arm is started at the closet face X = 33.5 (**M**); the written 153'-6" runs to grid 3.

### 4b. Door and side canopies — Approved A701 (p.49)
| Canopy | Plan size (W) | Heights | Slopes (W) |
| --- | --- | --- | --- |
| Main entry (over CW1 doors) | 31'-10 1/8" × 9'-0 1/8" from grid A | bottom 9'-11 5/8", top 11'-8 1/2" at wall — **W** from the A815 CW1 "door canopy framing area" | soffit 7/8":12, top 1/4":12 |
| Door 100A (CW3 door bay) | 10'-0 3/4" × 7'-5 1/8" | bottom 9'-11 5/8", top 12'-2 3/8" — **W** from A815 CW3 | same |
| East (over SF2) | 14'-10" × 3'-11 1/8" | bottom 10'-0" (**W**, SF2 head); top 11'-6" (**A** — S133 gives canopy steel TOS 11'-4") | soffit 2":12, top 1/4":12 |

Projection of the east canopy is taken from grid 12' (**A**; A701 dimensions it from the structure, not from the brick face).

### 4c. Glass railings GR-1
On the three 17'-6" parapet runs only — south recess (6'–7'), the J' face from 9.1' to 11', and the 11' face to H' — from 17'-6" to 19'-6" (**M**, glazing band on Rev 5 A300/A301; type "view glass railing, no top rail" per the A300 legend). 0.1 ft thick, centred on the parapet (**A**).

### 4d. Level 2 terrace closet
X 30.167 → 33.5, Y 10.378 → 22.95 (**M**, A122 linework, EW7 walls); top 34'-11" (**M**, Rev 5 A301 south elevation — same height as the Level 2 parapet). Modeled as a plain solid.

### 4e. Utility yard screen walls — Rev 5 A012 (p.2), Approved A302 west screening elevation
- Heights (**W**, A012): generator enclosure T.O. masonry **14'-0"**; north transformer site wall **3'-4"**; low site wall **2'-8"**.
- Transformer enclosure walls use 3'-4" (**M** — they line up with the 3'-4" wall on the A302 west screening elevation; A012 does not section the enclosure itself).
- Plan positions **M** from A112 linework: generator enclosure X −20.22 → building, Y 24.80 → 64.41, walls 1.43 ft; transformer enclosure X −26.41 → −10.65 (15'-9 3/4" **W**), Y 72.80 → 91.91, walls 1.27 ft, gate side left open; diagonal north site wall; diagonal "sight triangle" low wall and its stub.
- Door openings 4'-4" (north) and 3'-4" (south) wide (**W**, A012); **door head 7'-0" is an assumption**. Gates and brick caps BC-1/BC-2 not modeled.
- Walls are carried down to the flat model ground; real grade falls to the west (U-7).

### 4f. Drop-off canopy — unchanged, **PROVISIONAL** (owner item 10)
No stronger source was found. A700 still has no written heights; S133's "TOS 11'-4"" and "TOS 32'-0"" belong to the door canopies and the sun-shade, not the drop-off canopy (its framing is on S131/S132, not yet reviewed). Values stay as v001: top of glass at gutter 16.1 ft (**M**), column top 15.0 ft (**M**), 14" square columns (**A**). Plan size, column spacing and 1 1/2":12 slope are **W**. The collection is named `04_DropOff_Canopy_PROVISIONAL`.

## 5. Assumptions in v002

| ID | Assumption |
| --- | --- |
| A-1, A-3, A-5, A-6, A-7 | unchanged from v001 |
| A-2 | **retired** — parapet thickness now measured (section 2) |
| A-4 | revised: glass plane 2" inside face of stud; openings are plain recesses with a darker neutral panel |
| A-8 | Brick-insert zones (EW2) inside EW1 walls — 2" shallower panels between windows on the south and east — are not differentiated; those faces are uniformly EW1 |
| A-9 | Sun-shade louver tilt direction, centring, and open corner bays |
| A-10 | East canopy top 11'-6" and projection datum (grid 12') |
| A-11 | Glass railing thickness and position across the parapet |
| A-12 | Utility yard door head 7'-0"; transformer enclosure height taken from elevation alignment |
| A-13 | Terrace closet modeled as a solid to 34'-11" with no separate roof or parapet |

## 6. Unresolved items

| ID | Item |
| --- | --- |
| V-1 | Architectural revisions 6–10 not in hand. |
| U-4 | Drop-off canopy heights and column size still provisional — check S131/S132 and wall section A331. |
| U-7 | Ground modeled flat at Average Grade; site falls to the west, so yard walls read shorter or taller than in reality. |
| U-8 | A003 and A811/A816 are Rev 3 / permit-issue sheets; A815 is Rev 5. No conflict found between them, but A003 was not reissued in Rev 5. |
| U-9 | CW3 door-bay position is measured (±0.2 ft); its sizes are written. |
| U-10 | A702 dimensions the sun-shade from grid lines that sit 1'-7" inside the Level 2 wall face; the visible projection beyond the finish face is therefore 11'-8", not 13'-7". Recorded so it is not mistaken for an error. |
| U-11 | Low site wall east of the sight-triangle diagonal (toward the south stair) was not found in the linework and is not modeled. |
| U-6 | Civil revision-label conflict on CS-101 — unchanged. |
