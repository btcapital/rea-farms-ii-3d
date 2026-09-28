# Site / landscape coordination v009 — north entrance paving edge

Date: 2026-09-21
Scope: the paving / planting conflict west of the entrance only (conflict L-2 in `landscape_control_v008.md`). v001–v008 untouched. Coordinates are the model's building coordinates in feet. Written before v009 was built.

## 1. Sources re-reviewed

| Sheet | File, PDF page | Printed revision | What it shows at the west side of the entrance |
| --- | --- | --- | --- |
| **CS-101 Dimension Control Plan** | `00 PLANS\Revision 5\Rea Farms 2 - Civil Drawings 03.17.26.pdf` p.7 | rev 6 03.10.26 | Paver walk along the parking lot swings south-east in an S-curve and becomes a band along the building. Written: inner curve **R10.50'**, band width **8.50'**, flush-curb transition **97.16'**. Planting bed between the curve and the building. A narrow hatched strip (about 1 ft) against the building face on both sides of door 100A |
| CG-101 Grading & Drainage | same file p.3 | rev 6 03.10.26 | Same linework; spots 659.80, 660.08 on the walk, 660.30 at door 100A |
| **LP-101 Landscape Plan – Building** | `00 PLANS\Approved Civil\APPROVED-LDCP-2025-00715.pdf` p.13 | rev 1 11.06.25, City approval 1/9/2026 | Same S-curve and band. The seasonal bed "(29) SEAS" and "(1) GATE" occupy the area between the curve and the building, tapering to a point at the west jamb of door 100A. Planter with "(3) OSOR" in the strip in front of the CW2 bay |
| A112 Level 1 Dimension Plan; A010 Architectural Site Plan | Rev 5 arch. p.3; Approved set p.22 | Rev 5 02/27/2026; permit E | Building line, door 100A, canopy columns. Site paving is not dimensioned on the architectural sheets (A010 refers to civil) |
| CX-101 / CX-102 Site Details | civil p.13–14 | rev 1 11.06.25 | Paver and curb sections only; no enlarged entrance plan. **No enlarged hardscape plan exists in `source_documents`.** |
| Revision 5 log | `Revision 5\_00 REVISION LOG…pdf` | 02.27.2026 | "Landscape: clarification to pavers at entrance" — the revised sheet itself is not in the folder (open item carried) |

## 2. What the documents establish

Sampled directly from the vector linework of both sheets (independent drawings, agreeing within 0.5 ft):

| Edge | CS-101 rev 6 | LP-101 |
| --- | --- | --- |
| Outer (curb-side) S-curve | (61.6, 123.4) → (69.5, 119.1) → (78.3, 114.4) | (62.0, 123.6) → (70.0, 119.3) → (78.9, 114.5) |
| Inner (bed-side) curve, R10.50' | (63.7, 115.2) → (66.5, 111.9) → (70.0, 109.4) → (74.0, 107.9) → (78.3, 107.4) | (64.1, 115.4) → (67.0, 112.1) → (70.5, 109.6) → (74.5, 108.0) → (78.9, 107.4) |
| Band, building-side edge | straight line at **y = 107.35**, x = 88.3 → 109.1 | same |
| Band, curb lines | y = 114.35 and y = 115.85, x = 78.3 → 142.1 (115.85 − 8.50 = 107.35 ✓ written width) | same |
| Door 100A | pavers run up to the door between about x = 80.1 and 88.3 | same |

So the intended boundary is:
- **Pavers**: the parking-lot walk, then the S-curve, then an 8.50 ft band whose building-side edge is 107.35 (about 1.85 ft off the building finish face), reaching the building only at door 100A.
- **Planting bed**: everything between the inner curve and the building, from the upper walk to the west jamb of door 100A.
- **Narrow strip against the building** east of door 100A (y ≈ 105.5 → 107.35): drawn with a stone-like hatch on CS-101, blank on LP-101 with the OSOR planter in it. **Its surface material is not labelled on any sheet reviewed.**
- **Curb / drop-off**: unchanged — flush curb along the 97.16 ft transition (v006 finding).

v007's `Site_Dropoff_band_west` (a plain rectangle starting at x = 62) and `Site_Walk_north_transition_west` (a straight-edged wedge) were my simplifications; the v008 seasonal bed therefore sat on paving.

**Resolved: yes. Confidence: High** (two independent sheets, written radius and width). **Geometry change recommended: yes**, limited to those two hardscape objects and what directly depends on them.

## 3. Changes made in v009

1. `Site_Walk_north_transition_west` → **replaced** by `Site_Walk_entrance_curve_west`, following the documented outer and inner curves (CS-101 rev 6 points).
2. `Site_Dropoff_band_west` → **reshaped**: x = 78.3 → 108.3, building-side edge at 107.35 with the door-100A landing (x 80.1 → 88.3) running to the building line. Its north edge and its joint with the unchanged entry plaza stay exactly as in v007.
3. **New** `Site_Entrance_bed_fill_west`: ground for the documented bed where the old slab used to be (mulch surface).
4. **New** `Site_Building_base_strip_UNRES`: the 1.05 ft strip against the building east of door 100A, at walk level, **neutral placeholder material** because its finish is not labelled.
5. Landscape: `LAND_Bed_mulch_seasonal_west_OVER_V007_PAVING` **removed** (superseded by item 3). The **29 seasonal annuals** are re-packed inside the documented bed (their v008 positions were interpreted and several would have landed on the corrected walk). Quantity and 12" spacing unchanged. The camellia (63.5, 109.5) is inside the documented bed and **does not move**. No planting added.

Surface elevations of the new shapes are taken from the unchanged v007 interpolation (exact at the written CG-101 spots), so they meet the neighbouring unchanged slabs without a step. The interpolated terrain mesh is not rebuilt differently: the v007 interpolation inputs and the v007 "under-slab" test outlines are kept, so the terrain object is identical.

## 4. Still open (not changed, not guessed)

- Material of the narrow strip against the building (placeholder).
- Whether the CW2-bay planter is raised (L-3).
- The 1.5 ft flush-curb strip (y 114.35 → 115.85) is still modeled as part of the paving band, as in v007.
- Revised landscape sheet referred to by the Rev 5 log is not in the folder; CATM / CORA / LACE schedule shortfall (L-1) unchanged; architectural revisions 6–10 not in hand.
