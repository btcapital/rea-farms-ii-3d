# Building I — facade cleanup control document v005

Date: 2026-09-22
Applies to: `scripts\Building_I\BI_build_facade_cleanup_v005.py` + `notes\Building_I\BI_facade_regions_v005.json` → `models\Building_I\BI_landscape_v005.blend` (name kept in the version chain: building + site + landscape, facade overlay replaced), renders `renders\Building_I\BI_facade_v005_*.png`.
Base: **BI_landscape_v004.blend** (unapproved, kept unchanged) which carries the approved v001 geometry, v002 materials, v003 site and v004 landscape. Frozen: v001–v003 (`manifests\BI_freeze_BuildingI_v003_approved.json`, 56 files).
Scope: **facade finish-overlay implementation only.** No change to shell, footprint, roof, parapets, openings, canopy, grades, paving, landscape positions or plant quantities. No palette redesign. Nothing beyond this gate.

## 1. Diagnosis (measured on BI_landscape_v004.blend before any change)

The v002 overlay collection `07_Facade_overlay_v002` holds **1,580 objects** (`FD_*`), one per rectangle produced by the 1-ft raster classification of the shaded A4.01/A4.02 elevations, each a 0.10-ft-thick box placed 0.02 ft proud of the v001 wall face. The wall faces themselves keep the neutral `UNRES_unclassified_wall_area` grey (v002 changed material slots only; 402 shell faces).

| # | Visible defect | Measured cause | Count |
| --- | --- | --- | --- |
| D-1 | Fragmented white/grey/dark rectangles "breaking through" the wall | **Raster-classification speckle.** 566 of the 1,580 overlay boxes are under 4 sq ft (BRK1 172, PNL1 142, TWS1 148, PNL3 73, PNL2 31); 1 ft cells around drawing annotation (tag boxes, dimension text, leaders, hatch line-work) were classified as other materials. Each speckle is a separate 0.1-ft box standing 0.02 ft proud; between them the neutral grey wall shows. Per facade the classification produced 94 (north) / 62 (west) / 33 (south) / 8 (east) BRK1 components, most of them < 30 sq ft. | 566 boxes < 4 sq ft; ~1,000 boxes < 30 sq ft components |
| D-2 | Panels crossing windows and doors | The classifier's teal test only removed cells that were clearly glass; cells at frames, mullions and shadows became BRK1/PNL/TWS1 boxes lying over the v001 glazing placeholders. | **195 boxes intersect an opening placeholder** (BRK1 114, TWS1 34, PNL3 25, PNL2 13, PNL1 9) |
| D-3 | Wrong material zones at the entrance (white "TWS1" and brick fragments on the CW1/PNL1 wall) | **Incorrect zone assignment**: the white flush PNL1 texture and the white translucent TWS1 texture are indistinguishable in the raster, so PNL1 walls of the wing and entrance got TWS1 (10 boxes on plane x = 38.2, 6 on y = 83.7, 4 on y = 74.5) and BRK1 fragments (7 on y = 74.5). North-elevation drawing tags at the entrance are PNL1 / CW1 / BRK1 only. | 20+ boxes |
| D-4 | Tall white "block" with a black recess above the vestibule | **Incorrect depth**: v001 placed the CW1 glazing placeholders for x 40.7–63.7 at the vestibule plane y = 83.6 even above the 9-ft vestibule roof (curtain wall is on the band face y = 74.4). v002 then put **20 overlay boxes (PNL1 10, TWS1 6, BRK1 2, UNRES 2) on the same floating plane above z = 9**, 9 ft in front of the wall; their back faces and the unlit void behind read as a black box. | 20 floating boxes + 14 floating placeholders (v001, untouched) |
| D-5 | Isolated dark rectangles in white fields | Same as D-1 for PNL2/PNL3 cells (PNL3 = "medium gray" placeholder, 163 boxes of which 73 < 4 sq ft), e.g. the "+"-shaped grey mark on the north parapet wall is a drawing tag box. | 163 PNL3 boxes |
| D-6 | Panels floating on parapet screens and column strips | Overlay boxes were created per classified rectangle without checking that a wall face exists behind the full rectangle: boxes span the gap between the wing parapet (33.3) and the screen tops, and follow the mirrored north-elevation u-range past the building ends (north BRK1 components at u −25 … −2.5 = the canopy columns area, PNL1 at 282–290). | ~60 boxes outside any wall face |
| D-7 | Grey base wall visible between panels | Wall faces stay `UNRES_unclassified_wall_area`; every gap in the overlay shows grey. | all facades |
| not found | Coplanar overlay-on-overlay z-fighting | 0 overlapping coplanar overlay pairs (v002 offset the boxes uniformly), so no z-fighting between overlays; the "corruption" is speckle + wrong zones + floating depth, not shading. | 0 |

