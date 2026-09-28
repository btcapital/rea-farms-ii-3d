# Building I — landscape / site coordination cleanup control document v007

Date: 2026-09-22
Applies to: `scripts\Building_I\BI_build_landscape_cleanup_v007.py` + `notes\Building_I\BI_landscape_data_v007.json` → `models\Building_I\BI_landscape_v007.blend`, renders `renders\Building_I\BI_landscape_v007_*.png`.
Base: **BI_landscape_v006.blend (owner-approved corrected exterior geometry baseline; v001–v006 frozen in `manifests\BI_freeze_BuildingI_v006_approved.json`, 101 files)**.
Scope: landscape / site coordination only (skill gate 4 close-out). No redesign, no presentation work. Building, facade regions, entrance correction, materials and all unaffected site/landscape objects are preserved exactly.

## 0. Carried forward (nothing discarded)
G-1…G-6 (v001), the v002 material placeholders and F-1…F-8, SC-1…SC-5 (v003), LC-1…LC-7 (v004), the v005 facade cleanup, the v006 entrance corrections (G-7 closed). New geometry items raised here for the owner/architect: **G-8** (south wing slab edge −4.38 vs Level 1 wall lines at −2.0/−2.6 with a −5.4 step only west of x 48.5), **G-9** (wing north wall at grids 1–3 at y ≈ 52.75 on A1.00a/A1.01 vs v001 61.12), **G-10** (north-east corner notched to x ≈ 268.9 between y 171.6 and 197.8 on A1.00a vs v001 281.0). The building is not moved.

## 1. Sources reviewed
| Source | Building | Sheet / page | Printed status | Used for |
| --- | --- | --- | --- | --- |
| LP-101 / LP-100 (PCO 24 p.13 / p.12) | I | rev 13 07.22.25 | plant symbols, callouts, schedule (as v004); bed-line style test; parking-lot curb lines | 
| A1.00a Level 1 Edge of Slab Plan (registered vector 6.750 pt/ft, x residual 0.07 ft, y residual 2.7 ft) | I (Rev 14 p.23) | rev 7 1/20/2025 | slab edge at the south face, wing north face and NE corner |
| A1.01 Level 1 Building Plan (registered vector) | I (Rev 14 p.26) | rev 14 9/25/2025 | exterior wall lines at the same three places |
| A0.04 Dumpster Enclosure Details | I (p.11) | 6/16/2025 | Roman brick veneer on 8" CMU, rowlock cap, steel gate, bollards |
| PCO 14 RTAP #3 drawing changes | I | 7/15/2025 | brick Roman → utility with soldier band (building brick) |
| CX-104 brick landscape retaining wall (PCO 24 p.5/14) | I | RFI 78 07.29.25 | 8" CMU grouted, 12"×24" footing, TW 661.00, top sloped 8 1/2" to the bed, "finish grade see CG-101" |
| CG-101 (PCO 50 p.4) spot elevations | I | 10/15/2025 | grade at the wall 659.36–659.51 |
| **LP-100 Overall Landscape Plan rev 2 (Carolina Sports MOB)** | **II — shared-street register** | `APPROVED-LDCP-2025-00715.pdf` p.12, 12.12.25 (approved 1/9/2026) | existing-tree symbols along N Rea Park Ln (18), N Old Springs Rd (24), Golf Links Dr (12), Midway Park Dr (7); registered on the 17 parking-island ovals shared with Building I LP-100 (2.40 pt/ft, residual ≤ 1.5 ft) |
| Photographs 2026-07-28 (0045, 0053), 2026-08-10 overview | genuine | — | validation only |

## 2. Issues

### A. Foundation planting vs approved footprint
- Documented condition: LP-101/CS-101 building line at the south face y ≈ −1.2; A1.01 wall lines at −2.0/−2.6 and A1.00a slab edge at −2.0 (x 48.5–244.8) and −5.4 (x 2.5–48.5); wing north wall between grids 1–3 at y 52.25–53.4 (A1.01) / 52.75 (A1.00a); NE corner slab edge at x 268.9 (y 171.6–197.8) with a second line at 282.75.
- Current model: v001 footprint south edge −4.38 (x 6.9–48.5 and 118–271), wing north face 61.12 (x 6.88–28.62), NE corner 281.0 without notch; v004 pushed 84 plants outward (1–9.9 ft).
- Determination: plant positions are registered to fixed site geometry (curb-line correlation, ±1.5 ft) and agree with A1.00a/A1.01; the landscape background is not stale. The conflict is in the approved v001 footprint at three places (G-8/G-9/G-10). **Correction:** the 31 plants whose push-out was caused by G-9 (8 DAZA at y 55.87, x 11.6–26.6) and G-10 (12 ABKA, 8 CORA, 3 BUNN at x 272–276, y 173–194) are **returned to their documented positions** (they are hidden inside the approved shell until G-9/G-10 are resolved, flagged U). The other 53 plants (south face and entrance band, shifts ≤ 5 ft) stay pushed clear of the shell as in v004, because there the drawn wall (−1.2) and the modeled slab edge differ by only 1–3 ft (G-8, tolerance-level). Confidence: positions V, decision I. Objects: 4 shrub/ground-cover group objects and their mulch discs.

