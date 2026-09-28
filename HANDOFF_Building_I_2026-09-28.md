# HANDOFF — Rea Farms Building I digital twin (for a new Claude Code session on any device)

Written 2026-09-28 at the end of the session that built v010–v015 and moved the project to GitHub.
Give this file to the new session first: "Read HANDOFF_Building_I_2026-09-28.md, then AGENTS.md, then confirm the frozen manifests before doing anything."

## 1. Who / what / where

- Owner: Brandon (Taylor Capital, brandon@taylor-capital.com), novice Blender user. Wants novice-friendly, one-step-at-a-time instructions with exact button names.
- Project: document-driven 3D digital twin of **Building I** — Rea Farms Sports Medicine Center, 11415 Golf Links Dr — built inside the Building II project folder `Rea Farms II 3D`.
- Skill in use: `anthropic-skills:building-digital-twin` (one approval gate at a time; STOP at every gate; never overwrite approved files).
- Repository (the copy that travels between devices): **https://github.com/btcapital/rea-farms-ii-3d** (private, GitHub account `btcapital`, branch `main`). Everything is in it, including `source_documents` (Git LFS, 9.3 GB). Clone into a folder that is NOT inside OneDrive: `git clone https://github.com/btcapital/rea-farms-ii-3d.git` (needs Git for Windows with Git LFS, and `gh auth login`).
- Original working copy on the first machine: `C:\Users\Brandon\OneDrive - Taylor Capital\Shared - Documents\Dormie Equity Partners, LP\11425 Golf Links Drive, LLC\Rea Farms II 3D` (OneDrive sync to other devices is broken; GitHub replaces it). After every work session: `git add -A && git commit -m "..." && git push`; before starting: `git pull`.
- LFS quota: GitHub free = 10 GB storage / 10 GB download per month; one full clone per month is free, a second needs a data pack.

## 2. Standing rules (owner instructions, repeated every gate — keep them)

1. `source_documents` is READ-ONLY. Never modify, move, rename or delete anything in it.
2. Do not inspect or modify Building II models / scripts / notes / renders / exports / viewers (`viewer`, `viewer_v017`…`viewer_v026`, `exports/building_II_*`, `manifests/`, `tenant_testfits/`). Building II civil/landscape sheets may be used ONLY for shared-site information, and every Building II sheet used must be entered in the shared-site register (`notes/Building_I/BI_revision_review_v002.md` §5.1). Never use Building II architectural drawings to infer Building I geometry.
3. Rev 14 record set is controlling; Rev 6 is audit only; Rev 14 is a record set, not field-verified; post-Rev-14 PCOs / closeout are evaluated individually. Real photos validate only and never override dimensioned drawings; AI-generated or retouched images are never evidence; photos never invent hidden interior geometry.
4. Never silently discard or resolve open items; carry every unresolved item forward verbatim (G-1…G-6, G-15, F-1…F-9, SC-1, SC-3, LC-2, I-1…I-4, …).
5. Never overwrite frozen/approved files. New versioned files only, `BI_` prefix, under `notes/Building_I`, `scripts/Building_I`, `models/Building_I`, `renders/Building_I`, `exports/Building_I`, `viewer_BI_vNNN`. Freeze + validate manifests at every gate. Do not move the building; do not move plants; no signage/branding/vehicles/people; do not redesign.
6. Every gate ends with a report and "STOP for approval". Do not start the next gate without the owner's explicit authorisation.

## 3. Where things stand (gate history)

| Version | What | Status |
| --- | --- | --- |
| v001–v008 | document control, geometry, facade, site, landscape, entrance fixes, footprint correction | approved, frozen |
| v009 | presentation realism (first attempt) | NOT approved (entrance site missing) |
| v010 / v011 / v012 | entrance drop-off loop + island + curbs + terrain; tower-face duplicate-panel fix; tower-front finish fix (brick → PNL1/CW1 per A4.02) | approved together 2026-09-25; **v012 = exterior + site baseline** |
| v013 | final exterior presentation realism (shaders/sky/cameras only, vertex-identical to v012) | approved 2026-09-25 = **FINAL EXTERIOR PRESENTATION BASELINE** |
| v014 | interior base-building model (slabs, columns, cores, stairs, elevator, exterior-wall inner faces, FMK partitions; CNSA existing tenant as separate collection; empty Concept_A/B/C) | approved 2026-09-25 = **INTERIOR BASE-BUILDING BASELINE / controlling digital-twin model** |
| **v015** | **interactive browser viewer** `viewer_BI_v015` + GLB export of v014 | **built and validated 2026-09-25 — AWAITING OWNER APPROVAL** |
| gate 7 | tenant Concept A / B / C | NOT authorised, not started |

