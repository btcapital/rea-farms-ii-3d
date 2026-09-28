# Comparison — building_shell_v009 → building_shell_v010 (presentation pass)

Date: 2026-09-21
Basis: `notes/presentation_control_v010.md`.

## Validation

| Check | Result |
| --- | --- |
| Frozen v001–v009 files (93 files: models, scripts, all notes, build reports, all 47 renders) | SHA-256 identical before and after: **0 changed** |
| `source_documents` | 360 files, **0 modified** |
| v009 mesh objects in v010 | **925 of 925 with identical vertex coordinates** |
| Per-face material assignment | **925 of 925 identical** (same material name on every face) |
| Removed | none |
| Added | 4 objects, `PRES_backdrop_north / south / east / west`, in the new collection `13_Presentation_v010` (flat ground outside the modeled site; not site elements) + 6 presentation cameras |
| Render-visibility change | `Site_North_arrow` hidden from rendering (object itself unchanged) |
| Script control checks (205'-0" × 105'-10" face of stud, finish extents, top of parapet 43'-10") | pass |
| Signage, branding, people, vehicles, furniture, new planting | none added |

`build_shell_v010.py` = `build_shell_v009.py` + the presentation block, one call to it after the site is built, six new views, 256 samples and the exposure value. No data or geometry function was edited. (Three low-resolution lighting trials were run in a scratch folder first; two early drafts of the v010 script were regenerated before the final run. No approved file was involved.)

## What changed

1. **Shader response inside the existing materials** — color variation, roughness variation and fine bump for brick, metal panels and copings, frames, glass, roofing, paving, asphalt, lawn, mulch and plant proxies (table in the control document). Names and assignments untouched; `UNRES_` placeholders stay neutral grey.
2. **Light** — flat studio light replaced by a physical clear sky plus a sun lamp with the true solar disc size; sun at azimuth 80°, elevation 36° (an assumed mid-June morning, chosen because the front faces north).
3. **Exposure / color** — AgX, no look, exposure −0.35, no white-balance shift, no grading, bloom, vignette, depth of field or lens distortion.
4. **Cameras** — six new views, eye-level ones kept level with vertical shift so verticals do not converge.
5. **Backdrop ground** beyond the site edges.

## Renders (`renders/`)

`building_shell_v010_hero_front_north.png` · `…_entrance_oblique_northeast.png` · `…_rear_oblique_southeast.png` · `…_elevated_site_oblique_northwest.png` · `…_facade_material_closeup.png` · `…_corner_northwest_eye_level.png`
Cycles, OptiX GPU, 256 samples, denoised, 2560 × 1440 (hero 2560 × 1200); 19–70 s each.

## Unresolved realism issues

No surrounding context (Building I, streets, trees, cars) so the horizon is empty and reflections are plain · no interiors behind the glass · placeholder finishes still grey and named colors still approximations · planting is proxy geometry, lawn and mulch are flat · no paver / panel / sealant joints, fixtures, hardware, bollards or striping · the north front is in raking morning light because it faces north · a thin dark line appears near the top of the close-up view where the canopy glass is seen almost edge-on (render artifact of the simple glass slab).
