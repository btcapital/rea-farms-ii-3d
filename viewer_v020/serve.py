"""Tiny local web server for the Building II review viewer (v020).

Serves ONLY this "viewer" folder, ONLY to this computer (127.0.0.1). Nothing is published to the internet.
Started by start_viewer.bat; stop it by closing the black window.
"""
import functools
import http.server
import os
import sys

PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 8020
HERE = os.path.dirname(os.path.abspath(__file__))


class Handler(http.server.SimpleHTTPRequestHandler):
    # explicit types: some Windows installations report .js as text/plain, which browsers refuse for modules
    extensions_map = {**http.server.SimpleHTTPRequestHandler.extensions_map, ".js": "text/javascript", ".mjs": "text/javascript",
                      ".json": "application/json", ".glb": "model/gltf-binary", ".css": "text/css", ".html": "text/html", ".png": "image/png"}

    def end_headers(self):
        self.send_header("Cache-Control", "no-store")
        super().end_headers()


if __name__ == "__main__":
    handler = functools.partial(Handler, directory=HERE)
    with http.server.ThreadingHTTPServer(("127.0.0.1", PORT), handler) as httpd:
        print(f"Building II viewer running at http://127.0.0.1:{PORT}/   (close this window to stop)")
        httpd.serve_forever()
