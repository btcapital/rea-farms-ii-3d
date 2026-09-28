# Interior base-building control document v014

Date: 2026-09-21
Applies to: `scripts/build_shell_v014.py` → `models/building_shell_v014.blend`
Baseline: **v013, frozen.** Every v013 object is rebuilt by the identical code and is not edited. v014 only **adds** interior base-building objects (all named `INT_…`) in a new collection tree `Building_II`. Written before the build.

Scope: Building II only. The `source_documents\Building I` folder was not opened, listed or used. This is **not** a tenant upfit: no tenant partitions, furniture, casework, finishes or layouts.

Codes: **W** written on a sheet · **G** grid position (grid dimensions are written) · **M** measured from exact-scale vector linework of the sealed PDF (±0.03 ft on 1/4" plans, ±0.06 ft on 1/8" plans) · **A** assumed, with the reason.

## 1. Controlling source sheets

"Approved" = `Building II\00 PLANS\Approved Set\APPROVED-COS-001319.pdf` (PDF page in brackets). "Rev 5" = `Building II\00 PLANS\Revision 5\03 Architectural…` / `04 Structural…REV 5 2026.02.27.pdf`.

| Subject | Sheet | Set | Notes |
| --- | --- | --- | --- |
| Level 1 plan | **A112** Level 1 Dimension Plan | Rev 5 (p.3) | Rev 5 enlarges Elec. Room 102 |
| Level 2 plan | **A122** Level 2 Dimension Plan | Approved (p.25), rev 3 12/12/2025 | not reissued in Rev 5 |
| Level 1 slab | **A191** Level 1 Slab Plan | Rev 5 (p.5) | ribbon slab / future slab |
| Level 2 slab | A192 | Approved (p.28) | |
| Ceilings | **A212** Level 1 & 2 Dimension RCP | Rev 5 (p.7) | only core rooms have ceilings |
| Sections | A320 Overall Building Sections | Approved (p.34) | level datums |
| Restroom, amenity | **A420** Enlarged Plans | Approved (p.42) | 3/8" scale |
| Stair 1 + elevator | **A500** plans, **A501** sections | Approved (p.43, 44) | 1/4" and 3/8" scale |
| Stair 2 | **A502** plans, A503 sections | Approved (p.45, 46) | 1/4" scale |
| Doors | **A800** Door Schedule | Approved (p.51) | |
| Wall types | **A003** Interior Partition & Exterior Wall Types | Approved (p.20) | |
| Floor / roof assemblies | A004 | Approved (p.21) | |
| Foundation / slab on grade | **S101** | Rev 5 (p.2) | "future slab on grade not in scope" |
| Level 2 framing | **S102** 2nd Floor Framing Plan | Rev 5 (p.4) | structural grid dimensions, beam sizes, slab |
| Roof framing | S103 | Rev 5 (p.5) | 3" roof deck |
| Columns | **S600** Graphical Column Schedule | Approved (p.103) | sizes and heights |
| Suite boundaries | `Building II\2025.09.23_CSMC MOB 2 - Rentable & Usable Areas.pdf` | 09/23/2025 | BOMA 2017 areas |
| Also available, not yet used | G110 Life Safety, G111 Fireproofing, ID101/ID102 finish plans, ID201–ID303 interior elevations/details, M110/M120, P110–P122, E110/E120, FP110/FP120 | | for later phases |

## 2. Levels, floor-to-floor heights, slabs

| Item | Value | Source |
| --- | --- | --- |
| Level 01 finish floor | 0'-0" (= civil FFE 660.30) | **W** A300/A320/A501 |
| Level 02 finish floor | 16'-0" → floor-to-floor **16'-0"** | **W** |
| Terrace finish floor | 15'-2" | **W** |
| Roof structure | 32'-0" → Level 2 floor-to-structure **16'-0"** | **W** |
| Level 2 floor | 3½" normal-weight concrete on 3" 20-ga composite deck, **6½" total** | **W** S102 note 1 |
| Roof deck | 3" 20-ga wide-rib deck | **W** S103 |
| Level 1 slab actually poured | 4" slab on grade: **4'-0" wide perimeter "concrete ribbon slab"**, the lobby, Stair 2, Elec. Room 102 strip and Riser Room 104 | **W** A191 Rev 5 / S101 (extents **M**) |
| Level 1 tenant-area slab | **"Future slab on grade not in scope. Coordinate with tenant designers and GC."** | **W** S101 Rev 5 |
| Elevator pit | −5'-0" | **W** A191 |
| Clear height under Level 2 structure | slab underside 15'-5½"; under typical W21–W24 beams about 13'-5" to 13'-8"; under the deepest girders (W30x90/W30x99, grids 7 and 10 and grid F) about **12'-11"** | computed from **W** sizes on S102; beams are recorded here, **not modeled** |
| Clear height under roof structure (Level 2) | deck underside about 31'-9"; joist/beam depths not evaluated in this pass | **A** |

