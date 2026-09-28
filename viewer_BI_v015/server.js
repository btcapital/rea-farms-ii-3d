// Fallback static server for viewer_BI_v015 when Python is not installed (Node.js, no dependencies).
//   node server.js [port]
const http = require("http"), fs = require("fs"), path = require("path"), { exec } = require("child_process");
const HERE = __dirname;
const MIME = { ".js": "text/javascript", ".json": "application/json", ".glb": "model/gltf-binary", ".css": "text/css", ".html": "text/html",
  ".png": "image/png", ".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".svg": "image/svg+xml", ".txt": "text/plain", ".md": "text/plain" };
function serve(port) {
  const srv = http.createServer((req, res) => {
    let p = decodeURIComponent(req.url.split("?")[0]);
    if (p.startsWith("/__capture")) { res.writeHead(200, { "Content-Type": "application/json" }); res.end('{"capture":false}'); return; }
    if (p.endsWith("/")) p += "index.html";
    const file = path.normalize(path.join(HERE, p));
    if (!file.startsWith(HERE) || !fs.existsSync(file) || fs.statSync(file).isDirectory()) { res.writeHead(404); res.end("not found"); return; }
    res.writeHead(200, { "Content-Type": MIME[path.extname(file).toLowerCase()] || "application/octet-stream", "Cache-Control": "no-store" });
    fs.createReadStream(file).pipe(res);
  });
  srv.on("error", (e) => { if (e.code === "EADDRINUSE" && port < 8125) serve(port + 1); else { console.error(e); process.exit(1); } });
  srv.listen(port, "127.0.0.1", () => {
    const url = `http://127.0.0.1:${port}/`;
    fs.writeFileSync(path.join(HERE, "viewer_url.txt"), url + "\n");
    console.log(`Building I viewer v015 (node fallback) serving ${HERE}\n  open ${url}\n  (close this window to stop the viewer)`);
    exec(`start "" "${url}"`);
  });
}
serve(parseInt(process.argv[2] || "8115", 10));
