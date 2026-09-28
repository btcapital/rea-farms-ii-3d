// Rea Farms II - Building II review viewer, prototype v016.
// Lightweight Three.js viewer: orbit / walk / plan modes, saved viewpoints, group toggles, room information.
// Nothing here creates or edits building geometry. No door or opening is invented: walking is limited by a grid
// exported from the model (open = inside Level 1 and no solid object between 0.5 ft and 6.5 ft).
import * as THREE from 'three';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';
import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js';

const FT = 0.3048;                                   // model feet -> glTF metres
const EYE_FT = 5.5;                                  // 5'-6" eye height
const toWorld = (x, y, z) => new THREE.Vector3(x * FT, z * FT, -y * FT);        // model (x east, y north, z up) -> glTF (Y up)
const toFeet = (v) => ({ x: v.x / FT, y: -v.z / FT, z: v.y / FT });
const $ = (id) => document.getElementById(id);

const canvas = $('view');
const renderer = new THREE.WebGLRenderer({ canvas, antialias: true, preserveDrawingBuffer: true });
renderer.setPixelRatio(Math.min(window.devicePixelRatio, 1.5));
renderer.outputColorSpace = THREE.SRGBColorSpace;
const scene = new THREE.Scene();
scene.background = new THREE.Color(0xcfd8e3);
scene.add(new THREE.HemisphereLight(0xffffff, 0x9a9488, 2.2));
const sun = new THREE.DirectionalLight(0xffffff, 2.0);
sun.position.set(0.797, 0.588, -0.140).multiplyScalar(300);                     // v010 sun: azimuth 80 deg, elevation 36 deg
scene.add(sun);

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

const state = { mode: 'orbit', data: null, groups: {}, grid: null, yaw: 0, pitch: 0, pos: { x: 129.9, y: 79 }, keys: {}, selected: null,
                underlay: null, labels: null, highlight: null, fps: 0, ready: false };
const HOME = { pos: [-150, 300, 170], target: [95, 55, 10] };                     // model feet

// ---------------------------------------------------------------- loading
async function init() {
  state.data = await (await fetch('assets/viewer_data_v016.json')).json();
  $('warning').textContent = state.data.concept.warning;
  decodeGrid(state.data.walk_grid);
  const gltf = await new GLTFLoader().loadAsync(state.data.glb);
  scene.add(gltf.scene);
  gltf.scene.traverse((o) => {
    if (o.name.startsWith('GRP_')) state.groups[o.name] = o;
    if (o.isMesh) {
      const mats = Array.isArray(o.material) ? o.material : [o.material];
      for (const m of mats) { if (m.transparent) { m.depthWrite = false; } m.side = THREE.DoubleSide; }
    }
  });
  addEdgeLines(['GRP_Concept_A_CNSA_ASC', 'GRP_Base_Interior_Level_1', 'GRP_Base_Interior_Level_2']);
  buildUnderlay();
  buildLabels();
  buildHighlight();
  buildViewpointButtons();
  bindUi();
  setMode('orbit');
  resetView();
  applyUrlParameters();
  state.ready = true;
  $('loading').remove();
}

// Optional address-bar parameters (handy for bookmarks and for the v016 test screenshots), e.g.
//   ?vp=VP_A_08_operating_room   ?mode=plan&underlay=1   ?mode=orbit&exterior=0&upper=0&room=A-051
function applyUrlParameters() {
  const q = new URLSearchParams(location.search);
  const ids = { exterior: 't-exterior', upper: 't-upper', base: 't-base', concept: 't-concept', site: 't-site', land: 't-land', underlay: 't-underlay', labels: 't-labels' };
  if (q.get('mode')) setMode(q.get('mode'));
  if (q.get('vp')) gotoViewpoint(q.get('vp'));
  for (const [k, id] of Object.entries(ids)) if (q.has(k)) $(id).checked = q.get(k) === '1';
  if (q.get('cam')) { const v = q.get('cam').split(',').map(Number); persp.position.copy(toWorld(v[0], v[1], v[2])); orbit.target.copy(toWorld(v[3], v[4], v[5])); orbit.update(); }
  applyVisibility();
  if (q.get('room')) selectRoom(state.data.rooms.find((r) => r.id === q.get('room')) || null);
  if (q.has('note')) $('note').open = true;
}

