# Model control document v003 — drop-off canopy verification pass

Date: 2026-09-21
Applies to: `scripts/build_shell_v003.py` → `models/building_shell_v003.blend`
Scope: **drop-off canopy only.** Everything else is `notes/model_control_v002.md` unchanged (which in turn carries v001's origin, axes, units, datums, grids and face-of-stud control lines). v001 and v002 files were not modified.

Codes: **W** written on the sheet · **G** grid position · **M** measured from exact-scale vector linework · **A** assumption.

## 1. Search performed

| Sheet / detail | File, PDF page | Result |
| --- | --- | --- |
| **S132 "Enlarged Canopy Plans", Section 01** (3/4" = 1'-0") | Approved set p.73 | **Stronger source found.** Section through the drop-off canopy on grid XA with written steel elevations — see section 2. |
| S131, "02 – Level 2 – Enlarged Front Drop Off Canopy" plan | Approved set p.72 | Member sizes for the drop-off canopy (W27X84 (PC) beams, HSS12X6X3/8 purlins). The only TOS tags on the plan — HSS20X12X1/2 **TOS 11'-8 1/2"** and HSS12X4X3/8 **TOS 11'-6 1/4"** — belong to the *main entry door canopy*, not the drop-off canopy. (They independently confirm the 11'-8 1/2" door-canopy top used in v002.) |
| S132 Section 71 | Approved set p.73 | Main entry door canopy / Level 2 edge. Not the drop-off canopy. |
| S133 | Rev 5 structural p.10 | Side canopy and sun-shade steel (TOS 11'-4", 31'-10", 32'-0"). Not the drop-off canopy. |
| A331 (A5 section), A330 | Rev 5 arch. p.11, p.10 | Drop-off canopy is drawn and labelled, with the note "light held tight to underside of canopy at lowest point". **No elevation or height dimension.** |
| A700 (A5 section, B4/B5 details) | Rev 5 arch. p.13 | Plan size, 1 1/2":12 slope, 1" laminated glazing, 7 1/2" / 1'-1" fitting offsets. **No vertical elevation.** (unchanged finding) |
| A320 building sections | Approved set p.34 | Canopy drawn, no canopy dimension. |
| S301–S303 (sections referenced from S131) | Approved set p.83–85 | No drop-off canopy elevation text found. |

Revision status: S131 and S132 are permit issue E (09/29/2025), county-stamped, and were **not** reissued in Revision 5, so they are current under the approved source rule.

## 2. Written values from S132 Section 01 (all W)

| Item | Elevation |
| --- | --- |
| Top of column cap plate (W16X100 column, 1" cap plate) | **15'-1 1/2"** |
| Bottom of tapered W27X84 (PC) beam at the column | **13'-0"** (beam 2'-1 1/2" deep at column) |
| North tip — top of beam / bottom of beam | **16'-11 15/16"** / **16'-4"** (0'-8" deep) |
| South tip — top of beam / bottom of beam | **15'-8 15/16"** / **15'-1"** (0'-8" deep) |
| Horizontal reach from grid XA | 16'-7 1/2" north, 6'-7 1/2" south (agrees with A700); XA to grid A 9'-11 3/4" |
| Purlins | HSS12X6X3/8, 0'-6" from each tip, then 5'-0 3/8" o.c. (north, 4 purlins) and 5'-0 1/4" (south, 2 purlins), measured along the slope |
| Bottom plate | 10" × 3/4" PL |

Cross-check: the beam-top linework on S132 slopes exactly 0.1250 (1 1/2":12, as A700), and scaling the linework from the 13'-0" tag reproduces the 16'-11 15/16" and 15'-8 15/16" tags to within 0.002 ft.

## 3. What is still measured

The **glass** elevation is not written anywhere. S132 draws the glazing above the purlins for reference; on that linework the top of glass is **1.322 ft vertically above the top of the beam** (M, 3/4" scale, ±0.03 ft), and the two glass sheets stop 0.364 ft short of grid XA (M). v003 places the glass at the written top of steel plus this measured offset.

| Value | v002 | v003 | Status |
| --- | --- | --- | --- |
| Top of glass projected to grid XA | 16.10 ft (M, A700 at 3/8" scale) | **16.24 ft** | steel W + offset M |
| Top of glass, north edge | 18.18 ft | **18.32 ft** | steel W + offset M |
| Top of glass, south edge | 16.93 ft | **17.07 ft** | steel W + offset M |
| Top of column | 15.0 ft (M) | **15'-1 1/2"** | **W** |
| Column size | 14" square (A) | W16X100: 17" (north–south) × 10 3/8" | **W** member size |
| Beams | not modeled | tapered W27X84 at X1, X2, X3, 10" wide | **W** elevations |
| Purlins | not modeled | 6 × HSS12X6, full canopy length | **W** size and spacing; drawn vertical-sided (A) |
| Glass thickness | 3" placeholder (A) | 1" | **W** (A700) |

The v002 measured value was within 0.14 ft (about 1 3/4") of the result now tied to written steel.

## 4. Status of the canopy after v003

- Steel geometry: **resolved** by written dimensions.
- Glass height: **no longer provisional in the v002 sense**, but still carries one measured component (the 1.322 ft glass-above-steel offset). It would become fully written only if a glazing shop drawing or a dimensioned A700 detail gives the fitting height. Collection renamed from `04_DropOff_Canopy_PROVISIONAL` to `04_DropOff_Canopy`; the measured offset is recorded on the glass objects' `source` property.
- Not modeled: spider fittings, gutter, downspouts, stiffeners, cap plates, base plates/footings (S132 shows footing at −2'-0"), beam taper in plan, column web/flange shape (columns are plain boxes of the W16X100 overall size).

## 5. Assumptions and open items

Unchanged from `model_control_v002.md` sections 5 and 6, except:
- **U-4 closed** for steel; replaced by **U-4a**: glass-above-steel offset 1.322 ft is measured, not written.
- A-6 revised: column and beams now follow written member sizes; purlins drawn with vertical sides rather than square to the slope.
- V-1 (architectural revisions 6–10 not in hand) still open. Note S131/S132 are structural sheets from the permit issue; any later structural revision to them is likewise not in hand.
