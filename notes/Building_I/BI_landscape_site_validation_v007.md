# Building I — landscape / site coordination cleanup v007: validation and completion report

Date: 2026-09-22
Model: `models\Building_I\BI_landscape_v007.blend` (779 objects = 729 from the approved v006 + 50 landscape objects), built by `scripts\Building_I\BI_build_landscape_cleanup_v007.py` from `BI_landscape_data_v007.json`. Control document: `BI_landscape_site_coordination_control_v007.md`. Build report: `BI_landscape_v007_build_report.json`. Comparison: `BI_compare_geometry_v006_v007.py`.
Status: **built and validated, NOT approved.** v001–v006 remain frozen (101 files, manifest PASS).

## 1. Results by target issue

| Issue | Before (v006) | After (v007) | Basis |
| --- | --- | --- | --- |
| A. Foundation planting vs footprint | 84 plants pushed 1–9.9 ft outward to clear the v001 shell | 31 plants (8 DAZA wing-north row; 12 ABKA, 8 CORA, 3 BUNN north-east notch bed) **returned to their documented positions** (hidden inside the approved shell until G-9/G-10 are resolved); 53 south-face / entrance-band plants stay pushed ≤ 5 ft (G-8 tolerance); building not moved | A1.00a / A1.01 registered wall and slab lines (wing north wall y ≈ 52.75, NE notch x ≈ 268.9) agree with the landscape sheets, not with v001 |
| B. Species-unresolved symbols | 121 symbols; EMRA 0/37 | **117 symbols; EMRA 37/37** (4-ft circle chains at both EMRA leaders), LOJA +2 and ABFR +2 by adjacency with schedule headroom; signature matching rejected (7 % accuracy) | LP-100 leaders + symbol size (I); adjacency (I) |
| C. Ground-cover beds | 11 interpreted discs, 7 skipped | unchanged; bed lines on LP-101 are open tan polylines, not closed bed polygons → discs stay `_INTERPRETED`, the 7 hardscape-conflict callouts stay unresolved and unmodeled | LP-101 line-style test |
| D. Parking / islands | APPROX rectangle, 17 islands (V) | unchanged; LP-100 curb-line trace leaks into the perimeter lawn at the drive entrances (clipped fill 106,955 sq ft is not a curb polygon) → SC-3 stays open | LP-100 vector test |
| E. Street trees | Golf Links Dr 14 + Midway Park Dr 8 modeled; N Rea Park Ln / N Old Springs Rd photo-only | **+18 N Rea Park Ln (photo-confirmed) and +24 N Old Springs Rd (not photo-verified)** existing-tree symbols from the Building II LP-100 rev 2, registered on the 17 shared parking islands (2.40 pt/ft, ≤ 1.5 ft); LC-4 closes; no photo-only trees added | shared-street register entry |
| F. Site details | dumpster brick U; wall bottom A; bed edges I; islands V | dumpster stays U (A0.04 Roman vs PCO 14 building brick, no closeout record); landscape wall exposed height 1.6 ft documented from CX-104 + CG-101 (bottom unchanged, below grade); bed edges unchanged (I); islands unchanged (V) | A0.04, PCO 14, CX-104, CG-101 |

Plant totals: 608 placed (V 383, V-I 143, I 82) + 117 species-unresolved symbols; 42 context street trees added (64 existing street trees total).

## 2. Objects changed (v006 → v007, comparison script)

- Changed (11, all landscape): `LS_shrub_DAZA_LP-101_n12`, `LS_shrub_ABKA_LP-101_n14`, `LS_shrub_BUNN_LP-101_n15`, `LS_groundcover_CORA_LP-101_n5`, `LS_groundcover_CORA_LP-101_n6`, their five `LS_mulch_*` discs, `LS_shrub_UNRESOLVED_species_documented_symbol`.
- Added (50, all landscape): `LS_shrub_EMRA_LP-100_n26`, `LS_shrub_EMRA_LP-100_n11`, `LS_shrub_ABFR_LP-100_n0_adj`, `LS_shrub_LOJA_LP-101_n0_adj` and their mulch discs; `CTX_existing_street_tree_N_Rea_Park_Ln_01…18_BII-LP100`, `CTX_existing_street_tree_N_Old_Springs_Rd_01…24_BII-LP100`.
- Removed: none. Changed/added/removed outside the landscape collections: **none**.

## 3. Validation

| Check | Result |
| --- | --- |
| Hash of every mesh object except the 11 rebuilt landscape objects (703 objects: shell, facade regions, openings, canopy, site, remaining landscape) before/after | identical (`80ed4bb3…f410`) |
| `BI_compare_geometry_v006_v007.py` | building identical, facade regions identical, openings identical, entrance correction identical (Z4b, band, vestibule, all north openings), site identical; changes confined to 11 landscape objects, 50 landscape objects added |
| `BI_freeze_BuildingI_v006_approved.json` (101 files: all v001–v006) | PASS |
| `BI_freeze_project_and_BuildingII_v001.json` (311) | PASS |
| `BI_freeze_sources_BuildingI_longpath_v001.json` (1,231 source files) | PASS |
| Renders inspected | front north elevation, entrance oblique, north-west site oblique, elevated site view, landscape entry view, rear/south comparison: street trees now line N Rea Park Ln; entrance and facade unchanged |

## 4. Remaining site / landscape conflicts (carried forward)

- G-8 south wing slab edge vs wall lines (53 plants remain pushed ≤ 5 ft); **G-9** wing north wall at grids 1–3 (8 DAZA hidden in the shell); **G-10** north-east corner notch (23 plants hidden in the shell) — owner/architect decisions on v001 geometry.
- 117 species-unresolved symbols (mostly parking-lot beds: ABFR 79/114, VIBL 36/96, JEWL 40/88, BUNN 3/42, BLON 3/28, DOUB 5/16, COFA 5/10, LACE 9/10; 13 unattributed 4-ft circles along the wing west face).
- Ground-cover extents interpreted (11 discs); 7 hatched ground covers not modeled.
- SC-1 dumpster brick; SC-3 parking-lot outline approximate (islands exact); LC-2 Building I vs Building II lot quantities; N Old Springs Rd trees not photo-verified; vestibule height 9.0 ft (A-1); all v001 G-items, v002 material placeholders, v003 SC-items, v004 LC-items and v005 F-items otherwise unchanged.

## 5. Files created in this pass

```
models/Building_I/BI_landscape_v007.blend
notes/Building_I/BI_landscape_site_coordination_control_v007.md
notes/Building_I/BI_landscape_data_v007.json
notes/Building_I/BI_landscape_v007_build_report.json
notes/Building_I/BI_landscape_site_validation_v007.md
notes/Building_I/manifests/BI_freeze_BuildingI_v006_approved.json
renders/Building_I/BI_landscape_v007_{front_north_elevation,entrance_oblique,oblique_northwest,site_elevated,landscape_entry,rear_south}.png
renders/Building_I/BI_landscape_v007_comparison_rear_south.png
scripts/Building_I/BI_build_landscape_cleanup_v007.py
scripts/Building_I/BI_compare_geometry_v006_v007.py
```

## 6. Readiness

The landscape/site baseline is ready for the owner's decision as a **documented, coordination-checked layout**: every open item is either resolved with a cited source or carried forward with a code; nothing was redesigned and no plant was moved for appearance. The items that need the owner or architect are the three v001 footprint questions (G-8/G-9/G-10), which govern where 84 foundation plants meet the wall, and the remaining species shortfalls that the drawings cannot settle without the landscape CAD or a planting as-built.

Next single decision for the owner: **approve or redirect the v007 landscape/site baseline.**