function decodeGrid(g) {
  const cells = new Uint8Array(g.nx * g.ny);
  g.rows.forEach((runs, j) => {
    let i = 0, blocked = 0;
    for (const n of runs) { if (blocked) cells.fill(1, j * g.nx + i, j * g.nx + i + n); i += n; blocked ^= 1; }
  });
  state.grid = { ...g, cells };
}
function isOpen(x, y) {
  const g = state.grid, i = Math.floor((x - g.x0_ft) / g.cell_ft), j = Math.floor((y - g.y0_ft) / g.cell_ft);
  return i >= 0 && j >= 0 && i < g.nx && j < g.ny && g.cells[j * g.nx + i] === 0;
}
const BODY_FT = 0.75;                                 // body radius used for collision
function canStand(x, y) {
  if (!isOpen(x, y)) return false;
  for (let k = 0; k < 8; k++) { const a = k * Math.PI / 4; if (!isOpen(x + BODY_FT * Math.cos(a), y + BODY_FT * Math.sin(a))) return false; }
  return true;
}
function nearestStandable(x, y) {                     // used after a viewpoint teleport that sits close to a wall; never crosses a solid cell
  if (canStand(x, y)) return { x, y };
  for (let r = 0.25; r <= 3.0; r += 0.25) {
    for (let k = 0; k < 16; k++) {
      const a = k * Math.PI / 8, nx = x + r * Math.cos(a), ny = y + r * Math.sin(a);
      if (!canStand(nx, ny)) continue;
      let clear = true;
      for (let t = 0.125; t < r && clear; t += 0.125) clear = isOpen(x + t * Math.cos(a), y + t * Math.sin(a));
      if (clear) return { x: nx, y: ny };
    }
  }
  return null;
}

// ---------------------------------------------------------------- helpers built from the exported data
function addEdgeLines(groupNames) {                   // thin dark edges so plain neutral walls stay readable (display aid only, no geometry change)
  const mat = new THREE.LineBasicMaterial({ color: 0x3a4450, transparent: true, opacity: 0.55 });
  for (const name of groupNames) {
    const meshes = [];
    state.groups[name].traverse((o) => {              // slabs are built from cells: no edge lines on them
      const slab = (o.name + '|' + (o.parent ? o.parent.name : '')).includes('__BASE_Level');
      if (o.isMesh && !o.material.transparent && !slab && !o.name.startsWith('TEN_A_Room') && !o.name.startsWith('TEN_A_Circulation')) meshes.push(o);
    });
    for (const m of meshes) { const l = new THREE.LineSegments(new THREE.EdgesGeometry(m.geometry, 30), mat); l.raycast = () => {}; m.add(l); }
  }
}
function buildUnderlay() {
  const u = state.data.underlay, w = (u.x1_ft - u.x0_ft) * FT, h = (u.y1_ft - u.y0_ft) * FT;
  const tex = new THREE.TextureLoader().load(u.image);
  tex.colorSpace = THREE.SRGBColorSpace;
  tex.anisotropy = 8;
  const mesh = new THREE.Mesh(new THREE.PlaneGeometry(w, h), new THREE.MeshBasicMaterial({ map: tex, transparent: true, opacity: 0.92 }));
  mesh.rotation.x = -Math.PI / 2;                     // image top -> north
  mesh.position.copy(toWorld((u.x0_ft + u.x1_ft) / 2, (u.y0_ft + u.y1_ft) / 2, 0.07));
  mesh.name = 'Tenant_plan_underlay_registered';
  mesh.visible = false;
  scene.add(mesh);
  state.underlay = mesh;
}
function buildLabels() {
  const group = new THREE.Group();
  group.name = 'Room_labels';
  for (const r of state.data.rooms) {
    if (!r.printed_sf) continue;
    const c = document.createElement('canvas');
    c.width = 512; c.height = 192;
    const g = c.getContext('2d');
    g.fillStyle = '#10151c'; g.textAlign = 'center'; g.textBaseline = 'middle';
    g.font = '600 64px Segoe UI, Arial'; g.fillText(r.name, 256, 62, 500);
    g.font = '52px Segoe UI, Arial'; g.fillText(`${r.printed_sf} SF`, 256, 138, 500);
    const tex = new THREE.CanvasTexture(c);
    tex.colorSpace = THREE.SRGBColorSpace;
    const s = new THREE.Sprite(new THREE.SpriteMaterial({ map: tex, depthTest: false, transparent: true }));
    const [x0, y0, x1, y1] = r.rect_ft, w = Math.min((x1 - x0) * 0.92, 15) * FT;
    s.scale.set(w, w * 192 / 512, 1);
    s.position.copy(toWorld((x0 + x1) / 2, (y0 + y1) / 2, 11));
    s.renderOrder = 10;
    group.add(s);
  }
  group.visible = false;
  scene.add(group);
  state.labels = group;
}
function buildHighlight() {
  const m = new THREE.Mesh(new THREE.PlaneGeometry(1, 1), new THREE.MeshBasicMaterial({ color: 0xffc400, transparent: true, opacity: 0.45, depthWrite: false, side: THREE.DoubleSide }));
  m.rotation.x = -Math.PI / 2;
  m.visible = false;
  m.renderOrder = 5;
  scene.add(m);
  state.highlight = m;
}
function buildViewpointButtons() {
  for (const vp of state.data.viewpoints) {
    const b = document.createElement('button');
    b.textContent = vp.title;
    b.dataset.vp = vp.id;
    b.addEventListener('click', () => gotoViewpoint(vp.id));
    $('viewpoints').appendChild(b);
  }
}

