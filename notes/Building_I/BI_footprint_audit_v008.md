# Building I — footprint audit v008 (G-8 south edge, G-9 wing north wall, G-10 north-east notch)

Date: 2026-09-23
Baseline audited: `models\Building_I\BI_landscape_v007.blend` (v006 owner-approved exterior geometry + v007 landscape, not approved). Footprint = `BI_geometry_data_v001.json → footprint_union` (v001, unchanged through v007).
Status: **audit complete — v001 footprint is incorrect at all three disputed places and at four further places with the same cause; corrections are clearly established by the Rev 14 record set → Building I v008 built (see §9 and `BI_footprint_validation_v008.md`).**
Frozen before any change: `manifests\BI_freeze_BuildingI_v007_pre_v008.json` (114 files: every v001–v007 note, data file, script, model and render; PASS).

## 1. Sources reviewed (priority order of the owner's instruction)

| # | Sheet (Rev 14 record set 9/25/2025 unless noted) | Page | Printed status | Type | Used for |
| --- | --- | --- | --- | --- | --- |
| 1 | A1.01 Level 1 Building Plan | 26 | rev 14 9/25/2025 | vector | exterior wall lines at every disputed edge; general note 2 "all exterior dimensions are to outside face of wall assembly" |
| 2 | A1.02 Level 2 Building Plan | 27 | rev 13 7/25/2025 | vector | Level 2 wall lines (which Level 1 lines are one-storey projections / recesses) |
| 2 | A2.11 Level 1 Plan Detail Callout Plan | 36 | — | raster image only | not usable as vector; not needed |
| 3 | A1.00a Level 1 Edge of Slab Plan | 23 | rev 7 1/20/2025 | vector | slab-edge (ribbon-slab hatch clip) polygons — the v001 source |
| 3 | A1.00b Level 2 Edge of Slab Plan | 24 | rev 6 11/15/2024 | vector | Level 2 slab-edge polygons |
| 4 | S101 Foundation Plan (Moore Lindner) | 132 | rev 6 11/15/2024 | vector | foundation wall / footing lines at every disputed edge |
| 5 | A4.01 / A4.02 Building Elevations | 64 / 65 | 6/16/2025 | raster | one-storey vs two-storey conditions, projecting boxes, recesses (validation) |
| 6 | A5.11 A3, A5.12 A1/A2/A3, A5.15 A2 Exterior Wall Sections | 71, 72, 75 | 10/25/2024 – 7/25/2025 | raster image + text | heights of the storefront projections, Level 2 bay and gallery cantilever (written dimensions read on the sheet) |
| 6 | A1.00c Roof Edge of Slab Plan, A1.03 Roof Plan | 25, 28 | rev 7 / rev 12 | vector | roof edges tied to the disputed walls |
| 7 | CS-101 / LP-101 backgrounds (PCO 17 p.10, PCO 24 p.13) | — | 07.22.25 | vector | secondary registration check only (building line y ≈ −1.2, x ≈ 281) |
| 8 | Photographs 2025-09-09 (south side), 2026-07-28 drone a/b | — | genuine | validation only |

Not used: Rev 6 permit set (audit only), AI-generated images (never evidence), Building II architectural sheets.

## 2. Independent registration of the controlling plans (grid bubbles only)

