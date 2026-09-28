# Material control document v004 — first materials / facade-detailing pass

Date: 2026-09-21
Applies to: `scripts/build_shell_v004.py` → `models/building_shell_v004.blend`
Geometry baseline: **v003, frozen.** v004 rebuilds the identical v003 geometry and only (a) assigns materials to its faces and (b) adds thin facade-detail overlay objects in a separate collection. No approved object is moved, resized or re-cut. No surface-level build-up adjustment was needed (the A003 build-ups are already in the v003 geometry).
Written **before** v004 was built.

Status codes: **DOC** = named on the drawings · **INT** = needed interpretation (explained) · **UNRES** = not on the documents reviewed → neutral placeholder, no guess.

Important limit on color: the drawings give finish **names**, never color values. Where a named finish is used, the on-screen color is only an approximation of that name and is marked **INT-color**; it must be calibrated against a manufacturer sample or chip before any presentation work. No texture image files are used; everything is procedural.

## 1. Sources

| Ref | Sheet | File, PDF page |
| --- | --- | --- |
| Legend | Elevation Material Legend on A300 / A301 (Rev 5), A302 | Rev 5 arch. p.8–9; Approved p.33 |
| Tags | Material tags on the elevations, located in building coordinates; shaded elevation tones (brick hatch / light / black) sampled at each wall zone to confirm | same |
| Frames & glass | Storefront Notes + Glazing Schedule A811; Curtain Wall Notes A815 (Rev 5), A816 | Approved p.52, p.55; Rev 5 p.14 |
| Wall types | A003 (EW1–EW9) | Approved p.20 |
| Doors | Door schedule A800 | Approved p.51 |
| Roof | A132 Roof Plan Notes | Rev 5 p.4 |
| Canopies | A700 (Rev 5), A701 | Rev 5 p.13; Approved p.49 |
| Sun-shade | A702 note | Approved p.50 |
| Utility yard | A012 sections B2/B3/A3 (Rev 5); A302 west screening elevation | Rev 5 p.2; Approved p.33 |

## 2. Material / system schedule

