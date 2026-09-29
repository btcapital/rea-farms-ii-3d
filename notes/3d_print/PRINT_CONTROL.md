# Building II — 3D-print derivative control (v001 → v002 → v003 multicolor)

**Current status (2026-09-29): PRINT DERIVATIVE v003 = MULTICOLOR VERSION OF THE APPROVED v002 GEOMETRY AT 1:240 — BUILT, VALIDATED, EXPORTED (Bambu multi-part 3MF) AND SLICE-TESTED ON THE H2S PROFILE. AWAITING OWNER REVIEW BEFORE IT GOES TO AUSTIN.**

**Pass 5, v003 multicolor (§28–36):**
* **Controlling direction (owner, 2026-09-29), recorded verbatim:** "Rob approved the physical 1:250 Building II v001 print. The next print derivative is to reproduce the building's primary exterior material colors using white filament for white metal paneling, black filament for black metal paneling, gray filament for gray brick, and clear/translucent filament for exterior glazing/windows. v001 remains the frozen successful geometry/printability baseline."
* **Owner clarification (2026-09-29):** the printed and approved package was actually **v002 at 1:240**, so v003 is built on v002. v001 and v002 both remain frozen.
* **Permanent rule:** future print versions keep the four-filament colour mapping in §29. **They must not revert to a single-colour building unless the owner explicitly asks for it.**
* **Files:**
  - `models\Building_II\print_derivatives\building_II_print_v003.blend` (SHA-256 `27737a83…52a7`)
  - `exports\Building_II\3d_print\3mf\building_II_v003_1-240_*.3mf` (4 files)
* v023, v001 and v002 were not modified; hashes were verified before and after.

**Pass 4, v002 (§20–27):**

**Pass 4, v002 (§20–27):**
* Built from the physical v001 coupon print results and the owner's red-box crop.
* Files: `models\Building_II\print_derivatives\building_II_print_v002.blend` (SHA-256 `9aa5e3a4…a27c`) and `exports\Building_II\3d_print\3mf\building_II_v002_1-240_*.3mf`.
* v023 and v001 were not modified (hashes verified before and after).

*The history below is kept as it was written. Its "current status" lines refer to the state at the time of each pass.*

**Status as of 2026-09-23 (v001), superseded by Pass 4:** geometry preparation pass complete and validated; awaiting owner approval before STL/3MF export.
* **Pass 3 (2026-09-23, owner-approved): export and print-test.** The four approved parts were exported to STL and 3MF (mm, 1:250), along with an 8-piece test coupon set. Everything was validated, with no geometry change and no v002. See `notes\3d_print\PRINT_EXPORT.md`. **Awaiting approval after the physical test prints.**
* Pass 1 (§1–13, audit only) was approved by the owner with the decisions recorded in §14.
* Pass 2 (§14–19) prepared the print geometry inside `building_II_print_v001.blend`. Validation is in `notes\3d_print\PRINT_VALIDATION.md`.
* No STL or 3MF has been exported. v023 is unchanged (SHA-256 `7fe33f1e…5c91` before and after).

*§1–13 below are the original audit record and are kept unchanged. Where Pass 2 changed a detail of the audit plan, §14–19 say so.*

