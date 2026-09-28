// Building I - Rea Farms Sports Medicine Center - browser viewer v015 (model v014, read-only).
// Data-driven: floors, groups, concepts, spaces, viewpoints, underlays and collision all come from data/BI_viewer_data_v015.json.
// Coordinates: Building I feet (origin grid 1 x A at FFE 661.75, +X east, +Y north, z above LVL-01).
// three.js space = (X ft, Z ft, -Y ft): the GLB (glTF Y-up, metres) is scaled by 1/0.3048.
import * as THREE from 'three';
import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';
import { CSS2DRenderer, CSS2DObject } from 'three/addons/renderers/CSS2DRenderer.js';

const FT = 0.3048;
const T = (x, y, z) => new THREE.Vector3(x, z, -y);                 // Building I ft -> three
const B = (v) => ({ x: v.x, y: -v.z, z: v.y });                     // three -> Building I ft
const $ = (id) => document.getElementById(id);
const ftin = (v) => { const s = v < 0 ? '-' : ''; v = Math.abs(v); let f = Math.floor(v); let i = (v - f) * 12; let e = Math.round(i * 8) / 8; if (e >= 12) { f += 1; e = 0; }
  const w = Math.floor(e), fr = e - w; const FR = { 0: '', 0.125: ' 1/8', 0.25: ' 1/4', 0.375: ' 3/8', 0.5: ' 1/2', 0.625: ' 5/8', 0.75: ' 3/4', 0.875: ' 7/8' };
  return `${s}${f}'-${w}${FR[fr] || ''}"`; };
const fmt = (v) => `${ftin(v)} (${v.toFixed(2)} ft)`;

// ------------------------------------------------------------------------------------------------------------ state
const S = { mode: 'orbit', floor: 'BOTH', concept: 'cnsa', labels: false, labelsUser: false, underlay: false, presentation: false, measuring: false,
  measure: [], selected: null, layers: {}, data: null, groups: {}, meshes: [], spaces: [], captureOK: false };
const W = { pos: {}, yaw: 0, pitch: 0, keys: {}, shift: false, floorZ: 0, locked: false, dragging: false, lastRoute: null };   // walker

// ------------------------------------------------------------------------------------------------------------ renderer / scene
const canvas = $('c');
const renderer = new THREE.WebGLRenderer({ canvas, antialias: true, powerPreference: 'high-performance' });
renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
renderer.outputColorSpace = THREE.SRGBColorSpace;
renderer.toneMapping = THREE.ACESFilmicToneMapping; renderer.toneMappingExposure = 1.05;
const labelRenderer = new CSS2DRenderer({ element: $('labels') });
const scene = new THREE.Scene(); scene.background = new THREE.Color(0xcfdbe6);
const world = new THREE.Group(); world.scale.setScalar(1 / FT); scene.add(world);
const helpers = new THREE.Group(); scene.add(helpers);        // highlight, measure, underlays, pick planes (already in ft)
const persp = new THREE.PerspectiveCamera(60, 1, 0.5, 6000);
const ortho = new THREE.OrthographicCamera(-1, 1, 1, -1, 0.1, 4000);
let camera = persp;
const hemi = new THREE.HemisphereLight(0xe6eef7, 0x5c5a52, 1.15); scene.add(hemi);
const sun = new THREE.DirectionalLight(0xfff1dc, 1.7); sun.position.copy(T(-120, -90, 260)); scene.add(sun);
const amb = new THREE.AmbientLight(0xffffff, 0.22); scene.add(amb);
function setLighting(mode) { if (mode === 'walk') { hemi.color.set(0xffffff); hemi.groundColor.set(0x9a9a94); hemi.intensity = 1.3; amb.intensity = 0.75; sun.intensity = 1.2; } else { hemi.color.set(0xe6eef7); hemi.groundColor.set(0x5c5a52); hemi.intensity = 1.15; amb.intensity = 0.22; sun.intensity = 1.7; } }
const orbit = new OrbitControls(persp, canvas); orbit.enableDamping = true; orbit.dampingFactor = 0.1; orbit.maxPolarAngle = Math.PI * 0.499;
const clipPlane = new THREE.Plane(new THREE.Vector3(0, -1, 0), 0);
function resize() { const w = innerWidth, h = innerHeight; renderer.setSize(w, h, false); labelRenderer.setSize(w, h); persp.aspect = w / h; persp.updateProjectionMatrix(); setOrthoFrustum(); }
addEventListener('resize', resize);

// ------------------------------------------------------------------------------------------------------------ plan camera (north up)
const PLAN = { cx: 147, cy: 100, halfW: 175 };     // ft
function setOrthoFrustum() { const a = innerWidth / innerHeight; ortho.left = -PLAN.halfW; ortho.right = PLAN.halfW; ortho.top = PLAN.halfW / a; ortho.bottom = -PLAN.halfW / a; ortho.updateProjectionMatrix(); placeOrtho(); }
function placeOrtho() { ortho.position.copy(T(PLAN.cx, PLAN.cy, 600)); ortho.up.set(0, 0, -1); ortho.lookAt(T(PLAN.cx, PLAN.cy, 0)); ortho.updateMatrixWorld(); }
let planDrag = null;
canvas.addEventListener('pointerdown', (e) => { if (S.mode === 'plan' && e.button === 0 && !S.measuring) { planDrag = { x: e.clientX, y: e.clientY, cx: PLAN.cx, cy: PLAN.cy }; } });
addEventListener('pointermove', (e) => { if (planDrag && S.mode === 'plan') { const k = (2 * PLAN.halfW) / innerWidth; PLAN.cx = planDrag.cx - (e.clientX - planDrag.x) * k; PLAN.cy = planDrag.cy + (e.clientY - planDrag.y) * k; placeOrtho(); } });
addEventListener('pointerup', () => { planDrag = null; });
canvas.addEventListener('wheel', (e) => { if (S.mode !== 'plan') return; e.preventDefault(); const f = e.deltaY > 0 ? 1.12 : 1 / 1.12;
  const p0 = planPointAt(e.clientX, e.clientY); PLAN.halfW = Math.min(600, Math.max(8, PLAN.halfW * f)); setOrthoFrustum(); const p1 = planPointAt(e.clientX, e.clientY);
  PLAN.cx += p0.x - p1.x; PLAN.cy += p0.y - p1.y; placeOrtho(); }, { passive: false });
