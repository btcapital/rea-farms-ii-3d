# Building I — drawing revision review and source control v002

Review date: 2026-09-22 (v001 review); owner decisions recorded 2026-09-22 (this v002)
v002 = v001 unchanged in sections 1–4, plus the owner's source-control decisions in section 5 replacing the v001 recommendation and questions. `BI_revision_review_v001.md` is kept as the original review record.
Scope: establish the revision history of the Building I (Rea Farms Sports Medicine Center, 11415 Golf Links Drive) construction documents and recommend the base set for a future model. **No modeling was done.** Sources are read-only; see `BI_source_inventory_v001.md` for the full inventory.

Method: for both combined PDF sets, every page's title block was read from the PDF text layer (sheet number after the "SHEET NUMBER" label, sheet name after "SHEET NAME", revision rows "N Description Date"), then the cover sheets and the A1.01 title blocks were rendered to images and checked by eye. Tables: `BI_sheet_index_rev6_v001.tsv`, `BI_sheet_index_rev14_v001.tsv`, `BI_sheet_revision_comparison_v001.tsv`.

---

## 1. Revision history (from the Rev 14 cover, verified against the A1.01 title block)

| Rev | Description (printed) | Date (printed) | Where it lands | GC change-order reference |
| --- | --- | --- | --- | --- |
| — | Construction Documents | 10/25/2024 | both sets | — |
| 1 | Interactive Review | 09/09/2024 | both | — |
| 2 | County Permit Comments | 09/27/2024 | both | PCO 3 "Permit Drawing Changes" (void) |
| 3 | Interactive Review | 10/09/2024 | both | — |
| 4 | Interactive Review | 10/18/2024 | both | PCO 4/5 "RTAP #1 Drawing Changes" |
| 5 | Interactive Review | 10/31/2024 | both | — |
| **6** | **RTAP Owner Changes** | **11/15/2024** | **Rev 6 set = this issue** | — |
| 7 | RTAP Interiors Changes | 1/20/2025 | Rev 14 only | PCO 10 "RTAP #2 – Drawing Changes (Revision 7)" |
| 8 | RTAP2 Comments | 2/14/2025 | Rev 14 only | PCO 12 "RTAP #2 – Civil Drawings" |
| 9 | Owner Changes | 3/28/2025 | Rev 14 only | PCO 14 "RTAP 3 – Revision 9 Drawing Set" |
| 10 | RTAP3 Comments | 5/6/2025 | Rev 14 only | — |
| 11 | Owner Changes | 5/22/2025 | Rev 14 only | PCO 18 "Building Drawing Revisions 11 and 12" |
| 12 | Owner Changes | 6/16/2025 | Rev 14 only | PCO 18 |
| 13 | Design Coordination | 7/25/2025 | Rev 14 only | PCO 23 "Drawing Revision 13"; PCO 32/34 |
| **14** | **MEP Changes** | **9/25/2025** | **Rev 14 set = this issue** | PCO 38 (RFI 92 water heater / mop sink), PCO 40 "Drawing Revision 14" |

Notes:

- The Rev 6 cover (11/15/2024) lists revisions 1–6 with the same descriptions and dates, so the two sets share one revision sequence; Rev 14 is a complete re-issue of every sheet plus new sheets.
- Edifice's PCO titles call revision 7 "RTAP #2" while the architect's schedule calls revision 8 "RTAP2 Comments". This is a naming difference between GC and architect only; sheet dates are consistent.
- Per-sheet revision *dates* in the text layer are not reliable (the date column drifts one row in extraction); the revision *numbers* per sheet are reliable and were spot-checked on A1.01 (Rev 6 set lists 4, 5, 6; Rev 14 set lists 4, 5, 6, 7, 9, 12, 13, 14).

## 2. What changed between Rev 6 and Rev 14

Counts from `BI_sheet_revision_comparison_v001.tsv` (213 sheets in Rev 14):

| Highest revision listed on the sheet | Sheets |
| --- | --- |
| none listed | 37 |
| 4 or 5 | 4 |
| 6 (unchanged since the approved issue) | 36 |
| 7 | 11 |
| 8 | 1 |
| 9 | 15 |
| 10 | 2 |
| 11 | 6 |
| 12 | 40 |
| 13 | 44 |
| 14 | 17 (16 sheets plus the cover G0.00, whose schedule lists all 14) |

