# Browser viewer control document v017 — walk speed × 2

Date: 2026-09-21
Scope: viewer-only refinement. `viewer_v017/` is a copy of the approved `viewer/` (v016) with the Walk-mode speed doubled. **No Blender model, GLB, collision grid, eye height, orbit control, viewpoint, room data, plan mode, camera position or tenant geometry was changed.** The approved v016 viewer in `viewer/` is untouched and still works on its own port.

## Walk speed

| | Normal (W A S D / arrows) | With Shift held |
| --- | --- | --- |
| v016 | 4.5 ft per second | 9.0 ft per second |
| **v017** | **9.0 ft per second** | **18.0 ft per second** |

Exact code value changed — `viewer_v017/src/main.js`, function `walkStep`:

- v016: `const speed = (k.ShiftLeft || k.ShiftRight ? 9.0 : 4.5) * dt`
- v017: `const speed = (k.ShiftLeft || k.ShiftRight ? 18.0 : 9.0) * dt`

Both numbers are doubled exactly, so Shift remains 2 × normal. Forward, backward and strafe all use this one value and the direction is normalized as before, so they stay proportional (a W + D diagonal also moves at exactly 9.0 ft/s). Mouse-look sensitivity (`0.0032` per pixel) is unchanged. There is no acceleration in either version (movement starts and stops instantly).

## Collision-related adjustment: yes, one was needed

**Why.** The viewer limits one frame to 0.1 s. At the v016 speed the longest single step was 0.9 ft, which cannot cross a partition. At the v017 Shift speed the longest single step becomes 1.8 ft. I tested the unchanged v016 movement code at that worst case and found that **107 of 12,464 diagonal steps passed through the 4⅞" partition of PRE/POST A-002** (for example from x 3.10, y 92.00 to x 4.37, y 90.73). This only happens on a very slow frame (10 frames per second or less) with Shift held, but it must not be possible.

**What was changed.** Inside `walkStep`, a frame's movement is now applied in equal pieces of at most 0.2 ft, and every piece is tested with exactly the same v016 test and slide rule (`canStand`, then slide along x, then along y). Nothing else: the collision grid (`viewer_data_v016.json`, byte-identical), the body radius (0.75 ft), the `canStand` and `nearestStandable` functions, the eye height (5.5 ft) and the slide behavior are unchanged. At normal frame rates the pieces are the same size as a v016 step, so movement feels the same, only faster.

## Files

`viewer_v017/` differs from `viewer/` in four files only: `src/main.js` (the two changes above) and `start_viewer.bat`, `serve.py`, `serve.js` (port **8017** instead of 8016, so v016 and v017 can never be confused or collide). The GLB (`viewer_v017/models/building_II_CNSA_ASC_v016.glb`) and the viewer data are byte-identical copies of the approved v016 files. No UI or visual change was made; as a result the page heading still reads "Review prototype v016" — the address `127.0.0.1:8017` is what identifies v017.

## Validation (2026-09-21, final v017 code)

| Test | Result |
| --- | --- |
| W forward, 2 s in the open main corridor | 18.0 ft → **9.0 ft/s** (v016: 4.5) |
| S backward | 18.0 ft → 9.0 ft/s, opposite direction |
| A / D strafe | 18.0 ft each → 9.0 ft/s, left / right |
| W + D diagonal | 9.0 ft/s (normalized) |
| Shift + W | 36.0 ft → **18.0 ft/s** (v016: 9.0) |
| W at a slow 10 frames per second | 9.0 ft/s (speed does not depend on frame rate) |
| Collision at a wall (corridor, Shift-walk north into the PRE/POST wall at y 91.5) | stops at y 90.65, remains in the corridor |
| Documented open route: Lobby 101 → base-building door 101C → WAIT | passes through the documented opening, stops at the RECEPTION wall |
| Closed OR A-051 after teleport, Shift-walking 8 s toward each of the four walls | always ends inside A-051 (x 45.3–60.9, y 1.5–19.95; clear interior x 44.3–61.8, y 0.9–20.9) |
| Worst-case wall test: every 0.4 ft start point × 16 directions × 5 consecutive 0.1 s frames with Shift, in OR A-051, PRE/POST A-002, STERILE PROCESSING, LOUNGE and WAIT | **162,368 runs: 0 left their room, 0 ended inside a solid** |
| Unchanged items | eye height 5.5 ft; 10 viewpoints; 57 rooms; GLB and viewer data byte-identical |
| Launch test | `viewer_v017\start_viewer.bat` starts the server on port 8017; a real (headless Edge) browser loaded the page past "Loading…" and showed the corridor viewpoint; no console errors |
| Frozen files | all 257 files of v001–v016 (models, scripts, notes, renders, exports, the whole `viewer/` folder, tenant PDF): SHA-256 identical before and after |

Testing note: movement was driven through the viewer's built-in `step(dt)` test function, because the automated test browser does not hold keys down; mouse and keyboard handling itself is unchanged from v016.

## How to open v017 (novice steps)

1. Open File Explorer and go to the project folder `Rea Farms II 3D`.
2. Open the folder **`viewer_v017`** (not `viewer`).
3. Double-click **`start_viewer.bat`**. (If Windows shows a blue "Windows protected your PC" box, click **More info**, then **Run anyway**.)
4. A small black window appears and about three seconds later your browser opens `http://127.0.0.1:8017/`. Leave the black window open.
5. Wait until "Loading Building II model…" disappears, click **Walk** (or any saved viewpoint), and move with **W A S D**; hold **Shift** to go faster.
6. When finished, close the browser tab, then close the black window.

If the browser does not open by itself, type `127.0.0.1:8017` in its address bar. If an old tab is still showing, press **Ctrl + F5** to reload it.
