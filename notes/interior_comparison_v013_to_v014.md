# Comparison — building_shell_v013 → building_shell_v014 (interior base-building framework)

Date: 2026-09-21
Basis: `notes/interior_base_control_v014.md` (written before the build). Not a tenant upfit.

## Validation

| Check | Result |
| --- | --- |
| Frozen v001–v013 files (142 files: models, scripts, all earlier notes, build reports, all 73 renders) | SHA-256 identical before and after: **0 changed** |
| `source_documents\Building I` | **Not opened, listed by name, read or used.** Aggregate only: 1,231 files / 6,929,037,544 bytes / newest modification time — identical to the recorded baseline |
| `source_documents\Building II` | 360 files; path, size and modification time all identical: **0 differences** |
| v013 objects inside the v014 file | **1,347 of 1,347 identical** in geometry (vertex for vertex), collection, materials and visibility flags; none removed |
| New objects | **428**, all named `INT_…`, all inside the `Building_II` collection tree and nowhere else |
| Exterior openings | none moved or resized — the inside shell is generated from the same face-of-stud polygons, A003 build-ups and opening list as v013 |
| Cameras, sun, sky, exposure, samples | all v013 cameras and light settings identical in the saved file; six `Cam_INT_…` cameras added |
| `TENANT_CONCEPTS` → `Concept_A`, `Concept_B`, `Concept_C` | created, **empty** |
| Tenant partitions, furniture, casework, finishes, branding, people, vehicles | none added |

`build_shell_v014.py` = `build_shell_v013.py` + the interior block, three calls to it and the interior view list. My first full v014 build was deleted and rebuilt once (it had switched the hidden v013 north-arrow review aid back on; the final file preserves every v013 flag). No approved file was involved.

## Collection structure

`Building_II` → `BASE_Exterior` (198) · `BASE_Structure` (69) · `BASE_Core` (17) · `BASE_Vertical_Circulation` (108) · `BASE_Restrooms` (6) · `BASE_MEP_Constraints` (23) · `BASE_Level_1` (2 slabs) · `BASE_Level_2` (slab + 2 ceiling planes) · `BASE_Terraces` (2) · `TENANT_CONCEPTS` (empty). Every storey-specific object is also linked into `BASE_Level_1` or `BASE_Level_2`, and carries a `level` property, so one floor can be shown alone. Collections 01–15 from v001–v013 are untouched.

**How the exterior and interior coexist.** The v001–v013 exterior is made of solid masses. v014 adds a hollow inside shell (`BASE_Exterior`) with clear glass in the same openings. The file is saved in *exterior mode* (looks exactly like v013; the inside shell, terrace slab and roof lid are hidden so they do not clash with the solid masses). To look inside, hide collections `01_Masses` and `03_Opening_panels` and un-hide the `BASE_Exterior` / `BASE_Terraces` objects — the text block `README_v014_view_modes` inside the .blend says the same. The build script does this automatically for the six interior renders, by visibility flags only.

## What is fixed / base building (modeled)

