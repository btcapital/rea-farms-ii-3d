# Building I — landscape / immediate-context baseline v004: validation and completion report

Date: 2026-09-22
Model: `models\Building_I\BI_landscape_v004.blend` (2,247 objects = 2,052 from the approved v003 file + 195 new), built by `scripts\Building_I\BI_build_landscape_v004.py` from `BI_landscape_data_v004.json` on top of the approved `BI_site_v003.blend`. Control document: `BI_landscape_control_v004.md`. Build report: `BI_landscape_v004_build_report.json`.
Status: **built and validated, NOT approved.** Stopped at the landscape/context approval gate.

## 1. What was created

| Output | Content |
| --- | --- |
| `models\Building_I\BI_landscape_v004.blend` | v003 building + site unchanged + collection `09_Landscape_v004` (trees 35, shrub groups 37, ground-cover groups/discs 29, mulch discs + islands 71, context trees 22) + camera `BI_cam_landscape_entry` |
| `renders\Building_I\BI_landscape_v004_front_north.png`, `_rear_south.png`, `_left_west.png` (Building II mass hidden), `_right_east.png`, `_oblique_northwest.png`, `_site_elevated.png`, `_landscape_entry.png` | seven views, neutral lighting |
| `notes\Building_I\BI_landscape_control_v004.md`, `BI_landscape_data_v004.json`, `BI_landscape_v004_build_report.json` | control, data (schedules + every plant position with confidence code), report (incl. every plant shifted out of the footprint and every disc skipped) |
| `scripts\Building_I\BI_build_landscape_v004.py`, `BI_compare_geometry_v003_v004.py` | build, independent object comparison |

## 2. Landscape sources found

