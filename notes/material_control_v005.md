# Material control document v005 — after specification review

Date: 2026-09-21
Applies to: `scripts/build_shell_v005.py` → `models/building_shell_v005.blend`
Supersedes nothing: `material_control_v004.md` is unchanged and still describes v004. This document = v004 schedule **plus** what the project specifications add, confirm or contradict. Written before the final v005 build.

Specification reviewed: `source_documents\00 PLANS\Permit_Pricing CDs 09.30.25\00 SPECIFICATIONS_CSMC MOB 2_2025.09.29 - PERMIT SET.pdf` (554 pages, permit issue 09/29/2025; "p." below = PDF page). No later specification issue is in the folder; the Revision 5 log states no specifications were reissued. The 95% check-set specification was not used (superseded).

Status codes: **DOC** named in the documents · **INT** needed interpretation · **UNRES** unresolved → neutral placeholder · **CONFLICT** drawings and specification disagree (not resolved silently).

**General result:** the specifications name manufacturers, systems, coatings and installation rules, but for almost every exposed finish the **color is "as selected by Architect" or "match Architect's sample"**. The specification therefore resolves *no* color that the drawings left open. On-screen colors remain approximations of finish **names** (INT-color).

## 1. Schedule after specification review

| Material / system | Drawings (v004) | Specification adds | Spec ref. | Model change in v005 | Status |
| --- | --- | --- | --- | --- | --- |
| **BRK-1 brick** | Endicott, smooth, utility 3 5/8 × 3 5/8 × 11 5/8, Manganese Ironspot, ultra dark mortar, black SS drip plates | "Utility sized Endicott Clay Products Brick – Brick 1 with **Ultra Dark mortar (Holcim)**"; ASTM C216 **grade SW, type FBX**, "match Architect's sample"; **running bond** unless otherwise indicated; exposed joints **tooled slightly concave**; weeps/cavity vents **grey**; drip plates black stainless | 042000, p.99–100, 105, 115–116 | None needed — running bond and dark mortar were already modeled; v004's "running bond assumed" is now **documented**. Source note updated. | DOC; INT-color; joint thickness still not stated (3/8" modeled) |
| **ACM-1 / ACM-2 / ACM-3 / ACM-4** | Alucobond; dry reveal (1, 2) / wet seal (3, 4); Bone White (1, 4) / Tri-Corn Black (2, 3); 1/2" reveals | Basis of design **Alucobond Plus**, dry reveal with **integral coping**; alternate Mitsubishi Alpolic; panel **0.236 in.** thick; **three-coat fluoropolymer**; color "as indicated by manufacturer's designations and to match Architect's finishes on elevations"; "dry seal and wet seal systems – see elevations" | 074213.23, p.223, 227 | None | DOC; INT-color; panel joint layout not modeled |
| **MTL-1 coping** | "Metal coping cap", match ACM-2, manufacturer blank | Manufactured coping system; **galvanized steel 0.028 in.**, smooth, **two-coat fluoropolymer**, color "as selected by Architect"; note "(confirm option for all aluminum coping systems with owner)"; table of contents calls the section "Prefinished **Alum.** Copings" | 077100, p.257, 259–260 | None | DOC finish type; **CONFLICT-minor** (steel vs aluminum inside the spec itself); color by reference to ACM-2 |
| **MTL-2 / MTL-3 copings** | Alucobond aluminum coping integral with panel, match ACM-1 / ACM-2 | Confirmed: ACM system "with integral coping cap" | 074213.23, p.223 | None | DOC |
| **Frames (storefront / curtain wall)** | YKK YES 45 TU 2" × 4 1/2"; YKK YCW 750 SSG TU; **Beachstone Gray** | YKK AP America; "**painted finish** match Architect's sample", "**painted 3-coat fluoropolymer**"; curtain wall two-sided structural-sealant-glazed; "see projected mullions in sections and elevations" | 084113 p.346, 349; 084413 p.363 | **Changed:** frame material is now a non-metallic painted finish (v004 had used a metallic value). Color unchanged. | DOC; INT-color. **CONFLICT-minor:** spec writes the storefront as "**YES451 TU** Front Set", A811 says "YES 45 TU" |
| **Glass G1 / G2 / G3** | Viracon 1" VZE1-42 HS/HS; G2 tempered; G3 spandrel V953 Medium Gray | Same products listed as basis of design; spacer black; exposed glazing sealant color by Architect | 088000, p.389, 391–392 | None | DOC; INT-color |
| **Drop-off canopy glass** | 1" laminated clear on spider fittings | "GL-4: laminated safety canopy glazing … 1 inch, fully tempered … confirm thickness with span" | 088000, p.395 | None | DOC |
| **Drop-off canopy steel paint** | "Painted. **Color TBD**", AESS level 3 | Exterior painting is Sherwin-Williams; "**Colors: as selected by Architect** from manufacturer's full range"; steel systems listed with several sheen options left open. Sections 051200 / 051213 (AESS) are referenced but **not included** ("see structural drawings") | 099113, p.496–498, 503; TOC p.3 | None | **UNRES** — placeholder kept |
| **Painted CMU (utility yard)** | "Painted CMU, **color TBD**" | S-W latex system on block filler; flat / low-sheen / semi-gloss / gloss all left in the schedule; color by Architect. CMU faces "match Architect's sample" | 099113 p.503; 042000 p.104 | None | **UNRES** (color and sheen) |
| **Hollow-metal exterior doors / frames** | A800 "HM EXT", no color | Exterior HM galvanized A60, **factory primed**; finish painting under 099113 → color by Architect; "paint both sides and edges of exterior doors" | 081113 p.325, 328; 099113 p.501 | None | **UNRES** |
| **Terrace paving** | Paver hatch on A122 only | "Plaza-deck pavers: heavyweight hydraulically pressed concrete, square edged, **2 in. thick, 24 in. square**", **on pedestals** over hot fluid-applied waterproofing; "Color: as selected by Architect" | 071413 ("Deck Waterproofing"), p.185–188 | **Changed:** placeholder now carries a 24" × 24" joint grid; color stays the neutral placeholder. Material renamed `UNRES-colour_terrace_pavers_24in_concrete_pedestal_set`. | Size **DOC**; **color UNRES**; stacked layout is **INT** (A122 hatch suggests more than one pattern; layout not dimensioned) |
| **Terrace-side parapet finish** | A003 EW9 "architectural metal panel", finish not tagged | Nothing further | — | None | **UNRES** |
| **Roofing** | White TPO (A132 notes) | "**Mechanically fastened** TPO roofing. **White** colored TPO"; walkways around roof units | 075423, p.233 | None (note updated) | DOC. **CONFLICT-minor inside the drawings:** A132 note 1 says mechanically fastened 60 mil, but the A132 plan labels say "fully adhered white TPO". No visual effect. |
| **Glass railing GR-1** | Viva "View" structural glass rail, no top rail, **powder coat white** | Viva VIEW (exterior terrace, surface mounted, no top rail); glass **laminated tempered, clear**, clear interlayer; metal finishes listed are **stainless steel** (dull satin No. 6 / ECM color electro-plated) | 057313, p.147, 149, 151–152, 155 | None (base shoe not modeled) | Glass DOC. **CONFLICT-minor:** legend says powder coat white; spec lists stainless finishes only |
| **Louvered sun-shade** | A702 / S133: **steel-framed**, (12) 1" × 10" in-fill louvers at 40°, 11" o.c. (S133: "1" × 10" **A36 plates**"), "painted to match ACM-1", AESS 3 | Section titled "Aluminum Horizontal Louvers": basis of design **Construction Specialties**, "no substitutions"; **extruded aluminum airfoil blades 10" high**, 1/4" aluminum plate outriggers, **welding not acceptable**; finish fluoropolymer powder coat or 3-coat Kynar "high metallic color coat"; color "as indicated" | 107113, p.534–537; TOC p.4 | **None — model still follows the drawings** (steel frame, flat 1×10 louvers, painted to match ACM-1) | **CONFLICT (significant):** custom welded steel with flat plate louvers (drawings) vs. manufactured aluminum airfoil system (specification). Needs the architect's answer. Flagged, not resolved. |
| **Sealants** | — | "Colors of exposed joint sealants: as selected by Architect" | 079200 p.304, 318 | None (joints not modeled) | UNRES; no visible effect at this level of detail |
| **Brick caps BC-1 / BC-2** | Match BRK-1 | Special brick shapes to match; nothing further | 042000 p.105 | None | DOC by reference |

