# Site control document v006 — site and grading pass

Date: 2026-09-21
Applies to: `scripts/build_shell_v006.py` → `models/building_shell_v006.blend`
Building baseline: **v005, frozen** — geometry and materials rebuilt identically; the building is **not moved**.
Written **before** v006 was built.

Codes: **W** written on a civil or architectural sheet · **M** measured from exact-scale vector linework (positions) · **V** value read visually from the sheet because it is not in the PDF text layer (position ±2 ft) · **INT** interpolated / interpreted — **not exact** · **A** assumption.

## 1. Controlling sheets

| Sheet | Title | File, PDF page | Printed revision | Used for |
| --- | --- | --- | --- | --- |
| **CG-101** | Grading & Drainage Plan | `00 PLANS\Revision 5\Rea Farms 2 - Civil Drawings 03.17.26.pdf`, p.3 | rev 1 11.06.25; **rev 6 03.10.26 "Wall Revisions"**, sealed 3/10/26 | FFE, spot elevations, wall top/bottom elevations, stair riser count, contours |
| **CS-101** | Dimension Control Plan | same file, p.7 | rev 6 03.10.26 | horizontal layout: walks, curb line, drop-off, plaza, stairs, site walls, paving notes |
| CX-101 / CX-102 | Site Details | same file, p.13–14 | rev 1 11.06.25 | curb and gutter (1'-6", 6" high curb), curb taper, paving details — referenced, profiles not modeled |
| CG-100, CS-100 | Overall grading / dimension control | same file, p.2, p.6 | — | context only |
| A012 (Rev 5), A302, A320 | Utility yard plan & sections; elevations; building sections | architectural | Rev 5 02/27/2026; Rev 3 | cross-check of wall heights and grade line against civil |

Topographic base (printed on the civil title block): survey dated January 2, 2024 by Cloninger Bell Surveying. The parking lot north of the building, the plaza to the east and Building I are **existing**; work for Building II is limited to the pad, the perimeter walks, the west utility yard and its walls and stairs. Streets to the west and south are "proposed … by others".

## 2. Vertical datum

| Item | Value | Source |
| --- | --- | --- |
| **Building II FFE** | **660.30** | W — CG-101 and CS-101 ("Proposed two-level medical office building 'Building II' FFE: 660.30") |
| Building I FFE (existing, not modeled) | 661.75 | W — CG-101 |
| Model Z = 0 | = 660.30 = architectural Level 01 0'-0" | all site Z values below are *elevation − 660.30* |
| Architectural "Average Grade" | −1'-9 3/4" = 658.49 | W — A300 (a code/zoning datum; **no longer used as the ground surface**) |

## 3. Horizontal registration of the civil sheets (no placement discrepancy)

CS-101 and CG-101 are 1" = 20' (3.6 pt per ft), north up, building square to the sheet. Registered to the building coordinate system (origin grid 1' × K') by fitting the civil building outline to the modeled finish faces: `x_ft = (X_pt − 455.0) / 3.6`, `y_ft = (1835.5 − Y_pt) / 3.6`.

Checks: (a) the civil building outline is 741.0 × 380.5 pt = 205.8 × 105.7 ft against the model's 206.35 × 106.93 ft finish / 205.0 × 105.83 ft face of stud — it sits between the two, residual ±0.3 ft; (b) of the ten "660.30" threshold spots on CG-101, **seven land on modeled doors** (100A, 101A, 100B, 100C, 102, 104, 110B) and the other three fall at the south recess and at the two ends of the CW5 storefront, where the civil sheet shows doors that the architectural shell does not model separately; (c) the civil generator-enclosure wall is within 0.2 ft of the architectural one. **Conclusion: the civil drawings show the building where the model has it, within ±0.5 ft. Nothing was moved.** All site positions are therefore **M ±0.5 ft**, plus ±1 ft digitizing tolerance for walk edges.

## 4. Documented grades (W unless marked V)

Proposed spot elevations (CG-101, blue), model coordinates in ft:

| Location | x, y | Elev. | Z (ft) |
| --- | --- | --- | --- |
| Door thresholds (ten places) | — | 660.30 | 0.00 |
| North walk at CW3 west end / at building NW corner | 60.7, 105.6 / −0.4, 105.4 | 659.80 / 659.40 | −0.50 / −0.90 |
| North walk near door 100A canopy | 69.9, 109.6 | 660.08 | −0.22 |
| Entry plaza at east pier | 140.1, 107.5 | 660.27 | −0.03 |
| Walk at lobby east return / NE building corner | 145.2, 99.2 / 205.9, 98.9 | 660.09 / 659.79 | −0.21 / −0.51 |
| NW walk down to the street | −5.4, 106.4 / −17.3, 110.2 / −16.9, 99.1 / −12.7, 91.9 | 659.31 / 659.09 / 659.59 / 659.80 | −0.99 / −1.21 / −0.71 / −0.50 |
| Transformer pad / grade outside its west side | −12.4, 81.8 / −27.6, 82.5 | 659.94 / 655.32 | −0.36 / −4.98 |
| Generator yard slab, north / south | −9.0, 64.1 / −12.7, 26.7 | 660.18 / 659.90 | −0.12 / −0.40 |
| South face grade at 7' recess / 9.1' jog / SE corner | 88.4, 1.4 / 149.7, 1.4 / 202.5, 1.0 | 657.49 / 658.47 / 658.50 | −2.81 / −1.83 / −1.80 |

Walls and stairs (CG-101):

| Item | Written values |
| --- | --- |
| West stair | "(8) 12" treads and (9) 6" risers with cheekwall and handrail"; **TS 660.10**, **BS 655.60** (4.50 ft = 9 × 6" ✓) |
| South-west stair | **TS 660.19**, **BS 656.88** (3.31 ft). Riser count **not given** → 7 risers assumed (**A**) |
| Transformer retaining wall | "Proposed retaining wall, top elev. **663.63**, material and finish to match adjacent enclosure" (= FFE + 3'-4", agrees with A012 T.O. masonry 3'-4"). **TW 659.87 / BW 655.53** at its NW corner |
| West wall at the stair | BW 656.28 |
| South-west low/retaining wall | **TW 659.71 / BW 656.98** at the generator-enclosure corner; **BW 656.44** at its south-east end |

Existing spot elevations "EX:" (V — drawn as linework, read by eye): north walk/curb 658.81, 658.70, 659.80, **660.14 ×3 along the flush drop-off curb**, 659.77, 659.72; plaza between the buildings 660.04; west side 655.47; south-west corner 656.37; west street gutter 654.60, 655.11, 654.75, 654.86, 654.92.

Contours (CG-101, 1-ft interval, labels 655–662): parking lot falls **north** from about 660 at the building to 658 at the Golf Links Dr edge; site falls **west** to 655 at the west street and **south-west** to 656–657 along the south street; rises east to 661 toward Building I.

Slopes: no slope percentages are printed on CG-101 or CS-101 for the walks. Derived from written spots (INT): drop-off/entry plaza 660.30 → 660.14 over about 12 ft ≈ 1.3 %; north walk west of the drop-off 659.80 → 658.70 over about 55 ft ≈ 2.0 %; NW walk 659.80 → 659.09 over about 18 ft ≈ 3.9 %. CS-101 notes "proposed accessible ramps, refer to CLDSM 50.10B" at the accessible parking stalls (standard detail, not dimensioned on the sheet — **not modeled**).

Curbs: CS-101 "parking lot barrier to be 1'-6" curb and gutter, typ." and "proposed curb transition, see detail 11/CX-101, **97.16'**" with "proposed sidewalk to meet flush with existing" — i.e. the curb is **flush along the drop-off** in front of the entrance. CX-101: 6" high curb. No top-of-curb / gutter spot elevations are printed other than the EX values above.

## 5. What is modeled and how

| Element | Basis |
| --- | --- |
| **Terrain surface** (replaces the flat ground) | 4-ft grid, heights by inverse-distance interpolation through every W and V spot, the contour positions and the hardscape edges. **Entire surface is INTERPOLATED, not exact**; it is exact only at the written spots. |
| North paver walk, drop-off band, entry plaza, east walk to Building I plaza | Outlines M from CS-101 (±1 ft); elevations W/V at the spots, linear between them (INT) |
| Curb | Walk slabs stand 6" above the asphalt except along the 97-ft flush drop-off zone (W: flush; W: 6" curb). Curb-and-gutter profile not modeled |
| Existing asphalt parking / drive; three nearest landscape islands | Region M from CS-101; surface = interpolated terrain (INT); islands raised 6" (A) |
| West stair (9 risers), landings, transformer pad, generator yard slab, SW walk and SW stair | Outlines M; elevations W as listed; SW stair riser count A |
| East door walks and existing plaza | Outlines M; 660.30 at doors (W), 660.04 at plaza (V) |
| Landscape beds | Ground shapes only (terrain faces given a "bed" material inside the bed outlines, M ±1 ft). No planting |
| Foundation skirts | New objects carrying the podium and the yard walls from the v005 base (−1'-9 3/4") down below the real grade, so nothing floats where the site is lower (south, west). Elevations A301/A302 show brick continuing to grade. **A** — depth arbitrary (to −8 ft), hidden below terrain |
| Paving materials | CS-101 notes (W): pathways Techo-Bloc "Linea" large rectangles, **Shale Gray**; header Techo-Bloc "Blu 60 Smooth", **Greyed Nickel** (not modeled); plaza Techo-Bloc "Westmount", **Onyx**. Colors are approximations of the names (INT-color). Asphalt, concrete, lawn and bed surfaces are plain representational colors |

Not modeled (by instruction or not documented): planting, trees, signage, bollards, bike racks, lighting, handrails, cheek walls, vehicles, parking striping, accessible-ramp detail, curb-and-gutter profile, storm structures, Building I, the streets' curbs and on-street parking (by others).

## 6. Conflicts between civil and architectural documents (flagged, not resolved)

| # | Conflict | Handling in v006 |
| --- | --- | --- |
| C-1 | **Transformer enclosure position.** Architectural A112 and A012 (Rev 5, 02/27/2026) put it at x = −26.4 → −10.7 ft. Civil CS-101/CG-101 **rev 6 (03.10.26, "Wall Revisions")** put the same 15'-9" enclosure at x = −28.6 → −12.9 ft — **2.2 ft further west**. Y position and size agree. | Yard walls are frozen v005 geometry → **kept at the architectural position**. The west paver walk is fitted to it (about 5.7 ft wide instead of the civil 8 ft). Needs the design team's answer; the civil sheet is the later one. |
| C-2 | **South-west low site wall height.** A012 section B2: T.O. masonry **+2'-8"** above Level 01 (= 662.97). CG-101 rev 6: **TW 659.71** (0.59 ft *below* FFE) at the same wall. Difference 3.26 ft. | Wall kept at the frozen architectural height. Terrain uses the civil BW values outside it. |
| C-3 | **Drop-off canopy outline.** Civil CS-101 shows a dashed canopy box about **88 × 24 ft** at x ≈ 57 → 145, y ≈ 111 → 135. Architectural A700 / S132 (written): **65'-7 1/4" × 23'-3"** at x = 77.5 → 143.1, y = 106.7 → 129.9. | Architectural canopy kept. The civil outline looks like an earlier design background. |
| C-4 | **Building outline.** Civil footprint is 0.3–0.6 ft smaller than the architectural finish-face footprint (it sits between face of stud and face of brick). | Within registration tolerance; no action. |
| C-5 | **Grade datum.** Architectural "Average Grade −1'-9 3/4"" is a single datum; civil grades at the building vary from −0.0 ft (north) to −2.8 ft (south) and about −5 ft at the west street. | Not a true conflict; v006 uses the civil grades. |
| C-6 | **Transformer enclosure gate vs. grade.** A012 shows the enclosure open to the **west** for a gate ("gate – see civil"). CG-101 rev 6 gives the pad at **659.94** but the grade just outside that west side at **655.32** and BW 655.53 — a drop of about 4.6 ft at the gate line. | Pad modeled at 659.94 on retained fill; outside grade follows the civil spots; the open west side is left as in frozen v005. How the gate is reached is not shown on the sheets reviewed. |
| U-6 (carried) | CS-101 revision-label conflict ("Revision 4" vs "Revision 5" for 02.11.26). | rev 6 sheet used. |

## 7. Assumptions

Flat-topped islands 6" high · 7 risers at the SW stair · foundation skirt depth · walks are planar between written spots · asphalt edge 6" below the walk where the curb is not flush · the three far street edges and the parking lot interior follow interpolated contours only · stairs drawn as plain steps without cheek walls or handrails.
