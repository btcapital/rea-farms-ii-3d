// Rea Farms Building II - Review Prototype v025 (viewer version v025; MODEL version v023 = approved lobby baseline).
// v025 = v024 with viewer-only visual tuning: ACES filmic tone mapping and exposure, softer key / ambient lights, reduced edge lines.
// Navigation, collision, toggles, viewpoints and tools are the v024 code unchanged.
// v024 = the v022 viewer (v020 navigation framework: grids, Stair 1 surface, controls) showing the v023 export; furniture
// collision footprints and the baked wall-light graze come from the export data / GLB, not from viewer code.
// v020 adds to the approved v018 viewer: the v019 lobby concept as one toggleable GLB group, a "Lobby" one-click view state,
// four saved lobby viewpoints, a Base / Concept compare control, warm browser lights for the lobby, and a walkable Stair 1:
// viewer-only navigation ramps (run 1 -> landing -> run 2 -> Level 2) derived from the frozen tread geometry, with guard / void
// edges as fall protection. Walk speed, collision sub-stepping, measurement, plan mode etc. are unchanged from v018.
// Nothing here creates or edits building geometry. No door or opening is invented: walking is limited by grids exported from the model.
import * as THREE from 'three';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';
import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js';

const VERSION = 'v025';
const FT = 0.3048;                                   // model feet -> glTF metres
const EYE_FT = 5.5;                                  // 5'-6" eye height (unchanged)
const WALK_FT_S = 9.0, WALK_FAST_FT_S = 18.0, SUBSTEP_FT = 0.2;   // approved v017 values (unchanged)
const STAIR_FACTOR = 0.6;                            // modest climbing speed on the Stair 1 ramps
const STEP_FT = 1.0;                                 // largest surface-height change accepted in one sub-step (a riser is 0.571 ft)
const BODY_FT = 0.75;                                // body radius used for collision (unchanged)
const toWorld = (x, y, z) => new THREE.Vector3(x * FT, z * FT, -y * FT);        // model (x east, y north, z up) -> glTF (Y up)
const toFeet = (v) => ({ x: v.x / FT, y: -v.z / FT, z: v.y / FT });
const $ = (id) => document.getElementById(id);

const canvas = $('view');
const renderer = new THREE.WebGLRenderer({ canvas, antialias: true, preserveDrawingBuffer: true });
renderer.setPixelRatio(Math.min(window.devicePixelRatio, 1.5));
renderer.outputColorSpace = THREE.SRGBColorSpace;
renderer.toneMapping = THREE.ACESFilmicToneMapping;   // v025: filmic response keeps white walls, floor and emitters from clipping
renderer.toneMappingExposure = 1.0;
const scene = new THREE.Scene();
scene.background = new THREE.Color(0xcfd8e3);
scene.add(new THREE.HemisphereLight(0xffffff, 0x9a9488, 1.9));    // v025: 2.2 -> 1.9
const sun = new THREE.DirectionalLight(0xffffff, 1.9);              // v025: 2.0 -> 1.9
sun.position.set(0.797, 0.588, -0.140).multiplyScalar(300);                     // v010 sun: azimuth 80 deg, elevation 36 deg
scene.add(sun);
const lobbyLights = new THREE.Group();               // a few warm browser lights standing in for the 64 + 7 Blender fixtures (viewer only)
lobbyLights.name = 'viewer_lobby_lights';
for (const [x, y, z, i, d] of [[125.5, 89.2, 22.5, 44, 70], [111.5, 83.0, 14.0, 12, 45], [124.5, 98.0, 9.0, 22, 46], [131.0, 78.0, 9.0, 14, 40]]) {   // v025: slightly stronger warm fills under tone mapping
  const l = new THREE.PointLight(0xffd6a6, i, d * FT, 2);
  l.position.copy(toWorld(x, y, z));
  lobbyLights.add(l);
}
scene.add(lobbyLights);

const persp = new THREE.PerspectiveCamera(50, 1, 0.08, 3000);
const ortho = new THREE.OrthographicCamera(-50, 50, 50, -50, 0.1, 2000);
let camera = persp;
const orbit = new OrbitControls(persp, canvas);
orbit.enableDamping = true;
orbit.maxPolarAngle = Math.PI * 0.495;
const planCtl = new OrbitControls(ortho, canvas);
planCtl.enableRotate = false;
planCtl.screenSpacePanning = true;
planCtl.enabled = false;
planCtl.mouseButtons = { LEFT: THREE.MOUSE.PAN, MIDDLE: THREE.MOUSE.DOLLY, RIGHT: THREE.MOUSE.PAN };

const FLOORS = ['both', 'lobby', 'L1', 'L2'];
const state = { mode: 'orbit', floor: 'both', walkKey: 'level1', measuring: false, presentation: false, data: null, groups: {}, grids: {},
                concept: null, yaw: 0, pitch: 0, pos: { x: 129.9, y: 79 }, z: 0, zTarget: 0, posByFloor: {}, keys: {}, selected: null,
                underlay: null, labels: null, highlight: null, measure: { points: [], marks: [], line: null }, fps: 0, ready: false, lobbyView: null };
const HOME = { pos: [-150, 300, 170], target: [95, 55, 10] };                     // model feet
const helpers = new THREE.Group();                    // highlight, measurement marks, labels: never picked or measured
helpers.name = 'viewer_helpers';
scene.add(helpers);

