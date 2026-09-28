r"""Long-path-aware SHA-256 freeze manifest / validator for the Building I sources.

The bundled freeze_manifest.py skips files whose full path exceeds the Windows
260-character limit (159 of the 1,231 Building I source files). This script
walks the folder through the \\?\ extended-length prefix so every file is hashed.

Usage (from the project root):
  python scripts/Building_I/BI_freeze_manifest_longpath_v001.py write   -> writes the manifest
  python scripts/Building_I/BI_freeze_manifest_longpath_v001.py check   -> validates against it
"""
from pathlib import Path
import datetime
import hashlib
import json
import os
import sys

ROOT = Path(__file__).resolve().parent.parent.parent
SRC = ROOT / "source_documents" / "Building I"
SRC_LP = "\\\\?\\" + str(SRC) if os.name == "nt" else str(SRC)
OUT = ROOT / "notes" / "Building_I" / "manifests" / "BI_freeze_sources_BuildingI_longpath_v001.json"


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def walk():
    for dp, dn, fn in os.walk(SRC_LP):
        for f in fn:
            p = os.path.join(dp, f)
            yield os.path.relpath(p, SRC_LP).replace("\\", "/"), p


def write():
    rows = []
    for rel, p in walk():
        rows.append({"path": rel, "size": os.path.getsize(p), "sha256": sha256(p)})
    rows.sort(key=lambda r: r["path"])
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps({"root": str(SRC), "created_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
                               "files": rows}, indent=1), encoding="utf-8")
    print(f"Wrote {len(rows)} files ({sum(r['size'] for r in rows)} bytes) to {OUT}")


def check():
    d = json.loads(OUT.read_text(encoding="utf-8"))
    errors = []
    for r in d["files"]:
        p = os.path.join(SRC_LP, r["path"].replace("/", "\\"))
        if not os.path.exists(p):
            errors.append("MISSING " + r["path"])
        elif os.path.getsize(p) != r["size"]:
            errors.append("SIZE " + r["path"])
        elif sha256(p) != r["sha256"]:
            errors.append("HASH " + r["path"])
    present = sum(1 for _ in walk())
    if errors:
        print(f"FAILED: {len(errors)} mismatches")
        for e in errors[:50]:
            print(e)
        sys.exit(1)
    print(f"PASS: {len(d['files'])} frozen files unchanged; {present} files present now")


if __name__ == "__main__":
    {"write": write, "check": check}[sys.argv[1]]()
