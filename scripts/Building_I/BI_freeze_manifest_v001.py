#!/usr/bin/env python3
from pathlib import Path
import argparse, hashlib, json, datetime

def sha256(path, chunk=1024*1024):
    h = hashlib.sha256()
    with path.open("rb") as f:
        while True:
            b = f.read(chunk)
            if not b: break
            h.update(b)
    return h.hexdigest()

def main():
    p = argparse.ArgumentParser(description="Create SHA-256 manifest for files to freeze.")
    p.add_argument("root")
    p.add_argument("output")
    p.add_argument("--exclude", action="append", default=[])
    args = p.parse_args()
    root = Path(args.root).resolve()
    out = Path(args.output).resolve()
    excludes = [str((root / e).resolve()) for e in args.exclude]
    rows = []
    for f in sorted(x for x in root.rglob("*") if x.is_file()):
        rf = str(f.resolve())
        if f.resolve() == out or any(rf.startswith(e) for e in excludes):
            continue
        rows.append({"path": f.relative_to(root).as_posix(), "size": f.stat().st_size, "sha256": sha256(f)})
    payload = {"root": str(root), "created_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(), "files": rows}
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(f"Wrote {len(rows)} files to {out}")

if __name__ == "__main__":
    main()
