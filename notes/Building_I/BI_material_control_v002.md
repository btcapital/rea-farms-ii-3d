# Building I — facade / material control document v002

Date: 2026-09-22
Applies to: `scripts\Building_I\BI_build_facade_v002.py` + `notes\Building_I\BI_facade_data_v002.json` → `models\Building_I\BI_facade_v002.blend`, renders `renders\Building_I\BI_facade_v002_*.png`.
Base: **BI_shell_v001 (owner-approved geometry baseline, 2026-09-22), geometry unchanged.** v002 adds documented materials and a thin cladding overlay only. Frozen v001 files are listed in `notes\Building_I\manifests\BI_freeze_BuildingI_v001_approved.json`.
Scope: facade + material baseline (skill gate 3). Nothing beyond that gate. No site, no interiors, no signage.

Source-control rules: `BI_revision_review_v002.md` §5. No Building II document opened. No source file modified. Photographs used only to validate appearance (§7); no AI-generated or retouched image used.

## 1. Carried-forward geometry items (from v001, NOT resolved in this pass)

| # | Item | Status in v002 |
| --- | --- | --- |
| G-1 | F→G grid spacing measured (9.945 ft), not written | unchanged, still V |
| G-2 | Canopy north edge: plan shows grid J, section shows H.1 | unchanged, modeled to the written 16'-4 1/2" wing |
| G-3 | Vestibule 100 roof height assumed 9'-0" | unchanged (A-1) |
| G-4 | Printed 271'-0" north façade total does not reconcile with any face run | unchanged, open |
| G-5 | South parapet profile vs mechanical-screen profile not separable on the raster | unchanged; the v002 overlay follows the v001 strips |
| G-6 | Raster-derived parapet and opening heights are lower-confidence (R) | unchanged; the v002 material rectangles inherit the same R confidence |

No documented geometry error was found while reading the wall sections, details and closeout documents for this pass (see §8).

## 2. Controlling sources reviewed

| Source | File / sheet | Used for |
| --- | --- | --- |
| Rev 14 record set (controlling) | A4.01 / A4.02 Material Legend and elevations (p64–65); A4.03–A4.06 enlarged elevations (p66–69); A0.33/A0.34 wall types (p19–20); A0.04 dumpster enclosure (p11); A5.11–A5.27 wall sections/details (p71–86); A7.01 door schedule (p96); A7.11 exterior door details (p98); A7.21–A7.28 storefront/curtain-wall/translucent-wall elevations (p101–108); A7.31–A7.35 storefront details (p109–113); A1.03 roof plan (p28); A1.13 canopy (p29); A6.21 railings (p95) | material systems, products, colour intent, locations |
| Specifications | none for the base building in the folder (only the CNSA tenant-upfit spec book, not applicable) | — |
| Post-record documents | PCO 14 (RTAP 3 / Rev 9), PCO 18 (Rev 11/12), CONT 8 (rooftop screen), PCO 17 (site furnishing), Edifice closeout binder 7/8/2026 (warranties: Jollay Masonry, Cynergy Systems + 3A Composites Alucobond + Petersen PAC-CLAD, ECS Alucopanel, JRS/Johns Manville TPO + MRS sheet metal, CCWG + EFCO, ASSA ABLOY, NanaWall, Kingspan/KLA, Viracon, Raynor/Maxson, SEAS canopy, Palmetto Bituthene) | installed products / colours (decision 3) |
| Photographs (validation only) | `Pics\Drone Photos 7.28.26\dji_fly_20260728_113708_0045…JPEG`, `Pics\CSMC - Progress Photos 09.09. South Side of the Building.png` (genuine site photos) | colour/appearance check |

## 3. Material / system register

Codes: **W** written on the controlling sheet; **C** established by post-Rev-14 closeout/PCO documentation (applied where it clearly states the installed product); **R** extent measured from the shaded elevation raster (±1 ft); **I** interpretation; **U** unresolved → neutral placeholder, labelled `UNRES_…`.

