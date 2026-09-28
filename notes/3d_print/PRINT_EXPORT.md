# Building II — print exports and first-print guidance

* **Part A — v002 at 1:240 (2026-09-25): CURRENT.** Four 3MF files, validated, **awaiting owner approval before the full print**.
* Part B — v001 at 1:250 (2026-09-23): superseded and kept below unchanged. Its files are still on disk and were not overwritten.

---

# Part A — v002 export (1:240, millimetres)

| | |
| --- | --- |
| Source | `models\Building_II\print_derivatives\building_II_print_v002.blend`, SHA-256 `9aa5e3a4574e758f7fc914d9e6df887482791585a673d8b542420e7f4369a27c` (read-only during export) |
| Frozen v023 | `7fe33f1e4dc906c75b54122203fec75ee9ef948be70897e46fcfd1b288235c91`: identical before and after |
| v001 | `c4684e8d8345ff3105599b4ed2dbc67dbb47bc04bef0822bbae2eb8e36242875`: identical; v001 exports untouched |
| Exporter / validator | `scripts\3d_print\export_print_v002.py` / `scripts\3d_print\validate_export_v002.py` (reads the files back from disk) → `validation\print_export_v002_written.json`, `print_export_v002_validation.json` |
| Units | **millimetres**. 3MF declares `unit="millimeter"`. Vertices = model metres × 4.1667 (1:240, 1 in = 20 ft), matching the approved v002 mesh within 0.0001 mm. No other scaling. |
| Format | 3MF only, as requested. No v002 STL was written, so the old STL "touch point" welding issue can't arise. |

## A1. Files (`exports\Building_II\3d_print\3mf\`)

| Component | File | Size, model axes (mm) | On the bed as placed in the 3MF (mm) | Triangles | Vertices | SHA-256 |
| --- | --- | --- | --- | --- | --- | --- |
| Building body | `building_II_v002_1-240_building_body.3mf` | 266.09 × 143.64 × 65.83 | same, upright | 10,556 | 5,280 | `5b3d85eae4ea6d98d452241eafe75bf136aa6f7bb5cd303bb4293d8b340a82dd` |
| Site base | `building_II_v002_1-240_site_base.3mf` | 317.71 × 189.58 × 37.47 | same, upright | 84,862 | 42,433 | `9d99a9b5d7dbd6b7f92a8fb0cad541cc458a457f46aa5c74c8e3901b37131f64` |
| Porte cochère | `building_II_v002_1-240_dropoff_canopy.3mf` | 83.33 × 29.75 × 25.35 | 83.33 × 25.35 × **29.75 tall** (standing on its south edge) | 636 | 284 | `43466f1cf3616954abd80f6234b36b0ca12a30ac079e2448c6cefc5add4e29ba` |
| Sun-shade | `building_II_v002_1-240_sunshade.3mf` | 194.02 × 102.32 × 1.27 | same, **top face down** | 5,534 | 2,401 | `c4b36b22fd82cd4eaa15cd3bc2129ebf7d1ecb9f3842451233587c0f26bd739e` |

**Component count: 4 files, 1 object and 1 build item each.**

**Validation, all four files:**
- `unit="millimeter"`;
- watertight: 0 open, 0 non-manifold and 0 duplicated edges;
- normals outward;
- **1 component** each;
- size equal to the approved v002 size;
- the build transform is rigid (rotation and translation only), with the part's lowest point at Z = 0 and at least 11 mm clear of every bed edge.

**Triangulation:** body, canopy and sun-shade use exactly Blender's triangulation of the approved mesh. In the site base, 139 of 84,862 triangles inside 14 faces are split with the other diagonal, because the default split folds onto itself.
- 13 of those faces are flat walls or near-flat.
- One is a steep interpolated-terrain patch beside the transformer yard, which is up to 2.4 mm out of plane printed.
- The total volume change is 0.15 mm³.

Degenerate zero-area triangles: body 12, site base 39. They are harmless.

## A2. Recommended orientation, supports and brim

The 3MFs already open in these orientations.

