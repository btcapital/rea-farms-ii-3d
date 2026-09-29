# Handoff — Rea Farms Building II 3D print (state at end of 2026-09-29)

## Where things are
- **Repo:** private GitHub `btcapital/rea-farms-ii-3d` (Git LFS), branch `main`.
  - Last commits: `d88f2d5` (v003 build) and `48f357c` (freeze + Austin package).
  - Clone it outside OneDrive.
- **Local project root (Windows):** `C:\Users\Brandon\OneDrive - Taylor Capital\Shared - Documents\Dormie Equity Partners, LP\11425 Golf Links Drive, LLC\Rea Farms II 3D`
- **Main notes:**
  - `notes/3d_print/PRINT_CONTROL.md` (Pass 5 = §28–36 for v003)
  - `notes/3d_print/PRINT_VALIDATION.md` (Part C)
  - `notes/3d_print/PRINT_EXPORT.md` (Part C)

## Status
- **v002 (1:240, single colour):** printed and approved by Rob. Frozen.
- **v003 (1:240, MULTICOLOR):** approved by the owner for handoff and **FROZEN**.
  - No geometry or colour changes. Any change becomes a new version (v004).
  - Freeze record: `manifests/3d_print/print_phase_v003_FROZEN_2026-09-29.sha256` (+ `.json`). Verify with `sha256sum -c` from the project root.
- **Frozen sources (never modify):**
  - v023 `models/Building_II/building_shell_v023.blend` — `7fe33f1e…5c91`
  - v001 print — `c4684e8d…2875`
  - v002 print — `9aa5e3a4…a27c`
  - v003 print — `27737a83…52a7`

## Colour mapping (PERMANENT rule: never revert to single colour unless the owner asks)
| AMS slot | Filament | Prints |
| --- | --- | --- |
| 1 | White | White metal panels (ACM-1/4, MTL-2), white TPO roofs, terrace tops, sun-shade |
| 2 | Black | Black metal panels (ACM-2/3), MTL-1/3 copings |
| 3 | Gray | Brick BRK-1, storefront/curtain-wall frames, drop-off canopy steel, site base |
| 4 | Clear | Glazing, glass rails, canopy glass (Bambu PLA Translucent) |

## How v003 works (don't redo this)
- Each 3MF holds one object made of **parts**:
  - building: body = 3, white = 1, black = 2, glazing = 4, frames = 3
  - canopy: steel = 3, glass = 4
  - sun-shade: 1
  - site base: 3
- **In Bambu, a later part overrides earlier ones where they overlap, so part order = colour priority. Never reorder the parts.**
- The body is the exact v002 geometry; the colour parts sit inside it.
- Never colour-partition with Blender booleans. The Manifold solver produced non-planar n-gons, which showed up as diagonal colour wedges.

## Files for Austin
- **Handoff folder:** `exports/Building_II/3d_print/handoff/Building_II_v003_multicolor_Austin_2026-09-29/` (+ `.zip`).
  - It holds only the four 3MFs (multicolor_building, dropoff_canopy, sunshade, site_base) and `README.txt`.