- **Building I landscape plans exist only as bulletin copies inside PCO 24 (RFI 78, 07.29.25):** LP-100 Overall Landscape Plan (p.12, 1" = 30') and LP-101 Landscape Plan – Building (p.13, 1" = 20'), both V3 project 230959, revision 13 "Site Furnishings RFI" 07.22.25, with full plant schedules, quantity callouts, plant symbols, planting notes and a lighting schedule. The Rev 14 cover lists C-LP-100/101 but neither combined set binds them.
- Supporting Building I: PCO 34 landscape lighting allowance (20 path lights, 10/28/2025); PCO 17 CS-101 (site furnishings); RFI 78 text (bike lockers/racks).
- Shared-site register (Building II): LP-100 rev 2 (12.12.25) and LP-101 rev 1 (11.06.25) in `APPROVED-LDCP-2025-00715.pdf` p.12–13; 03.17.26 civil cover p.5; infrastructure bulletin 2026-5-14 (grading only — no planting plan).
- Not found: LDCP-2025-00064 (Building I), Rea Farms Major Infrastructure Plans Phase 2 (street trees on N Rea Park Ln / N Old Springs Rd), irrigation plan, landscape as-built or closeout planting record.
- Photos used for validation only: 2026-07-28 drone 0045 and 0053, 2026-08-10 overview.

## 3. Planting added

| Group | Count | Basis |
| --- | --- | --- |
| Trees (new) | 35: WILO 22, LACE 9, BUTT 2, STAR 2 | symbol positions V, species by leader V |
| Shrubs (species resolved) | 393 in 37 callout groups (ABKA 46, LOJA 93, ABFR 77, JEWL 40, VIBL 36, GATE 19, JADE 18, LOPE 13, DAZA 12, FOAR 8, RHCO 7, COFA 5, DOUB 5, CASL 4, ILST 4, BLON 3, BUNN 3) | positions V; species V 250 / V-I 102 / I 41 |
| Ground-cover plants drawn as symbols | 139 (CORA 27, LAMB 25, CARZ 18, JUNE 17, CATM 13, VANG 12, RUSS 9, OSOR 8, CARE 6, SNOW 4) | V / V-I |
| Ground-cover discs (hatched beds) | 11 modeled, 7 skipped (centre on a walk/plaza surface) | **I** — area = quantity × spacing² at the leader tip |
| Species-unresolved symbols | 121 (92 LP-100, 29 LP-101) as neutral shrubs | position V, species U |
| Mulch | one disc (r 1.6 ft) under every documented plant | I (bed outlines not modeled) |
| Parking islands | 17 raised mulch ovals 37 × 10 ft | LP-100 V |
| Existing street trees (context) | 22 (14 Golf Links Dr, 8 Midway Park Dr) | position V, size I |

Totals: 567 plants placed of 1,474 scheduled (859 + 615); the balance is 121 unresolved symbols, 540 hatched ground-cover plants represented by area (11 discs = 396 plants' worth modeled, 7 discs = 152 plants' worth skipped), and 37 EMRA + parts of ABFR/VIBL/JEWL/BUNN/BLON/DOUB/COFA whose symbols are among the unresolved set (§6 LC-3 of the control document).

## 4. Exact vs interpreted

- **Exact (V):** every plant symbol position (±1.5 ft registration), species for 383 plants (leader fully resolved), island geometry, existing-tree positions, all schedule data.
- **Partly interpreted (V-I / I):** species for 184 plants where the leader group was short or found in a second pass; sizes of all vegetation; mulch discs; 6-in island height.
- **Interpreted (I):** ground-cover disc extents and positions; existing-tree size.
- **Unresolved (U):** species of 121 drawn symbols; EMRA (0/37) not isolated.
- **Shifted (documented, LC-1):** 84 foundation plants pushed 1.2–9.9 ft outward because the civil/landscape building outline sits inside the approved v001 slab-edge polygon (south y ≈ −1.2 vs −4.38; east x ≈ 281 vs 287). Building not moved. Each shift is listed in the build report.

## 5. Shared-site sources used (register)

| Sheet | File / page | Printed status | Used for |
| --- | --- | --- | --- |
| LP-100 Overall Landscape Plan rev 2 (Carolina Sports MOB) | `source_documents\Building II\00 PLANS\Approved Civil\APPROVED-LDCP-2025-00715.pdf` p.12 | 12.12.25, city final approval 1/9/2026 | comparison of the shared parking-lot schedule (LC-2); existing-tree counts on Golf Links Dr / Midway Park Dr; not used for any Building I plant position |
| LP-101 Landscape Plan – Building rev 1 (Bldg II) | same file p.13 | 11.06.25 | reviewed for the plaza strip; Building II beds not modeled |
| CO-100 cover / sheet index rev 6 | `…Revision 5\Rea Farms 2 - Civil Drawings 03.17.26.pdf` p.5 | 03.10.26 | latest Building II landscape issue confirmation |
| Rea Farms Infrastructure Extension bulletin | `Building II\00 PLANS\APPROVED Bulletin_…2026-5-14.pdf` | 5/14/2026 | checked for street-tree plan; grading only |

No Building II architectural document was used; no Building II model, script, note, render or export was opened.

## 6. Unresolved landscape / site conflicts

LC-1 building outline vs approved footprint (owner/architect question on the −4.38 slab edge); LC-2 Building I vs Building II parking-lot schedules; LC-3 species-unresolved symbols and EMRA; LC-4 N Rea Park Ln / N Old Springs Rd street trees undocumented; LC-5 hatched bed extents interpreted; LC-6 no landscape as-built; LC-7 plaza strip beds (Building II scope). Carried forward unchanged: G-1…G-6, v002 material placeholders, SC-1…SC-5 including the simplified north parking-lot rectangle (islands now sit on it as landscape objects) and the absence of a sealed Building I civil set.

## 7. Validation

| Check | Result |
| --- | --- |
| v003 vertex + material-slot hash before/after the landscape pass (2,044 mesh objects, inside the build) | identical (`e7fc1b97…cf033`) |
| Independent comparison `BI_site_v003.blend` vs `BI_landscape_v004.blend` (`BI_compare_geometry_v003_v004.py`) | 2,044/2,044 mesh objects present, 0 vertex / material / collection / visibility changes; 195 objects added, all `LS_`/`CTX_` inside `09_Landscape_v004` plus camera `BI_cam_landscape_entry` in `90_Cameras` |
| `BI_freeze_BuildingI_v003_approved.json` (56 approved v001–v003 files) | PASS |
| `BI_freeze_project_and_BuildingII_v001.json` (311 pre-existing project + Building II files) | PASS |
| `BI_freeze_sources_BuildingI_longpath_v001.json` (all 1,231 Building I source files) | PASS |
| Renders inspected | seven views; islands, lot trees, perimeter and foundation beds, street trees read correctly; vegetation is simple clay-like geometry; the v003 terrain bumps at the drop-off curb pairs remain (approved v003, untouched) |

## 8. Files created in this pass

```
models/Building_I/BI_landscape_v004.blend
notes/Building_I/BI_landscape_control_v004.md
notes/Building_I/BI_landscape_data_v004.json
notes/Building_I/BI_landscape_v004_build_report.json
notes/Building_I/BI_landscape_validation_v004.md
notes/Building_I/manifests/BI_freeze_BuildingI_v003_approved.json
renders/Building_I/BI_landscape_v004_{front_north,rear_south,left_west,right_east,oblique_northwest,site_elevated,landscape_entry}.png
scripts/Building_I/BI_build_landscape_v004.py
scripts/Building_I/BI_compare_geometry_v003_v004.py
```

## 9. Readiness

The landscape/context baseline is ready for the owner's gate decision as a **documented planting layout**: every modeled plant stands on a drawn symbol from Building I's own LP-100/LP-101, species and quantities come from the printed schedules and callouts, and every interpreted element carries `_INTERPRETED`, `UNRESOLVED` or a confidence code. Its limitations are the 121 species-unresolved symbols (mostly parking-lot shrubs and EMRA), the interpreted ground-cover extents, the undocumented street trees on N Rea Park Ln / N Old Springs Rd, simple vegetation geometry, and the LC-1 footprint question that affects where the foundation beds meet the wall. Recommended next step after approval: freeze v004; obtain LDCP-2025-00064 / the V3 landscape CAD to resolve the unresolved symbols and bed outlines, and put LC-1 to FMK.

Next single decision for the owner: **approve or redirect the v004 landscape/context baseline.**