// ---------------------------------------------------------------- loading
async function init() {
  state.data = await (await fetch('assets/viewer_data_v025.json')).json();
  for (const [k, g] of Object.entries(state.data.walk_grids)) state.grids[k] = decodeGrid(g);
  const gltf = await new GLTFLoader().loadAsync(state.data.glb);
  scene.add(gltf.scene);
  gltf.scene.traverse((o) => {
    if (o.name.startsWith('GRP_')) state.groups[o.name] = o;
    if (o.isMesh) {
      const mats = Array.isArray(o.material) ? o.material : [o.material];
      for (const m of mats) { if (m.transparent) { m.depthWrite = false; } m.side = THREE.DoubleSide; }
    }
  });
  addEdgeLines(['GRP_Base_Interior_Level_1', 'GRP_Base_Interior_Level_2', ...state.data.concepts.map((c) => c.group)]);
  addLobbyEdgeLines();
  buildHighlight();
  buildConceptSelector();
  setConcept(state.data.concepts[0].id);
  buildLobbyViews();
  bindUi();
  setMode('orbit');
  resetView();
  applyUrlParameters();
  state.ready = true;
  $('loading').remove();
}

function decodeGrid(g) {
  const cells = new Uint8Array(g.nx * g.ny);
  g.rows.forEach((runs, j) => {
    let i = 0, blocked = 0;
    for (const n of runs) { if (blocked) cells.fill(1, j * g.nx + i, j * g.nx + i + n); i += n; blocked ^= 1; }
  });
  return { ...g, cells, rows: undefined };
}
// ---- navigation surface: grid cell (open / blocked) + height (floor, or the Stair 1 ramps / landing exported from the frozen treads)
function gridKeyFor(floor) { return floor === 'L2' ? 'level2' : (lobbyOn() ? state.data.floors.L1.grid_with_lobby_concept : state.data.floors.L1.grid); }
function otherKey(key) { return key === 'level2' ? gridKeyFor('L1') : 'level2'; }
function cellOpen(key, x, y) {
  const g = state.grids[key], i = Math.floor((x - g.x0_ft) / g.cell_ft), j = Math.floor((y - g.y0_ft) / g.cell_ft);
  return i >= 0 && j >= 0 && i < g.nx && j < g.ny && g.cells[j * g.nx + i] === 0;
}
function stairAt(key, x, y) {
  for (const s of state.data.stair_surfaces) {
    if (key && !s.grids.includes(key)) continue;
    const r = s.rect;
    if (x <= r[0] || x >= r[1] || y <= r[2] || y >= r[3]) continue;
    return s;
  }
  return null;
}
function surfaceAt(key, x, y) {                        // height of the walkable surface in this grid, or null if blocked
  if (!cellOpen(key, x, y)) return null;
  const s = stairAt(key, x, y);
  if (!s) return state.grids[key].floor_z_ft;
  if (s.kind === 'plane') return s.z;
  const d = ((s.axis === 'y' ? y : x) - s.start) * s.direction;
  return Math.min(s.z_max, Math.max(s.z_base, s.z_base + s.riser_ft * (0.5 + d / s.tread_ft)));
}
function standAt(x, y, zRef, keys) {                    // the body (radius 0.75 ft) must fit and the surface must be within one step of zRef
  for (const key of keys) {
    const z = surfaceAt(key, x, y);
    if (z === null || Math.abs(z - zRef) > STEP_FT) continue;
    let ok = true;
    for (let k = 0; k < 8 && ok; k++) {
      const a = k * Math.PI / 4, zr = surfaceAt(key, x + BODY_FT * Math.cos(a), y + BODY_FT * Math.sin(a));
      ok = zr !== null && Math.abs(zr - z) <= STEP_FT + 0.5;
    }
    if (ok) return { key, z };
  }
  return null;
}
function keysNow() { return [state.walkKey, otherKey(state.walkKey)]; }
function isOpen(x, y) { return cellOpen(state.walkKey, x, y); }
function canStand(x, y) { return !!standAt(x, y, state.zTarget, keysNow()); }
function nearestStandable(x, y) {                     // used after a teleport that sits close to a wall; never crosses a solid cell
  const here = standAt(x, y, state.zTarget, keysNow());
  if (here) return { x, y, ...here };
  for (let r = 0.25; r <= 3.0; r += 0.25) {
    for (let k = 0; k < 16; k++) {
      const a = k * Math.PI / 8, nx = x + r * Math.cos(a), ny = y + r * Math.sin(a), st = standAt(nx, ny, state.zTarget, keysNow());
      if (!st) continue;
      let clear = true;
      for (let t = 0.125; t < r && clear; t += 0.125) clear = cellOpen(st.key, x + t * Math.cos(a), y + t * Math.sin(a));
      if (clear) return { x: nx, y: ny, ...st };
    }
  }
  return null;
}
function settle(x, y, key) {                          // place the walker on a surface (teleports); returns false if nothing standable nearby
  state.walkKey = key;
  state.zTarget = state.grids[key].floor_z_ft;
  const p = nearestStandable(x, y);
  if (!p) return false;
  state.pos = { x: p.x, y: p.y }; state.walkKey = p.key; state.zTarget = p.z; state.z = p.z;
  return true;
}
function walkFloorLabel() {
  if (stairAt(null, state.pos.x, state.pos.y) && state.zTarget > 0.3 && state.zTarget < 15.9) return 'Stair 1';
  return state.zTarget >= 8 ? 'Level 2' : 'Level 1';
}
function lobbyOn() { return $('t-lobby').checked; }

