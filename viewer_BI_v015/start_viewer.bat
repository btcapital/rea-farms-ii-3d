@echo off
rem Building I viewer v015 - double-click to start. Serves this folder on http://127.0.0.1:8115/ (local only) and opens the browser.
rem Nothing is installed and nothing leaves this computer. Close this window to stop the viewer.
setlocal
cd /d "%~dp0"
title Building I viewer v015
echo Building I - Rea Farms Sports Medicine Center - viewer v015 (model v014)
echo.
where py >nul 2>nul
if %errorlevel%==0 ( py -3 server.py --port 8115 & goto :end )
where python >nul 2>nul
if %errorlevel%==0 ( python server.py --port 8115 & goto :end )
where node >nul 2>nul
if %errorlevel%==0 ( node server.js 8115 & goto :end )
echo Neither Python nor Node.js was found. Trying the PowerShell fallback server...
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0server_fallback.ps1" -Port 8115
:end
echo.
echo Viewer stopped. Press any key to close.
pause >nul
