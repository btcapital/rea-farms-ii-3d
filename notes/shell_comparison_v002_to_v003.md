# Comparison note — building_shell_v002 → building_shell_v003

Date: 2026-09-21
Reason for v003: owner-requested verification of the drop-off canopy height only. A stronger documented source was found, so v003 was created. Full sourcing: `notes/model_control_v003.md`.

## Integrity checks

- v001 and v002 models, scripts, control documents, the v001→v002 comparison note and the v002 renders: SHA-256 checksums identical before and after the v003 build.
- `source_documents`: 360 files, none modified.
- Object-by-object comparison of the two saved models: **154 mesh objects identical** (same vertex count and bounds). **5 objects changed** and **12 objects added**, all in the drop-off canopy collection. Nothing else differs.
- `build_shell_v003.py` is `build_shell_v002.py` with 84 changed lines: the header, the version string, the `CANOPY` data block, the canopy build block, and the collection name.

## Source of the change

**Structural sheet S132, "Enlarged Canopy Plans", Section 01 (3/4" = 1'-0")** — `source_documents\00 PLANS\Approved Set\APPROVED-COS-001319.pdf`, PDF page 73; permit issue E 09/29/2025, county stamp COS-001319 1/30/2026; not reissued in Revision 5.

## Exactly what changed

| Object(s) | v002 | v003 | Basis |
| --- | --- | --- | --- |
| `Canopy_column_X1…X3` | 14" square, top 15.0 ft | 17" × 10 3/8" (W16X100), top **15'-1 1/2"** | **W** S132 |
| `Canopy_glass_north` | top 16.10 ft at XA rising to 18.18 ft; 3" thick; met the south sheet at XA | top 16.28 ft at its inner edge rising to **18.32 ft**; 1" thick; stops 0.364 ft from XA | steel **W** + glass offset 1.322 ft **M** (S132); thickness **W** (A700) |
| `Canopy_glass_south` | 16.10 → 16.93 ft | 16.28 → **17.07 ft** | same |
| `Canopy_beam_X1…X3_north/south` (6, new) | — | tapered W27X84: bottom 13'-0" at column; tips 16'-11 15/16" / 16'-4" north and 15'-8 15/16" / 15'-1" south; 10" wide | **W** S132 |
| `Canopy_purlin_*` (6, new) | — | HSS12X6X3/8, 0'-6" from tips, 5'-0 3/8" (north) and 5'-0 1/4" (south) o.c., full 65'-7 1/4" length | **W** S132; vertical sides **A** |
| Collection name | `04_DropOff_Canopy_PROVISIONAL` | `04_DropOff_Canopy` | — |

Net effect on the glass: about **+0.14 ft (1 3/4")** higher than v002. Plan size, column positions and slope are unchanged.

## Directly dimensioned / measured / assumed

- **Directly dimensioned (W):** all steel elevations, beam depths, column and purlin member sizes, purlin spacing, horizontal reach, slope, glass thickness.
- **Measured from vector drawings (M):** top of glass 1.322 ft above top of steel; glass stopping 0.364 ft short of grid XA (both from S132 linework).
- **Assumptions (A):** purlins drawn with vertical sides; columns and beams as plain boxes/wedges of the written overall sizes; fittings, gutter, plates and footings omitted.

## Conflicts / unresolved

- No conflict between S132 and A700: reach (16'-7 1/2" / 6'-7 1/2") and slope (1 1/2":12) agree.
- A330, A331, A700 and A320 give **no** canopy elevation — confirmed.
- S131's TOS 11'-8 1/2" and 11'-6 1/4" are the main entry door canopy, not the drop-off canopy; they match v002's door canopy.
- **Still unresolved:** the glass-above-steel offset is measured, not written (U-4a). V-1 (revisions 6–10 not in hand) remains open.