// ---------------------------------------------------------------- helpers built from the exported data
function addEdgeLines(groupNames) {                   // thin dark edges so plain neutral walls stay readable (display aid only)
  const mat = new THREE.LineBasicMaterial({ color: 0x3a4450, transparent: true, opacity: 0.55 });
  for (const name of groupNames) {
    if (!state.groups[name]) continue;
    const meshes = [];
    state.groups[name].traverse((o) => {
      const slab = (o.name + '|' + (o.parent ? o.parent.name : '')).includes('__BASE_Level');
      if (o.isMesh && !o.material.transparent && !slab && !o.name.startsWith('TEN_A_Room') && !o.name.startsWith('TEN_A_Circulation')) meshes.push(o);
    });
    for (const m of meshes) { const l = new THREE.LineSegments(new THREE.EdgesGeometry(m.geometry, 30), mat); l.raycast = () => {}; m.add(l); }
  }
}
function addLobbyEdgeLines() {                        // subtle edges on the built lobby elements only (not floor tiles, lights or paint overlays)
  const g = state.groups[state.data.lobby_concept.group];
  if (!g) return;
  const mat = new THREE.LineBasicMaterial({ color: 0x2a2220, transparent: true, opacity: 0.20 });   // v025: 0.35 -> 0.20
  const want = ['ARCH_WOOD_WALL', 'ARCH_STAIR_FINISH', 'ARCH_GUARDRAIL'];                            // v025: no outlines on chairs / directory
  g.traverse((o) => {
    // multi-material nodes load as a group of meshes named <node>_<n>, so match by inclusion
    if (o.isMesh && want.some((w) => o.name.includes('__' + w))) { const l = new THREE.LineSegments(new THREE.EdgesGeometry(o.geometry, 40), mat); l.raycast = () => {}; o.add(l); }
  });
}
function disposeObject(o) {
  if (!o) return;
  o.traverse((c) => { if (c.geometry) c.geometry.dispose(); const ms = c.material ? [].concat(c.material) : []; for (const m of ms) { if (m.map) m.map.dispose(); m.dispose(); } });
  if (o.parent) o.parent.remove(o);
}
function buildUnderlay(c) {
  disposeObject(state.underlay);
  state.underlay = null;
  if (!c.underlay) return;
  const u = c.underlay, w = (u.x1_ft - u.x0_ft) * FT, h = (u.y1_ft - u.y0_ft) * FT;
  const tex = new THREE.TextureLoader().load(u.image);
  tex.colorSpace = THREE.SRGBColorSpace;
  tex.anisotropy = 8;
  const mesh = new THREE.Mesh(new THREE.PlaneGeometry(w, h), new THREE.MeshBasicMaterial({ map: tex, transparent: true, opacity: 0.92 }));
  mesh.rotation.x = -Math.PI / 2;                     // image top -> north
  mesh.position.copy(toWorld((u.x0_ft + u.x1_ft) / 2, (u.y0_ft + u.y1_ft) / 2, state.data.floors[c.floor].floor_z_ft + 0.07));
  mesh.name = 'Tenant_plan_underlay_registered';
  mesh.visible = false;
  helpers.add(mesh);
  state.underlay = mesh;
}
function buildLabels(c) {
  disposeObject(state.labels);
  const group = new THREE.Group();
  group.name = 'Room_labels';
  const z = state.data.floors[c.floor].floor_z_ft + 11;
  for (const r of c.rooms) {
    if (!r.printed_sf) continue;
    const cv = document.createElement('canvas');
    cv.width = 512; cv.height = 192;
    const g = cv.getContext('2d');
    g.fillStyle = '#10151c'; g.textAlign = 'center'; g.textBaseline = 'middle';
    g.font = '600 64px Segoe UI, Arial'; g.fillText(r.name, 256, 62, 500);
    g.font = '52px Segoe UI, Arial'; g.fillText(`${r.printed_sf} SF`, 256, 138, 500);
    const tex = new THREE.CanvasTexture(cv);
    tex.colorSpace = THREE.SRGBColorSpace;
    const s = new THREE.Sprite(new THREE.SpriteMaterial({ map: tex, depthTest: false, transparent: true }));
    const [x0, y0, x1, y1] = r.rect_ft, w = Math.min((x1 - x0) * 0.92, 15) * FT;
    s.scale.set(w, w * 192 / 512, 1);
    s.position.copy(toWorld((x0 + x1) / 2, (y0 + y1) / 2, z));
    s.renderOrder = 10;
    group.add(s);
  }
  group.visible = false;
  helpers.add(group);
  state.labels = group;
}
function buildHighlight() {
  const plane = new THREE.Mesh(new THREE.PlaneGeometry(1, 1), new THREE.MeshBasicMaterial({ color: 0xffc400, transparent: true, opacity: 0.45, depthWrite: false, side: THREE.DoubleSide }));
  plane.rotation.x = -Math.PI / 2;
  plane.renderOrder = 5;
  const box = new THREE.LineSegments(new THREE.EdgesGeometry(new THREE.BoxGeometry(1, 1, 1)), new THREE.LineBasicMaterial({ color: 0xff9d00, depthTest: false, transparent: true, opacity: 0.95 }));
  box.renderOrder = 11;
  const h = new THREE.Group();
  h.add(plane); h.add(box);
  h.visible = false;
  helpers.add(h);
  state.highlight = { group: h, plane, box };
}

// ---------------------------------------------------------------- concepts (selector architecture: one entry per concept in the data file)
function buildConceptSelector() {
  const sel = $('concept');
  sel.innerHTML = '';
  for (const c of state.data.concepts) { const o = document.createElement('option'); o.value = c.id; o.textContent = c.label; sel.appendChild(o); }
  sel.addEventListener('change', () => setConcept(sel.value));
}
function setConcept(id) {
  const c = state.data.concepts.find((x) => x.id === id);
  if (!c) return;
  state.concept = c;
  $('concept').value = id;
  $('warning').textContent = c.warning;
  selectRoom(null);
  buildUnderlay(c);
  buildLabels(c);
  $('viewpoints').innerHTML = '';
  for (const vp of c.viewpoints) {
    const b = document.createElement('button');
    b.textContent = vp.title;
    b.dataset.vp = vp.id;
    b.addEventListener('click', () => gotoViewpoint(vp.id));
    $('viewpoints').appendChild(b);
  }
  applyVisibility();
}
function buildLobbyViews() {
  $('lobby-views').innerHTML = '';
  for (const vp of state.data.lobby_concept.viewpoints) {
    const b = document.createElement('button');
    b.textContent = vp.title;
    b.dataset.lv = vp.id;
    b.addEventListener('click', () => gotoLobbyView(vp.id));
    $('lobby-views').appendChild(b);
  }
}

