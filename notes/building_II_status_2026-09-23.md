# Building II — project status and approved baselines (closeout 2026-09-23)

**CURRENT APPROVED BUILDING II MODEL: v023** — `models/building_shell_v023.blend` (built by `scripts/build_shell_v023.py`; report `notes/building_shell_v023_build_report.json`; control `notes/lobby_refinement_control_v023.md`; comparison `notes/interior_comparison_v021_to_v023.md`). SHA-256 `7fe33f1e4dc906c75b54122203fec75ee9ef948be70897e46fcfd1b288235c91`.

**CURRENT APPROVED BUILDING II VIEWER: v026** — folder `viewer_v026/` (port 8026, launch with `viewer_v026\start_viewer.bat`), export `exports/building_II_model_v023_viewer_v026.glb` (identical copy in `viewer_v026/models/`), data `viewer_v026/assets/viewer_data_v026.json`, export script `scripts/export_viewer_v026.py`, control `notes/browser_viewer_control_v026.md`. GLB SHA-256 `bc24b1edb000b67df166bfc5a6a9bc661ff060073ab0135de6e7281fd34f2782`.

**Lobby phase: COMPLETE / APPROVED.** Model v023 contains the approved architectural lobby (v019 Pass 1), the approved Pass 2 FF&E (v021) and the approved visual refinement (v023). Viewer v026 shows it with the approved v020 navigation framework (walkable Stair 1, furniture collision, Lobby / Base / Concept controls, six lobby viewpoints). No further lobby or viewer change is to be made unless specifically requested.

Freeze manifest for this state: `notes/freeze_manifest_2026-09-23_model_v023_viewer_v026.sha256` (every Building II project file of v001–v026; verify with `sha256sum -c`).

## Version ledger (all preserved, nothing deleted)

| Version | Type | Status |
| --- | --- | --- |
| v001–v013 | exterior, site, landscape, presentation model | approved history (frozen) |
| v014 | interior base-building model | approved history (frozen) |
| v015 | tenant Concept A (CNSA ASC) registration model | approved history (frozen) |
| v016 (`viewer/`), v017, v018 | tenant-review viewers | approved history (frozen) |
| v019 | architectural lobby milestone (Pass 1) | **approved milestone, preserved; superseded as working model by v023** |
| v020 | lobby viewer with walkable Stair 1 | approved navigation framework, preserved; superseded by v026 |
| v021 | Pass 2 development model (FF&E, planters, art, directory graphic, DP-01) | **development, superseded by v023** |
| v022 | development viewer of v021 | **development, superseded by v026** |
| **v023** | visual-refinement model | **APPROVED MODEL BASELINE** |
| v024 | viewer development baseline (v023 export, furniture collision, graze pools, seating view) | **development baseline, superseded by v026** |
| v025 | viewer visual-development baseline (walnut, tone mapping, edges) | **development baseline, superseded by v026** |
| **v026** | final viewer polish (walnut, colour balance) | **APPROVED VIEWER BASELINE** |

## Unresolved display note (do not change without new evidence or explicit instruction)
The permit documents show a **55-inch inset TV** centred on the elevator block's north face behind the DP-01 Clarus glass (ID201 B1, ID301 C2 / B4) with a TV receptacle on the revised Level 1 power plan (RV-001319-001, E110, circuit DP1H-8,10,12). Later procurement (XL Media quote 21283, 8/10/2026) shows a **75-inch portrait "Lobby Display"** on a surface portrait wall mount with no stated location. The current approved model and viewer retain **the 75-inch portrait display only**, on the east lobby wall south of door 101B, with a neutral graphic and no tenant or building names. No inset TV is modeled.

## Other open items carried forward (no action taken)
ID101 draws the WOM-01 walk-off mat at about 20 × 5 ft (the model uses 14 × 8 ft, an assumption) · the ID303 two-step tile platform is not modeled (location ambiguous) · loose chairs, tables, planters, artwork and plants are design assumptions (labeled in the model) · the ID201 PT-02 tag behind the stair landing vs the ID302 wood boxes was resolved in favour of ID302.

## Standing rules (unchanged)
`source_documents` is read-only (Building II: 360 files unchanged since the baseline inventory; `Building I` sub-folder is reserved for a separate reconstruction and has not been opened by this work). Approved versions are never overwritten; every new phase is a new version with its own control and comparison notes and a freeze-manifest check.

## How to resume (next session)
1. Read this note, `notes/lobby_refinement_control_v023.md` and `notes/browser_viewer_control_v026.md`.
2. Run `sha256sum -c notes/freeze_manifest_2026-09-23_model_v023_viewer_v026.sha256` from the project root before changing anything.
3. Any new work starts as model v027 / viewer v027 (or the next free number); v023 and v026 stay untouched.
