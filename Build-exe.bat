@echo off
REM Rebuilds dist\Rough Cut.exe from RoughCut.py
cd /d "%~dp0"
REM python-mpv is bundled so the in-app "Enable playback" button can load a
REM downloaded libmpv. libmpv itself is NOT bundled (fetched on demand).
python -m PyInstaller --noconfirm --onefile --windowed ^
  --name "Rough Cut" ^
  --collect-all tkinterdnd2 ^
  --hidden-import mpv ^
  RoughCut.py
echo.
echo Done. The exe is in the "dist" folder.
pause