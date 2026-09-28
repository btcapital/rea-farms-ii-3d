"""Extract straight segments from a pdftocairo SVG with transforms applied.
Output TSV in PDF points (origin top-left, y down). Curve commands (C) are
reduced to their end point so long outline paths are not dropped."""
import re, sys


def parse_matrix(t):
    m = re.match(r'matrix\(([^)]+)\)', t)
    if not m:
        return (1, 0, 0, 1, 0, 0)
    return tuple(float(v) for v in re.split(r'[,\s]+', m.group(1).strip()))


def mul(A, B):  # A after B
    a, b, c, d, e, f = A
    g, h, i, j, k, l = B
    return (a * g + c * h, b * g + d * h, a * i + c * j, b * i + d * j, a * k + c * l + e, b * k + d * l + f)


def apply(M, x, y):
    a, b, c, d, e, f = M
    return (a * x + c * y + e, b * x + d * y + f)


TOK = re.compile(r'([MLCZ])|(-?\d*\.?\d+(?:e-?\d+)?)')


def run(path, out):
    s = open(path, encoding="utf-8", errors="replace").read()
    s = s[s.find("</defs>"):]
    tok = re.compile(r'<(g|/g|path|/path)\b([^>]*)>')
    stack = [(1, 0, 0, 1, 0, 0)]
    n = 0
    with open(out, "w") as fo:
        fo.write("x0\ty0\tx1\ty1\tsw\tcolor\n")
        for m in tok.finditer(s):
            tag, attrs = m.group(1), m.group(2)
            if tag == "g":
                t = re.search(r'transform="([^"]+)"', attrs)
                stack.append(mul(stack[-1], parse_matrix(t.group(1))) if t else stack[-1])
            elif tag == "/g":
                if len(stack) > 1:
                    stack.pop()
            elif tag == "path":
                if 'stroke="none"' in attrs or ('fill="rgb' in attrs and "stroke=" not in attrs):
                    continue
                t = re.search(r'transform="([^"]+)"', attrs)
                M = mul(stack[-1], parse_matrix(t.group(1))) if t else stack[-1]
                d = re.search(r' d="([^"]+)"', attrs)
                if not d:
                    continue
                sw = re.search(r'stroke-width="([\d.]+)"', attrs)
                sw = float(sw.group(1)) if sw else 0
                col = re.search(r'stroke="rgb\(([^)]+)\)"', attrs)
                col = col.group(1).split(",")[0].strip() if col else "?"
                cmds = []
                cur_cmd = None
                for c, v in TOK.findall(d.group(1)):
                    if c:
                        cur_cmd = [c]
                        cmds.append(cur_cmd)
                    elif cur_cmd is not None:
                        cur_cmd.append(float(v))
                cur = None
                start = None
                for cmd in cmds:
                    op, args = cmd[0], cmd[1:]
                    if op == "M" and len(args) >= 2:
                        cur = apply(M, args[0], args[1])
                        start = cur
                    elif op == "L" and len(args) >= 2 and cur:
                        p = apply(M, args[0], args[1])
                        fo.write(f"{cur[0]:.3f}\t{cur[1]:.3f}\t{p[0]:.3f}\t{p[1]:.3f}\t{sw:g}\t{col}\n")
                        n += 1
                        cur = p
                    elif op == "C" and len(args) >= 6 and cur:
                        p = apply(M, args[4], args[5])
                        fo.write(f"{cur[0]:.3f}\t{cur[1]:.3f}\t{p[0]:.3f}\t{p[1]:.3f}\t{sw:g}\t{col}\n")
                        n += 1
                        cur = p
                    elif op == "Z" and start and cur and cur != start:
                        fo.write(f"{cur[0]:.3f}\t{cur[1]:.3f}\t{start[0]:.3f}\t{start[1]:.3f}\t{sw:g}\t{col}\n")
                        n += 1
                        cur = start
    print(out, n, "segments")


if __name__ == "__main__":
    for p in sys.argv[1:]:
        run(p, p.replace(".svg", ".seg.tsv"))
