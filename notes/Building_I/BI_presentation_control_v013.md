# Building I — final exterior presentation realism v013: control document

Date: 2026-09-25
Controlling baseline: `models\Building_I\BI_entrance_finish_v012.blend` — owner-approved 2026-09-25 (v010 entrance site + v011 tower west-face regions + v012 tower-front finish = the exterior + site baseline; v008 footprint, v006 entrance geometry, v005 finish regions, v004 landscape, v003 site inside it). Frozen: `manifests\BI_freeze_BuildingI_v012_approved.json` (224 files, PASS).
Authorised gate: FINAL EXTERIOR PRESENTATION REALISM BASELINE (skill gate 3/4 presentation layer). Not authorised: interiors, tenant upfits, viewer, signage, branding, people, vehicles.
Data: `BI_presentation_data_v013.json` (every material, sky, view, render and camera parameter). Script: `scripts\Building_I\BI_build_presentation_v013.py`. Output: `models\Building_I\BI_presentation_v013.blend`, renders `BI_presentation_v013_*.png`. Validation: `BI_presentation_validation_v013.md`.

## 1. Scope and hard rules

Changed: material node trees (29 materials, same names, same slot assignments, same users), the world (physical sky), colour management / exposure, Cycles settings, and two validation cameras. Obsolete v009 shader logic is not carried: v013 rebuilds every node tree from the v013 data on the v012 model.
Not changed (hash-verified before and after in the build script, and by `BI_compare_geometry_v012_v013.py`): every vertex, transform, collection, render-visibility flag, per-face material index and material slot of all 816 v012 objects; plant positions and sizes; site grades; openings; roof; canopy; curbs.
Not done: no geometry, no plant shape change (a shape change would break vertex identity, so plants keep their approved low-poly forms and receive material-only realism), no signage/branding/people/vehicles, no invented details (no mullions, no paver joints, no TWS1 ribs, no ACM seam pitch beyond the assumption flagged below), no interiors.

## 2. Evidence for each finish (codes: W written, C closeout record, P photo-consistent, I interpreted shading, A assumed, U unresolved)

| Material (slot name unchanged) | Documented product | v013 shader | Codes |
| --- | --- | --- | --- |
| BRK1 Endicott Manganese Ironspot utility (also `SITE_brick_veneer_wall`) | A4.02 legend: running bond 1/3, utility 3 5/8 × 3 5/8 × 11 5/8, light grey mortar; PCO 14 | 12 × 4 in module with 3/8 in joints, 1/3 offset alternate rows, three brick tones blotched per brick, iron-spot speckle, mortar recess 6 mm, roughness brick 0.62 / mortar 0.92 | W / C / P tone / I |
| PNL1 Alucobond PLUS PVDF Bone White | closeout Cynergy warranty (11,477 sf); legend PNL1 "Panel Type 1 (Vertical Pattern)" | satin PVDF (roughness 0.30, coat 0.25), 3 % tonal variation, **vertical reveal seams 3/4 in wide every 2.0 ft** (bump + darkening, no geometry) | C / W pattern type / **A pitch** / I |
| PNL2 Alucobond PLUS SMP Tricorn Black | closeout (13,248 sf); legend PNL2 "Grid Pattern … vertical and horizontal 3/4 in seams" | roughness 0.38, coat 0.2, **grid seams 3/4 in every 4.0 × 2.0 ft** | C / W seam width and pattern type / **A pitch** / I |
| PNL3 flush & reveal medium grey | unresolved (F-6) | placeholder colour kept, plain | U |
| Enoc White rooftop screen (Alucopanel FR) | CONT 8 | satin, 2 % variation, no joints (layout undocumented) | C |
| TWS1 Kingspan Unigrid Verti-Lite | A7.27 | white frosted translucent (transmission 0.30, roughness 0.55); rib spacing undocumented → no ribs | W / I |
| GLZ Viracon VZE1-42 in EFCO framing (placeholder) | A7.21/A7.26 glass; frames unresolved; interiors not modeled | opaque low-E stand-in: dark blue-grey base (interior reads as unlit), clear coat 0.6 at roughness 0.03 (outer-lite sky reflection), roughness 0.06, ±11 % per-lite tone variation so the wall is not one flat plate | W glass / U frames / I |
| Canopy 1 in laminated clear glass | A1.13 | clear glass, transmission 1.0, IOR 1.52 | W |
| JM TPO 60 mil white | closeout | two-scale noise, roughness 0.70 | C |
| Canopy steel, vestibule, unclassified wall | unresolved | placeholder colours kept; steel with a painted sheen | U |
| Asphalt | v003 | two-scale noise (1.5 / 45), roughness 0.78, fine bump; tone medium-dark grey checked against the drone photo | I / P |
| Concrete walks and curbs | v003 / v010 | two-scale noise, roughness 0.75, fine bump | I |
| Techo-Bloc Westmount pavers | CS-101 notes; module undocumented | placeholder tone kept, fine noise, no joints | placeholder |
| Lawn (interpolated terrain) | v003 | two-scale noise (0.7 / 25), roughness 0.95, fine bump | I |
| Mulch | v004 | two-scale noise, roughness 0.95, bump | I |
| Plant foliage (7 materials) | v004/v007 | per-object hue/value variation (Object Info random), leaf bump noise, subsurface 0.18–0.2; unresolved species keep grey-green | I / U |
| Bark | v004 | noise + bump | I |
| Building II context mass | context | unchanged tone; hidden in the photo-match view only (the July 2026 photo predates it) | context |