| System | Source (sheet / spec / detail) | Manufacturer / product as documented | Finish / colour as documented | Location | Applied in v002 | Confidence | Conflicts |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **Brick veneer BRK1** | A4.01 legend; PCO 14 (Roman → utility size with soldier band); PCO 18 (soldier height 10", storefront inset 1 1/2" at brick per RFI 60); A0.33 | Endicott utility brick 3 5/8 × 3 5/8 × 11 5/8, running bond 1/3, thru-body | Manganese Ironspot Smooth, light gray mortar | South-wing field (L1 + L2), west-block base, courts base band, entry, east lounge | **Yes** — material `BRK1_Endicott_Manganese_Ironspot_utility`, dark charcoal (photos confirm) | W product / R extent | Dumpster enclosure A0.04 still says "Roman brick veneer" (site item, not modeled) |
| **Metal panel PNL1 (vertical flush, white)** | A4.01 legend, A5.24 "Metal Panel Parapet Wall", A5.22/A5.25 coping notes | Drawn: Petersen PAC-CLAD flush wall panels. **Closeout: 3A Composites Alucobond PLUS ACM, PVDF-2 Bone White, 8,101 + 3,376 sq ft (Cynergy Systems, 2/15/2026)** | Bone White | Parapet band of the south wing (all faces), west-block upper walls, courts frames/columns wraps | **Yes** — `PNL1_Alucobond_PLUS_PVDF_Bone_White` | C product+colour / R extent | Drawing product (formed PAC-CLAD) vs installed ACM; a Petersen 35-year PVDF warranty is also in the package (flashings/trim or other PAC-CLAD components — location unknown) |
| **Metal composite panel PNL2 (grid pattern, dark)** | A4.01 legend, A5.11/A5.22 "vertical ACM panel" | Drawn: PAC-CLAD PAC-3000 RS 4 mm MCM, dark bronze. **Closeout: Alucobond PLUS, SMP Tricorn Black, 5,485 + 6,920 + 843 sq ft** | Tricorn Black | SF2 storefront boxes (south L1 west end, south L2 grids 10–12), 13–14 end block, courts east/north dark bands, gallery portal | **Yes** — `PNL2_Alucobond_PLUS_SMP_Tricorn_Black` | C / R | Colour dark bronze (drawing) vs Tricorn Black (closeout); photos show black |
| **Metal panel PNL3 (horizontal flush & reveal, medium gray)** | A4.01 legend | Drawn: PAC-CLAD Flush & Reveal, medium gray | medium gray | Vertical strips at the CAP1 storefront extensions (south, east, west, north) | **Placeholder** `UNRES_PNL3_flush_reveal_medium_gray` | U | Closeout lists only Bone White and Tricorn Black ACM lots; no medium-gray product found |
| **Translucent wall TWS1** | A4.01 legend; A7.27 note 1 ("Kingspan Unigrid Verti-Lite 2 3/4" thermally broken"), note 3 frame colour by architect | Kingspan Unigrid Verti-Lite | white exterior / white interior; frames: architect's selection (U). Closeout: Kingspan Light + Air (KLA) anodized-finish warranty 1/16/2026 | Courts north and west walls above the base, clerestory bands | **Yes** — `TWS1_Kingspan_Unigrid_Verti-Lite_white` (semi-translucent) | W / R | PCO 18: Gallery Kingspan → 6" curtain wall and MOB west entrance Kingspan → 4.5" storefront (already reflected in Rev 14) |
| **Storefront SF1/SF2/SF3 and curtain wall CW1** | A4.01 legend; A7.21–A7.28 notes: storefront "YES 45FT" / YES-45 TU, curtain wall YKK YCW-750 OG, factory-applied YKK finish, custom colour to match architect's sample; glazing V1/V2 Viracon 1" VZE1-42 insulating HS/HS (V2 tempered at ground floor around the gym), spandrel Viracon V953 Medium Gray | **Closeout: EFCO Corporation storefront (084113) and curtain wall (084413), job K608601, installed by Carolina Classic Window & Glass; Viracon glass (warranty letter 1/19/2026)** | frames: custom colour (U); glass: VZE1-42 vision, V953 Medium Gray spandrel | All glazed openings (376 placeholders from v001) | **Placeholder** `GLZ_Viracon_VZE1-42_in_EFCO_framing_placeholder` (dark glass tone, frames not modeled) | W glass / C framing / U colour | Framing manufacturer YKK (drawing) vs EFCO (closeout); spandrel locations not mapped |
| **Window cap CAP1** | A4.01 legend | YKK E9-7326 aluminum 5" face cap storefront extension | — | Vertical storefront extensions | Not modeled (part of the PNL3 strips) | U | EFCO framing conflict as above |
| **Entry sliding doors 100b / 100c** | A7.01: 12'-0" × 8'-8 5/8", aluminum & glazing, Kynar, curtain-wall frame; A7.11 sliding door details | **Closeout: ASSA ABLOY SL500 OHC FBO ×2, painted to match Alucobond "Beachstone Gray Metallic" (14006XL)** | Beachstone Gray Metallic (door) | Vestibule 100 north and south faces | Placeholder (within the vestibule box) | C / U location detail | "Beachstone Gray Metallic" implies an Alucobond element in that colour at the entry portal — not found in the Alucobond warranty lots (Tricorn Black / Bone White only) |
| **Exterior storefront doors** (115a/b, 121, 123a, 119b…) | A7.01: aluminum & glazing, clear anodized, storefront | EFCO (closeout) | clear anodized (W) | west, north, courts vestibule | Within glazing placeholders | W / C | — |
| **Overhead door 119a** (16' × 10') and folding wall 119d | A7.01: aluminum, black anodized overhead door; NanaWall 24' × 8' clear anodized | **Closeout: Raynor AV300 AlumaView sectional door, clear-anodize frame, sections Armorbrite RAL 7012, 1/8" insulated tempered glass; NanaWall SL45, 8 panels** | RAL 7012 (closeout) vs black anodized (schedule) | 119a at the training area west wall (x = 71); 119d interior between training area and courts | Not separately modeled (within glazing placeholder) | C | Finish conflict schedule vs closeout |
| **Hollow-metal exterior doors** | A7.01 (painted, welded HM frames); A7.11 insulated HM door | Cook & Boardman (closeout warranty package) | painted, colour not stated (U) | service doors | Not modeled | U | — |
| **Roof membrane** | A1.03 notes (mechanically fastened TPO on two layers polyiso, tapered crickets, walk pads, river-rock ballast at the vestibule roof) | **Closeout: Johns Manville JM TPO 60 mil, mechanically fastened (JRS)** | white (photo 2025-09-09) | all roofs | **Yes** — `ROOF_JM_TPO_60mil_white` on the top faces of the shell prisms (simplification: parapet tops carry the roof material) | C | — |
| **Coping / flashing** | A5.19–A5.27: prefinished aluminum coping with integral cleats, "colour to match vertical metal panel / ACM"; A5.27: ACM panels extended to form the coping | **Closeout: MRS/JRS sheet-metal finish warranty, colours Slate Gray and Regal White; .050" prefinished aluminum coping** | Slate Gray / Regal White (which where: U) | all parapets | Not modeled as a separate element | C colours / U location | — |
| **Soffits / portals** | A7.32 "Storefront header @ MOB entry and ACM soffit"; A5.23/A5.27 "Gallery ACM portal" and "Mezzanine ACM portal": 4 mm ACM, 4' × 4' panels, 1/2" reveals | Alucobond (Cynergy) or Alucopanel (ECS) — not assignable | to match vertical panels (W); Beachstone Gray Metallic likely at the entry (I from the door finish) | entry portal at the vestibule; gallery (east) and mezzanine (west) portals | Not modeled | U | — |
| **Entry canopy** | A1.13: exposed structural steel framing, 1" laminated clear glass, .040" aluminum gutter, 3" aluminum downspouts, spider fittings | **Closeout: SEAS "prefabricated aluminum canopies" warranty (3/23/2026)** — no shop drawing in hand | steel paint colour not found (U) | west entry drop-off | Glass `CANOPY_1in_laminated_clear_glass` applied; steel `UNRES_exposed_steel_canopy_framing` placeholder | W glass / U steel | Drawing "exposed structural steel" vs closeout "prefabricated aluminum canopies" (may refer to other canopies, e.g. rear vestibule 133) |
| **Rooftop mechanical screen** | A1.03 (90'-0" × 40'-7"), A5.25 "aluminum louvered equipment screen" | **CONT 8 (11/17/2025) + ECS warranty: Alucopanel FR ACM panels on existing steel framing, colour "Enoc White"**; PCO 18 "show RTU screenwall in white" | Enoc White | roof, grids 8–11 / C–F | **Yes** — `SCREEN_Alucopanel_FR_Enoc_White` | C | Louvered aluminum (drawing) superseded by ACM (closeout) |
| **Louvers** | A5.25 only (the equipment screen, superseded) | — | — | none on the exterior walls found in the Rev 14 text | none | — | — |
| **Railings / guards** | A6.11–A6.21: glass fascia-mount guardrail (gallery), cable guardrails (mezzanine, balcony), VIVA Circa cable rail, stainless powder-coated black | SteelFab glass rail (closeout) | black powder coat | interior only | none (interior) | — | — |
| **Dumpster enclosure** | A0.04: Roman brick veneer on 8" CMU, rowlock cap, galvanized steel tube gate painted, painted steel bollards | — | — | site | not modeled (site gate) | W | Roman vs utility brick after PCO 14 |
| **Below-grade waterproofing** | closeout: GCP Bituthene 3000 | — | — | foundations | not modeled | — | — |

## 4. Facade extents — how the material areas were located

The four building elevations on A4.01/A4.02 are shaded raster images. Each was classified at 144 dpi into 1 ft × 1 ft cells using the drawing's own material tags (BRK1, PNL1, PNL2, PNL3, TWS1) as calibration samples and the teal colour test for glass, then majority-filtered and merged into rectangles (`scripts\Building_I\BI_extract_tools_v001\facade_classify.py`). Confidence **R**: ±1 ft along the facade, ±0.5 ft vertically; small tag boxes inside the drawing leave isolated mis-classified cells. Areas classified per elevation (sq ft): south BRK1 4,472 / PNL1 3,557 / PNL2 879 / PNL3 277; east BRK1 1,200 / PNL1 5,214 / PNL2 1,543 / PNL3 379 / TWS1 862; west BRK1 1,897 / PNL1 4,349 / PNL2 154 / PNL3 427 / TWS1 2,280; north BRK1 1,535 / PNL1 3,572 / PNL2 402 / PNL3 377 / TWS1 3,356. Rectangles are placed as cladding panels 0.02 ft proud of the v001 wall faces (0.10 ft thick), behind the v001 glazing placeholders; wall areas not covered by any rectangle keep the neutral `UNRES_unclassified_wall_area` material.

Cross-check with the closeout quantities: classified PNL1 ≈ 16,700 sq ft vs 11,477 sq ft Bone White ACM; PNL2 ≈ 3,000 sq ft vs 13,248 sq ft Tricorn Black ACM. The classified areas include faces seen twice and the parapet screen; the Tricorn Black quantity also covers the portals, soffits and interior east-wall panels (PCO 36). The comparison is indicative only.

## 5. Photo validation (genuine photographs only)

| Photo | Date | What it confirms |
| --- | --- | --- |
| `Pics\Drone Photos 7.28.26\dji_fly_20260728_113708_0045_1785252548613_photo.JPEG` | 2026-07-28 | White/light vertical panels on the courts block, white frames, dark clerestory glazing, white rooftop screen, dark brick and white parapet band on the south wing, entry canopy and vestibule at the north-west |
| `Pics\CSMC - Progress Photos 09.09. South Side of the Building.png` | 2025-09-09 | White TPO roof, dark charcoal brick field, white parapet band, black panel boxes around the large windows; rooftop units before the screen |

No geometry discrepancy was concluded from photographs (decision 5). Excluded: all files listed in `BI_revision_review_v002.md` §5 decision 6.

## 6. PCO / closeout documents considered

| Document | Content | Applied? |
| --- | --- | --- |
| PCO 14 (7/15/2025, Rev 9) | brick Roman → utility with soldier band; Kingspan box-out at the lab | Already in Rev 14 (consistent) |
| PCO 18 (Rev 11/12) | Gallery Kingspan → 6" curtain wall; west entrance Kingspan → 4.5" storefront; soldier 10"; RTU screen shown white | Already in Rev 14; white screen corroborated by CONT 8 |
| CONT 8 (11/17/2025) | Alucopanel FR "Enoc White" rooftop screen | **Applied** (colour/product) |
| Closeout: 3A Composites Alucobond warranty (2/15/2026) | Alucobond PLUS, Tricorn Black and Bone White lots | **Applied** to PNL2 and PNL1 |
| Closeout: EFCO warranty | EFCO storefront + curtain wall installed | Recorded; framing not modeled |
| Closeout: JRS/JM TPO, MRS sheet metal colours | JM TPO 60 mil; Slate Gray / Regal White | TPO applied; coping colours recorded |
| Closeout: ASSA ABLOY, Raynor, NanaWall, Kingspan KLA, Viracon, SEAS, Jollay, Cook & Boardman | products as tabulated | Recorded |
| PCO 17 (site furnishing) | Pine Hall brick pavers, colour to match building brick | Site gate |
| PCO 36 | interior east-wall metal panels | Interior, not applicable |

## 7. Unresolved finishes (placeholders, labelled `UNRES_`)

PNL3 medium-gray flush & reveal panels; storefront/curtain-wall frame colour (and EFCO vs YKK); canopy steel paint; vestibule enclosure build-up; coping colour allocation (Slate Gray vs Regal White); soffit/portal ACM colour (Beachstone Gray Metallic inferred only from the door finish); hollow-metal door paint; overhead-door colour (RAL 7012 vs black anodized); wall areas not classified on the elevations.

## 8. Geometry issues discovered

None. The wall sections read for this pass (A5.12–A5.27) show the parapet build-ups and coping details consistent with the v001 tops (2'-0", 3'-0"/3'-3", 5'-2", 10'-0" above T.O.S.). The frozen baseline was not altered; the build script verifies the v001 vertex hash before saving.

## 9. Planned outputs

`models\Building_I\BI_facade_v002.blend`; `renders\Building_I\BI_facade_v002_front_north.png`, `_rear_south.png`, `_left_west.png`, `_right_east.png`, `_oblique_northwest.png`, `_closeup_entry.png`; `notes\Building_I\BI_facade_v002_build_report.json`; `notes\Building_I\BI_facade_validation_v002.md`.
