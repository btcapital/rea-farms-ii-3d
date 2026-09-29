"""Building II print v003 - helpers for Bambu Studio multi-part / multi-filament 3MF files and Bambu CLI tests.

Pure Python + numpy (usable from system Python or Blender). Nothing here touches project models.

write_bambu_3mf(path, objects, filaments, title)
    objects   = [dict(name, parts=[dict(name, co_mm (N,3), tv (M,3), extruder)], transform=12 floats)]
    filaments = [dict(name, colour "#RRGGBB", type)] in slot order 1..n (only used for the project colour list)
    Writes the Bambu Studio project layout: 3D/3dmodel.model (objects built from <components>),
    3D/Objects/object_<k>.model (one mesh per part), Metadata/model_settings.config (per-part extruder),
    Metadata/project_settings.config (filament colours / names) when a base config is given.
flatten_profile(system_dir, kind, name, overrides) -> dict    resolves the "inherits" chain of a system preset
"""
import json, os, uuid, zipfile
import numpy as np

NS = ('xmlns="http://schemas.microsoft.com/3dmanufacturing/core/2015/02" '
      'xmlns:BambuStudio="http://schemas.bambulab.com/package/2021" '
      'xmlns:p="http://schemas.microsoft.com/3dmanufacturing/production/2015/06" requiredextensions="p"')

def _mesh_xml(obj_id, co, tv):
    v = "".join(f'<vertex x="{x:.6f}" y="{y:.6f}" z="{z:.6f}"/>' for x, y, z in co)
    t = "".join(f'<triangle v1="{a}" v2="{b}" v3="{c}"/>' for a, b, c in tv)
    return (f'<object id="{obj_id}" p:UUID="{uuid.uuid4()}" type="model"><mesh><vertices>{v}</vertices>'
            f'<triangles>{t}</triangles></mesh></object>')

def write_bambu_3mf(path, objects, title, project_settings=None, designer="Rea Farms Building II print derivative", app_tag=False):
    """app_tag=False (default) writes a GENERIC 3MF (no Bambu application tag in the main model): Bambu Studio then
    imports it as a model with per-part filaments from Metadata/model_settings.config. With the application tag but no
    full project settings the Bambu CLI crashes (0xC0000005) - see PRINT_EXPORT.md Part C."""
    top = [f'<?xml version="1.0" encoding="UTF-8"?>\n<model unit="millimeter" xml:lang="en-US" {NS}>']
    if app_tag:
        top += ['<metadata name="Application">BambuStudio-02.08.02.61</metadata>', '<metadata name="BambuStudio:3mfVersion">1</metadata>']
    top += [f'<metadata name="Title">{title}</metadata>', f'<metadata name="Designer">{designer}</metadata>', '<resources>']
    subfiles, rels, cfg, build = {}, [], ['<?xml version="1.0" encoding="UTF-8"?>\n<config>'], []
    next_id = 1
    for k, ob in enumerate(objects, 1):
        sub = f"3D/Objects/object_{k}.model"
        comps, meshes = [], []
        cfg.append(f'  <object id="{{OID}}">\n    <metadata key="name" value="{ob["name"]}"/>\n'
                   f'    <metadata key="extruder" value="{ob["parts"][0]["extruder"]}"/>')
        part_cfg = []
        for part in ob["parts"]:
            pid = next_id; next_id += 1
            meshes.append(_mesh_xml(pid, part["co_mm"], part["tv"]))
            comps.append(f'<component p:path="/{sub}" objectid="{pid}" p:UUID="{uuid.uuid4()}" transform="1 0 0 0 1 0 0 0 1 0 0 0"/>')
            part_cfg.append(f'    <part id="{pid}" subtype="normal_part">\n      <metadata key="name" value="{part["name"]}"/>\n'
                            f'      <metadata key="matrix" value="1 0 0 0 0 1 0 0 0 0 1 0 0 0 0 1"/>\n'
                            f'      <metadata key="extruder" value="{part["extruder"]}"/>\n    </part>')
        oid = next_id; next_id += 1
        cfg[-1] = cfg[-1].replace("{OID}", str(oid))
        cfg.extend(part_cfg); cfg.append("  </object>")
        top.append(f'<object id="{oid}" p:UUID="{uuid.uuid4()}" type="model"><components>{"".join(comps)}</components></object>')
        build.append(f'<item objectid="{oid}" p:UUID="{uuid.uuid4()}" transform="{" ".join(f"{t:.6f}" for t in ob["transform"])}" printable="1"/>')
        subfiles[sub] = (f'<?xml version="1.0" encoding="UTF-8"?>\n<model unit="millimeter" xml:lang="en-US" {NS}>'
                         f'<metadata name="BambuStudio:3mfVersion">1</metadata><resources>{"".join(meshes)}</resources><build/></model>')
        rels.append(f'<Relationship Target="/{sub}" Id="rel-{k}" Type="http://schemas.microsoft.com/3dmanufacturing/2013/01/3dmodel"/>')
    top.append("</resources>"); top.append(f'<build p:UUID="{uuid.uuid4()}">{"".join(build)}</build></model>')
    # one plate holding every object (Bambu's slicer iterates plates; a project without a plate block crashes the CLI)
    top_ids = [int(b.split('objectid="')[1].split('"')[0]) for b in build]
    cfg.append('  <plate>\n    <metadata key="plater_id" value="1"/>\n    <metadata key="plater_name" value=""/>\n'
               '    <metadata key="locked" value="false"/>')
    for i, oid in enumerate(top_ids):
        cfg.append(f'    <model_instance>\n      <metadata key="object_id" value="{oid}"/>\n'
                   f'      <metadata key="instance_id" value="0"/>\n      <metadata key="identify_id" value="{100 + i}"/>\n    </model_instance>')
    cfg.append("  </plate>\n  <assemble>\n  </assemble>")
    cfg.append("</config>")
    ct = ('<?xml version="1.0" encoding="UTF-8"?>\n<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
          '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
          '<Default Extension="model" ContentType="application/vnd.ms-package.3dmanufacturing-3dmodel+xml"/>'
          '<Default Extension="png" ContentType="image/png"/><Default Extension="gcode" ContentType="text/x.gcode"/></Types>')
    root_rels = ('<?xml version="1.0" encoding="UTF-8"?>\n<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
                 '<Relationship Target="/3D/3dmodel.model" Id="rel-1" Type="http://schemas.microsoft.com/3dmanufacturing/2013/01/3dmodel"/></Relationships>')
    model_rels = ('<?xml version="1.0" encoding="UTF-8"?>\n<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
                  + "".join(rels) + "</Relationships>")
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("[Content_Types].xml", ct); z.writestr("_rels/.rels", root_rels)
        z.writestr("3D/3dmodel.model", "".join(top)); z.writestr("3D/_rels/3dmodel.model.rels", model_rels)
        for k, v in subfiles.items():
            z.writestr(k, v)
        z.writestr("Metadata/model_settings.config", "\n".join(cfg))
        if project_settings is not None:
            z.writestr("Metadata/project_settings.config", json.dumps(project_settings, indent=4))

