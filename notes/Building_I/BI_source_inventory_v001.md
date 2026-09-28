# Building I — source document inventory v001

Inventory date: 2026-09-22
Scope: inventory of `source_documents\Building I\` only. **No modeling was done. Nothing in `source_documents` was modified, moved or renamed.** Nothing in `source_documents\Building II\` or any Building II model, script, note, render, export or viewer was opened or touched.
All paths below are relative to `source_documents\Building I\`. Dates marked "printed" come from the document itself; other dates are Windows file dates.

Companion files (all written by `scripts\Building_I\BI_inventory_v001.py`, which only reads the sources):

- `BI_file_inventory_v001.tsv` — every file (1,231 files, 6,929,037,544 bytes) with modified date, size, extension, path.
- `BI_sheet_index_rev6_v001.tsv` and `BI_sheet_index_rev14_v001.tsv` — page → sheet number → sheet name → revisions listed in the title block, for the two combined drawing sets.
- `BI_sheet_revision_comparison_v001.tsv` — sheet-by-sheet revision lists, Rev 6 versus Rev 14.
- `BI_revision_review_v001.md` — the revision history and the recommended base set.

---

## 1. Building identified

| Item | Printed on the documents |
| --- | --- |
| Project name | **Rea Farms Sports Medicine Center** (drawings). Also called **Carolina Sports Medicine Center / CSMC / "MOB 1"** in owner files. GC job NC4450, FMK project 2329. |
| Address | **11415 Golf Links Drive, Charlotte, NC 28277** |
| Owner | Dormie Equity Partners, LP (drawings); contract entity Rea Park Lane 1031, LLC |
| Architect / interiors | FMK Architects, Charlotte (Russ DeVita, AIA) |
| Structural | Moore Lindner Engineering (Rob Moore, PE) |
| MEP / fire protection | AME Consulting Engineers (Michael Lawler, PE) |
| Civil | V3 Southeast (David Klausman, PE) — **civil sheets are not in this folder, see section 4** |
| Contractor | Edifice, LLC (PM Shawn Berting); owner representative Playbook Management (Chad Dameron) |
| Building | Two levels plus roof / high roof; training courts (three basketball courts) with mezzanine; lobby stair, south stair, gallery stair; elevator and wheelchair lift. Column grid 1–14 (plus 3.7 and 12.9) by letters. |
| Datum | Architectural Site Plan A0.01 prints **FFE: 661.75**. Building II civil CS-101 (used earlier for the v011 context mass) gives the same 661.75 for "Existing Building I". |
| Permit | Temporary Certificate of Occupancy placard, permit **B4733342**, gym only, expiry 03/01/2026 (`Contractors\Edifice\TCO.PlacardB4733342.pdf`). |
| Tenants seen | Architech Sports (physical therapy / performance), Slay Basketball, Carolina NeuroSurgery & Spine Associates (CNSA, Atrium Health) upfit, Taylor Capital / TM Advisors offices. |
| Timeline | Groundbreaking Jan 2025 → gym TCO Jan 2026 → closeout binders Jun/Jul 2026 → grand-opening photos 28 Jul 2026. |

## 2. Folder map (top level, 1,231 files)

| Folder | Files | What it holds | Modeling relevance |
| --- | --- | --- | --- |
| *(root)* | 16 | **`241115_RFSMC_Combined approved permit set_rev6.pdf`** (202 p, 144 MB); a Building II concept PDF (misfiled, see section 6); contracts, erosion/grading agreement letter, appraisal | **High** (Rev 6 set) |
| `GC Closeouts\` | 82 | **`FMK Closeout\CD Record Set\250925_RFSMC_Combined permit set_rev14_RecordSet.pdf`** (213 p, 89 MB); **58 FMK DWGs** (8 architectural, 47 MEP, 3 fire protection); special-inspection letters; two Edifice closeout binders (3,925 p and 4,601 p) with bookmark PDFs; HBE electrical as-builts (18 sheets); TAB report; warranty tracker | **High** |
| `PLANS\` | 29 | CNSA upfit sets by McCulloch England (three issues plus Rev 10 sheets), Security 101 camera layout, UVD cabling mark-ups, XL Media AV drawings | Medium (tenant interiors) |
| `Contractors\` (61 sub-folders) | 383 | Edifice PCOs / owner change orders / pay apps / monthly field reports; Southwood signage drawings V18–V21, Phase II, ADA; Security 101 door and zone plans; Jays Cleaning janitorial SF plans; DCal locker design; Warco marker boards; vendor W-9s, COIs, invoices | Medium (PCOs record post-record-set changes; signage) |
| `Pics\` | 305 | Dated progress photo folders (2/7/25 → 9/15/26), drone photos and two MP4 videos (8/10/26), Edifice DroneDeploy 11/14/25, grand opening 7/28/26, 9/9/25 progress PNGs, early plan PDFs (`240726_RFSMC_RevisedPlans.pdf`, interiors visioning) | Medium (discrepancy log only) |
| `FMK Architects\` | 18 | Egress exhibit B (4/21/2025), CNSA renderings (3 PNG, Oct 2024) plus a zip of the same, egress easement declaration (recorded 5/2/2025), contract and settlement | Low–medium |
| `Survey\` | 6 | **`3513 1-11-2024 - Survey.pdf`** (boundary/topo, 1 sheet 36×24 in), ECS CMT field reports, appraisal | Medium (site) |
| `Subsurface Exploration and Geotechnical…\` | 8 | ALTA survey 8-15-23 (marked PRELIMINARY), subdivision plat 8-4-23, sketch plan 7-13-23, geotech report 8-21-2023, Phase I ESA | Low (scanned, no text layer) |
| `Meeting Minutes\` | 41 | CSMC OAC minutes 82–114 (Jul 2025 → Mar 2026), PDF and XLSX | Low (context for changes) |
| `Monthly Pay App Reports\`, `Schedule\`, `Project Budgets\` | 36 | Field reports with photos, look-ahead schedules, master budgets | Low |
| `Keying\` | 2 | Key schedule floor plans (4/13/2026) on the A1.01/A1.02 background | Low |
| `Condo Assocation\`, `Closing Docs\`, `Construction Loan\`, `Insurance\`, `PSA\`, `Liens NC\`, `Property Taxes\`, `CAM\`, `Grand Opening\`, `Plat Application Fee\`, `V3 Southeast PC\`, `DD Documents\` | 118 | Legal, title, HOA declarations and maps, plats, lighting-plan coordination exhibit (3/5/2025), invoices | None (lighting exhibit: low) |
| `Tenant Logo Files\`, `RF Pictures\`, `CBJ Heavy Hitters\` | 104 | Logos (EPS/AI/PSD/SVG), marketing renderings, monthly marketing photos, a 529 MB MP4 | None (renderings are not drawings) |
| Utilities: `AT&T`, `Backflow`, `Charlotte Water`, `Duke`, `Piedmont Natural Gas`, `Spectrum`, `Chem-Bac` | 22 | Bills, agreements, backflow requirements | None |
| `Contractors\New Folder`, `New folder (2)`, `Interior Elements`, `JanPro`, `GC Closeout Documents`, `Owner & Contractor Agreement` | 0 | Empty folders | — |

File types: 623 PDF, 186 JPG, 96 JPEG, 84 PNG, 58 XLSX, 58 DWG, 40 EPS, 22 DOCX, 15 AI, 12 HEIC, 11 DOC, 10 PSD, 7 MP4, 2 ZIP, 2 SVG, 1 XLS, 1 TIF, 1 MSG, 1 CSV, 1 extension-less MP4 (`Pics\attachment1737730919979`).

## 3. Drawing sets found (printed dates)

| # | Set | File | Pages / size | Printed issue | Notes |
| --- | --- | --- | --- | --- | --- |
| A | **Rev 6 "Combined approved permit set"** | `241115_RFSMC_Combined approved permit set_rev6.pdf` | 202 p, 3024×2160 pt (42×30 in), 144 MB | Cover 11/15/2024; revisions 1–6; FMK seal dated 11/15/2024 on every sheet | **No county approval stamp found** as page content, text or annotation (only 1,922 hyperlink annotations). The file name says "approved"; owner to confirm. Interiors are five unnumbered sheets. |
| B | **Rev 14 Record Set** | `GC Closeouts\FMK Closeout\CD Record Set\250925_RFSMC_Combined permit set_rev14_RecordSet.pdf` | 213 p, same size, 89 MB | Cover 9/25/2025; revisions 1–14; created 2/7/2025, last saved 3/10/2026 | Latest complete sealed set. No "record" or "as-built" note on any sheet: it is the final revised CD set, not a field-verified as-built. Adds G1.03, E0.02, P4.02 and 14 numbered ID sheets versus Rev 6. Contains one ink highlight by rdevita on page 111 (A7.33). |
| C | FMK CAD files | `GC Closeouts\FMK Closeout\DWG\Architectural\*.dwg` (A1-00a, A1-00b, A1-00c, A1-01, A1-02, A1-03, A3-01, A3-02) plus `MEP\` (47) and `Fire Protection\` (3) | 58 DWG | Files dated 8/20/2026 | Architectural DWGs are AutoCAD 2018 format (AC1032); MEP/FP are 2010 format (AC1024). **No DWG reader is installed** (no ezdxf, no ODA File Converter; Blender has no DWG import). Installing a converter would need owner approval. |
| D | Edifice closeout binders | `GC Closeouts\Edifice\Core Shell As-Builts\Final Closeout Binder.pdf` (3,925 p, bookmarks 6/22/2026) and `GC Closeouts\Edifice\Rea Farms Closeout Binder\Rea Farms Sports Medicine Closeout Binder.pdf` (4,601 p, 7/8/2026) | letter size | — | Section "07 As-Builts": Boda plumbing and underground, MCI HVAC, HBE electrical, Blythe storm and water/sewer as-builts. Warranties, O&Ms, keying, training. Binder 2 supersedes binder 1 (adds Flooring Solutions, Stonhard, SFG wood floor). |
| E | HBE electrical as-builts | `GC Closeouts\Edifice\Core Shell As-Builts\HBE - Electrial As-Builts.pdf` | 18 sheets E0.01–E7.02 | Oct 2025 | Marked-up electrical set. |
| F | CNSA tenant upfit, McCulloch England for Atrium Health | `PLANS\CNSA Upfit\01 ARCHITECTURAL.pdf` (issue 07/31/2025, revs 1–4), `…\CDs\01 ARCHITECTURAL.pdf` (rev 6 "Drawing Cleanup" 12/23/2025), `…\Revisions\01 ARCHITECTURAL.pdf` (rev 8 "Submittal Updates" 2/18/2026), `…\Revisions\Rev10 - Equipment Updates\` (rev 10, 2/27/2026, sheets A102A, A112A, E202A, E701, E702) | 33 p per set; 28 architectural sheets A000–A710 | Cover prints "11425 Golf Links Dr" (wrong street number; the plans are for this building) | Tenant interiors only; MEP/FP/interiors/specs and a JAZZ security plan in the same folders. Same role as the Building II CNSA test-fit. |
| G | Early / pre-CD | `Pics\240726_RFSMC_RevisedPlans.pdf` (7/26/2024, 7 p, floor plans), `Pics\240925_ReaFarms Interiors Visioning-FMK-reduced (003).pdf`, `RF Pictures\ReaFarms_Renderings.pdf` (8/2024), `FMK Architects\CNSA Renderings\*.png` | — | — | Superseded; visual reference only. |
| H | Signage | `Contractors\SouthWood Corporations\Drawings\` (V18 8/20/25 → V21 11/11/25, Phase II, ADA, Options V2), `Contractors\Rec Plus…\Taylor Capital _Signpackage Rev6 (072126)_TC Comments 08.21.26.pdf`, `…\CSMC - Directional Sign Locations_Rough Utility Locations.pdf` (9/1/2026) | — | — | Exterior and interior signage as built. Building II policy was "no signage"; Building I is finished, so the owner decides. |
| I | Site references | `Survey\3513 1-11-2024 - Survey.pdf`; `Condo Assocation\Rea Farms Lighting Plan Coordination.pdf` (3/5/2025); `FMK Architects\250429_RFSMC egress_exhibit B .pdf`; `Final Agreement Letter For Rea Farms with Soil Erosion and Grading Plans 7.12.24.pdf` (letter only, cites V3 sheets CE-101/CE-201); ALTA, plat, sketch plan (scanned) | — | — | See section 4 for the civil gap. |
| J | Building-plan derivatives | `Keying\CSMC Key Schedule Floorplan.pdf`; `Contractors\Jays Cleaning Services\Janitorial Floor Plans\CSMC - Level 1/2 Building Plan SF (with CNSA).pdf` (10/2/2025); `Contractors\Security 101\CSMC - 1st/2nd Floor Access Control Door Locations.pdf`, `Intrusion Zones\`; `PLANS\XL Media\21053 - AV Drawings 8-28-25.pdf` | — | — | All drawn on the FMK A1.01/A1.02 background; useful for room names and door numbering cross-checks. |

## 4. Gaps and open items

1. **No civil / landscape drawings for Building I are in the folder.** The Rev 14 cover index lists V3 sheets CO-100, CD-101, CE-101…CE-401, CS-100…CS-201, CT-101…CT-103, CG-100…CG-201, CU-101, C-LP-100/101, CX-101…CX-104, but none is bound into either combined set and no separate civil PDF exists. Only the 1/11/2024 survey, the preliminary ALTA and the plat are here. The Building II civil set (in the Building II folder) shows the Building I footprint and FFE, but that folder is off limits for this task.
2. **No county-stamped set located.** The Rev 6 file is titled "approved" but carries no Mecklenburg County stamp on the cover, on the plan sheets, or as annotations. Building II's approved set had a visible COS stamp. Owner to confirm whether a stamped set exists elsewhere or whether Rev 6 is accepted as-is.
3. **Rev 14 is not a field-verified as-built.** Changes after 9/25/2025 exist only in PCOs and the closeout binders: lobby stair redesign and railing (PCO 29/30/54), rooftop mechanical screen (CONT 8), wall pads and sound panels in the gym (PCO 42/49), J2 engraved panels and roll-up door returns (PCO 51/64), turf baffles (PCO 47), grade issue at canopy (PCO 50), basketball goal bracing (PCO 55), second-floor partition/soffit height adjustment (CONT 11, Apr 2026), Slay office full-lite glass (PCO 72), millwork (PCO 76), black electrical devices (PCO 77), signage.
4. **DWG files cannot be read with the installed tools.** Optional: ask the owner to approve installing the free ODA File Converter (DWG → DXF) or LibreDWG; otherwise model from the sealed PDFs exactly as for Building II.
5. **AI-generated images are mixed into the photo folders** (`Gemini_Generated_Image_*`, `ChatGPT Image *`, `Court_View_Gemini.jpg`, `CSMC Best Rendered Version`). They must never be used as evidence of built condition.
6. Scanned documents with no text layer: ALTA survey, subdivision plat, sketch plan, geotech report (not OCR'd).
7. Windows long-path note: several files sit deeper than 260 characters; scripts must open them with the `\\?\` prefix (the inventory script does).

## 5. Photo evidence available for a discrepancy log (not used yet)

| Date (folder) | Type | Count |
| --- | --- | --- |
| 2/7/2025 (`Pics\Update 2-7-25`) | DJI drone, site cleared | 8 |
| 4/21/2025, 6/26/2025 | phone HEIC, drone PDF (10 p) | 3 + 1 |
| 9/9/2025 (`Pics\` root) | progress PNGs by elevation (east, south, SW, NW, entrances) | 12 |
| 10/9/2025, 11/10/2025, 12/11/2025 | phone photos (plus a zip of 8) | 9 + 14 + 10 |
| 11/14/2025 (`Pics\Edifice Drone 11.14.25\DroneDeploy`) | drone orthos/obliques | 21 |
| 1/26/2026, 2/5/2026, 2/16/2026, 3/18/2026, 4/14/2026 | interior/exterior phone photos | 23 + 16 + 14 + 7 + 9 |
| 7/28/2026 (`Drone Photos 7.28.26`, `Grand Opening`) | drone and DSLR, finished building | 26 + 29 |
| 8/10/2026 | drone MP4 ×2 (529 MB, 103 MB), trimmed MP4, overview JPG | 4 |
| 9/15/2026 (`Main_Entrance_Traffic_Flow`) | entrance photos and a PDF | 9 |
| Marketing (`CBJ Heavy Hitters\9.15.26 Materials`, `RF Pictures`) | monthly project photos Jan 2025 → Mar 2026, renderings | about 45 |

## 6. Building II material stored in the Building I folder (noted, not moved)

- `2025.03.25_Carolina Sports MOB_Concept Design_sc4-Alternatives-Revised (002).pdf` (root, 13 p) — Building II concept design.
- `Contractors\Edifice\20250107 - Rea Farms MOB II Deliverable.pdf` and the identical copy `Insurance\20250107 - Rea Farms MOB II Deliverable.pdf` — Building II concept estimate.
- `Pics\High Resolution MOB 2 Balcony/Front/Terrace.png` — Building II renderings.
- `Contractors\Edifice\PCOs\OCO #7\PCO 26 - MOB2 - Site Preparation Deduct*.pdf` — Building II site preparation carved out of the Building I contract.
