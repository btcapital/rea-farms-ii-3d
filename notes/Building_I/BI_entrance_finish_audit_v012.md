# Building I — lobby-tower facade-finish audit v012 (brick vs white panel above the porte cochere)

Date: 2026-09-23
Baseline audited: `models\Building_I\BI_entrance_facade_v011.blend` (geometry = v008 approved + v011 region fix; site = v010; materials = v009).
Frozen before any change: `manifests\BI_freeze_BuildingI_v011_pending_approval.json` (202 files: every v001–v011 note, data file, script, model and render; PASS at the start and at the end of this pass).
Status: **finish assignment error confirmed on one face of the tower; the drawings and the photograph agree; Building I v012 created (finish regions only, no vertex changed).**

## 1. The tower and its faces in the v011 model (before any change)

The "lobby tower" is the E–F.2 band, `BI_Z2_band_E_F2`: x 28.5–71.0, y 54.2–74.38, z 0–40 (top 40.0 at x 30 sloping to 36.0 at x 71, R). Its finish regions are separate single-face objects 0.03 ft in front of the wall (v005 convention).

| Face | Wall object / plane | Finish region object(s) | Material in v011 | Orientation | Area |
| --- | --- | --- | --- | --- | --- |
| **Front (north) upper, west part** — the face in question | band y 74.38, x 28.5–40.0, z 24.08–40 | `FR_NORTH_BRK1_N1` face 41 | **BRK1** Endicott Manganese Ironspot | +y | 176.9 sq ft |
| Front (north) lower, west part | band y 74.38, x 28.5–40.0, z 0–24.08 between the five CW1 lite placeholders `BI_open_NORTH_010…014` | `FR_NORTH_BRK1_N1` faces 36–40, 42–47 | **BRK1** | +y | 167.4 sq ft (11 pier / spandrel faces) |
| Front (north) upper, east part | band y 74.38, x 40.0–71.0, z 24.6–38.9 | `FR_NORTH_PNL1_N3` face 0 | PNL1 Bone White | +y | 398.6 sq ft |
| Front (north) lower, east part | band y 74.38, x 40.7–70.3, z 0–24.6 (curtain wall CW1) | `FR_NORTH_GLZ_N2` (29 faces, backdrop) + 22 lite placeholders `BI_open_NORTH_015…037` | GLZ placeholder | +y | 428 sq ft backdrop |
| Front lower slivers | band y 74.38, x 40.0–40.7 (z 0–24.5) and x 70.3–71.0 (z 0–24.6) | `FR_NORTH_PNL1_N3` faces 1–4 | PNL1 | +y | 17.1 + 17.2 sq ft |
| **Left return (west face)** — corrected in v011 | band x 28.5, y 54.2–74.38 | `FR_WEST_PNL1_W2b` (z 24.6–40, 310.8 sq ft), `FR_WEST_GLZ_W2` (z 0–24.6 backdrop, 159.3 sq ft) + 16 lite placeholders `BI_open_WEST_029…044` | PNL1 above the head, GLZ below | −x | 310.8 / 159.3 |
| Right return | none — the band's east end (x 71) meets the north block; the exposed face there is the north block's west face x 71, y 74.38–97.75 | `FR_WEST_PNL2_W4` (z 0–15.33), `FR_WEST_PNL1_W4b` (z 15.33–34.07) | PNL2 Tricorn Black below, PNL1 above | −x | 358.3 / 423.3 |
| Transition to the adjacent brick wall (south-west) | wing north face y 54.2, x 10.67–28.5 (with SF1 windows `BI_open_NORTH_001…009`) and wing west face x 10.67 | `FR_NORTH_BRK1_N1` (wing part), `FR_WEST_BRK1_W1`, `FR_WEST_PNL1_W1c` (above 33.3) | BRK1; PNL1 parapet above 33.3 | +y / −x | — |
| Under the tower | vestibule `BI_Z3_vestibule_100` (38.25–62.25 × 74.54–83.58, 9 ft), canopy `BI_canopy_*` (78 × 23.4 ft), doors | unchanged placeholders | — | — | — |

So in v011 the tower's north face is brick from its west corner to grid 3.7 (11.5 ft) for the full 40 ft height, and white panel from grid 3.7 eastward — the brick strip the reviewer sees at the left of the white front above the canopy.

## 2. Source check