def _load_chain(system_dir, kind, name):
    chain, cur = [], name
    while cur:
        with open(os.path.join(system_dir, kind, cur + ".json"), encoding="utf-8") as f:
            j = json.load(f)
        chain.append(j); cur = j.get("inherits")
    out = {}
    for j in reversed(chain):
        out.update(j)
    return out

def _machine_templates(system_dir, flat):
    """H2S machine presets keep their G-code in '<name> template <key>.json' files referenced by name."""
    for k, v in list(flat.items()):
        if isinstance(v, str) and v.endswith(".json") is False and " template " in v:
            p = os.path.join(system_dir, "machine", v + ".json")
            if os.path.exists(p):
                t = json.load(open(p, encoding="utf-8"))
                for tk, tv in t.items():
                    if tk not in ("name", "instantiation", "type", "from", "inherits", "setting_id"):
                        flat[tk] = tv
    return flat

def project_settings(system_dir, machine, process, filaments):
    """Full Bambu project config: machine + process + per-filament arrays. filaments = [(preset, colour)]."""
    mach = _machine_templates(system_dir, _load_chain(system_dir, "machine", machine))
    proc = _load_chain(system_dir, "process", process)
    fils = [_load_chain(system_dir, "filament", f) for f, _ in filaments]
    ps = {}
    for src in (mach, proc):
        for k, v in src.items():
            if k not in ("name", "inherits", "from", "instantiation", "setting_id", "type", "compatible_printers",
                         "compatible_printers_condition", "compatible_prints", "compatible_prints_condition", "filament_id"):
                ps[k] = v
    fkeys = set().union(*[set(f) for f in fils]) - {"name", "inherits", "from", "instantiation", "setting_id", "type",
                                                   "compatible_printers", "compatible_printers_condition",
                                                   "compatible_prints", "compatible_prints_condition"}
    for k in sorted(fkeys):
        vals = []
        for f in fils:
            v = f.get(k)
            if isinstance(v, list):
                vals.append(v[0] if v else "")
            elif v is not None:
                vals.append(v)
            else:
                vals.append("")
        ps[k] = vals
    ps["filament_colour"] = [c for _, c in filaments]
    ps["filament_settings_id"] = [f for f, _ in filaments]
    ps["filament_ids"] = [f.get("filament_id", "") for f in fils]
    ps["print_settings_id"] = process; ps["printer_settings_id"] = machine
    ps["filament_map"] = ["1"] * len(filaments)
    return ps

def flatten_profile(system_dir, kind, name, overrides=None):
    """Resolve a Bambu system preset's inherits chain (kind = machine | process | filament)."""
    chain = []
    cur = name
    while cur:
        with open(os.path.join(system_dir, kind, cur + ".json"), encoding="utf-8") as f:
            j = json.load(f)
        chain.append(j); cur = j.get("inherits")
    out = {}
    for j in reversed(chain):
        out.update(j)
    out.pop("inherits", None)
    out["from"] = "User"; out["name"] = name + (" (flattened)" if overrides else "")
    if overrides:
        out.update(overrides)
    return out
