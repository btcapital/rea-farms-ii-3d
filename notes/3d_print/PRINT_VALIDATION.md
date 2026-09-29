# Building II — print derivatives: geometry validation

* **Part C — v003 MULTICOLOR at 1:240 (2026-09-29): CURRENT — APPROVED FOR HANDOFF AND FROZEN.** The v002 geometry plus colour overlay parts (White / Black / Gray / Clear); validated, exported and slice-tested. The validation state is frozen with it: `manifests\3d_print\print_phase_v003_FROZEN_2026-09-29.sha256`.
* Part A — v002 at 1:240 (2026-09-25): the printed and approved single-colour package (Rob approved the physical print). **Frozen.**
* Part B — v001 at 1:250 (2026-09-23): superseded by v002 and kept unchanged below as the record.

---

# Part C — print derivative v003 (multicolor, 1:240)

| | |
| --- | --- |
| Validated file | `models\Building_II\print_derivatives\building_II_print_v003.blend`, SHA-256 `27737a83aee78fa464a9e3c75b518540909339b42845283857293232bb6352a7` |
| Built by | `scripts\3d_print\build_print_v003.py`. The input is a pristine copy of the archive audit copy (= v023). The build refuses to save unless every save gate passes. |
| Checked by | `scripts\3d_print\validate_print_v003.py` (read-only; v002 and v023 are *linked* read-only). Outputs: `validation\print_validation_v003.json`, `print_validation_v003_colour_mismatches.csv`, `print_validation_v003_samples.npz`. |
| G-code check | `scripts\3d_print\check_gcode_colours_v003.py` → `validation\print_gcode_colour_check_v003.json` |
| Previews | `scripts\3d_print\preview_print_v003.py` → `previews_v003\print_v003_01…10_*.png`. The expected-colour references are `reference_v023_*.png` (made by `reference_colours_v023.py`). Bambu's own renders are `bambu_v003_*.png`. |
| Method | Priority overlay: the exact v002 part plus colour parts inside it; a later part wins in Bambu Studio. See `PRINT_CONTROL.md` §30–31. |

## C1. Frozen files

* v023 `7fe33f1e…5c91`, v001 `c4684e8d…2875` and v002 `9aa5e3a4…a27c` are unchanged.
* In `manifests\3d_print\print_phase_v002.sha256`, all 32 model, export, script, validation and preview entries are OK.
* The 3 notes files in that list were updated for v003 on purpose; they are living documents.
* The archive audit copy is still identical to v023.

## C2. Parts (same four-part assembly; the colour parts are parts of the same objects, not pieces)

| Object | Part (priority order) | Filament | Triangles | Shells | Notes |
| --- | --- | --- | --- | --- | --- |
| Building | 1 body | 3 Gray | 10,556 | 1 | **Identical to v002** (vertices, faces, and the printed 3MF triangles) |
| | 2 white paneling + roofs | 1 White | 3,226 | 378 | 373 skin prisms + 2 door canopies + 3 doorbay panels |
| | 3 black paneling + copings | 2 Black | 710 | 75 | 74 skin prisms + the East door canopy |
| | 4 glazing + glass rails | 4 Clear | 916 | 42 | 39 recess-back slabs + rails |
| | 5 storefront / CW frames | 3 Gray | 3,708 | 309 | 308 frame pieces + the NW corner post |
| Drop-off canopy | 1 canopy (steel) | 3 Gray | 636 | 1 | Identical to v002 |
| | 2 canopy glass | 4 Clear | 24 | 2 | The two glass plates |
| Sun-shade | sun-shade | 1 White | 5,534 | 1 | Identical to v002 |
| Site base | site base | 3 Gray | 84,862 | 1 | Identical to v002 (pocket 0.50 mm and sockets 0.40 mm unchanged) |

* **Scale 1:240.**
* **Printed sizes are unchanged from v002:** building 266.1 × 143.6 × 65.8 mm, site base 317.7 × 189.6 × 37.5 mm.
* All parts fit the H2S (340 × 320 × 340 mm).

## C3. Mesh health

