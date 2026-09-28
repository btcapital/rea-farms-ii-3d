# Building I — presentation realism control document v009

Date: 2026-09-23
Applies to: `scripts\Building_I\BI_build_presentation_v009.py` → `models\Building_I\BI_presentation_v009.blend`, renders `renders\Building_I\BI_presentation_v009_*.png`.
Base: **BI_footprint_v008.blend — owner-approved corrected geometry + site + landscape baseline (2026-09-23); v001–v008 frozen in `manifests\BI_freeze_BuildingI_v008_approved.json` (142 files, PASS).**
Scope: presentation realism only (materials, glazing response, surface roughness, planting appearance, daylight/sky, exposure, cameras). **No geometry, opening, plant position, site grade or context change.** No signage, people, vehicles, interiors, undocumented context, cinematic lighting, depth of field or colour grading.

## 0. Carried forward — unresolved items (nothing silently resolved)

| Item | Status carried into v009 |
| --- | --- |
| Gallery cantilever soffit 9.0 ft | measured on A5.15 A2 at 1/2" = 1'-0" (M ± 0.3), not written — unchanged |
| North-face Level 2 overhang soffit 14.83 ft | assumption (slab underside) — unchanged |
| Rear vestibule / end block parapet 32.0 ft | v001 raster-derived (R) — unchanged |
| G-15 brick-ledge tolerance | north-block west face and north face x 91–148 stay 0.5–0.7 ft inside the brick face — unchanged |
| Unresolved facade materials (v002 §7) | PNL3 medium-gray flush & reveal panel, storefront/curtain-wall frame colour (EFCO vs YKK), canopy steel paint, vestibule enclosure build-up, coping colour allocation (Slate Gray vs Regal White), soffit/portal ACM colour, hollow-metal door paint, overhead-door colour, unclassified wall areas — **all keep neutral placeholders; only their roughness/shading model is made physically plausible; no colour or product guessed** |
| Unresolved plant species | 117 symbols remain `LS_shrub_UNRESOLVED_species_documented_symbol` (grey-green placeholder) — unchanged |
| Simplified parking geometry | `SITE_asphalt_parking_north_APPROX` rectangle, islands exact — unchanged |
| Dumpster enclosure (Roman vs utility brick) and landscape wall footing/bottom | `SITE_dumpster_enclosure_APPROX` keeps the site brick placeholder; wall bottom below grade — unchanged |
| Earlier items G-1…G-6, F-1…F-8, SC-1/SC-3, LC-2, interpreted ground-cover discs, N Old Springs Rd trees not photo-verified, vestibule height (A-1) | carried forward unchanged |

## 1. Sources for the material refinement (already-approved assignments only)