| Part | Orientation | Supports | Brim |
| --- | --- | --- | --- |
| **Building body** | upright, foundation on the bed | **Paint** tree supports only under the three door-side canopies (main entry, door 100A, east), about 680 mm² in total. Keep automatic supports off, because window heads and rib/cap undersides (≤ 1.3 mm) bridge by themselves. | none |
| **Site base** | upright, long side along the bed's 340 mm X axis (11 mm free each side) | none (the 4 luminaire heads overhang 2.8 mm; slight droop is acceptable) | none (≤ 5 mm if you want one) |
| **Porte cochère** | **standing on its south edge**: the glass wings are vertical and the three columns point sideways | **Tree (auto), build plate only**, threshold about 30°. Bambu should place supports **only under the three horizontal columns** (about 390 mm²). Check the preview: if any support lands on the glass wings, remove it with a support blocker. Top Z distance 0.2 mm, 2 interface layers. Remove each support by cutting it at the column and pulling it straight down, never levering against the roof. | **5 mm outer brim**, brim-object gap 0.1 mm (the bed contact is the 1 mm south glass edge plus three beam ends) |
| **Sun-shade** | **top face down** (already flipped) | none | **4 mm outer brim** (a large thin 1.27 mm lattice) |

## A3. Suggested Bambu Lab H2S setup

Starting points to confirm on the first plate; they are not a Bambu specification.

* **Nozzle:** standard **0.4 mm** hardened steel. The v002 minimums (0.70 mm ribs, 1.0 mm fins and bars, 1.4 mm posts) were set for a 0.4 mm nozzle; no 0.2 mm nozzle is needed.
* **Material:** single-colour matte PLA (for example Bambu PLA Matte, white or light grey), stock PLA profile, no chamber heating.
* **Plate:**
  - Textured PEI for the body, site base and porte cochère.
  - Smooth PEI (or Cool Plate / SuperTack) for the sun-shade, whose visible top prints against the plate.
* **Layer height:**

  | Part | Layer | Profile |
  | --- | --- | --- |
  | Building body, porte cochère, sun-shade | **0.12 mm** | "0.12mm Fine" |
  | Site base | **0.16 mm** | "0.16mm Optimal" |

  First layer 0.2 mm.
* **Walls:** **3 wall loops**, Arachne wall generator (default). The 0.70 mm ribs and 1.0 mm members print as one or two lines. Top shell 5 layers, bottom 4.
* **Infill:**

  | Part | Infill | Notes |
  | --- | --- | --- |
  | Building body | 10 % gyroid | 1,438 cm³ if solid |
  | Site base | 10 % gyroid | |
  | Porte cochère, sun-shade | 15 % | effectively all wall |
* **Speed:**
  - Fine-profile defaults; keep "Slow down for overhangs" on.
  - For the porte cochère (small and tall on a thin edge), a lower outer-wall speed (about 60 mm/s) and the default minimum layer time help avoid wobble.
* **Support details, where used:** Tree, build plate only, top Z distance 0.2 mm, 2 top interface layers, XY distance 0.35 mm, "Remove small overhangs" on.
* **Fit settings:** leave elephant-foot compensation at the default 0.15 mm and X-Y compensation at 0. The v002 clearances already include the coupon lesson (0.50 mm pocket and 0.40 mm sockets, with lead-ins).
* **Import:**
  - Open the 3MF files; don't use Auto-orient.
  - If Bambu asks to load several files as one object with multiple parts, answer **No**.
  - Don't let Bambu rescale or "convert units".

## A4. Expected problem areas

1. **Porte cochère on its edge:**
   - It is a 30 mm-tall part standing on a 1 mm × 83 mm edge. Adhesion and wobble are the risks, which is why it gets the 5 mm brim and slower walls.
   - The three column supports must come off by cutting, not twisting.
   - If Bambu offers to "auto-orient" it back upright, decline.
2. **Sun-shade:**
   - Large thin lattice (194 × 102 × 1.27 mm): corner lift is the main risk (brim, clean plate).
   - It is still light and flexible, so handle it by the frame.
   - Visible change from v001: 9 slats per side instead of 12 (documented).