- **137 rows in the comparison table (136 sheets plus the cover) have a different revision list in Rev 14 than in Rev 6**, i.e. were re-issued after the permit set. 17 sheets are new in Rev 14: G1.03 (egress easement), E0.02 (electrical site plan), P4.02, and the 14 numbered interiors sheets ID1.0–ID8.0, which replace five unnumbered interiors sheets in Rev 6.
- Sheets that govern **exterior geometry** and were revised after Rev 6: A1.01 Level 1 plan (to 14), A1.02 Level 2 plan (13), A1.03 roof plan (12), A1.13 entry canopy (13), A1.00a/A1.00c edge-of-slab (7), A4.01–A4.02 building elevations (12), A4.03–A4.06 enlarged elevations (11–12), A5.01 building sections (7), A5.12–A5.18 exterior wall sections (12–13), A5.21–A5.27 wall section details (9–13), A7.21–A7.28 storefront / curtain wall / translucent wall elevations (9–12), A7.31–A7.35 storefront details (9–12), A6.11–A6.14 stairs (12–13), A0.01 site plan (9), A0.04 dumpster enclosure (7), S001, S102, S103, S120, S303, S305 (11–12).
- Sheets unchanged since Rev 6 (identical revision list in both sets, 76 sheets) include A0.31–A0.36 UL assemblies, A5.11, most structural details S2xx–S5xx, most plumbing, mechanical M0.01/M5.02/M6.03/M7.xx and E7.xx.
- The record set has no field mark-ups; the only annotation is one highlight by the architect on A7.33.

## 3. Changes after the Rev 14 record set (not on any drawing sheet in hand)

