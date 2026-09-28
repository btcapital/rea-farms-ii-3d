# Model control document v001 — Building II geometry validation shell

Date: 2026-09-18
Applies to: `scripts/build_shell_v001.py` → `models/building_shell_v001.blend`
Purpose: record, before geometry is built, where every major dimension comes from, what is assumed, and what is unresolved. **This is a geometry validation model only — no finishes, no site detailing.**

## 1. Source set (as approved by owner 2026-09-18)

- Base: county-approved permit set `source_documents\00 PLANS\Approved Set\APPROVED-COS-001319.pdf` ("Approved").
- Overlay: `source_documents\00 PLANS\Revision 5\03 Architectural_CSMC MOB 2_REV 5 2026.02.27.pdf` ("Rev 5") wherever it reissues the same sheet.
- Site context: CS-101 rev 6 (03.10.26) in `source_documents\00 PLANS\Revision 5\Rea Farms 2 - Civil Drawings 03.17.26.pdf`, PDF p.7.
- The architectural drawings are the source of truth. Construction photos are compared separately in `notes/photo_discrepancy_log_v001.md` and do not change geometry without owner approval.

**Open verification item V-1:** No architectural sheets for revisions 6–10 are in the project folder, and there is no confirmation that the exterior was unchanged after Revision 5. Later electrical revisions (8, 10) are *not* assumed to have changed the exterior. To be confirmed with McMillan Pazdan Smith / Edifice.

## 2. How dimensions were obtained — confidence codes

