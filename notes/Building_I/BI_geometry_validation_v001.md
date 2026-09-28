# Building I — geometry baseline v001: validation and completion report

Date: 2026-09-22
Model: `models\Building_I\BI_shell_v001.blend` (449 objects) built by `scripts\Building_I\BI_build_shell_v001.py` from `notes\Building_I\BI_geometry_data_v001.json`; control document `BI_geometry_control_v001.md`; build report `BI_shell_v001_build_report.json`.
Status: **built and validated, NOT approved.** Stopped at the geometry approval gate (skill gate 2).

## 1. What was created

| Output | Content |
| --- | --- |
| `models\Building_I\BI_shell_v001.blend` | Collections `01_Shell` (7 zone prisms), `02_Parapet_screens` (9 strips), `03_Canopy` (7 columns, gutter beam, 2 glass wings), `04_Openings` (376 flush glazing placeholders), `05_Grid_control` (39 grid bars), `06_Reference` (Level 2 slab, grade plane at 660), `90_Cameras` (5 cameras, sun). Neutral clay materials only. |
| `renders\Building_I\BI_shell_v001_front_north.png` | Front = north face (orthographic) |
| `…_rear_south.png`, `…_left_west.png`, `…_right_east.png` | Orthographic elevations |
| `…_oblique_northwest.png` | Perspective from the north-west |
| `notes\Building_I\BI_shell_v001_build_report.json` | Extents, per-zone bounding boxes, counts, render times |
| `scripts\Building_I\BI_extract_tools_v001\` | The vector/raster extraction tools used for the control document (SVG segment extractor, grid-line matcher, slab-clip union, raster skyline, glazing detector) |
| `notes\Building_I\manifests\` + `scripts\Building_I\BI_freeze_manifest_longpath_v001.py` | Freeze manifests (see §3) |

## 2. Overall modeled dimensions vs source

| Check | Modeled | Source | Δ | Code |
| --- | ---: | ---: | ---: | --- |
| Shell X extent | 280.12 ft (x 6.88 → 287.00) | Slab-edge union A1.00a/A1.00b | 0.00 | V |
| Shell Y extent | 207.26 ft (y −4.38 → 202.88) | same | 0.01 | V |
| Grid 1 → 14 | 280.00 | S101 written strings | 0.00 | W |
| Grid A → N | 198.53 | S101 chain (F→G measured) | 0.02 vs vectors | W/V |
| Highest element | 40.10 (mechanical screen) | 40.0 max height from fenestration calcs; screen 40.1 raster | 0.1 | I/R |
| North block cornice at N | 39.59 | raster 39.1–40.2 | within | R |
| North block cornice at F | 32.62 | raster 33.13 at G, T.O.S. F 31.5 | 0.5 | R |
| East strip top at K.7 | 37.42 | raster 36.5–37.1 at L.6 region | 0.3 | R |
| South wing parapet | 33.30 | raster 33.30–33.32 (three elevations) | 0.0 | R |
| PNL1 screen, south face west end | 40.00 | A5.24 10'-0" above T.O.S. A = 40.0 | 0.0 | W |
| 13–14 end block | 32.00 | raster 32.04 / 32.08 | 0.1 | R |
| Level 2 slab top | 15.333 | LVL-02 15'-4" | 0.0 | W |
| Canopy | x −13.0 → 65.0 (78.0), gutter 13.021 on G.2, wings 16.375 / 6.1875 | A1.13 78'-0", Mezzanine datum, 16'-4 1/2", 6'-2 1/4" | 0.0 | W (position V) |
| Mechanical screen | 90.0 × 40.5 | A1.03 90'-0" × 40'-7" | 0.08 | W |
| Vestibule 100 | 24.0 × 9.04 | A1.13 24'-0"; F.2→G.2 | 0.0 | W/V |

Written façade totals on the elevations (not bounding boxes): south 273'-8 1/2" vs modeled south-face run 6.88 → 281.0 = 274.1 ft (Δ 0.4 ft, façade-segment definition uncertain); north 271'-0" vs 6.88 → 281.0 (west end of the wing's north face to the east face) = 274.1 ft (Δ 3.1 ft — the printed total likely excludes the 13–14 block or starts at the band; flagged); east 198'-1" vs −4.38 → 198.5 = 202.9 ft including the lab projection, 198.5 excluding it (Δ 0.4 ft). These are consistency indicators only; the slab-edge vectors govern.

## 3. Frozen baseline and source integrity

| Manifest | Before build | After build |
| --- | --- | --- |
| `BI_freeze_project_and_BuildingII_v001.json` — every pre-existing project file (Building II models, scripts, notes, renders, exports, viewers, tenant test fits, `source_documents\Building II`, AGENTS.md; 311 files) | PASS 311 unchanged | PASS 311 unchanged |
| `BI_freeze_sources_BuildingI_v001.json` — Building I sources reachable within the 260-character path limit (1,072 files) | PASS 1,072 unchanged | PASS 1,072 unchanged |
| `BI_freeze_sources_BuildingI_longpath_v001.json` — all 1,231 Building I source files via extended-length paths (created after the build) | — | PASS 1,231 files present, total 6,929,037,544 bytes = exactly the pre-modeling inventory count and size of 2026-09-22 |

No Building II file was opened, read or modified during this pass. No source file was modified. All new files are under `notes\Building_I`, `scripts\Building_I`, `models\Building_I`, `renders\Building_I` with the `BI_` prefix (full list in §8). Existing Building I review files (`BI_source_inventory_v001.md`, `BI_revision_review_v001/v002.md`, TSV tables, inventory script) are unchanged (they are inside the 311-file manifest).

## 4. Registration and dimensional checks performed

- Sheet scale: 6.7500 ± 0.0004 pt/ft on A1.00a, A1.00b, A1.01, S101 (grids 2 → 9 = 137.667 ft written).
- S101 vector grid lines reproduce every written X string within 0.02 ft; Y lines match the written chain within 0.05 ft.
- Elevation datum lines (vector) at 9.000 pt/ft: LVL-02 138.0 pt above LVL-01 = 15.333 ft; T.O.S. N 335.6 pt = 37.29 ft (both exact).
- Level 1 and Level 2 slab-edge polygons registered independently to grids 2/9/N on their own sheets; their union closed without gaps except the unhatched E–F.2 corridor band, added from A1.01 wall lines (x 28.75/29.25 and 71.0/72.0 walls, y 61.5 and 73.8/74.3 walls).
- Reopened the saved .blend in a separate Blender session: 449 objects, zone bounding boxes equal to the build-session report; top-of-wall samples: north block 39.59 at N, 32.62 at F, east strip 37.42 at y 160.4.
- Build-time assertions: X extent 280.12, Y extent 207.25, highest element 40.1 (all passed).

## 5. PCOs / post-record documents: applied or rejected

None applied. CONT 8 (rooftop screen cladding), PCO 50 (canopy footing drainage/grading), PCO 29/30/54 (lobby stair), PCO 24 (retaining wall/drainage), interior PCOs and signage packages were reviewed and rejected for this pass because none states a dimensioned final exterior geometry (control document §10).

## 6. Documented facts vs measured / interpreted / assumed

- Written (W): grids (X complete, Y except F→G), level datums, T.O.S. datums, canopy dimensions and slope, mechanical screen size, vestibule width, max height (via fenestration calcs).
- Vector-measured (V): footprint polygon (slab edges), F→G 9.945, minor grids F.2/G.1/G.2/K.1, canopy and screen positions, band wall faces.
- Raster-measured (R, ±0.15 ft): every parapet / cornice top, screen-wall profile, all 376 glazing lites, vestibule glazing head.
- Interpreted (I): roof planes linear between datums; cornice formula; 40.0 max height.
- Assumed (A): vestibule roof 9.0; canopy column height 13.0 and 8" size; Level 2 slab over the whole south wing; 1 ft screen thickness; mechanical screen bottom 31.0; flat grade at 660.

## 7. Unresolved items (carried from the control document)

C-1 F→G not written; C-2 structural "H" vs architectural "H.1"; C-3 canopy north edge H.1 (section) vs J (plan); C-4 south-face screen vs mechanical screen overlap on the raster; C-5 band top vs cornice formula near grid 6/7; C-6 no Building I civil drawings, flat grade only; C-7 no county-stamped set; C-8 PCO 24 unreadable file name. Plus the north façade total (271'-0") not reproduced (§2).

## 8. Files created in this pass

```
models/Building_I/BI_shell_v001.blend
notes/Building_I/BI_geometry_control_v001.md
notes/Building_I/BI_geometry_data_v001.json
notes/Building_I/BI_geometry_validation_v001.md
notes/Building_I/BI_shell_v001_build_report.json
notes/Building_I/manifests/BI_freeze_project_and_BuildingII_v001.json
notes/Building_I/manifests/BI_freeze_sources_BuildingI_v001.json
notes/Building_I/manifests/BI_freeze_sources_BuildingI_longpath_v001.json
renders/Building_I/BI_shell_v001_front_north.png
renders/Building_I/BI_shell_v001_rear_south.png
renders/Building_I/BI_shell_v001_left_west.png
renders/Building_I/BI_shell_v001_right_east.png
renders/Building_I/BI_shell_v001_oblique_northwest.png
scripts/Building_I/BI_build_shell_v001.py
scripts/Building_I/BI_freeze_manifest_v001.py, BI_validate_manifest_v001.py (skill copies)
scripts/Building_I/BI_freeze_manifest_longpath_v001.py
scripts/Building_I/BI_extract_tools_v001/{svgseg,words,gridlines2,slabpoly,slabunion,rskyline,glass}.py
```

## 9. Readiness for approval

The baseline is ready for the owner's geometry-gate decision as a **massing / dimensional-control model**: grids, footprint, levels, roof datums and the overall silhouette are traceable to written or exact-vector values; parapet tops and openings are raster-measured and labelled so. It is not yet a faithful façade: parapet screens are simplified strips, translucent wall panels are absent, openings are flush placeholders, and the entry vestibule roof height is an assumption. Recommended decision: approve as the frozen dimensional baseline (v001), then open the façade/material gate, where the raster-derived items are re-checked against the storefront elevations A7.21–A7.28 and the wall sections.

Next single decision for the owner: **approve or redirect the v001 geometry baseline.**