Recorded in `Contractors\Edifice\PCOs\` and the closeout binders (dates are submittal or signature dates):

| Item | Document | Likely visible in a model |
| --- | --- | --- |
| Lobby stair redesign, railing change, Stonhard treads | PCO 29 (signed 11/11/2025), PCO 30, PCO 54 | Interior, lobby |
| Rooftop mechanical screen | CONT 8 (11/17/2025) | **Exterior, roof** |
| Grade issue at canopy | PCO 50 (12/18/2025) | **Exterior, entry canopy / site** |
| Wall pads, sound panels, Acrovyn in the gym | PCO 42, 49, 65 | Interior, training courts |
| J2 engraved panels; panels returned into the roll-up door | PCO 51, 64 | Interior east wall / roll-up door |
| Turf baffles changed | PCO 47 | Interior |
| Basketball goal bracing | PCO 55 | Interior |
| Second-floor partitions cut down for a lower soffit | CONT 11 (4/20/2026) | Interior, Level 2 |
| Slay office full-lite glass; door 134 electronic hardware; millwork lobby/kitchen; black electrical devices | PCO 72, 75, 76, 77 (Apr–Jun 2026) | Interior |
| Exterior / interior signage | Southwood V18–V21, Phase II, ADA; Rec Plus sign package rev 6 (7/21/2026) | **Exterior** |
| Storm line, retaining wall (RFI 57/78/90), unsuitable soils, Golf Links entrance | PCO 16, 24, 15, 41 | Site (civil, not in hand) |
| MEP as-builts (plumbing, HVAC, electrical, storm, water/sewer) | Closeout binder section 07; `HBE - Electrial As-Builts.pdf` | MEP only |

## 4. CNSA tenant upfit revision history (McCulloch England, for Atrium Health)

| Rev | Description | Date | Set in hand |
| --- | --- | --- | --- |
| — | Issue | 07/31/2025 | `PLANS\CNSA Upfit\` (Bluebeam 8/20/2025) |
| 1 | Review Comments | 08-07-2025 | same |
| 2 | Review Comments | 08-11-2025 | same |
| 3 | Review Comments (MEP) | 08/18/2025 | MEP sets |
| 4 | Plan Adjustments / Coordination | 08-22-2025 | same |
| 5 | Building Review | 09-16-2025 | Revisions set |
| 6 | Drawing Cleanup | 12-23-2025 | `PLANS\CNSA Upfit\CDs\` |
| 7 | Electrical | 01/16/2026 | Revisions electrical |
| 8 | Submittal Updates / Electrical | 02-18-2026 / 02/02/2026 | `PLANS\CNSA Upfit\Revisions\` |
| 9 | Scope Verification (MEP) | 02/18/2026 | Revisions MEP |
| 10 | Equipment Update | 2-27-2026 | `…\Revisions\Rev10 - Equipment Updates\` (A102A, A112A, E202A, E701, E702 only) |

Latest tenant set = the `Revisions\` folder plus the five Rev 10 sheets. Revisions 3, 7 and 9 exist only on MEP sheets. The cover prints the wrong street number (11425); the plans are for 11415.

## 5. Owner decisions — source control for the Building I model (2026-09-22)

These decisions govern all future Building I work. They replace the v001 recommendation and the v001 questions list.

| # | Decision | How it is applied |
| --- | --- | --- |
| 1 | **Rev 14 record set is the controlling architectural and structural geometry source.** `GC Closeouts\FMK Closeout\CD Record Set\250925_RFSMC_Combined permit set_rev14_RecordSet.pdf` (213 sheets, 9/25/2025). | All plans, elevations, sections, details and structural sheets are read from this file only. Sheet numbers and revisions per sheet: `BI_sheet_index_rev14_v001.tsv`. |
| 2 | **Rev 6 permit set is audit / reference only.** `241115_RFSMC_Combined approved permit set_rev6.pdf`. | Never used as geometry input; used only to explain what changed since permit. **Open records issue, documented, not blocking:** no county approval stamp exists on the Rev 6 file (checked as page content, text and annotations). |
| 3 | **Post-Rev-14 PCOs and closeout documents are evaluated one by one.** No PCO is applied automatically. | A post-record change is applied to the model **only where the documentation clearly establishes the final geometry or condition** (dimensioned sketch, approved shop drawing, as-built drawing). Anything less is logged as a candidate in a Building I discrepancy/change log with its document reference and left unmodeled. Candidate list: section 3 of this note. |
| 4 | **Rev 14 is a record drawing set, not a field-verified as-built.** | Every note, script and comparison must describe it that way. Field condition is established only through decision 3 and decision 5. |
| 5 | **Real construction photographs** may be used for discrepancy checking, material and context validation, and identification of obvious field changes. | Photos never silently override dimensioned drawings. A photo finding goes into the discrepancy log and changes geometry only after explicit owner approval, exactly as for Building II. Photo folders listed in `BI_source_inventory_v001.md` section 5. |
| 6 | **AI-generated or altered images are never evidence** of the constructed condition. | Known files: `Pics\Court_View_Gemini.jpg`, `Pics\Gemini_Court_To_Viewing_Area.jpg`, `Pics\04.14.26\ChatGPT Image Jul 14, 2026…png`, `Pics\Drone Photos 7.28.26\ChatGPT Image Aug 5, 2026…png`, `RF Pictures\Gemini_Generated_Image_*.jpg`, `RF Pictures\CSMC Best Rendered Version 12.10.2025.jpg`, `RF Pictures\RF 1 (CSMC) Executive One-Pager Option #1-3.jpg`, `Contractors\Warco\Gemini_Generated_Image_*coaches board 2.png`, `Pics\01.26.26\CSMC_Exterior_Day_Blue_Light_v1/v2.jpg` (retouched), the `CSMC_Inside_Image_01-10.jpg` series (rendered look, treat as non-evidence unless proven otherwise). Marketing renderings (`RF Pictures\*.pdf`, `FMK Architects\CNSA Renderings`) are design renderings, not evidence either. Any further such file found later is added to this list. |
| 7 | **Building II civil documents may be referenced only for shared-site information affecting Building I:** Building I footprint/location, site relationship, surrounding drives, grades, shared plazas and utilities. | Building II *architectural* information is never used to infer Building I geometry. **Every Building II civil sheet used is recorded** in the register below (sheet, file, revision, what was taken from it). Nothing in `source_documents\Building II\` or the Building II model/notes/scripts is modified. |
| 8 | **Do not start modeling yet.** | No `models\Building_I` or `renders\Building_I` content until the owner gives the go-ahead. |

### 5.1 Register of Building II civil sheets used as shared-site references

| Date | Sheet | File (under `source_documents\Building II\`) | Revision printed | Information taken for Building I |
| --- | --- | --- | --- | --- |
| — | *(none yet — no Building I modeling or site work has started)* | | | |

Known candidate for later entry (from the Building II work already on file, not re-opened for this note): CS-101 Dimension Control Plan rev 6 (03.10.26), which labels "Existing two-level mixed use building 'Building I', FFE 661.75"; the same FFE is printed on Building I's own A0.01.

### 5.2 Still open (documented, not blocking)

- County-stamped permit set for Building I not located (decision 2).
- Building I civil/landscape sheets by V3 (CO-100 … CX-104, C-LP-100/101) are listed on the Rev 14 cover but not in the folder; shared-site data comes from decision 7 until the owner supplies them.
- DWG files unreadable with installed tools; not needed for the PDF workflow.
- Signage: not decided; Building I signage packages are inventoried and will be raised as a separate question before any signage is modeled.