| Source | Finding |
| --- | --- |
| **A4.02 Building North Elevation, Rev 14 (1/8" = 1'-0")** — `scratchpad …/v5/north_entry_crop.png`, corner zoom `…/v11/north_elev_tower_corner_zoom.png`; grid bubbles 7, 6, 5, 4, 3.7, 3 read right-to-left (view from the north), 18 px/ft on the 144-dpi render | The tower reads as **one element from x 28.5 (its west corner, 1.5 ft east of grid 3) to grid 6 (x 72): CW1 curtain wall with a continuous mullion grid from grade to its head, and the white vertical-pattern PNL1 panel with the sloping top above it, tagged "PNL1"**. The PNL1 panel's right (west) edge is at 1,482 px = x 28.5 ± 0.2; the CW1 glazing's right edge is at 1,477 px = x 28.8. Immediately to the right (px > 1,482, i.e. x < 28.5) the drawing shows brick with a soldier course, a brick pier with a bollard, SF1 windows and two "BRK1" tags: that is the **wing north face (y 54.2, x 10.67–28.5)** which stands 20 ft south of the tower face and appears beside it in the projection. The "A1/A4.06" leader ("Add cut soldier band … bottom of soldier at 24'-0" …") points at that brick, not at the tower. **No brick is drawn on the tower's north face; no PNL2 occurs on it.** |
| A4.02 Building West Elevation (grids N…A, view from the west) | The tower (between D and F.2) is CW1 with PNL1 above, tagged; the element north of it (F.2 to H.1 = the north block west face x 71) is PNL1 above with PNL2 below; the element south of it (D to A = the wing west face) is BRK1 with SF1 and a PNL1 parapet — consistent with the model's W2/W2b, W4/W4b and W1/W1c regions. |
| A4.02 Material Legend | BRK1 Endicott Manganese Ironspot utility brick; PNL1 Panel Type 1 (vertical pattern) flush wall panels "shown in white and aluminum finish"; PNL2 Panel Type 2 (grid pattern) dark bronze; CW1 curtain wall YKK YCW-750 OG, Viracon VZE1-42. |
| A7.26 Curtain Wall Elevations (CW1 41'-7" × 24'-6") | 41.58 ft wide = x 28.6–70.2 on the band face: the curtain wall spans the whole tower front, so the strip x 28.5–40 below the head is curtain wall, not brick piers. |
| A5.18 A2 wall section at the entry / A5.24 A3 parapet detail | one wall plane with the curtain wall below and the panel parapet above (v011 audit §2). |
| Closeout (Edifice 7/8/2026): Cynergy ACM warranty / submittal | Alucobond PLUS **Bone White** (11,477 sf) = PNL1 as installed; **Tricorn Black** (13,248 sf) = PNL2. No brick change order at the entrance; PCO 14 (Roman → utility brick) concerns the brick itself, not its extent. |
| PCOs / bulletins | none touching the tower finishes (PCO 50 canopy grades, PCO 17/24 civil, CONT 8 rooftop screen). |
| Raster classifier (v002/v005, support only) | the v005 region N1 note "BRK1 tags x 19.9 (upper and lower); component −2.5–65.5 × 1–25; wing north face … and band face y 74.38 **west of grid 3.7**" shows the mechanism: the BRK1 tags sit on the wing north face and the brick raster component of the wing was read as continuing across the tower's west edge up to grid 3.7. The grid-3.7 limit is an interpretation, not a drawn boundary. |
| **Photograph** `drone_2026-07-28_a.jpg` (genuine, validation only) | the entrance tower above the canopy is a continuous white ACM box for its full front width, the lower tower is dark glazing wrapping the corner, and the brick sits only on the wing to the left and on the north block to the right. **Agrees with the drawings.** No newly supplied photo was found in the source folders on this pass; the 2026-07-28 drone frame is the clearest genuine view of the tower front. |

Determination:
- **BRK1**: the wing north face (y 54.2, x 10.67–28.5) including its part above the tower's curtain-wall head up to the wing parapet (33.3), the wing west face (x 10.67) below 33.3, and (per the west elevation) nothing on the tower.
- **PNL1 Bone White**: the tower's north face x 28.5–71 above the CW1 head (24.6) to the sloping top; the tower's west face above 24.6 (v011); the wing parapet above 33.3; the north block west face above 15.33.
- **Transition around the tower corner**: PNL1 wraps the north-west corner (x 28.5 / y 74.38) continuously above the head; the curtain wall wraps it below. The brick/panel transition is not at the tower corner at all — it is the 20-ft step back from the tower face (y 74.38) to the wing north face (y 54.2) at x 28.5, and the 17.8 ft step from the tower west face (x 28.5) to the wing west face (x 10.67) at y 54.2.
- **PNL2 (dark ACM)**: only on the north block west face below 15.33 (x 71, y 74.38–97.75, the recess east of the tower) and on the canopy column wraps (note "Wrapped structural columns. Match PNL2 finish", item F-1, columns not modeled). None on the tower.

## 3. Decision

The documents establish the tower's north face as CW1 + PNL1 from x 28.5 to x 71 (§2); the v011 model has BRK1 on x 28.5–40. Building I **v012** moves exactly those finish faces to the documented materials (`scripts\Building_I\BI_build_entrance_finish_fix_v012.py`; validation `BI_entrance_finish_validation_v012.md`): the face above the head becomes PNL1, the pier/spandrel faces below become the curtain-wall backdrop placeholder like the rest of the CW1, and the 0.7-ft PNL1 slivers at x 40–40.7 below the head (a v001 lite-detection boundary artifact) join the backdrop. No vertex moves; brick stays on the wing faces and everywhere else N1 applies.
