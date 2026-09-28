# Lobby concept control document v019 — INT_LOBBY_CONCEPT_A (Pass 1, architectural)

Date: 2026-09-22 · Applies to: `scripts/build_shell_v019.py` → `models/building_shell_v019.blend`
Baseline: **v015, frozen** (v016–v018 are viewer-only). Every v015 object is rebuilt by the identical code and is not edited. v019 only **adds** objects named `LOB_A_…` inside `Building_II > INT_LOBBY_CONCEPT_A`. Written before modeling. Basis: owner approval of `notes/lobby_concept_fit_analysis_2026-09-22.md` (2026-09-22) with the documented permit-set interior design as the controlling source and `source_documents\concept_design\Rea_Farms_2_Lobby.pptx` as aesthetic reference only.

Codes: **W** written · **M** measured from sealed vector linework (ID302 elevations are at ¾" = 1'-0", 54 pt/ft, self-checked: the drawn wall height is exactly 28'-11⅜"; ID201 elevations 3/8" = 1'-0", 27 pt/ft, checked against the 16'-0" floor-to-floor) · **C** concept (PowerPoint) · **A** assumption / design choice.

## 1. Targeted revision check (documents issued after the ID sheets)

Searched all Building II sources (360 files) for ASIs, bulletins, addenda, RFIs, PCOs, submittals, substitutions, closeout and record documents touching the lobby. Findings:

| Document | Date | Lobby relevance | Effect |
| --- | --- | --- | --- |
| `00 PLANS\APPROVED-COS-RV-001319-001.pdf` (permit revision, electrical sheets E003/E010/E210/E220/E603/E701, RTAP rev 8 04/21/2026, rev 10 05/06/2026) | approved 6/18/2026 | Re-issues the lighting schedule: **SH1 "pendant square hollow LED", Lightnet Caleo Inverse, 3,570 lm, 3500 K, 47 W × 7**, "coordinate finish, mounting type and suspension"; **WLC wall-mounted cylinder, BEGA 33590, 3500 K × 64** (wattage 8 W in this revision, 4 W / 294 lm on the original E003), "color chosen by architect"; RTAP narrative changes only exit-sign / egress fixtures in the lobby | **Confirms** the pendant family, count and 3500 K, and the 64 wall cylinders. Controlling. |
| `Contractors\XL Media\21283 - CSMC 2 Lobby_approved.pdf` | 8/10/2026 | Approved quote "Lobby Display": **Panasonic TH-75EQ3W 75" commercial monitor, Chief AS3PL Tempo portrait wall mount, BrightSign player** | The directory is a **75" portrait display** (not the 55" assumed in the analysis). Location not stated → east wall south of door 101B per approval. |
| `Edifice\chaos (1) lobby fixture.pdf` | 6/5/2026 | Cut sheet: Modern Forms "Chaos" PD-64875 75" sculptural pendant, 3000 K, black/brass/aluminum. No quantity, no stamp, no transmittal | **Not controlling**: the permit revision approved 13 days later still schedules SH1 × 7. Recorded as a candidate substitution; **not modeled**; flagged for the owner. |
| `McMillan Pazdan Smith\2026_0810_CSMC MOB 2_RFI 51 Add Service Proposal_signed.pdf` | 8/10–8/18/2026 | Add-service for revising door and hardware schedules to security drawings | No lobby finish / design change. |
| `00 PLANS\2025.09.11 … Interior Concepts with Renderings.pdf` (concept design 04/18/2025) | pre-permit | Notes: walnut vs rift oak decided (ID801 = walnut); "wood treads with concealed glass railing channel; under-stair metal panel; **stair framing gunmetal finish**" | Superseded by the permit set but consistent with it; supports the dark stair finish. |
| Edifice PCOs 1–8, Lanier PCOs / scope changes, ASI Signs (a sign vendor, not architect's supplemental instructions), pay apps, V3 civil, bulletin 2026-5-14 (infrastructure) | various | site / civil / foundation / fees | none |

No later document supersedes ID201 / ID302 / ID303 / ID801 / A212 / A500. **Proceeding.**

## 2. Controlling sources per component

| Component | Controlling source | Notes |
| --- | --- | --- |
| Wood feature wall extent | ID201 B2 west elevation (W dims 8¼" + 1'-6" + 8'-7⅞" + 7'-0" + 11" + 8" = 19'-4⅛"; north end line **M** at model y 92.86; south end = lobby south wall face y 73.41 incl. the 8¼" return) → **y 73.41 → 92.86 (19.45 ft), z 0 → 28.95** on the west wall face x 106.59 | matches ID302 A6 drawn width 19.4 ft |
| Wood wall module | ID302 A6/A5/A4: repeating group **36.5" (M)** of six contiguous boxes **6" / 8" / 6" / 4" / 4" / 8"** wide (M ±⅛"), staggered lengths (M, table in the script); boxes bottom at 13.7" AFF on the POR-02 plinth; all boxes are laminate-wrapped plywood on a laminate-wrapped wall (W) | 6.4 groups across the wall |
| Box depth | ID302 B4 plan section (¾" scale): boxes **2.4" (M)** proud of the wall face; wall build-up 4.8" (M) | |
| Wood material | ID801 PL-01 Wilsonart Uptown Walnut Softgrain, **grain vertical (W)** | colour tone **A** (warm mid walnut) |
| Wall lights | ID302 A6 + E003/RV: **64 WLC** BEGA 33590, 3500 K (W); positions **M ±3" from the A6 raster** (10 per group: 2 at 22'-2", 1 each at 18'-10", 17'-9", 16'-11", 13'-4", 2 at 4'-4", 2 at 2'-5"/2'-1" AFF) | fixture 3" × 5⅛" × 3¾" (ID801 LT-04, W) |
| Plinth / banquettes | ID303: west banquette 8'-7⅞" long (W) at y 75.6–84.3 (from the ID201 string); POR-02 plinth 1'-1¾" high (W) × 1'-10" deep (W); south banquette 9'-3" (W) along the south wall from the SW corner; seat 1'-6" (W), FAB-01 leather (W) | seat cushion thickness 4" **A**; the ID303 two-step tile platform is **not modeled** (location ambiguous) |
| PT-02 panel behind the landing | ID201 B2: PT-02 tag on the rectangle y 73.4–79.4, z 8.6–15.5 and on the balcony fascia (W) | modeled as a flush metallic panel |
| Stair finishes | A500/A501 (W): (2) 1" × 14" stringer plates, wood treads (WD-01 walnut, ID801), painted risers/stringers, metal-panel soffit between stringers, glass shoe guardrail with metal-panel shoe wrap, 1½" O.D. handrail at 36", 42" guard | **dark charcoal colour = design choice (C, supported by the 2025 concept "gunmetal")**; nosing 1" **A**; PT-02 Scuffmaster metallic used as the dark-metal tone |
| Pendants | A212 Rev 5 (coffer 23'-6" × 18'-7" at 12'-6" AFF L2, inner panel 11'-6" × 6'-6¾" at 12'-0" AFF, W; position M ±0.5 ft) + E003/RV (SH1 × 7, 3500 K, W) | ring sizes, black frame, stagger of hanging lengths = **C/A** (pendant lengths "as directed by the architect") |
| Coffer and track | A212 (W), ID801 LT-02 Coronet Magneto black recessed track, mitered corners (W) | |
| Floor | ID801 POR-01 Porcelanosa Santorini Gray Nature **47" × 47"** (W), custom #643 warm-gray grout (W); ID101 WOM-01 24" × 24" walk-off at the entry (W) | grout ⅛" **A**; tile origin on the entry axis **A**; walk-off extent 14 × 8 ft **A** |
| Walls | ID801 PT-01 SW 7646 First Star satin (W) on gypsum; PT-02 on fascia (W); RB-01 6" base (W) | |
| Directory | XL Media approved quote (75" Panasonic, portrait mount) | location east wall y 82.58–88.16 (owner-approved proposal); bottom 2'-6" AFF **A** |
| Cameras | owner-approved three lobby cameras | new; approved cameras untouched |

## 3. Frozen / not touched
All v015 geometry; the Level 1 lobby walls, slab, columns, elevator, doors, CW1 / SF7 glazing, Stair 1 treads / landing / guards (finishes are overlay shells offset 1/16"–⅛" from the frozen faces), Level 2 slab and guards, ceiling plane CA-1 (the coffer hangs below it), cameras and lights of v010–v015.

## 4. Pass 1 scope (this build)
Wood wall (field, boxes, 64 lights, PT-02 landing panel) · stair finish package (walnut treads, dark risers, stringers, soffits, landing fascia, shoes, handrails) · balcony fascia PT-02 and shoes / handrails on the Level 2 guards · coffer with LT-02 track and 7 pendants · POR-01 floor, WOM-01 walk-off, POR-02 plinths, banquette seats · PT-01 wall overlays · directory massing · 3 cameras · 3 renders. **Excluded until Pass 2:** loose chairs, tables, planters, artwork, directory detailing, final material / lighting tuning.

## 5. Assumptions (design choices) — all labeled `A` in the script's `LOBBY_A` parameter block
Stair dark-metal colour and roughness · nosing 1" · walnut tone · seat cushion 4" · pendant ring sizes 3'-6" to 6'-0" and hanging lengths (bottoms 21–26 ft) · LT-02 slot emission · WLC emission level · grout ⅛" · tile origin · walk-off extent · directory height · PT-01 / PT-02 RGB values · the two-step tile platform omitted · glass shoe 2½" × 4" profile · handrail brackets omitted.