3. **Light poles:** 1.9 mm × about 22 mm, sturdier than v001's 1.5 mm but still the most slender features on the base. The luminaire heads may droop slightly. Print the site base with them upright as exported.
4. **Fits:**
   - Clearances are now 0.50 mm (pocket) and 0.40 mm (sockets), each with a lead-in.
   - If the body is still tight, check for elephant's foot or over-extrusion on the site-base pocket walls before changing anything.
   - If it is loose, a small dot of glue fixes it.
   - No geometry change should be made from slicer behaviour without a new version.
5. **Bonded thin spots kept as documented** (not free-standing): the door-bay pier 0.64 mm, the high-block chamfer wedge 0.58 mm, and curbs 0.64 mm. They may print slightly soft; they cannot break off.
6. **Degenerate triangles and surface skins:** body 12 and site base 39 zero-area triangles, plus near-coplanar skins on the site base thinner than one layer. If Bambu offers "repair", it only removes these; allowing it is harmless.

## A5. Recommended order for the physical prints

1. **Porte cochère + sun-shade on one plate** (0.12 mm): short, and it checks the two parts that failed or were fragile on the coupon. Then check that the canopy wing and tie are intact after support removal and that the sun-shade gaps are open.
2. **Site base** (0.16 mm): then plug the porte cochère into its sockets to confirm the 0.40 mm fit.
3. **Building body** (0.12 mm): then drop it into the pocket to confirm the 0.50 mm fit, and glue the sun-shade against the low-roof walls, flush with the roof.

---

# Part B — print v001 export (1:250, millimetres) and first-print guidance — superseded record

**Status (2026-09-23): EXPORTED AND VALIDATED — AWAITING APPROVAL.** No geometry was changed, and there is no v002. The next step is physical test printing, then the owner's decision.

| | |
| --- | --- |
| Source (approved print derivative) | `models\Building_II\print_derivatives\building_II_print_v001.blend`, SHA-256 `c4684e8d8345ff3105599b4ed2dbc67dbb47bc04bef0822bbae2eb8e36242875` (unchanged; opened read-only, never saved) |
| Frozen v023 | `models\Building_II\building_shell_v023.blend`, SHA-256 `7fe33f1e4dc906c75b54122203fec75ee9ef948be70897e46fcfd1b288235c91` — **identical before (17:25) and after this phase** |
| Export script | `scripts\3d_print\export_print_v001.py` (own binary-STL and 3MF writers; nothing is saved to the .blend) |
| Validation script | `scripts\3d_print\validate_export_v001.py` (reads every file back from disk with its own parsers and compares it with the approved mesh) |
| Validation output | `exports\Building_II\3d_print\validation\print_export_v001_validation.json`, `print_export_v001_written.json` |
| Units | **Millimetres.** Model metres × 4.0 = mm at 1:250 (1 m real = 4 mm). STL files have no unit field, so their numbers are mm; 3MF files declare `unit="millimeter"`. No other scaling or conversion is applied. |

## 1. Exported files — the four approved components

