# Presentation control document v010

Date: 2026-09-21
Applies to: `scripts/build_shell_v010.py` → `models/building_shell_v010.blend`
Baseline: **v009, frozen.** v010 rebuilds the identical geometry, material assignments, site and planting, and changes **presentation only**. No signage, branding, names, logos, wayfinding, people, vehicles, furniture or new planting. Written before the final v010 build (after low-resolution lighting tests).

Nothing in this pass is a documented finish. **Every value below is an assumption made only for visual realism**, and none of it alters what the control documents of v001–v009 record.

## 1. What is preserved exactly

Building, facade detail, openings, parapets, canopies, sun-shade, railings, utility enclosure, grades, paving, walks, walls, plant positions and quantities — same objects, same vertices. Material **names** and **per-face assignments** are unchanged; the unresolved-finish placeholders (`UNRES_…`) remain neutral grey placeholders and are still named as such.

## 2. Presentation changes

### Material response (shader nodes added inside the existing materials)

| Material group | Refinement | Why |
| --- | --- | --- |
| BRK-1 brick, brick caps | low-frequency color variation (up to about ±35 % value), roughness 0.55–0.85 varying, fine surface bump on top of the existing joint bump | brick-to-brick variation and the slight sheen of an ironspot face |
| ACM-1…4, copings MTL-1…3, sun-shade paint, canopy-steel and HM-door placeholders | roughness 0.22–0.36 varying at panel scale, very faint large-scale bump, 15 % clear-coat | coil-coated / painted metal with faint oil-canning in reflections |
| Frames | roughness 0.28–0.40 varying | painted extrusions |
| Vision glass G1/G2 | zero roughness, slightly raised reflectivity, very slight large-scale normal waviness, dark body | coated insulating glass seen from outside in daylight; **interior visibility kept minimal** because no interior is modeled |
| Spandrel G3 | roughness 0.03 | glass-faced spandrel |
| TPO roof | slight color and roughness variation | membrane seams and dust are not modeled |
| Pavers, plaza, concrete, terrace pavers, base strip, painted CMU | color variation, roughness 0.7–0.9, fine bump | cast / concrete surfaces. Paver joint patterns are **not** added (unit sizes are not documented) |
| Existing asphalt | color variation, roughness 0.75–0.95, fine aggregate bump | |
| Lawn, mulch / bed surfaces | color variation and coarse bump | still flat surfaces — see unresolved issues |
| Plant proxies | per-plant brightness variation (±18 %), leaf-scale mottling, strong bump to break up the smooth proxy, 5 % subsurface | same proxy shapes, sizes and positions as v008/v009 |

### Light, sky, exposure

| Setting | Value | Note |
| --- | --- | --- |
| Sun | azimuth 80° (just north of east), elevation 36°, angular size 0.545°, strength 7, color (1.0, 0.95, 0.88) | **assumed**: about 8:20 am solar time in mid-June at 35° N. Chosen because the front faces north: a morning summer sun is the only ordinary daylight that rakes across the front. Not golden hour (sun well above 30°) |
| Sky | Blender physical sky ("multiple scattering" model in 5.2), sun disc off (the lamp provides it), strength 0.16 | clear sky, default atmosphere |
| White balance | none applied; neutral | shade areas keep a natural cool skylight tint |
| View transform | AgX, look "None", exposure −0.35 | no contrast look, no grading, no bloom, no vignette |
| Depth of field / lens distortion | off / none | |
| Ambient occlusion | none added — contact shading comes from the path tracer's global illumination | |

Project north is still assumed equal to plan north (assumption A-1 from v001), so the sun direction relative to the building inherits that assumption.

### Cameras (new; the v009 review cameras remain in the file, unused)

| View | Position (ft) → target | Lens | Notes |
| --- | --- | --- | --- |
| `hero_front_north` | (112, 292) → front, eye height 5.5 ft | 30 mm | level camera with vertical shift: no converging verticals |
| `entrance_oblique_northeast` | (205, 196) → entrance | 30 mm | primary entrance oblique |
| `rear_oblique_southeast` | (262, −118) → south-east corner | 40 mm | |
| `elevated_site_oblique_northwest` | (−165, 262, 135 ft up) | 35 mm | |
| `facade_material_closeup` | (48, 140) → curtain wall / brick / door 100A bay | 45 mm | |
| `corner_northwest_eye_level` | (−92, 196) → glazed north-west corner and utility yard | 30 mm | additional view |

All 2560 × 1440 except the hero (2560 × 1200). 36 mm sensor.

### Presentation-only objects

Collection `13_Presentation_v010`: four flat **backdrop ground** slabs outside the modeled site rectangle (dark paving tone to the north, neutral green elsewhere), set at the mean height of each terrain edge, so eye-level views do not show the cut edge of the site model. They are not site elements. `Site_North_arrow` is hidden from rendering (object unchanged).

## 3. Render settings

Cycles, GPU (OptiX, NVIDIA RTX A1000), 256 samples, OpenImageDenoise on, PNG 8-bit, film exposure 1.0, no motion blur, no compositing.

## 4. Known realism limits (not faked)

1. **No surroundings.** Building I, the streets, cars, trees and the skyline are not modeled, so the horizon is empty and the glass reflects only sky and flat ground. Real photographs would show reflected context.
2. **No interiors**, so glazing reads uniformly dark; no blinds, ceilings or lights.
3. **Placeholders remain grey**: drop-off canopy steel, painted CMU, HM doors, terrace pavers' color, terrace-side parapet, building base strip. Named colors (brick, ACM, frames, glass) are still approximations of finish names.
4. **Planting is still proxy geometry** (rounded forms at installed size); lawn and mulch are flat shaded surfaces without blades or chips.
5. No paver joints, ACM panel joints, sealant joints, brick-insert panels, coping profiles, railing shoes, canopy fittings, door hardware, light fixtures, bollards or striping — none are in the approved geometry.
6. Terrain between written spot elevations is interpolated (v006), and the thin lawn sliver beside the entrance curve (v009) remains.
7. Schedule shortfall (CATM / CORA / LACE), architectural revisions 6–10 and the sun-shade drawings-vs-spec conflict remain open.
