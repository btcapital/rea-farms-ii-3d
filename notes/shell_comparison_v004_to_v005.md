# Comparison note — building_shell_v004 → building_shell_v005

Date: 2026-09-21
v005 = targeted correction pass: (1) door 100A jamb correction, (2) specification review of exterior finishes. Finish sourcing: `notes/material_control_v005.md`.

## 1. Validation

| Check | Result |
| --- | --- |
| Frozen v001–v004 files (models, scripts, control documents, comparison notes, build reports, all 20 renders — 39 files) | SHA-256 identical before and after the v005 build: **0 changed** |
| `source_documents` | 360 files, **0 modified** |
| Objects in v004 vs v005 | 528 mesh objects in each; none added, none removed |
| Geometry identical (vertex coordinates + face connectivity) | **514 of 528** |
| Geometry changed | **14 objects — all listed in section 2, all at door 100A** |
| Podium mesh (`L1_Podium`) | 229 vertices in both; 221 identical; **exactly 8 vertices moved**, each by 0.25 ft (3") in −X (west): the four corners of the door opening at X 80.64 → 80.39 and X 89.35 → 89.10, at Y 104.75 / 105.511 and Z 0 / 9.969. No other vertex differs. |
| Control checks in script (205'-0" × 105'-10" face of stud; finish extents; top of parapet 43'-10") | pass |
| Cameras, lighting, render settings | unchanged from v004 |

`build_shell_v005.py` was generated from `build_shell_v004.py` by text patch: the door opening line, two new jamb constants, the three door-bay panel lines, the frame and terrace-paver materials, and source-note strings. Nothing else.

## 2. Part 1 — door 100A correction: exactly what changed

Source: **A815 (Rev 5, PDF p.14), CW3 elevation**, drawn from outside so its left is east. Bottom dimension string, left to right: **9"**, 1'-2 3/4", 6'-0", 1'-5 3/4", **6"** = 9'-11 1/2". So the 9" panel is on the **east** jamb and the 6" panel on the **west**. Cross-check: on the Rev 5 A300 north elevation the white jamb panel scales about 9" on the east side and about 6" on the west.

The door bay itself (X 79.89 → 89.85) did **not** move. Inside it:

| | v002–v004 | v005 |
| --- | --- | --- |
| West panel | 9" (79.89 → 80.64) | **6"** (79.89 → 80.39) |
| Door + sidelite opening | 80.64 → 89.35 | **80.39 → 89.10** (same 8'-8 1/2" width, 3" further west) |
| East panel | 6" (89.35 → 89.85) | **9"** (89.10 → 89.85) |

Objects changed (14):

| Object | Collection | Change |
| --- | --- | --- |
| `L1_Podium` | 01_Masses | door opening recut 3" west (8 vertices, see above) |
| `Opening_02_N_Door` | 03_Opening_panels | glass panel moved 3" west |
| `CUT_02_N` | zz_Cutters (hidden, not rendered) | boolean cutter moved 3" west |
| `FD_02_Door_sill`, `_head`, `_jambA`, `_jambB`, `_h00`, `_h01`, `_v00`, `_v01` (8) | 11_Facade_Detail_v004 | door frame, two horizontals and the two door/sidelite verticals follow the corrected opening (each 3" west). Sidelite order was already correct: 1'-5 3/4" west, 6'-0" doors, 1'-2 3/4" east. |
| `FD_CW3_doorbay_panel_west` | 11_Facade_Detail_v004 | 9" → 6" wide |
| `FD_CW3_doorbay_panel_east` | 11_Facade_Detail_v004 | 6" → 9" wide |
| `FD_CW3_doorbay_panel_head` | 11_Facade_Detail_v004 | moved 3" west with the opening |

Not changed: the CW3 main glazing and the glazing above the door bay, all other openings and mullions, the door 100A canopy (it is centred on the bay, which did not move), walls, parapets, canopies, railings, sun-shade, utility yard, site context.

Remaining measured value: the bay's position along the wall (79.89 → 89.85) is still **M** (±0.2 ft). A re-check on the A300 raster gave about 80.0 → 89.9, inside that tolerance, so it was left alone.

## 3. Part 2 — specification review: what changed in the model

Only two materials changed (308 frame objects share the first; one object carries the second):

| Material | Change | Basis |
| --- | --- | --- |
| Frames `FRAME_YKK_Beachstone_Gray` → `…_painted_fluoropolymer` | metallic 0.6 → 0, roughness 0.40 → 0.35; same color | Spec 084113 / 084413: "painted 3-coat fluoropolymer finish, match Architect's sample" |
| Terrace `UNRES_terrace_paving` → `UNRES-colour_terrace_pavers_24in_concrete_pedestal_set` | same neutral placeholder color, 24" joint grid added | Spec 071413 2.6: plaza-deck pavers 24" square × 2", pedestal set; color by Architect |

Source notes stored on several other materials now cite the specification. **No color value changed.**

Confirmed by the specification (no model change needed): Endicott utility brick with Holcim Ultra Dark mortar, **running bond**, concave tooled joints; Alucobond Plus, three-coat fluoropolymer, integral copings; Viracon VZE1-42 and V953 Medium Gray; 1" laminated tempered canopy glass; white TPO; Viva VIEW laminated clear glass railing with no top rail.

## 4. Conflicts flagged (not resolved silently)

1. **Sun-shade — significant.** Drawings (A702, S133): custom **steel**-framed, flat 1" × 10" A36 plate louvers, painted to match ACM-1. Specification 107113: manufactured **aluminum** airfoil-blade system by Construction Specialties, "no substitutions", "welding not acceptable". The model still follows the drawings.
2. **MTL-1 coping metal.** Spec body says galvanized steel (with a note to confirm all-aluminum); its table of contents says aluminum; the legend says only "metal coping cap".
3. **Railing metal finish.** Legend: powder coat white. Spec 057313: stainless steel finishes only.
4. **Storefront product name.** A811: "YES 45 TU". Spec 084113: "YES451 TU".
5. **TPO attachment (inside the drawings).** A132 note 1 and the spec: mechanically fastened; A132 plan labels: "fully adhered". No visual effect.

## 5. Unresolved materials after specification review

Still neutral placeholders: drop-off canopy steel paint (color TBD) · painted CMU (color and sheen) · hollow-metal door paint · terrace paver **color** and laying pattern · terrace-side parapet finish.
Still approximations of a finish name only: Manganese Ironspot, Bone White, Tri-Corn Black, Beachstone Gray, V953 Medium Gray, VZE1-42.
Not dimensioned anywhere: brick joint thickness, brick-insert pattern, ACM panel joint layout, 4 × 10 cap projection.
Open verification items: V-1 (architectural revisions 6–10 not in hand); U-4a (canopy glass height above steel is measured).

The specification defers nearly every color to "Architect's sample / as selected by Architect". The documents that would resolve them — approved finish submittals or the architect's color schedule — are not in the project folder.