| | |
| --- | --- |
| Phase | 3D-print derivative, pass v001 = printability audit of an unmodified copy |
| Frozen source (READ-ONLY) | `models\Building_II\building_shell_v023.blend` |
| Source full path | `C:\Users\Brandon\OneDrive - Taylor Capital\Shared - Documents\Dormie Equity Partners, LP\11425 Golf Links Drive, LLC\Rea Farms II 3D\models\Building_II\building_shell_v023.blend` |
| Source SHA-256 | `7fe33f1e4dc906c75b54122203fec75ee9ef948be70897e46fcfd1b288235c91` (6,509,440 bytes) |
| Print derivative | `models\Building_II\print_derivatives\building_II_print_v001.blend` — byte-identical copy, same SHA-256 |
| Audit script | `scripts\3d_print\audit_print_v001.py` (opens the derivative in background Blender 5.2.2, measures, **never saves**) |
| Audit outputs | `exports\Building_II\3d_print\validation\print_audit_v001.json` (summary, extents, probes) and `print_audit_v001_objects.csv` (one row per object, 2,778 rows) |
| Phase manifest | `manifests\3d_print\print_phase_manifest_v001.json` + `print_phase_v001.sha256` |
| Target printer | Bambu Lab H2S, build volume **340 × 320 × 340 mm** ([Bambu Lab H2S tech specs](https://bambulab.com/nl-nl/h2s/tech-specs)). A 10 mm planning margin (330 × 310 × 330 mm usable) is used below as an assumption. |

---

## 1. Baseline confirmation

* `notes/building_II_status_2026-09-23.md` names **v023 as the CURRENT APPROVED BUILDING II MODEL** and records SHA-256 `7fe33f1e…5c91`. The file hashed today matches exactly.
* `notes/lobby_refinement_control_v023.md` is marked "APPROVED — CURRENT APPROVED BUILDING II MODEL v023 (lobby phase complete)".
* Freeze manifest `notes/freeze_manifest_2026-09-23_model_v023_viewer_v026.sha256` (443 entries) was checked from the project root: **423 files OK at their recorded paths**. The other **20 entries are the `.blend` models** (blender_test v001–v002, building_shell v001–v023). These have been moved from `models\` to `models\Building_II\`, and **all 20 are byte-identical at the new location**. So nothing frozen has changed; only the folder moved. The status note and the freeze manifest still quote the old `models/…` path. I have not edited either note, because they are frozen records. The print manifest records the new paths.
* No earlier 3D-print notes or decisions exist in the project.

**Conclusion:** v023 is the approved, frozen baseline. The derivative is an exact copy of it. The audit opened only the derivative, never saved it, and re-hashing after each run confirmed that both files are unchanged.

## 2. Model units and dimensions

* Scene unit system **Imperial, display unit feet, unit scale 1.0**. **Geometry is stored in metres** (Blender units): the build scripts convert with `FT = 0.3048`. This matters for export. An STL written "as is" is in metres. Any print scaling must start from **1 Blender unit = 1 m**.
* Origin: grid 1/K at Level 01, **Z 0 = FFE 660.30**. X runs east, Y runs north (the front faces north).
* Object inventory in the copy: 2,616 meshes, 69 lights, 37 cameras, 56 text objects. Only one modifier type is used (92 bevel modifiers, all on lobby FF&E). There are no particles, geometry nodes or collection instances.

| Extent set | Objects | Size X × Y × Z (m) | Notes |
| --- | --- | --- | --- |
| Building masses only (01_Masses) | 5 | 62.90 × 32.59 × 11.18 | podium Z −0.55 → 4.62, Level 2 blocks 4.62 → 9.75, terrace closet to 10.64 |
| Building exterior, everything attached (masses, parapets, glazing, mullions, canopies, sun-shade, railings, utility yard) | 491 | **71.73 × 41.14 × 13.91** | X −8.05 (transformer yard) → 63.68 (east canopy); Y −1.54 (SW low wall) → 39.60 (drop-off canopy); top = lobby parapet Z 13.36 |
| Building + modeled site (terrain, hardscape, beds, site detail, plants) | 931 | 101.19 × 69.49 × 16.41 | the terrain object sets this |
| Terrain only (INTERPOLATED) | 1 | 101.19 × 69.49 × 3.05 | closed slab; grade top −1.70 → −0.01 m; flat bottom −3.05 m |
| Above + parking context curbs/striping | 951 | 183.6 × 129.9 | striping reaches into the context parking |
| Everything incl. 14_Context (Building I mass, streets, horizon trees) | 1,308 | 824 × 819 | not printable, not intended |

## 3. Scale options and fit on the H2S (340 × 320 × 340 mm)

Physical size in mm = metres × 1000 ÷ scale. "Fit" also allows any rotation on the bed.

| Printed set | 1:200 | 1:250 | 1:300 |
| --- | --- | --- | --- |
| Building masses only | 314.5 × 163.0 × 56.0 — fits | 251.6 × 130.4 × 44.8 — fits | 209.7 × 108.6 × 37.3 — fits |
| **Complete building exterior** (with yard walls, canopies) | 358.7 × 205.7 × 69.6 — **does not fit at any rotation** → must be split | **286.9 × 164.6 × 55.7 — fits, with margin** | 239.1 × 137.1 × 46.4 — fits, with margin |
| Full modeled terrain + building | 506.0 × 347.5 × 82.0 — no (needs 2 × 2 tiles) | 404.8 × 278.0 × 65.6 — no (2 tiles) | 337.3 × 231.6 × 54.7 — fits raw, **not with the 10 mm margin** |
| **Documented-site window** (proposed crop X −8.5 → 71.5, Y −4 → 51 m = 80 × 55 m; contains every modeled walk (incl. the walk to the Building I plaza), stair, yard, curb, bed, plant, parking island, bollard and light pole; only the east end of the undetailed *existing* plaza between the buildings (to X 75.7) and the north arrow fall outside) | 400 × 275 — no (2 tiles) | **320 × 220 — fits, with margin** (330 × 230 with a 5 mm border) | 267 × 183 — fits |
| Building height above FFE (13.36 m) | 66.8 | 53.4 | 44.5 |
| Terrain grade relief (1.69 m) | 8.5 | 6.8 | 5.6 |

Reading: at **1:200** the building itself must be printed in two pieces and the site in 2–4 tiles. At **1:250** the whole building fits in one piece, and so does a site base cropped to the documented area. At **1:300** everything fits easily, but most facade detail falls below printable size (see §5).

## 4. Mesh health (non-manifold, open and zero-thickness geometry)

The audit measures each object's evaluated mesh (modifiers applied in memory only):

| Group | Objects | Watertight | Open edges | Non-manifold (>2 faces) | Zero-thickness parts | Flipped winding |
| --- | --- | --- | --- | --- | --- | --- |
| Exterior (masses, parapets, glazing, mullions, canopies, sun-shade, railings, yard, doors) | 491 | **491 / 491** | 0 | 0 | 0 | 0 |
| Terrain | 1 | 1 / 1 | 0 | 0 | 0 | 0 |
| Site hardscape / stairs / walls | 52 | 51 | 7 edges (Site_North_arrow only) | 0 | 1 (north arrow, flat) | 0 |
| Site beds / lawn (LAND_ beds) | 6 | **0** | 34 — all 6 are open sheets | 0 | 0 | 0 |
| Site detail (bollards, poles, curbs, drains, hardware, joints) | 41 | 38 | 192 (2 walk curbs, control-joint lines) | 0 | 1 (DET_Joint_concrete_control_joints, flat lines) | 0 |
| Parking striping / context curbs | 20 | 18 | 2,438 | 0 | 2 (DET_Striping_stalls, DET_Striping_hatch: flat paint) | 0 |
| Vegetation (LAND_ plants) | 340 | **1** | 314,616 | 0 | 101 objects (SEAS 63, COZA 27, OSOR 11: single-sided leaf cards) | 0 |
| Interior base / lobby / tenant / hollow shell | 1,269 | 1,266 | lobby plant leaves, tenant underlay | 0 | 3 | 0 |

Key points:
* No non-manifold (>2-face) edges or inverted shells anywhere. The building exterior is 491 separate closed solids.
* The exterior solids **overlap and touch one another** (glass sits in mass pockets, parapets sit on masses, mullions sit on glass). Each shell is valid, but a print needs them **boolean-unioned into one closed shell per printed part**. That is a geometry change for the next pass.
* **All open or zero-thickness geometry is in site dressing and planting:** 6 bed/lawn sheets, flat striping, joint lines, the north arrow, and leaf-card plants (71,247 separate leaf islands, 266k triangles). None of it can be printed as it stands.

## 5. Thin and fragile features (from the audit and probes)

Minimum thickness is measured along each part's own face normals, which is exact for boxes, plates and prisms. Values are real size, then printed mm.

| Feature | Real | 1:200 | 1:250 | 1:300 | Verdict at 1:250 |
| --- | --- | --- | --- | --- | --- |
| Masses (roof/walls as solids) | ≥ 1.02 m | ≥ 5.1 | ≥ 4.1 | ≥ 3.4 | fine |
| Parapet, thinnest (terrace edge) | 0.164 m | 0.82 | 0.66 | 0.55 | fragile, thicken to ≥ 0.8 mm or merge with the mass |
| Parapet, low roof / high block | 0.305–0.457 m | 1.5–2.3 | 1.2–1.8 | 1.0–1.5 | fine |
| Glazing recess depth (glass behind facade face), typical | 0.145–0.275 m | 0.7–1.4 | 0.6–1.1 | 0.5–0.9 | printable as recess |
| Glass panes | 0.015 m (spandrel 0.005) | 0.07 | 0.06 | 0.05 | not printable as panes, see §6 |
| Storefront mullion face | 0.051 m | 0.26 | 0.20 | 0.17 | below minimum |
| Curtain-wall vertical face line | 0.019 m | 0.10 | 0.08 | 0.06 | below minimum |
| Mullion caps (8 in × 4 in, 0.198 m proud of glass) | 0.203 m | 1.0 | 0.81 | 0.68 | borderline, OK as relief ribs |
| Drop-off canopy columns / beams | 0.254–0.265 m | 1.3 | 1.0–1.1 | 0.85–0.9 | fragile, thicken |
| Drop-off canopy purlins | 0.151 m | 0.76 | 0.60 | 0.50 | below minimum |
| Drop-off canopy glass (1 in laminated) | 0.025 m | 0.13 | 0.10 | 0.08 | below minimum |
| Door-side canopies (ACM) | 0.451–0.678 m | 2.3–3.4 | 1.8–2.7 | 1.5–2.3 | fine |
| Sun-shade outriggers / edges | 0.152 m | 0.76 | 0.61 | 0.51 | below minimum |
| Sun-shade louver blades | 0.025 m | 0.13 | 0.10 | 0.08 | below minimum |
| Glass railings (3 panels, 0.61 m high) | 0.030 m | 0.15 | 0.12 | 0.10 | below minimum |
| HM door leaves | 0.024 m | 0.12 | 0.10 | 0.08 | ignore (flush), or show as recess |
| Utility-yard walls | 0.387–0.532 m | 1.9–2.7 | 1.5–2.1 | 1.3–1.8 | fine |
| Bollards (0.945 m high) | 0.152 m | 0.76 | 0.61 | 0.51 | too fragile |
| Light poles (5.3 m high) | 0.128 m | 0.64 | 0.51 | 0.43 | too fragile (21 mm tall needle at 1:250) |
| Curbs | 0.152 m | 0.76 | 0.61 | 0.51 | OK only as relief in the base |
| Site stair tread / riser | 0.279 / 0.170 m | 1.4 / 0.85 | 1.1 / 0.68 | 0.9 / 0.57 | readable steps |
| Parking striping, control joints | 0 m (flat) | — | — | — | omit, or engrave |

Counts of exterior objects thinner than 0.8 mm at 1:250: all 311 mullion/frame pieces, 67/67 sun-shade pieces, 39/39 glazing panes, 6/6 doors, 3/3 railings, 2/2 canopy glass panes, 6/15 canopy steel members and 1/25 parapets.

## 6. Topic-by-topic findings

* **Mullions (311 objects, 11_Facade_Detail_v004):** all watertight, all below printable size individually. Only the 8-inch horizontal caps (42 objects) reach about 0.8 mm at 1:250. Recommendation: represent the curtain wall/storefront grid as **raised relief ribs at a printable minimum width**. This is a deliberate exaggeration and must be approved. Alternatives are printing caps only, or omitting mullions and showing the glass as a flat recessed plane.
* **Glazing (39 objects):** thin panes (15 mm, spandrels 4.6 mm) sit in pockets 0.145–0.275 m deep; the lobby curtain wall recess is 0.9 m. Recommendation: **drop the glass panes and keep the recess** as the glazing read (0.6–1.1 mm deep at 1:250). The glass plane can be filled flush as a separate colour (dark grey) if the owner wants multi-colour. Transparent glazing is not practical on FDM at this scale.
* **Drop-off canopy (17 objects):** the glass is modeled **0.112 m above the steel with no standoffs**, so it floats (see §7). Steel members are 0.15–0.27 m (0.6–1.1 mm at 1:250). Recommendation: print the canopy as a **separate part**, flat, with columns and beams thickened to ≥ 1.2 mm, purlins merged into the glass slab, and the glass as one ≥ 1.0 mm plate bonded to the steel. This is an approved-exaggeration item.
* **Door-side canopies (3):** fine as is (≥ 1.5 mm at every scale).
* **Roof:** the roofs are the flat tops of the solid masses plus 25 separate parapet solids. **No rooftop equipment or screens are modeled** in v023, and none will be invented. The sun-shade (67 objects, a horizontal frame at Z 9.45–9.75 m around the low roof) is the only roof-level feature; it is far below printable size as modeled. Recommendation: simplify it to a thickened perimeter frame with ≥ 0.8 mm outriggers and a few merged louver bars, or a single slotted plate. This is a simplification to approve.
* **Glass railings (3):** 30 mm glass. Options are a thickened 0.8 mm solid strip or omitting them.
* **Vegetation (340 LAND_ objects, 266k triangles, 71k leaf islands):** single-sided leaf-card plants, 193 of them not touching the ground (median gap 1.3 cm), 61 sunk more than 1 cm below it, and 101 containing zero-thickness cards. Plant sizes are 0.24–1.38 m in plan (1.0–5.5 mm at 1:250). The only tree trunk (SANJ) is 0.05 m. Recommendation: **replace, don't repair**. Each plant becomes a simple closed dome/blob with the same position and plan size (minimum 1.5–2 mm), and beds become shallow raised or recessed pads. The single tree becomes a lollipop with a ≥ 1.2 mm trunk. Positions and species counts stay traceable to LP-101 (v008); only the shape is simplified.
* **Site geometry:** the terrain is a clean closed slab and forms a good base. It is **IDW-interpolated** (v006/v007) and must still be labelled that way. Hardscape (walks, plaza, drop-off bands, stairs, landings, pads) is watertight and sits at documented spot grades. Beds/lawns are open sheets. Striping, joints and the north arrow are flat. Bollards and light poles are too fragile. The parking-context curbs/striping extend outside the site window. Recommendation: build the base from the terrain, crop it to the documented-site window, and keep hardscape as raised or recessed relief. Omit striping, joints, drains, hardware and the north arrow. Bollards and poles are optional: omit them, or print as thickened 1.2 mm posts (flagged).
* **Interior geometry (1,068 visible interior objects + 201 hidden hollow-shell objects):** 1,060 of the 1,068 lie inside the building envelope, and **the exterior masses are solid**, so none of it is visible from outside. It should be **excluded from the exterior print**. Interior items are mostly sub-millimetre at these scales (lobby chair posts 0.021 m, tenant partitions 0.125 m, rated walls 0.12–0.18 m).
* **Other non-print content to exclude:** 14_Context_v011 (Building I mass, streets, horizon trees; 888k triangles), 13_Presentation_v010 backdrops, zz_Cutters (boolean cutters), 106 cameras/lights and 56 text labels.

## 7. Floating objects (true mesh contact, 1 cm tolerance, exterior + site print set)

Grounded means connected, through actual mesh contact, to the terrain, the foundation skirt or the podium. **200 objects are not connected:**

| Objects | Count | Cause |
| --- | --- | --- |
| Canopy_glass_north / _south | 2 | glass modeled 0.112 m above the steel; no standoffs modeled |
| LAND_ plants | 193 | leaf-card clusters placed just above the bed/terrain surface |
| LAND_Planter_bed_at_CW2_bay, LAND_Lawn_northeast_bed | 2 | open decal sheets slightly above grade |
| DET_Area_drain_AD-208 / AD-209 | 2 | about 7 cm above the terrain directly below them |
| Site_North_arrow | 1 | presentation marker, 0.12 m above grade |

Every other exterior object (masses, parapets, glazing, mullions, canopy steel, sun-shade, railings, yard walls) is connected. Light poles, bollard lenses and door hardware register as connected through their bases, bollards or doors.

## 8. Recommended minimum printable feature sizes (Bambu H2S, 0.4 mm nozzle, PLA/PETG, 0.08–0.12 mm layers)

These are general FDM rules of thumb, not a Bambu specification. A **test coupon at the chosen scale** should confirm them before the full print (proposed for the next pass).

| Feature | Minimum (printed) | Preferred | Real size at 1:200 / 1:250 / 1:300 (preferred) |
| --- | --- | --- | --- |
| Free-standing wall / fin / parapet | 0.8 mm | 1.2 mm | 0.24 / 0.30 / 0.36 m |
| Column, post, pole | 1.2 mm | 1.5–2.0 mm | 0.30–0.40 / 0.38–0.50 / 0.45–0.60 m |
| Cantilevered plate (canopy, sun-shade) | 0.8 mm | 1.2 mm | 0.24 / 0.30 / 0.36 m |
| Raised relief rib (mullions) | 0.4 mm wide × 0.2 mm high | 0.6–0.8 wide × 0.3–0.4 high | 0.8 mm wide = 0.16 / 0.20 / 0.24 m |
| Recess / engraving (glazing, joints) | 0.5 mm wide × 0.3 mm deep | 0.8 × 0.5 mm | 0.8 mm = 0.16 / 0.20 / 0.24 m |
| Gap between features | 0.4 mm | 0.6 mm | — |
| Clearance for removable / plug-in parts | 0.2 mm per side | 0.3 mm per side | — |
| Plant / tree canopy blob | 1.5 mm | 2.0 mm+ | 0.4 / 0.5 / 0.6 m |
| Tree trunk | 1.2 mm | 1.5 mm | — |

A 0.2 mm nozzle roughly halves the wall/relief minimums (0.4–0.5 mm walls), but the print is slower and the parts are more fragile. That is optional and the owner's choice.

## 9. One piece or modular? (recommendation)

**Modular, at 1:250:**
1. **Site base**: terrain cropped to the documented-site window (80 × 55 m → 320 × 220 mm, plus a 5 mm border = 330 × 230 mm), hardscape relief, beds, planting. One print.
2. **Building body**: masses + parapets + glazing recesses + mullion relief + door canopies + utility-yard walls, boolean-unioned into one closed solid, printed upright. One print, 287 × 165 × 56 mm maximum.
3. **Delicate add-ons**, printed separately and flat, then glued: drop-off canopy, sun-shade frame, and optionally glass railings, light poles and bollards. They print better lying flat than as unsupported overhangs on the body.

Alternatives: **1:300 single plate** (whole site + building fits, but most facade detail is lost) or **1:200** (best detail, but the building splits into two parts and the site into 2–4 tiles with pins).

## 10. Removable roof or Level 2?

**Not recommended for this derivative.**
* The exterior masses are **solid**. A removable level would have to be rebuilt from the hidden hollow shell (BASE_Exterior: 0.27–0.40 m walls, 24 mm glass) plus the interior, so it would be a different model, not a cut.
* A natural cut plane exists at **Z 4.623 m** (top of L1_Podium = underside of the three Level 2 blocks; L2 slab 4.71–4.88 m). However, the **two-storey north curtain wall (8.8 m tall) and the lobby double-height volume cross it**, and so do the tall storefront/CW mullions.
* At 1:200–1:300, the interior is mostly below printable size (lobby furniture, stair guards, partitions, labels). Only slabs, the core and columns would read.
* If an interior study model is wanted later, it should be a **separate interior derivative** (for example Level 1 + removable Level 2 at 1:200, which fits the bed at 312 × 161 mm). Tenant concepts would go in as separate optional inserts. That requires its own approval.

## 11. Base / plinth strategy (recommendation)

* Use the existing terrain slab as the base: its flat bottom is at −3.05 m, 1.35 m (5.4 mm at 1:250) below the lowest grade. Crop it to the documented-site window and **keep the grade relief** (1.69 m = 6.8 mm at 1:250). The model and any label must keep stating that the terrain is **IDW-interpolated**.
* Flat bottom, vertical sides and a 5 mm border. Minimum 3 mm solid under the lowest grade point, which is already satisfied.
* Walks, plaza, drop-off bands, landings and pads: 0.3–0.5 mm relief or colour change. Stairs as real steps. Curbs as relief. Striping, joints, drains, hardware and the north arrow are omitted.
* Registration: the building sits in a **0.3 mm-per-side clearance pocket** following the foundation skirt footprint. The podium extends 0.55 m (2.2 mm) below FFE, which naturally keys it in. Canopy column feet get small sockets.
* **No text, logos or branding** on the plinth (standing owner instruction), unless the owner asks for it.
* At 1:200 the base becomes 2 tiles joined with 3 mm pins.

## 12. Decisions needed from the owner before any geometry change

1. **Scale:** 1:250 (recommended), 1:200, or 1:300.
2. **Site extent:** documented-site window crop (recommended), full interpolated terrain (tiles needed below 1:300), or building-only on a plain plinth.
3. **Modular split** as in §9 (recommended), or a single piece.
4. **Approved exaggerations:** mullions as relief ribs at printable minimum width; parapets, canopy steel and the sun-shade thickened to minimums; canopy glass as a ≥ 1 mm plate joined to the steel.
5. **Glazing:** recess only (recommended), or filled flush in a second colour.
6. **Vegetation:** replace with simplified solids at the same positions (recommended), or omit.
7. **Optional small items:** bollards, light poles, glass railings. Thicken or omit.
8. **Colour:** monochrome (recommended for a first print) or multi-colour (AMS).
9. **Removable roof/Level 2:** not in this derivative (recommended); a separate interior derivative later if wanted.

## 13. What changed / what stayed frozen

* **Created:** `models\Building_II\print_derivatives\building_II_print_v001.blend` (exact copy), `scripts\3d_print\audit_print_v001.py`, the two validation files, this note and the phase manifest.
* **Unchanged:** `building_shell_v023.blend` and every other frozen file (see §1). **The derivative's geometry is unchanged**: it has never been saved by Blender and its SHA-256 still equals v023.
* **Proposed next pass (after approval):** `building_II_print_v002.blend` with a new `PRINT_` collection tree (base / body / add-ons), built by a script from the approved decisions. It will include a boolean union per part, manifold validation (zero open and non-manifold edges, positive volume), a minimum-thickness check against §8 and a test coupon. STL/3MF export comes only after that validation is approved.
  *(Pass 2 note: the owner directed that the print work happen in `building_II_print_v001.blend` itself, so the prepared geometry is v001, not v002. See §15.)*

---

# Pass 2 — geometry preparation (2026-09-23)

## 14. Owner decisions (approved 2026-09-23)

| # | Decision |
| --- | --- |
| 1 | Scale **1:250** |
| 2 | **Cropped site base.** The documented crop keeps every modelled walk, stair, curb, bed and planting area and leaves out only the far, undetailed plaza extent. |
| 3 | Thicken fine details **only where FDM needs it**, keeping proportions as close as practical. Every exaggerated class is documented with its final printed thickness (§16). |
| 4 | Glazing = **recessed openings / facade relief** (never flush solid glass) |
| 5 | Plants replaced by **simplified printable forms at the documented positions** |
| 6 | Bollards, poles and railings **kept and thickened where practical**; any omission documented |
| 7 | **Single-colour** first prototype |
| + | v023 stays frozen; work only in the print derivative. The building and site base stay separate. The building is one body if reliable. Separate only parts that materially improve reliability or surface quality. No removable roof or Level 2. Interior excluded. Major form is not altered without approval. No STL/3MF yet. |

## 15. Method and versioning

* **Input:** the pristine `building_II_print_v001.blend` (byte-identical to v023). Before the build it was copied to `print_derivatives\archive\building_II_print_v001_audit_copy.blend` (hash verified = v023).
* **Build:** `scripts\3d_print\build_print_v001.py` (Blender 5.2.2, Manifold boolean solver).
  - The script checks that its input is the pristine copy.
  - It builds four parts from world-space copies of the approved v023 objects.
  - Every boolean input must be watertight, and every boolean must actually change the mesh, or the script stops without saving.
  - It deletes everything else from the derivative and saves v001 only if all four parts are single watertight solids.
  - Build time is about 12 s.
* **Rebuild:** to rebuild this pass, copy the archive audit copy back over v001 and run the script again.
* **Versioning:** v001 has **not** yet been approved as a geometry milestone. Once it is, it will never be overwritten, and any later revision becomes `building_II_print_v002.blend`.
* **Scale and units:** the geometry stays at real size in metres. Export (next pass) applies ×4.0 to write millimetres at 1:250.

## 16. Part structure, treatments and printed thickness by feature class

**Components: 4 printed parts.**
1. `PRINT_building_body`: one watertight body.
2. `PRINT_site_base`: one watertight base.
3. `PRINT_canopy_dropoff`: separate part.
4. `PRINT_sunshade`: separate part.

The body and site base are separate.

Why exactly two add-ons were separated:
* **Drop-off canopy.** It stands on its own three columns on the plaza and never touches the building, as documented. Its glass sits directly above the building's main-entry canopy. If it were fixed to the site base, the body could not be lowered into its pocket, and if printed on the body its V-shaped glass would need supports reaching 20 mm down. As a separate part it is fitted last, into 0.2 mm-clearance column sockets.
* **Sun-shade.** Printed on the body, its 14 mm cantilevered slatted frame at roof level would need support towers from the terrace, and removing them would destroy the slats. As a separate part it prints flat, top face down, with no supports. It butt-glues against the low-roof walls, flush with the roof top.
* Nothing else was separated: railings, bollards, poles, trees and door canopies all stay on the body or the base.

| Feature class | Objects | Documented (real) | Printed thickness / treatment |
| --- | --- | --- | --- |
| Masses (walls/roof), terrace closet, door-side canopies | 5 + 3 | ≥ 0.45 m | unchanged (≥ 1.8 mm) |
| Foundation below FFE | 1 | skirt −2.438 → −0.552 m | rebuilt from the L1_Podium bottom outline (1,945.6 m²; the skirt is 1,954.2 m², the difference being the lobby-entrance notch, which stays open for the plaza). Flat underside = body print face. |
| **Parapets** | 25 | 0.164–0.457 m | all ≥ **0.80 mm** already, except `Par_HighBlock_edge03`. That one is a 0.49 m, 45° chamfer bonded at both ends and is **kept at its documented 0.66 mm** (thickening pushed its ends past the neighbours). |
| **Glazing** (39 panes incl. 5 spandrels) | 39 | 5–15 mm glass at the back of 0.15–0.91 m pockets | **omitted as panes**. The approved v023 opening pockets remain as recesses **0.61–3.66 mm** deep. The three CW3/CW4 spandrels (18 mm behind the facade face) are glass too, so they became recess and the spandrel band now reads only through its horizontal caps. |
| **Mullions / frames / door frames** | 311 | face 0.019–0.064 m; projection in front of the glass 0.019–0.052 m | bonded relief ribs, **0.50 mm wide** (0.125 m), projecting **≥ 0.40 mm** (0.100 m) from the former glass plane and extended back into the wall. Proportion change: storefront mullions ×2.5 wide, curtain-wall face lines ×6.6. |
| Horizontal caps (8 × 4 in), within the 311 | 42 | 0.102 × 0.203 m, 0.218 m proud | height 0.102 → 0.125 m (0.50 mm); projection unchanged (0.87 mm) |
| **Glass railings** | 3 | 30 mm glass × 0.61 m | solid fin **0.80 mm** (0.200 m), centred on the glass line on the low parapet (×6.6 thicker) |
| **Drop-off canopy columns** | 3 | 0.265 × 0.431 m | **1.20 × 1.72 mm**, extended to the socket floor (−0.50 m) |
| Drop-off canopy beams | 6 | 0.254 m wide | unchanged (1.02 mm) |
| **Drop-off canopy purlins** | 6 | 0.151 m | **0.80 mm** |
| **Drop-off canopy glass** | 2 | 25 mm laminated, floating 0.112 m above steel | **0.80 mm plates**, documented top surface kept; the thickening fills the standoff gap onto the purlins (no longer floating) |
| **Sun-shade frame** (edges, ends, 24 outriggers, 2 hips) | 31 | 0.152 × 0.305 m | **0.80 mm** wide × 1.22 mm deep. Edges and ends keep their outer face. Hip ends are mitred to the building corners. |
| **Sun-shade louvers** | 36 | 25 mm blades inside a 0.211 × 0.183 m envelope | solid bars of the documented plan width **0.84 mm** (0.211 m). Top raised 0.061 m to the frame top (0.98 mm deep) so the part prints flat. The documented clear gap between bars is 0.27 mm, so the slats may fuse into a finely grooved plate at this scale (proportions kept, not re-spaced). |
| Utility-yard walls (moved to the site base) | 15 | 0.387–0.532 m | unchanged (≥ 1.55 mm); bottoms extended into the base |
| Generator-yard door leaves | 2 | 55 mm | **0.80 mm**, centred in the wall openings (recessed about 0.12 m from each face) and bonded to the jambs and lintel |
| **Bollards** (steel + light) incl. lenses | 10 + 4 | 0.152 m round × 0.95 m | **1.20 mm** posts, documented height kept |
| **Light poles** | 4 | 0.128 m shaft × 5.33 m | **1.50 mm** square shafts (21 mm tall); bases unchanged (1.83 mm); luminaire heads **0.80 mm** thick, top kept |
| Curbs (walk + island) | 5 | 0.152 m | kept at 0.61 mm as bonded relief (not free-standing); the two open walk-curb meshes were closed |
| Hardscape (walks, plaza, drop-off bands, stairs, landings, pads, slabs, islands, retained fill, base strip) | 50 | at documented tops | unchanged tops; bottoms extended into the base so nothing overhangs |
| Beds / planting areas | 6 | open sheets | closed pads raised **+0.30 mm** above the higher of the documented bed surface and local grade |

## 17. Omitted (documented, not silently deleted)

| Omitted | Count | Reason |
| --- | --- | --- |
| Glazing panes incl. spandrels | 39 | glazing represented as recesses (decision 4) |
| Hollow-metal door leaves flush with the wall faces (102, 104, 110B, 210B) | 4 | 0–0.024 m relief (≤ 0.1 mm), invisible and unprintable |
| Door pulls and levers | 5 | sub-0.2 mm hardware |
| Area drains AD-208, 209, 213, 214 | 4 | 1 ft flush grates (1.2 mm) with no relief; AD-208/209 were floating in v023 |
| Parking striping (stalls, hatch) | 2 | zero-thickness paint lines |
| Concrete control joints | 1 | zero-thickness lines |
| North arrow | 1 | presentation marker, floating |
| Context parking curbs | 18 | outside the crop window |
| Whole collections | — | **14_Context_v011** (Building I mass, streets, south sidewalk, 7 young street trees and the 3 existing parking-island trees that fall inside the crop, horizon), 13_Presentation backdrops, zz_Cutters, cameras/lights, text labels, **all interior / lobby / tenant geometry** (hidden inside solid masses) |

**Deliberately omitted and worth reviewing:** the 3 existing parking-island trees are context (approximate size, not part of the Building II landscape plan), so the parking islands print without trees. If you want them, they can be added as simplified trees in the next revision.

## 18. Vegetation, canopy, sun-shade, site base: summary

* **Vegetation:** the 340 LAND_ plants became **338 shrub domes + 1 tree**, one per documented plant, at its documented plan centre, sitting on the local grade/bed. Each dome's diameter is the documented plan size, 1.5–5.5 mm (91 enlarged to the 1.5 mm minimum). Heights are documented, minimum 1.0 mm (163 raised to that). The single tree (SANJ) is a 1.2 mm trunk with an onion canopy (45° underside, so it prints without support). Species counts are unchanged (CARE 69, SEAS 63, CATM 37, DAZA 28, JUNE 28, COZA 27, CORA 24, JADE 17, OSOR 11, RHCO 10, FOAR 8, JEWL 8, ILST 6, GATE 2, SANJ 1). No leaf detail is reproduced.
* **Site base:** 330.0 × 230.0 mm. That is the documented window of X −8.5 → 71.5 m and Y −4 → 51 m, plus a 1.25 m (5 mm) terrain border, so the crop box is X −9.75 → 72.75 and Y −5.25 → 52.25 m.
  - Flat underside at −3.048 m; the highest point is the light poles at 36.0 mm.
  - Grade relief kept (IDW-**interpolated** terrain). The base is 5.4 mm under the lowest grade and 12.2 mm at the highest.
  - Pocket for the body: footprint outline plus 0.3 mm, floor at −2.438 m, 2.44 mm of base left under it, with 0.3 mm clearance boxes around the 48 grade-level facade ribs.
  - Three canopy column sockets: 0.2 mm clearance, 2 mm deep.
* **Removable roof / Level 2:** none (as instructed).

## 19. What changed / what stayed frozen (Pass 2)

* **Changed:** `building_II_print_v001.blend` now contains only the four prepared parts in collection `PRINT_v001` (SHA-256 `c4684e8d…2875`).
* **Created:**
  - `print_derivatives\archive\building_II_print_v001_audit_copy.blend` (= v023)
  - `scripts\3d_print\build_print_v001.py`, `validate_print_v001.py`, `preview_print_v001.py`
  - `exports\Building_II\3d_print\validation\print_prep_v001_build_log.json`, `print_validation_v001.json`, `print_validation_v001_thin_regions.csv`, `previews\print_v001_01…11_*.png`
  - `notes\3d_print\PRINT_VALIDATION.md`
  - `manifests\3d_print\print_phase_manifest_v001_geometry_prep.json` + `print_phase_v001_geometry_prep.sha256`
* **Unchanged:** `building_shell_v023.blend` (re-hashed before and after), every other frozen project file, and `stl\` and `3mf\` (empty).
* **Superseded record:** `manifests\3d_print\print_phase_v001.sha256` from Pass 1 recorded v001 = v023. Its v001 line is now expected to fail; the audit state is preserved in the archive copy.
* **Next, only after approval:** export STL/3MF of the four parts at ×4.0 (mm), with a slicer-side check. Optionally print a small test coupon of the ribs, posts and sockets first.

---

# Pass 4 — print derivative v002 (2026-09-25)

## 20. Inputs and physical test evidence

* **Hashes before starting (09:22):** v023 `7fe33f1e…5c91` and v001 `c4684e8d…2875`, both unchanged. All 27 entries of `print_phase_v001_export.sha256` verified.
* **Physical v001 coupon print (owner photo), treated as manufacturing evidence:**
  1. The mating fit pieces (03/04 socket, 07/08 pocket) would not assemble reliably.
  2. Several small details printed but were visibly too thin or fragile.
  3. The light pole printed but is delicate.
  4. The sun-shade printed, but its members are very fine.
  5. The rear (south) part of the porte-cochère coupon snapped off while its supports were being removed. The photo shows the coupon with only a stub where that wing was, and 7°-sloped glass showing layer steps.
* **Bambu Studio screenshot with a red outline:** used as **design intent only**, not as dimensional evidence. The view is from the back of the bed (the plate label reads upside down), so north is at the bottom of the image and east is on the left. The red box:
  - keeps the south edge and the west utility yard;
  - stops about 5 m east of the building;
  - excludes the north parking islands, with its north edge just past the drop-off canopy.
* v002 was created as a pristine copy of `print_derivatives\archive\building_II_print_v001_audit_copy.blend` (= v023) and built by `scripts\3d_print\build_print_v002.py` (v001 method plus the changes below).

## 21. Revised crop (model space)

| | v001 | **v002** |
| --- | --- | --- |
| Crop X (m) | −9.75 → 72.75 | **−9.00 → 67.25** (west: 0.95 m beyond the transformer-yard walls; east: 0.57 m beyond the east door walks) |
| Crop Y (m) | −5.25 → 52.25 | **−5.00 → 40.50** (north: 0.9 m beyond the drop-off canopy tip at 39.6 m, above the parking islands at 44.6 m) |
| Real extent | 82.5 × 57.5 m (4,744 m²) | **76.25 × 45.5 m (3,469 m², −27 %)** |

**Kept:**
- the building;
- the porte cochère, drop-off bands, plaza and entry walks;
- all walks and stairs east, west and south, and the curbs along the walks;
- all 6 planting beds and all 339 simplified plants;
- the 10 bollards and 4 light poles;
- the utility and transformer yard;
- the south planting strip and tree;
- the interpolated grade.

**Omitted because of the crop:**
- 3 parking islands (`Site_Parking_island_1–3`) and their curbs (`DET_Curb_island_site_1–3`);
- the east end of the undetailed existing plaza between the buildings (was cut at 72.75, now at 67.25);
- the east end of the walk to the Building I plaza (now cut at 67.25).

The three context-only parking-island trees stay excluded. The building was **not** moved.

## 22. Uniform scale

* **The limit:** the red-box crop keeps the full east–west length, because the utility yard on the west and the east door walks bracket the building. So the site base's long side (76.25 m) governs the scale. The north trim does not.
* **Result:**
  - With at least 10 mm margin on each side of the 340 mm bed axis, the largest uniform scale is 1:238.
  - The standard **1:240 (1 in = 20 ft)** gives 317.7 mm, leaving **11.1 mm each side in X and 65 mm each side in Y**.
  - Rotating the base on the bed does not help: the axis-aligned placement is optimal for this aspect ratio.
* **The same 1:240 applies to all four parts.** Every socket, pocket, clearance and minimum was regenerated for it.

| | v001 (1:250) | **v002 (1:240)** | Change |
| --- | --- | --- | --- |
| Building body (mm) | 255.4 × 137.9 × 63.2 | **266.1 × 143.6 × 65.8** | **+4.17 % linear** (+8.5 % footprint, +13 % volume) |
| Site base (mm) | 330.0 × 230.0 × 36.0 | **317.7 × 189.6 × 37.5** | −3.7 % X, −17.6 % Y, **−20.6 % area** |
| Porte cochère (mm) | 80.0 × 28.5 × 24.3 | 83.3 × 29.7 × 25.3 | |
| Sun-shade (mm) | 186.2 × 98.1 × 1.2 | 194.0 × 102.3 × 1.27 | |
| Assembled (mm) | 330.0 × 230.0 × 65.6 | 317.7 × 189.6 × 68.4 | |

**If a substantially larger building is wanted:** the east–west span would have to shrink, for example by trimming the west utility/transformer yard or the east door walks, or the site base would have to print in two tiles. Either is a design decision for the owner and is not done here.

## 23. Coupon-derived minimums (1:240) — every intentional exaggeration

| Class | Documented | v001 printed | **v002 printed** |
| --- | --- | --- | --- |
| Mullion/frame relief ribs (bonded) | 0.019–0.064 m | 0.50 mm | **0.70 mm** wide (0.168 m, ×2.6–8.8), ≥ 0.42 mm proud of the glazing plane |
| NW curtain-wall corner post | 0.12 m | 0.50 mm | **0.70 mm** (flush with both facades); the adjacent west-wall end rib is trimmed to the facade plane so nothing sticks out past the corner |
| Glass railings | 30 mm | 0.8 mm | **1.00 mm** (0.24 m, ×7.9) |
| Parapets | ≥ 0.305 m | ≥ 0.8 mm | unchanged (≥ 1.27 mm); the bonded 45° chamfer piece stays at its documented 0.164 m (0.68 mm) |
| Porte-cochère glass plates | 25 mm | 0.8 mm | **1.00 mm** (top surface kept) |
| Porte-cochère purlins | 0.151 m | 0.8 mm | **1.00 mm** |
| Porte-cochère beams | 0.254 m | 1.02 mm | **1.20 mm** |
| Porte-cochère columns | 0.265 × 0.431 m | 1.2 × 1.7 mm | **1.40 × 1.80 mm** + 0.3 mm foot chamfer |
| Porte-cochère valley tie | — | — | **new**, §25 |
| Sun-shade frame | 0.152 m | 0.8 mm | **1.00 mm** |
| Sun-shade louvers | 12 × 0.211 m per side | 0.84 mm, 0.27 mm gaps | **9 × 1.076 mm per side, 0.50 mm gaps**, §26 |
| Bollards | 0.152 m | 1.2 mm | **1.40 mm** |
| Light-pole shafts | 0.128 m | 1.5 mm | **1.90 mm** |
| Light-pole bases | 0.457 m | 1.83 mm | **2.60 mm** (widened so the base stays wider than the shaft) |
| Luminaire heads | 0.122 m | 0.8 mm | **1.00 mm** (top kept) |
| Tree trunk | 0.049 m | 1.2 mm | **1.40 mm** |
| Yard door leaves | 55 mm | 0.8 mm | **1.00 mm** |
| Shrubs | 0.05–1.38 m | ≥ 1.5 / 1.0 mm | ≥ 1.5 mm diameter / ≥ 1.0 mm high (87 enlarged, 159 raised) |
| Planting pads | open sheets | +0.3 mm | +0.3 mm |

**Not exaggerated (the larger scale is enough, or they are bonded):**
- masses, door canopies (≥ 1.88 mm) and utility-yard walls (≥ 1.61 mm);
- curbs (0.64 mm, bonded relief);
- glazing recesses (≥ 0.63 mm);
- two bonded full-height pieces of v023 massing: the pier between CW3 and the door bay (0.64 mm) and the wedge at the high-block chamfer corner (0.58 mm).

**Glazing:** still recessed openings, with no panes. Even at 1:240 a 15 mm pane would be 0.06 mm.

## 24. Fit tolerances (owner direction after the coupon fits failed)

| Interface | v001 | **v002** |
| --- | --- | --- |
| Building body ↔ site-base pocket | 0.30 mm | **0.50 mm** per side, plus a **0.4 mm × 45° lead-in chamfer** round the bottom edge of the foundation (hidden in the pocket; also absorbs elephant's foot) |
| Grade-level facade ribs ↔ base | 0.30 mm | **0.50 mm** clearance boxes (48) |
| Porte-cochère columns ↔ sockets | 0.20 mm | **0.40 mm** per side, plus a **0.4 mm lead-in flare** at each socket rim and a **0.3 mm chamfer** on each column foot |

- **Pocket rim:** there is no chamfer there, because the rim follows the sloping interpolated grade all round the building. The body-side chamfer provides the lead-in instead.
- **Final positions** are unchanged: the body sits on the pocket floor, and the columns bottom out on the socket floor at the documented height.

## 25. Porte-cochère (canopy) — failure analysis and treatment

* **Vulnerable geometry:**
  - In v023 the canopy is a butterfly roof. Two glass wings meet at a 0.22 m open valley over the column line.
  - Above the column tops, the south ("rear") wing and the north wing share **no material**: each wing hangs on its three beam cantilevers, and they meet only at the column tops.
  - The coupon had one column, so the rear wing hung on a single 1.06 mm beam root. Pulling the supports from under the 7°-sloped glass bent it off.
* **Reinforcement (print-specific, documented):**
  1. **Valley tie**:
     - Location: x 23.615–43.613 m, y 34.068–35.008 m, z 4.581–4.905 m (printed about 83 × 3.9 × 1.35 mm).
     - It spans between the two innermost purlins, under the valley, along the full canopy.
     - It sits 0.058 m (0.24 mm) below the glass plane, so from above it reads only as a gutter inside the existing valley gap.
     - Across the valley, the section joining the wings goes from **0 m² (v001) to 5.69 m²**.
  2. Beams thickened to **1.2 mm**; purlins and glass plates to **1.0 mm**; columns to **1.4 × 1.8 mm**.
  3. No other form change; the visible roof profile is preserved.
* **Orientation and supports:** print the canopy **standing on its south edge**. The 3MF is already placed this way: rotated +90° about X, real north pointing up.
  - Both glass wings and every beam become near-vertical walls, so there are no sloped-glass layer steps.
  - The south wing prints first from the bed; the tie and north wing grow up from it.
  - **Support is needed only under the three horizontal columns** (387 mm², against 2,578 mm² upright). The supports touch only the sturdy 1.4 mm columns and never either wing, so removing them puts no bending force on the roof.
  - Use a 4–5 mm brim: the bed contact is the 1 mm south glass edge plus three beam ends.

## 26. Sun-shade

- **The constraint:** at 1:240 the documented 12 louvers per side sit at a 1.16 mm pitch. A 1.0 mm bar plus a 0.45–0.50 mm gap needs about 1.5 mm, so no local adjustment can resolve the gaps.
- **What changed:**
  - Each side's louvers are **redistributed evenly inside the same documented band** (first and last louver edges unchanged): **9 bars of 1.076 mm with exact 0.50 mm gaps**, 1.02 mm deep.
  - Bars run from the documented underside to the frame top.
  - Frame members are 1.0 mm.
- **What stayed the same:** the footprint, the mounting against the low-roof walls, and the frame layout (edges, 24 outriggers, 2 hips).
- **How it prints:** top face down with no supports. Scanned gaps are 0.500 mm on all three sides, and the minimum bar is 1.075 mm.
- **Visual difference:** 9 instead of 12 slats per side. This is the only change to the sun-shade's appearance, made for printability.

## 27. What changed / what stayed frozen (Pass 4)

* **Created:**
  - `models\Building_II\print_derivatives\building_II_print_v002.blend`
  - `scripts\3d_print\build_print_v002.py`, `validate_print_v002.py`, `preview_print_v002.py`, `export_print_v002.py`, `validate_export_v002.py`
  - in `exports\Building_II\3d_print\validation\`: `print_prep_v002_build_log.json`, `print_validation_v002.json`, `print_validation_v002_thin_regions.csv`, `print_export_v002_written.json`, `print_export_v002_validation.json`, and `previews_v002\` (13 images)
  - `exports\Building_II\3d_print\3mf\building_II_v002_1-240_{building_body,site_base,dropoff_canopy,sunshade}.3mf`
  - `manifests\3d_print\print_phase_manifest_v002.json` + `.sha256`
* **Unchanged:**
  - v023 (hashed before and after);
  - v001 and its archive audit copy;
  - all v001 exports and coupons;
  - all other project files.
* **No new coupon set:** the v002 changes directly address every coupon finding, and no new unresolved printability risk was found.

---

# Pass 5 — print derivative v003: MULTICOLOR (2026-09-29)

## 28. Direction and baseline

* **Owner direction (verbatim):** "Rob approved the physical 1:250 Building II v001 print. The next print derivative is to reproduce the building's primary exterior material colors using white filament for white metal paneling, black filament for black metal paneling, gray filament for gray brick, and clear/translucent filament for exterior glazing/windows. v001 remains the frozen successful geometry/printability baseline."
* **Owner clarification (same day):** the package actually printed and approved was **v002 at 1:240** (the direction's "v001 1:250" wording refers to it). v003 therefore uses the **v002 geometry and scale unchanged**. Every v002 improvement is kept: the crop, 1:240, the fits, the porte-cochère reinforcement, the sun-shade, and the minimums.
* **Frozen:**
  - v023 `7fe33f1e…5c91`
  - v001 `c4684e8d…2875`
  - v002 `9aa5e3a4…a27c`
  - All 35 entries in `print_phase_v002.sha256` were OK at the start of the phase.
  - At the end, all 32 model, export, script, validation and preview entries are still OK. The 3 notes files (`PRINT_CONTROL/VALIDATION/EXPORT.md`) were updated for v003 on purpose; they are living documents.
* **Permanent rule:** every later print version keeps the §29 mapping. **It must not revert to a single-colour building unless the owner explicitly requests it.**

## 29. Controlling filament mapping (owner-approved; do not change without the owner)

| AMS slot | Filament | Finishes (v023 materials) |
| --- | --- | --- |
| **1** | **White** | White metal paneling: ACM-1 / ACM-4 Alucobond Bone White, MTL-2 coping. **Roofs** (white TPO) and **terrace tops** (UNRES pavers) — owner 2026-09-29. Sun-shade (paint to match ACM-1). |
| **2** | **Black** | Black metal paneling: ACM-2 / ACM-3 Alucobond Tri-Corn Black, MTL-1 / MTL-3 copings. |
| **3** | **Gray** | Gray brick BRK-1 and brick caps. **Storefront / curtain-wall frames** (YKK Beachstone Gray) — owner 2026-09-29. **Drop-off canopy steel** (colour TBD in the drawings → gray) — owner 2026-09-29. Interior core. Site base. |
| **4** | **Clear / translucent** | Exterior glazing: vision and spandrel glass, glass railings, drop-off canopy glass. |

* No façade finish was guessed. Every face takes its colour from its v023 material, using the rule in `colour_of_material()` in `build_print_v003.py`.
* The three open cases (frames, roofs/terrace, canopy steel) were decided by the owner before the build.

## 30. How the colours are built (priority overlay)

* **The building body stays the exact v002 part.** It is gray (slot 3) and is vertex- and triangle-identical to v002.
* Colour parts lie **inside** it:
  - **WHITE / BLACK:** 1.0 mm skins (0.240 m real) behind every exterior white/black face of the masses and parapets. There are 373 white and 74 black prisms.
    - Each skin is mitred on the bisector at convex edges to a different finish, so the neighbouring face keeps its own colour up to the edge.
    - Undersides are skipped. So are shared internal walls, which are checked on a 7-point sample and confirmed on a 28-point grid.
    - Depth is limited to the body thickness behind the face.
    - The white and black door canopies and the CW3 doorbay panels are included whole.
  - **CLEAR:** a 1.2 mm slab (0.288 m) behind each of the 39 glazing panes, at the back of its recess. Each slab is intersected with a copy of the body so it cannot cross a neighbouring pocket. The glass rails are included whole.
  - **FRAMES (gray):** all 309 storefront and curtain-wall frame pieces and the NW corner post.
* **Part order is colour priority:** body < white < black < clear < frames. In Bambu Studio a later part of an object clips the earlier parts where they overlap. This was verified with the H2S CLI (§33): coplanar 1 mm skins print at full volume in their own filament and are removed from the body.
* **Each colour part is a join of closed convex shells, not a 3D union.** Bambu fills overlapping or touching shells of one part as their union. Verified: two half-overlapping 10 mm cubes print exactly the filament of one 15 × 10 × 10 mm box.
* **Drop-off canopy:** the exact v002 canopy is gray (steel), with a clear part made of its two glass plates.
* **Sun-shade:** white. **Site base:** gray. Both are unchanged v002 parts.
* **Result:** the four-part assembly is unchanged, and no new detachable pieces were added.

## 31. Why not a boolean partition (lessons, keep)

* The first v003 build cut the body into four disjoint parts with Blender's Manifold boolean. The renders showed **diagonal wedges** in the colour regions, for example half of the black SE storefront panel.
* **Root cause:** Blender 5.2's Manifold boolean sometimes returns **non-planar n-gons** that merge triangles from different planes (seen up to 4.4 m out of plane). The triangulation of such a face cuts a wedge.
* It happens even with triangulated or planar inputs, with unique materials, and through Geometry Nodes. The Exact solver failed differently: open or non-manifold results on many touching prisms.
* **Rule:**
  - Never partition an approved print part with a 3D boolean for colour.
  - Use overlay parts plus slicer priority.
  - Check every colour part for non-planar faces (0 allowed).
  - Use winding-number containment, not ray parity. Ray parity miscounts on internal interface planes.

## 32. Validation summary (details: `PRINT_VALIDATION.md` Part C)

* The four v002 parts are identical to v002 (vertex- and face-identical, loaded read-only).
* The 3MF base parts are triangle-identical to the printed v002 3MF files.
* Every part is closed, with 0 open, 0 non-manifold and 0 flipped edges. Colour parts have 0 non-planar faces.
* All colour parts lie inside their base part, checked by vertices plus face centroids with the winding number.
* **Colour correctness (24,000 area-weighted surface samples):** the effective colour agrees with the v023 finish on **99.0 %** of the visible surface.
  - Visible surface split: white 57.5 %, gray 26.4 %, clear 13.1 %, black 2.9 %.
  - The remaining 1 % is at finish boundaries (within about 0.4 mm printed) and on the glass-rail feet.
  - No panel or face is assigned to the wrong filament.
* **Sliced G-code check:** Bambu's actual outer-wall filament at 14,196 façade points matches the intended colour on **98.4 %** of points, and the v023 finish on 97.4 %.

## 33. Bambu Studio compatibility (H2S)

* The 3MF files are generic 3MF with `Metadata/model_settings.config`, giving **one object with one filament per part**.
* The CLI crashes on a Bambu-tagged 3MF without full project settings, so the Bambu application tag is omitted.
* **Slice test (Bambu Studio 02.08.02.61 CLI):**
  - System machine `Bambu Lab H2S 0.4 nozzle` and process `0.12mm High Quality @BBL H2S`.
  - Filaments: slot 1 PLA Matte White, 2 PLA Matte Black, 3 PLA Matte Gray, 4 PLA Translucent. The filament profiles were flattened with only the colour overridden.
  - **All four files sliced successfully.**
  - Building: all four filaments used, 598 filament changes, about 35.0 h and 487 g. The single-colour v002 building is about 27.6 h and 461 g.
* **Bambu may rotate the building 90° on the plate on load.** The CLI did this. It is harmless.
* **Single-part files (sun-shade, site base) must be checked in Bambu before slicing.** The CLI reports single-filament jobs as filament 1, so confirm the site base object shows **Gray (slot 3)**.

## 34. Print implications and risks

* **Time and waste:** the building needs about 600 filament changes on the single-nozzle H2S (AMS). That is about +7.4 h (+27 %) and about +26 g of purge compared with single colour. Black and clear appear on few layers, but white and gray alternate on almost every layer.
* **Clear filament:** translucent PLA reads as frosted light-blue, not transparent glass. The glazing is a 1.2 mm slab at the back of a recess, so it shows as tinted recessed windows. A clear inner-wall pattern is expected.
* **Thin colour features:**
  - Skins are 1.0 mm (clear 1.2 mm) deep, but mitres taper to 0 at convex corners.
  - Features under about 0.4 mm are absorbed by the neighbouring colour. This gives a fuzzy boundary of up to one line width (0.4 mm) at colour edges.
  - The frames are 0.50–0.70 mm (v002 minimums), printed gray over clear and white.
* **Prepare-view flicker:** in Bambu's Prepare tab, the coplanar surfaces of overlapping parts show z-fighting stripes. That is cosmetic. **Judge colours in the Preview tab after slicing.**
* **Supports and orientation are unchanged from v002:** building upright, canopy on its south edge, sun-shade top down. Support removal on the porte-cochère is as documented in §25.
* **Keep one print profile for all colours.** All four filaments are PLA, so there are no adhesion or temperature conflicts.

## 35. What changed / what stayed frozen (Pass 5)

* **Created:**
  - `models\Building_II\print_derivatives\building_II_print_v003.blend`
  - Scripts in `scripts\3d_print\`:
    - `build_print_v003.py`, `validate_print_v003.py`, `preview_print_v003.py`, `reference_colours_v023.py`
    - `export_print_v003.py`, `validate_export_v003.py`, `check_gcode_colours_v003.py`
    - `bambu_3mf_v003.py`
  - Files in `exports\Building_II\3d_print\validation\`:
    - `print_prep_v003_build_log.json`, `print_validation_v003.json` and its samples/mismatch files
    - `print_export_v003_written.json`, `print_export_v003_validation.json`, `print_gcode_colour_check_v003.json`
    - `previews_v003\`
    - The CLI's sliced check projects are **not** kept in the project. They go to the system temp folder, are about 450 MB, and are not printable.
  - `exports\Building_II\3d_print\3mf\building_II_v003_1-240_{multicolor_building,dropoff_canopy,sunshade,site_base}.3mf`
  - `manifests\3d_print\print_phase_manifest_v003.json` + `.sha256`
* **Unchanged:**
  - v023, v001, v002 and the archive audit copy (hashed);
  - all v001/v002 exports and coupons;
  - the visualization master;
  - all other project files.
* **Geometry change vs v002:** none. The v002 parts are identical; v003 only adds colour overlay parts inside them.

## 36. Before it goes to Austin (owner checklist)

1. Review the renders in `exports\Building_II\3d_print\validation\previews_v003\`:
   - `print_v003_*`: our colour renders.
   - `reference_v023_*`: the same views coloured from the v023 finishes.
   - `bambu_v003_*`: Bambu's own part/filament renders.
2. In Bambu Studio:
   - Load White / Black / Gray / Clear into AMS slots 1–4.
   - Open `building_II_v003_1-240_multicolor_building.3mf` and confirm the 5 parts show filaments 3/1/2/4/3.
   - Slice, then check the Preview tab.
3. Print order suggestion:
   - Print the sun-shade and canopy first (short jobs). They check the clear filament and the white.
   - Then print the building (about 35 h), then the site base (gray).