// ---------------------------------------------------------------- visibility
function applyVisibility() {
  const on = (id) => $(id).checked, g = state.groups, inside = state.mode !== 'orbit';
  const solid = on('t-exterior') && !inside;          // the exterior is a solid model: never shown from inside
  const upper = on('t-upper') && state.mode !== 'plan';
  g.GRP_Exterior_Solid_Shell.visible = solid;
  g.GRP_Exterior_Envelope.visible = on('t-exterior') && state.mode !== 'plan';
  g.GRP_Exterior_Upper.visible = on('t-exterior') && upper;
  g.GRP_Base_Interior_Level_1.visible = on('t-base') && !solid;
  g.GRP_Base_Interior_Level_2.visible = on('t-base') && upper && !solid;
  g.GRP_Base_Interior_Roof.visible = on('t-base') && upper && !solid;
  g.GRP_Concept_A_CNSA_ASC.visible = on('t-concept') && !solid;
  g.GRP_Site_Context.visible = on('t-site');
  g.GRP_Landscaping.visible = on('t-land');
  state.underlay.visible = on('t-underlay') && !solid;
  state.labels.visible = on('t-labels') && on('t-concept') && !solid;
  if (!on('t-concept')) selectRoom(null);
}

// ---------------------------------------------------------------- modes
function setMode(mode) {
  state.mode = mode;
  for (const m of ['orbit', 'walk', 'plan']) $('mode-' + m).classList.toggle('on', m === mode);
  orbit.enabled = mode === 'orbit';
  planCtl.enabled = mode === 'plan';
  $('crosshair').hidden = mode !== 'walk';
  camera = mode === 'plan' ? ortho : persp;
  if (mode === 'walk') {
    if (!isOpen(state.pos.x, state.pos.y)) { const vp = state.data.viewpoints[0]; state.pos = { x: vp.position_ft[0], y: vp.position_ft[1] }; lookAlong(vp.forward); }
    persp.fov = 62; persp.updateProjectionMatrix();
    $('help').innerHTML = 'Walk: <b>W A S D</b> or arrow keys to move (Shift = faster), <b>drag the mouse</b> to look around, click a room for its data. Eye height 5\'-6".';
  } else if (mode === 'plan') {
    $('t-labels').checked = true;
    frameplan();
    $('help').innerHTML = 'Plan: drag to pan, wheel to zoom. North is up. Roof, Level 2 and the solid exterior are hidden. Tick <b>Tenant plan underlay</b> to compare with the PDF.';
  } else {
    persp.fov = 50; persp.updateProjectionMatrix();
    $('help').innerHTML = 'Orbit: left-drag to rotate, right-drag to pan, wheel to zoom. Untick <b>exterior</b> and <b>roof / Level 2</b> to look into Level 1 from above.';
  }
  document.querySelectorAll('#viewpoints button').forEach((b) => b.classList.remove('on'));
  applyVisibility();
  onResize();
}
function resetView() {
  if (state.mode === 'plan') { frameplan(); return; }
  if (state.mode === 'walk') { gotoViewpoint(state.data.viewpoints[0].id); return; }
  persp.position.copy(toWorld(...HOME.pos));
  orbit.target.copy(toWorld(...HOME.target));
  orbit.update();
}
function frameplan() {
  ortho.position.copy(toWorld(60, 53, 400));          // building sits to the right of the side panel
  ortho.up.set(0, 0, -1);                              // north up
  planCtl.target.copy(toWorld(60, 53, 0));
  ortho.zoom = 1;
  planCtl.update();
  onResize();
}
function lookAlong(f) {                                // f = forward vector in model axes
  state.yaw = Math.atan2(f[0], f[1]);                  // 0 = north, clockwise positive
  state.pitch = Math.asin(Math.max(-1, Math.min(1, f[2])));
}
function gotoViewpoint(id) {
  const vp = state.data.viewpoints.find((v) => v.id === id);
  if (!vp) return false;
  state.pos = { x: vp.position_ft[0], y: vp.position_ft[1] };
  lookAlong(vp.forward);
  setMode('walk');
  const aspect = canvas.clientWidth / canvas.clientHeight, h = Math.atan(18 / vp.lens_mm);
  persp.fov = THREE.MathUtils.radToDeg(2 * Math.atan(Math.tan(h) / aspect));
  persp.updateProjectionMatrix();
  document.querySelectorAll('#viewpoints button').forEach((b) => b.classList.toggle('on', b.dataset.vp === id));
  toast('Viewpoint: ' + vp.title + ' - placed here for review; this is not a documented door connection.');
  return true;
}