// ---------------------------------------------------------------- visibility (View buttons decide the layers; advanced boxes are overrides)
function setVis(o, v) { if (o) o.visible = v; }
function applyVisibility() {
  const on = (id) => $(id).checked, g = state.groups, mode = state.mode, floor = state.floor;
  const inside = mode !== 'orbit' || floor !== 'both';
  const solid = on('t-exterior') && !inside;                 // the exterior is a solid model: never shown from inside
  const walk = mode === 'walk', lobby = floor === 'lobby';
  setVis(g.GRP_Exterior_Solid_Shell, solid);
  setVis(g.GRP_Exterior_Envelope, on('t-exterior') && mode !== 'plan' && !(lobby && mode === 'orbit'));   // lobby orbit: canopies / parapets would hide the void
  setVis(g.GRP_Exterior_Upper, on('t-exterior') && mode !== 'plan' && (walk || floor === 'both'));
  setVis(g.GRP_Base_Interior_Level_1, on('t-base') && !solid);
  setVis(g.GRP_Base_Interior_Level_2, on('t-base') && !solid && (walk || floor !== 'L1'));
  setVis(g.GRP_Base_Interior_Roof, on('t-base') && !solid && (walk || floor === 'both'));
  setVis(g.GRP_Site_Context, on('t-site'));
  setVis(g.GRP_Landscaping, on('t-land'));
  const lob = state.data.lobby_concept;
  setVis(g[lob.group], lobbyOn() && !solid);
  lobbyLights.visible = lobbyOn() && !solid;
  $('cmp-base').classList.toggle('on', !lobbyOn());
  $('cmp-concept').classList.toggle('on', lobbyOn());
  const c = state.concept;
  const cFloor = lobby ? 'L1' : floor;
  for (const k of state.data.concepts) setVis(g[k.group], k === c && on('t-concept') && !solid);
  const conceptShown = !!(c && g[c.group] && g[c.group].visible);
  const conceptFloorShown = c && (cFloor === 'both' || cFloor === c.floor || walk);
  setVis(state.underlay, on('t-underlay') && !solid && conceptFloorShown && cFloor !== (c.floor === 'L1' ? 'L2' : 'L1'));
  setVis(state.labels, on('t-labels') && conceptShown && !walk && cFloor !== (c.floor === 'L1' ? 'L2' : 'L1'));
  if (!conceptShown) selectRoom(null);
  // the walk grid follows the lobby toggle (banquettes / directory block only while the concept is shown)
  if (state.walkKey !== 'level2') { const want = gridKeyFor('L1'); if (state.walkKey !== want) { state.walkKey = want; if (state.mode === 'walk') { const p = nearestStandable(state.pos.x, state.pos.y); if (p) { state.pos = { x: p.x, y: p.y }; state.walkKey = p.key; state.zTarget = p.z; } } } }
}

