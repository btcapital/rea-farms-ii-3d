# Building I — interior base-building framework v014: validation and completion report

Date: 2026-09-25
Model: `models\Building_I\BI_interior_base_v014.blend` (853 objects = 818 of v013 + 28 interior mesh objects + 7 validation cameras; 4.6 MB), built by `scripts\Building_I\BI_build_interior_base_v014.py` from `BI_interior_base_data_v014.json` on `BI_presentation_v013.blend`. Control: `BI_interior_base_control_v014.md`. Build report: `BI_interior_base_v014_build_report.json`. Viewer data: `BI_interior_base_viewer_v014.json`. Overlays: `BI_interior_base_overlays_v014.py`.
Status: **built and validated, NOT approved.** v001–v013 frozen (`manifests\BI_freeze_BuildingI_v013_approved.json`, 244 files, PASS after this pass).

## 1. Collections (as required)

```
Building_I
  BASE_BUILDING            24 objects in BB_10_slabs … BB_17_roof_deck_underside
  EXISTING_TENANT
    CNSA                   4 objects (CNSA_L1_partitions, CNSA_L2_partitions, CNSA_tenant_zones)
  FUTURE_CONCEPTS
    Concept_A / Concept_B / Concept_C   empty (asserted)
```
No `BB_*` object is in EXISTING_TENANT, no `CNSA_*`/`TENANT_*` object is in BASE_BUILDING (asserted). The seven interior cameras are in `90_Cameras`.

## 2. Exterior integrity (asserted in the build script; every check must pass or the script aborts)

| Check | Result |
| --- | --- |
| Every one of the 818 v013 objects: world-space vertices, transform, collections, render/viewport flags, per-face material indices, material slots | **identical** (per-object hash before / after, re-checked after rendering) |
| The 32 v013 material node trees | identical (0 changed); 11 materials added (`BB_*`, `TENANT_*`) |
| Existing collections (flags and children) | identical |
| Exterior openings | none moved (the interior only reads their bounding boxes) |
| All new objects inside `Building_I/*` or `90_Cameras` | asserted |
| `BI_freeze_BuildingI_v013_approved.json` (244), `BI_freeze_BuildingI_v012_approved.json` (224) | PASS |
| `BI_freeze_sources_BuildingI_longpath_v001.json` (1,231) | PASS — `source_documents` unchanged |

## 3. Areas (modeled vs published; not forced)

| Quantity | Modeled | Published | Difference / note |
| --- | --- | --- | --- |
| Level 1 gross (v008 envelope = slab on grade) | 45,091 sq ft | — | |
| Level 1 inside the exterior walls | 43,937 sq ft | — | wall-type thickness deducted along the 99 exterior faces |
| Level 2 slab (A1.00b hatch) | 24,095 sq ft | — | |
| Mezzanine slab (233) | 1,423 sq ft | — | |
| **Total L1 + L2 + mezzanine** | **70,608 sq ft** | **70,967 sq ft** (G0.01 total building area) | **−359 sq ft (−0.5 %)**: the code figure is to the outside face with the canopy/overhang conventions of the code plan; not reconciled |
| L1 core zones (bounding boxes of the fixed rooms) | 4,294 sq ft | Jays: lobby+corridor 3,400, RR 500, south stair 135 | different basis (bounding zones vs net rooms) |
| Courts 121 open floor | ≈ 17,160 sq ft | Jays "courts and turf track ±17,200" | agrees |
| CNSA L1 tenant zone (MOB Shell 150-S) | 16,216 sq ft | — | the whole shell south of corridor 102 |
| CNSA L2 tenant zone | 10,846 sq ft | — | x 11.3–185 of MOB Shell 250-S |
| MOB Shell 250-S remaining (SHELL 2300) | 5,371 sq ft | — | available for a future concept |
| Level 2 FMK program (Taylor Capital suite etc.) | — | Jays: office 3,760, corridor 2,430, gallery/stairs 1,225+1,460 | recorded, not re-measured |

No BOMA or lease area document was found in the source folders; the check is against the code summary and the owner's janitorial SF plans only.

## 4. Height checks