// ---------------------------------------------------------------- rooms
function roomAt(x, y) {
  let best = null;
  for (const r of state.data.rooms) {
    const [x0, y0, x1, y1] = r.rect_ft;
    if (x >= x0 && x <= x1 && y >= y0 && y <= y1 && (!best || (x1 - x0) * (y1 - y0) < (best.rect_ft[2] - best.rect_ft[0]) * (best.rect_ft[3] - best.rect_ft[1]))) best = r;
  }
  return best;
}
function selectRoom(r) {
  state.selected = r;
  const h = state.highlight;
  if (!r) { h.visible = false; $('room-info').innerHTML = 'Click a tenant room (any mode) to see its data.'; $('room-info').className = 'hint'; return; }
  const [x0, y0, x1, y1] = r.rect_ft;
  h.scale.set((x1 - x0) * FT, (y1 - y0) * FT, 1);
  h.position.copy(toWorld((x0 + x1) / 2, (y0 + y1) / 2, 0.12));
  h.visible = true;
  const row = (k, v) => `<tr><td>${k}</td><td>${v}</td></tr>`;
  $('room-info').className = '';
  $('room-info').innerHTML = `<div class="name">${r.name}</div><table>` +
    row('Room ID', r.id) + row('Concept', r.concept.replaceAll('_', ' ')) + row('Floor', r.floor) +
    row('Printed area', r.printed_sf ? r.printed_sf.toLocaleString() + ' SF (on tenant plan)' : 'not printed on the plan') +
    row('Modeled area', r.modeled_sf.toLocaleString() + ' SF') +
    (r.overlapping_smaller_rooms.length ? row('Net of rooms inside', r.modeled_net_sf.toLocaleString() + ' SF (less ' + r.overlapping_smaller_rooms.join(', ') + ')') : '') +
    row('As drawn', r.enclosure) + '</table>';
}
const ray = new THREE.Raycaster();
function pick(clientX, clientY) {
  if (!state.groups.GRP_Concept_A_CNSA_ASC.visible) { selectRoom(null); return null; }
  const rect = canvas.getBoundingClientRect();
  const ndc = new THREE.Vector2(((clientX - rect.left) / rect.width) * 2 - 1, -((clientY - rect.top) / rect.height) * 2 + 1);
  ray.setFromCamera(ndc, camera);
  const targets = [state.groups.GRP_Concept_A_CNSA_ASC, state.groups.GRP_Base_Interior_Level_1].filter((g) => g.visible);
  const hits = ray.intersectObjects(targets, true).filter((h) => !(h.object.material && h.object.material.transparent));
  if (!hits.length) { selectRoom(null); return null; }
  const p = toFeet(hits[0].point);
  const r = p.z < 12 ? roomAt(p.x, p.y) : null;
  selectRoom(r);
  return r;
}