// ---------------------------------------------------------------- floors, view states and modes
function markFloor(f) { for (const k of FLOORS) $('floor-' + k).classList.toggle('on', k === f); }
function setFloor(f) {
  if (f === 'lobby') { lobbyView(); return; }
  if (f === 'both' && state.mode === 'walk') { state.floor = 'both'; setMode('orbit'); return; }
  const prev = state.floor;
  state.floor = f;
  markFloor(f);
  if (f !== 'both' && state.mode === 'walk') placeOnFloor(f);
  if (state.mode === 'plan') frameplan();
  applyVisibility();
  if (prev !== f && f !== 'both') toast(`${state.data.floors[f].label}` + (state.mode === 'walk' ? ' — moved by the View selector (or walk Stair 1 between the floors)' : ''));
}
function lobbyView() {                                // one click: concept on, two-storey lobby layers, walk mode at the entrance looking at the stair / wood wall
  $('t-lobby').checked = true;
  state.floor = 'lobby';
  markFloor('lobby');
  gotoLobbyView(state.data.lobby_concept.viewpoints[0].id);
  toast('Lobby Concept A (model v019). Walk with W A S D, drag to look; Stair 1 leads to Level 2. Orbit for the composition view.');
}
function placeOnFloor(f) {                            // walk position remembered per floor; otherwise the floor's default start
  const cur = state.zTarget >= 8 ? 'L2' : 'L1';
  state.posByFloor[cur] = { ...state.pos, yaw: state.yaw, pitch: state.pitch };
  const saved = state.posByFloor[f], d = state.data.floors[f];
  if (saved && settle(saved.x, saved.y, gridKeyFor(f))) { state.yaw = saved.yaw; state.pitch = saved.pitch; return; }
  settle(d.default_walk_ft[0], d.default_walk_ft[1], gridKeyFor(f));
  lookAlong(d.default_forward);
}
function setMode(mode) {
  if (mode === 'walk' && state.floor === 'both') { state.floor = 'L1'; markFloor('L1'); }
  if (mode === 'walk' && state.mode !== 'walk') {
    if (state.floor === 'lobby') { const vp = state.data.lobby_concept.viewpoints[0]; settle(vp.position_ft[0], vp.position_ft[1], gridKeyFor('L1')); lookAlong(vp.forward); state.pitch = 0; }
    else if (!standAt(state.pos.x, state.pos.y, state.zTarget, keysNow())) placeOnFloor(state.floor);
  }
  state.mode = mode;
  for (const m of ['orbit', 'walk', 'plan']) $('mode-' + m).classList.toggle('on', m === mode);
  orbit.enabled = mode === 'orbit';
  planCtl.enabled = mode === 'plan';
  $('crosshair').hidden = mode !== 'walk';
  camera = mode === 'plan' ? ortho : persp;
  if (mode === 'walk') {
    persp.fov = 62; persp.updateProjectionMatrix();
    $('help').innerHTML = 'Walk: <b>W A S D</b> or arrow keys to move (Shift = faster), <b>drag the mouse</b> to look around, click a room for its data. Eye height 5\'-6". Stair 1 is walkable; the View buttons also move between floors.';
  } else if (mode === 'plan') {
    $('t-labels').checked = true;
    frameplan();
    $('help').innerHTML = 'Plan: drag to pan, wheel to zoom. North is up. The selected floor is shown from above; use the View buttons to switch.';
  } else {
    persp.fov = 50; persp.updateProjectionMatrix();
    if (state.floor === 'lobby') frameLobbyOrbit();
    $('help').innerHTML = 'Orbit: left-drag to rotate, right-drag to pan, wheel to zoom. Choose <b>Lobby</b>, <b>Level 1</b> or <b>Level 2</b> to open the building up.';
  }
  document.querySelectorAll('#viewpoints button, #lobby-views button, #lobby-free').forEach((b) => b.classList.remove('on'));
  applyVisibility();
  onResize();
}
function placeDefault() { const d = state.data.floors[state.zTarget >= 8 ? 'L2' : 'L1']; settle(d.default_walk_ft[0], d.default_walk_ft[1], gridKeyFor(state.zTarget >= 8 ? 'L2' : 'L1')); lookAlong(d.default_forward); }
function resetView() {
  if (state.mode === 'plan') { frameplan(); return; }
  if (state.mode === 'walk') { if (state.floor === 'lobby') gotoLobbyView(state.data.lobby_concept.viewpoints[0].id); else placeDefault(); return; }
  if (state.floor === 'lobby') { frameLobbyOrbit(); return; }
  persp.position.copy(toWorld(...HOME.pos));
  orbit.target.copy(toWorld(...HOME.target));
  orbit.update();
}
function frameLobbyOrbit() {                          // orbit target = centre of the wood wall + stair + pendant composition (not a distant site point)
  const o = state.data.lobby_concept.orbit;
  persp.position.copy(toWorld(...o.position_ft));
  orbit.target.copy(toWorld(...o.target_ft));
  orbit.update();
}
function frameplan() {
  const z = state.floor === 'L2' ? state.data.floors.L2.floor_z_ft : 0;
  ortho.position.copy(toWorld(60, 53, z + 400));      // building sits to the right of the side panel
  ortho.up.set(0, 0, -1);                              // north up
  planCtl.target.copy(toWorld(60, 53, z));
  ortho.zoom = 1;
  planCtl.update();
  onResize();
}
function lookAlong(f) {                                // f = forward vector in model axes
  state.yaw = Math.atan2(f[0], f[1]);                  // 0 = north, clockwise positive
  state.pitch = Math.asin(Math.max(-1, Math.min(1, f[2] || 0)));
}
function applyLens(lens) {
  const aspect = (persp.aspect && isFinite(persp.aspect)) ? persp.aspect : (window.innerWidth / window.innerHeight || 1.6), h = Math.atan(18 / lens);   // camera aspect (the canvas can be unsized while the page is hidden)
  persp.fov = THREE.MathUtils.radToDeg(2 * Math.atan(Math.tan(h) / aspect));
  persp.updateProjectionMatrix();
}
function gotoViewpoint(id) {
  const vp = state.concept.viewpoints.find((v) => v.id === id);
  if (!vp) return false;
  if (state.floor !== vp.floor) { state.floor = vp.floor; markFloor(vp.floor); }
  state.mode = 'orbit';                                // force the walk placement below
  setMode('walk');
  settle(vp.position_ft[0], vp.position_ft[1], gridKeyFor(vp.floor));
  lookAlong(vp.forward);
  applyLens(vp.lens_mm);
  document.querySelectorAll('#viewpoints button').forEach((b) => b.classList.toggle('on', b.dataset.vp === id));
  toast('Viewpoint: ' + vp.title + ' — placed here for review; this is not a documented door connection.');
  return true;
}
function gotoLobbyView(id, free) {
  const vp = state.data.lobby_concept.viewpoints.find((v) => v.id === id);
  if (!vp) return false;
  $('t-lobby').checked = true;
  if (state.floor !== 'lobby') { state.floor = 'lobby'; markFloor('lobby'); }
  state.mode = 'orbit';
  setMode('walk');
  settle(vp.position_ft[0], vp.position_ft[1], gridKeyFor(vp.floor));
  lookAlong(vp.forward);
  if (free) { state.pitch = 0; persp.fov = 62; persp.updateProjectionMatrix(); state.lobbyView = null; }
  else { applyLens(vp.lens_mm); state.lobbyView = id; }
  document.querySelectorAll('#lobby-views button').forEach((b) => b.classList.toggle('on', !free && b.dataset.lv === id));
  $('lobby-free').classList.toggle('on', !!free);
  applyVisibility();
  toast(free ? 'Free walk from the lobby entrance (W A S D, drag to look).' : 'Lobby view: ' + vp.title);
  return true;
}

