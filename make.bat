@echo off
REM ================================================
REM   Gravity Engine - Build System
REM   by Nils DONTOT
REM   https://github.com/NilsDontot/GravityEngine
REM ================================================

title Gravity Engine - Build System
color 0A

:menu
cls
echo.
echo  ================================================
echo    Gravity Engine - Build System
echo    by Nils DONTOT
echo  ================================================
echo.
echo  [1] Build Development      (with console)
echo  [2] Build Release          (ready to distribute)
echo  [3] Clean                  (remove build files)
echo  [4] Clean + Build Release  (fresh release build)
echo  [5] Run                    (without building)
echo  [6] Test Executable        (run last built .exe)
echo  [7] Open dist folder       (view executables)
echo  [8] Help
echo  [0] Exit
echo.
echo  ================================================
echo.

set /p choice="  Select option [0-8]: "

if "%choice%"=="1" goto build_dev
if "%choice%"=="2" goto build_release
if "%choice%"=="3" goto clean
if "%choice%"=="4" goto clean_build
if "%choice%"=="5" goto run
if "%choice%"=="6" goto test_exe
if "%choice%"=="7" goto open_dist
if "%choice%"=="8" goto help
if "%choice%"=="0" goto exit
echo.
echo  [ERROR] Invalid option. Please choose 0-8.
timeout /t 2 >nul
goto menu

:build_dev
cls
echo.
echo  Building Development Version...
echo.
call build.bat
if errorlevel 1 (
    echo.
    echo  [ERROR] Development build failed!
    pause
) else (
    echo.
    echo  [SUCCESS] Development build complete!
    echo.
    set /p run_choice="  Run the executable now? (Y/N): "
    if /i "%run_choice%"=="Y" (
        if exist "dist\GravityEngine_Dev.exe" (
            start "" "dist\GravityEngine_Dev.exe"
        )
    )
)
pause
goto menu

:build_release
cls
echo.
echo  Building Release Version...
echo.
call build_release.bat
if errorlevel 1 (
    echo.
    echo  [ERROR] Release build failed!
    pause
) else (
    echo.
    echo  [SUCCESS] Release build complete!
    echo.
    set /p run_choice="  Run the executable now? (Y/N): "
    if /i "%run_choice%"=="Y" (
        if exist "dist\GravityEngine.exe" (
            start "" "dist\GravityEngine.exe"
        )
    )
)
pause
goto menu

:clean
cls
echo.
echo  Cleaning Build Files...
echo.
call clean.bat
pause
goto menu

:clean_build
cls
echo.
echo  Clean + Build Release...
echo.
call clean.bat
echo.
echo  ---
echo.
call build_release.bat
if errorlevel 1 (
    echo.
    echo  [ERROR] Build failed!
    pause
) else (
    echo.
    echo  [SUCCESS] Fresh release build complete!
    pause
)
goto menu

:run
cls
echo.
echo  Running from source (Python)...
echo.
echo  ================================================
echo.
python src/gravity_engine
echo.
echo  ================================================
echo.
echo  Program closed.
pause
goto menu

:test_exe
cls
echo.
echo  Testing Executable...
echo.

if exist "dist\GravityEngine.exe" (
    echo  [INFO] Running: dist\GravityEngine.exe
    echo.
    start "" "dist\GravityEngine.exe"
    timeout /t 2 >nul
) else if exist "dist\GravityEngine_Dev.exe" (
    echo  [INFO] Running: dist\GravityEngine_Dev.exe
    echo.
    start "" "dist\GravityEngine_Dev.exe"
    timeout /t 2 >nul
) else (
    echo  [ERROR] No executable found in dist/
    echo.
    echo  Please build first (option 1 or 2)
    pause
    goto menu
)
goto menu

:open_dist
cls
echo.
echo  Opening dist folder...
echo.
if exist "dist" (
    explorer dist
) else (
    echo  [ERROR] dist/ folder not found
    echo.
    echo  Please build first (option 1 or 2)
    pause
)
goto menu

:help
cls
echo.
echo  ================================================
echo    Gravity Engine - Build System Help
echo  ================================================
echo.
echo  [1] Build Development
echo      - Builds with console window visible
echo      - Good for debugging
echo      - Output: dist\GravityEngine_Dev.exe
echo.
echo  [2] Build Release
echo      - Builds without console window
echo      - Professional looking
echo      - Ready to distribute
echo      - Output: dist\GravityEngine.exe
echo.
echo  [3] Clean
echo      - Removes all build files
echo      - Removes __pycache__
echo      - Removes .spec files
echo.
echo  [4] Clean + Build Release
echo      - Does a clean first
echo      - Then builds release version
echo      - Ensures fresh build
echo.
echo  [5] Run
echo      - Runs the Python source directly
echo      - No building required
echo      - Good for quick testing
echo.
echo  [6] Test Executable
echo      - Runs the last built .exe
echo      - Tests if build works
echo.
echo  [7] Open dist folder
echo      - Opens Windows Explorer to dist/
echo      - View your built executables
echo.
echo  [8] Help
echo      - This screen
echo.
echo  [0] Exit
echo      - Closes the build system
echo.
echo  ================================================
echo.
pause
goto menu

:exit
cls
echo.
echo  ================================================
echo    Gravity Engine - Build System
echo  ================================================
echo.
echo  Thank you for using Gravity Engine!
echo  by Nils DONTOT
echo.
echo  GitHub: https://github.com/NilsDontot/GravityEngine
echo.
echo  ================================================
echo.
timeout /t 2 >nul
exit
```

---

## 📋 Fichiers créés

Voici ce que vous devez avoir à la racine de votre projet :
```
GravityEngine/
├── src/
│   └── gravity_engine.py
├── assets/
│   ├── font.ttf
│   └── icon.ico (optionnel)
├── build.bat          ✅ Nouveau
├── build_release.bat  ✅ Nouveau
├── clean.bat          ✅ Nouveau
├── make.bat           ✅ Nouveau
├── README.md
├── ROADMAP.md
├── LICENSE
├── .gitignore
└── .gitattributes
