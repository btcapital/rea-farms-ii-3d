#!/usr/bin/env python3
from pathlib import Path
import argparse, hashlib, json, sys

def sha256(path, chunk=1024*1024):
    h = hashlib.sha256()
    with path.open("rb") as f:
        while True:
            b = f.read(chunk)
            if not b: break
            h.update(b)
    return h.hexdigest()

def main():
    p = argparse.ArgumentParser(description="Validate files against a freeze manifest.")
    p.add_argument("manifest")
    args = p.parse_args()
    mpath = Path(args.manifest).resolve()
    data = json.loads(mpath.read_text(encoding="utf-8"))
    root = Path(data["root"])
    errors = []
    for row in data["files"]:
        f = root / row["path"]
        if not f.exists():
            errors.append(f"MISSING {row['path']}")
            continue
        if f.stat().st_size != row["size"]:
            errors.append(f"SIZE {row['path']}")
            continue
        if sha256(f) != row["sha256"]:
            errors.append(f"HASH {row['path']}")
    if errors:
        print(f"FAILED: {len(errors)} mismatches")
        for e in errors[:100]: print(e)
        sys.exit(1)
    print(f"PASS: {len(data['files'])} frozen files unchanged")

if __name__ == "__main__":
    main()
