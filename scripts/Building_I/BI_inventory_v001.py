"""BI_inventory_v001.py - Building I source-document inventory (READ-ONLY).

Reads only. Never writes inside source_documents. Produces four TSV tables in
notes/Building_I/:
  BI_file_inventory_v001.tsv                 every file under source_documents/Building I
  BI_sheet_index_rev6_v001.tsv               page -> sheet number / name / revisions listed (Rev 6 approved set)
  BI_sheet_index_rev14_v001.tsv              same for the Rev 14 record set
  BI_sheet_revision_comparison_v001.tsv      sheet-by-sheet revision lists, Rev 6 vs Rev 14

Requires Poppler's pdftotext on PATH (installed via winget) and system Python (no numpy needed).
Run from the project root:  python scripts/Building_I/BI_inventory_v001.py
"""
import os, re, subprocess, sys, time

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SRC = os.path.join(ROOT, "source_documents", "Building I")
# Windows long-path prefix: several Building I file paths exceed 260 characters.
SRC_LP = (r"\\?" + "\\" + SRC) if os.name == "nt" else SRC
OUT = os.path.join(ROOT, "notes", "Building_I")
REV6 = os.path.join(SRC, "241115_RFSMC_Combined approved permit set_rev6.pdf")
REV14 = os.path.join(SRC, "GC Closeouts", "FMK Closeout", "CD Record Set",
                     "250925_RFSMC_Combined permit set_rev14_RecordSet.pdf")

SHEET = re.compile(r'^(G[01]\.\d{2}|A\d\.\d{2}[a-c]?|ID\d\.\d|S\d{3}|FP\d\.\d{2}|M\d\.\d{2}|P\d\.\d{2}|E\d\.\d{1,2})$')
REVROW = re.compile(r'\b(1[0-4]|[1-9])\s+(Interactive Review|County Permit Comments|RTAP Owner Changes|'
                    r'RTAP Interiors Changes|RTAP2 Comments|RTAP3 Comments|Owner Changes|Design Coordination|MEP Changes)\b')
NOISE = re.compile(r'(Craft\. Solutions\.|Solutions\.|lutions\.|utions\.|tions\.|\d{1,2}/\d{1,2}/20\d\d \d{1,2}:\d{2}:\d{2} [AP]M)')


def pdftotext(path, page, mode):
    return subprocess.run(["pdftotext", "-f", str(page), "-l", str(page), mode, path, "-"],
                          capture_output=True, text=True, errors="replace").stdout


def npages(path):
    info = subprocess.run(["pdfinfo", path], capture_output=True, text=True, errors="replace").stdout
    m = re.search(r'^Pages:\s+(\d+)', info, re.M)
    return int(m.group(1))


def file_inventory():
    rows = []
    for dp, dn, fn in os.walk(SRC_LP):
        for f in fn:
            p = os.path.join(dp, f)
            st = os.stat(p)
            rel = os.path.relpath(p, SRC_LP).replace("\\", "/")
            rows.append((time.strftime("%Y-%m-%d %H:%M", time.localtime(st.st_mtime)), st.st_size,
                         os.path.splitext(f)[1].lower().lstrip("."), rel))
    rows.sort(key=lambda r: r[3].lower())
    with open(os.path.join(OUT, "BI_file_inventory_v001.tsv"), "w", encoding="utf-8") as fh:
        fh.write("modified\tbytes\text\trelative_path (under source_documents/Building I)\n")
        for r in rows:
            fh.write("\t".join(map(str, r)) + "\n")
    print("files:", len(rows), "bytes:", sum(r[1] for r in rows))
    return rows


def sheet_index(path, out):
    n = npages(path)
    rows = []
    for p in range(1, n + 1):
        raw = [l.strip() for l in pdftotext(path, p, "-raw").splitlines() if l.strip()]
        lay = pdftotext(path, p, "-layout")
        num = ""
        lines = lay.splitlines()
        # 1) layout text: the big sheet number is printed on the lines right after the "SHEET NUMBER" label
        for i, l in enumerate(lines):
            j = l.find("SHEET NUMBER")
            if j < 0:
                continue
            for k in range(i + 1, min(i + 6, len(lines))):
                toks = [t for t in lines[k][max(0, j - 25):].split() if SHEET.match(t)]
                if toks:
                    num = toks[-1]; break
            if num:
                break
        # 2) fallback: last stand-alone sheet-number line in the raw text (title block is emitted last)
        if not num:
            m = [l for l in raw if SHEET.match(l)]
            num = m[-1] if m else ""
        name = ""
        for i, l in enumerate(lines):
            j = l.find("SHEET NAME")
            if j < 0:
                continue
            parts = []
            for k in range(i + 1, min(i + 8, len(lines))):
                if "SHEET NUMBER" in lines[k]:
                    break
                s = NOISE.sub("", lines[k][max(0, j - 25):]).strip()
                if s and not re.fullmatch(r'\d{4}', s):
                    parts.append(s)
            name = " ".join(parts); break
        revs = sorted({int(m.group(1)) for m in REVROW.finditer(lay)})
        rows.append((p, num, name, ",".join(map(str, revs))))
    with open(out, "w", encoding="utf-8") as fh:
        fh.write("page\tsheet\tsheet_name\trevisions_listed_in_title_block\n")
        for r in rows:
            fh.write("\t".join(map(str, r)) + "\n")
    print(os.path.basename(out), n, "pages")
    return rows


def comparison(r6, r14):
    d6 = {r[1]: r for r in r6 if r[1]}
    d14 = {r[1]: r for r in r14 if r[1]}
    sheets = sorted(set(d6) | set(d14), key=lambda s: (s[0], s))
    out = os.path.join(OUT, "BI_sheet_revision_comparison_v001.tsv")
    with open(out, "w", encoding="utf-8") as fh:
        fh.write("sheet\tsheet_name_rev14\trevs_rev6_set\trevs_rev14_set\tmax_rev_rev14\tchanged_after_rev6\tin_rev6\tin_rev14\n")
        for s in sheets:
            a = d6.get(s); b = d14.get(s)
            ra = a[3] if a else ""; rb = b[3] if b else ""
            mx = max([int(x) for x in rb.split(",") if x] or [0])
            changed = "yes" if (ra != rb or not a) else "no"
            fh.write("\t".join([s, (b or a)[2], ra, rb, str(mx), changed, "yes" if a else "no", "yes" if b else "no"]) + "\n")
    print(os.path.basename(out), len(sheets), "sheets")


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    file_inventory()
    r6 = sheet_index(REV6, os.path.join(OUT, "BI_sheet_index_rev6_v001.tsv"))
    r14 = sheet_index(REV14, os.path.join(OUT, "BI_sheet_index_rev14_v001.tsv"))
    comparison(r6, r14)