- **Windows path-length trap:** this folder path is over 260 characters. Python needs the `\\?\` prefix to open it; Git Bash tools cope.

## What we learned today in the Bambu Studio app (important)
1. **The 3MFs carry each part's filament NUMBER but not the filament LIST.** If Project Filaments has only one filament when a file is opened, every part prints in filament 1.
   - Fix: add 4 filaments (1 White, 2 Black, 3 Gray, 4 PLA Translucent) **before** opening the file.
   - Or set each part's number by hand: Process → Objects → expand the object → Fila column.
   - On Brandon's machine the building's parts now read **3, 1, 2, 4, 3** and it slices in all four colours.
2. **Brandon's app was set to a 0.2 mm nozzle with the 0.10 mm process.**
   - Real slice: **6 d 11 h, 932 g total (397 g model + 481 g purge + 54 g tower), 1,208 filament changes.**
   - Bambu also warns that translucent PLA isn't recommended on a 0.2 nozzle.
3. **The notes' estimates are WRONG** (35 h, 487 g, "+26 g purge", 598 changes). They came from the Bambu command-line slicer, which leaves out the filament-swap time and the purge.
   - The real cost is about 5 min and 0.4 g per swap.
   - Estimate for a 0.4 nozzle at 0.12 mm: roughly 3–3.5 days and about 240 g of purge. This is **unconfirmed**; re-slice to get the real number.
4. Also expected:
   - "Floating cantilever" warning = the 3 door canopies. Paint supports there (same as v002).
   - The Prepare tab shows flickering stripes where parts overlap. Judge colours in Preview.
   - The CLI turned the building 90° on the plate.

## Open tasks
1. **Brandon, in Bambu:**
   - Confirm a 0.4 mm nozzle is installed.
   - Printer → Nozzle Diameter **0.4**; Process **0.12mm High Quality @BBL H2S**.
   - Process → Others → Flush options → **Flush into objects' infill** (switch on Advanced if hidden).
   - **Purging volumes** multiplier **0.8**.
   - Re-check parts 3/1/2/4/3; paint supports under the 3 door canopies; slice.
   - **File → Save Project As** `Building_II_v003_multicolor_H2S.3mf`.
2. **Add that saved Bambu project** to the handoff package.
   - Update `README.txt` with the filament setup steps and the realistic time.
   - Rebuild the zip, and add the new files to a new freeze addendum. Don't edit the frozen v003 files.
3. **Correct the time and purge figures** in `PRINT_CONTROL.md` §33–34 and `PRINT_EXPORT.md` Part C (text only; the notes are living documents).
4. **Email to Austin:** the draft is below. Brandon will send it himself (no address on file). If the saved project from task 1 is sent instead, steps 2–4 of the email can be dropped.

## Rules
- `source_documents` is read-only. Never overwrite a frozen file; always create a new version.
- Only change what was asked.
- The owner is a novice: explain only the actions they must take.
- Commit and push after each session, staging **only** Building II print paths. The uncommitted Building I files (`scripts/Building_I/BI_build_entrance_fix_v006.py`, `...-Brandon-9PC.py`) belong to another session. Leave them alone.
- Don't install software or send email without approval.

## Email draft for Austin (Brandon sends)
Subject: Rea Farms Building II – colour model print files (v003)

Attached are the colour print files for the Building II model (same 1:240 scale and geometry as the model Rob approved). Four files: building, drop-off canopy, sun-shade, site base.

1. **AMS (all PLA):**
   - 1 White
   - 2 Black
   - 3 Gray
   - 4 Clear (Bambu PLA Translucent)
2. **Setup:**
   - Use a 0.4 mm nozzle with 0.12mm High Quality @BBL H2S.
   - Before opening the files, make sure Project Filaments shows all 4 filaments in that order. Use + or Sync info.
   - If a file is opened with only 1 filament listed, everything prints in filament 1.
3. **Building:**
   - Process → Objects → expand the building. Its 5 parts must read 3, 1, 2, 4, 3; fix any that show 1.
   - **Do not reorder the parts.**
4. **Settings:**
   - Others → Flush options → Flush into objects' infill.
   - Purging volumes multiplier 0.8.
   - Paint supports under the 3 small door canopies only.
5. **Before printing:**
   - The Slicing Result must list all 4 filaments and many filament changes. **If it says 0 changes, don't print.**
   - Check colours in Preview.
   - Expect a multi-day print.
6. **Other pieces:**
   - Site base: Gray/slot 3.
   - Sun-shade: White/slot 1, top face down, 4 mm brim.
   - Canopy: 2 parts on 3 and 4, standing on its edge as opened, tree supports under the columns, 5 mm brim.
7. **Order:** sun-shade → canopy (a good first check of the colours and the clear filament) → building → site base.