function planPointAt(px, py) { const a = innerWidth / innerHeight; return { x: PLAN.cx + (px / innerWidth - 0.5) * 2 * PLAN.halfW, y: PLAN.cy - (py / innerHeight - 0.5) * 2 * PLAN.halfW / a }; }

// ------------------------------------------------------------------------------------------------------------ loading
async function main() {
  const data = await (await fetch('./data/BI_viewer_data_v015.json')).json(); S.data = data;
  try { S.captureOK = (await (await fetch('/__capture/ping')).json()).capture === true; } catch (e) { S.captureOK = false; }
  $('overlayText').textContent = `Loading model (${(data.meta.glb_bytes / 1e6).toFixed(1)} MB) ...`;
  const gltf = await new Promise((res, rej) => new GLTFLoader().load('./model/' + data.meta.glb.split('/').pop(), res, (ev) => { if (ev.total) $('overlayText').textContent = `Loading model ${(100 * ev.loaded / ev.total).toFixed(0)} % ...`; }, rej));
  world.add(gltf.scene);
  data.groups.forEach((g) => { S.groups[g.id] = { def: g, meshes: [] }; S.layers[g.id] = g.default; });
  const stack = [[gltf.scene, null]];
  while (stack.length) {
    const [o, inh] = stack.pop();
    const g = o.userData?.bi_group || (data.objects[o.name] ? data.objects[o.name].group : null) || inh;
    if (o.isMesh) {
      o.userData.bi_group = g; S.groups[g]?.meshes.push(o); S.meshes.push(o);
      const mats = Array.isArray(o.material) ? o.material : [o.material];
      mats.forEach((m) => { m.side = THREE.DoubleSide; if (m.transparent || m.opacity < 1) { m.transparent = true; m.depthWrite = false; o.renderOrder = 2; } m.roughness = Math.max(0.3, m.roughness ?? 0.7); });
      if (g === 'CNSA' && o.name.startsWith('CNSA_tenant_zone')) { o.renderOrder = 1; }
      // the v008 shell prisms are solids whose bottom caps are coplanar with the slab on grade and whose faces carry the v005 facade regions:
      // push them back (rendering only) so the base-building slab and the facade regions win the depth test in cutaway views
      if (g === 'EXTERIOR_SHELL' && /^BI_Z/.test(o.name)) { o.material = (Array.isArray(o.material) ? o.material : [o.material]).map((m) => { const c = m.clone(); c.polygonOffset = true; c.polygonOffsetFactor = 2; c.polygonOffsetUnits = 2; return c; }); if (o.material.length === 1) o.material = o.material[0]; }
    }
    o.children.forEach((c) => stack.push([c, g]));
  }
  buildUI(); buildSpaces(); buildUnderlays(); buildCollision(); buildViewpoints();
  setFloor('BOTH'); setMode('orbit'); resetOrbit(); resize();
  const r0 = data.viewpoints.find((v) => v.id === 'vp_ext_entrance'); if (r0) gotoViewpoint(r0.id);
  $('overlay').classList.add('hidden');
  renderer.setAnimationLoop(frame);
  window.BI = api;
}

// ------------------------------------------------------------------------------------------------------------ UI
function buildUI() {
  const d = S.data;
  document.querySelectorAll('button.mode').forEach((b) => b.onclick = () => setMode(b.dataset.mode));
  document.querySelectorAll('button.floor').forEach((b) => b.onclick = () => setFloor(b.dataset.floor));
  const sel = $('concept'); d.concepts.forEach((c) => { const o = document.createElement('option'); o.value = c.id; o.textContent = c.label; if (c.empty) o.disabled = true; sel.appendChild(o); });
  sel.value = S.concept; sel.onchange = () => setConcept(sel.value);
  $('cnsaToggle').onclick = () => setConcept(S.concept === 'cnsa' ? 'base' : 'cnsa');
  const lay = $('layers');
  d.groups.forEach((g) => { const l = document.createElement('label'); const cb = document.createElement('input'); cb.type = 'checkbox'; cb.checked = g.default; cb.onchange = () => setLayer(g.id, cb.checked); cb.id = 'layer_' + g.id;
    l.appendChild(cb); l.appendChild(document.createTextNode(g.label + (g.category === 'concept' ? '' : ''))); lay.appendChild(l); });
  $('measureBtn').onclick = () => setMeasuring(!S.measuring);
  $('clearMeasure').onclick = () => clearMeasure();
  $('labelsBtn').onclick = () => { S.labelsUser = !S.labels; setLabels(!S.labels); };
  $('underlayBtn').onclick = () => setUnderlay(!S.underlay);
  $('clearHl').onclick = () => clearHighlight();
  $('resetView').onclick = () => { if (S.mode === 'plan') { PLAN.cx = 147; PLAN.cy = 100; PLAN.halfW = 175; setOrthoFrustum(); } else if (S.mode === 'orbit') resetOrbit(); else { const o = S.data.collision.route_origins[S.floor === 'BOTH' ? 'L1' : S.floor]; teleport(o.x, o.y); } };
  $('saveImg').onclick = () => saveImage();
  $('presToggle').onclick = () => setPresentation(true); $('presExit').onclick = () => setPresentation(false);
  $('notes').innerHTML = `Model: ${d.meta.model}<br>GLB: ${d.meta.glb} (${(d.meta.glb_bytes / 1e6).toFixed(1)} MB)<br>Collision: ${d.collision.note}<br>Open items: ${d.open_items.join('; ')}`;
  addEventListener('keydown', (e) => { if (e.target.tagName === 'INPUT' || e.target.tagName === 'SELECT') return;
    if (e.key === 'Escape') { clearHighlight(); if (S.measuring) setMeasuring(false); }
    W.keys[e.code] = true; if (e.key === 'Shift') W.shift = true; if (['ArrowUp', 'ArrowDown', 'ArrowLeft', 'ArrowRight', 'Space'].includes(e.code) && S.mode === 'walk') e.preventDefault(); });
  addEventListener('keyup', (e) => { W.keys[e.code] = false; if (e.key === 'Shift') W.shift = false; });
  addEventListener('blur', () => { W.keys = {}; W.shift = false; });
  // mouse look (pointer lock, drag fallback)
  canvas.addEventListener('click', (e) => { if (S.mode === 'walk' && !S.measuring && !W.locked) { canvas.requestPointerLock?.(); } });
  document.addEventListener('pointerlockchange', () => { W.locked = document.pointerLockElement === canvas; });
  canvas.addEventListener('pointerdown', (e) => { if (S.mode === 'walk' && e.button === 0) W.dragging = { x: e.clientX, y: e.clientY }; });
  addEventListener('pointerup', () => { W.dragging = false; });
  addEventListener('mousemove', (e) => { if (S.mode !== 'walk') return; let dx = 0, dy = 0;
    if (W.locked) { dx = e.movementX; dy = e.movementY; } else if (W.dragging) { dx = e.clientX - W.dragging.x; dy = e.clientY - W.dragging.y; W.dragging = { x: e.clientX, y: e.clientY }; } else return;
    W.yaw += dx * 0.0032; W.pitch = Math.max(-1.45, Math.min(1.45, W.pitch - dy * 0.0032)); });
  canvas.addEventListener('pointerdown', onPickDown); canvas.addEventListener('pointerup', onPickUp);
}
let pickStart = null;
function onPickDown(e) { pickStart = { x: e.clientX, y: e.clientY, t: performance.now() }; }
function onPickUp(e) { if (!pickStart) return; const moved = Math.hypot(e.clientX - pickStart.x, e.clientY - pickStart.y); pickStart = null; if (moved > 4 || e.button !== 0) return;
  if (S.measuring) { measureClick(e.clientX, e.clientY); return; }
  if (S.mode === 'walk' && W.locked) return;
  pickSpace(e.clientX, e.clientY); }

