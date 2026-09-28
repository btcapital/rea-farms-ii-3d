# Browser viewer control document v016

Date: 2026-09-21
Purpose: first interactive browser review prototype of Building II with the real tenant concept `Concept_A_CNSA_ASC`, usable without Blender. Review prototype, not the final application. **No architectural geometry was created or changed in this phase.** Building I was not touched; `source_documents` and the tenant PDF were not modified. Nothing is published to the internet.

## 1. Source and outputs

| Item | Path |
| --- | --- |
| Source model (read only, never saved) | `models/building_shell_v015.blend` |
| Export script | `scripts/export_viewer_v016.py` (run with Blender 5.2: `blender --background --python scripts/export_viewer_v016.py`; refuses to overwrite) |
| **GLB export** | **`exports/building_II_CNSA_ASC_v016.glb`** — glTF 2.0 binary, **8.4 MB** (8,409,512 bytes); earlier GLB files in `exports/` untouched |
| Viewer | `viewer/` (9.7 MB in total) |
| Copy of the GLB used at run time | `viewer/models/building_II_CNSA_ASC_v016.glb` (byte-identical copy) |
| Viewer data | `viewer/assets/viewer_data_v016.json` (groups, 10 viewpoints, 57 rooms, walk grid, underlay registration) and `viewer/assets/tenant_underlay_Concept_A_CNSA_ASC_v015.png` (copy of the v015 underlay image) |
| Validation screenshots | `renders/viewer_v016_01 … 06b_*.png` |

Viewer folder: `index.html` · `src/main.js`, `src/style.css` · `assets/` · `models/` · `vendor/` (Three.js) · `start_viewer.bat`, `serve.py`, `serve.js`. At run time the viewer reads only files inside `viewer/`; it does not read `source_documents`, `notes`, `models` or the internet.

**Three.js** 0.160.1 (MIT license), five files downloaded once from cdn.jsdelivr.net with the owner's approval on 2026-09-21 into `viewer/vendor/`: `three.module.min.js` (671 KB), `addons/controls/OrbitControls.js`, `addons/loaders/GLTFLoader.js`, `addons/utils/BufferGeometryUtils.js`, `THREE_LICENSE.txt`. No framework, no build step, nothing installed on the computer.

## 2. Object / group organization in the GLB

Nine top-level nodes. Inside each, objects of the same v015 collection are joined into one mesh (fewer draw calls); instanced planting / trees and the tenant room plates stay separate. Names are kept (`TEN_A_Room_A-051_OR`, `Base_Interior_Level_1__BASE_Core`, …); custom properties are exported as glTF "extras".

| GLB node | v015 content | v015 objects → GLB nodes |
| --- | --- | --- |
| `GRP_Exterior_Solid_Shell` | 01_Masses, 03_Opening_panels (the solid exterior) | 39 → 2 |
| `GRP_Exterior_Envelope` | terrace parapets, canopies, glass railings, facade detail, utility yard | 360 → 5 |
| `GRP_Exterior_Upper` | roof parapets and sun-shade (upper obstruction) | 92 → 2 |
| `GRP_Base_Interior_Level_1` | v014 Level 1: inside shell with glazing, slabs, columns, core, stairs, elevator, service rooms | 254 → 6 |
| `GRP_Base_Interior_Level_2` | v014 Level 2 and terrace slab (upper obstruction) | 173 → 8 |
| `GRP_Base_Interior_Roof` | v014 roof deck lid (upper obstruction) | 1 → 1 |
| `GRP_Concept_A_CNSA_ASC` | v015 tenant concept: `TEN_A_Partitions`, `TEN_A_Bay_dividers_TYPE_UNKNOWN`, `TEN_A_Table_proxies`, `TEN_A_Floor_markers`, 57 room plates, 18 circulation plates | 213 → 79 |
| `GRP_Site_Context` | site, context, site detail, backdrop | 474 → 301 |
| `GRP_Landscaping` | Building II planting | 346 → 335 |

**Concept A is not baked into the base building**: it is its own node and toggles independently. Not exported: cutters, the hidden north-arrow aid, the 28 hidden ambiguous perimeter-outline walls, the Blender underlay plane (the viewer draws the underlay itself), Blender text labels (the viewer draws labels), cameras and lights.

Materials: Cycles procedural materials cannot be exported, so each material is flattened **in memory** to a plain color (its Blender viewport color, or its base color when not procedural); glass becomes a 28 %-opaque blue-grey. The .blend is not saved, so v015 materials are unchanged.

## 3. Coordinate conversion

Model: decimal feet, origin grid 1' × K' at Level 01 finish floor, X east, Y north, Z up (unchanged since v001). GLB: metres, Y up (glTF standard).
`x_ft = X / 0.3048` · `y_ft (north) = −Z / 0.3048` · `z_ft (up) = Y / 0.3048`. The viewer converts with `toWorld()` / `toFeet()` in `src/main.js`. No scaling, rotation or re-origin was applied.

## 4. Camera / viewpoint mapping