* Every part is closed: 0 open, 0 non-manifold and 0 flipped edges, with outward normals.
* Colour parts have **0 non-planar faces** (tolerance 1 mm real = 0.004 mm printed).
* The site base keeps its 461 non-planar n-gons from v002. It is exported with the exact printed v002 triangles.
* Colour parts are sets of closed shells, and shells may overlap. The winding number reaches up to 4 inside overlaps. Bambu fills a part's shells as their union (tested).

## C4. Colour parts lie inside their base part

* The check covers every vertex and every BEAUTY-triangle centroid, using the generalized winding number with a tolerance of 3 mm real (0.0125 mm printed).
* **0 points outside** for white, black, clear and canopy glass.
* Frames use a documented tolerance of 20 mm real (0.08 mm printed). The approved v002 body deviates from its own frame operands by up to about 1 cm on the north façade. Result: 0 outside.
* 14 skin pieces at parapet corners and recesses were intersected with a body copy, which removed only the part outside. No piece was dropped.

## C5. Colour correctness

**Model check:**

* 24,000 area-weighted samples cover 5,368.5 m² of visible body surface.
* At each sample, the **effective** colour (priority frames > clear > black > white > body, winding-number test 0.05 mm printed inside the surface) is compared with the **v023 finish** at that point:
  - clear where a glass pane is directly in front;
  - gray on a frame;
  - otherwise the nearest non-glass v023 face.

| | expected White | Black | Gray | Clear |
| --- | --- | --- | --- | --- |
| effective **White** | 3,055.3 m² | 1.3 | 29.8 | 0.5 |
| effective **Black** | 1.3 | 149.4 | 6.9 | 0 |
| effective **Gray** | 2.2 | 3.4 | 1,412.1 | 1.6 |
| effective **Clear** | 0 | 5.4 | 0.5 | 698.8 |

* **Agreement: 99.0 %.**
* Visible surface split: white 57.5 %, gray 26.4 %, clear 13.1 %, black 2.9 %.
* The largest mismatch cluster is 0.9 m² real (about 4 × 4 mm printed).
* Mismatches sit within about 0.1 m real (0.4 mm printed) of a finish boundary, which is mostly the oracle's 12 cm frame radius reaching onto the adjacent wall, or on the glass-rail feet in the terrace copings.
* **No whole panel or face is assigned to the wrong filament.**

**Sliced G-code check (what the printer will actually do):**

* Bambu CLI, H2S 0.4, 0.12 mm High Quality: 247,457 outer-wall segments on 290 layers.
* 14,196 of 14,485 façade wall samples fall within 0.35 mm of a printed outer wall. Bambu turned the object 90° on the plate.
* The filament printed there matches the model's intended colour for **98.4 %** of samples and the v023 finish for **97.4 %**.

## C6. Thickness of the colour parts (printed mm, inward ray per shell)

* White and black skins are 1.0 mm deep (median). The low percentiles are the mitre wedges at convex corners and parapet-corner trims, by design.
* Clear slabs are 1.2 mm; canopy glass is 1.0 mm.
* Frames are 0.50–0.70 mm (the v002 minimums).
* Anything thinner than one extrusion line (about 0.4 mm) is absorbed by the neighbouring colour at slicing, giving a boundary blur of 0.4 mm or less.

## C7. Visual check against the v023 finishes

* The renders `print_v003_03…06` (elevations), `08` (roof) and `10` (south-west) match `reference_v023_*` from the same cameras.
* This includes the black SE storefront panel, the black vertical strip, the white LobbyBlock and LowRoof bands, gray brick, clear glazing and gray frames.
* The earlier diagonal wedges (from a Blender boolean defect) are gone; see `PRINT_CONTROL.md` §31.

---

# Part A — print derivative v002 (1:240)

