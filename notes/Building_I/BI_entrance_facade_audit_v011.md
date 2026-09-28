# Building I — upper-entry / porte-cochere facade audit v011 (the "black rectangle" above the entrance)

Date: 2026-09-23
Baseline audited: `models\Building_I\BI_entrance_site_v010.blend` (site = v010, building = v008 approved, finish regions = v008 regeneration of the v005 regions, materials = v009).
Frozen before any change: `manifests\BI_freeze_BuildingI_v010_pending_approval.json` (182 files: every v001–v010 note, data file, script, model and render; PASS at the start and at the end of this pass).
Status: **cause found and documented; the condition is a mesh defect in one finish-region object, not a documented recess → Building I v011 created (targeted correction, §6).**

## 1. Diagnosis — what produces the black area

| Step | Method | Result |
| --- | --- | --- |
| Locate | ray-cast from `BI_cam_entrance_eye_level` (2000 × 1400) through the black pixels (x 1290–1470, y 345–400) and a control band below them | every ray hits **`FR_WEST_PNL1_W2b`**, material `PNL1_Alucobond_PLUS_PVDF_Bone_White`, front-facing (normal −x), on the plane **x 28.47**, y 55.8–70.4, **z 29.8–34.8**; the control band hits the same object at z 25–30, which renders white |
| Per-pixel object-ID image of the region (ray-cast every pixel) | the whole tower face is one object (W2b); no other object, no sky, no occluder inside the black area |
| Hidden / render-only objects | `hide_viewport`, view-layer exclusion and collection flags listed | only `BI_grade_plane_660` (hidden both ways); nothing renders that the ray-cast cannot see |
| Hide tests (24-sample region renders) | W2b hidden → black stays (the lobby-band prism face behind it shows); `BI_Z2_band_E_F2` hidden → black stays; PNL1 replaced by a plain diffuse → black stays; **view-layer material override = diffuse white on everything → black stays** | not a material, not glazing, not backface culling, not an occluder |
| Mesh dump of W2b | 3 faces / 11 vertices: **face 0 = x 28.47, y 54.2–70.58, z 24.6–33.3 (142.5 sq ft); face 1 = x 28.47, y 54.2–74.38, z 24.6–40.0 (310.8 sq ft); face 2 = x 70.97, y 70.58–74.38, z 24.6–32.6/32.8 (30.8 sq ft)** | face 0 lies entirely inside face 1 on the same plane (0.03 ft in front of the wall); face 2 sits inside the lobby-band prism (invisible) |
| Face tests | render with face 1 deleted → black gone but the tower top (z 33.3–40) uncovered; render with **face 0 deleted → clean white face, no artifact** | the black patch is the region of face 1 where camera rays hit face 1 and the shading point's shadow / bounce rays are immediately blocked by the coincident face 0 (Cycles offsets rays only against the triangle that was hit, not against a *different* coplanar triangle) → no light reaches those pixels → solid black. Where the camera rays happen to hit face 0 first, the same happens in reverse for the pixels of face 1; the wedge shape follows the two faces' triangulations |
| Coplanar scan of all `FR_*` objects (vertical faces, same plane ± 0.05 ft, overlap > 1 sq ft) | 17 pairs: **W2b face 0 ⊂ face 1 (142.5 sq ft)**; 10 pairs inside `FR_WEST_GLZ_W2` on the same plane (0.2–10.3 sq ft each; the curtain-wall backdrop below 24.6 has the same duplicated strips); 6 pairs of 1-ft-wide parapet-return strips at the south recess corners (`FR_SOUTH_PNL1_S8` 3/4, 7/8, 11/12; `FR_EAST_BRK1_E1` 10/11, 18/19; `FR_WEST_PNL1_W1c` 6/7; 3.7–6.2 sq ft each) | the entrance-tower pairs are corrected in v011; the six small parapet-return strips are outside the entrance scope and are recorded as **F-9** (same defect class, not visible in the validation views; to be cleaned in a later facade pass) |
| Shell prisms | `BI_Z2_band_E_F2` (28.5–71 × 54.2–74.38 × 0–40) is closed and manifold (8 faces, 0 boundary edges); the south-wing Level 2 prism `BI_Z1_south_wing_L2` shares the plane x 28.5 for y 54.2–70.58, z 13.5–33.3 — coincident shell faces inside the union of the two zones, both covered by the finish region 0.03 ft in front | no visual effect (the FR panel is hit first and its light paths leave the wall outward); left untouched (approved v008 shell) and noted |

Category from the owner's list: **duplicate / coplanar faces in a facade finish region** (mesh defect). Not missing wall geometry, not a deleted face, not an open mesh, not a reversed normal (all normals −x), not backface culling, not an oversized cutter, not a missing finish region, not a material assignment failure, not glazing, and **not a documented recess**.

## 2. Source check — what the documents show for this face

The face in question is the **west face of the lobby tower** (the E–F.2 "band", grids 3–6 × D–F.2): plane x 28.50 (A1.01 / A1.02, v008 registration RMS 0.027 ft), y 54.2 (wing north wall, v008 G-9) to 74.38 (curtain-wall plane, v006), height 0–40 ft.

