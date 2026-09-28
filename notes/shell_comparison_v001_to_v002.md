# Comparison note — building_shell_v001 → building_shell_v002

Date: 2026-09-18
v001 files were not opened for writing; checksums of `models/building_shell_v001.blend`, `scripts/build_shell_v001.py` and `notes/model_control_v001.md` were identical before and after the v002 build. `source_documents` was not changed.

Full sourcing is in `notes/model_control_v002.md`. Codes: **W** written on a sheet · **M** measured from exact-scale vector drawings or elevation raster · **A** assumption.

## 1. What did not change

Origin, axes, units, datum table, grid table, face-of-stud control lines, Level 1 and Level 2 footprints, roof zones, all parapet heights, drop-off canopy, site context, cameras and neutral clay look. The 205'-0" × 105'-10" control box is still asserted by the script.

## 2. What changed

| # | Change | Basis |
| --- | --- | --- |
| 1 | Exterior faces moved out from face of stud by the documented build-up: brick 9 1/8", brick insert 7 1/8", metal panel 4". Overall finish size is now 206.35 × 106.93 ft. | **W** (A003) — locations from EW tags, confirmed **M** |
| 2 | Parapet thickness 1.0 ft → 1.5 / 1.13 / 1.0 / 1.0 ft by zone | **M** (A132) |
| 3 | Level 1 storefront sill/head 3.09/13.77 → 3'-0" / 13'-11 5/8" | **W** (A811) |
| 4 | Level 2 storefront sill/head 19.81/28.77 → **19'-0"** / 28'-11 1/4" (v001 sill was hidden behind the terrace parapet in the elevations) | **W** (A811) |
| 5 | Curtain walls to 28'-10 7/8", starting at finish floor; CW2 made one continuous opening; CW1 split at the written canopy band; CW5 and CW6 heads 14'-0"; SF2 head 10'-0" with its door | **W** (A815, A816, A811) |
| 6 | Storefront widths set to written frame widths; SF5A is now a full-height terrace door | **W** (A811, A122) |
| 7 | Door bay added inside the big north curtain wall (CW3): solid bay, door opening, canopy band | sizes **W** (A815); position **M** |
| 8 | Louvered sun-shade added: frame, bay beams, corner hips, louvers | plan **W** (A702); top of steel 32'-0" **W** (S133); depth **W** (A340); louver tilt/centring/corner bays **A** |
| 9 | Three door/side canopies added (main entry, door 100A, east) | plan sizes and slopes **W** (A701); heights **W** (A815/A811) except east canopy top **A** |
| 10 | Glass railings added on the three 17'-6" parapet runs, to 19'-6" | **M** (A300/A301); thickness/position **A** |
| 11 | Level 2 terrace closet added | **M** (A122, A301) |
| 12 | Utility yard screen walls added: generator enclosure 14'-0", transformer walls 3'-4", low walls 2'-8" | heights **W** (A012); plan positions **M** (A112); door head **A** |
| 13 | Glazed north-west corner: CW3 and CW4 now meet with no corner post | **W/M** (A815 widths, A300/A301) |
| 14 | Front and rear views widened slightly so the utility yard is in frame | — |

## 3. Directly dimensioned (W)

Wall build-ups (A003) · all storefront and curtain-wall sills, heads and frame widths (A811, A815, A816) · CW3 door-bay sizes and canopy band · sun-shade plan, bay spacing, top of steel and beam depth (A702, S133, A340) · louver size, count, spacing and angle (A702) · canopy plan sizes and slopes (A701) · main-entry and door-100A canopy heights (A815) · utility yard wall heights and door widths (A012).

## 4. Measured from vector drawings or elevation raster (M)

Parapet thicknesses · where each wall type applies (tags + linework) · CW3 door-bay position · opening centres not covered by a plan string · glass railing extents and top · terrace closet plan and height · utility yard wall positions and thicknesses · transformer enclosure height (from elevation alignment) · sun-shade south-arm start at the closet face · **drop-off canopy heights (still provisional)**.

## 5. Still assumptions (A)

Glass plane 2" inside face of stud · louver tilt direction, centring and open corner bays · east canopy top (11'-6") and its projection datum · glass railing thickness and position on the parapet · utility yard door head 7'-0" · closet as a plain solid · brick-insert panels not differentiated within EW1 walls · drop-off canopy column size · flat ground · project north = plan north.

## 6. Conflicts and unresolved items

- **V-1** Architectural revisions 6–10 still not in hand.
- **Drop-off canopy height** — no stronger source found; remains provisional. Next places to look: S131/S132 and wall section A331.
- **Elevation vs. frame sheets** — not a true conflict, but worth knowing: the building elevations show Level 2 glazing starting at about 19'-10" because the 19'-6" terrace parapet is in front of it; A811 gives the real sill at 19'-0". v002 follows A811.
- **Sun-shade depth** — A702's 13'-7" is measured from grid lines inside the wall; visible projection beyond the finish face is 11'-8".
- **Sheet revision mix** — A003, A811, A816, A701, A702 are permit/Rev 3 issue; A815, A012, A112, A132, A300, A301, S133 are Rev 5. No contradiction found.
- **Flat ground** makes the west utility yard walls read differently from reality (site falls to the west).
- Low wall east of the sight-triangle diagonal not found; gates, brick caps, louver detail at corners, brick-insert panels not modeled.
