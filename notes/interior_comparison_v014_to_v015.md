# Comparison — building_shell_v014 → building_shell_v015 (first tenant test fit: Concept_A_CNSA_ASC)

Date: 2026-09-21
Basis: `notes/tenant_testfit_control_v015.md` (written before tenant geometry was built). Source: `tenant_testfits\CNSA_ASC\ASC Rea Farms PRESENTATION PLAN v3 20260915.pdf`. The plan is modeled as drawn; nothing was redesigned.

## Validation of the files

| Check | Result |
| --- | --- |
| Frozen v001–v014 files (153 files: models, scripts, notes, reports, all 79 renders) | SHA-256 identical before and after: **0 changed** |
| Tenant PDF | SHA-256 identical before and after (read-only) |
| `source_documents\Building I` | not opened; aggregate count / size / newest date identical to the baseline |
| `source_documents\Building II` | 360 files, 0 differences |
| v014 objects inside the v015 file | **1,796 of 1,796 identical** (geometry or camera/light placement, collection, materials, visibility flags); none removed |
| `BASE_…` collections | object counts unchanged; nothing added to or removed from any base collection |
| New objects | **313**, every one inside `Building_II > TENANT_CONCEPTS > Concept_A_CNSA_ASC` (or its sub-collections): 242 meshes, 56 text labels, 13 cameras, 2 review lights |
| Only structural change to v014 content | the empty placeholder collection `Concept_A` is named `Concept_A_CNSA_ASC` in this version; `Concept_B` and `Concept_C` remain empty |

`build_shell_v015.py` = `build_shell_v014.py` + one data dictionary (`TENANT_CONCEPTS["Concept_A_CNSA_ASC"]`) + a generic `build_tenant_concept()` function. A future Concept_B, Concept_C or a revised plan is one more dictionary. My first two full v015 builds were deleted and rebuilt (three render cameras had been created outside the concept collection); no approved file was involved.

## Collection layout

`Concept_A_CNSA_ASC` (partitions, demising partition, bay dividers, floor markers, table proxies) → `…_rooms` (57 room plates + 18 circulation plates, each carrying `room_id`, `room_name`, `printed_sf`, `modeled_sf`, `enclosure`) · `…_labels` (56 flat text labels) · `…_viewpoints` (10 eye-level cameras + 3 review cameras) · `…_underlay` (registered image of the tenant sheet, hidden) · `…_review_lighting` (2 soft overhead lights, not a design) · `…_ambiguous_perimeter_outline_walls` (28 hidden objects). Hiding or deleting `Concept_A_CNSA_ASC` removes the whole concept and leaves v014 intact.

## Geometric comparison with the source plan

