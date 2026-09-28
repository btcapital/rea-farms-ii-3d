# Building I — facade / material baseline v002: validation and completion report

Date: 2026-09-22
Model: `models\Building_I\BI_facade_v002.blend` (2,023 mesh objects = 443 from v001 + 1,580 cladding panels), built by `scripts\Building_I\BI_build_facade_v002.py` from `BI_facade_data_v002.json` on top of the approved `BI_shell_v001.blend`. Control document: `BI_material_control_v002.md`. Build report: `BI_facade_v002_build_report.json`.
Status: **built and validated, NOT approved.** Stopped at the facade/material approval gate (skill gate 3).

## 1. What was created

| Output | Content |
| --- | --- |
| `models\Building_I\BI_facade_v002.blend` | v001 geometry + collection `07_Facade_overlay_v002` (1,580 panels: BRK1 477, PNL1 445, PNL2 101, PNL3 163 placeholders, TWS1 394) + documented materials + close-up camera |
| `renders\Building_I\BI_facade_v002_front_north.png`, `_rear_south.png`, `_left_west.png`, `_right_east.png`, `_oblique_northwest.png`, `_closeup_entry.png` | six views, neutral lighting |
| `notes\Building_I\BI_material_control_v002.md`, `BI_facade_data_v002.json`, `BI_facade_v002_build_report.json` | control, data, report |
| `scripts\Building_I\BI_build_facade_v002.py`, `BI_compare_geometry_v001_v002.py`, `BI_extract_tools_v001\facade_classify.py` | build, independent geometry check, elevation classifier |

## 2. Materials applied (documented product and colour)

| Code | Material name in the model | Basis |
| --- | --- | --- |
| BRK1 | `BRK1_Endicott_Manganese_Ironspot_utility` | A4.01 legend (W), PCO 14 utility size; photos confirm dark charcoal |
| PNL1 | `PNL1_Alucobond_PLUS_PVDF_Bone_White` | closeout Alucobond warranty 2/15/2026 (C) supersedes drawn PAC-CLAD white |
| PNL2 | `PNL2_Alucobond_PLUS_SMP_Tricorn_Black` | closeout (C) supersedes drawn PAC-3000 RS dark bronze |
| TWS1 | `TWS1_Kingspan_Unigrid_Verti-Lite_white` | A4.01 / A7.27 (W); Kingspan KLA closeout warranty |
| Roof | `ROOF_JM_TPO_60mil_white` on the top faces of the shell prisms | A1.03 (W) + JRS/JM closeout (C) |
| Screen | `SCREEN_Alucopanel_FR_Enoc_White` | CONT 8 + ECS closeout (C) |
| Canopy glass | `CANOPY_1in_laminated_clear_glass` | A1.13 (W) |

## 3. Materials unresolved (neutral placeholders, labelled)

`UNRES_PNL3_flush_reveal_medium_gray` (drawn medium gray; no matching closeout lot); `GLZ_Viracon_VZE1-42_in_EFCO_framing_placeholder` (glass product written, framing EFCO per closeout vs YKK drawn, frame colour "match architect's sample"); `UNRES_exposed_steel_canopy_framing` (paint colour not found; SEAS "prefabricated aluminum canopies" warranty of unknown location); `UNRES_vestibule_100_enclosure`; `UNRES_unclassified_wall_area` (faces/areas not classified on the elevations). Not modeled: coping (Slate Gray / Regal White allocation unknown), ACM soffits/portals (Beachstone Gray Metallic inferred only), CAP1 window caps, hollow-metal door paint, overhead-door finish (RAL 7012 closeout vs black anodized schedule), dumpster enclosure (site).

## 4. Specification / drawing / closeout conflicts recorded

