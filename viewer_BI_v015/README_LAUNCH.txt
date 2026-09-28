BUILDING I - REA FARMS SPORTS MEDICINE CENTER - BROWSER VIEWER v015 (model v014)
================================================================================

HOW TO START (no installation, nothing leaves this computer)
1. Open this folder:  viewer_BI_v015
2. Double-click:      start_viewer.bat
   A black window opens and says "open http://127.0.0.1:8115/". Your web browser opens the viewer by itself.
   If it does not, open Chrome or Edge and type   127.0.0.1:8115   in the address bar.
   (If port 8115 is busy the window says 8116, 8117 ... - use the number it prints.)
3. Wait for "Loading model ... 100 %" (13 MB, a few seconds).
4. To stop: close the black window.

WHAT YOU SEE
- Top bar:  Mode (Orbit / Walk / Plan)   Floor (Level 1 / Level 2 / Mezzanine / Both-Exterior)   Existing CNSA ON/OFF   Concept selector   Presentation Mode
- Left:     Viewpoints (click one to jump there), tools, layers
- Right:    Selection info (click a room in Orbit or Plan mode), measurement readout, notes
- Bottom:   status line (mode, floor, walker position in feet, fps)

ORBIT   drag = rotate, right-drag = pan, wheel = zoom.  "Reset view" recentres.
WALK    click the picture once so the mouse steers (Esc gives the mouse back), then
        W A S D or the arrow keys walk at 9 ft/s; hold Shift for 18 ft/s.  Eye height 5'-6".
        Walls, columns, the elevator shaft, stairs and slab edges stop you.  Doors drawn on A1.01/A1.02 are open.
        Stairs are not climbable in v015 - use the Floor buttons (each floor remembers where you were) or a viewpoint.
        Green "DOCUMENTED WALKABLE ROUTE" = you can walk there from the entrance (Level 1) / elevator (Level 2) / mezzanine stairs.
        Orange "VIEWPOINT TELEPORT" = the viewer puts you there directly; no documented walking route from those origins.
PLAN    top-down, north up.  Drag = pan, wheel = zoom.  "Plan underlay" shows the Rev 14 A1.01 / A1.02 sheet under the model.
        Room labels are on automatically in Plan mode.

EXISTING CNSA  ON shows the CNSA tenant partitions (A100 rev 8); OFF shows the base building only. Same for the Concept selector.
CONCEPT A/B/C  are placeholders - nothing has been modeled for them yet, so they are greyed out.

MEASURE   click "Measure", then click two points on the model: total / horizontal / vertical distance in feet-inches
          and the model coordinates of both points.  SPATIAL REVIEW ONLY - this is the v014 model, not a survey.
CLICK A ROOM   in Orbit or Plan mode: name, room number, level, category, area (when available) and whether the
          boundary is documented or interpreted.  "Clear Highlight" or Esc clears it.
SAVE VIEW IMAGE   writes a PNG of the current view to your Downloads folder, named
          BuildingI_v015_<mode>_<floor>_<date_time>.png
PRESENTATION MODE   hides the technical panels; "Exit Presentation Mode" brings them back.

IF THE PAGE STAYS BLANK
- Do not open index.html directly (double-clicking the file does not work - the model must be served). Use start_viewer.bat.
- If neither Python nor Node.js is installed the .bat falls back to a PowerShell server automatically.
- Press F5 to reload.  If the model still does not load, press F12 and send the red text in the Console tab.

FILES
  model/BI_model_v014_viewer_v015.glb   the exported v014 model (13.0 MB)
  data/BI_viewer_data_v015.json         floors, groups, concepts, rooms, viewpoints, collision, underlay registration
  plans/                                 Rev 14 A1.01 / A1.02 underlays (150 dpi, registered, cropped only)
  src/app.js, src/style.css, index.html  the viewer
  vendor/three/                          three.js 0.186.1 (MIT) - offline copy
  server.py / server.js / server_fallback.ps1 / start_viewer.bat   local server + launcher