// ---------------------------------------------------------------- rooms
function roomAt(x, y) {
  let best = null;
  for (const r of state.concept.rooms) {
    const [x0, y0, x1, y1] = r.rect_ft;
    if (x >= x0 && x <= x1 && y >= y0 && y <= y1 && (!best || (x1 - x0) * (y1 - y0) < (best.rect_ft[2] - best.rect_ft[0]) * (best.rect_ft[3] - best.rect_ft[1]))) best = r;
  }
  return best;
}
function selectRoom(r) {
  state.selected = r;
  const h = state.highlight;
  $('room-clear').hidden = !r;
  if (!r) { if (h) h.group.visible = false; $('room-info').innerHTML = 'Click a tenant room (any mode) to see its data.'; $('room-info').className = 'hint'; return; }
  const [x0, y0, x1, y1] = r.rect_ft, z = state.data.floors[state.concept.floor].floor_z_ft, ht = 10;
  h.plane.scale.set((x1 - x0) * FT, (y1 - y0) * FT, 1);
  h.plane.position.copy(toWorld((x0 + x1) / 2, (y0 + y1) / 2, z + 0.12));
  h.box.scale.set((x1 - x0) * FT, ht * FT, (y1 - y0) * FT);
  h.box.position.copy(toWorld((x0 + x1) / 2, (y0 + y1) / 2, z + ht / 2));
  h.group.visible = true;
  const row = (k, v) => `<tr><td>${k}</td><td>${v}</td></tr>`;
  $('room-info').className = '';
  $('room-info').innerHTML = `<div class="name">${r.name}</div><table>` +
    row('Room ID', r.id) + row('Concept', state.concept.label) + row('Floor', state.data.floors[state.concept.floor].label) +
    row('Printed area', r.printed_sf ? r.printed_sf.toLocaleString() + ' SF (on tenant plan)' : 'not printed on the plan') +
    row('Modeled area', r.modeled_sf.toLocaleString() + ' SF') +
    (r.overlapping_smaller_rooms.length ? row('Net of rooms inside', r.modeled_net_sf.toLocaleString() + ' SF (less ' + r.overlapping_smaller_rooms.join(', ') + ')') : '') +
    row('As drawn', r.enclosure) + '</table>';
}
const ray = new THREE.Raycaster();
function castModel(clientX, clientY, filterFn) {
  const rect = canvas.getBoundingClientRect();
  const ndc = new THREE.Vector2(((clientX - rect.left) / rect.width) * 2 - 1, -((clientY - rect.top) / rect.height) * 2 + 1);
  ray.setFromCamera(ndc, camera);
  const targets = Object.values(state.groups).filter((g) => g.visible);
  return ray.intersectObjects(targets, true).filter((h) => h.object.visible && (!filterFn || filterFn(h)))[0] || null;
}
function pick(clientX, clientY) {
  const c = state.concept, g = state.groups[c.group];
  if (!g || !g.visible) { selectRoom(null); return null; }
  const hit = castModel(clientX, clientY, (h) => !(h.object.material && h.object.material.transparent));
  if (!hit) { selectRoom(null); return null; }
  const p = toFeet(hit.point), z0 = state.data.floors[c.floor].floor_z_ft;
  const r = p.z >= z0 - 0.5 && p.z < z0 + 12 ? roomAt(p.x, p.y) : null;
  selectRoom(r);
  return r;
}

// ---------------------------------------------------------------- measurement (spatial review only)
function ftin(v) {
  const neg = v < 0; v = Math.abs(v);
  let ft = Math.floor(v), e = Math.round((v - ft) * 12 * 8);       // eighths of an inch
  if (e === 96) { ft++; e = 0; }
  const inch = Math.floor(e / 8);
  let n = e % 8, d = 8, frac = '';
  if (n) { while (n % 2 === 0) { n /= 2; d /= 2; } frac = ` ${n}/${d}`; }
  return `${neg ? '-' : ''}${ft}'-${inch}${frac}"`;
}
function setMeasuring(on) {
  state.measuring = on;
  $('measure').classList.toggle('on', on);
  $('measure-section').hidden = !on;
  document.body.classList.toggle('measuring', on);
  if (!on) clearMeasure();
  else toast('Measure: click a first point, then a second point.');
}
function clearMeasure() {
  const m = state.measure;
  for (const o of m.marks) disposeObject(o);
  disposeObject(m.line);
  m.points = []; m.marks = []; m.line = null;
  $('measure-readout').innerHTML = '';
  $('measure-hint').textContent = 'Click a first point, then a second point on the model.';
}
function addMeasurePoint(pFt) {
  const m = state.measure;
  if (m.points.length === 2) clearMeasure();
  m.points.push(pFt);
  const mark = new THREE.Mesh(new THREE.SphereGeometry(0.18 * FT, 14, 10), new THREE.MeshBasicMaterial({ color: 0xff3b00, depthTest: false }));
  mark.position.copy(toWorld(pFt.x, pFt.y, pFt.z));
  mark.renderOrder = 12;
  helpers.add(mark);
  m.marks.push(mark);
  if (m.points.length === 1) { $('measure-hint').textContent = 'Now click the second point.'; return; }
  const [a, b] = m.points;
  m.line = new THREE.Line(new THREE.BufferGeometry().setFromPoints([toWorld(a.x, a.y, a.z), toWorld(b.x, b.y, b.z)]), new THREE.LineBasicMaterial({ color: 0xff3b00, depthTest: false }));
  m.line.renderOrder = 12;
  helpers.add(m.line);
  const dx = b.x - a.x, dy = b.y - a.y, dz = b.z - a.z, horiz = Math.hypot(dx, dy), total = Math.hypot(horiz, dz);
  $('measure-hint').textContent = 'Distance between the two points (model coordinates). Click again to start a new measurement.';
  $('measure-readout').innerHTML = `<div class="big">${ftin(total)}</div><table>` +
    `<tr><td>Horizontal</td><td>${ftin(horiz)}</td></tr><tr><td>Vertical</td><td>${ftin(Math.abs(dz))}</td></tr>` +
    `<tr><td>East-west / north-south</td><td>${ftin(Math.abs(dx))} / ${ftin(Math.abs(dy))}</td></tr>` +
    `<tr><td>Point 1</td><td>x ${a.x.toFixed(2)}, y ${a.y.toFixed(2)}, z ${a.z.toFixed(2)} ft</td></tr><tr><td>Point 2</td><td>x ${b.x.toFixed(2)}, y ${b.y.toFixed(2)}, z ${b.z.toFixed(2)} ft</td></tr></table>`;
}
function measureClick(clientX, clientY) {
  const hit = castModel(clientX, clientY);
  if (!hit) { toast('No model surface under the cursor.'); return; }
  addMeasurePoint(toFeet(hit.point));
}

