# Building I — drawing revision review v001

Review date: 2026-09-22
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

## 5. Recommendation for the future Building I model (owner decision needed)

1. **Base set: the Rev 14 record set** (`GC Closeouts\FMK Closeout\CD Record Set\250925_RFSMC_Combined permit set_rev14_RecordSet.pdf`, 9/25/2025). It is the latest complete sealed set, it re-issues every sheet, and 136 of its 212 sheets supersede the Rev 6 versions. For Building II the approved permit set was the base with a partial revision overlay; here the same result is obtained by using Rev 14 directly, because it is complete.
2. **Keep the Rev 6 set as an audit reference only** (what was permitted), not as geometry input.
3. **Site**: no Building I civil set is in the folder. Options: (a) the owner supplies the V3 civil set for Building I, or (b) the owner authorizes reading the Building II civil sheets (CS-101 / CG-101 rev 6, which already show Building I's footprint and FFE 661.75) for Building I's site, or (c) the site is modeled from the A0.01 architectural site plan plus the 1/11/2024 survey only.
4. **Post-record changes** (section 3) to be layered only after the owner picks which ones matter, exactly like the Building II photo-discrepancy process: rooftop mechanical screen, canopy grade fix, and signage are the exterior candidates.
5. **Photos** feed a discrepancy log only and never change geometry without approval (same rule as Building II); AI-generated images are excluded.
6. **DWGs**: not needed for the PDF-based workflow. If the owner wants them used, installing a DWG-to-DXF converter needs explicit approval first.

## 6. Owner confirmations requested before modeling starts

- Accept Rev 14 (9/25/2025) as the geometry baseline for Building I? (yes / no)
- Is there a county-stamped permit set for Building I? The Rev 6 file has no stamp.
- Which civil option in section 5.3?
- Should Building I include signage (it is a finished building), unlike Building II?
- Same folder rules as Building II: new files only under `notes\Building_I`, `scripts\Building_I`, `models\Building_I`, `renders\Building_I`, all prefixed `BI_`.
