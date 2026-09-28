# Building I — final exterior presentation realism v013: validation and completion report

Date: 2026-09-25
Model: `models\Building_I\BI_presentation_v013.blend` (818 objects = 816 of v012 + 2 validation cameras), built by `scripts\Building_I\BI_build_presentation_v013.py` from `BI_presentation_data_v013.json` on `BI_entrance_finish_v012.blend` (owner-approved 2026-09-25). Control: `BI_presentation_control_v013.md`. Build report: `BI_presentation_v013_build_report.json`. Comparison: `BI_compare_geometry_v012_v013.py` → `BI_compare_v012_v013.json`. Photo validation: `BI_presentation_photo_validation_v013.py` → `renders\Building_I\BI_presentation_v013_photo_validation.png`.
Status: **built and validated, NOT approved.** v001–v012 frozen (`manifests\BI_freeze_BuildingI_v012_approved.json`, 224 files, PASS after this pass).

## 1. Realism changes made (shaders, world, render settings, cameras only)

| Area | v012 (= v009 shaders) | v013 |
| --- | --- | --- |
| Brick BRK1 (+ site brick wall) | 12 × 4 in module, 2 tones, noise mottle, mortar bump | 12 × 4 in module, **three tones blotched per brick, iron-spot speckle, deeper mortar recess (6 mm), brick roughness 0.62 / mortar 0.92**; tone checked against the drone photo |
| ACM PNL1 Bone White | flat satin | **PVDF satin with clear coat, 3 % tonal variation, vertical reveal seams 3/4 in every 2.0 ft (bump + darkening)** — pattern type from the A4.02 legend, pitch assumed |
| ACM PNL2 Tricorn Black | flat | **coated black, grid reveal seams 3/4 in every 4 × 2 ft** (legend: grid pattern, 3/4 in seams; pitch assumed) |
| Enoc White rooftop screen | flat | satin with coat and slight variation; no joints (undocumented) |
| TWS1 Kingspan translucent | frosted, transmission 0.35 | frosted, transmission 0.30, roughness 0.55, slight tonal variation; no ribs (spacing undocumented) |
| Glazing placeholder (Viracon low-E, EFCO frames unresolved) | opaque dark blue-grey, roughness 0.04 | **opaque low-E stand-in: lighter dark blue-grey base, clear coat (0.6, roughness 0.03) for the outer-lite sky reflection, roughness 0.06, ±11 % per-lite tone variation** → no pure black, no mirror, no single flat plate; interiors still not modeled |
| Canopy glass | clear laminated, roughness 0.02 | clear laminated, roughness 0.03 (unchanged in kind) |
| TPO roof | fine noise | two-scale noise, roughness 0.70 |
| Asphalt | near-black, one noise | **medium-dark grey (photo-checked), two-scale noise, fine bump, roughness 0.78** |
| Concrete walks / curbs | one noise | two-scale noise, fine bump, roughness 0.75 |
| Pavers (placeholder) | one noise | two-scale noise; placeholder tone kept, no joints (module undocumented) |
| Lawn | two-tone noise, no bump | two-scale noise with fine bump, roughness 0.95 |
| Mulch | one noise | two-scale noise, bump |
| Plants (7 foliage materials) | per-object hue/value, subsurface 0.15 | per-object hue/value, **leaf-scale bump noise**, subsurface 0.18–0.20; forms unchanged (vertex identity) |
| Bark | noise bump | noise bump (stronger) |
| Daylight | physical sky, sun elevation 42°, azimuth ENE | physical sky, **sun elevation 47°**, azimuth ENE, aerosol 0.9; neutral matte tone below the horizon |
| Colour / exposure | AgX, −4.3 | AgX, look None, **−4.35**, gamma 1.0; no grading |
| Cycles | 256 samples | **384 samples, adaptive (0.01), OptiX denoise, light tree**, caustics off, indirect clamp 10; no DOF, no motion blur |
| Cameras | — | `BI_cam_hero_porte_cochere` and `BI_cam_courts_exterior` added; all others untouched |

Nothing else changed. Obsolete v009 node logic is not carried; every node tree was rebuilt from the v013 data on the v012 model.

## 2. Unresolved placeholders (neutral, unchanged in status)

PNL3 medium-grey panel (F-6); storefront / curtain-wall frame colour and mullions (frames not modeled; EFCO per closeout); canopy steel paint (F-1 column wraps, drawing says PNL2 finish, columns not modeled as wraps); vestibule enclosure; coping colour allocation; soffit / portal ACM colour; hollow-metal and overhead-door colours; unclassified wall areas (UNRES); ACM seam pitch (assumed 2.0 ft PNL1 / 4 × 2 ft PNL2 — pattern type and 3/4 in width documented, pitch not); paver module and joints; TWS1 rib spacing; 117 species-unresolved plants (grey-green); annual bed colour; the SEAS annual disc on the median (interpreted); dumpster enclosure brick (SC-1); landscape-wall footing; parking-lot outline (SC-3); plant forms (approved low-poly placeholders — shape realism would break vertex identity and was not authorised as geometry). Geometry items G-1…G-6, G-15, F-2…F-9, the gallery soffit (M), north overhang (A), rear-vestibule parapet (R) and the v010 curb fade at the regrade-window edges are carried unchanged.

## 3. Photo-validation findings (`BI_presentation_v013_photo_validation.png`; genuine drone photo 2026-07-28, validation only)