// ---------------------------------------------------------------- screenshot and presentation mode
function saveViewImage() {
  renderer.render(scene, camera);                     // fresh frame, viewport only (no panels)
  const t = new Date(), p = (n) => String(n).padStart(2, '0');
  const stamp = `${t.getFullYear()}${p(t.getMonth() + 1)}${p(t.getDate())}-${p(t.getHours())}${p(t.getMinutes())}${p(t.getSeconds())}`;
  const name = `BuildingII_${VERSION}_${state.mode}_${state.floor}_${stamp}.png`;
  canvas.toBlob((blob) => {
    if (!blob) { toast('The browser could not capture the view.'); return; }
    const a = document.createElement('a');
    a.href = URL.createObjectURL(blob); a.download = name;
    document.body.appendChild(a); a.click(); a.remove();
    setTimeout(() => URL.revokeObjectURL(a.href), 3000);
    toast('Saved ' + name + ' (check your Downloads folder).');
  }, 'image/png');
}
function setPresentation(on) {
  state.presentation = on;
  document.body.classList.toggle('presentation', on);
  $('present').classList.toggle('on', on);
  if (on) setMeasuring(false);
}

// ---------------------------------------------------------------- input
function bindUi() {
  for (const m of ['orbit', 'walk', 'plan']) $('mode-' + m).addEventListener('click', () => setMode(m));
  for (const f of FLOORS) $('floor-' + f).addEventListener('click', () => setFloor(f));
  $('reset').addEventListener('click', resetView);
  $('measure').addEventListener('click', () => setMeasuring(!state.measuring));
  $('measure-clear').addEventListener('click', clearMeasure);
  $('measure-exit').addEventListener('click', () => setMeasuring(false));
  $('shot').addEventListener('click', saveViewImage);
  $('present').addEventListener('click', () => setPresentation(true));
  $('present-exit').addEventListener('click', () => setPresentation(false));
  $('room-clear').addEventListener('click', () => selectRoom(null));
  $('cmp-base').addEventListener('click', () => { $('t-lobby').checked = false; applyVisibility(); toast('Base building (Lobby Concept A hidden)'); });
  $('cmp-concept').addEventListener('click', () => { $('t-lobby').checked = true; applyVisibility(); toast('Lobby Concept A shown'); });
  $('lobby-free').addEventListener('click', () => gotoLobbyView(state.data.lobby_concept.viewpoints[0].id, true));
  document.querySelectorAll('#panel input[type=checkbox]').forEach((c) => c.addEventListener('change', applyVisibility));
  window.addEventListener('resize', onResize);
  window.addEventListener('keydown', (e) => {
    if (e.target && e.target.tagName === 'SELECT') return;
    state.keys[e.code] = true;
    if (state.mode === 'walk' && e.code.startsWith('Arrow')) e.preventDefault();
    if (e.code === 'Escape') { if (state.measuring) setMeasuring(false); else selectRoom(null); }
  });
  window.addEventListener('keyup', (e) => { state.keys[e.code] = false; });
  window.addEventListener('blur', () => { state.keys = {}; });
  let down = null;
  canvas.addEventListener('pointerdown', (e) => { down = { x: e.clientX, y: e.clientY, moved: false }; canvas.setPointerCapture(e.pointerId); });
  canvas.addEventListener('pointermove', (e) => {
    if (!down) return;
    if (Math.abs(e.clientX - down.x) + Math.abs(e.clientY - down.y) > 4) down.moved = true;
    if (state.mode === 'walk' && down.moved) {
      state.yaw += e.movementX * 0.0032;                // mouse-look sensitivity unchanged
      state.pitch = Math.max(-1.35, Math.min(1.35, state.pitch - e.movementY * 0.0032));
    }
  });
  canvas.addEventListener('pointerup', (e) => { if (down && !down.moved) { if (state.measuring) measureClick(e.clientX, e.clientY); else pick(e.clientX, e.clientY); } down = null; });
}
function onResize() {
  const w = window.innerWidth, h = window.innerHeight;
  renderer.setSize(w, h, false);
  persp.aspect = w / h; persp.updateProjectionMatrix();
  const half = 125 * FT, a = w / h;                   // plan view: about 250 ft across at zoom 1
  ortho.left = -half; ortho.right = half; ortho.top = half / a; ortho.bottom = -half / a; ortho.updateProjectionMatrix();
}
let toastTimer = 0;
function toast(msg) { const t = $('toast'); t.textContent = msg; t.hidden = false; clearTimeout(toastTimer); toastTimer = setTimeout(() => { t.hidden = true; }, 5200); }