| Code | Meaning |
| --- | --- |
| **W** | Written dimension or datum printed on the sheet. Governs. |
| **G** | Position of a named grid line. Grid spacing was cross-checked: the vector linework in the sealed PDFs reproduces every written grid dimension checked (top, bottom and left strings of A112; 27'-11" and 1'-7" on A122; 28'-7" / 32'-8 1/4" on A700) to within 0.01 ft, so the PDFs are exact-scale exports. |
| **M** | No written dimension found; value measured from the exact-scale vector linework (plans, ±0.02 ft) or from the 200-dpi raster of the shaded elevations (openings, ±0.1 ft). To be replaced by a written value if one is found. |
| **A** | Assumption — not documented on the sheets reviewed. Listed in section 8. |

No dimension was taken from photographs or from the conceptual rendering.

## 3. Unit system and coordinate origin

- Working unit: **decimal feet**, from the drawings' feet-and-inches. Blender scene is metric internally at true scale (1 ft = 0.3048 m exactly) with display set to Imperial/feet, so exports are real-world size.
- **Origin (0,0,0): intersection of grid line 1' and grid line K' at Level 01 finish floor (0'-0").** This is the south-west corner of the 205'-0" × 105'-10" overall dimension box on A112.
- **+X = project east** (increasing grid numbers 1 → 12). **+Y = project north** (grid letters K → A). **+Z = up.**
- "Project North" is the arrow on A112. On civil sheet CS-101 the building is drawn square to the sheet with north up, so project north is taken as plan north (A-1).
- Front of building = **north** face (lobby, drop-off canopy, parking lot, Golf Links Dr beyond). Rear = south (North Rea Park Ln). Existing Building I is to the **east**.

## 4. Floor, roof and parapet datum table

Source: level heads on Rev 5 A300 (p.8) and A301 (p.9); Approved A302 (p.33), A320 (p.34). All **W**. Identical on every sheet checked.

| Datum | Elevation | Decimal ft |
| --- | --- | ---: |
| Average Grade | −1'-9 3/4" | −1.8125 |
| Level 01 – Finish Floor | 0'-0" | 0.000 |
| Terrace – Finish Floor | 15'-2" | 15.167 |
| Level 02 – Finish Floor | 16'-0" | 16.000 |
| Low Parapet 1 | 17'-6" | 17.500 |
| Low Parapet 2 | 19'-6" | 19.500 |
| Roof Structure | 32'-0" | 32.000 |
| High Parapet 1 | 34'-11" | 34.917 |
| (parapet at CW2 bay, A132 tag) | 38'-9 1/2" | 38.792 |
| High Parapet 2 | 42'-0" | 42.000 |
| High Parapet 3 | 43'-10" | 43.833 |

Civil: Building II FFE = 660.30 (CS-101, **W**); Building I FFE = 661.75. The model uses Level 01 = 0.

## 5. Building grid (Rev 5 A112 p.3; identical grid positions on Approved A122 and Rev 5 A132)

Overall (**W**): 205'-0" (grid 1' to 12') × 105'-10" (grid A' to K').

Numbered grids — X in ft from grid 1' (**G**, with the written strings that fix them):

| Grid | X | Grid | X | Grid | X |
| --- | ---: | --- | ---: | --- | ---: |
| 1' | 0.000 | 6' | 82.875 | 8.4 | 125.378 |
| 1 | 1.500 | 7 | 92.500 | 9 | 143.500 |
| 1.2' | 5.000 | 7' | 94.125 | 9' | 144.500 |
| 2 | 6.000 | 7.1' | 94.375 | 9.1 | 145.125 |
| 3 | 32.500 | 7.2 | 95.500 | 9.1' | 147.875 |
| 3.1 | 34.500 | 8' | 104.646 | 10 | 172.411 |
| 4 | 59.000 | 8 | 105.500 | 11 | 202.000 |
| 5 | 65.500 | 8.3 | 115.500 | 11' | 203.000 |
| 6 | 80.500 | | | 12 / 12' | 203.500 / 205.000 |

Written strings used: top of A112 1'-6" + 92'-10 1/2" + 10'-3 1/4" + 10 1/4" + 38'-0" + 1'-0" + 59'-0" + 1'-6" = 205'-0"; bottom 5'-0" … 11'-3", 1'-4 1/2", 49'-7 1/2", 2'-9", 54'-1 1/2", 1'-0", 2'-0".

Lettered grids — Y in ft from grid K':

| Grid | Y | Grid | Y | Grid | Y |
| --- | ---: | --- | ---: | --- | ---: |
| K' | 0.000 | G | 50.944 | C | 83.789 |
| K | 1.833 | F' | 57.604 | B | 96.833 |
| J' | 2.000 | F | 58.789 | B' | 97.833 |
| J | 3.833 | E.4 | 65.944 | A | 103.333 |
| H' | 23.056 | E | 71.833 | A.1' | 104.917 |
| H | 24.533 | D | 77.378 | A' | 105.833 |
| | | | | XA (canopy) | 113.311 |

Written strings used: left of A112 11" + 1'-7" + 45'-8 3/4" + 55'-9 1/4" + 1'-10" = 105'-10". Lettered grids not covered by that string are **G** from vector positions.

**Control-line convention.** A112 Floor Plan Note 3: exterior dimensions are to **face of stud**. The primed grids (1', 1.2', 6', 7', 7.1', 8', 9', 9.1', 11', 12', A', A.1', B', F', H', J', K') lie on the exterior stud faces, confirmed against the wall linework. **The model surfaces are placed on these stud-face control lines.** Cladding thickness outside the stud face (brick veneer zone measures about 0.75 ft on plan; curtain wall about 0) is *not* added in v001 — see U-1.

## 6. Geometry schedule and source of each major dimension

### 6a. Level 1 footprint (podium, Z 0 → 15.167) — Rev 5 A112

Vertices (X,Y), counter-clockwise from SW: (5,0) 1.2'/K' → (82.875,0) 6' → (82.875,2) J' → (94.125,2) 7' → (94.125,0) → (147.875,0) 9.1' → (147.875,2) → (203,2) 11' → (203,23.056) H' → (205,23.056) 12' → (205,97.833) B' → (144.5,97.833) 9' → (144.5,105.833) A' → (104.646,105.833) 8' → (104.646,104.417) → (94.375,104.417) 7.1' → (94.375,104.917) A.1' → (0,104.917) 1' → (0,57.604) F' → (5,57.604).

- All vertices are primed-grid intersections (**G/W**) except the 6" setback of the CW2 bay between 7.1' and 8' (Y = 104.417, **M**).
- Lobby front (between 8' and 9'): two piers 3'-8" wide (**W**, A112 second top string 94'-4 1/2", 10'-3 1/4", 3'-8", 32'-6 1/4", 3'-8", 60'-6") with their north face on A'; glazing between them on grid A, i.e. recessed 2'-6" (**W**: 11" + 1'-7").

### 6b. Level 2 enclosed footprint (Z 15.167 → 32.0) — Approved A122, Rev 5 A132

- West wall X = 30.500: 25'-6" east of 1.2' (**W**, A122).
- East wall X = 174.000 (rounded from 173.994): grid 10 + 1'-7" (**W**, A122 "27'-11"" from 9' to 10, then "1'-7"").
- South wall Y = 22.950: grid H + 1'-7" south (**M**; matches the 1'-7" offset used on the east side, wall linework centred on it).
- North wall of east wing Y = 78.961: grid D + 1'-7" north (**M**, same logic).
- North and west faces of the west block and lobby block: same control lines as Level 1 (1', A.1', A', 8', 9').
- Three roof zones, all with roof structure at 32'-0" (**W**):
  - **High block** X 0 → 104.646, Y 57.604 (F') → 104.917. Parapet 42'-0" (**W**, A132 tags ×3; A300/A301). North parapet of the CW2 bay (7.1' → 8') 38'-9 1/2" (**W**, A132 tag; equals 42'-0" minus the 3'-2 1/2" shown on A300).
  - **Lobby block** X 104.646 (8') → 144.5 (9'), Y 48.789 → 105.833 (A'). Parapet 43'-10" (**W**, A132 tags ×3). South limit Y = 48.789 is **M** from A132 linework.
  - **Low roof** = remainder of the Level 2 footprint. Parapet 34'-11" (**W**, A132 tags ×3).

### 6c. Terrace (Level 1 roof not covered by Level 2) — Approved A122 / Rev 5 A132

- Terrace finish floor 15'-2" (**W**).
- Perimeter parapet 19'-6" (**W**, A132 tags on south, east, north and west runs), except 17'-6" (**W**, A132 tags) at the south recess between 6' and 7', along the J' face from 9.1' to 11', and the 11' face up to H' (A301/A300 show glass railing GR-1 above these — not modeled).

### 6d. Major exterior openings — plain rectangles

Horizontal positions: **W** where the A112/A122 dimension strings give rough openings (south face 10'-0" windows at 5'-0" piers starting 18'-6" from 1.2'; 45'-0" opening on the J' face; 25'-0" openings on the north face of the east wing and along Level 2). Otherwise **M** from plan linework / elevation raster. Sill and head heights: **M** from the shaded elevations Rev 5 A300/A301 (not yet cross-checked against frame elevations A811/A815/A816 — see U-3).

| Face (plane) | Along-face range (ft) | Z range (ft) | Drawing tag |
| --- | --- | --- | --- |
| North, high block (Y 104.917) | X 0.0 – 89.8 | 0.21 – 28.77 | CW3 (door 100A and ACM-4 infill inside it not modeled) |
| North, CW2 bay (Y 104.417) | X 95.05 – 104.05 | 0.21 – 14.97 and 18.25 – 28.77 | CW2 (middle band is hidden by the canopy in elevation) |
| North, lobby (Y 103.333, recessed) | X 108.69 – 140.29 | 0.21 – 9.81 and 18.25 – 28.77 | CW1 / door 101A |
| North, east wing (Y 97.833) | X 145.63 – 170.63; 175.63 – 200.63 | 3.09 – 13.77 | SF3 ×2 (25'-0" W) |
| North, Level 2 east wing (Y 78.961) | X 151.77 – 173.29; 146.97 – 149.97 | 19.81 – 28.77; 24.09 – 28.77 | SF5B; SF5A |
| East (X 205) | Y 33.88 – 48.36 | 3.14 – 9.78 | storefront under side canopy |
| East (X 205) | Y 53.68 – 63.36; 68.64 – 93.36 | 3.14 – 13.78 | SF1 / SF2 |
| East (X 203) | Y 7.20 – 16.96 | 0.10 – 13.82 | entrance storefront |
| East, Level 2 (X 174) | Y 23.68 – 48.36; 53.68 – 78.36 | 19.82 – 28.78 | SF6 ×2 |
| East, lobby block (X 144.5) | Y 83.68 – 96.76 | 19.82 – 28.78 | SF7 |
| South (Y 0) | X 23.5–33.5, 38.5–48.5, 53.5–63.5, 68.5–78.5, 103.5–113.5, 118.5–128.5, 133.5–143.5 | 3.09 – 13.77 | SF1 ×7 (10'-0" W) |
| South (Y 2.0) | X 153.47 – 198.47 | 3.05 – 13.81 | 45'-0" W storefront |
| South, Level 2 (Y 22.95) | X 38.67–63.33, 68.67–93.33, 98.67–113.33, 118.67–143.33, 148.67–173.33 | 19.81 – 28.77 | SF6 ×5 |
| West (X 5) | Y 4.35 – 14.03 | 3.18 – 13.78 | SF1 |
| West, Level 2 (X 30.5) | Y 25.55 – 50.27 | 19.82 – 28.78 | SF6 |
| West, high block (X 0) | Y 74.07 – 104.83 | 0.22 – 28.82 | CW4 |

### 6e. Drop-off canopy — Rev 5 A700 (p.13)

- Plan size 65'-7 1/4" × 23'-3" (**W**). Columns X1, X2, X3 on grid XA: 2'-2" from the west end, then 28'-7" and 32'-8 1/4", 2'-2" to the east end (**W**). X1 = 79.644, X2 = 108.233, X3 = 140.922 (**G**, A112).
- Canopy extends 6'-7 1/2" south of XA and 16'-7 1/2" north (**W**). Roof slope 1 1/2" per 12" draining to a gutter on XA (**W**).
- **Heights are not written on A700.** Measured from section A5/A700: top of glass at the gutter ≈ 16.1 ft, top of column ≈ 15.0 ft (**M**, ±0.2 ft). Edge heights then follow from the written slope. See U-4.

### 6f. Site context (minimal, for orientation only)

Flat ground plane at Average Grade −1'-9 3/4" (**W** value, **A** that it is flat); north arrow; text markers for Golf Links Dr (north) and existing Building I (east). Building I is **not modeled** — no drawings, and its height is undocumented.

## 7. Unresolved conflicts and items (carried into the shell)

| ID | Item | Effect on v001 |
| --- | --- | --- |
| V-1 | Architectural revisions 6–10 not in hand. | Shell follows Rev 5 / Rev 3. |
| U-1 | Exterior finish thickness beyond face of stud not added (wall types on A003 not yet applied). Brick faces would sit roughly 9" outside the modeled surface. | Overall model is 205'-0" × 105'-10" to stud face, not to finished face. |
| U-2 | A122 carries a 205'-0" string (top) and a 203'-0" string (bottom). 203'-0" = 1.2' to 11' + … is between different grids; not a conflict for this model, recorded for completeness. | None. |
| U-3 | Opening sill/head heights are measured from shaded elevations, not yet read from A811/A815/A816 frame elevations. | ±0.1 ft on opening heights. |
| U-4 | Drop-off canopy heights not dimensioned on A700; column size not confirmed. | Canopy heights ±0.2 ft. |
| U-5 | Level 2 plan and sections were not reissued in Rev 5 (roof hatch change not shown on A320). | None for exterior massing. |
| U-6 | Civil revision label conflict on CS-101 (same 02.11.26 date labelled "Revision 5" in one file and "Revision 4" in the other). Rev 6 (03.10.26) used. | Site context only. |
| U-7 | Site grade is modeled flat at Average Grade; A320/A301 show grade falling toward the west (utility yard). | Visual only. |

## 8. Assumptions

| ID | Assumption |
| --- | --- |
| A-1 | Project north = plan north of CS-101 (building drawn square to sheet, north arrow up). |
| A-2 | Parapets modeled as 1'-0" thick walls set inside the control line. Actual thickness not taken from wall sections yet. |
| A-3 | Roof surfaces modeled flat at Roof Structure 32'-0" and terrace at 15'-2"; roofing build-up and slopes ignored. |
| A-4 | Openings are 0.5 ft deep plain recesses with a darker neutral panel; no frames, mullions, doors or glass. |
| A-5 | Lobby recess (between the piers) is modeled continuous from 0 to 28.77 ft; the band between the lower and upper glazing is left as plain wall in the recessed plane. |
| A-6 | Canopy columns modeled as 14" square posts; tapered steel beams, purlins and gutter omitted. Canopy glass modeled as two 3" thick sloped slabs. |
| A-7 | Upper masses start at Terrace FF 15'-2" (not Level 02 FF 16'-0") so there is no gap at the podium top. |

## 9. Deliberately not modeled in v001

Materials/colors, signage, landscaping, curtain-wall mullions, doors (including solid doors 001A/001B/110B not detected as glazing), louvered sun-shade (outline is documented on A132 — candidate for next pass), glass railings GR-1, smaller door/side canopies (A701/A702), utility yard and transformer/generator screen walls (A012), the small Level 2 terrace closet at X≈30–33.5, Y≈10–23 (A122), rooftop equipment and roof hatch, interiors, MEP, Building I.
