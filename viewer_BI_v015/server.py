"""Local static server for viewer_BI_v015 (no dependencies beyond the Python standard library).

  python server.py [--port 8115] [--no-browser] [--capture <dir>]

Serves this folder on 127.0.0.1 only (never on the network).  If the port is busy the next free one up to +10 is used
and the chosen URL is printed and written to viewer_url.txt.  --capture <dir> enables a POST /__capture endpoint that the
viewer's Save View Image button also uses to write validation PNGs into <dir> (disabled by default).
"""
import argparse, base64, http.server, json, os, socket, socketserver, sys, threading, webbrowser

HERE = os.path.dirname(os.path.abspath(__file__))
ap = argparse.ArgumentParser()
ap.add_argument("--port", type=int, default=8115)
ap.add_argument("--no-browser", action="store_true")
ap.add_argument("--capture", default=None)
args = ap.parse_args()

MIME = {".js": "text/javascript", ".mjs": "text/javascript", ".json": "application/json", ".glb": "model/gltf-binary", ".gltf": "model/gltf+json",
        ".css": "text/css", ".html": "text/html", ".png": "image/png", ".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".svg": "image/svg+xml", ".txt": "text/plain", ".md": "text/plain"}

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *a, **kw):
        super().__init__(*a, directory=HERE, **kw)
    def guess_type(self, path):
        ext = os.path.splitext(path)[1].lower()
        return MIME.get(ext, super().guess_type(path))
    def end_headers(self):
        self.send_header("Cache-Control", "no-store")
        super().end_headers()
    def log_message(self, fmt, *a):
        sys.stdout.write("%s - %s\n" % (self.address_string(), fmt % a)); sys.stdout.flush()
    def do_GET(self):
        if self.path.startswith("/__capture/ping"):
            body = json.dumps({"capture": bool(args.capture)}).encode()
            self.send_response(200); self.send_header("Content-Type", "application/json"); self.send_header("Content-Length", str(len(body))); self.end_headers(); self.wfile.write(body); return
        return super().do_GET()
    def do_POST(self):
        if self.path.startswith("/__capture") and args.capture:
            n = int(self.headers.get("Content-Length", "0"))
            payload = json.loads(self.rfile.read(n).decode("utf-8"))
            name = os.path.basename(payload.get("name", "capture.png"))
            data = payload["dataURL"].split(",", 1)[1]
            os.makedirs(args.capture, exist_ok=True)
            out = os.path.join(args.capture, name)
            with open(out, "wb") as f:
                f.write(base64.b64decode(data))
            body = json.dumps({"saved": out}).encode()
            self.send_response(200); self.send_header("Content-Type", "application/json"); self.send_header("Content-Length", str(len(body))); self.end_headers(); self.wfile.write(body); return
        self.send_response(404); self.end_headers()

class Server(socketserver.ThreadingTCPServer):
    allow_reuse_address = False      # Windows: SO_REUSEADDR would let a second copy bind the same port; keep it off so the port fallback works
    daemon_threads = True

port = args.port
srv = None
for p in range(port, port + 11):
    try:
        srv = Server(("127.0.0.1", p), Handler); port = p; break
    except OSError:
        continue
if srv is None:
    raise SystemExit(f"no free port between {args.port} and {args.port + 10}")
url = f"http://127.0.0.1:{port}/"
with open(os.path.join(HERE, "viewer_url.txt"), "w") as f:
    f.write(url + "\n")
print(f"Building I viewer v015 serving {HERE}\n  open {url}\n  (close this window to stop the viewer)"); sys.stdout.flush()
if not args.no_browser:
    threading.Timer(0.8, lambda: webbrowser.open(url)).start()
try:
    srv.serve_forever()
except KeyboardInterrupt:
    pass