| | |
| --- | --- |
| Validated file | `models\Building_II\print_derivatives\building_II_print_v002.blend`, SHA-256 `9aa5e3a4574e758f7fc914d9e6df887482791585a673d8b542420e7f4369a27c` |
| Built by | `scripts\3d_print\build_print_v002.py` (input = pristine copy of the archive audit copy = v023; refuses to save unless all four parts are single watertight solids) |
| Checked by | `scripts\3d_print\validate_print_v002.py` (independent, read-only) → `exports\Building_II\3d_print\validation\print_validation_v002.json`, `print_validation_v002_thin_regions.csv`; build log `print_prep_v002_build_log.json` |
| Previews | `scripts\3d_print\preview_print_v002.py` → `exports\Building_II\3d_print\validation\previews_v002\print_v002_01…13_*.png` |
| Units / scale | real-world metres in the .blend; **1:240** at export: 1 m = 4.1667 mm (1 in = 20 ft) |

## A1. Frozen and previous versions

| File | Result |
| --- | --- |
| `building_shell_v023.blend` | `7fe33f1e…5c91`: **identical** before (09:22) and after the phase |
| `building_II_print_v001.blend` | `c4684e8d…2875`: **identical**, only read (for the comparison previews and the canopy joint measurement) |
| v001 exports (27 manifest entries: STL, 3MF, coupons, notes) | all verify against `print_phase_v001_export.sha256` |
| Archive audit copy | `7fe33f1e…5c91` (= v023): the input for v002 |

## A2. Parts, size, scale and H2S fit (component count = 4)

| Part | Printed size X × Y × Z (mm) | Real (m) | Triangles | Solid volume | Bed margin each side (X / Y) |
| --- | --- | --- | --- | --- | --- |
| Building body | **266.1 × 143.6 × 65.8** | 63.86 × 34.47 × 15.80 | 10,556 | 1,438 cm³ | 37.0 / 88.2 mm |
| Site base | **317.7 × 189.6 × 37.5** | 76.25 × 45.50 × 8.99 | 84,862 | 388 cm³ | **11.1** / 65.2 mm |
| Porte cochère (canopy) | **83.3 × 29.7 × 25.3** (on the bed standing on its south edge: 83.3 × 25.3 × 29.7) | 20.00 × 7.14 × 6.08 | 636 | 3.2 cm³ | fits easily |
| Sun-shade | **194.0 × 102.3 × 1.27** | 46.57 × 24.56 × 0.305 | 5,534 | 3.4 cm³ | fits easily |
| Assembled | **317.7 × 189.6 × 68.4** | 76.25 × 45.50 × 16.41 | | | |

All four parts use the same scale, 1:240. The largest part, the site base, keeps at least 11 mm clear on every side of the 340 × 320 bed.

## A3. Manifold, normals and components

| Check | Body | Site base | Porte cochère | Sun-shade |
| --- | --- | --- | --- | --- |
| Open / non-manifold / inconsistent-normal edges | 0 / 0 / 0 | 0 / 0 / 0 | 0 / 0 / 0 | 0 / 0 / 0 |
| Normals outward (positive volume) | yes | yes | yes | yes |
| Disconnected components (floating parts) | **1** | **1** | **1** | **1** |
| **Watertight** | **YES** | **YES** | **YES** | **YES** |

- **Floating geometry:** none. No boolean slivers had to be removed in v002.
- **Overlaps between parts:** none. The largest measured intersection is 0.0002 m³ real (about 0.004 mm³ printed), which is rounding noise at coplanar contact faces.

## A4. Fit clearances (measured on the finished parts)

| Interface | Design | Measured | Notes |
| --- | --- | --- | --- |
| Building body in the site-base pocket (side walls) | 0.50 mm | **0.500 mm** | The body rests on the pocket floor (−2.438 m). It has a **0.4 mm × 45° lead-in chamfer** round the bottom edge of the foundation, hidden inside the pocket. 48 grade-level ribs have their own 0.5 mm clearance boxes. |
| Porte-cochère columns in their 3 sockets (side walls) | 0.40 mm | **0.400 mm** | Each socket has a **0.4 mm lead-in flare** at the grade rim. Each column foot has a **0.3 mm chamfer**. The columns bottom out on the socket floor at the documented height. |
| Porte cochère to building | none (documented free-standing) | 0.33 mm gap | never touches the building |
| Sun-shade to building | butt-glue contact | 0.000 mm, no overlap | trimmed against the body |

