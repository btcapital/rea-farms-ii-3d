# Building I — presentation realism v009: validation and completion report

Date: 2026-09-23
Model: `models\Building_I\BI_presentation_v009.blend` (800 objects = 798 of v008 + 2 presentation cameras), built by `scripts\Building_I\BI_build_presentation_v009.py` from `BI_presentation_data_v009.json`. Control document: `BI_presentation_control_v009.md`. Build report: `BI_presentation_v009_build_report.json`. Comparison: `BI_compare_geometry_v008_v009.py`.
Status: **built and validated, NOT approved.** v001–v008 frozen (`manifests\BI_freeze_BuildingI_v008_approved.json`, 142 files, PASS).

## 1. What changed (object-by-object comparison v008 → v009)

| Class | Result |
| --- | --- |
| Geometry, transforms, collections, material slot names, per-face material indices of all 798 v008 objects | **identical** (scene hash `248c0b66…85a2` before and after in the build script; comparison script: no object with changed vertices, transform, assignment or collection) |
| Objects added | 2 cameras: `BI_cam_hero_front`, `BI_cam_material_closeup` |
| Objects removed | none |
| Object flags | `BI_sun` (v001 validation sun lamp) hidden for render — replaced by the physical sky's sun disc; the lamp is not deleted. Smooth-shading flag set on 255 objects (plant spheres, street-tree canopies, top faces of the interpolated terrain and the hardscape slabs) — a shading attribute, vertices untouched |
| Materials | 29 existing materials had their node trees rebuilt (same names, same users): BRK1, PNL1, PNL2, PNL3 (placeholder), TWS1, GLZ, canopy glass, canopy steel (placeholder), vestibule (placeholder), unclassified wall (placeholder), TPO roof, Enoc White screen, Building II context mass, 6 site materials, 10 landscape materials. Untouched: `BI_grid`, `BI_ground`, `BI_slab` (hidden reference objects). No material added or removed |
| World | plain grey background → physical sky (multiple-scattering, sun disc on, elevation 42°, azimuth from the east-north-east) with a neutral matte tone below the horizon so views past the modeled terrain do not fall into black (world shader only) |
| Colour management / render | Standard → AgX, look None, exposure −4.3; Cycles 64 → 256 samples, OptiX denoise, caustics off, indirect clamp 10, film filter 1.5 px, persistent data; no depth of field, no motion blur, no grading |

## 2. Realism refinements made (all on the already-approved assignments)

- **Brick BRK1** (Endicott Manganese Ironspot utility): true 12" × 4" course module with 3/8" light-grey joints, two iron-spot tones mottled by noise, mortar recess bump, brick/mortar roughness 0.72/0.90. The 1/3 running bond is approximated by an alternate-row 1/3 offset (Blender brick-node limitation). The landscape wall shares the shader (PCO 17 "to match building brick"); the dumpster enclosure keeps its unresolved status.
- **ACM panels**: PNL1 Bone White PVDF (satin, roughness 0.32) and PNL2 Tricorn Black SMP (roughness 0.40) as installed per the closeout warranty; panel joint layout not documented → no joints.
- **Translucent wall TWS1** (Kingspan Unigrid Verti-Lite): white frosted panel (transmission 0.35 at roughness 0.5) instead of the 55 % alpha placeholder; rib spacing not documented → no rib pattern.
- **Glazing** (Viracon VZE1-42): dark blue-grey reflective low-E response (roughness 0.04) — still opaque placeholders because interiors are not modeled and the EFCO frames remain unresolved.
- **Canopy glass**: real clear laminated glass (transmission 1.0, IOR 1.52). Canopy steel keeps its neutral grey with a painted-steel sheen.
- **Roof / screen**: JM TPO white with fine surface noise; Alucopanel Enoc White screen.
- **Site**: asphalt (mottled near-black, roughness 0.85), concrete walks (warm light grey), pavers (placeholder tone kept, no joint pattern — module not documented), interpolated lawn (two-scale colour noise), foundation skirt earth tone.
- **Planting**: per-plant hue/value variation (Object Info random), leaf translucency (subsurface 0.15), bark noise bump on trunks, dark mulch; annual bed placeholder toned neutral; the 117 unresolved-species symbols keep their grey-green placeholder. Locations, quantities and sizes unchanged.
- **Daylight**: physical sky, clear summer morning from the east-north-east so the entrance/north face receives grazing sun and the east face full sun; neutral AgX exposure calibrated on an 18 % grey test scene; shadows and sky gradient from the physical model only.