| # | Item | Result |
| --- | --- | --- |
| 1 | **Registration** | Successful. Uniform, no rotation. Fitted scale **1.0000158**, rotation **0.0006°**, 2,875 matched points, **RMS 0.027 ft (⅓"), max 0.070 ft (⅞")**; every anchor group (four exterior walls, lobby / Stair 1, elevator, Stair 2, electrical / riser rooms) is below 0.031 ft RMS |
| 2 | **ASC area** | modeled **12,444 SF** vs printed 12,503 SF (**−0.5 %**, −59 SF) |
| 3 | **Shell area** | modeled **5,713 SF** vs printed 5,716 SF (**−0.05 %**, −3 SF) |
| 4 | **Partition positions** | partitions are generated directly from the drawing's own vector coordinates (face-to-face, drawn thickness), so their error relative to the drawing is the registration residual (≤ 0.07 ft). Independent check: the modeled room area (fill minus extracted partitions) matches the printed SF **within 1.5 SF in 35 of the 45 walled rooms**; the rest differ by 2–15 SF where a room borders a base-building wall or overlaps another room (see the room schedule) |
| 5 | **Door positions** | **not measurable — the plan draws no tenant doors.** None were modeled |
| 6 | **Columns** | pinch points: H-7.2 (1.2 ft off the OR A-050 wall in the sterile corridor), H-5 (3.2 ft off the OR wall, same corridor), F-3 (leaves about 5.6 ft in the corridor outside Stair 2 door 110A). Free-standing inside rooms: H-3 (STERILE PROCESSING), H-8.3 (LOCKER A-043), E.1-2.8 (JAN A-025), G-9 (WAIT), A-3, K-3.1, K-5, K-8.3. Within or against partitions: F-4, F-7, G-8, K-6, A-1, A-5, A-7, C-1, K-2. No column was moved |
| 7 | **Exterior glazing** | every north-side room partition ends on the continuous CW3 curtain wall; two partitions and toilet A-010 end on the CW4 glazed corner, and a partition is drawn on column line 1 about 1.4 ft inside CW4; five south partitions end inside SF1 windows (x = 44.14, 62.05, 110.59, 122.59, 128.00). ORs, STERILE INSTRUMENTS, CLEAN, both LOCKER rooms, LOUNGE and MECH. PUMP have existing windows. 28 room-outline segments lying along the exterior wall are kept hidden rather than shown over the glass |
| 8 | **Stairs / elevator / core** | no overlap with Stair 1, Stair 2, the elevator, lobby walls or electrical / riser rooms. **Lobby door 101D opens against the east wall of PRE/POST A-009** — no route is shown from it. Tenant entry is lobby door 101C into WAIT; exterior door 100A serves the DISCHARGE VESTIBULE; Stair 2 door 110A opens into a tenant corridor |
| 9 | **Shafts** | none on Level 1; no conflict. (The Level 2 mechanical shaft and exhaust shafts sit above PRE/POST A-009 / A-012, WAIT, and the corridor outside Stair 2 respectively; vertical services were not evaluated) |
| 10 | **Rooms not determinable with confidence** | PACU bays and the 64–65 SF PRE/POST bays (single lines, open fronts, yet printed areas net of a wall allowance); RECEPTION and NURSE STATION (fully walled rectangles, no counter or opening); NURSE 19 SF and CONTROL 41 SF (labels outside small fills, treated as open alcoves); the two LOCKER rooms (printed area includes the toilet drawn inside); WAIT (unlabeled 62 SF arm to the corridor); EM. ELECT. ROOM (drawn as existing, only "future" in the base building) |
| 11 | **Circulation pinch points visible in the drawing / model** | the three columns in item 6; the 4.4 ft passage between the DISCHARGE VESTIBULE and the main corridor; 4.5–5.0 ft staff corridors at the LOCKER / JAN / CLEAN cluster and along the east side of RECEPTION / OFFICE; 3.8 ft gap between CONTROL and PROCEDURE A-041. No code-compliance statement is made |

Base-building condition to keep in view: almost all of the ASC stands where the base building provides **no slab on grade** (future slab, not in scope).

## Assumptions

Partition and demising height 10'-0"; demising thickness 4⅞"; bay dividers 7'-0" × 2" of unknown type; tables 3'-0" high; no ceilings; neutral materials lightly tinted by the plan's own color groups; two overhead review lights (not a lighting design); perimeter room-outline lines treated as ambiguous and hidden; EM. ELECT. ROOM east wall modeled from the tenant drawing because the base model has no wall there.

## Walkthrough preparation

Ten saved eye-level viewpoints at 5'-6" (`VP_A_01_ASC_entrance_arrival`, `VP_A_02_reception`, `VP_A_03_waiting`, `VP_A_04_main_clinical_circulation`, `VP_A_05_nurse_station`, `VP_A_06_pre_post_room`, `VP_A_07_procedure_room_approach`, `VP_A_08_operating_room`, `VP_A_09_sterile_processing`, `VP_A_10_staff_lounge`), each with a `title` property, plus room plates that carry name and area data.

**Ready for a browser walkthrough prototype?** Yes for a *viewpoint-to-viewpoint* prototype (jump between saved viewpoints, look around, toggle the concept, show room names and areas) and for free walking through the lobby, WAIT and all corridors. **Not yet** for continuous room-to-room walking: every walled room is a closed box because the source plan has no doors. A plan from McCulloch England Architects that shows doors (and the reception / nurse-station openings) would close that gap without any change to the workflow.

## Render time (160 samples, RTX A1000, OptiX)

Overlay 18 s · plan 78 s (3200 × 1800) · oblique 33 s · six first-person views 66–73 s each. Model file 2.7 MB → 2.8 MB.

## Renders (`renders/`)

`building_shell_v015_tenant_A_01_registration_overlay.png` · `…_02_L1_topdown_plan.png` · `…_03_L1_oblique_cutaway.png` · `…_04_fp_ASC_entrance.png` · `…_05_fp_reception_waiting.png` · `…_06_fp_main_clinical_corridor.png` · `…_07_fp_pre_post_room.png` · `…_08_fp_operating_room.png` · `…_09_fp_sterile_processing.png`

Other outputs: `notes/tenant_concept_A_CNSA_ASC_room_schedule_v015.json` (machine-readable room schedule) · `exports/tenant_underlay_Concept_A_CNSA_ASC_v015.png` (registered underlay image).