Object counts: v004 = 2,247 objects (2,044 mesh); overlay = 1,580 (all 0.10 ft thick, 0.02 ft proud); openings = 376 glazing placeholders on 17 planes.

## 2. Rebuild method (v005)

The pixel classifier is **not** used to generate geometry. Finish regions are defined as continuous rectangles in facade coordinates (u along the facade, z above FFE) from, in order: (1) the written material tags on A4.01/A4.02 (registered to the grid bubbles: 9.00 pt/ft, residual ≤ 0.5 ft on the north/south sheets, ≤ 4 ft on east/west where bubble text is sparse), (2) the v001 zone faces (Z1 wing, Z2 band, Z4a/Z4b north block, Z5 end block, parapet screens), (3) the v001 opening placeholders (storefront / curtain-wall boundaries), (4) the documented datums (LVL02 15.33, mezzanine 13.02, gallery 11.0, T.O.S. 28/30/31.5/37.29, parapet tops 33.3/40), (5) elevation details (soldier band, PNL3 bands between stacked windows), (6) the large connected components of the v002 classification only to support boundary positions (e.g. the PNL2 boxes 6.9–47.9 × 0–15 and 169.9–229.9 × 14–28 on the south), (7) photographs for appearance only.

Generation rules: every exterior wall face of the shell and the parapet screens is covered completely by regions (no grey gaps) — undocumented areas get the labelled placeholder; regions are clipped to the actual face polygon (sloped tops respected); **all opening placeholders on the same plane are subtracted** (no opaque overlay in any glazing or door opening); faces are single planes at **+0.03 ft (3/8 in)** — the smallest stable offset, since no wall section in the folder gives a finish projection that should read at model scale; faces buried inside another zone are skipped; the vestibule (UNRES, documented) and the mechanical screen keep their materials; region objects are one mesh per (facade, region) named `FR_<facade>_<material>_<id>` in `07_Facade_regions_v005`.

Materials unchanged from v002: BRK1 Endicott Manganese Ironspot, PNL1 Alucobond PLUS Bone White, PNL2 Alucobond PLUS Tricorn Black, TWS1 Kingspan Unigrid Verti-Lite, TPO, Enoc White screen, canopy glass; placeholders kept: PNL3 medium gray (U), GLZ (curtain-wall backdrop), vestibule (U).

## 3. Region register

See `BI_facade_regions_v005.json` (each region: facade, u0–u1, z0–z1, material, basis code, evidence). Basis codes: **T** written tag, **Z** v001 zone face, **O** opening boundary, **D** datum, **R** raster component (support), **I** interpreted from the drawing, **P** photo-consistent. Summary:

| Facade | Regions | Key boundaries |
| --- | --- | --- |
| South (y = −4.38 wing; 13–14 block) | PNL2 SF2 box 6.88–48 × 0–15.33 (T, R); BRK1 field 6.88–92 and 118–241 × 0–33.3 (T, R); PNL1 bays 92–118 and 241–270.4 with PNL3 bands 96–106 / 245–255 × 11–15.33 (T, I); PNL2 SF2 box 170–230 × 15.33–28 (T, R, D); PNL2 13–14 block 270.4–287 × 0–32 (T, Z); PNL1 parapet 30–270.4 × 33.3–40.1 (T, Z) | 11 |
| North (y = 61.12 wing, 74.38 band, 169.6 bay, 197.5/198.5/202.88 courts; x-faces facing north) | BRK1 0–40 × 0–40 (T); CW1 backdrop 40.7–70.3 × 0–24.6 (T, O); PNL1 40–72 × 24.6–40 (T); PNL1 bay 72–91 with PNL3 76–84.3 × 10.7–17.1 (T, O); courts: PNL1 base 91–271.4 × 0–11 (R, I), PNL2 entry surround 140–160 × 0–11 (T), TWS1 91–271.4 × 11–30.2 (T), PNL1 column wraps 3 ft at grids 7–12.9 (I, P), PNL1 parapet 91–271.4 × 30.2–40 (T, P); 13–14 block PNL2 271.4–287 × 9–34, BRK1 base × 0–9 (T, R) | 14 |
| East (x = 271.38 wing, 281, 287) | BRK1 corner −4.38–8.6 × 0–40 (R, Z); PNL1 bay 8.6–44 × 0–40 with PNL3 11.8–23.8 / 38.8–44.8 × 11–15.33 (T, R); BRK1 base 44–130 × 0–18 and 130–175 × 0–9 (T, R); PNL2 field 44–175 × 9/18–34 (T, R); PNL1 44–175 × 34–40 (T); courts PNL1 base 175–202.9 × 0–11, TWS1 × 11–30.2, PNL1 parapet × 30.2–40 (T, R) | 10 |
| West (x = 6.88 wing, 28.62 band, 28.71 Z4b, 71 north block) | BRK1 −4.38–61.12 × 0–33.3 with PNL2 box 6.3–38.3 × 0–15.33 (T, R); PNL1 parapet × 33.3–40 (Z); band: CW1 backdrop 61.12–74.38 × 0–24.6 (O), PNL1 × 24.6–40; Z4b face 74.38–97.75: PNL2 × 0–15.33, PNL1 × 15.33–34.07 (T, I); north block 97.75–133.8: BRK1 × 0–18, PNL1 × 18–40, PNL3 121.3–132.3 × 11–15.33 and 26–33 (T, R); courts 133.8–202.9: PNL1 base × 0–11, TWS1 × 11–30.2, PNL1 × 30.2–40 (T, R) | 13 |

## 4. Conflicts and uncertain conditions (kept, not resolved)

| # | Item | Handling |
| --- | --- | --- |
| F-1 | North-elevation note "Wrapped structural columns. Match PNL2 finish" vs the shaded drawing and the 2026 photographs showing white column wraps on the courts block | wraps modeled PNL1 (photo-consistent, as in v002); flagged U |
| F-2 | West-elevation tags PNL2 at the courts parapet (u ≈ 141 and 185, top) vs PNL1 tag on the east courts parapet and white in photographs | parapet PNL1; flagged U |
| F-3 | Courts north base band: no tag; drawing tone light, photograph 2026-07-28 ambiguous | PNL1 base with the tagged PNL2 entry surround; flagged U |
| F-4 | Vestibule enclosure: west-elevation PNL2 tag at u ≈ 78 (low) may refer to the vestibule side | vestibule keeps `UNRES_vestibule_100_enclosure` (v002 decision) |
| F-5 | v001 CW1 placeholders floating at y = 83.6 above the vestibule (geometry, frozen) | not altered; the wall behind (band face y = 74.38, x 40.7–63.7, z 9–24.6) gets the CW1 backdrop placeholder so nothing opaque reads through the glass; new geometry item **G-7** for the owner |
| F-6 | PNL3 medium-gray product unresolved (v002) | placeholder kept |
| F-7 | Soldier-course band at window heads (24'-0"–24'-10"), coping colours, ACM soffits/portals | not modeled (as v002) |
| F-8 | Finish projection depth (brick 3 5/8 in + air space vs ACM on Z-girts) | not modeled; all finishes at +0.03 ft |

All v001 G-items, v002 material placeholders, v003 SC-items and v004 LC-items carry forward unchanged.

## 5. Planned outputs and validation

`models\Building_I\BI_landscape_v005.blend`; renders `BI_facade_v005_front_north_elevation.png` (orthographic, straight-on), `_entrance_closeup.png`, `_oblique_northwest.png`, `_oblique_northeast.png`, `_rear_south.png`, `_site_elevated.png`; `BI_facade_v005_build_report.json`; `BI_facade_validation_v005.md`. Validation: hash of every non-overlay mesh object before/after (shell, openings, site, landscape); independent `BI_compare_geometry_v004_v005.py`; manifests v003-approved (56), project/Building II (311), Building I sources (1,231); opening-intersection check on every new face; coplanar-face check between new faces.