| Component | STL (`exports\Building_II\3d_print\stl\`) | 3MF (`exports\Building_II\3d_print\3mf\`) | Size X × Y × Z (mm) | Triangles | Vertices | Parts in file |
| --- | --- | --- | --- | --- | --- | --- |
| Building body | `building_II_v001_1-250_building_body.stl` | `building_II_v001_1-250_building_body.3mf` | **255.45 × 137.90 × 63.20** | 10,934 | 5,453 | 1 |
| Site base | `building_II_v001_1-250_site_base.stl` | `building_II_v001_1-250_site_base.3mf` | **330.00 × 230.00 × 35.97** | 86,616 | 43,310 | 1 |
| Drop-off canopy | `building_II_v001_1-250_dropoff_canopy.stl` | `building_II_v001_1-250_dropoff_canopy.3mf` | **79.99 × 28.52 × 24.33** | 580 | 264 | 1 |
| Sun-shade | `building_II_v001_1-250_sunshade.stl` | `building_II_v001_1-250_sunshade.3mf` | **186.20 × 98.12 × 1.22** | 7,410 | 3,155 | 1 |

**Component count: 4 production files per format, one component each.**

**How positions are stored:**
* **STL:** the model coordinates × 4, unmoved, so the four STLs keep their assembled relationship. Bambu Studio places them on the bed automatically when you import them.
* **3MF:** the same vertices and triangles. The only addition is a build-item **translation** that centres the part on a 340 × 320 bed with its lowest point at Z = 0. There is no rotation and no scaling.

### SHA-256

| File | SHA-256 | Bytes |
| --- | --- | --- |
| stl\building_II_v001_1-250_building_body.stl | `7d7d3fe1e464300f711b535091324757e3d74a22cabc48ba7afec7eb57ed76f7` | 546,784 |
| stl\building_II_v001_1-250_site_base.stl | `9b5ee0824be7edf88cbd26b2a0599b9e830bf40ff8e4280ab5e2847af2b988d0` | 4,330,884 |
| stl\building_II_v001_1-250_dropoff_canopy.stl | `a989f9a623e2778d8934c7dbf70fba031be0348492a7aa9ba0fcecb37c39a81e` | 29,084 |
| stl\building_II_v001_1-250_sunshade.stl | `60be2efbb032e3941416e3c369e9d47844fabb0bf91d4ec11c18f4ec0431dc59` | 370,584 |
| 3mf\building_II_v001_1-250_building_body.3mf | `006e7bd00fff97a7e289a69a2343bee8ca6f1502138385d7a1c51d755b2a0639` | 97,144 |
| 3mf\building_II_v001_1-250_site_base.3mf | `70165f4fcc187a9416852d78f46fcb2cd53170d7971d4edc8c54fb573fe41b5a` | 1,067,965 |
| 3mf\building_II_v001_1-250_dropoff_canopy.3mf | `c1fbf86f5190defcadfc2579e928522829e1abed4f146e55ca6008a9e8f91156` | 6,246 |
| 3mf\building_II_v001_1-250_sunshade.3mf | `ee961c9fd268bcd42fd89d556a045b18b35b80cb4120af395608a98b4e424dd2` | 68,542 |
| 3mf\building_II_v001_1-250_test_coupons_v001.3mf | `1b5d7cec56bdc12c25cc8d56f30a95f6128e2c2a8431a8cbf819d27deaca5612` | 82,551 |
| stl\test_coupons_v001\…_testcoupon_01_facade_storefront_railing.stl | `57b6ef5770c2a458d4d7e47fbfc7c4d49c4cb90ff790d840b2a251684efeff3a` | 15,984 |
| stl\test_coupons_v001\…_testcoupon_02_facade_curtainwall_west.stl | `46b737fe9d119093f2ef5661887b28c5f3e7a90cbd2798883c56a42bf38eb12e` | 22,684 |
| stl\test_coupons_v001\…_testcoupon_03_canopy_bay_column_X1.stl | `d775d234b9985fa5b051bd7b1d893b2fd08bbcd62e23d7f94a784ae893e39b02` | 14,284 |
| stl\test_coupons_v001\…_testcoupon_04_socket_bollards.stl | `1e7517237dc885618fd0635efdbbfbaff95f9ff34375fd44c77d7fe5f64093c6` | 12,184 |
| stl\test_coupons_v001\…_testcoupon_05_light_pole_1.stl | `0aec416c242dfa81f22a88666bbecdea9c03912df7dbb3c8485321005e2fd8bf` | 44,284 |
| stl\test_coupons_v001\…_testcoupon_06_sunshade_SE_corner.stl | `ab68564487afbb227e790043a83a969bb578d4c63a753dbef1c7f6a936a767cc` | 59,384 |
| stl\test_coupons_v001\…_testcoupon_07_pocket_body_corner_SE.stl | `d80ee097891dbc1d0b76c5ad617d9e4c192bb67ad836cd29e1077c96b8f72d4b` | 3,784 |
| stl\test_coupons_v001\…_testcoupon_08_pocket_site_corner_SE.stl | `a9878be50a376c811f795687bbe1ba4085359acee825746af07918d220ec3f8e` | 201,784 |

(`…` = `building_II_v001_1-250`)

## 2. Validation results (files read back from disk)

| Check | Body | Site base | Canopy | Sun-shade |
| --- | --- | --- | --- | --- |
| Units = mm, size matches the approved size (±0.06 mm) | ✔ | ✔ | ✔ | ✔ |
| No unexpected scale (every vertex = approved vertex × 4.0, within 0.00001 mm) | ✔ | ✔ | ✔ | ✔ |
| STL triangles identical to the 3MF triangles | ✔ | ✔ | ✔ | ✔ |
| 3MF: `unit="millimeter"`, 1 object, 1 build item, pure translation, sits at Z = 0 inside the bed | ✔ | ✔ | ✔ | ✔ |
| **3MF watertight** (0 open, 0 non-manifold, 0 duplicated edges), 1 component, normals outward | ✔ | ✔ | ✔ | ✔ |
| **STL watertight after welding by coordinates** | **✘ — see §6 item 1** | ✔ | ✔ | ✔ |
| STL facet normals agree with the triangle winding | ✔ | ✔ | ✔ | ✔ |
| Triangles = Blender's own triangulation of the approved mesh | ✔ identical | ✔ except 14 faces (see below) | ✔ identical | ✔ identical |
| Zero-area (degenerate) triangles | 55 | 75 | 0 | 0 |

**Site-base triangulation note.** STL and 3MF can only hold triangles. Blender's default split of 14 of the site base's 41,184 faces folds onto itself, producing 6 non-manifold edges. Only those 14 faces were re-split, with Blender's "beauty" method, which changed 122 of the 86,616 triangles.
- No vertex was added or moved.
- The faces involved are two flat pocket walls and a few terrain and walk faces east of the building.
- Those faces are out of plane by at most 0.22 mm printed, so that is the most the printed surface can differ from the approved one.
- Every other triangle in all four parts is exactly Blender's default triangulation of the approved mesh.

## 3. Test coupon set (printability test)

Each coupon is a box cut straight out of an approved part: no thickening, editing or simplification. That lets it test the real exported geometry at 1:250.

* **One plate for Bambu Studio:** `3mf\building_II_v001_1-250_test_coupons_v001.3mf`. It holds all 8 coupons laid out on a 340 × 320 bed (they use 227 × 30 mm), each already in its recommended orientation. The sun-shade coupon is flipped top-face-down by the build transform.
* **Individual files:** `stl\test_coupons_v001\` (model coordinates, so coupon pairs that fit together keep their real relationship).

| # | Coupon | Size (mm) | What it tests (measured feature thickness) | Orientation |
| --- | --- | --- | --- | --- |
| 01 | facade_storefront_railing | 28.0 × 8.2 × 26.2 | south storefront bay: **0.61 mm glazing recess**, **0.5 mm mullion ribs**, parapet, **0.8 mm railing fin** on the parapet | upright |
| 02 | facade_curtainwall_west | 10.7 × 16.0 × 24.4 | west curtain wall: **0.93 mm recess**, **0.5 mm curtain-wall ribs with 0.4 mm projection** (the most exaggerated class) | upright |
| 03 | canopy_bay_column_X1 | 13.5 × 28.5 × 24.3 | canopy bay: **1.2 mm column**, **0.8 mm purlins and glass plate**, 1.02 mm beams. Its column foot plugs into coupon 04. | upright (needs support under the glass, like the real canopy) |
| 04 | socket_bollards | 14.0 × 7.2 × 9.8 | site base at column X1: **socket with 0.2 mm clearance** (receives coupon 03) and **two 1.2 mm bollards** | upright |
| 05 | light_pole_1 | 8.0 × 8.8 × 26.6 | **1.5 mm light pole, 21 mm tall**, **0.8 mm luminaire head** (2.7 mm overhang), pole base, a few shrub domes | upright |
| 06 | sunshade_SE_corner | 37.0 × 28.9 × 1.2 | **0.84 mm louver bars (0.27 mm gaps)**, **0.8 mm frame**, 45° hip | **top face down** |
| 07 | pocket_body_corner_SE | 15.9 × 12.0 × 11.8 | building body SE corner below grade (foundation and podium). Fits into coupon 08. | upright |
| 08 | pocket_site_corner_SE | 30.0 × 30.0 × 12.6 | site base around the SE pocket corner: **pocket walls with 0.3 mm clearance** and pocket floor (receives coupon 07) | upright |

Measured on the exported coupon files:
- the 03 column sits in the 04 socket with **0.200 mm** side clearance;
- the 07 corner sits in the 08 pocket with **0.300 mm** side clearance;
- all 8 coupons are watertight single components.

**How to read the coupon print:**
- Ribs on 01/02: continuous and visible, and not merged with the recess?
- Railing fin on 01: intact?
- Louvers on 06: separate slats, or fused into a grooved plate? (Fused is expected and acceptable.)
- Bollards on 04 and the pole on 05: upright, not wavy, and the luminaire head not badly drooped?
- Fits: 03 drops into 04 by hand, and 07 drops into 08 without force and without visible slop?
- Recesses on 01/02: clearly legible?

## 4. Recommended orientation and supports per part

| Part | Orientation on the bed | Supports | Brim |
| --- | --- | --- | --- |
| **Building body** | Upright, foundation (flat underside) on the bed. It prints as imported. | **Paint supports only under the three door-side canopies** (main entry, door 100A, east). Use Tree (manual), build plate only, about 620 mm² in total. Don't enable automatic supports: the window heads and rib or cap undersides (≤ 1.2 mm) bridge on their own, and automatic supports would scar the recesses. | none (large flat footprint) |
| **Site base** | Upright, flat underside on the bed, long side (330 mm) along the bed's 340 mm X axis. It can't be rotated 90°. | None. Only the four luminaire heads (2.7 mm overhang at 21–24 mm) overhang; accept a slight droop, or check coupon 05 first. | none, or at most 3 mm (only 5 mm of bed is free on each side in X) |
| **Drop-off canopy** | Upright, standing on its three column feet | Tree (auto), threshold about 30°, support under the glass and beams from the build plate. Its V-shaped glass has no flat face, so no orientation avoids supports (upright and inverted need about the same). | **3–4 mm outer brim** (the column feet are only 1.2 × 1.7 mm) |
| **Sun-shade** | **Flip it top face down** ("Lay on face" and pick the roof-level top face). All top surfaces are coplanar by design. | **None** | **3–4 mm outer brim** (a thin 1.2 mm lattice 186 mm long) |

## 5. Suggested Bambu Lab H2S setup (Bambu Studio)

These settings come from general FDM practice for fine architectural models. They are a starting point to confirm with the coupon print, not a Bambu specification.

* **Printer and nozzle:** H2S with the standard **0.4 mm** hardened-steel nozzle for the first tests and for the site base. A 0.2 mm nozzle is only worth considering later, for the building body, canopy and sun-shade, and only if the coupon shows the 0.5 mm ribs or the louvers are unacceptable. It roughly doubles print time.
* **Filament:** one colour, matte PLA (for example Bambu PLA Matte in white or light grey). Matte hides layer lines and reads like an architectural model. Use the stock PLA profile, with no chamber heating.
* **Build plate:**
  - Textured PEI for the body, site base, canopy and coupons.
  - Smooth PEI (or Cool Plate / SuperTack) for the **sun-shade**, whose visible top face prints against the plate.
* **Layer height:**

  | Part | Layer | Profile | Notes |
  | --- | --- | --- | --- |
  | Coupons, building body, canopy, sun-shade | **0.12 mm** | "0.12mm Fine" | |
  | Site base | **0.16 mm** | "0.16mm Optimal" | 0.12 mm gives smoother terrain steps but a much longer print |

  Keep the first layer at 0.2 mm.
* **Walls:** **3 wall loops**, Arachne wall generator (the Bambu default), which handles the 0.5–0.84 mm features as one- or two-line walls. Keep the default minimum feature / minimum wall width settings, and don't enable "Only one wall on top surfaces". **Top shell 5 layers, bottom 4.**
* **Infill:**

  | Part | Infill |
  | --- | --- |
  | Building body | **10 % gyroid** (it is a large solid, 1,272 cm³ if fully solid) |
  | Site base | 10 % gyroid |
  | Canopy, sun-shade, coupons | 15 % (in practice almost all wall) |
* **Speed:** the Fine profile defaults are fine. Keep "Slow down for overhangs" on. Outer walls at about 60–100 mm/s help the ribs.
* **Support settings, where used:**
  - Type Tree (manual/painted) for the body and Tree (auto) for the canopy.
  - Build plate only.
  - Top Z distance 0.12–0.16 mm (one layer at 0.12).
  - 2 top interface layers.
  - Support-to-object XY distance 0.35 mm.
  - Turn "Remove small overhangs" on.
* **Fit-related:**
  - Leave elephant-foot compensation at the default 0.15 mm and X-Y hole/contour compensation at 0 for the first coupon print.
  - If 03→04 or 07→08 is too tight, adjust XY compensation in the slicer (for example −0.05 mm hole compensation) rather than the geometry.
* **Import:**
  - Load the 3MF files (preferred) or the STLs.
  - If you load several STLs at once and Bambu Studio asks to "load as a single object with multiple parts", answer **No**.
  - Don't use Auto-orient.
  - Bambu Studio shouldn't ask about units, because the sizes are plausible mm. If it offers to convert from inches or metres, answer **No**.

## 6. Expected problem areas in Bambu Studio / on the printer

1. **Building-body STL shows "non-manifold edges" (25 edges at 19 points).** In two places surfaces of the approved body touch along a line: 2 points where the terrace railing's end corners meet the parapet, and 17 on one east-facade opening (CUT_13_E) where vertical and horizontal ribs meet with identical front faces. The **3MF keeps shared vertex references, so it is watertight — use `building_body.3mf`**. STL can't store those references, so Bambu will offer to repair the STL; the repair only splits those points and is harmless. The geometry was **not** altered to hide this, as instructed; a permanent fix would be a v002 geometry change.
2. **Degenerate facets:** 55 zero-area triangles in the body and 75 in the site base (boolean by-products). Bambu may mention them; they carry no volume.
3. **0.5 mm mullion ribs** print as a single extrusion line. Expect them to be legible but soft. The curtain-wall ribs project only 0.4 mm, so check coupon 02.
4. **Sun-shade louvers:** the 0.27 mm gaps are below what a 0.4 mm nozzle can resolve, so they will probably fuse into a finely grooved plate. That is expected, and the proportions are kept as drawn.
5. **Light poles** (1.5 mm × 21 mm): risk of wobble or stringing near the top and a slight droop at the luminaire heads. Check coupon 05.
6. **Canopy:** tiny column feet (use a brim), and supports under the 0.8 mm glass plates and purlins must be removed carefully. Print coupon 03 first.
7. **Site base size:** 330 mm leaves 5 mm free on each side in X. If Bambu Studio reports it outside the printable area on the H2S, stop and tell me; do not scale it in the slicer.
8. **Fits:** the 0.3 mm pocket and 0.2 mm sockets can close up with elephant's foot or over-extrusion, which is why coupons 03/04 and 07/08 exist.
9. **Site-base surface skins:** the near-coplanar slivers (thinner than one layer) are ignored by the slicer; no action needed.

## 7. Recommended order for the first physical test prints

1. **Test coupon plate** (`3mf\building_II_v001_1-250_test_coupons_v001.3mf`, 0.4 mm nozzle, 0.12 mm layers). This is the short, cheap print that checks every minimum feature and both fits. Stop and review it before anything else.
2. **Building body** (`3mf\building_II_v001_1-250_building_body.3mf`): the key visual part, and the longest-standing print risk (ribs, recesses, door-canopy supports).
3. **Site base** (`3mf\building_II_v001_1-250_site_base.3mf`, 0.16 mm): the largest print. Then trial-fit the body in the pocket.
4. **Drop-off canopy + sun-shade** (can share one plate; flip the sun-shade top-face-down): quick parts, then glue the sun-shade and plug in the canopy.

## 8. Frozen-file and scope record

* v023 `7fe33f1e…5c91`: identical before and after the phase.
* v001 `c4684e8d…2875`: unchanged; only read.
* No geometry was changed, and no v002 was created.
* The three context-only parking-island trees were not added.
* The four-part strategy is kept.
* The export validation found one item needing an owner decision (§6 item 1: body STL touch points, solved by using the 3MF); nothing was changed for it.