// ---------------------------------------------------------------- frame loop
let last = performance.now(), frames = 0, fpsT = last;
function tryMove(dx, dy) {                            // one sub-step: stay on the current surface, or cross to the other floor's grid at the stair ends
  const st = standAt(state.pos.x + dx, state.pos.y + dy, state.zTarget, keysNow());
  if (!st) return false;
  state.pos.x += dx; state.pos.y += dy; state.walkKey = st.key; state.zTarget = st.z;
  return true;
}
function walkStep(dt) {
  const k = state.keys, f = (k.KeyW || k.ArrowUp ? 1 : 0) - (k.KeyS || k.ArrowDown ? 1 : 0), s = (k.KeyD || k.ArrowRight ? 1 : 0) - (k.KeyA || k.ArrowLeft ? 1 : 0);
  if ((f || s) && !standAt(state.pos.x, state.pos.y, state.zTarget, keysNow())) { const p = nearestStandable(state.pos.x, state.pos.y); if (p) { state.pos = { x: p.x, y: p.y }; state.walkKey = p.key; state.zTarget = p.z; } }
  if (f || s) {
    const onStair = !!stairAt(null, state.pos.x, state.pos.y);
    const speed = (k.ShiftLeft || k.ShiftRight ? WALK_FAST_FT_S : WALK_FT_S) * (onStair ? STAIR_FACTOR : 1) * dt, n = Math.hypot(f, s);   // approved v017 speeds
    // v017 sub-stepping (unchanged): the frame's movement is applied in pieces of at most 0.2 ft, each tested, so no wall can be tunnelled.
    const parts = Math.max(1, Math.ceil(speed / SUBSTEP_FT));
    const dx = (Math.sin(state.yaw) * f + Math.cos(state.yaw) * s) / n * speed / parts, dy = (Math.cos(state.yaw) * f - Math.sin(state.yaw) * s) / n * speed / parts;
    for (let i = 0; i < parts; i++) {
      if (!tryMove(dx, dy) && !tryMove(dx, 0)) tryMove(0, dy);            // slide along the obstacle
    }
  }
  state.z += (state.zTarget - state.z) * Math.min(1, dt * 12);          // eased height: no bounce on the stair ramps
  persp.position.copy(toWorld(state.pos.x, state.pos.y, state.z + EYE_FT));
  const cp = Math.cos(state.pitch);
  persp.lookAt(persp.position.clone().add(toWorld(Math.sin(state.yaw) * cp, Math.cos(state.yaw) * cp, Math.sin(state.pitch))));
}
function frame(now) {
  const dt = Math.min(0.1, (now - last) / 1000); last = now;
  if (state.ready) {
    if (state.mode === 'walk') walkStep(dt); else if (state.mode === 'plan') planCtl.update(); else orbit.update();
    renderer.render(scene, camera);
    frames++;
    if (now - fpsT > 1000) {
      state.fps = Math.round(frames * 1000 / (now - fpsT)); frames = 0; fpsT = now;
      const c = state.concept, here = state.mode === 'walk' && state.zTarget < 8 && $('t-concept').checked ? roomAt(state.pos.x, state.pos.y) : null;
      const lr = state.data.lobby_concept.lobby_rect_ft, inLobby = state.pos.x > lr[0] && state.pos.x < lr[1] && state.pos.y > lr[2] && state.pos.y < lr[3];
      $('status').textContent = `${state.mode} mode` + (state.mode === 'walk' ? ` | ${walkFloorLabel()} | x ${state.pos.x.toFixed(1)} ft, y ${state.pos.y.toFixed(1)} ft, z ${state.zTarget.toFixed(1)} ft | ${here ? 'in: ' + here.name + ' (' + here.id + ')' : (inLobby ? 'Lobby 101' + (lobbyOn() ? ' — Lobby Concept A (v023)' : ' — base building') : 'circulation / base building')}` : '') +
        ` | ${state.fps} fps | ${renderer.info.render.triangles.toLocaleString()} triangles`;
    }
  }
  requestAnimationFrame(frame);
}

// Optional address-bar parameters (bookmarks, validation screenshots), e.g.
//   ?lv=LV_01_entrance   ?floor=lobby   ?lobby=0   ?vp=VP_A_08_operating_room   ?mode=plan&floor=L2   ?mode=walk&floor=L2&pos=118,69&yaw=0   ?present=1
function applyUrlParameters() {
  const q = new URLSearchParams(location.search);
  const ids = { exterior: 't-exterior', base: 't-base', concept: 't-concept', site: 't-site', land: 't-land', underlay: 't-underlay', labels: 't-labels', lobby: 't-lobby' };
  for (const [k, id] of Object.entries(ids)) if (q.has(k)) $(id).checked = q.get(k) === '1';
  if (q.get('floor')) setFloor(q.get('floor'));
  if (q.get('mode')) setMode(q.get('mode'));
  if (q.get('vp')) gotoViewpoint(q.get('vp'));
  if (q.get('lv')) gotoLobbyView(q.get('lv'), q.get('free') === '1');
  if (q.get('pos')) { const v = q.get('pos').split(',').map(Number); settle(v[0], v[1], v[2] === 2 ? 'level2' : gridKeyFor('L1')); }
  if (q.get('yaw')) state.yaw = THREE.MathUtils.degToRad(Number(q.get('yaw')));
  if (q.get('pitch')) state.pitch = THREE.MathUtils.degToRad(Number(q.get('pitch')));
  if (q.get('fov')) { persp.fov = Number(q.get('fov')); persp.updateProjectionMatrix(); }
  if (q.get('cam')) { const v = q.get('cam').split(',').map(Number); persp.position.copy(toWorld(v[0], v[1], v[2])); orbit.target.copy(toWorld(v[3], v[4], v[5])); orbit.update(); }
  applyVisibility();
  if (q.get('room')) selectRoom(state.concept.rooms.find((r) => r.id === q.get('room')) || null);
  if (q.get('measure')) { const v = q.get('measure').split(',').map(Number); setMeasuring(true); addMeasurePoint({ x: v[0], y: v[1], z: v[2] }); addMeasurePoint({ x: v[3], y: v[4], z: v[5] }); }
  if (q.has('note')) $('note').open = true;
  if (q.get('present') === '1') setPresentation(true);
}

// small test / automation surface (used for validation; harmless otherwise)
window.viewerApp = { state, step: (dt) => { walkStep(dt); renderer.render(scene, camera); }, renderer, scene, getCamera: () => camera, setMode, setFloor, setConcept,
  gotoViewpoint, gotoLobbyView, lobbyView, resetView, pick, selectRoom, roomAt, canStand, isOpen, nearestStandable, standAt, surfaceAt, stairAt, settle, applyVisibility,
  setMeasuring, addMeasurePoint, clearMeasure, ftin, saveViewImage, setPresentation, setToggle: (id, v) => { $(id).checked = v; applyVisibility(); },
  walkTo: (x, y) => settle(x, y, state.walkKey), lobbyLights };

init().catch((e) => { $('loading').textContent = 'Could not load the model: ' + e.message; console.error(e); });
requestAnimationFrame(frame);