| ID in model | Material / system (as printed) | Documented finish | Where it applies in the model | Status |
| --- | --- | --- | --- | --- |
| `BRK-1` | Brick veneer — Endicott Clay Products, smooth texture, **utility size 3 5/8" × 3 5/8" × 11 5/8"**, **Manganese Ironspot**, ultra dark mortar, black stainless drip plates | named | All EW1/EW2 faces: podium south, east (12'), north (B') and west faces; all faces of the high west block incl. its parapet; recess returns; H' jog. Confirmed by BRK-1 tags on all four elevations and brick hatch at every sampled point. | DOC; **INT-color**; brick bond not stated → running bond, 3/8" joint assumed (**INT**) |
| `ACM-1` | Aluminum composite panel — Alucobond, dry reveal 1/2", **Bone White** | named | Lobby block (all levels), CW2 bay, lobby piers and east return at Level 1, all Level 2 low-roof walls, terrace closet, their parapets | DOC (tags N, E, S, W; light tone sampled); **INT-color**; panel joint layout **not modeled** |
| `ACM-2` | Alucobond, dry reveal 1/2", **Tri-Corn Black** | named | South recess back wall (6'–7'), J' south-east face around CW5, 11' face around CW6, and their parapets | DOC (ACM-2 tags S and E; black tone sampled); **INT-color** |
| `ACM-3` | Alucobond, wet seal, Tri-Corn Black | named | East side canopy (all faces incl. soffit) | DOC (A300 tag at the canopy; A701 plan tag ACM-3) |
| `ACM-4` | Alucobond, wet seal, Bone White | named | Main entry door canopy and door 100A canopy (all faces incl. soffit); solid door bay in CW3 ("architectural metal panel", A815) | DOC (A300 tags; A701 plan tag ACM-4). Door-bay panel = ACM-4 is **INT** (A815 says only "architectural metal panel"; the adjacent A300 tag is ACM-4) |
| `MTL-1` | Metal coping cap, color **match ACM-2** | named by reference | Tops of brick parapets (terrace perimeter, high block), top of generator enclosure wall | DOC (tags N, E, S, W, A302); manufacturer blank in legend |
| `MTL-2` | Aluminum coping cap, Alucobond, **match ACM-1**, integral with panel | named by reference | Tops of ACM-1 parapets (lobby, low roof, CW2 bay) | DOC |
| `MTL-3` | Aluminum coping cap, Alucobond, **match ACM-2**, integral with panel | named by reference | Tops of ACM-2 parapets (the three 17'-6" runs) | DOC |
| `BC-1_BC-2` | Brick cap, match BRK-1 | named by reference | Tops of transformer walls, north site wall, low site walls | DOC (A012, A302). Cap profile not modeled |
| `GLASS_G1_G2` | G1 clear vision insulated; G2 same, tempered — BOD Viracon 1" **VZE1-42** insulating HS/HS | product named; no color value | All storefront and curtain-wall vision glazing | DOC; represented as dark reflective glass because there is no interior behind it (**INT**) |
| `GLASS_G3_spandrel` | G3 insulated spandrel — BOD Viracon **V953 Medium Gray** | named | Spandrel band in CW2/CW3/CW4 (13'-8 5/8" to 16'-3 5/8") and CW1 (11'-8 1/2" to 13'-8 5/8") per A815 | DOC; **INT-color** |
| `FRAME_Beachstone_Gray` | Storefront YKK YES 45 TU, 2" × 4 1/2"; curtain wall YKK YCW 750 SSG TU, horizontals 2 1/2", verticals 2-sided structural silicone, 4" sill, 4" × 10" horizontal caps "as noted"; color **Beachstone Gray** | named | Mullion/frame overlay on every glazed opening, bay widths and heights from A811/A815/A816 | DOC sizes; **INT-color**; cap projection 8" beyond glass is **INT**; SF6 bays shown "EQ" → equal bays |
| `TPO_white` | Fully adhered / mechanically fastened **white TPO** roof (A132 notes) ; A003 EW8 shows TPO membrane up the back of the parapet | "white" | Roof surfaces at 32'-0", roof side of roof parapets, closet top | DOC; closet roof = TPO is **INT** |
| `GLASS_clear_laminated` | 1" laminated clear glazing on post-mounted spider fittings (A700) | clear | Drop-off canopy glass | DOC |
| `GLASS_GR-1` | Glass railing — Viva Railings "View" structural glass railing, no top rail; **powder coat white** (metal parts) | named | The three glass railing runs | DOC; white base shoe not modeled |
| `PAINT_match_ACM-1` | Steel-framed louvered sun-shade "painted to match ACM-1", AESS level 3 (A702) | named by reference | Sun-shade frame, beams, hips, louvers | DOC; **INT-color** (same as ACM-1) |
| `UNRES_canopy_steel_paint` | Exposed structural steel canopy framing, **"painted. Color TBD"**, AESS 3 (A700) | **TBD on drawing** | Drop-off canopy columns, beams, purlins | **UNRES** — neutral placeholder |
| `UNRES_painted_CMU` | "Painted CMU, **color TBD**" (A012) | **TBD on drawing** | Inside faces of generator enclosure; inner side of low site walls | **UNRES**; which side of the low wall is CMU is **INT** (brick put on the street side) |
| `UNRES_HM_door_paint` | Hollow metal exterior doors and frames "HM EXT" (A800) — no finish color in schedule | not given | Doors 110B, 102, 104, 210B, 001A, 001B (overlay leaves) | **UNRES**; door positions from plan tags ±1 ft (**INT**) |
| `UNRES_terrace_paving` | Terrace surface (paver hatch on A122) | not reviewed / not given on architectural sheets | Terrace floor at 15'-2" | **UNRES** — civil rooftop sheets CS-301 / CX-201 not yet reviewed |
| `UNRES_terrace_parapet_inner` | EW9 (amenity deck): architectural metal panel on the terrace side — which ACM finish is not tagged | not given | Terrace side of terrace parapets | **UNRES** |
| `CLAY_ground`, `CLAY_context` | — | — | Ground plane, north arrow, labels (site work excluded) | unchanged from v003 |

Aluminum entrance doors (100A, 100B, 100C, 101A, 200D) are "ALUM, integral with storefront / curtain wall" (A800) and are covered by the glazing and frame materials.

## 3. Missing or ambiguous information (flag list)

1. **No color values anywhere** — Bone White, Tri-Corn Black, Manganese Ironspot, Beachstone Gray, V953 Medium Gray, VZE1-42 are names only. All on-screen colors are approximations.
2. **Drop-off canopy steel: "Color TBD"** on A700. **Painted CMU: "Color TBD"** on A012.
3. **MTL-1 manufacturer/product blank** in the legend (only "match ACM-2").
4. **HM door and frame paint color** not in A800.
5. **Terrace paving and terrace-side parapet finish** not identified on the architectural sheets reviewed.
6. **Brick bond, mortar joint size and brick-insert (EW2) panel pattern** not stated on the sheets reviewed; specifications (Division 04) not reviewed.
7. **ACM panel joint layout** is drawn on the elevations but not dimensioned; not modeled.
8. **"4 × 10 horizontal caps as noted"** — locations read from A815/A811 leaders (curtain walls: 9'-11 5/8", 13'-8 5/8", 16'-3 5/8", 25'-10"; storefronts: at the transom line); how far they project beyond the glass is not dimensioned.
9. **Future signage zones** on the north elevation are excluded (signage not in scope).
10. Specifications (`00 SPECIFICATIONS…PERMIT SET.pdf`) were **not** reviewed in this pass; they may resolve items 3–6.
11. Revision caution: legend sheets A300/A301 and A815 are Rev 5; A302, A811, A816, A800, A003, A701, A702 are permit / Rev 3 issue. No conflicts found between them. V-1 (revisions 6–10 not in hand) still open.

## 4. Representation rules used in Blender

- All materials are Principled BSDF, procedural, physically plausible roughness; no image textures, no brand-specific assets.
- Brick: procedural brick pattern sized to the **documented utility module** (12" × 4" coursing including a 3/8" joint), applied by world position so courses line up around corners.
- Placeholders: one flat neutral mid-grey per unresolved item, each with `UNRES_` in its name so it can be found and replaced.
- Lighting: neutral daylight (sun + uniform sky), no color grading, for material review only.
