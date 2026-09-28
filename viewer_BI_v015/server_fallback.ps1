# Last-resort static server for viewer_BI_v015 (Windows PowerShell 5.1, no installation). Used by start_viewer.bat only when
# neither Python nor Node.js is available.  Serves this folder on http://127.0.0.1:<Port>/ (local only).
param([int]$Port = 8115)
$here = Split-Path -Parent $MyInvocation.MyCommand.Path
$mime = @{ ".js"="text/javascript"; ".json"="application/json"; ".glb"="model/gltf-binary"; ".css"="text/css"; ".html"="text/html"; ".png"="image/png"; ".jpg"="image/jpeg"; ".svg"="image/svg+xml"; ".txt"="text/plain"; ".md"="text/plain" }
$listener = $null
for ($p = $Port; $p -le $Port + 10; $p++) {
  try { $listener = New-Object System.Net.HttpListener; $listener.Prefixes.Add("http://127.0.0.1:$p/"); $listener.Start(); $Port = $p; break } catch { $listener = $null }
}
if ($null -eq $listener) { Write-Host "no free port"; exit 1 }
$url = "http://127.0.0.1:$Port/"
Set-Content -Path (Join-Path $here "viewer_url.txt") -Value $url -Encoding ascii
Write-Host "Building I viewer v015 (PowerShell fallback) serving $here"; Write-Host "  open $url"; Write-Host "  (close this window to stop the viewer)"
Start-Process $url
while ($listener.IsListening) {
  $ctx = $listener.GetContext(); $req = $ctx.Request; $res = $ctx.Response
  $path = [uri]::UnescapeDataString($req.Url.AbsolutePath)
  if ($path.StartsWith("/__capture")) { $b = [Text.Encoding]::UTF8.GetBytes('{"capture":false}'); $res.ContentType = "application/json"; $res.OutputStream.Write($b, 0, $b.Length); $res.Close(); continue }
  if ($path.EndsWith("/")) { $path += "index.html" }
  $file = Join-Path $here ($path.TrimStart("/").Replace("/", "\"))
  if ((Test-Path $file -PathType Leaf) -and ($file.StartsWith($here))) {
    $bytes = [IO.File]::ReadAllBytes($file); $ext = [IO.Path]::GetExtension($file).ToLower()
    $res.ContentType = if ($mime.ContainsKey($ext)) { $mime[$ext] } else { "application/octet-stream" }
    $res.Headers.Add("Cache-Control", "no-store"); $res.ContentLength64 = $bytes.Length; $res.OutputStream.Write($bytes, 0, $bytes.Length)
  } else { $res.StatusCode = 404 }
  $res.Close()
}