Cast stone (047200) and EIFS (072419) sections exist in the specification, but neither material appears on the exterior elevations or legend reviewed; not used.

## 2. Material changes actually made in v005

1. `FRAME_YKK_Beachstone_Gray` → `FRAME_YKK_Beachstone_Gray_painted_fluoropolymer`: metallic 0.6 → 0 (painted, not anodized/metallic); roughness 0.40 → 0.35. Same color.
2. `UNRES_terrace_paving` → `UNRES-colour_terrace_pavers_24in_concrete_pedestal_set`: same neutral placeholder color, now with a 24" stacked joint grid.
3. Source notes on brick, TPO, canopy glass, railing glass and the three paint placeholders now cite the specification. No color value was changed anywhere.

## 3. Unresolved after specification review

| Item | Why it is still unresolved |
| --- | --- |
| Every color value | Specifications defer to "Architect's sample" / "as selected by Architect". Needs the approved color/finish submittals or physical samples. |
| Drop-off canopy steel paint color (and sheen) | A700 "color TBD"; spec "as selected by Architect". |
| Painted CMU color and sheen | A012 "color TBD"; spec leaves four sheen options. |
| HM door and frame paint color | Not in A800 or the specification. |
| Terrace paver color and laying pattern | Spec gives size only. |
| Terrace-side parapet finish (EW9 panel) | Not tagged on drawings, not in specification. |
| MTL-1 coping metal (steel or aluminum) and manufacturer | Spec internally undecided. |
| Sun-shade system | Drawings vs. specification conflict (above). |
| Railing metal finish | Legend vs. specification conflict (above). |
| Brick joint thickness; brick-insert (EW2) pattern; ACM joint layout; 4 × 10 cap projection | Not dimensioned in either. |
| Architectural revisions 6–10 (V-1) | Not in hand. |

Best next sources (not in the project folder): approved **submittals / color selections** for brick, mortar, ACM, paint, pavers and sun-shade, or the architect's finish schedule. Construction photos after cladding is complete could calibrate colors, subject to the owner's rule that photos do not change the model without approval.