Method (`scratchpad …/v8/register.py`): the centres of the numeric grid-bubble labels in the top/bottom margins constrain x, the letter bubbles in the left/right margins constrain y; rotation from the alignment of each bubble row/column; robust least squares dropping bubbles whose residual exceeds 1 ft (the bent-leader bubbles at the close grids 12.9, H, J, C.9, C.6, B, M.7, F.2, D, G.1, G.2, K.1, K.7 — their labels are offset along the column). No title-block text, sheet labels, revision clouds or annotations were used. Scale cross-checked against written grid dimensions on S101 (12'-4", 17'-8", 10'-0", 5'-0", 15'-0", 12'-0", 18'-0", 30'-0" … = 280'-0" grid 1→14; 4'-0", 17'-8", 8'-4" … = 198'-6 3/8" grid A→N) and the written 5'-4" / 4'-8" storefront rhythm on A1.01 (33.7 pt per 5'-0").

| Sheet | Scale (pt/ft) | Scale (1" = ) | Rotation | Translation (grid 1, grid A in pt) | Bubbles used | RMS | Max |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **A1.01** | 6.7500 (x), 6.7502 (y) | 10.667 ft = 3/32" = 1'-0" | −0.0008° | x 199.81, y 1795.91 | 29 (14 x, 15 y) | **0.027 ft** | **0.113 ft** |
| A1.02 | 6.7499 / 6.7505 | 3/32" = 1'-0" | 0.022° | 197.71, 1796.00 | 30 | 0.015 ft | 0.069 ft |
| A1.00a | 6.7497 / 6.7442 | 3/32" = 1'-0" | −0.0015° | 254.06, 1794.75 | 31 | 0.073 ft | 0.19 ft |
| A1.00b | 6.7499 / 6.881 (y under-determined, 7 y bubbles) | 3/32" | 0.002° | 253.98, 1800.56 | 21 | 0.23 ft | 0.75 ft |
| A1.00c | 6.7496 / 6.7504 | 3/32" | −0.0013° | 254.07, 1795.99 | 32 | 0.038 ft | 0.165 ft |
| A1.03 | 6.7496 / 6.7505 | 3/32" | −0.0013° | 227.07, 1822.93 | 33 | 0.026 ft | 0.113 ft |
| **S101** | 6.7501 / 6.7506 | 3/32" | 0.011° | 230.43, 1901.21 | 66 (two rows / two columns) | **0.025 ft** | **0.152 ft** |

The v007 registration of A1.01 (y residual 2.7 ft) had included bent-leader bubbles; the independent registration confirms the disputed wall lines within 0.1 ft (wing north wall 54.15–54.22 instead of the v007 estimate 52.25–53.4; NE notch 268.28 instead of 268.9; south lines −4.16 / −1.46 / +2.88 instead of −2.0 / −2.6).

## 3. Root cause of the v001 footprint error (applies to G-8, G-9, G-10 and to G-11…G-14)

`BI_extract_tools_v001/slabunion.py` unioned **every `<clipPath>` polygon** of A1.00a and A1.00b and traced the outline of the union. Those sheets carry two kinds of clips: the fractional-coordinate polygons that really bound the ribbon-slab / slab hatch (e.g. `clip-1`, 72 vertices) and, for every hatch group, an **integer-coordinate axis-aligned rectangle** that is the hatch viewport (`clip-0` 301,1382–2086,1824 pt = x 6.95…271.42, y −4.23…61.20 ft; `clip-2` 120.59…280.01 × 71.86…196.95; `clip-4` 148.45…241.05 × 186.74…202.87; `clip-11` 240.60…281.05 × 155.65…198.43; A1.00b `clip-0` 263.85…287.11 × 98.08…160.72). The rectangles are bounding boxes, not slab edges. Their union filled every recess, notch, step and one-storey projection: the flat south edge at −4.38, the wing north face at 61.12 (= the top of `clip-0`), the north-east corner at x 281 (`clip-11`), the east face at 287 from y 97.9 to 160.4 (A1.00b `clip-0`), the flat north face at 202.88 (`clip-4`) and the flat west face at 6.88 (`clip-0`). The footprint was then extruded to the zone roof height, so one-storey elements and Level 2 overhangs became full-height walls. A second, independent defect: `prism()` triangulated the concave caps with bmesh EAR_CLIP, which overlaps triangles on these outlines (the cap area of the south wing came out 8 % larger than its polygon) — the same mechanism as the v006 false overhang.

Note also that the v001 control document equated "slab edge" with "outside face of wall assembly". On the brick walls the A1.01 outside face lies **0.55 ft outside** the A1.00a slab edge (brick ledge on the foundation wall: −1.46 vs −0.91, 281.62 vs 281.05, 10.67 vs 11.28); at storefront and curtain wall the two coincide within 0.07 ft (−4.16 vs −4.23). This is why the civil/landscape backgrounds (drawn to the brick face, y ≈ −1.2, x ≈ 281) never matched v001.

## 4. G-8 — south edge

| Item | Finding |
| --- | --- |
| Current modeled condition (v001–v007) | `BI_Z1_south_wing` south face a single plane **y = −4.38** from x 6.88 to 271.38, full height 0–33.3 ft (+ PNL1 screen strips to 40). `BI_Z5_end_block_13_14` starts at y 60.5. |
| Controlling drawing condition (A1.01, outside face of wall assembly) | five different planes: **y = −4.16** x 7.0–48.5 (storefront SF2 in the dark PNL2 box, one storey); **y = −1.46** x 48.5–91.66 and 118.33–241.67 (brick BRK1, two storeys); **y = +2.88** x 91.66–118.33 and **+2.91** x 241.67–271.29 (recessed bays, two storeys, PNL3/CAP1 windows); the Level 2 wall behind the storefront box is at **−1.46** from x 10.67 (A1.02 heavy lines y −1.45, x 10.67–62). A Level 2 storefront projection (`SF2` box, A4.01 grids 9–11) stands at **y = −4.15** for x 172.01–228.01 between z 12'-7" and 27'-4". |
| Written dimensions | A1.01: 40'-10" (storefront box length, pier at x 7.67 → step at 48.5 = 40.83 ft ✓), 5'-4"/4'-8" window rhythm, 1'-11 1/2" + 1'-0 1/2" jambs at the recess piers; A5.12 A1/A2: storefront 3'-0" sill + 8'-0" = 11'-0" head, fascia 8" + 1'-10" below LVL-02 15'-4" → projection top **13'-6"**; A5.11 A3: bay bottom LVL-02 − 2'-9" = **12'-7"**, head T.O.S.@A 30'-0" − 5'-2" = 24'-10", fascia 8" + 1'-10" → **27'-4"**. |
| Exact / vector-measured | A1.01 −4.16 / −1.46 / 2.88 / 2.91 (±0.05); S101 foundation −4.22 / −1.52 / 2.85 (±0.05); A1.00a slab −4.23 / −0.91 / 2.84; A1.00b Level 2 slab −0.95 (x 11.33–91, 119–241), 3.06 (x 91–119, 241–271), −3.46 (x 171.05–228.97, the bay); CS-101/LP-101 building line −1.2 (civil, brick face within 0.3 ft). |
| What each line represents | −4.16 = exterior face of the one-storey storefront projection (A5.12 "Wall Section @ Level 1 Storefront Projection"); −1.46 = exterior brick face of the two-storey wall; −0.91 = Level 1 slab edge behind the brick ledge; +2.88 / +2.91 = exterior face of the recessed bays on both levels; −4.15 (Level 2 only) = face of the Level 2 storefront projection (A5.11 "Wall Section @ Level 2 Storefront Projection"); −4.38 (v001) = bottom of the hatch-clip rectangle — **not a building line**. |
| Does the slab project beyond the wall? | No. Where the wall is brick the slab edge is 0.55 ft *inside* the wall face; at the storefront they coincide (0.07 ft). |
| Does the modeled wall follow the slab edge? | No — it follows the clip rectangle, 0.2 ft outside the storefront and 2.9–7.3 ft outside the brick wall and recesses. |
| v001 correct? | **Incorrect** over 224 of 264 ft of south face (correct within 0.22 ft only at the storefront box x 7–48.5). |
| Confidence | V (five independent vector lines agree within 0.06 ft), heights W (A5.11/A5.12 written). |
| Recommended correction (built in v008) | Level 1 outline per A1.01; Level 2 outline per A1.02 (storefront box 0–13.5 ft only); Level 2 bay 172.01–228.01 × −4.15…−1.46 × 12.58–27.33; south face should move: yes, by +2.92 ft (brick), +7.26 / +7.29 ft (recesses), +0.22 ft (storefront box). |

## 5. G-9 — wing north wall, grids 1–3

| Item | Finding |
| --- | --- |
| Current modeled condition | wing north face **y = 61.12** from x 6.88 to 28.62 (full height 33.3); lobby band `BI_Z2_band_E_F2` 28.62–71 × 61.12–74.38 (top 40→36). |
| Controlling drawing condition | A1.01: exterior wall from x 10.67 to 28.5 with faces y 53.03 / 53.58 (inside) and **54.15–54.22 (outside)**; nothing is drawn north of it at grids 1–3 (exterior); the lobby west wall turns north at **x = 28.50** and runs from 54.22 to the curtain wall at 74.13–74.54 (grid F.2). Level 2 identical (A1.02 y 53.04/53.59/54.16, x 28.5). The MOB shell 150 S lies south of this wall; Corridor 102 / Tele 148 lie north of it only east of x 29. |
| Written dimensions | A1.01 along the wall: 3'-8", 4'-0", 10'-4", 4'-3 1/8" (window/pier string); 1'-0 1/2" pier at grid 1; S101 grid D = 52'-4" from grid A (chain 4'-0" + 17'-8" + 8'-4" + 12'-0" + 8'-0" + 2'-4") — the wall face lies 1'-10 1/2" north of grid D. Roof: A1.00c / A1.03 roof edge at 54.07–54.35 (x 11.84–28.5). |
| Exact / vector-measured | A1.01 54.15 (sw3) / 54.22 (sw10); S101 54.14 (foundation wall, x 10.68–29.27) and 53.51 (slab edge line x 11.3–88.97); A1.00a slab 53.47; A1.00b Level 2 slab 53.48 (x 11.33–71); A1.00c 54.35 / A1.03 54.20 roof edge. |
| What the lines represent | 54.2 = exterior face (brick) of the wing north wall and of the roof edge above it; 53.47 = slab edge (brick ledge 0.7); 61.07 = the Level 1 ribbon under the **interior** bearing line E (x 89–271) — its bounding box gave v001 its 61.12; 61.12 is not a plane of the wing at all. Different architectural planes: yes — 54.2 is the wing wall, 61.1 is an interior ribbon 60 ft further east. Roof/slab projection: none. |
| Is the landscape bed outside the building as drawn? | Yes — the DAZA row at y 55.87 (x 11.6–26.6) sits 1.7 ft north of the wall face, in the bed shown on LP-101; the plants were not used to decide the wall. |
| v001 correct? | **Incorrect** — the wall is 6.9 ft too far north for 17.8 ft of length (x 10.67–28.5), and the lobby's west face is exposed from y 54.2 (not 61.12). |
| Confidence | V (A1.01, A1.02, S101, A1.00a, A1.00c, A1.03 agree within 0.2 ft). |
| Recommended correction (built) | wing north wall y = 54.20, x 10.67–28.50; lobby band 28.50–71.0 × 54.20–74.38 (west face x 28.50 per A1.01/A1.00c, top unchanged); openings `BI_open_NORTH_001…009` moved −6.89 ft; lobby west-face finish regions W2/W2b extended to u0 54.2. |

## 6. G-10 — north-east notch

| Item | Finding |
| --- | --- |
| Current modeled condition | `BI_Z4a_north_block` east face **x = 281.0** from y 160.5 to 198.5 (and 287.0 from 97.9 to 160.4); north face 198.5 for x 241–281. |
| Controlling drawing condition | A1.01: east wall of the courts block at **x = 268.28** (outside face; inner lines 268.91 / 269.30 / 269.94) from y 171.67 to 197.9 with 9'-0" windows and 10" piers; the **Gallery Stair 126** block projects east to **x = 281.62** between y 134 and 170.41, its north face at **170.41** (heavy lines 169.24–170.41). North face of the courts block at 197.91 (x 211–268.6). Level 2 (A1.02): stair 226 landing to 287.39 × 165.9–170.6, otherwise the same notch (x 271.35 wall line at y 170.6–200). Roof (A1.03 rev 12) and structural (S101): notch present. Elevation A4.01 east: the TWS1/SF1 bay at M–N is the notch face seen beyond the stair block. |
| Written dimensions | A1.01 notch wall: 9'-0" + 10" + 9'-0" + 10" + 7'-1" + 11" windows/piers, 1'-11" / 2'-7" / 8" at the corner, 5'-9 1/4" stair-block return, 1'-8" jamb; A1.02: 14'-1 7/8" + 7'-0 1/2" landing (x 265.7 → 286.9). |
| Exact / vector-measured | A1.01 268.28 (y 171.67–197.04), 170.41 (x 270.04–281.67), 281.62 (y 44.89–170.41); S101 268.31 (y 170.34–196.97), 170.34 (x 268.84–281.68), 281.64 (y 59.31–170.34); A1.00a slab 268.93 (notch), 281.05 (stair block), 169.6 (stair-block north edge). |
| What the lines represent | 268.28 = exterior brick face of the courts block east wall; 281.62 = exterior face of the Gallery Stair block (and of the whole east face south of it); 170.41 = exterior face of the stair block's north wall; 281.0 (v001) = east edge of the `clip-11` rectangle; the "notch" is an **architectural notch** (re-entrant corner) — real. |
| v001 correct? | **Incorrect** — v001 filled the notch: 13.3 ft × 27.5 ft ≈ 370 sq ft of false footprint, full height. |
| Confidence | V (A1.01, A1.02, S101, A1.00a, A1.03 agree within 0.65 ft — the 0.65 is the slab-to-brick offset). |
| Recommended correction (built) | notch x 268.28 × y 170.41–197.91; stair block east face 281.62, north face 170.41; Level 2 stair landing 281.62–287.39 × 165.92–170.41 above the gallery soffit (I: same soffit as the gallery). |

## 7. Further footprint discrepancies found with the same root cause (new items)

| Item | Where | Modeled (v001) | Documented (A1.01 / A1.02 / S101) | Δ | Conf. | v008 |
| --- | --- | --- | --- | --- | --- | --- |
| **G-11** west face of the wing | grids 1–2, y −4.2…54.2 | flat plane x 6.88, full height | Level 1: x 7.0 (y −4.16…−2.35), **canted storefront** from (8.59, −2.35) to (10.93, 18.42), recessed entry door x 12.30 (y 18.42–28.74), TWS projection x 7.0 (y 28.74–38.63), brick x 10.67 (y 38.63–54.2). Level 2: x 10.67 throughout (y −1.46…54.2). Projections are one storey (A5.12 A3/A4, top 13'-6"); A4.02 west elevation: dark one-storey SF1 box at B–C, two-storey brick above/behind. | up to 5.4 ft | V / W | corrected |
| **G-12** east face y 97.9–170.4 | grids 13–14, J–M.7 | x 287.0 full height (y 97.9–160.4), 281.0 above | Level 1 wall **x = 281.62** (A1.01, S101 281.64); Level 2 **Gallery 234 / Lounge 235 cantilever** to 287.39 (y 97.92–107.5), 284.4 (107.5–121.9), 284.62 CW1 (121.9–156.2) over a soffit at ≈ 9.0 ft (A5.15 A2, 1/2" = 1'-0", M ± 0.3); A1.00b slab 287.01 / 285.09 / 284.22. | 5.4 ft at grade | V (plan) / M (soffit) | corrected (soffit M) |
| **G-13** rear vestibule 133 | grids 13–14, C.6–D | end block starts at y 60.5 (x 271.38–281) | end block + rear vestibule: x 271.29–281.62 from **y 44.21** (A1.01 y=44.21, x=281.62 from 44.89; A1.02 44.44 / 281.38), two storeys; parapet not separately dimensioned → top kept at the v001 end-block 32.0 (R) | 16.3 ft × 10.3 ft missing | V (plan) / R (top) | corrected |
| **G-14** north face x 149–268 | grids 9–12.9, N | flat plane y 202.88 (x 148.4–241), 198.5 (241–281) | Level 1: 203.03 (x 149–165), diagonal to 198.55 (x 187.55–202.72), 203.03 (202.72–211), **197.91** (211–268.28) (A1.01; slab 202.82/198.34/197.45; S101 196.97/197.59); Level 2: 203.03 (149–210.14), **200.9** (210.14–240.66) (A1.02 / A1.00b) → Level 2 overhangs the Level 1 recess (soffit = slab underside 14.83, A) | up to 5 ft | V / A (soffit) | corrected |
| **G-15** brick-ledge tolerance on unchanged faces | north-block west face (x 71 / 72.88 / 89–91), north face x 91–148 (197.5) | slab-edge positions | outside faces 70.33 / 72.66 / 90.70 and 198.07 — 0.5–0.7 ft outside | ≤ 0.7 ft | V | **not changed** (documented tolerance; v006 entrance geometry preserved) |

Consistency check of the corrected outline against the landscape plan: with the v008 Level 1 outline, **all 84 plants that v004 had to push out of the v001 footprint sit at their documented LP-100/LP-101 positions with no conflict (0 pushed)** — an independent confirmation that the landscape backgrounds were never stale.

## 8. Conclusion

G-8, G-9 and G-10 are all v001 errors with one documented root cause; none of the three represents a slab projection, foundation projection, canopy or structural element. The controlling condition is established by five mutually consistent vector sources (A1.01, A1.02, A1.00a, A1.00b, S101), by the roof plans where roof edges follow the walls, and by the wall sections for the heights of the one-storey / Level 2-only elements. Nothing remains unresolved for the three items; the only assumed values in the correction are the soffit of the north-face Level 2 overhang (14.83 ft, slab underside, A), the gallery soffit measured from A5.15 (9.0 ft, M ± 0.3), the stair-landing soffit (I) and the rear-vestibule parapet (R, v001 end block). The brick-ledge offsets on the faces that were *not* wrong (G-15) are left as a documented tolerance so the approved v006 entrance geometry stays untouched.

## 9. Correction carried out (Building I v008)

`scripts\Building_I\BI_build_footprint_fix_v008.py` + `notes\Building_I\BI_footprint_data_v008.json` → `models\Building_I\BI_footprint_v008.blend`. Only the affected shell geometry and its dependents were rebuilt: south wing (Level 1 / Level 2 prisms), lobby band, end block, north block (three level prisms), Level 2 bay; the 376 opening placeholders re-placed on the corrected faces (same extents); parapet screen strips; Level 2 slab reference; foundation skirts; finish regions regenerated (`BI_facade_regions_v008.json` = v005 data + W2/W2b/S7/N6 extents); the 14 landscape groups holding formerly pushed plants rebuilt at their documented positions. Canopy, vestibule, mechanical screen, grid, site surfaces, materials and all other landscape objects are unchanged (hash-verified). Validation, renders and the square-foot change are in `BI_footprint_validation_v008.md`.
