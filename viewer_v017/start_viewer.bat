@echo off
rem Rea Farms II - Building II review viewer (v016). Double-click this file to open the viewer.
rem It starts a small web server that only this computer can reach, then opens your web browser.
cd /d "%~dp0"
title Building II viewer - keep this window open while you use the viewer
echo.
echo   Building II review viewer
echo   -------------------------
echo   Your browser will open in a moment at  http://127.0.0.1:8017/
echo   Keep this window open while you use the viewer. Close it when you are done.
echo.
start "" /min cmd /c "ping -n 3 127.0.0.1 >nul & start http://127.0.0.1:8017/"
python -c "import http.server" >nul 2>nul
if %errorlevel%==0 (
  python serve.py 8017
) else (
  node serve.js 8017
)
echo.
echo   The viewer server has stopped. If you saw an error above, tell Claude what it says.
pause