| Item | Photo | Model | Verdict |
| --- | --- | --- | --- |
| Tower above the porte cochere | continuous white ACM box; glazed lower tower wrapping the corner; brick only on the wing (left) and north block (right) | same (v012 finish, v011 geometry); PNL1 now with vertical seams | agrees |
| White ACM vs brick transitions | brick on the wing north/west faces and the north-block east part; white panel on the tower, wing parapet, courts | same assignments | agrees |
| Curtain wall / glazing darkness | dark blue-grey with soft sky reflections, not black | dark blue-grey, coated, per-lite variation | agrees; mullions absent in the model (unresolved frames) |
| Porte-cochere glass and steel | clear glass canopy on slender painted steel columns | clear laminated glass, grey painted steel (placeholder colour) | agrees in kind; steel colour unresolved |
| Court-building white panel massing | long west facade of light vertical-pattern panels with a continuous clerestory band and a lower storefront band | PNL1 with vertical seams, clerestory lites, storefront lites | massing agrees; the photo's panels read cooler/greyer under haze than the closeout "Bone White" — documented colour kept |
| Brick tone | dark grey-brown, lighter joints | three-tone Manganese Ironspot with light grey mortar | agrees |
| Paving and landscape | grey concrete pavers at the drop-off, medium-dark asphalt, lawn, young trees and shrubs | placeholder-tone pavers (module unknown), asphalt lightened to match, lawn, low-poly plants at the documented positions | agrees in tone; plant forms remain placeholders |
| Temporary conditions | construction fence, containers, equipment at the Building II site | not modeled (Building II mass hidden in this view only, present elsewhere as context) | not copied |

The photo-match camera is an approximation (no camera metadata in the frame): vantage, direction and field of view are within a few degrees; it is a validation aid, not a calibrated match.

## 4. Render settings and performance

| View | Camera | Resolution | Seconds (384 samples, RTX A1000 OptiX) |
| --- | --- | --- | --- |
| 1 hero porte cochere | `BI_cam_hero_porte_cochere` | 2400 × 1350 | 43.1 |
| 2 photo-match drone | `BI_cam_photo_match_drone_2026-07-28a` | 2000 × 1125 | 24.3 |
| 3 northwest oblique | `BI_cam_oblique_northwest` | 2000 × 1400 | 27.2 |
| 4 southeast oblique | `BI_cam_oblique_southeast` | 2000 × 1400 | 25.3 |
| 5 courts exterior | `BI_cam_courts_exterior` | 2000 × 1400 | 27.0 |
| 6 site elevated | `BI_cam_site_elevated` | 2000 × 1400 | 17.2 |
| 7 facade material closeup | `BI_cam_material_closeup` | 2000 × 1400 | 51.6 |
| 8 entrance eye level | `BI_cam_entrance_eye_level` | 2000 × 1400 | 43.0 |

Performance impact vs v009 (256 samples, 15–37 s): +50 % samples with adaptive sampling and the coated / bump shaders give 17–52 s per frame (roughly +40 %); the model file is 4.4 MB (materials are procedural, no textures). Exposure check: all eight views 0.00 % of pixels ≥ 250, ≤ 0.52 % ≤ 8, means 123–163 / 255. Site artifacts checked in views 1, 2, 6, 8: no z-fighting, no terrain through pavement, no floating curbs, no faceted paved surfaces, no dark streaks (v010 grid slabs and terrain cut carried).

## 5. Validation

| Check | Result |
| --- | --- |
| `BI_freeze_BuildingI_v012_approved.json` (224 files: every v001–v012 note, data, script, model, render) | PASS |
| `BI_freeze_BuildingI_v008_approved.json` (142) | PASS |
| `BI_freeze_sources_BuildingI_longpath_v001.json` (1,231) | PASS — `source_documents` unchanged |
| Scene hash (all vertices, transforms, collections, render-visibility, face material indices, material slots) before / after in the build script, re-checked after rendering | identical (`6d2d993f…`) |
| `BI_compare_geometry_v012_v013.py` | geometry identical for all 816 common objects; building identical; site identical; plants identical (positions, sizes, assignments); 0 objects changed; 2 cameras added; 0 removed |
| Materials | 29 node trees rebuilt (same names, same users), 0 added, 0 removed; `BI_grid`, `BI_ground`, `BI_slab` untouched |
| Only shaders, world, colour management, render settings and cameras changed | yes |

## 6. Files created in this pass

```
notes/Building_I/BI_presentation_control_v013.md
notes/Building_I/BI_presentation_data_v013.json
notes/Building_I/BI_presentation_v013_build_report.json
notes/Building_I/BI_presentation_validation_v013.md
notes/Building_I/BI_compare_v012_v013.json
notes/Building_I/manifests/BI_freeze_BuildingI_v012_approved.json
notes/Building_I/manifests/BI_freeze_BuildingI_v013_pending_approval.json
scripts/Building_I/BI_build_presentation_v013.py
scripts/Building_I/BI_compare_geometry_v012_v013.py
scripts/Building_I/BI_presentation_photo_validation_v013.py
models/Building_I/BI_presentation_v013.blend
renders/Building_I/BI_presentation_v013_{1_hero_porte_cochere,2_photo_match_drone,3_northwest_oblique,4_southeast_oblique,5_courts_exterior,6_site_elevated,7_facade_material_closeup,8_entrance_eye_level}.png
renders/Building_I/BI_presentation_v013_photo_validation.png
```

## 7. Readiness

v013 is ready to become the exterior presentation baseline **within the limits above**: it is vertex-identical to the approved v012, every finish keeps its approved assignment, the daylight is neutral, and the photo comparison agrees on massing, material placement and tone. What it cannot claim: window mullions, plant forms, paver joints, TWS1 ribs and the ACM seam pitch are placeholders or assumptions, and interiors are absent behind the glazing. Those are documented, not hidden.

Next decision for the owner: **approve or redirect v013** (then freeze v001–v013). Not started: interiors, tenant upfits, viewer work.