Frozen manifests (validate with `python scripts/Building_I/BI_validate_manifest_v001.py <manifest>`; sources with `python scripts/Building_I/BI_freeze_manifest_longpath_v001.py check notes/Building_I/manifests/BI_freeze_sources_BuildingI_longpath_v001.json`):
- `notes/Building_I/manifests/BI_freeze_BuildingI_v014_approved.json` — 263 files, v001–v014, PASS
- `notes/Building_I/manifests/BI_freeze_BuildingI_v015_pending_approval.json` — 317 files, v001–v015, PASS
- `notes/Building_I/manifests/BI_freeze_sources_BuildingI_longpath_v001.json` — 1,231 source files, PASS
- (`BI_freeze_project_and_BuildingII_v001.json` reports 17 Building II model files MISSING because someone moved them into `models\Building_II\`; hashes identical; not touched by this work — reported at v010.)

**Next decision for the owner: approve or redirect v015.** If approved: write `BI_freeze_BuildingI_v015_approved.json` (v015 pending list + the pending manifest itself), validate, update memory/notes. Then only if authorised: Concept A (gate 7) — model it in `FUTURE_CONCEPTS/Concept_A` of a new v016 blend built from v014 read-only, re-run the GLB export (the CONCEPT_A group node already exists), set `empty: false` for concept_a in the viewer data, add its spaces / viewpoints / collision rectangles; the viewer code needs no change.

## 4. Key files to read first in a new session

- `AGENTS.md` (project rules)
- `notes/Building_I/BI_browser_viewer_control_v015.md` and `BI_browser_viewer_validation_v015.md` (latest gate)
- `notes/Building_I/BI_interior_base_control_v014.md` and `BI_interior_base_validation_v014.md` (controlling model; heights, areas, assumptions, I-1…I-4)
- `notes/Building_I/BI_interior_base_viewer_v014.json`, `BI_viewer_data_v015.json` (structured data)
- `notes/Building_I/BI_presentation_control_v013.md` (shaders, sky, cameras)
- `notes/Building_I/BI_footprint_audit_v008.md` (outline, registration, root causes)
- `notes/Building_I/BI_revision_review_v002.md` (source inventory, revision hierarchy, shared-site register §5.1)
- Skill reference files: `references/` in the skill package (workflow, source-priority, blender-standards, interior-tenant-viewer, output-contract)

## 5. Technical facts that save hours

- Blender 5.2.2 headless: `"C:\Program Files\Blender Foundation\Blender 5.2\blender.exe" --background <blend> --python <script> -- [args]`. Scripts refuse to overwrite outputs; common flags `-- --no-render`, `-- --out <folder>`, `-- --samples N`, `-- --views a,b`. Cycles OPTIX on the RTX A1000 (8 GB), 384 samples adaptive ≈ 17–52 s/frame at v013 settings. Blender python has no PIL: composites run in system python (3.14) + Pillow. numpy/OpenCV are blocked by Application Control (pure-Python only).
- Units/axes: Building I feet, origin grid 1 × grid A at FFE 661.75, +X east, +Y north, z above LVL-01; Blender metres (× 0.3048). Grid X: 1=0, 2=12.33, 3=30, 3.7=40, 4=45, 5=60, 6=72, 7=90, 8=120, 9=150, 10=180, 11=210, 12=240, 12.9=268, 13=270, 14=280; Y: A=0, B=4, B.7=22.0, C=30, C.6=42, C.9=50.5, D=52.33, E=61.5, F=70.583, F.2=74.54, G=80.53, G.2=83.58, H/H.1=98.695, J=102.03, K=119.28, K.1=124.78, K.7=133.78, L=138.53, L.6=154.53, M=168.53, M.7=187.11, N=198.53. Levels: LVL01 0 / gallery datum 11.0 / mezzanine 13.021 / LVL02 15.333; T.O.S. 28.0 (col 14) / 30.0 (A) / 31.5 (F) / 37.292 (N); elevator pit −5.
- Plan registrations (PDF points): A1.01 `x_pt = 199.81 + 6.7500x; y_pt = 1795.91 − 6.7502y`; A1.02 `197.71 / 1796.00`; A1.00b `253.98 + 6.7502x / 1779.35 − 6.7794y`; A3.01 `181.8/1807.0`; A3.02 `161.8/1803.5`; civil sheets `x_BI = 141 + (X−1859)/3.6, y_BI = 173.53 − (Y−1211.1)/3.6`; CNSA A100 L1 `x = 10.67 + (X−265.6)/8.575; y = −1.46 + (802.6−Y)/8.606`, L2 `y = 70.58 − (Y−980.3)/8.606`.
- Rev 14 PDF page map (213 pages): A0.21 p15, A0.22 p16, A1.00b p24, A1.01 p26, A1.02 p27 (page rotated 90°, coordinates are in the landscape frame), A2.01 p30, A3.01 p50, A3.02 p51, A4.01 p64, A4.02 p65, A5.01 p70, A6.01 p89, A6.11–A6.14 p91–94, A7.01 p96, S101 p132, S102 p133, S103 p134, S104 p135, S120 p136, S401–S403 p154–156, S601 p161. Building I landscape LP-100/LP-101 exist only inside PCO 24 pages 12–13; civil lives in PCO 17 (CS-101 p.10), PCO 24 (CG-101 p.11), PCO 50 p.4.
- Poppler (pdftotext -bbox-layout / -layout, pdftocairo -svg/-png, pdfinfo): `C:\Users\Brandon\AppData\Local\Microsoft\WinGet\Packages\oschwartz10612.Poppler_Microsoft.Winget.Source_8wekyb3d8bbwe\poppler-25.07.0\Library\bin` (the pdftotext on PATH is xpdf and lacks -bbox-layout). PDF names containing `&` must be copied to a scratch folder first.
- Wall extraction: pairs of parallel black lines of SVG stroke class 3 (partitions) / 10 (exterior + shaft) 1.8–9.5 pt apart with ≥ 5 pt overlap → boxes → union on a 0.125 ft raster. CNSA A100: tenant walls are BLACK, the FMK background is GREY (18.8 %), so black-only extraction isolates the tenant.
- Cycles renders coplanar duplicate faces of the SAME object solid black (self-occlusion) whatever the material; diagnose with a per-pixel `scene.ray_cast` object-ID image, hide tests, `view_layer.material_override`, face dumps across versions.
- Workbench views need Standard / exposure 0 (AgX −4.35 makes them black); unlit interiors need ≈ 3 stops more (AgX −1.3); hide at collection level for renders so object flags (which are hashed) stay intact.
- Terrain: never use self-intersecting cutters with EXACT booleans; make open-sheet operands closed slabs first; strip bottom faces before joining; grid slabs clipped by boolean INTERSECT (ear-clip fan triangles give shading streaks); polygon miter offset for curb rings.
- Bash heredocs containing long quoted Python fail sporadically on this machine — write generator/patch scripts with the Write tool and run them. Windows python needs `C:/` paths, not `/c/`.
- Viewer v015: three.js 0.186.1 vendored; three.js space = (X ft, Z ft, −Y ft) after scaling the GLB by 1/0.3048; floors clip at 10 / 20.5 / 26 ft; walker radius 1.0 ft, eye 5'-6", 9 / 18 ft/s, sub-steps ≤ 0.2 ft; collision only from v014 rectangles/faces (door gaps = drawn gaps, nothing invented); stairs not climbable; test API `window.BI` (simulate, teleport, measureAt, saveImage, setLayer…). The desktop app's built-in browser pauses requestAnimationFrame while `javascript_tool` runs, so captures must render explicitly; canvas captures exclude DOM labels (composited in `saveImage`); `server.py --capture <dir>` writes validation PNGs; Windows SO_REUSEADDR lets a second server bind the same port, so `allow_reuse_address = False`.
- Launch for the owner: double-click `viewer_BI_v015\start_viewer.bat` → http://127.0.0.1:8115/ (falls back to 8116…8125). Building II viewers use their own ports/folders and must not be touched.

## 6. Open items carried forward (verbatim list lives in the control notes)

Exterior/site/landscape: G-1…G-6, G-15 (brick-ledge tolerance on north-block west/north faces), F-1…F-9 (column wraps, courts parapet tags, courts base band, vestibule tag, floating CW1 placeholders, PNL3, soldier band/coping/soffits, finish depth, six coplanar parapet-return strips), SC-1 (dumpster brick), SC-3, LC-2 (parking-lot quantities). Interior: I-1 mezzanine east stair tread count (drawn 7 vs written 8), I-2 MOB-shell inner GWB by tenant, I-3 gallery datum 11'-0" vs Gallery 234 on the L2 slab, I-4 braced-frame grid lines by section reading only. Viewer: stairs not walkable, exterior doors closed, room 101 (lobby) has no numeric tag in the sheet text, flat viewer colours are not the v013 look.

## 7. How to resume in one line

"Continue the Building I digital twin (building-digital-twin skill). Read HANDOFF_Building_I_2026-09-28.md and AGENTS.md, run `git pull`, validate the three manifests in §3, then wait for my decision on v015 — do not start Concept A/B/C."
