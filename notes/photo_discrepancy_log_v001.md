# Photo discrepancy log v001 — shell v001 vs. August 2026 construction photos

Date: 2026-09-18
Model compared: `models/building_shell_v001.blend` (renders `renders/building_shell_v001_*.png`)
Rule: the architectural drawings remain the source of truth. **No geometry was changed because of a photo.** Any change below needs the owner's explicit approval first.

## Photos used (all under `source_documents\Photos\`, read-only)

| Ref | File | View |
| --- | --- | --- |
| P1 | `8.29.26 Drone Photos\dji_fly_20260829_140134_0019_1788026871926_photo.JPG` (12288×8192) | North (front), drone, straight on |
| P2 | `8.29.26 Drone Photos\image.jpg` (512 px) | South (rear), drone |
| P3 | `8.29.26 Drone Photos\image (1).jpg` (512 px) | West, drone |
| P4 | `8.29.26 Drone Photos\image (4).jpg` (512 px) | Roof, straight down |
| P5 | `8.29.26 Drone Photos\image (8).jpg` (512 px) | North-west oblique, drone |
| P6 | `08.04.26\IMG_1427.jpeg` (4032×3024) | South-east corner, from the ground |

Not used as evidence: `pass1–pass5.jpg`, `test.jpg`, `Finished_Front_Render_No_Logo.png`, `NORTH_Render_Reference.jpg`, `NORTHEAST_Render_Reference.jpg`, `PC_Canopy_Reference.jpg` — these are edited or rendered images, not field conditions. Most drone images other than P1 are only 512 px wide, which limits confidence.

## Findings

| ID | Element type | Drawing condition (as modeled) | Observed field condition | Photo | Confidence | Assessment |
| --- | --- | --- | --- | --- | --- | --- |
| D-01 | Geometry (massing) | Tall west block 42'-0", lobby block 43'-10", two-level east wing with Level 2 set back behind an L-shaped terrace (A300/A301/A132) | Same arrangement and relative heights; lobby block reads slightly taller than the west block | P1, P2, P5 | High | **Consistent.** No action. |
| D-02 | Roof / parapet | Lower parapet (38'-9 1/2") on the short bay between the west block and the lobby block (A132 tag, A300) | A visible notch in the parapet line at that bay | P1 | High | **Consistent.** |
| D-03 | Roof / parapet | South-east corner: parapet 17'-6" on the J' and 11' faces, stepping up to 19'-6" on the 12' face (A132) | Corner mass parapet is clearly lower than the wall beyond the jog; black steel rail shoe installed on the low parapet, no glass yet | P6 | High | **Consistent.** Glass railing GR-1 is documented but not modeled. |
| D-04 | Opening location | South face: Level 1 four + three 10'-0" windows either side of a recess, then a 45'-0" storefront; Level 2 five units 25/25/15/25/25 ft (A112/A122/A301) | Same count, rhythm and relative sizes | P2 | Medium (low-res) | **Consistent.** |
| D-05 | Opening location | South-east: tall entrance storefront on the 11' face; on the 12' face a lower storefront, then a 10' and a 25' opening (A300 east elevation) | Same sequence seen around the corner; small canopy over the lower storefront | P6 | High | **Consistent.** |
| D-06 | Opening location | Glazed north-west corner — CW3 (north) and CW4 (west) meet at the corner, two storeys (A300/A301) | Two-storey glazed corner, scaffolded | P3, P5 | Medium | **Consistent.** |
| D-07 | Opening location (model simplification) | CW3 modeled as one plain opening 0–89.8 ft. Drawings show door 100A, an ACM-4 panel and a small door canopy inside its east end | Field shows that solid/boarded door bay with a small canopy at the east end of CW3 | P1 | High | Drawings and field agree with each other; **the model is simplified**. Candidate refinement — needs approval. |
| D-08 | Canopy | Drop-off canopy 65'-7 1/4" × 23'-3", butterfly glass roof on three columns on grid XA (A700); heights measured, not written | Steel frame erected in the same position and extent (from west of the lobby into the CW3 zone); glazing not installed. Frame top sits at about the Level 2 floor band | P1, P5 | Medium | **Consistent in plan.** Height cannot be verified from the photo; stays open item U-4. |
| D-09 | Other (not modeled) | Louvered sun-shade around Level 2 on the north, east and south of the east wing (A132 outline; A300/A301) | Steel outrigger frame for the sun-shade is erected | P1, P2, P6 | High | Documented and built, **omitted from v001 by scope**. Recommend adding next pass — needs approval. |
| D-10 | Canopy (not modeled) | Side/door canopies on A701/A702 | Small canopy over the east storefront; a second horizontal bracket/ledger band higher on the same wall | P6 | High (canopy) / Low (what the upper band is) | Omitted from v001 by scope. Upper band to be identified on A701/A330 before modeling. |
| D-11 | Site condition (not modeled) | Utility yard with transformer and generator screen walls west of the building (A012) | CMU screen walls under construction at the west side | P3, P5 | High | Omitted from v001 by scope. |
| D-12 | Material | BRK-1 dark brick on the west block and podium; ACM panels on Level 2 and the lobby block (A300 legend) | Most faces show grey sheathing/air barrier with white joint tape; dark brick is installed on parts of the west and north-east podium | P1, P3, P5, P6 | High that this is construction progress | **Not a discrepancy** — cladding incomplete. Re-check with later photos before finishes. |
| D-13 | Geometry | Lobby block X = 104.6 → 144.5 ft; Level 2 low roof X = 30.5 → 174.0 ft | On the straight-down photo the lobby roof scales to roughly 110 → 153 ft and the low roof to roughly 35 → 181 ft | P4 | Low | Differences are within what lens perspective does to raised roofs on a 512 px image. **No action.** A full-resolution nadir photo would allow a real check. |
| D-14 | Site condition | Model ground is flat at Average Grade −1'-9 3/4" | Ground is near floor level at the north entrance and lower toward the west utility yard | P1, P3 | Medium | Known model simplification (U-7), also shown on the drawings. Site work is outside the approved scope. |

## Result

- **No photo shows a condition that contradicts the modeled geometry.** Nothing in the model was changed.
- Items D-07, D-09, D-10 are things that both the drawings and the field show but v001 leaves out on purpose. They are listed for the owner's decision on the next pass.
- Better evidence would help: full-resolution versions of the 8.29.26 south, west and straight-down drone photos (the copies in the folder are 512 px).