**Assembled positions:** all four parts keep their exact v023 architectural coordinates. Only the clearances were cut into the site base; no visible building alignment was changed.

## A5. Minimum feature sizes as built (1:240)

| Feature class | Documented | Printed | Target |
| --- | --- | --- | --- |
| Mullion / frame relief ribs (bonded) | 0.019–0.064 m face | **0.70 mm** wide, **≥ 0.42 mm** proud of the glazing plane (caps 0.91 mm) | 0.65–0.70 mm ✔ |
| NW curtain-wall corner post | 0.12 m (0.50 mm) | **0.70 mm** (widened, flush with both facades) | ✔ |
| Glass railings (free-standing fins) | 30 mm glass | **1.00 mm** | 1.00 mm ✔ |
| Parapets | ≥ 0.305 m (1.27 mm) | unchanged, ≥ 1.27 mm | ✔ (one bonded 45° chamfer piece kept at its documented 0.68 mm) |
| Porte-cochère purlins / glass plates | 0.151 m / 25 mm | **1.00 mm / 1.00 mm** | 1.0–1.2 mm ✔ |
| Porte-cochère beams | 0.254 m | **1.20 mm** | 1.0–1.2 mm ✔ |
| Porte-cochère columns | 0.265 × 0.431 m | **1.40 × 1.80 mm** | ✔ |
| Porte-cochère valley tie (new) | not documented | 3.9 × 1.35 mm, full length | reinforcement ✔ |
| Sun-shade frame (edges, ends, outriggers, hips) | 0.152 m | **1.00 mm** wide × 1.27 mm deep | 1.00 mm ✔ |
| Sun-shade louvers | 0.211 m bars, 0.069 m gaps | **1.076 mm bars, 0.50 mm gaps** (9 per side) | ≥ 1.0 mm / 0.45–0.50 mm ✔ |
| Bollards (incl. light-bollard caps) | 0.152 m | **1.40 mm** | ≈ 1.4 mm ✔ |
| Light poles | 0.128 m shaft | **1.90 mm** shaft; base 2.60 mm; luminaire head 1.00 mm | 1.8–2.0 mm ✔ |
| Tree trunk | 0.049 m | **1.40 mm** | ✔ |
| Shrub forms | plan 0.05–1.38 m | ≥ 1.5 mm diameter, ≥ 1.0 mm high | ✔ |
| Generator-yard door leaves | 55 mm | **1.00 mm** | ✔ |
| Curbs (bonded relief) | 0.152 m | 0.64 mm (documented, bonded to walks) | bonded relief ✔ |
| Glazing recess depth (35 openings) | 0.15–0.91 m | **0.63–3.8 mm** (openings under door canopies read up to 8.8 mm because the canopy projection is counted) | ≥ 0.3 mm ✔ |

**Ray-cast thickness check** (every triangle, inward ray):

| Part | Minimum | 1st percentile | What sits below the targets |
| --- | --- | --- | --- |
| Body | 0.32 mm | 0.70 mm (the ribs) | Only three places, all bonded full-height pieces of the approved v023 massing, left as documented (not free-standing): (1) the 0.153 m pier between the north curtain wall (CW3) and the door bay, 0.64 mm; (2) the 0.14 m wedge where the high block's 45° corner meets the CW2 recess, 0.58 mm; (3) that chamfer's 0.32 mm corner tip. |
| Porte cochère | 0.35 mm | 0.70 mm | Only 10 tiny wedges (about 0.9 mm² printed in total) where the tapered beam tips meet the glass underside. Every member is ≥ 1.0 mm. |
| Sun-shade | 0.23 mm | 1.00 mm | Only the two mitred hip tips at the building corners (about 3.6 mm² printed). |
| Site base | slivers | 0.18 mm | Near-coplanar skins where bed pads and hardscape meet the interpolated terrain (0.014 % of the surface). They are thinner than a layer, so the slicer ignores them. |

## A6. Porte-cochère reinforcement (the coupon failure)