function setMode(m) {
  if (S.mode === 'walk' && m !== 'walk') { W.pos[S.floor] = { ...walkerPos() }; document.exitPointerLock?.(); }
  S.mode = m; document.body.classList.toggle('walk', m === 'walk'); setLighting(m);
  document.querySelectorAll('button.mode').forEach((b) => b.classList.toggle('on', b.dataset.mode === m));
  if (m === 'plan') { camera = ortho; setOrthoFrustum(); orbit.enabled = false; setLabels(true); }
  else if (m === 'walk') { camera = persp; orbit.enabled = false; if (S.floor === 'BOTH') setFloor('L1'); else applyFloor(); setLabels(false); }
  else { camera = persp; orbit.enabled = true; setLabels(S.labelsUser); }
  applyFloor(); applyVisibility(); updateUnderlay(); updateStatus();
}
function setFloor(f) { if (S.mode === 'walk' && S.floor !== f) W.pos[S.floor] = { ...walkerPos() }; if (S.mode === 'walk' && f === 'BOTH') f = 'L1';
  S.floor = f; document.querySelectorAll('button.floor').forEach((b) => b.classList.toggle('on', b.dataset.floor === f)); applyFloor(); applyVisibility(); updateLabels(); updateUnderlay(); updateStatus(); }
function floorDef() { return S.data.floors.find((f) => f.id === S.floor); }
function applyFloor() {
  const fd = floorDef();
  if (S.mode !== 'walk' && fd.clip_z != null) { clipPlane.constant = fd.clip_z; renderer.clippingPlanes = [clipPlane]; } else renderer.clippingPlanes = [];
  if (S.mode === 'walk') { W.floorZ = fd.z; const p = W.pos[S.floor] || (() => { const o = S.data.collision.route_origins[S.floor]; return { x: o.x, y: o.y }; })(); W.pos[S.floor] = p; rebuildCollision(); }
}
function setConcept(id) { S.concept = id; $('concept').value = id; const on = id === 'cnsa'; $('cnsaToggle').textContent = on ? 'ON' : 'OFF'; $('cnsaToggle').classList.toggle('on', on); applyVisibility(); rebuildCollision(); updateLabels(); updateStatus(); }
function setLayer(id, on) { S.layers[id] = on; const cb = $('layer_' + id); if (cb) cb.checked = on; applyVisibility(); }
function conceptGroups() { const c = S.data.concepts.find((c) => c.id === S.concept); return new Set(c ? c.groups : []); }
function applyVisibility() {
  const cg = conceptGroups(); const floorView = S.floor !== 'BOTH' && S.mode !== 'walk';
  for (const [id, g] of Object.entries(S.groups)) {
    let vis = S.layers[id];
    if (g.def.category === 'tenant' || g.def.category === 'concept') vis = vis && cg.has(id);
    if (floorView && (id === 'CONTEXT')) vis = false;
    g.meshes.forEach((m) => { m.visible = vis; });
  }
}
function setLabels(on) { S.labels = on; $('labelsBtn').classList.toggle('on', on); updateLabels(); }
function setUnderlay(on) { S.underlay = on; $('underlayBtn').classList.toggle('on', on); updateUnderlay(); }
function setPresentation(on) { S.presentation = on; document.body.classList.toggle('presentation', on); $('presToggle').classList.toggle('hidden', on); $('presExit').classList.toggle('hidden', !on); if (on) { setMeasuring(false); } }
function setMeasuring(on) { S.measuring = on; $('measureBtn').classList.toggle('on', on); document.body.classList.toggle('measuring', on); if (on) { S.measure = []; document.exitPointerLock?.(); $('measure').classList.remove('hidden'); $('measureOut').innerHTML = '<span class="dim">Click two points on the model.</span>'; } }