1. Storefront and curtain-wall manufacturer: YKK YES-45 / YCW-750 OG (Rev 14) vs EFCO (closeout, job K608601).
2. Metal panel products: Petersen PAC-CLAD formed panels PNL1/PNL3 and PAC-3000 RS PNL2 (Rev 14) vs 3A Composites Alucobond PLUS ACM in Bone White and Tricorn Black (closeout); the Petersen PVDF warranty in the same package has no stated location.
3. PNL2 colour: dark bronze (Rev 14) vs Tricorn Black (closeout, photos).
4. PNL3 medium gray: no closeout product.
5. Rooftop screen: louvered aluminum (A5.25) vs Alucopanel FR ACM Enoc White (CONT 8, ECS).
6. Overhead door 119a: black anodized (A7.01) vs Raynor AV300 clear anodized frame with RAL 7012 sections (closeout).
7. Entry doors: Kynar (A7.01) vs painted to match Alucobond Beachstone Gray Metallic (ASSA ABLOY closeout) — implies an ACM colour not in the Alucobond warranty lots.
8. Dumpster enclosure brick: Roman (A0.04) vs utility brick after PCO 14 (site item).
9. Canopy: exposed structural steel (A1.13) vs SEAS prefabricated aluminum canopies (closeout).
10. No base-building specification book exists in the Building I folder; only the CNSA tenant-upfit specifications.

## 5. PCO / closeout changes considered

PCO 14, PCO 18 (already embodied in Rev 14), CONT 8 (applied), PCO 17 (site, deferred), PCO 36 (interior), closeout warranties for Alucobond/PAC-CLAD (applied), TPO (applied), EFCO, ASSA ABLOY, Raynor, NanaWall, Kingspan, Viracon, SEAS, Jollay, Cook & Boardman, MRS sheet metal (recorded). Nothing applied without a stated installed product.

## 6. Geometry issues discovered

None. Carried-forward items G-1 … G-6 (F→G spacing V; canopy edge J vs H.1; vestibule 9'-0" assumed; 271'-0" north total unreconciled; south parapet vs screen inseparable; raster heights lower confidence) remain open and are restated in the control document §1.

## 7. Validation

| Check | Result |
| --- | --- |
| v001 vertex hash before/after the material pass (443 mesh objects, inside the build) | identical (`3a8230d6…46cc`) |
| Independent comparison of `BI_shell_v001.blend` vs `BI_facade_v002.blend` (`BI_compare_geometry_v001_v002.py`) | 443/443 v001 objects present, 0 vertex changes, 1,580 objects added (all `FD_` prefix), material slots changed on 402 v001 objects (materials only) |
| `BI_freeze_BuildingI_v001_approved.json` (29 approved v001 files) | PASS |
| `BI_freeze_project_and_BuildingII_v001.json` (311 pre-existing project + Building II files) | PASS |
| `BI_freeze_sources_BuildingI_longpath_v001.json` (all 1,231 Building I source files) | PASS |
| Renders inspected | six views; classification speckle (isolated 1 ft cells from drawing tags) visible on white areas, as expected for R confidence |

Overlay statistics: panels 0.02 ft proud of the v001 walls, 0.10 ft thick, behind the v001 glazing placeholders; 555 classified rectangles fell outside the footprint (annotation areas) and were skipped; overlay areas (sq ft): BRK1 8,320, PNL1 8,562, PNL2 2,837, PNL3 1,431, TWS1 6,162.

## 8. Files created in this pass

```
models/Building_I/BI_facade_v002.blend
notes/Building_I/BI_material_control_v002.md
notes/Building_I/BI_facade_data_v002.json
notes/Building_I/BI_facade_v002_build_report.json
notes/Building_I/BI_facade_validation_v002.md
notes/Building_I/manifests/BI_freeze_BuildingI_v001_approved.json
renders/Building_I/BI_facade_v002_{front_north,rear_south,left_west,right_east,oblique_northwest,closeup_entry}.png
scripts/Building_I/BI_build_facade_v002.py
scripts/Building_I/BI_compare_geometry_v001_v002.py
scripts/Building_I/BI_extract_tools_v001/facade_classify.py
```

## 9. Readiness

The facade/material baseline is ready for the owner's gate-3 decision as a **documented material assignment**: every applied material names its product and its source; every uncertain finish is a labelled placeholder; installed products from the closeout binder are applied only where the warranty states them. Its limitations are the raster-derived material extents (±1 ft, tag speckle), the absence of coping, soffit, frame and door-finish detail, and the open conflicts in §4. Recommended next step after approval: a targeted v003 that resolves the coping/soffit/frame questions with the owner (or FMK/Edifice) and replaces the raster extents with the storefront-schedule geometry.

Next single decision for the owner: **approve or redirect the v002 facade/material baseline.**