* **What failed:** the canopy's two glass wings are separated by an open 0.22 m valley in v023. **Above the column tops, the two wings shared no material at all:** the rear (south) wing hung only on the three column tops. Measured cross-section across the valley, above z = 4.62 m:

  | Version | Cross-section |
  | --- | --- |
  | v001 | **0.0 m²** |
  | v002 | **5.69 m²** (continuous tie, 20 m × 0.285 m) |

* **Checks:**
  - 25 vertical rays down through the valley all hit the tie at z = 4.905 m, 0.058 m below the glass plane.
  - Beams are 1.2 mm, purlins and glass 1.0 mm, columns 1.4 mm.
  - The part remains a single watertight component.
* **Print orientation:** standing on its south edge.
  - Support area falls from 2,578 mm² (upright) to **387 mm²**, all of it under the three columns.
  - No support touches either glass wing.
  - The glass faces print as near-vertical walls, so there is no 7° staircasing like on the v001 coupon.

## A7. Sun-shade

A scan across the louver field on the south, east and north sides measured:
- **every clear gap 0.500 mm** (min = max);
- **minimum bar 1.075 mm**.

The frame members are 1.00 mm. The part is watertight, one component, and needs no supports when printed top face down.

## A8. Revised crop

* **Crop:** X −9.0 → 67.25 m, Y −5.0 → 40.5 m (76.25 × 45.5 m real, 317.7 × 189.6 mm printed), against v001's 82.5 × 57.5 m.
* **Removed by the crop:**
  - 3 north parking islands (`Site_Parking_island_1–3`) and their 3 curbs (`DET_Curb_island_site_1–3`);
  - the far east part of the undetailed existing plaza (cut at x = 67.25);
  - the east end of the walk to the Building I plaza (cut at x = 67.25).
* **Kept in full:** all 339 plants, all 6 beds, every bollard and light pole, all utility-yard walls, and every walk, stair, landing and curb near the building.
* The three context-only parking-island trees stay excluded, as instructed.

---

# Part B — print derivative v001 (1:250) — superseded record