## 3. Structural grid (unchanged from v001–v013)

Face-of-stud control box 205'-0" × 105'-10" (**W** A112). Column grid X (ft from grid 1'): 1 = 1.5, 2 = 6.0, **2.8 = 27.719**, 3 = 32.5, 3.1 = 34.5, 4 = 59.0, 5 = 65.5, 6 = 80.5, 7 = 92.5, 7.2 = 95.5, 8 = 105.5, 8.3 = 115.5, 8.4 = 125.378, 9 = 143.5, 9.1 = 145.125, 10 = 172.411, 11 = 202.0, 12 = 203.5 (**W** S102 / A112 grid strings). Grid Y (ft from grid K'): K = 1.833, J = 3.833, H = 24.533, G = 50.944, F = 58.789, E.4 = 65.944, **E.1 = 68.29 (M, S102 bubble position; not dimensioned on the sheets read)**, E = 71.833, D = 77.378, C = 83.789, B = 96.833, A = 103.333.

## 4. Columns (S600 sizes **W**, positions **G**)

Full height (Level 1 to roof or parapet): A-1, A-3, A-5, A-7 W10x68 · A-8, A-9 W14x90 · C-1 W10x49 · D-10 HSS12x12x5/8 · E-8 W10x68 · E-9 W10x60 · F-1 W10x60 · F-3, F-4, F-7 W12x79 · G-8 W10x68 · G-9 W10x60 · G-10 HSS12x12x1/2 · H-3, H-5, H-7.2, H-8.3, H-9.1 W12x65 · H-10 HSS12x12x5/8.
Level 1 only (to Level 2 / terrace framing): B-9.1, B-10 W10x39 · B-12 W10x49 · E-8.4 W10x68 · E.1-2.8 HSS8x8x3/8 · E.4-12 W10x49 · G-12 W10x45 · H-2 W10x49 · H-12 W10x54 · J-10, J-11 W10x39 · K-2, K-3.1, K-5, K-6, K-7.2, K-8.3 W10x39 · K-9.1 W10x49 · A(1'-4")-6 and A(1'-4")-7(−2'-11¾") HSS6x6x3/8.
Level 2 only: G-3(−1'-9") HSS6x6x3/8 · G-12(1'-3") HSS6x6x3/8 post · H(8'-3")-11(2'-9") HSS6x6x3/8.
Canopy columns X1/X2/X3-XA: already in v003–v013, untouched.

Modeled as plain boxes of the AISC depth × flange width. **A:** orientation of W shapes (web assumed north–south), direction of the written offsets for the five offset columns, and no fireproofing / furring wrap (G111 not yet applied). Free-standing interior columns that affect tenant planning: F-3, F-4, F-7, G-8, G-9, G-10, D-10, H-3, H-5, H-7.2, H-8.3, H-9.1, H-10 (Level 1), and the same less the H line (which is the Level 2 south wall line) on Level 2.

## 5. Core walls (rated walls **M** from the blue rated-wall hatch on A500 / A502 / A420, cross-checked on A112 Rev 5 / A122: agreement ≤ 0.03 ft)

Coordinates are face of stud / face of CMU. Type code per A003 (**W**): S = steel stud, M = masonry; A = gypsum both sides, C = one side, D/J = shaft wall; number = stud size (3 = 3⅝", 6 = 6", 8 = 7⅝" CMU); ".1" = 1-hour. Finish thickness = stud + ⅝" type X each side (A003 **W**).

| Element | Geometry (ft) | Type | Source |
| --- | --- | --- | --- |
| Lobby 101 / 204 west wall | x 106.24–106.54; L1 y 72.36→105.8 with door 101D gap 97.56→101.12; L2 y 71.4→105.8 plus stub 64.07→64.76, door 200A in the gap 64.76→71.4 | SA3.1 | A500 |
| Lobby 101 south wall (L1) | y 72.34–72.84, x 106.55→135.75; door 101C gap 126.66→133.2 | SA6.1 | A500 |
| Lobby 101 east wall (L1) | x 142.5–143.0, y 82.58→97.84; door 101B gap 88.16→94.74; return y 97.34–97.84 to x 144.5 | SA6.1 | A500 |
| Level 2 lobby 204 south wall | y 64.06–64.56, x 106.55→139.91; door 200B gap 126.46→132.88 | SA6.1 | A500 |
| Level 2 lobby / corridor east wall | x 150.5–151.0, y 55.32→78.45 | SA6.1 / SA6.1A | A420 |
| Elevator shaft | CMU 7⅝": outside x 135.75→143.08, y 72.58→82.58; clear 6'-0¾" × 8'-8¾" (**W**); door in west wall (3'-6" car door **W**); both levels, pit −5'-0", top at roof structure | MA8.1 | A500, A501 |
| Mechanical shaft (L2 → roof) | x 100.76→106.24, y 73.31→100.73, 1" shaft-liner walls | SJ2.1 | A500 |
| Exhaust shaft at restroom (L2) | x 136.61→140.03, y 59.18→63.99 | SJ2.1 | A420 |
| Exhaust shaft at Stair 2 (L2) | x 27.19→31.0, y 59.37→63.14 | SJ2.1 | A502 |
| Stair 2 enclosure | walls 6": south y 59.38–59.87, north y 69.64–70.14, east x 26.69–27.19; west = exterior wall; L1 door 110A gap y 60.75→64.21, L2 door 210A gap y 65.98→69.64, L2 exterior door 210B gap x 21.67→25.08 | SA6.1 | A502 |
| Elec. Room 102 (Rev 5 size) | south wall y 45.14–45.63 (door 103 gap x 5.83→10.18), east wall x 17.59–18.08 up to the Stair 2 wall; ceiling 10'-0" | SA6.1 | A112 Rev 5, A212 |
| Riser Room 104 | walls 3⅝": y 15.5–15.8 and 28.4–28.71, east x 17.78–18.08; ceiling 10'-0" | SA3.1 | A112 Rev 5, A212 |
| Restroom 205 (L2, single-user) | room x 139.64→150.5, y 55.81→64.07; west wall x 139.14–139.64; south wall y 55.32–55.81; north wall y 64.07–64.57 with door 200C (3'-6") at the east end; ceiling 10'-0" | SA6.1, SA6.0 | A420, A212 |

Not built in the base building: **"Future Emergency Elect. Room 103"** (drawn dashed, 12'-7" × 16'-11"); recorded, not modeled as walls. It is shown as a floor outline only.

## 6. Stairs and elevator

| Item | Value | Source |
| --- | --- | --- |
| Stair 1 (open lobby stair) | 28 risers: **15 risers** (14 treads at 11" = 12'-10") north→south along the west wall, landing at **8'-6 7/8"**, then **13 risers** (12 treads at 11" = 11'-0") west→east to Level 2 | **W** A500, A501 |
| Stair 1 position | run 1 x 107.9→113.02, bottom riser y 92.20, landing y 73.44→79.37 (5'-11 1/8" **W**), run 2 to x 124.52; glass guardrails | **M** A500 (dimension strings 6½", 6'-1", 11'-0", 7¼", 12'-10" agree) |
| Level 2 floor edge ("open to below") | lobby is double height over x 106.54→142.5, y 82.52→103.3 and over Stair 1; Level 2 floor exists south of y 73.44, and x 124.52→135.75 up to y 82.52 | **M** A500 Level 2 plan |
| Stair 2 (enclosed egress stair) | switchback, 13 treads at 11" = 11'-11" per run (**W**), runs x 7.64→19.55; north run y 65.53→69.35 rises westward from Level 1, south run returns to Level 2; 28 risers assumed equal (6.857") | **W/M** A502; mid-landing height **A** (= 8'-0") |
| Elevator | Otis Gen3 Core, 2500 lb, front opening, side-justified, car door 3'-6" × 7'-0" | **W** A500 basis of design |

Railings, stringers, treads' thickness and nosings are simplified (**A**).

## 7. Fixed doors (A800 **W** sizes; positions **M**)

101A 14'-0" × 10'-0" automatic bi-parting entry (in CW1, already an opening in v013) · 101B 6'-0" × 7'-0" pair, 45 min · 101C pair (size per hatch gap 6.5 ft; tag on A112) · 101D 3'-0", 45 min · 110A 3'-0" × 7'-0", 45 min · 200A, 200B 6'-0" × 7'-0" pairs, 45 min · 200C 3'-6" × 7'-0" · 210A 3'-0" × 7'-0", 45 min · exterior: 100A, 100B, 100C, 102 (4'-0"), 104, 110B, 200D (terrace), 210B (terrace). Doors are modeled as **openings only** (7'-0" head); leaves and frames are not modeled. Doors 101B, 101C, 200A, 200B are the documented tenant entries off the lobbies.

## 8. Common areas and suite boundaries

Common / base building: Lobby 101, Stair 1, elevator, Level 2 Lobby 204 (including the strip to the terrace door 200D), Restroom 205, Stair 2, Elec. Room 102, Riser Room 104, shafts.
Tenant area: one undivided "TENANT(S)" space per floor — room 100 (Level 1) and room 200 (Level 2). **No demising walls are documented.** BOMA 2017 (09/23/2025): Level 1 rentable 19,803 SF / usable 18,484 SF; Level 2 rentable 10,564 SF / usable 9,918 SF. The Level 1 figure predates the Rev 5 electrical-room enlargement. The model reports its own tenant-area figure for comparison.

## 9. Ceiling / soffit constraints (A212 Rev 5 **W**)

Tenant areas: no ceiling — exposed to structure. Lobby 204 gypsum ceiling CA-1 at 12'-11 3/8" AFF with a 12'-6" / 12'-0" feature drop; Level 1 lobby is double height under it. Restroom 205, Elec. 102, Riser 104: 10'-0". Stair 2 Level 2: 14'-0" and 15'-8 7/8". Modeled: the three 10'-0" room lids and the Level 2 lobby ceiling plane at 12'-11 3/8" above Level 2; lobby feature drop not modeled.

## 10. Exterior walls as seen from inside (`BASE_Exterior`)

The v001–v013 exterior is a set of solid masses, which cannot be looked into. v014 therefore adds an inside shell built from the **same** face-of-stud polygons, the **same** A003 outer build-ups and the **same** opening list as v013 — no opening is moved or resized. Wall = outer finish face to inside face of gypsum: 6" stud + ⅝" gypsum inside the face of stud (**W** A003). New clear glass panes fill the openings. The solid masses, their opening panels and the cutters stay in the file unchanged; they are switched off only while the interior views are rendered, and switched back on before saving.

## 11. Unresolved conflicts

1. **Level 1 usable area vs. Rev 5.** The 09/23/2025 area plan shows the smaller pre-Rev 5 electrical room.
2. **Stair 2 south wall at Level 2** (y 59.4) sits 1.8 ft inside the exterior face-of-stud line F' (57.6) used for the v001–v013 mass. Both are kept; the space between is treated as wall cavity.
3. **Usable-area plan vs. A122 at Level 2**: the area plan includes the strip to terrace door 200D in tenant usable area, while A122/A420 label it as part of Level 2 Lobby 204. Modeled as common (A420).
4. Architectural revisions 6–10 are not in hand (carried). Electrical revisions to rev 10 exist; any later change to the electrical room is not reflected.
5. Carried from exterior phases: sun-shade drawings-vs-spec conflict, unresolved finishes.

## 12. Assumptions

Column orientation and offset directions · Stair 2 mid-landing height and run widths outside the measured tread lines · stair and railing simplifications · door head 7'-0" for all interior openings except 101A · wall heights: rated walls run to the underside of the deck above (A003 **W** "slab structure or decking above"); room lids at the RCP height · shaft walls continuous from Level 2 floor to roof deck · glass pane 1" thick at the v013 glass plane.

## 13. Intentionally excluded

Tenant partitions, furniture, workstations, casework, decorative ceilings, finishes, prospective layouts, branding, people, vehicles · floor framing (beams/joists), bracing, fireproofing wraps · plumbing fixtures and toilet accessories · elevator car and equipment · MEP equipment, ducts, risers inside shafts, panels · lighting · door leaves, frames, hardware · lobby millwork, banquette and feature wall (ID sheets) · the future emergency electrical room walls.
