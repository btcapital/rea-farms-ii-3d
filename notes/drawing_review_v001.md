# Drawing review v001 — source set for the first building model

Review date: 2026-09-18
Scope: identify the correct construction-document set for exterior geometry. **No modeling was done.**
All paths are relative to `source_documents\`. Nothing in `source_documents` was modified, moved, or renamed.

Method: title blocks were read from the PDF text layer page-by-page (sheet number, issue date, revision list), then the key sheets were rendered to images and inspected visually (cover sheet, A112, A122, A132, A300, A301, A302, A320, A700, civil CS-101 and its title blocks). Dates below are **printed on the sheets**, not Windows file dates.

Note: a folder `notes\drawing_review_v001_previews\` already existed from an earlier, unfinished session (page images + a text dump, no report). It was left untouched. Findings here were re-derived independently from the source PDFs; the images in that folder are consistent with them and can be used as quick visual references.

---

## 1. Building identified

| Item | Printed on drawings |
| --- | --- |
| Project name | **Carolina Sports MOB** (file names abbreviate it "CSMC MOB 2") |
| Address | **11425 Golf Links Drive, Charlotte, NC 28277** |
| Owner | 11425 Golf Links Dr, LLC |
| Architect | McMillan Pazdan Smith Architecture — MPS Project No. 025043.00 |
| Civil / landscape | V3 Southeast — Project No. 241355 |
| Structural | Moore Lindner Engineering |
| Contractor | Edifice |
| Permit | Mecklenburg County stamp **COS-001319, 1/30/2026** |

- The civil Dimension Control Plan (CS-101) labels the subject as **"Proposed two-level medical office building 'Building II', FFE 660.30"**, directly west of **"Existing two-level mixed use building 'Building I', FFE 661.75"** on the same block.
- So there is **one building to model: Building II** (two levels plus a partial rooftop terrace). Building I is existing context only and no architectural drawings for it were found in `source_documents`.
- Design phases printed in the sheet-issue blocks: A 05/22/2025 Schematic Design → B 06/19/2025 Design Development → (C 08/18/2025, structural only) → D 09/12/2025 95% Check Set → E 09/29/2025 Permit Set → numbered revisions after permit.

## 2. Drawing sets found, in date order

| Set | File(s) | Printed status | Use |
| --- | --- | --- | --- |
| DD Set | `00 PLANS\DD Set\2025.06.19 - Carolina Sports MOB 2 - DD Set.pdf` | 06/19/2025 Design Development | Superseded — do not use |
| 95% Check Set | `00 PLANS\95% Check Set\*.pdf` | 09/12/2025 | Superseded — do not use |
| Permit / Pricing set | `00 PLANS\Permit_Pricing CDs 09.30.25\*.pdf` | 09/29/2025 Permit Set (issue E) | Superseded by approved set |
| **Approved permit set** | `00 PLANS\Approved Set\APPROVED-COS-001319.pdf` (161 pages, all disciplines) | Cover: "12/12/2025 Cycle 1 Comments" (Rev 3); county approval stamp 1/30/2026 | **BASELINE** |
| Approved civil | `00 PLANS\Approved Civil\APPROVED-LDCP-2025-00715.pdf` (20 pages) | Civil revs to 12.12.25 / 01.08.26; also contains zoning sheets A010A, A300A, A320 | Site reference |
| **Revision 5** (partial reissue) | `00 PLANS\Revision 5\03 Architectural_…REV 5 2026.02.27.pdf` (17 sheets), `04 Structural…` (18 sheets), `08 Electrical…`, `_00 REVISION LOG 2026.02.27…pdf` | 02/27/2026 Revision 05, sealed 2/27/26 | **OVERLAY — supersedes matching baseline sheets** |
| Civil after Rev 5 | `00 PLANS\Revision 5\Rea Farms 2 - Civil Drawings 03.17.26.pdf` (15 sheets) | CS-101 and CG-101 carry rev 6, 03.10.26 "Wall Revisions" | **Latest civil** |
| Approved revision RV-001 | `00 PLANS\APPROVED-COS-RV-001319-001.pdf` (6 sheets) | Electrical sheets only, revs 8 (04/21/2026) and 10 (05/06/2026) | Not needed for geometry (see conflicts) |

## 3. Recommended source set

**Approved permit set (Rev 3) as the baseline, with every Revision 5 sheet replacing the same-numbered baseline sheet.** The Revision 5 log states that only modified sheets were reissued and each is "reissued in its entirety", so this combination is the most current consistent architectural set in the folder.

Revision 5 architectural changes per the log: enlarged electrical room, exterior lighting added, roof hatch revised, miscellaneous clarifications. Visually, the Rev 5 clouds on the elevations are around the louvered sun-shade and new wall sconces. None of this changes the overall footprint or level heights.

### 3a. Key modeling sheets

"Rev 5" = `00 PLANS\Revision 5\03 Architectural_CSMC MOB 2_REV 5 2026.02.27.pdf`
"Approved" = `00 PLANS\Approved Set\APPROVED-COS-001319.pdf`

| Need | Sheet | Title | Use this file | PDF page | Latest printed revision |
| --- | --- | --- | --- | ---: | --- |
| Identity / index | G001 | Cover Sheet | Approved | 143 | 3 — 12/12/2025 |
| Footprint, Level 1 | **A112** | Level 1 Dimension Plan | **Rev 5** | 3 | 5 — 02/27/2026 |
| Level 2 + terrace | **A122** | Level 2 Dimension Plan | Approved (not reissued in Rev 5) | 25 | 3 — 12/12/2025 |
| Roof / parapets | **A132** | Roof Dimension Plan | **Rev 5** | 4 | 5 — 02/27/2026 |
| Roof deck | A193 | Roof Deck Plan | Rev 5 | 6 | 5 — 02/27/2026 |
| Elevations N, E | **A300** | Building Elevations (+ material legend) | **Rev 5** | 8 | 5 — 02/27/2026 |
| Elevations S, W | **A301** | Building Elevations | **Rev 5** | 9 | 5 — 02/27/2026 |
| Terrace / screening elevations | A302 | Building Elevations (amenity deck, west screening) | Approved | 33 | 3 — 12/12/2025 |
| Building sections | **A320** | Overall Building Sections | Approved | 34 | 3 — 12/12/2025 (also 2 — 10/27/2025 zoning) |
| Wall sections | A330, A331 | Wall Sections | Rev 5 | 10, 11 | 5 — 02/27/2026 |
| Wall sections | A332 | Wall Sections | Approved | 37 | E — 09/29/2025 |
| Parapet / roof details | A340, A345 | Section Details / Roof | Approved | 38, 40 | E — 09/29/2025 |
| Parapet details | A341 | Section Details | Rev 5 | 12 | 5 — 02/27/2026 |
| **Entrance canopy** | **A700** | Drop-Off Canopy Plans & Sections | **Rev 5** | 13 | 5 — 02/27/2026 |
| Other canopies | A701, A702 | Canopy Plans & Sections | Approved | 49, 50 | E — 09/29/2025 |
| Openings | A811 | Storefront Elevations / Types | Approved | 52 | E — 09/29/2025 |
| Openings | A815 | Curtain Wall Frame Elevations / Types | Rev 5 | 14 | 5 — 02/27/2026 |
| Openings | A816 | Curtain Wall Frame Elevations / Types | Approved | 55 | E — 09/29/2025 |
| Utility yard / screen walls | A012 | Utility Yard Plan & Sections | Rev 5 | 2 | 5 — 02/27/2026 |
| Arch. site plan | A010 | Architectural Site Plan | Approved | 22 | E — 09/29/2025 |
| Cross-check only | S114, S123, S133 | Parapet girt, roof deck edge, canopy framing | `Revision 5\04 Structural_…pdf` | 7, 9, 10 | 5 — 02/27/2026 |

### 3b. Civil / site

| Sheet | Title | File | PDF page | Latest printed revision |
| --- | --- | --- | ---: | --- |
| **CS-101** | Dimension Control Plan (shows Building II and Building I, FFE 660.30) | `00 PLANS\Revision 5\Rea Farms 2 - Civil Drawings 03.17.26.pdf` | 7 | 6 — 03.10.26 "Wall Revisions" |
| CG-101 | Grading & Drainage Plan | same | 3 | 6 — 03.10.26 |
| CS-301 | Dimension Control Plan – Rooftop | same | 11 | Permit set 09/29/2025 |
| CS-100 | Overall Dimension Control Plan | same | 6 | none listed |

### 3c. Exterior finish information

The **Elevation Material Legend** is printed on A300, A301 and A302 (use Rev 5 A300, PDF p.8):
ACM-1/ACM-4 Alucobond panels "Bone White"; ACM-2/ACM-3 Alucobond "Tri-Corn Black"; BRK-1 Endicott brick veneer, utility size, "Manganese Ironspot", ultra-dark mortar; BC-1/BC-2 brick caps; GR-1 Viva glass railing; MTL-1/2/3 metal and aluminum copings. Per project rules, finishes come **after** geometry is approved — recorded here for later only.

### 3d. Key values confirmed on the rendered sheets (for orientation, not yet for modeling)

- Overall grid dimensions on A112: **205'-0"** (grid 1' to 12') × **105'-10"** (grid A' to K').
- Level datums on A300/A301/A320: Average Grade −1'-9 3/4"; Level 01 FF 0'-0"; Terrace FF 15'-2"; Level 02 FF 16'-0"; Low Parapet 1 17'-6"; Low Parapet 2 19'-6"; Roof Structure 32'-0"; High Parapet 1 34'-11"; High Parapet 2 42'-0"; High Parapet 3 43'-10".
- Level 2 is set back from the Level 1 footprint, with an L-shaped "Partial Rooftop Terrace" on the east and south and a louvered sun-shade above it.
- Drop-off canopy: glazed, steel-framed, on column line XA north of the lobby (A700).

## 4. CAD / BIM / 3D files

| File | Finding |
| --- | --- |
| `00 PLANS\CAD Files\Carolina Sports MOB - A112 - LEVEL 1 DIMENSION PLAN.dwg` | AutoCAD 2013-format DWG, 553 KB. **No printed revision inside that I can read**, so it is unknown whether it matches Rev 3, Rev 5 or another state. |
| `00 PLANS\CAD Files\Carolina Sports MOB - A122 - LEVEL 2 DIMENSION PLAN.dwg` | AutoCAD 2018-format DWG, only 48 KB — may be largely empty or depend on external references. Not opened. |

- No Revit (.rvt), IFC, SketchUp, or other 3D model files exist in `source_documents`. The four .zip files contain only photos and one PDF.
- Blender cannot open DWG directly. Using these would require converting to DXF with software that is not installed, so **they are not required for the first scope**; the dimensioned PDFs are sufficient. If used later, they must be checked against Rev 5 A112 before being trusted.

Reference-only images (not dimensional sources): architect perspectives in `Photos\8.3A_*.png` and `Photos\Compiled Perspectives RF2.pdf`; construction drone photos in `Photos\8.29.26 Drone Photos\` and `Photos\Edifice Drone\`. The renders in `Photos\9.1.26 Renders\` are of unknown origin and should not be treated as design documents.

## 5. Conflicts and unclear revisions

1. **Civil revision numbering conflict.** CS-101 exists twice with the same 02.11.26 seal date: in `02 Civil & Landscape_…REV 5 2026.02.12.pdf` it is labelled "**5** – 02.11.26 – Revision 5"; in `Rea Farms 2 - Civil Drawings 03.17.26.pdf` the same date is labelled "**4** – 02.11.26 – Revision 4", followed by "6 – 03.10.26 – Wall Revisions". The 03.10.26 sheet is the later one and is recommended, but the numbering is inconsistent. Also, the file name says 2026.02.12 while the sheet says 02.11.26.
2. **Revision log vs. civil.** The Rev 5 log says "Civil – no revisions included", yet a civil CS-101 marked Revision 5 is in the Rev 5 folder.
3. **Later revisions exist that are not in the folder.** The approved revision package RV-001 shows electrical revisions **8 (04/21/2026) and 10 (05/06/2026)**. Revisions 6, 7 and 9 are not present for any architectural sheet. It is unknown whether any of revisions 6–10 touched architectural sheets. The 03.10.26 civil "Wall Revisions" (rev 6) suggests at least site walls changed after Rev 5.
4. **Rev 5 not shown as county-approved.** The Rev 5 architectural sheets carry the architect's seal (2/27/26) but no county approval stamp; the stamped approved set is Rev 3.
5. **Mixed revision levels by design.** Because Rev 5 is partial, the working set mixes Rev 5 sheets (A112, A132, A300, A301, A700…) with Rev 3/E sheets (A122, A302, A320, A701, A702…). This is normal, but A122 (Level 2) and A320 (sections) will not show Rev 5 changes such as the revised roof hatch.
6. **A122 dimension to verify.** A122 shows an overall string of 205'-0" at the top and a 203'-0" string at the bottom. This is probably measured between different grid lines, not an error, but it must be read carefully at modeling time rather than assumed.
7. **Zoning variants.** Sheets A010A / A300A (zoning versions, revs 2 and 4, 10/27/2025 and 12/09/2025) exist only inside the approved civil package. They should not be mixed with A010 / A300.
8. **Test-fit plans** in `00 PLANS\Test Fits\` (including a 06/25/2026 plan and an "A122 …_r1.pdf") are interior tenant layouts. They were not reviewed in depth and are not exterior sources; if any of them moves an exterior door or window, that is not yet reflected in the architect's set.

## 6. Missing information

- Architectural sheets for revisions 6–10, if any were issued (see conflict 3).
- A Rev 5-era Level 2 plan and building sections (none reissued; presumably unchanged).
- Any architect BIM/3D model; DWGs have no readable revision.
- Drawings for existing Building I (only its outline appears on civil sheets).
- Canopy and sun-shade colors are noted "COLOR TBD" on A700.
- Signage is "Future signage by others" on the elevations — no geometry documented.
- Rooftop mechanical units are shown as "Future Unit(s)" with approximate locations only.
- Site grading is on CG-101 but was not reviewed in detail; the first scope assumes a flat base at Level 01 = 0'-0" with Average Grade −1'-9 3/4" noted.

Nothing above will be guessed. Where a dimension is not printed, it will be listed as an open item rather than estimated.

## 7. Proposed first modeling scope (for approval — not started)

A simple untextured massing model of **Building II only**, built strictly from printed dimensions:

1. **Exterior footprint** — Level 1 outline from Rev 5 A112 (grid and face-of-wall dimensions); Level 2 outline and terrace edge from Approved A122.
2. **Floor levels** — Level 01 0'-0", Terrace 15'-2", Level 02 16'-0", Roof Structure 32'-0" from A300/A301/A320.
3. **Roof and parapets** — parapet tops at 17'-6", 19'-6", 34'-11", 42'-0", 43'-10" placed per the "TO PARAPET" tags on Rev 5 A132.
4. **Major exterior openings** — storefront and curtain-wall openings as plain recessed rectangles, located from A112/A122 and sized from A300/A301 with A811/A815/A816. No mullions, doors, or glass detail yet.
5. **Entrance canopy** — drop-off canopy from Rev 5 A700 as simple slabs and columns. Smaller door canopies (A701/A702) only if fully dimensioned.

Excluded from the first pass: materials and colors, louvered sun-shade detail, glass railings, utility yard/screen walls, site, landscaping, signage, rooftop equipment, interiors.

Each item would be saved as a new versioned .blend; nothing existing would be overwritten.

## 8. Summary

- One building: **Carolina Sports MOB ("Building II"), 11425 Golf Links Drive, Charlotte NC 28277**, by McMillan Pazdan Smith, project 025043.00.
- Use the **county-approved permit set (COS-001319, Rev 3, 12/12/2025) overlaid with the Revision 5 sheets (02/27/2026)**. Latest civil is the 03.17.26 package (CS-101 rev 6, 03.10.26).
- All geometry needed for the first scope is present and dimensioned in PDF. The two DWGs are optional and unverified; there is no BIM/3D model.
- Main uncertainty: revisions 6–10 exist for other disciplines, and it is unknown whether architectural sheets changed after Rev 5.

## 9. Questions

1. Do you have (or can you ask McMillan Pazdan Smith / Edifice for) any **architectural sheets issued after Revision 5** — revisions 6 through 10 — or confirmation that none affected the exterior?
2. Should the model follow the **drawings as issued (Rev 5)**, or should I also flag visible differences against the August 2026 drone photos of the actual construction?
3. Is the **proposed first scope in section 7 approved** as written, including leaving out the sun-shade, railings and utility yard for now?

**Stopped here. No modeling has been started; waiting for approval.**