**Status (2026-09-23): GEOMETRY PREPARED AND VALIDATED — AWAITING OWNER APPROVAL. No STL or 3MF has been exported** (`exports\Building_II\3d_print\stl\` and `\3mf\` are empty).

| | |
| --- | --- |
| Validated file | `models\Building_II\print_derivatives\building_II_print_v001.blend` (prepared; SHA-256 `c4684e8d8345ff3105599b4ed2dbc67dbb47bc04bef0822bbae2eb8e36242875`) |
| Frozen baseline | `models\Building_II\building_shell_v023.blend` — SHA-256 `7fe33f1e4dc906c75b54122203fec75ee9ef948be70897e46fcfd1b288235c91` **before and after this phase (unchanged)** |
| Built by | `scripts\3d_print\build_print_v001.py` (runs only on the pristine audit copy; refuses to save if any part is not a single watertight solid) |
| Checked by | `scripts\3d_print\validate_print_v001.py` (independent; opens the prepared file and never saves) |
| Previews | `scripts\3d_print\preview_print_v001.py` → `exports\Building_II\3d_print\validation\previews\print_v001_01…11_*.png` (never saves) |
| Machine-readable results | `exports\Building_II\3d_print\validation\print_validation_v001.json`, `print_validation_v001_thin_regions.csv`, `print_prep_v001_build_log.json` |
| Units | Geometry is stored at **real-world size in metres**. The 1:250 scale is applied only at export: **1 m real = 4 mm printed** (export factor 4.0 when writing millimetres). |

## 1. Printed parts (component count = 4)

| Part | Printed size X × Y × Z (mm) | Real size (m) | Triangles | Solid volume printed | Fits H2S 340 × 320 × 340 with a 10 mm margin |
| --- | --- | --- | --- | --- | --- |
| `PRINT_building_body` | **255.4 × 137.9 × 63.2** | 63.86 × 34.47 × 15.80 | 10,934 | 1,272 cm³ (before infill) | yes |
| `PRINT_site_base` | **330.0 × 230.0 × 36.0** | 82.50 × 57.50 × 9.00 | 86,616 | 569 cm³ | yes (5 mm margin each side in X) |
| `PRINT_canopy_dropoff` | **80.0 × 28.5 × 24.3** | 20.00 × 7.13 × 6.08 | 580 | 2.3 cm³ | yes |
| `PRINT_sunshade` | **186.2 × 98.1 × 1.2** | 46.55 × 24.53 × 0.305 | 7,410 | 3.2 cm³ | yes |
| **Assembled model** | **330.0 × 230.0 × 65.6** | 82.50 × 57.50 × 16.41 | — | — | — |

The heights run from the flat underside to the highest point:
- **Body:** foundation underside −2.438 m to the top of the lobby parapet, +13.360 m.
- **Site base:** base underside −3.048 m to the light-pole luminaires, +5.95 m.
- **Assembled:** −3.048 m to +13.360 m.

## 2. Manifold, normals and components

| Check | Body | Site base | Canopy | Sun-shade |
| --- | --- | --- | --- | --- |
| Open (boundary) edges | 0 | 0 | 0 | 0 |
| Non-manifold edges (> 2 faces) | 0 | 0 | 0 | 0 |
| Wire edges / loose vertices | 0 | 0 | 0 | 0 |
| Edges with inconsistent normals | 0 | 0 | 0 | 0 |
| Signed volume positive (normals face outward) | yes | yes | yes | yes |
| Disconnected components | **1** | **1** | **1** | **1** |
| **Watertight** | **YES** | **YES** | **YES** | **YES** |

**Floating objects:** none. Every part is a single connected solid. The 200 floating objects found in the audit (193 plants, 2 canopy glass panes, 2 bed sheets, 2 area drains, north arrow) were each resolved:
- plants were replaced with forms seated on grade;
- the canopy glass was thickened down onto its purlins;
- the beds were rebuilt as bonded pads;
- the drains and north arrow were omitted (see PRINT_CONTROL.md §15).

One zero-volume boolean sliver (4 vertices, 14 × 63 mm real, at the northwest lawn pad edge) was deleted automatically and logged.

The body contains 55 zero-area triangles and the site base 100. These are degenerate by-products of the Manifold booleans, and they are topologically consistent. They add no volume and do not affect slicing.

## 3. Minimum thickness (ray cast inward from every triangle)

Each triangle was tested by casting a ray inward along its normal and measuring the material thickness to the far side.

| Part | Minimum measured | 1st percentile | Area thinner than 0.8 mm | What the thin readings are |
| --- | --- | --- | --- | --- |
| Body | 0.31 mm | 0.50 mm | 3.3 % of surface | Almost all are the **0.5 mm mullion/frame relief ribs** (by design; bonded to the wall behind). Also: v023 wall piers between adjacent openings, 0.56–0.61 mm, bonded full height; the documented 45° parapet chamfer (0.66 mm, and its 0.31 mm corner tip). No free-standing element is under 0.8 mm. |
| Site base | slivers | 0.25 mm | 0.011 % | Near-coplanar skins where bed pads or hardscape meet the interpolated terrain. They are below one layer height (about 0.34 mm² printed in total have no measurable thickness), so the slicer simply won't print them. Curbs are 0.61 mm relief bonded to walks and islands. |
| Canopy | 0.55 mm | 0.75 mm | 0.01 % | Six tiny faces at the beam tips (about 0.1 mm² each). |
| Sun-shade | 0.8 mm | 0.8 mm | 0.02 % | Everything is 0.8 mm or more, except the two mitred hip tips where the 45° hips meet the building corners (0.08 / 0.19 mm tips, about 1.4 mm² each). |

## 4. Design minimums as built (per feature class)

| Feature | Documented (real) | Printed as | Rule |
| --- | --- | --- | --- |
| Free-standing walls, parapets, railings, plates, bars | — | **≥ 0.80 mm** (0.200 m) | thicken only if thinner |
| Columns, bollards, tree trunk | 0.152–0.265 m | **1.20 mm** (0.300 m) | posts |
| Light-pole shafts (21 mm tall) | 0.128 m | **1.50 mm** (0.375 m) | tall slender posts |
| Mullion / frame relief ribs (bonded) | 0.019–0.064 m face | **0.50 mm** wide (0.125 m) | relief, not free-standing |
| Rib projection in front of the glazing plane | 0.019–0.052 m (caps 0.218 m) | **≥ 0.40 mm** (0.100 m); caps kept at 0.87 mm | relief |
| Glazing recess (facade face to former glass plane) | 0.15–0.91 m | **0.61–3.66 mm** (35 openings) | recess ≥ 0.3 mm |
| Planting-area pads | open sheets | **+0.30 mm** above grade | relief |
| Shrub forms | 0.05–1.38 m plan | **1.5–5.5 mm** diameter, ≥ 1.0 mm high | simplified solids |

Glazing recess depth per opening: 13 openings measure 0.61 mm, 3 measure 0.93 mm, 12 measure 1.13 mm, the CW2 opening measures 2.34 mm and the lobby curtain wall and recess measure 3.66 mm. The openings under the door canopies (CUT_02_N, CUT_04_N, CUT_10/11_E) read 3.8–8.4 mm only because the canopy projection sits above them.

## 5. Assembly fit (parts checked against each other in place)

| Pair / clearance | Result |
| --- | --- |
| Body inside the site-base pocket | pocket side-wall clearance **0.300 mm** all round (0.075 m real); body rests flat on the pocket floor (floor = body underside, −2.438 m) |
| Canopy columns in their three sockets | side clearance **0.200 mm** (0.050 m); columns bottom out on the socket floor at the documented height |
| Canopy to building (nearest point) | 0.317 mm gap — the canopy never touches the building (as documented) |
| Sun-shade to building | **0.000 mm contact** at the low-roof walls = butt-glue joint; overlap volume 0 |
| Overlap volumes between any two parts | ≤ 0.00024 m³ real (≈ 0.015 mm³ printed) — numerical noise from coplanar contact faces; effectively zero |

Assembly order: (1) drop the body into the site-base pocket, (2) insert the drop-off canopy columns into their sockets, (3) glue the sun-shade against the east end of the low-roof block, flush with the roof top. The canopy must go on after the body, because its glass sits directly over the main-entry canopy.

## 6. Support needs (intended print orientation, faces steeper than 45°)

| Part | Recommended orientation | Area needing support | Notes |
| --- | --- | --- | --- |
| Body | upright, foundation on the bed | 2,729 mm² | About 620 mm² is under the three door canopies. The rest is opening heads and rib/cap undersides at most about 1.2 mm deep, which bridge without support. Supports on the build plate only: under the door canopies. |
| Site base | upright, flat bottom on the bed | 17.5 mm² | only the four luminaire heads (2.7 mm overhang) |
| Canopy | upright on its columns | 2,289 mm² (inverted: 2,294 mm²) | tree supports under the glass/beam soffits; the V-shaped glass has no flat side, so no orientation avoids supports |
| Sun-shade | **top face down** on the bed | **0 mm²** | all tops are coplanar by design, so it needs no supports |

## 7. Preview images

`exports\Building_II\3d_print\validation\previews\`:

- `print_v001_01_assembly_northwest.png`
- `02_assembly_southeast`
- `03_assembly_plan`
- `04_north_entrance_closeup` (recesses, ribs, canopy, bollards)
- `05_sunshade_terrace_southeast`
- `06_exploded_parts`
- `07_site_base_only` (pocket and sockets visible)
- `08_building_body_only_northwest`
- `09_canopy_part`
- `10_sunshade_part`
- `11_west_utility_yard`

## 8. Frozen-file and scope checks

- v023: `7fe33f1e…5c91` before the phase (16:51) and after the phase. **Unchanged.**
- Pristine audit copy archived at `models\Building_II\print_derivatives\archive\building_II_print_v001_audit_copy.blend`, same hash as v023. It is the input for any rebuild of this pass.
- v001 now holds only the four print parts (collection `PRINT_v001`). The visualization, interior, lobby, context, cameras and lights were not carried into it.
- No STL/3MF exported. No other project file was modified, apart from the new files listed in the print-phase manifest.