// ------------------------------------------------------------------------------------------------------------ spaces (rooms / zones) + labels
const pickGroup = new THREE.Group(); helpers.add(pickGroup);
const hlGroup = new THREE.Group(); helpers.add(hlGroup);
const LZ = { L1: 0.0, L2: 15.3333, MEZZ: 13.0208 };
function buildSpaces() {
  S.data.spaces.forEach((sp) => {
    const z = LZ[sp.level] ?? 0; let mesh;
    if (sp.kind === 'zone') { const [x0, x1, y0, y1] = sp.rect; mesh = new THREE.Mesh(new THREE.PlaneGeometry(x1 - x0, y1 - y0), new THREE.MeshBasicMaterial({ visible: false }));
      mesh.position.copy(T((x0 + x1) / 2, (y0 + y1) / 2, z + 0.2)); mesh.rotation.x = -Math.PI / 2; sp.center = [(x0 + x1) / 2, (y0 + y1) / 2]; }
    else { mesh = new THREE.Mesh(new THREE.CircleGeometry(3.0, 24), new THREE.MeshBasicMaterial({ visible: false })); mesh.position.copy(T(sp.point[0], sp.point[1], z + 0.25)); mesh.rotation.x = -Math.PI / 2; sp.center = sp.point; }
    mesh.layers.set(1); mesh.userData.space = sp; mesh.visible = true; pickGroup.add(mesh); sp.pick = mesh;
    const div = document.createElement('div'); div.className = 'lbl ' + (sp.category === 'EXISTING CNSA' ? 'tenant' : sp.kind);
    div.innerHTML = sp.kind === 'tag' ? `<b>${sp.number}</b> ${sp.name}` : sp.name;
    const lbl = new CSS2DObject(div); lbl.position.copy(T(sp.center[0], sp.center[1], z + (sp.kind === 'tag' ? 0.6 : 0.4))); lbl.visible = false; helpers.add(lbl); sp.label = lbl;
  });
  S.spaces = S.data.spaces;
}
function labelFloorMatch(level) { if (S.floor === 'BOTH') return true; if (S.floor === 'L1') return level === 'L1'; return level === 'L2' || level === 'MEZZ'; }
function updateLabels() { const cg = conceptGroups(); S.spaces.forEach((sp) => { let v = S.labels && labelFloorMatch(sp.level); if (sp.category === 'EXISTING CNSA') v = v && cg.has('CNSA'); if (sp.kind === 'zone' && sp.id.startsWith('core_') && S.mode !== 'plan') v = v && false; sp.label.visible = v; }); }
const rayPick = new THREE.Raycaster(); rayPick.layers.set(1);
function pickSpace(px, py) {
  const cg = conceptGroups();
  const nd = new THREE.Vector2((px / innerWidth) * 2 - 1, -(py / innerHeight) * 2 + 1); rayPick.setFromCamera(nd, camera);
  const hits = rayPick.intersectObjects(pickGroup.children, false).filter((h) => { const sp = h.object.userData.space; if (sp.category === 'EXISTING CNSA' && !cg.has('CNSA')) return false; if (!labelFloorMatch(sp.level) && S.mode !== 'walk') return false; return true; });
  if (!hits.length) return;
  // prefer tags (small discs) over zones, then the smallest zone
  hits.sort((a, b) => { const sa = a.object.userData.space, sb = b.object.userData.space; const ka = sa.kind === 'tag' ? 0 : 1, kb = sb.kind === 'tag' ? 0 : 1; if (ka !== kb) return ka - kb; return (sa.area_sqft || 0) - (sb.area_sqft || 0); });
  selectSpace(hits[0].object.userData.space.id);
}
function selectSpace(id) {
  const sp = S.spaces.find((s) => s.id === id); if (!sp) return; clearHighlight(); S.selected = sp;
  const z = LZ[sp.level] ?? 0; const col = sp.category === 'EXISTING CNSA' ? 0x2f80ff : (sp.category === 'FUTURE CONCEPT' ? 0xff9f1c : 0xffd23f);
  if (sp.kind === 'zone') { const [x0, x1, y0, y1] = sp.rect; const geo = new THREE.PlaneGeometry(x1 - x0, y1 - y0);
    const fill = new THREE.Mesh(geo, new THREE.MeshBasicMaterial({ color: col, transparent: true, opacity: 0.32, depthWrite: false, side: THREE.DoubleSide })); fill.position.copy(T((x0 + x1) / 2, (y0 + y1) / 2, z + 0.3)); fill.rotation.x = -Math.PI / 2; fill.renderOrder = 5; hlGroup.add(fill);
    const box = new THREE.LineSegments(new THREE.EdgesGeometry(new THREE.BoxGeometry(x1 - x0, 9.5, y1 - y0)), new THREE.LineBasicMaterial({ color: col })); box.position.copy(T((x0 + x1) / 2, (y0 + y1) / 2, z + 4.9)); hlGroup.add(box); }
  else { const ring = new THREE.Mesh(new THREE.RingGeometry(2.4, 3.4, 40), new THREE.MeshBasicMaterial({ color: col, transparent: true, opacity: 0.85, depthWrite: false, side: THREE.DoubleSide })); ring.position.copy(T(sp.point[0], sp.point[1], z + 0.3)); ring.rotation.x = -Math.PI / 2; ring.renderOrder = 5; hlGroup.add(ring);
    const post = new THREE.Mesh(new THREE.CylinderGeometry(0.15, 0.15, 8, 8), new THREE.MeshBasicMaterial({ color: col })); post.position.copy(T(sp.point[0], sp.point[1], z + 4)); hlGroup.add(post); }
  const rows = [['Name', sp.name], ['Room number', sp.number || '(not documented)'], ['Level', sp.level], ['Category', sp.category], ['Area', sp.area_sqft != null ? `${sp.area_sqft.toLocaleString()} sq ft` : '(not available)'],
    ['Boundary', sp.boundary], ['Source', sp.source || ''], ...(sp.status ? [['Status', sp.status]] : []), ...(sp.note ? [['Note', sp.note]] : []),
    [sp.kind === 'zone' ? 'Extent (ft)' : 'Tag position (ft)', sp.kind === 'zone' ? `x ${sp.rect[0]}-${sp.rect[1]}, y ${sp.rect[2]}-${sp.rect[3]}` : `x ${sp.point[0]}, y ${sp.point[1]}`]];
  $('info').innerHTML = '<table>' + rows.map(([k, v]) => `<tr><td>${k}</td><td>${v}</td></tr>`).join('') + '</table>';
}
function clearHighlight() { while (hlGroup.children.length) { const c = hlGroup.children.pop(); c.geometry?.dispose(); c.material?.dispose(); } S.selected = null; $('info').innerHTML = '<span class="dim">Click a room / space in Orbit or Plan mode.</span>'; }

