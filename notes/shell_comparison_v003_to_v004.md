# Comparison note — building_shell_v003 → building_shell_v004

Date: 2026-09-21
v004 = first materials / facade-detailing pass on the frozen v003 geometry. Material sourcing and the flag list are in `notes/material_control_v004.md` (written before the build).

## 1. Integrity checks

- **Frozen files:** SHA-256 of all v001–v003 models, scripts, control documents, comparison notes and the v003 renders identical before and after the v004 build (0 changed).
- **`source_documents`:** 360 files, none modified.
- **Geometry, vertex by vertex:** every one of the 206 mesh objects in `building_shell_v003.blend` exists in `building_shell_v004.blend` with **identical vertex coordinates and face connectivity** (206 of 206; 0 changed, 0 missing). Nothing was moved, resized or re-cut.
- The script still asserts the 205'-0" × 105'-10" face-of-stud control box and the finish-face extents.
- **No surface-level build-up adjustment was needed or made** — the A003 build-ups were already in the v003 geometry.
- `build_shell_v004.py` was generated from `build_shell_v003.py` by text patch: DATA section and all geometry functions unchanged; one line in `parapets()` now stores the edge number and inward direction on each parapet object (used only to pick materials).

## 2. What v004 adds

1. **Materials, assigned per face** on the existing objects (24 materials; list in the control document).
2. **322 new overlay objects**, all in the new collection `11_Facade_Detail_v004`, all named `FD_…`:
   - storefront and curtain-wall perimeter frames, mullions, horizontals, 4" × 10" caps and G3 spandrel panels, laid out from the written bay widths and heights on A811 / A815 / A816;
   - the ACM-4 panel on the solid door bay inside CW3;
   - hollow-metal door leaves for doors 110B, 102, 104, 210B (surface-applied, no openings cut) and 001A / 001B (inside the existing yard-wall gaps).
   These sit inside the existing reveals or a fraction of an inch proud of an existing face. Deleting the collection returns the model to exactly v003 plus materials.
3. **Lighting:** neutral daylight — white sun plus a uniform pale sky, AgX view transform with no "look", 128 samples. Same five cameras.

## 3. Materials applied (documented)

Brick BRK-1 (procedural, sized to the documented utility module) · ACM-1 Bone White · ACM-2 Tri-Corn Black · ACM-3 (east canopy) · ACM-4 (main entry and door 100A canopies, CW3 door bay) · copings MTL-1 / MTL-2 / MTL-3 on parapet tops · brick caps BC-1/BC-2 on site walls · vision glass G1/G2 · spandrel glass G3 · Beachstone Gray frames · white TPO on roofs and the roof side of roof parapets · clear laminated canopy glass · GR-1 glass railing · sun-shade painted to match ACM-1.

## 4. Neutral placeholders (unresolved — not guessed)

`UNRES_canopy_steel_paint_COLOR_TBD` (A700 says "color TBD") · `UNRES_painted_CMU_COLOR_TBD` (A012 says "color TBD") · `UNRES_HM_door_paint` · `UNRES_terrace_paving` · `UNRES_terrace_parapet_inner`.

## 5. Assignments that required interpretation

| Item | Interpretation |
| --- | --- |
| All named colors | On-screen values are approximations of finish *names*; no color values exist on the drawings. |
| Brick | Running bond and 3/8" joint assumed; brick-insert (EW2) panels not differentiated. |
| Vision glass | Shown dark and reflective because no interior is modeled behind it. |
| CW3 door bay panel | A815 says "architectural metal panel"; ACM-4 chosen from the adjacent A300 tag. |
| 4" × 10" horizontal caps | Locations from A815/A811 leaders; 8" projection beyond the glass assumed. |
| Curtain-wall verticals | 2-sided structural silicone → drawn as a thin flush joint in the frame color. |
| SF6 bays | Drawn "EQ" on A811 → five equal bays. |
| Terrace closet roof | TPO assumed. |
| Low site walls | Brick placed on the street (south-west) side, painted-CMU placeholder on the other; A012 does not say which side faces out. |
| Generator enclosure | Brick outside, painted-CMU placeholder inside, MTL-1 coping (A302 tag). |
| HM door positions | From plan door tags, ±1 ft. |
| Coping | Applied as a material on the parapet top faces; no coping profile modeled (parapet heights are written as top-of-parapet). |

## 6. Geometry observation found while detailing — **not changed** (v003 is frozen)

**Door 100A inside its CW3 bay is mirrored by 3".** A815 draws CW3 from outside, so its left side is east: the 9" panel is on the **east** jamb and the 6" panel on the **west**. v002/v003 put 9" on the west and 6" on the east, so the door opening sits 3" too far east within its 9'-11 1/2" bay. The v004 overlay follows the as-built v003 opening so everything lines up. Recommend correcting in a future geometry revision **only with owner approval**.

## 7. Still open

V-1 (architectural revisions 6–10 not in hand) · U-4a (canopy glass-above-steel offset measured) · specifications not yet reviewed for finishes · ACM panel joint layout, brick inserts, coping and brick-cap profiles, railing base shoe, canopy fittings/gutter not modeled · flat ground, no site, landscaping or signage (excluded from this phase).
