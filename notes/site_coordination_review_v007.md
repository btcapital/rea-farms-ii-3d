# Site coordination review v007

Date: 2026-09-21
Scope: three targeted site questions left open by `notes/site_control_v006.md`. v001–v006 untouched. Paths relative to `source_documents\00 PLANS\`. Positions are in the model's building coordinates (ft; origin grid 1' × K'); "x" is east–west, negative = west of the building.

Confidence: **High** = two or more independent documents agree, or a written dimension governs · **Medium** = one document plus consistent circumstantial evidence · **Low** = inference only.

---

## Target 1 — Transformer enclosure position

### Sources reviewed

| Sheet | File, PDF page | Printed revision / date | What it shows |
| --- | --- | --- | --- |
| CS-101 Dimension Control Plan | `Permit_Pricing CDs 09.30.25\02 CIVIL & LANDSCAPE…PERMIT SET.pdf` p.3 | permit 09/29/2025 | Enclosure in a **different, earlier location** (x ≈ −34, y ≈ 66–82) |
| CS-101 | `Approved Civil\APPROVED-LDCP-2025-00715.pdf` p.4 | rev 1 10.31.25, rev 2 12.12.25 | Enclosure east wall at x = −14.1 / −12.9 (inner / outer face), y = 73.1 → 92.1 |
| CS-101 | `Revision 5\02 Civil & Landscape…REV 5 2026.02.12.pdf` p.2 | "5 – 02.11.26" | **Identical** to the approved civil |
| CS-101 and CG-101 | `Revision 5\Rea Farms 2 - Civil Drawings 03.17.26.pdf` p.7, p.3 | rev 6 03.10.26 "Wall Revisions" | **Identical** position again. CS-101 note beside it: "**APPROXIMATE LOCATION OF DUKE TRANSFORMER AND SCREENING WALL. DESIGN BY OTHERS.** Contractor to utilize same door configuration as dumpster enclosure." |
| A012 Utility Yard Plan | `Permit_Pricing…\03 ARCHITECTURAL…` p.5; `Approved Set\APPROVED-COS-001319.pdf` p.23; `Revision 5\03 Architectural…` p.2 | permit E 09/29/2025; approved; **Rev 5 02/27/2026** | East wall at x = −11.84 / −10.73 in **all three issues** (unchanged). The Rev 5 issue adds, inside revision-5 clouds, **written dimensions tying the enclosure to the building**: 12'-8 3/8" to grid 1, 15'-9 3/4" "to transformer pad (10'-0" min)", 10'-5 3/4" "to transformer pad (10'-0" min)", 14'-8", 7'-0 3/4", and "3' min clear in front of transformer" |
| A112 Level 1 Dimension Plan | Rev 5 p.3 | Rev 5 02/27/2026 | Same position as A012 |
| **S141 Enlarged Foundation Screen Walls** | `Revision 5\04 Structural…` p.11 | **Rev 5 02/27/2026**, sealed | Wall foundations and 8" CMU walls for the enclosure; east wall at x = −11.87 / −10.76 measured from structural grid 1 — **matches the architectural position to 0.03 ft** |
| E010 Electrical Site Plan | `APPROVED-COS-RV-001319-001.pdf` p.2 | rev 10 05/06/2026, county-stamped 6/18/2026 | Transformer and enclosure drawn on the architectural background. General note 2: contractor to meet the electricity provider "before proceeding with the installation of primary conduit and/or **utility transformer pad**". RTAP narrative for revs 8/10 concerns tenant disconnects and conduits only |
| Revision 5 log | `Revision 5\_00 REVISION LOG 2026.02.27…pdf` | 02.27.2026 | "Civil – no revisions included". Architectural items do not mention the enclosure position |

### Finding

- The civil position is **not a revision-6 change**. It has been identical on every civil issue since at least the 12.12.25 approved civil set. "Rev 6 – Wall Revisions" added the retaining-wall note and wall grades, not a new enclosure location. My v006 note that "the civil sheet is the later one" was therefore misleading on this point.
- The civil sheet itself calls its enclosure an **approximate location, design by others**.
- The party that *does* design it — architectural A012 with written, clouded Rev 5 dimensions, and structural S141 with its foundations — agree with each other to 0.03 ft.
- Conclusion: the 2.2 ft offset is a **civil background mismatch**, not a coordination change.

**Resolved: yes. Confidence: High. Geometry change: none** — the enclosure stays at the architectural / structural position already in v005–v006.
Still worth telling the design team: the civil background should be updated, and the final pad location is subject to Duke Energy (E010 note 2).

---

## Target 2 — South-west low site wall height

### Sources reviewed

| Sheet / detail | File, PDF page | Revision | What it shows |
| --- | --- | --- | --- |
| A012 section **B2 "Section at Low Site Wall"** | Rev 5 arch. p.2 | Rev 5 02/27/2026 | **T.O. masonry 2'-8"** above Level 01. The wall is drawn as a **retaining wall**: on its painted-CMU side the ground is just below Level 01; on its brick (BRK-1) side the ground is lower — "grade varies, see civil" |
| A012 section B3 "Section at North Transformer Site Wall" | same | same | T.O. masonry **3'-4"**; "sidewalk – see civil" just below Level 01 on one side, lower "grade varies" on the other |
| S141 elevations CMU-1, CMU-2, CMU-3 | Rev 5 struct. p.11 | Rev 5 02/27/2026 | Low wall top tagged **2'-8"** above the Level 1 datum; top of footing −6'-0". CMU-1 notes "coord. wall cap and rail details with arch docs" |
| A302 west screening elevation | Approved set p.33 | Rev 3 | Low wall top at the same height, BC-1 brick cap |
| CG-101 | civil 03.17.26 p.3 | rev 6 03.10.26 | At this wall: "**TW: 659.71 / BW: 656.98**", and "BW: 656.44" at its south-east end |
| CG-101, transformer wall (the key to the civil notation) | same | same | The **same wall** carries both "**TW: 659.87** / BW: 655.53" **and** the note "proposed retaining wall, **top elev. 663.63**" |

### Finding

On CG-101 the transformer wall is given *both* TW 659.87 and a top elevation of 663.63 (= FFE + 3'-4", exactly A012's T.O. masonry). So on this civil sheet **"TW" is the finished grade on the high (retained) side, not the top of the masonry**; "BW" is the grade on the low side.

Applied to the south-west wall: TW 659.71 is the retained grade behind it (0.59 ft below the floor — what A012 B2 draws), BW 656.98 / 656.44 is the street-side grade, and the masonry top is A012's and S141's +2'-8" (662.97), which stands about 3.3 ft above the retained side as a guard.

**The two values describe different things on the same wall; there is no conflict.**

**Resolved: yes. Confidence: High** (architectural and structural agree on +2'-8"; the civil notation is demonstrated on the same sheet).
**Geometry change — wall: none.** **Geometry change — ground: yes.** v006 had interpolated the ground *inside* this wall down to the street level. A012 B2 and TW 659.71 show it is retained fill at about 659.71. v007 adds that fill. (Incidentally this confirms the v004 interpretation: painted CMU on the inner side, brick on the street side.)

---

## Target 3 — Transformer access / gate condition

### Sources reviewed

| Sheet / detail | File, PDF page | Revision | What it shows |
| --- | --- | --- | --- |
| **S141 elevation 7 "CMU-5"** (the west, gate side) | Rev 5 struct. p.11 | Rev 5 02/27/2026 | Walls **9'-4" tall**, from top of footing **−6'-0"** to top **+3'-4"**; a **full-height double-leaf gate** whose bottom is at the footing level, i.e. at the *low* grade |
| S141 elevations 8 "CMU-6", 9 "CMU-7", 6 "CMU10" | same | same | The other three enclosure walls are also 9'-4" tall from −6'-0"; CMU10 steps its footing up toward the stair |
| S141 plan | same | same | Footing elevations −6'-0" all round the enclosure; "see civil and arch drawings for stair on grade extents" |
| A012 plan | Rev 5 arch. p.2 | Rev 5 | "Gate – see civil"; two 3'-0" gate leaves on the west side; "3' min clear in front of transformer" |
| A302 west screening elevation | Approved p.33 | Rev 3 | Gate drawn from the low grade line up to the +3'-4" wall top |
| CG-101 | civil p.3 | rev 6 03.10.26 | Spot **655.32** with its leader ending **at the gate line** of the enclosure; BW 655.53 at the north-west corner; **659.94** with its leader ending on the **east side of the east wall**, i.e. on the walk, not inside |
| CS-101 note | civil p.7 | rev 6 | "Contractor to utilize same door configuration as dumpster enclosure" |
| E010 | RV-001 p.2 | rev 10 05/06/2026 | Transformer inside the enclosure; conduits to the property edge to the west |

### Finding

There is no missing stair or ramp. **The inside of the transformer enclosure is at the low, west-street level (about 655.3), entered at grade through the west gate.** The enclosure's east and north walls retain the building-side walk (about 659.9), which is why they are 9'-4" tall structurally while showing only 3'-4" above the floor level. No steps, landing or ramp are drawn because none are needed.

The 4.6 ft "drop at the gate" in v006 was **my error**: I read the 659.94 spot as the pad elevation. Its leader ends on the walk east of the wall.

**Resolved: yes. Confidence: High** for "interior at the low level" (structural gate elevation + civil spot at the gate + A302). **Medium** for the exact pad elevation: 655.32 is written at the gate; a flat pad at that elevation is assumed, and the final pad is by Duke Energy.
**Geometry change: yes** — pad lowered to 655.32 and the terrain inside the enclosure lowered with it. The gate itself is still not modeled (no dimensions beyond the two 3'-0" leaves).

---

## Outcome

All three issues are resolved from the documents, and both geometry changes are document-supported, so **v007 was created** (`notes/site_comparison_v006_to_v007.md`). Nothing was guessed; no access solution was invented.

## Suggested notes to the design team (no longer blocking)

1. Civil CS-101/CG-101 show the transformer enclosure about 2.2 ft west of A012/S141 and label it "approximate". Please update the civil background to the A012 Rev 5 dimensions, and confirm the final pad location once Duke Energy has approved it.
2. Please confirm the transformer pad elevation inside the enclosure (model uses 655.32, the CG-101 spot at the gate).
3. Please confirm that on CG-101 "TW" means the high-side finished grade (as the transformer wall's TW 659.87 / top elev. 663.63 implies), so that the south-west low wall top is +2'-8" (662.97) as on A012 and S141.
4. Still open from earlier passes: the CS-101 canopy outline is an older design; architectural revisions 6–10 are not in hand.