// ------------------------------------------------------------------------------------------------------------ underlays
const underlays = [];
function buildUnderlays() {
  const tl = new THREE.TextureLoader();
  S.data.underlays.forEach((u) => {
    const tex = tl.load('./' + u.file); tex.colorSpace = THREE.SRGBColorSpace; tex.anisotropy = Math.min(8, renderer.capabilities.getMaxAnisotropy());
    const m = new THREE.Mesh(new THREE.PlaneGeometry(u.x1 - u.x0, u.y1 - u.y0), new THREE.MeshBasicMaterial({ map: tex, transparent: true, opacity: 0.72, depthWrite: false }));
    m.rotation.x = -Math.PI / 2; m.renderOrder = 3; m.visible = false; m.userData.u = u; helpers.add(m); underlays.push(m);
  });
}
function updateUnderlay() { underlays.forEach((m) => { const u = m.userData.u; const on = S.underlay && u.floors.includes(S.floor === 'BOTH' ? 'L1' : S.floor) && S.mode !== 'walk';
  const z = (S.floor === 'MEZZ' ? LZ.MEZZ : (S.floor === 'L2' ? LZ.L2 : LZ.L1)) + 0.06; m.position.copy(T((u.x0 + u.x1) / 2, (u.y0 + u.y1) / 2, z)); m.visible = on; }); }

// ------------------------------------------------------------------------------------------------------------ collision (documented solid geometry only)
const C = { rects: [], segs: [], walk: null, hash: null, cell: 4, reach: null, reachMeta: null };
function buildCollision() { rebuildCollision(); }
function rebuildCollision() {
  const d = S.data.collision; const f = S.floor === 'BOTH' ? 'L1' : S.floor; const fz = LZ[f]; const z0 = fz + d.walker.body_z0_ft, z1 = fz + d.walker.body_z1_ft;
  const zin = (a, b) => a < z1 && b > z0;
  const rects = [];
  const lv = f === 'MEZZ' ? 'L1' : f;                       // the mezzanine sits in the courts volume: Level 1 walls at 13-19.5 ft do not reach, filtered by z anyway
  const push = (arr, tag) => arr.forEach((r) => { if (zin(r[4], r[5])) rects.push([r[0], r[1], r[2], r[3], tag || r[6]]); });
  push(d.walls[lv] || [], null); push(d.columns, null); push(d.hoistway, null); push(d.stairs, null); push(d.opening_lites, null);
  if (f === 'MEZZ') push(d.walls.L2 || [], null);
  if (conceptGroups().has('CNSA')) push(d.cnsa[lv] || [], 'CNSA partition');
  const segs = d.exterior_segments.filter((s) => zin(s[4], s[5]));
  C.rects = rects; C.segs = segs; C.walk = d.walkable[f]; C.floor = f;
  // spatial hash
  const cell = C.cell; const h = new Map(); const key = (i, j) => i * 100003 + j;
  const add = (k, v) => { let a = h.get(k); if (!a) { a = []; h.set(k, a); } a.push(v); };
  rects.forEach((r, idx) => { for (let i = Math.floor((r[0] - 1.5) / cell); i <= Math.floor((r[1] + 1.5) / cell); i++) for (let j = Math.floor((r[2] - 1.5) / cell); j <= Math.floor((r[3] + 1.5) / cell); j++) add(key(i, j), ['r', idx]); });
  segs.forEach((s, idx) => { const x0 = Math.min(s[0], s[2]) - 1.5, x1 = Math.max(s[0], s[2]) + 1.5, y0 = Math.min(s[1], s[3]) - 1.5, y1 = Math.max(s[1], s[3]) + 1.5;
    for (let i = Math.floor(x0 / cell); i <= Math.floor(x1 / cell); i++) for (let j = Math.floor(y0 / cell); j <= Math.floor(y1 / cell); j++) add(key(i, j), ['s', idx]); });
  C.hash = h; C.key = key; C.reach = null;
}
function pointInPoly(x, y, poly) { let inside = false; for (let i = 0, j = poly.length - 1; i < poly.length; j = i++) { const xi = poly[i][0], yi = poly[i][1], xj = poly[j][0], yj = poly[j][1];
  if (((yi > y) !== (yj > y)) && (x < (xj - xi) * (y - yi) / (yj - yi) + xi)) inside = !inside; } return inside; }
function onWalkable(x, y) { const w = C.walk; if (!w) return true; if (w.rects) for (const r of w.rects) if (x >= r[0] && x <= r[1] && y >= r[2] && y <= r[3]) return true;
  let inside = false; for (const p of (w.polygons || [])) if (pointInPoly(x, y, p)) inside = !inside; return inside; }
function blockedAt(x, y, r) {
  const bucket = C.hash.get(C.key(Math.floor(x / C.cell), Math.floor(y / C.cell))); if (!bucket) return null;
  for (const [t, i] of bucket) {
    if (t === 'r') { const q = C.rects[i]; if (x > q[0] - r && x < q[1] + r && y > q[2] - r && y < q[3] + r) return q[4] || 'wall'; }
    else { const s = C.segs[i]; const dx = s[2] - s[0], dy = s[3] - s[1]; const L2 = dx * dx + dy * dy; let tt = L2 > 0 ? ((x - s[0]) * dx + (y - s[1]) * dy) / L2 : 0; tt = Math.max(0, Math.min(1, tt));
      const px = s[0] + tt * dx, py = s[1] + tt * dy; if ((x - px) * (x - px) + (y - py) * (y - py) < r * r) return 'exterior wall'; }
  }
  return null;
}
const PROBES = [[0, 0], [1, 0], [-1, 0], [0, 1], [0, -1], [0.707, 0.707], [-0.707, 0.707], [0.707, -0.707], [-0.707, -0.707]];
function free(x, y) { const r = S.data.collision.walker.radius_ft; if (blockedAt(x, y, r)) return false; for (const [px, py] of PROBES) if (!onWalkable(x + px * r * 0.95, y + py * r * 0.95)) return false; return true; }
function blockReason(x, y) { const r = S.data.collision.walker.radius_ft; const b = blockedAt(x, y, r); if (b) return b; for (const [px, py] of PROBES) if (!onWalkable(x + px * r * 0.95, y + py * r * 0.95)) return 'slab edge / floor opening'; return null; }
// reachability grid (documented walking route from the floor's route origin)
function reachGrid() {
  if (C.reach && C.reachMeta === C.floor + '|' + S.concept) return C.reach;
  const cs = 0.5, x0 = -10, y0 = -15, nx = Math.ceil(320 / cs), ny = Math.ceil(240 / cs); const g = new Uint8Array(nx * ny); const o = S.data.collision.route_origins[C.floor];
  const idx = (x, y) => { const i = Math.floor((x - x0) / cs), j = Math.floor((y - y0) / cs); return (i < 0 || j < 0 || i >= nx || j >= ny) ? -1 : j * nx + i; };
  const start = idx(o.x, o.y); const q = [start]; g[start] = 1; let head = 0;
  while (head < q.length) { const k = q[head++]; const i = k % nx, j = (k - i) / nx;
    for (const [di, dj] of [[1, 0], [-1, 0], [0, 1], [0, -1]]) { const ii = i + di, jj = j + dj; if (ii < 0 || jj < 0 || ii >= nx || jj >= ny) continue; const kk = jj * nx + ii; if (g[kk]) continue;
      const x = x0 + (ii + 0.5) * cs, y = y0 + (jj + 0.5) * cs; if (free(x, y)) { g[kk] = 1; q.push(kk); } else g[kk] = 2; } }
  C.reach = { g, idx, cells: q.length }; C.reachMeta = C.floor + '|' + S.concept; return C.reach;
}
function reachable(x, y) { const r = reachGrid(); const k = r.idx(x, y); return k >= 0 && r.g[k] === 1; }
function freeRun(x, y, ang) { let d = 0; const dx = Math.sin(ang), dy = Math.cos(ang); while (d < 80 && free(x + dx * (d + 0.5), y + dy * (d + 0.5))) d += 0.5; return d; }
function nearestFree(x, y, maxR = 8) { if (free(x, y)) return { x, y, adjusted: 0 }; for (let rad = 0.5; rad <= maxR; rad += 0.5) for (let a = 0; a < 360; a += 15) { const xx = x + rad * Math.cos(a * Math.PI / 180), yy = y + rad * Math.sin(a * Math.PI / 180); if (free(xx, yy)) return { x: xx, y: yy, adjusted: rad }; } return { x, y, adjusted: -1 }; }