// ---------------------------------------------------------------- input
function bindUi() {
  for (const m of ['orbit', 'walk', 'plan']) $('mode-' + m).addEventListener('click', () => setMode(m));
  $('reset').addEventListener('click', resetView);
  document.querySelectorAll('#panel input[type=checkbox]').forEach((c) => c.addEventListener('change', applyVisibility));
  window.addEventListener('resize', onResize);
  window.addEventListener('keydown', (e) => { state.keys[e.code] = true; if (state.mode === 'walk' && e.code.startsWith('Arrow')) e.preventDefault(); });
  window.addEventListener('keyup', (e) => { state.keys[e.code] = false; });
  window.addEventListener('blur', () => { state.keys = {}; });
  let down = null;
  canvas.addEventListener('pointerdown', (e) => { down = { x: e.clientX, y: e.clientY, moved: false }; canvas.setPointerCapture(e.pointerId); });
  canvas.addEventListener('pointermove', (e) => {
    if (!down) return;
    if (Math.abs(e.clientX - down.x) + Math.abs(e.clientY - down.y) > 4) down.moved = true;
    if (state.mode === 'walk' && down.moved) {
      state.yaw += e.movementX * 0.0032;
      state.pitch = Math.max(-1.35, Math.min(1.35, state.pitch - e.movementY * 0.0032));
    }
  });
  canvas.addEventListener('pointerup', (e) => { if (down && !down.moved) pick(e.clientX, e.clientY); down = null; });
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
function walkStep(dt) {
  const k = state.keys, f = (k.KeyW || k.ArrowUp ? 1 : 0) - (k.KeyS || k.ArrowDown ? 1 : 0), s = (k.KeyD || k.ArrowRight ? 1 : 0) - (k.KeyA || k.ArrowLeft ? 1 : 0);
  if ((f || s) && !canStand(state.pos.x, state.pos.y)) { const p = nearestStandable(state.pos.x, state.pos.y); if (p) state.pos = p; }
  if (f || s) {
    const speed = (k.ShiftLeft || k.ShiftRight ? 18.0 : 9.0) * dt, n = Math.hypot(f, s);     // ft per second (v017: exactly 2 x the v016 values 9.0 : 4.5)
    // v017: the frame's movement is applied in pieces of at most 0.2 ft, each tested exactly as in v016, so the doubled speed can
    // never carry the viewer across a thin partition in one slow frame. The collision grid and the tests themselves are unchanged.
    const parts = Math.max(1, Math.ceil(speed / 0.2));
    const dx = (Math.sin(state.yaw) * f + Math.cos(state.yaw) * s) / n * speed / parts, dy = (Math.cos(state.yaw) * f - Math.sin(state.yaw) * s) / n * speed / parts;
    for (let i = 0; i < parts; i++) {
      if (canStand(state.pos.x + dx, state.pos.y + dy)) { state.pos.x += dx; state.pos.y += dy; }
      else if (canStand(state.pos.x + dx, state.pos.y)) state.pos.x += dx;                   // slide along the obstacle
      else if (canStand(state.pos.x, state.pos.y + dy)) state.pos.y += dy;
    }
  }
  persp.position.copy(toWorld(state.pos.x, state.pos.y, EYE_FT));
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
      const here = state.mode === 'walk' && $('t-concept').checked ? roomAt(state.pos.x, state.pos.y) : null;
      $('status').textContent = `${state.mode} mode` + (state.mode === 'walk' ? ` | x ${state.pos.x.toFixed(1)} ft, y ${state.pos.y.toFixed(1)} ft | ${here ? 'in: ' + here.name + ' (' + here.id + ')' : 'circulation / base building'}` : '') +
        ` | ${state.fps} fps | ${renderer.info.render.triangles.toLocaleString()} triangles`;
    }
  }
  requestAnimationFrame(frame);
}

// small test / automation surface (used for the v016 validation; harmless otherwise)
window.viewerApp = { state, step: (dt) => { walkStep(dt); renderer.render(scene, camera); }, renderer, scene, getCamera: () => camera, nearestStandable, setMode, gotoViewpoint, resetView, pick, selectRoom, roomAt, canStand, applyVisibility,
  setToggle: (id, v) => { $(id).checked = v; applyVisibility(); }, walkTo: (x, y) => { if (canStand(x, y)) { state.pos = { x, y }; return true; } return false; } };

init().catch((e) => { $('loading').textContent = 'Could not load the model: ' + e.message; console.error(e); });
requestAnimationFrame(frame);