### B. Unresolved plant symbols (121 in v004)
- Method tried: drawn-symbol signature matching against the legend symbols — **not discriminative** (7% accuracy on the 613 resolved dot plants), rejected. Leader targets with symbol-size support: the two EMRA callouts (26 + 11) each land within 9 pt of a chain of 4.2-ft-diameter circles (2.4 pt/ft × 10 pt = the 4 ft o.c. spacing of the 5-gal EMRA); chains of exactly 26 and 11 circles exist and coincide with no placed plant → **EMRA 37/37 resolved (I)**. Adjacency with schedule headroom (a resolved group of the same species within 6.5 ft, ≥ 2 neighbours): **LOJA +2, ABFR +2 (I)**. Not forced: ABFR 77+2/114, VIBL 36/96, JEWL 40/88, BUNN 3/42, BLON 3/28, DOUB 5/16, COFA 5/10, LACE 9/10 keep their shortfalls; 13 further 4-ft circles along the west face of the wing (x 5–9) remain unattributed.
- Result: species-unresolved symbols **121 → 117**; EMRA 0 → 37. Objects: `LS_shrub_UNRESOLVED_species_documented_symbol` rebuilt; new `LS_shrub_EMRA_LP-100_n26`, `_n11`, `LS_shrub_ABFR_LP-100_adj`, `LS_shrub_LOJA_LP-100_adj`.

### C. Ground-cover beds (11 interpreted discs, 7 skipped)
- Bed-line test: LP-101 draws "proposed mulch bed line" polylines in a distinct tan style (rgb 70 %, 2-pt), but they are open polylines along walks and islands, not closed bed polygons; hatch floods leak between adjacent beds (v004). No stronger extraction achieved. **Discs preserved as interpreted** (`_INTERPRETED` names, area = quantity × spacing²); the 7 leader targets landing on hardscape (CORA 19, CATM 48, OSOR 22, OSOR 31, CARZ 6, CARZ 25, CORA 1) stay **unresolved, not modeled**. Confidence I / U. Objects: none changed.

### D. Parking / island context
- LP-100 curb lines (grey 17-pt) flood-filled: unclipped 176,000 sq ft (leaks to the streets); clipped to x −225…310 / y 196…432 → 106,955 sq ft but the fill still runs into the perimeter lawn strip along Golf Links Dr through the two drive entrances, so the outline is not a curb polygon. CS-101 (v003) had the same stripe/curb line-weight problem. **No clearly documented correction → `SITE_asphalt_parking_north_APPROX` retained** (SC-3 stays open); 17 islands (LP-100 ovals, V) unchanged; island planting note 8 ("mound 6 in above back of curb") already modeled. Objects: none changed.

### E. Street trees
- Documented and modeled (v004): Golf Links Dr 14 and Midway Park Dr 8 (Building I LP-100 "existing to remain"). Building II LP-100 rev 2 (shared streets) shows the same trees (12 / 7 within its viewport) plus **18 existing-tree symbols along N Rea Park Ln (y ≈ −18, 40-ft spacing) and 24 along N Old Springs Rd** (x ≈ −333 and −298/−357). The N Rea Park Ln row is confirmed by photo 0053; the N Old Springs Rd rows (verge and median) are not photo-verified. **Added as `CTX_existing_street_tree_*_BII-LP100`** (position V ± 1.5 ft, size I). Photo-only trees: none remain unmodeled on N Rea Park Ln; LC-4 closes.

### F. Site detail open items
- Dumpster enclosure: A0.04 Roman brick veneer / rowlock cap / steel gate; PCO 14 changes the building brick to utility size but does not mention the enclosure; no closeout record → **unresolved (SC-1 stays)**; box unchanged.
- Landscape wall bottom: CX-104 gives no BW; wall bears on a 12"×24" footing below finish grade "see CG-101" → exposed height = 661.00 − 659.4 ≈ 1.6 ft; the modeled bottom 658.5 is below grade and invisible → **documented, no change** (SC-4 closes as "exposed height 1.6 ft, footing depth not modeled").
- Planter/bed edges: not extractable (C) → mulch discs remain.
- Island extents: 37 × 10 ft ovals (V) consistent with the LP-100 note "typical parking lot tree island minimum area 274 sq ft" → unchanged.

## 3. Objects affected in v007 (all inside `09_Landscape_v004*` sub-collections)
Rebuilt: `LS_shrub_DAZA_LP-101_n12`, `LS_shrub_ABKA_LP-101_n14`, `LS_groundcover_CORA_LP-101_n6`/`n5` (whichever holds the NE-notch plants), `LS_shrub_BUNN_LP-101_n15` and their `LS_mulch_*` discs; `LS_shrub_UNRESOLVED_species_documented_symbol`. Added: `LS_shrub_EMRA_LP-100_n26`, `LS_shrub_EMRA_LP-100_n11`, `LS_shrub_ABFR_LP-100_adj`, `LS_shrub_LOJA_LP-100_adj` (+ mulch discs), 42 `CTX_existing_street_tree_{N_Rea_Park_Ln,N_Old_Springs_Rd}_*_BII-LP100`. Unchanged: every other landscape, site, shell, facade, opening and camera object.

## 4. Validation planned
Hash of every mesh object outside the rebuilt/added set before/after; `BI_compare_geometry_v006_v007.py` (building, facade, openings, site identical; only the listed landscape objects changed/added); manifests v006-approved (101), project/Building II (311), Building I sources (1,231). Renders: front elevation (orthographic north), entrance oblique, north-west site oblique, elevated site view, landscape-focused entry view, and the rear/south comparison (v005 render vs v007) showing the largest landscape change (N Rea Park Ln street trees).