## 3. Render settings and performance

| Item | Value |
| --- | --- |
| Engine / device | Cycles, OptiX GPU (RTX A1000) |
| Samples / denoise | 256, OptiX denoise; caustics off; indirect clamp 10 |
| Colour management | AgX, look None, exposure −4.3, gamma 1.0 |
| Resolutions | hero 2400 × 1350; other views 2000 × 1400 |
| Render times | front hero 29.5 s; entrance oblique 31.2 s; south-east oblique 15.9 s; north-west oblique 21.5 s; elevated site 15.4 s; facade close-up 36.7 s (v008 validation views at 64 samples took 5–22 s) |
| File size | 4.49 MB (v008 4.45 MB) |
| Exposure check | no view has clipped highlights (0.00 % of pixels ≥ 254); mid-tones 97–167/255 |

## 4. Validation

| Check | Result |
| --- | --- |
| Scene hash (all vertices, transforms, collections, material assignments) before/after in the build script | identical, re-checked after rendering |
| `BI_compare_geometry_v008_v009.py` | geometry identical for all common objects; only `BI_sun` render flag, 29 material node trees, world, view transform, samples and 2 cameras differ |
| Site geometry / landscape locations | unchanged (hash) |
| `BI_freeze_BuildingI_v008_approved.json` (142 files: all v001–v008) | PASS |
| `BI_freeze_BuildingI_v007_pre_v008.json` (114), `BI_freeze_BuildingI_v006_approved.json` (101) | PASS |
| `BI_freeze_project_and_BuildingII_v001.json` (311) | PASS |
| `BI_freeze_sources_BuildingI_longpath_v001.json` (1,231 source files) | PASS |
| Renders inspected | all six: no clipping, neutral daylight, materials read as documented |

## 5. Renders

`renders\Building_I\BI_presentation_v009_1_front_hero.png`, `_2_entrance_oblique.png`, `_3_southeast_oblique.png`, `_4_northwest_oblique.png`, `_5_site_elevated.png`, `_6_facade_material_closeup.png`.

## 6. Remaining placeholder / approximate items (nothing resolved silently)

- Geometry items carried unchanged: gallery soffit 9.0 ft (M), north overhang soffit 14.83 (A), rear vestibule parapet 32.0 (R), G-15 brick-ledge tolerance, G-1…G-6, vestibule height (A-1).
- Facade: PNL3 medium-grey panel, storefront/curtain-wall frame colour (frames not modeled), canopy steel paint, vestibule enclosure, coping colour allocation, soffit/portal ACM colour, hollow-metal and overhead-door colours, unclassified wall areas — all still neutral placeholders; glazing placeholders are opaque (no interiors); ACM panel joints and TWS1 ribs not modeled (layout/spacing undocumented); the canted storefront face still carries no finish region; the tops of the one-storey projections and the Level 2 bay show wall material (no roof tag).
- Site: parking-lot outline approximate (islands exact); mulch islands read as dark mounds; the west drive/plaza slabs are terrain-following triangulations and show faint facets and small terrain patches at their edges (v003 geometry, untouched); paver module unknown; dumpster enclosure brick unresolved (SC-1); landscape wall footing not modeled.
- Planting: 117 species-unresolved symbols (grey-green), 11 interpreted ground-cover discs, 7 unmodeled hatched ground covers, N Old Springs Rd trees not photo-verified; low-poly sphere/cylinder plant forms (no leaf geometry — appearance only was in scope).
- Context: Building II plain mass only; no other context.
- Lighting: single clear-sky condition (east-north-east morning sun); no overcast alternative rendered.

## 7. Files created in this pass

```
models/Building_I/BI_presentation_v009.blend
notes/Building_I/BI_presentation_control_v009.md
notes/Building_I/BI_presentation_data_v009.json
notes/Building_I/BI_presentation_v009_build_report.json
notes/Building_I/BI_presentation_validation_v009.md
notes/Building_I/manifests/BI_freeze_BuildingI_v008_approved.json
renders/Building_I/BI_presentation_v009_{1_front_hero,2_entrance_oblique,3_southeast_oblique,4_northwest_oblique,5_site_elevated,6_facade_material_closeup}.png
scripts/Building_I/BI_build_presentation_v009.py
scripts/Building_I/BI_compare_geometry_v008_v009.py
```

Next decision for the owner: **approve or redirect the v009 presentation baseline** (then freeze v001–v009). Not started: interiors, viewer work, further landscape refinement, signage, vehicles, people.