// ------------------------------------------------------------------------------------------------------------ walker
function walkerPos() { return W.pos[S.floor] || { x: 50, y: 70 }; }
function teleport(x, y) { const p = nearestFree(x, y); W.pos[S.floor] = { x: p.x, y: p.y }; return p; }
function stepWalker(dt, keys, shift) {
  const wk = S.data.collision.walker; const sp = shift ? wk.shift_speed_ft_s : wk.speed_ft_s;
  let f = 0, r = 0; if (keys.KeyW || keys.ArrowUp) f += 1; if (keys.KeyS || keys.ArrowDown) f -= 1; if (keys.KeyD || keys.ArrowRight) r += 1; if (keys.KeyA || keys.ArrowLeft) r -= 1;
  if (!f && !r) return { moved: 0, blocked: null };
  const n = Math.hypot(f, r); f /= n; r /= n;
  const fx = Math.sin(W.yaw), fy = Math.cos(W.yaw); const rx = Math.cos(W.yaw), ry = -Math.sin(W.yaw);
  let dx = (fx * f + rx * r) * sp * dt, dy = (fy * f + ry * r) * sp * dt;
  const dist = Math.hypot(dx, dy); const nsub = Math.max(1, Math.ceil(dist / wk.substep_ft)); const sx = dx / nsub, sy = dy / nsub;
  const p = walkerPos(); let blocked = null, moved = 0;
  for (let i = 0; i < nsub; i++) {
    if (free(p.x + sx, p.y + sy)) { p.x += sx; p.y += sy; moved += Math.hypot(sx, sy); continue; }
    let slid = false;
    if (Math.abs(sx) > 1e-9 && free(p.x + sx, p.y)) { p.x += sx; moved += Math.abs(sx); slid = true; }
    else if (Math.abs(sy) > 1e-9 && free(p.x, p.y + sy)) { p.y += sy; moved += Math.abs(sy); slid = true; }
    if (!slid) { blocked = blockReason(p.x + sx, p.y + sy) || 'blocked'; break; }
  }
  return { moved, blocked };
}
function placeWalkerCamera() { const p = walkerPos(); const eye = W.floorZ + S.data.collision.walker.eye_ft; persp.position.copy(T(p.x, p.y, eye));
  const cp = Math.cos(W.pitch); persp.lookAt(T(p.x + Math.sin(W.yaw) * cp, p.y + Math.cos(W.yaw) * cp, eye + Math.sin(W.pitch))); }

// ------------------------------------------------------------------------------------------------------------ viewpoints
function buildViewpoints() {
  const box = $('viewpoints'); box.innerHTML = '';
  S.data.viewpoints.forEach((v) => { const b = document.createElement('button'); b.className = 'vp'; b.id = 'vp_btn_' + v.id; b.innerHTML = `${v.label}<span class="sub">${v.mode.toUpperCase()} &middot; ${v.floor}</span>`; b.onclick = () => gotoViewpoint(v.id); box.appendChild(b); v.button = b; });
  // route classification (needs the collision of each floor): computed lazily per floor when the viewpoint is used, and for the list now
  ['L1', 'L2', 'MEZZ'].forEach((f) => { const keep = S.floor; S.floor = f; rebuildCollision(); S.data.viewpoints.filter((v) => v.mode === 'walk' && v.floor === f).forEach((v) => { const p = nearestFree(v.eye[0], v.eye[1]); v.route = reachable(p.x, p.y) ? 'walk' : 'tele'; v.adjusted = p.adjusted;
      v.button.innerHTML = `${v.label}<span class="route ${v.route}">${v.route === 'walk' ? 'DOCUMENTED WALKABLE ROUTE' : 'VIEWPOINT TELEPORT'}</span><span class="sub">${v.note}</span>`; }); S.floor = keep; });
  rebuildCollision();
}
function gotoViewpoint(id) {
  const v = S.data.viewpoints.find((x) => x.id === id); if (!v) return;
  if (v.mode === 'walk') { setFloor(v.floor); setMode('walk'); const p = teleport(v.eye[0], v.eye[1]); const dx = v.look_at[0] - p.x, dy = v.look_at[1] - p.y; W.yaw = Math.atan2(dx, dy); W.pitch = Math.atan2(v.look_at[2] - v.eye[2], Math.hypot(dx, dy)); W.lastRoute = v.route;
    // if the documented look direction is blocked within 8 ft (a partition in front of the eye), turn to the longest free run so the reviewer sees the space
    const run = freeRun(p.x, p.y, W.yaw); v.orientAdjusted = false;
    if (run < 8) { let best = W.yaw, bestRun = run; for (let a = 0; a < 32; a++) { const ang = a * Math.PI / 16; const r = freeRun(p.x, p.y, ang); if (r > bestRun) { bestRun = r; best = ang; } } if (best !== W.yaw) { W.yaw = best; W.pitch = 0; v.orientAdjusted = true; } } }
  else if (v.mode === 'orbit') { setFloor(v.floor); setMode('orbit'); persp.position.copy(T(...v.eye)); orbit.target.copy(T(...v.look_at)); orbit.update(); }
  else { setFloor(v.floor); setMode('plan'); PLAN.cx = v.eye[0]; PLAN.cy = v.eye[1]; PLAN.halfW = 175; setOrthoFrustum(); }
  if (S.mode === 'walk') placeWalkerCamera();
  updateStatus();
}
function resetOrbit() { persp.position.copy(T(-140, 330, 150)); orbit.target.copy(T(145, 100, 10)); orbit.update(); }

