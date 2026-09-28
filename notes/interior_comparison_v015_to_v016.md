# Comparison — v015 → v016 (browser walkthrough prototype)

Date: 2026-09-21
Basis: `notes/browser_viewer_control_v016.md`. v016 adds an export and a viewer. **It adds no model version: there is no `building_shell_v016.blend`, and no architectural geometry was created, moved or edited.**

## What v016 added

`scripts/export_viewer_v016.py` · `exports/building_II_CNSA_ASC_v016.glb` · the `viewer/` folder · `notes/browser_viewer_control_v016.md` · this note · eight screenshots `renders/viewer_v016_*.png`.

## Verification that no approved geometry changed

| Check | Result |
| --- | --- |
| All frozen files — v001–v015 models, scripts, notes, reports, room schedule, 88 renders, the two earlier test GLBs, the v015 underlay image and the tenant PDF (172 files) | SHA-256 identical before and after: **0 changed** |
| `models/building_shell_v015.blend` | opened read-only by the export script and **never saved**; the script asserts its SHA-256 is unchanged after the export, and records it in `viewer/assets/viewer_data_v016.json` |
| `source_documents\Building I` | not opened; aggregate 1,231 files / 6,929,037,544 bytes unchanged |
| `source_documents\Building II` | 360 files, 0 differences |
| GLB geometry vs v015, group by group (GLB re-imported into Blender; every vertex position compared at 1 mm; triangle counts compared) | see table — **all seven building and tenant groups identical** |

| Group | Unique vertex positions v015 / GLB | Missing / extra | Triangles v015 / GLB |
| --- | --- | --- | --- |
| Exterior solid shell | 520 / 520 | 0 / 0 | 1,206 / 1,206 |
| Exterior envelope | 2,546 / 2,546 | 0 / 0 | 4,320 / 4,320 |
| Exterior upper | 650 / 650 | 0 / 0 | 1,104 / 1,104 |
| Base interior Level 1 | 3,350 / 3,350 | 0 / 0 | 11,292 / 11,292 |
| Base interior Level 2 | 1,766 / 1,766 | 0 / 0 | 5,076 / 5,076 |
| Base interior roof | 68 / 68 | 0 / 0 | 252 / 252 |
| **Concept_A_CNSA_ASC** | 1,572 / 1,572 | 0 / 0 | 2,556 / 2,556 |
| Site / context | 1,504,323 / 1,504,323 | 579 / 579 | 902,800 / 902,800 |
| Landscaping | 362,011 / 362,011 | 3 / 3 | 266,000 / 266,000 |

The 579 and 3 mismatches in the two planting-heavy groups are leaf-card vertices whose coordinate falls exactly on a 1 mm rounding boundary after the 32-bit export (0.04 % and 0.001 %, equal numbers missing and extra, identical triangle counts); no object moved.

What the export does change, in memory only and only for the browser: objects are grouped under nine nodes and joined per collection; procedural materials are replaced by flat colors; hidden helper objects are left out (list in the control note). The walk grid and the viewer add **no doors or openings**.

## Viewer validation

All items requested were tested locally and passed: model loads · Concept A toggles independently · orbit · walk with collision · ten saved viewpoints · room selection and metadata panel · plan mode · registered tenant-underlay toggle. Details and measured performance are in the control note, section 8–9.

## Screenshots (`renders/`)

`viewer_v016_01_exterior_orbit.png` · `viewer_v016_02_plan_concept_A.png` · `viewer_v016_02b_plan_with_tenant_underlay.png` · `viewer_v016_03_viewpoint_reception.png` · `viewer_v016_04_viewpoint_operating_room.png` · `viewer_v016_05_room_information_panel.png` · `viewer_v016_06a_cutaway_concept_shown.png` · `viewer_v016_06b_cutaway_concept_hidden.png`

## How to open the viewer (novice steps)

1. Open File Explorer and go to the project folder `Rea Farms II 3D`, then open the folder **`viewer`**.
2. Double-click **`start_viewer.bat`**. (If Windows shows a blue "Windows protected your PC" box, click **More info**, then **Run anyway**.)
3. A small black window appears and, about three seconds later, your web browser opens the viewer at `http://127.0.0.1:8016/`. Leave the black window open.
4. Wait a few seconds until "Loading Building II model…" disappears.
5. Use the panel on the left: choose **Orbit**, **Walk** or **Plan (Level 1)**; tick or untick the **Show / hide** boxes; click a **Saved viewpoint** to stand in that room; click any tenant room to see its data at the top right.
6. When you are finished, close the browser tab and then close the black window.

If the browser does not open by itself, open it and type `127.0.0.1:8016` in the address bar. The viewer works only on this computer and is not on the internet.