## 3. Daylight, colour, render

- Sky: Blender physical sky (multiple scattering), sun disc, elevation 47° (v009 42°), rotation 75° (from the east-north-east so the entrance/north faces receive grazing light and the east face full sun), aerosol 0.9, altitude 220 m; neutral matte tone below the horizon (world shader only). Clear late-morning daylight; no golden hour, no dramatic contrast.
- Colour management: AgX, look None, exposure −4.35 (v009 −4.3), gamma 1.0; no grading. Exposure check on the trial views: mean 123–163 / 255, 0.00 % of pixels ≥ 250, ≤ 0.31 % ≤ 8.
- Cycles: 384 samples, adaptive sampling threshold 0.01, OptiX denoise, caustics off, indirect clamp 10, light tree, filter 1.5 px, persistent data; no depth of field, no motion blur.
- Smooth-shading flags as v009 (plants all faces; terrain and hardscape top faces) — a shading attribute, no vertex change.

## 4. Cameras / views (7 required + 1)

| View | Camera | Note |
| --- | --- | --- |
| 1 hero entrance / porte cochere | `BI_cam_hero_porte_cochere` (−72, 212, 13) → (40, 86, 12), lens 32 — new | drop-off loop, median island, canopy, lobby tower |
| 2 drone-photo match | `BI_cam_photo_match_drone_2026-07-28a` (v012) | explicit validation camera; Building II mass hidden in this view only |
| 3 northwest oblique | `BI_cam_oblique_northwest` (v003) | |
| 4 southeast oblique | `BI_cam_oblique_southeast` (v003) | |
| 5 court-building exterior | `BI_cam_courts_exterior` (−40, 340, 20) → (165, 200, 22), lens 30 — new | TWS1 band, PNL1 massing, brick base |
| 6 elevated site oblique | `BI_cam_site_elevated` (v003) | |
| 7 close facade / material | `BI_cam_material_closeup` (v009) | north-east corner: PNL1, TWS1, brick, lites |
| 8 entrance eye level (extra) | `BI_cam_entrance_eye_level` (v010) | continuity with the v010–v012 validation views |

## 5. Assumptions and unresolved items (carried, none resolved silently)

- **A**: ACM reveal pitch (PNL1 2.0 ft vertical; PNL2 4.0 × 2.0 ft grid) — the legend gives the pattern type and the 3/4 in seam width, not the pitch; shader-only, easily changed in the data file.
- **U**: PNL3 colour; storefront / curtain-wall frame colour (frames not modeled); canopy steel paint; vestibule enclosure; coping colour allocation; soffit/portal ACM colour; hollow-metal and overhead-door colours; unclassified wall areas; 117 species-unresolved plants; annual bed colour; paver module; TWS1 rib spacing; dumpster enclosure brick (SC-1); landscape-wall footing.
- Geometry items carried unchanged: G-1…G-6, G-15, F-1…F-9, gallery soffit 9.0 (M), north overhang 14.83 (A), rear vestibule parapet 32.0 (R), SC-3 parking outline, LC-2, interpreted ground-cover discs, the SEAS annual disc on the island, the curb fade at the regrade-window edges (v010).
- Lighting: one clear-sky condition; no overcast alternative.
- Plant forms remain the approved low-poly placeholders (material realism only).