// ------------------------------------------------------------------------------------------------------------ measurement
const mGroup = new THREE.Group(); helpers.add(mGroup);
const rayM = new THREE.Raycaster(); rayM.layers.set(0);
function measureClick(px, py) {
  const nd = new THREE.Vector2((px / innerWidth) * 2 - 1, -(py / innerHeight) * 2 + 1); rayM.setFromCamera(nd, camera);
  const cands = S.meshes.filter((m) => m.visible); const hits = rayM.intersectObjects(cands, false);
  const hit = hits.find((h) => { let o = h.object; while (o) { if (o.visible === false) return false; o = o.parent; } if (renderer.clippingPlanes.length && h.point.y > clipPlane.constant) return false; return true; });
  if (!hit) return; measureAdd(B(hit.point));
}
function measureAdd(p) {
  if (S.measure.length >= 2) { clearMeasure(true); }
  S.measure.push(p);
  const mk = new THREE.Mesh(new THREE.SphereGeometry(0.35, 12, 12), new THREE.MeshBasicMaterial({ color: 0xff3b3b })); mk.position.copy(T(p.x, p.y, p.z)); mGroup.add(mk);
  if (S.measure.length === 2) {
    const [a, b] = S.measure; const line = new THREE.Line(new THREE.BufferGeometry().setFromPoints([T(a.x, a.y, a.z), T(b.x, b.y, b.z)]), new THREE.LineBasicMaterial({ color: 0xff3b3b })); mGroup.add(line);
    const dz = b.z - a.z, dh = Math.hypot(b.x - a.x, b.y - a.y), dt = Math.hypot(dh, dz);
    $('measureOut').innerHTML = '<table>' + [['Total distance', fmt(dt)], ['Horizontal', fmt(dh)], ['Vertical', fmt(dz)], ['Point A (x, y, z ft)', `${a.x.toFixed(2)}, ${a.y.toFixed(2)}, ${a.z.toFixed(2)}`], ['Point B (x, y, z ft)', `${b.x.toFixed(2)}, ${b.y.toFixed(2)}, ${b.z.toFixed(2)}`]].map(([k, v]) => `<tr><td>${k}</td><td>${v}</td></tr>`).join('') + '</table><div class="warn">SPATIAL REVIEW ONLY - model v014 coordinates, not a survey</div>';
    return { total: dt, horizontal: dh, vertical: dz, a, b };
  }
  $('measureOut').innerHTML = `<span class="dim">Point A: ${p.x.toFixed(2)}, ${p.y.toFixed(2)}, ${p.z.toFixed(2)} ft - click the second point.</span>`;
}
function clearMeasure(keepTool) { while (mGroup.children.length) { const c = mGroup.children.pop(); c.geometry?.dispose(); c.material?.dispose(); } S.measure = []; if (!keepTool) { setMeasuring(false); $('measure').classList.add('hidden'); } }

// ------------------------------------------------------------------------------------------------------------ save image
function timestamp() { const d = new Date(), p = (n) => String(n).padStart(2, '0'); return `${d.getFullYear()}${p(d.getMonth() + 1)}${p(d.getDate())}_${p(d.getHours())}${p(d.getMinutes())}${p(d.getSeconds())}`; }
async function saveImage(nameOverride) {
  if (S.mode === 'walk') placeWalkerCamera();
  renderer.render(scene, camera); labelRenderer.render(scene, camera);
  // composite: WebGL frame + visible HTML room labels + a footer (the labels are DOM elements, not part of the canvas)
  const off = document.createElement('canvas'); off.width = canvas.width; off.height = canvas.height; const g = off.getContext('2d'); g.drawImage(canvas, 0, 0);
  const k = canvas.width / innerWidth; g.textBaseline = 'middle';
  document.querySelectorAll('#labels .lbl').forEach((el) => { if (el.style.display === 'none' || !el.offsetParent) return; const r = el.getBoundingClientRect(); if (r.width === 0) return;
    g.font = `${Math.round(11 * k)}px system-ui, Arial`; const txt = el.textContent; const w = g.measureText(txt).width + 10 * k; const x = r.left * k, y = r.top * k, h = r.height * k;
    g.fillStyle = el.classList.contains('tenant') ? 'rgba(214,232,255,0.92)' : (el.classList.contains('zone') ? 'rgba(255,246,214,0.9)' : 'rgba(255,255,255,0.88)'); g.fillRect(x, y, w, h); g.strokeStyle = 'rgba(0,0,0,0.4)'; g.strokeRect(x, y, w, h); g.fillStyle = '#111'; g.fillText(txt, x + 5 * k, y + h / 2); });
  if (S.measure.length === 2) { const [a, b] = S.measure; const dz = b.z - a.z, dh = Math.hypot(b.x - a.x, b.y - a.y), dt = Math.hypot(dh, dz);
    g.font = `${Math.round(13 * k)}px Consolas, monospace`; const lines = [`MEASURE (SPATIAL REVIEW ONLY): total ${ftin(dt)}  horizontal ${ftin(dh)}  vertical ${ftin(dz)}`, `A (${a.x.toFixed(2)}, ${a.y.toFixed(2)}, ${a.z.toFixed(2)}) ft   B (${b.x.toFixed(2)}, ${b.y.toFixed(2)}, ${b.z.toFixed(2)}) ft`];
    g.fillStyle = 'rgba(0,0,0,0.65)'; g.fillRect(10 * k, 10 * k, 640 * k, 44 * k); g.fillStyle = '#ffd23f'; lines.forEach((t, i) => g.fillText(t, 18 * k, (22 + 18 * i) * k)); }
  g.font = `${Math.round(12 * k)}px Consolas, monospace`; const foot = `Building I  model v014 / viewer v015  |  ${S.mode.toUpperCase()}  floor ${S.floor}  concept ${S.concept}  |  ${new Date().toISOString().slice(0, 19).replace('T', ' ')}  |  spatial review only`;
  g.fillStyle = 'rgba(0,0,0,0.6)'; g.fillRect(0, off.height - 22 * k, off.width, 22 * k); g.fillStyle = '#ddd'; g.fillText(foot, 10 * k, off.height - 11 * k);
  const url = off.toDataURL('image/png');
  const name = nameOverride || `BuildingI_v015_${S.mode}_${S.floor}_${timestamp()}.png`;
  if (S.captureOK) { try { const r = await (await fetch('/__capture', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ name, dataURL: url }) })).json(); if (!nameOverride) download(url, name); return r.saved; } catch (e) { /* fall through */ } }
  download(url, name); return name;
}
function download(url, name) { const a = document.createElement('a'); a.href = url; a.download = name; document.body.appendChild(a); a.click(); a.remove(); }