| Item | Value | Code |
| --- | --- | --- |
| LVL-01 / Mezzanine / LVL-02 | 0 / 13.021 / 15.333 | W |
| Stairs arrive at | lobby 15.328, south 15.328, gallery 15.328 (27 × 6 13/16" = 15.328 vs LVL-02 15.333: 1/16 in), mezzanine E/W 13.057 (23 risers vs 13.021: 7/16 in) | W counts |
| Elevator | pit −5.0, hoistway top 33.0, inside 8.67 × 7.04 | W / V |
| Roof T.O.S. plates | 30.0 (A) → 31.5 (F) wing; 31.5 → 37.29 (N) north block; 28.0 end block; 27.33 bay; 9.0 vestibule | W datums, I linear |
| Clear heights | see control §5 (L1 13.5–13.6 to structure; L2 12.7–14.2; courts ≈ 27–31 M; training ≈ 30 M; ceilings 8'-0"–11'-8" W) | |

## 5. Structural constraints modeled / recorded

Modeled: 84 columns (S601), elevator hoistway and pit, 5 stairs, core walls to deck, slabs with their openings (lobby double-height, courts, training area, stair wells, hoistway), roof T.O.S. plates. Recorded only: braced frames (S401–S403 members; bays from A5.01), beam depths (S102/S103) as clear-height ranges, plumbing stacks (not extracted — P1.01/P1.02 not used this pass).

## 6. Validation views (`renders\Building_I\`)

| View | File | Engine |
| --- | --- | --- |
| 1 Level 1 top-down cutaway (cut at 10 ft; L2 objects and roof plates hidden) | `BI_interior_base_v014_1_L1_plan_cutaway.png` | Workbench |
| 2 Level 2 top-down cutaway (cut at 26 ft) | `_2_L2_plan_cutaway.png` | Workbench |
| 3 longitudinal section (y = 30, looking north) | `_3_longitudinal_section.png` | Workbench |
| 4 transverse section (x = 95.5 through the hoistway, looking east) | `_4_transverse_section.png` | Workbench |
| 5 lobby / core perspective | `_5_lobby_core.png` | Cycles |
| 6 courts interior toward the mezzanine | `_6_courts_interior.png` | Cycles |
| 7 structure / core oblique (shell, liner and roof plates hidden) | `_7_structure_core_oblique.png` | Cycles |
| Overlays vs the controlling plans | `_overlay_L1_A1.01.png`, `_overlay_L2_A1.02.png` | render at 55 % over the registered Rev 14 plan |

Render mechanics: the exterior shell prisms, parapet screens, facade regions and canopy collections are hidden by collection flag for the interior views only (restored before saving; object flags are hashed); the opaque lite placeholders are hidden in the Cycles views so daylight enters through the apertures; Workbench views use Standard/exposure 0, Cycles interiors AgX −1.3 (v013's −4.35 restored in the saved file). The interiors are unlit spaces lit by daylight through the apertures only, so they read dark by design; no interior lighting was added. Overlay findings: wall rectangles sit on the drawn walls on both levels; the elevator, stairs, cores and the CNSA zone match; the Level 2 slab edge follows A1.00b (lobby double-height, courts and training-area openings, mezzanine, gallery).

## 7. Readiness for a first tenant test fit

Ready, with these caveats: the model gives fixed slabs, columns, cores, stairs, elevator, exterior wall inner faces with apertures, clear heights and the existing CNSA extent, all in Building I coordinates, with `BI_interior_base_viewer_v014.json` holding the levels, columns, shafts, stairs, fixed rooms, tenant zones and constraints for the future viewer. A test fit should be registered against the corridor 202 south wall / exterior inner faces / columns (not against the CNSA walls), placed in `FUTURE_CONCEPTS/Concept_A`, and must not move anything in BASE_BUILDING. Items I-1…I-4 (control §7) should be confirmed before areas are quoted from the model.

## 8. Files created in this pass

```
notes/Building_I/BI_interior_base_control_v014.md
notes/Building_I/BI_interior_base_data_v014.json
notes/Building_I/BI_interior_base_v014_build_report.json
notes/Building_I/BI_interior_base_viewer_v014.json
notes/Building_I/BI_interior_base_validation_v014.md
notes/Building_I/manifests/BI_freeze_BuildingI_v013_approved.json
notes/Building_I/manifests/BI_freeze_BuildingI_v014_pending_approval.json
scripts/Building_I/BI_build_interior_base_v014.py
scripts/Building_I/BI_interior_base_overlays_v014.py
models/Building_I/BI_interior_base_v014.blend
renders/Building_I/BI_interior_base_v014_{1_L1_plan_cutaway,2_L2_plan_cutaway,3_longitudinal_section,4_transverse_section,5_lobby_core,6_courts_interior,7_structure_core_oblique,overlay_L1_A1.01,overlay_L2_A1.02}.png
```

Next decision for the owner: **approve or redirect v014** (then freeze v001–v014). Not started: tenant concepts, browser viewer.