| Source (Rev 14 record set, 9/25/2025) | What it shows here |
| --- | --- |
| A1.01 Level 1 / A1.02 Level 2 building plans | the lobby west wall turns north at x 28.50 and runs straight from y 54.22 to the curtain wall at 74.13–74.54; Level 2 identical (v008 audit §G-9, G-11). No jog, no recess in this wall on either level |
| A1.00c / A1.03 roof plans | roof edge at the tower follows the same x 28.5 line (v008 audit: roof edge 54.07–54.35 for x 11.84–28.5, then north along x 28.5) |
| A4.02 West Elevation (raster, 144-dpi render, `scratchpad …/v5/west_elev_crop.png`) | the tower reads as **CW1 curtain wall from grade to its head, PNL1 above it continuously to the top of the tower**; tags PNL1 (tower), CW1, and the detail callouts B2/A7.26 (curtain-wall elevation) and A3/A7.21 (storefront elevations); **no opening and no material change between the CW1 head and the top**; the T.O.S. datum lines cross the tower |
| A7.26 Curtain Wall Elevations | CW1 = YKK YCW-750 OG (installed EFCO, closeout) — the curtain wall is the only opening in this face; head at 24.6 ft (v001 opening extraction, unchanged) |
| A5.18 A2 Wall Section @ entry (vestibule / F.2, `scratchpad …/v6/a518_vestibule_section.png`) | the tower wall is one plane from the floor to the parapet: curtain wall full height, roof deck at T.O.S. 30'-0", parapet wall continuing above it to the coping (detail A3/A5.24); 6'-11" above T.O.S. at this cut |
| A5.24 A3 Exterior Wall Section Details (parapet) | ACM parapet continues the wall plane above the roof deck (no step back at the roof line) |
| v001 datums (approved) | tower top 40.0 ft at x 30 sloping to 36.0 at x 71 (R, raster A4.01/A4.02); T.O.S. F 31'-6"; wing roof edge 33.3 |
| Closeout (Edifice 7/8/2026) | Alucobond PLUS ACM Bone White by Cynergy = PNL1 (v002 material register) |
| Photographs (validation only) | drone 2026-07-28 a/b and overview 2026-08-10: the entrance tower is a continuous white ACM face above the curtain wall, no dark recess, no opening |

Determination:
- **Recess depth of the "brick/upper-entry mass":** there is no recess in the tower's west face. The step the eye reads is the documented **17.8 ft** offset between the wing west face (x 10.67, brick / PNL1 above 33.3) and the tower face (x 28.5) at y 54.2, plus the tower standing 6.7 ft above the wing roof edge (40 vs 33.3). Both are unchanged v008 geometry.
- **Surface at the "back":** the tower face itself, a single plane at x 28.5.
- **Finish:** PNL1 Bone White ACM from the CW1 head (24.6 ft) to the top (40 ft at x 30, R); CW1 curtain wall below; no brick, no PNL2 on this face.
- **Vertical limits:** 24.6–40.0 ft (PNL1), 0–24.6 (CW1). **Horizontal limits:** y 54.2–74.38 (20.18 ft).
- **Openings:** none above the CW1 head.

## 3. History — where the defect came from

| Version | `FR_WEST_PNL1_W2b` | Visible? |
| --- | --- | --- |
| v005 (facade cleanup) | 2 faces: x 28.64, y 61.12–70.58, z 24.6–33.3 and x 28.7, y 70.58–74.38, z 24.6–32.6/32.8 — no overlap | no artifact |
| v006 (entrance correction) | 1 face: x 28.64, y 61.12–70.58, z 24.6–33.3 (the north part re-cut) | no artifact (the v006 entrance renders show a clean white tower) |
| **v008 (footprint correction)** | regions regenerated by `BI_build_footprint_fix_v008.py` with W2b extended to u0 54.2: **3 faces, face 0 (wing-L2 zone face, y 54.2–70.58, z 24.6–33.3) inside face 1 (lobby-band zone face, y 54.2–74.38, z 24.6–40)**, plus the buried face at x 70.97 | **yes** — `BI_footprint_v008_oblique_northwest.png` already shows the black patch on the tower (v008 used flat placeholder materials; self-occlusion is material-independent) |
| v009 (presentation) | geometry identical to v008 (hash) | yes (in `BI_presentation_v009_2_entrance_oblique.png`) |
| v010 (entrance site) | building / regions identical to v009 (hash) | yes (all v010 entrance views) |

Mechanism in the v008 builder (`BI_build_footprint_fix_v008.py` §"finish regions"): for every region it loops over *all* exterior zone faces of that facade direction and emits one panel per face that intersects the region rectangle. On the lobby-tower west plane two zone faces coincide — the lobby band's west face (0–40) and the south-wing Level 2 prism's west face (13.5–33.3, created by the v008 wing outline that ends at x 28.5 for y 54.2–70.58) — so the region was emitted twice. The same loop emitted the x 71 faces of the north block for y 70.58–74.38 although that strip is inside the band. v005 had no such coincidence because the wing north wall then sat at y 61.12 and the band started at 61.12 (no shared plane). **So the defect was introduced by the v008 region regeneration, not by v005, v006, v009 or v010; the wall geometry itself was never wrong.** It is a finish-region (mesh) error, not a material-assignment error: the material on both faces is the correct PNL1.

## 4. Decision

The documents establish one continuous PNL1 plane with no opening or recess (§2), so the correction is to remove the duplicate and buried faces of the two lobby-tower west-face finish regions (`FR_WEST_PNL1_W2b`, `FR_WEST_GLZ_W2`) and nothing else — Building I **v011** (`scripts\Building_I\BI_build_entrance_facade_fix_v011.py`, validation `BI_entrance_facade_validation_v011.md`). The v010 site correction is untouched. F-9 (six parapet-return strips of the same class elsewhere) is carried forward.