- **Exterior walls from inside**, both floors, with every v013 opening (6" stud + ⅝" gypsum inside the face of stud, A003).
- **Floor-to-floor 16'-0"**; Level 2 slab 6½" (S102); terrace slab at 15'-2"; roof structure 32'-0".
- **Level 1 slab as actually built:** 4" slab only on a 4'-0" perimeter ribbon, the lobby, Stair 2, Elec. Room 102 and Riser Room 104 (about 4,000 SF). The remaining **16,500 SF of tenant floor is "future slab on grade, not in scope"** (S101 / A191) and is modeled as a separate dark-brown object so it cannot be mistaken for a finished floor.
- **46 steel columns** from the S600 schedule on the written grid (69 objects, one per storey).
- **Core:** two-storey Lobby 101 with the open Stair 1 (15 + 13 risers, landing 8'-6 7/8"), Level 2 Lobby 204 with its floor edge, glass guards and the "open to below" void; CMU elevator shaft with a −5'-0" pit; enclosed Stair 2; Elec. Room 102 (Rev 5 size); Riser Room 104; mechanical shaft and two exhaust shafts at Level 2; single-user Restroom 205; rated-wall positions from the architect's rated-wall hatch.
- **Fixed door openings** (A800): 101B, 101C, 101D, 110A, 103 on Level 1; 200A, 200B, 200C, 210A on Level 2; exterior doors through the shell.
- **Ceilings that exist in the base building:** 10'-0" lids in 102, 104 and 205; Level 2 lobby ceiling at 12'-11 3/8". Tenant areas have no ceiling (exposed structure).
- **Tenant areas:** one undivided space per floor. Model check against the architect's BOMA 2017 usable areas (09/23/2025): Level 1 **18,362 SF modeled vs 18,484 SF** (−0.7 %, and the Rev 5 electrical room is larger than in the area plan); Level 2 **10,038 SF vs 9,918 SF** (+1.2 %; boundary convention differs at the lobby/terrace strip).

## What remains unknown or approximate

Column orientation, the offset direction of five offset columns, and fireproofing / furring wraps (G111 not yet applied) · floor and roof framing is recorded in the control note (clear height about 12'-11" under the deepest Level 2 girders, 13'-5" to 13'-8" typical) but **not modeled** · Stair 2 mid-landing height and the position of its upper run · stairs and guards are simplified stepped solids · elevator door position along the shaft wall · exact Level 1 poured-slab outline at the electrical strip · grid E.1 position (measured, not dimensioned) · restroom fixtures, plumbing chase walls, lobby millwork / banquette / feature wall (ID sheets) not modeled · door leaves and frames not modeled · interior faces of the shell are neutral; brick and metal-panel materials live on the (hidden) exterior masses · architectural revisions 6–10 not in hand.

## What would prevent an accurate tenant upfit

1. **No demising plan.** The documents show one tenant space per floor. Any multi-tenant split needs a lease plan that fixes demising walls and the common corridor that a second suite on a floor would need.
2. **MEP constraints are not modeled yet**: underside-of-beam heights per bay, roof-top unit and duct drops through the mechanical shaft, plumbing stub locations (relevant because the Level 1 slab is left out for tenant plumbing), sprinkler mains, electrical panel clearances. The sheets exist (M110/M120, P110–P122, FP110/FP120, E110/E120) but were not part of this pass.
3. **Braced-frame bays** (S501/S502) are not modeled; a brace in a bay blocks doors and openings there.
4. **Exterior window mullion spacing** matters for where partitions may land; mullions exist in the v004 facade detail but have not been checked from the inside.
5. **Tenant plan quality**: a PDF with a scale bar or two known dimensions registers well; an image-only sketch without dimensions can only be placed approximately.

## Are the documents sufficient for a first tenant-layout test?

**Yes, for a single-tenant, full-floor or partial-floor test fit** at partition level (walls, doors, rooms, eye-level walk-through): exterior walls, openings, columns, core, stairs, elevator, shafts, restroom, door locations and floor-to-floor heights are all documented and now in the model. The folder already contains candidate plans (`Building II\00 PLANS\Test Fits\…`, including a Level 1 ASC space plan and a 06/25/2026 plan) that could be registered to grids 1'–12' / A'–K'. **Not yet sufficient** for ceiling-height-critical rooms, plumbing-heavy layouts or multi-tenant demising without the items listed above.

## Render time

| View | Seconds (160 samples, RTX A1000, OptiX) |
| --- | --- |
| interior_L1_topdown_cutaway | 27.5 |
| interior_L2_topdown_cutaway | 33.1 |
| interior_L1_oblique_cutaway | 28.0 |
| interior_L2_oblique_cutaway | 31.9 |
| interior_section_looking_north (cut at y = 75 ft through elevator, Stair 1 and Level 2 lobby) | 17.0 |
| interior_eye_level_lobby (eye height 5'-6", Level 1 lobby looking south-west at Stair 1) | 66.2 |

Model file 2.5 MB → 2.7 MB. The seven exterior presentation views were not re-rendered in this pass (their cameras and settings are unchanged in the file).

## Renders (`renders/`)

`building_shell_v014_interior_L1_topdown_cutaway.png` · `…_interior_L2_topdown_cutaway.png` · `…_interior_L1_oblique_cutaway.png` · `…_interior_L2_oblique_cutaway.png` · `…_interior_section_looking_north.png` · `…_interior_eye_level_lobby.png`