// ------------------------------------------------------------------------------------------------------------ frame loop
const timer = new THREE.Timer(); let fpsAcc = 0, fpsN = 0, fps = 0, lastBlocked = null;
function frame() {
  timer.update(); const dt = Math.min(timer.getDelta(), 0.25);
  if (S.mode === 'walk') { const r = stepWalker(dt, W.keys, W.shift); lastBlocked = r.blocked; placeWalkerCamera(); }
  else if (S.mode === 'orbit') orbit.update();
  renderer.render(scene, camera); labelRenderer.render(scene, camera);
  fpsAcc += dt; fpsN++; if (fpsAcc >= 0.5) { fps = fpsN / fpsAcc; fpsAcc = 0; fpsN = 0; updateStatus(); }
}
function updateStatus() {
  const p = walkerPos(); const i = renderer.info.render; let s = `mode ${S.mode.toUpperCase()} | floor ${S.floor} | concept ${S.concept} | fps ${fps.toFixed(0)} | draw calls ${i.calls} | triangles ${i.triangles.toLocaleString()}`;
  if (S.mode === 'walk') { const rc = reachable(p.x, p.y); s += ` | walker x ${p.x.toFixed(1)} y ${p.y.toFixed(1)} z ${(W.floorZ + 5.5).toFixed(2)} ft (eye 5'-6") heading ${((W.yaw * 180 / Math.PI) % 360 + 360).toFixed(0) % 360}° | ${rc ? 'on DOCUMENTED WALKABLE ROUTE' : 'TELEPORTED - no documented walking route from the ' + S.data.collision.route_origins[S.floor].why.split(' (')[0]}${lastBlocked ? ' | blocked by ' + lastBlocked : ''}`; }
  $('st').textContent = s;
}

// ------------------------------------------------------------------------------------------------------------ test / automation API (window.BI)
const api = {
  get state() { return { mode: S.mode, floor: S.floor, concept: S.concept, labels: S.labels, underlay: S.underlay, presentation: S.presentation, measuring: S.measuring, layers: { ...S.layers }, walker: { ...walkerPos(), yaw: W.yaw, pitch: W.pitch, floorZ: W.floorZ }, captureOK: S.captureOK }; },
  setMode, setFloor, setConcept, setLayer, setLabels, setUnderlay, setPresentation, gotoViewpoint, selectSpace, clearHighlight, setMeasuring, clearMeasure, saveImage, teleport, free, reachable, blockReason,
  look(yawDeg, pitchDeg) { W.yaw = yawDeg * Math.PI / 180; W.pitch = pitchDeg * Math.PI / 180; placeWalkerCamera(); },
  measureAt(px, py) { if (!S.measuring) setMeasuring(true); measureClick(px, py); return S.measure.map((p) => ({ ...p })); },
  measure(a, b) { clearMeasure(true); $('measure').classList.remove('hidden'); measureAdd(a); return measureAdd(b); },
  simulate(keys, seconds, shift, fps) { const dt = 1 / (fps || 60); const from = { ...walkerPos() }; let t = 0, moved = 0, blocked = null; const k = {}; keys.forEach((x) => k[x] = true);
    while (t < seconds - 1e-9) { const r = stepWalker(Math.min(dt, seconds - t), k, !!shift); moved += r.moved; if (r.blocked) blocked = r.blocked; t += dt; } const to = { ...walkerPos() }; placeWalkerCamera();
    return { from, to, displacement: Math.hypot(to.x - from.x, to.y - from.y), moved, blocked, seconds, fps: fps || 60, shift: !!shift }; },
  stats() { const i = renderer.info.render; return { fps, calls: i.calls, triangles: i.triangles, meshes: S.meshes.length, groups: Object.fromEntries(Object.entries(S.groups).map(([k, g]) => [k, g.meshes.length])) }; },
  collision() { return { floor: C.floor, rects: C.rects.length, segs: C.segs.length, reach: reachGrid().cells }; },
  orbitTo(eye, target) { setMode('orbit'); persp.position.copy(T(...eye)); orbit.target.copy(T(...target)); orbit.update(); },
  planTo(cx, cy, halfW) { setMode('plan'); PLAN.cx = cx; PLAN.cy = cy; PLAN.halfW = halfW; setOrthoFrustum(); },
  render() { if (S.mode === 'walk') placeWalkerCamera(); renderer.render(scene, camera); labelRenderer.render(scene, camera); },
  spaces: () => S.data.spaces.map((s) => ({ id: s.id, kind: s.kind, name: s.name, number: s.number, level: s.level, category: s.category })),
  viewpoints: () => S.data.viewpoints.map((v) => ({ id: v.id, label: v.label, mode: v.mode, floor: v.floor, route: v.route || null, adjusted: v.adjusted, orientAdjusted: !!v.orientAdjusted })),
};
main().catch((e) => { $('overlayText').textContent = 'Viewer failed to load: ' + e; console.error(e); });