The ten v015 cameras `VP_A_01 … VP_A_10` are exported as data (position in feet, forward direction, lens) — not as GLB cameras. A viewpoint button switches to Walk mode, places the eye at the saved position (z = 5.5 ft = 5'-6") looking along the saved direction, and sets the field of view from the saved lens (36 mm sensor width). Buttons: ASC entrance / arrival · Reception · Waiting · Main clinical corridor · Nurse station · Pre/post room A-002 · Procedure-room approach · OR A-051 · Sterile processing · Staff lounge.
**A viewpoint button is review navigation (a teleport), not a documented door connection**; the panel says so and a message appears on every jump.

## 5. Room metadata

From `notes/tenant_concept_A_CNSA_ASC_room_schedule_v015.json` and the v015 room plates: room ID, name as labeled on the tenant plan, concept, floor, printed SF, modeled SF, net SF where a smaller room is drawn inside, enclosure as drawn, fill rectangle in feet. A click in any mode casts a ray into the model, converts the hit point to feet and selects the smallest room rectangle containing it; the room is highlighted and its data shown in the **Room information** panel (top right). Nothing is invented: where the plan prints no area the panel says "not printed on the plan". In Walk mode the status line also names the room you are standing in.

## 6. Controls

| Function | How |
| --- | --- |
| Orbit mode | left-drag rotate, right-drag pan, wheel zoom, **Reset view** |
| Walk mode | eye height 5'-6"; **W A S D** or arrow keys (Shift = faster: 4.5 / 9 ft per second); **drag the mouse** to look; click = room data |
| Plan (Level 1) mode | true top-down, north up; drag = pan, wheel = zoom; roof, Level 2 and the solid exterior hidden automatically; room labels on |
| Show / hide | Building II exterior · Roof / Level 2 (upper obstruction) · Base-building interior · Concept A – CNSA ASC · Site / context · Landscaping · Tenant plan underlay (registered PDF) · Room labels |
| Review note | collapsible note at the bottom of the panel: "Concept plan does not document tenant doors/openings. Room-to-room circulation is incomplete and no openings have been invented." |
| Address-bar parameters (optional) | e.g. `?vp=VP_A_08_operating_room`, `?mode=plan&underlay=1`, `?mode=orbit&exterior=0&upper=0&concept=0` |

The exterior is a solid model, so it is never shown from inside: it switches off in Walk and Plan mode, and while it is on in Orbit mode the interior groups are not drawn (they would be invisible inside the solid anyway, and would flicker where surfaces coincide).

**Walking and doors.** Collision uses a 0.25 ft grid exported from the model: a cell is open only if it lies inside the Level 1 outline and no base-building or tenant solid stands between 0.5 ft and 6.5 ft above the floor (315 blocking objects; exterior glazing, stairs, columns, tables and the elevator hoistway block). **No opening was added.** Documented base-building door openings (for example lobby door 101C into WAIT) are passable because they exist in the v014 model; every walled tenant room is closed because the tenant plan draws no doors, so you can walk inside a room after a viewpoint jump but cannot walk out of it. Walking is limited to Level 1.

## 7. Known limitations

Flat colors only (no procedural brick, paving or foliage shading), no shadows, uniform sky light — a spatial review tool, not a rendering · no doors, ceilings, furniture, finishes or MEP (not documented / out of scope) · bay dividers of unknown type and assumed heights are carried over from v015 · Level 2 cannot be walked; stairs cannot be climbed · the underlay is one 150 dpi image of the whole sheet (slightly soft when zoomed far in) · labels are shown for rooms with a printed area only · mouse-look is by dragging (no pointer lock) · tested in Microsoft Edge (Chromium); not tested in Safari or on phones/tablets · the local server serves only `127.0.0.1` and must be running while the viewer is used.

## 8. File size and browser performance

GLB 8.4 MB · viewer folder 9.7 MB · page ready about 2–4 s after opening on this computer. Unique geometry about 100,000 triangles; with instanced planting and context trees about 0.9–1.0 million triangles and 650–1,300 draw calls are on screen. Measured GPU cost per frame at 1280 × 720 on this computer's **integrated Intel graphics** (the browser did not use the NVIDIA card): exterior orbit 7 ms, walk views 7 ms, plan view 33 ms — i.e. smooth (30–100+ frames per second). Turning **Landscaping** and **Site / context** off drops a frame to under 2 ms if a slower computer ever needs it.

## 9. Validation performed (2026-09-21)

Model loads with no console errors · all nine groups found · Concept A toggles independently of the base building · orbit drag / zoom / reset work (real mouse events) · walk movement and collision work (corridor walk 45 ft in 10 s; inside OR A-051 a 15-second walk toward each wall stays inside the OR; lobby → door 101C → WAIT works and stops at the RECEPTION wall) · all ten viewpoints land in the intended space · room click selects the right room and shows printed / modeled areas (tested: OR A-052 by mouse click, OR A-051 by parameter) · plan mode works · underlay toggle works and lines up with the model · launcher `start_viewer.bat` starts the server and opens the browser; Node fallback server also tested · GLB geometry compared with v015 group by group (see `notes/interior_comparison_v015_to_v016.md`).