| Material (v002 name, unchanged) | Documented product / finish (source) | Photo validation | v009 shading (all procedural — no product textures exist in the project) | Conf. |
| --- | --- | --- | --- | --- |
| `BRK1_Endicott_Manganese_Ironspot_utility` | Endicott utility brick 3 5/8 × 3 5/8 × 11 5/8 in, running bond 1/3, Manganese Ironspot Smooth, light gray mortar (A4.01 legend; PCO 14; A0.33) | dark charcoal-brown field with light joints (2025-09-09, 2026-07-28) | Brick Texture at true module (12" × 4" course incl. 3/8" joints), two iron-spot tones blended by noise, light gray mortar, mortar recess bump, roughness 0.72 (brick) / 0.9 (mortar). 1/3 running bond approximated by alternate-row 1/3 offset (node limitation) | W product / I shading |
| `PNL1_Alucobond_PLUS_PVDF_Bone_White` | Alucobond PLUS ACM, PVDF-2 Bone White (closeout warranty 2/15/2026, Cynergy) | warm off-white panels (photos) | satin painted aluminium: Bone White tone, roughness 0.32, non-metallic, specular 0.5. Panel joint layout not documented → **no joints modeled** | C colour / I shading |
| `PNL2_Alucobond_PLUS_SMP_Tricorn_Black` | Alucobond PLUS, SMP Tricorn Black (closeout) | black boxes around the large windows (photos) | Tricorn Black tone, roughness 0.40 | C / I |
| `TWS1_Kingspan_Unigrid_Verti-Lite_white` | Kingspan Unigrid Verti-Lite 2 3/4", white exterior/interior (A7.27; KLA warranty) | bright white translucent panels with vertical ribs (2026-07-28 b) | white frosted translucent panel: base white, transmission 0.35 at roughness 0.5, opaque alpha (was 0.55 alpha placeholder). Rib spacing not documented → **no rib pattern** | W / I |
| `GLZ_Viracon_VZE1-42_in_EFCO_framing_placeholder` | Viracon 1" VZE1-42 insulating (A7.2x); EFCO framing (closeout); frame colour U | slightly blue-gray reflective glass (photos) | reflective low-E glass placeholder: dark blue-gray base, roughness 0.04, IOR 1.5 — opaque (the placeholders are thin boxes on opaque walls; interiors not modeled); **frames still not modeled (U)** | W glass / U frames |
| `ROOF_JM_TPO_60mil_white` | JM TPO 60 mil white (closeout) | white roof (2025-09-09) | white, roughness 0.75, fine noise bump | C |
| `SCREEN_Alucopanel_FR_Enoc_White` | Alucopanel FR "Enoc White" (CONT 8, ECS) | white screen (2026-07-28 a) | off-white, roughness 0.40 | C |
| `CANOPY_1in_laminated_clear_glass` | 1" laminated clear glass (A1.13) | clear (2026-07-28 a) | real glass: transmission 1.0, roughness 0.02, IOR 1.52, faint green tint | W |
| `UNRES_exposed_steel_canopy_framing` | steel paint colour not found (U) | grey in photos | **neutral grey kept**, painted-steel roughness 0.45, metallic 0.3 | U |
| `UNRES_PNL3_flush_reveal_medium_gray` | PAC-CLAD flush & reveal medium gray drawn; no closeout product (U) | — | **placeholder colour kept**, roughness 0.45 | U |
| `UNRES_vestibule_100_enclosure`, `UNRES_unclassified_wall_area` | U | — | placeholder colours kept, roughness 0.5–0.6 | U |
| `SITE_asphalt`, `SITE_concrete_walk`, `SITE_pavers_Techo-Bloc_Westmount_Onyx_placeholder`, `SITE_lawn_INTERPOLATED_terrain`, `SITE_brick_veneer_wall`, `SITE_foundation_skirt_A` | v003 site materials (asphalt, concrete, pavers per PCO 17 "colour to match building brick" / Techo-Bloc placeholder, interpolated lawn, brick wall RFI 78) | 2026-07-28 a/b | asphalt near-black with mottle, roughness 0.85; concrete warm light grey with noise, roughness 0.8; pavers keep the placeholder tone (module size not documented → no joint pattern); lawn green with two-scale noise; landscape wall uses the building-brick shader (PCO 17 "to match building brick"); skirt earth-toned matte | I |
| `LS_*` foliage, trunk, mulch, ground cover, unresolved | v004 landscape materials | 2026-07-28 a/b | leaf materials with per-object hue/value variation (Object Info random), subsurface translucency 0.15, roughness 0.85; trunks brown with bark noise bump; mulch dark brown matte; `LS_unresolved_grey_green` keeps its placeholder colour | I |
| `CTX_Building_II_plain_mass` | context only | — | plain matte light grey, unchanged tone | — |

Nothing else changes: material names, slot assignments and per-face material indices are identical to v008 (verified by hash).

## 2. Lighting, sky, exposure

- World: Cycles Sky Texture (multiple-scattering physical sky), sun disc on, sun elevation 46°, sun azimuth from the south-west (the same side as the v001 validation sun: 40° elevation from the south-west) so the north entrance face is lit by sky light and the south/west faces by the sun — neutral late-morning/midday daylight, no golden hour; air/dust/ozone at defaults, altitude 220 m (site elevation ~660 ft).
- The v001 sun lamp `BI_sun` is disabled for render (the sky's sun disc replaces it); it is not deleted.
- View transform AgX (neutral), look None, exposure tuned on a test scene so that an 18 % grey ground reads mid-grey (value recorded in the validation note); no colour grading, no depth of field, no bloom, no motion blur.
- Film filter 1.5 px; Cycles path tracing 256 samples with OptiX denoising; persistent data on.

## 3. Cameras (6 presentation views, perspective, eye heights 5–25 ft except the site view)

| View | Camera | Location (ft) → target | Lens |
| --- | --- | --- | --- |
| 1 front hero | `BI_cam_hero_front` (new) | (150, 330, 22) → (140, 100, 14) | 35 mm |
| 2 main entrance oblique | `BI_cam_entrance_oblique` (v006) | (−40, 165, 24) → (50, 82, 12) | 35 mm |
| 3 south-east oblique | `BI_cam_oblique_southeast` (v008) | (470, −330, 150) → (150, 80, 12) | 35 mm |
| 4 north-west oblique | `BI_cam_oblique_northwest` (v001) | (−260, 420, 190) → (140, 100, 10) | 32 mm |
| 5 elevated site oblique | `BI_cam_site_elevated` (v003) | (560, −390, 320) → (80, 160, 0) | 28 mm |
| 6 close facade / material | `BI_cam_material_closeup` (new) | (2, 122, 6) → (40, 80, 12): brick wing, lobby curtain wall, PNL1 band, canopy glass | 45 mm |

## 4. Validation planned

Hash of every mesh object (world-space vertices + per-face material indices) and of every object transform and collection membership before/after — must be identical; comparison script `BI_compare_geometry_v008_v009.py` (vertices identical for all 798 objects, material slot names identical, node trees changed only); manifests v008-approved (142), project/Building II (311), Building I sources (1,231); render times and memory recorded.
