# Lobby visual-refinement control document v023 (on the approved v019 lobby + v021 Pass 2)

**STATUS (2026-09-23): APPROVED — CURRENT APPROVED BUILDING II MODEL v023 (lobby phase complete). Viewer baseline v026. See `notes/building_II_status_2026-09-23.md`.**

Date: 2026-09-23 · Applies to: `scripts/build_shell_v023.py` → `models/building_shell_v023.blend` · Baseline: v021 (= approved v019 architecture + Pass 2). v023 is v021 rebuilt by the identical code with a text-patched refinement layer. **No architectural geometry is changed**: shell, Stair 1 (rise / run / landing), wood wall extent and box pattern, Level 2 opening, curtain wall, glass guards, the seven pendants and their positions, porcelain layout, banquettes, DP-01 geometry, ID101 furniture positions, planter positions, directory location, and the viewer navigation (viewer v020 / v022 files untouched) are exactly as before. Everything in this note is a presentation / design assumption (**A**) unless a source is quoted.

## 1. Wood-wall lights (64 BEGA 33590, 3500 K, positions and count unchanged)
| | v021 | v023 |
| --- | --- | --- |
| Light | omni point, 0.7 W, 0.12 ft in front of the fixture centre | **spot 1.8 W, 105° cone, blend 0.95**, at the fixture base, aimed 17° off vertical back toward the wall (grazing down the wood) |
| Lens / emitter | full front face, strength 0.40 | **⅜ in. exit slot at the fixture base**, strength 1.4 (small area, reads as the light source without a glowing face) |
| Body | black 0.02, rough 0.5, metallic 0.3 | **0.05 charcoal, rough 0.55, metallic 0.35** |
Result: the wall reads as walnut with warm scallops below each fixture; the fixtures recede to dark cylinders.

## 2. Stair dark metal (PT-02 tone; geometry untouched)
Base 0.055 / rough 0.42 / metallic 0.65 → **base 0.115 (charcoal-gunmetal), roughness 0.46–0.62 with object-space noise, metallic 0.45**. Same material drives the shoes and rails. Combined with the fill light, the underside keeps surface detail in shadow.

## 3. Lounge chairs (ID101 positions exact; footprint 2.2 × 2.3 ft unchanged; design assumption)
Rebuilt procedurally: 0.07 ft (⅞ in.) wood members, front posts to arm height, **rear posts raked 0.22 ft over 2'-9"** (about 7°), side / front / rear rails, thin seat deck, **3 in. seat cushion and 2⅜ in. raked back cushion**, arms with a small overhang, bevel modifiers (cushions 20 mm × 3 segments, frame 5 mm × 2). Cushion fabric 0.84 / 0.81 / 0.75, roughness 0.92, sheen 0.35 (woven textile response, no gloss). Frame walnut tone.

## 4. Tables (positions unchanged)
Top 1'-4" Ø, **thickness 5⁄8 → 7⁄16 in.**, 32-sided; **pedestal Ø 1.7 in → 1.1 in**; base Ø 10 in → 9 in, 3⁄8 in. thick; bevels 4 mm. Dark bronze metallic.

## 5. Plants (SP-01 planters unchanged: size, taper, positions)
Sphere clusters replaced by a **procedural branching plant**: leaning tapered trunk, 7 tapered branches at 38–62° tilt with one sub-branch each, 12–16 elliptical leaves along the outer 60 % of each branch, tip clusters, 10 crown leaves; random yaw / tilt / size per leaf (seeded, repeatable). One branch mesh + one leaf mesh per plant (about 130 leaves, roughly 1,300 triangles each plant). About 4 ft above the pot. Not a species.

## 6. Artwork (positions unchanged; assumption)
Generated **landscape-inspired** images: pale grey-blue sky gradient, three soft ridges (blue-grey haze → sage), warm-grey foreground, fine grain; no text, logos or saturated colour. A1 6 × 4 ft on the Level 2 west wall, A2 2 × 3½ ft by door 101B.

## 7. Pendants (count 7, positions unchanged)
Cables **0.19 in. black → 1⁄16 in. dark grey** (28 cables); ring emitters 9.0 → **4.2, warmer** (1.0 / 0.86 / 0.68); frames use the charcoal fixture material; 4 mm bevel on the tube boxes.

## 8. Displays — documentation conclusion (no change made)
See the report: the permit set documents one 55" inset TV on the elevator block's north face (ID201 B1, ID301 B4 / C2) with a TV receptacle on the revised Level 1 power plan (RV-001319-001, sheet E110, circuit DP1H-8,10,12); the XL Media quote (8/10/2026) procures one "Lobby Display" 75" portrait monitor on a surface portrait wall mount, no location. No document shows two displays; the quote differs in size, orientation and mounting from the inset detail. **Stopped as instructed**: the 75" directory stays where approved and the TV is not added until the owner decides.

## 9. Materials
Walnut: same vertical grain, ramp 0.225/0.135/0.078 → 0.36/0.235/0.14, **plus a 0.35-scale tonal variation** (10 % mix toward a 0.82 multiplied tone) to break repetition; treads a shade darker. FAB-01 leather 0.25/0.215/0.185 with roughness 0.50–0.62 noise. PT-01 First Star keeps its colour, roughness 0.62 → 0.67–0.77 noise. POR-01 keeps the 47 in. module; roughness 0.38 → 0.54–0.64, tonal variation 18 % → 10 % (matte commercial). PT-02 roughness 0.32–0.45 noise. Glass: the documented neutral glass is unchanged (already clear with 7 % gloss).

## 10. Presentation lighting (render aids, hidden in the saved file)
Sun + physical sky unchanged (v010). Added `LOB_A_V23_fill_daylight_CW1` (30 × 24 ft area, 115 W, cool daylight, just inside the curtain wall facing in) and `LOB_A_V23_fill_ceiling_soft` (22 × 16 ft area, 90 W, warm-neutral, under the coffer facing down). Exposure 0.45 → 0.55, AgX view transform unchanged.

## 11. Cameras
The three review cameras unchanged. Added **temporary** `Cam_lobby_A_04_seating` at (131.8, 97.2, 5.0) looking at (120.8, 85.8, 3.0), 28 mm, for furniture / material evaluation only (not a viewer viewpoint).
