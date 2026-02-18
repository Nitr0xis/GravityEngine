@echo off
REM ================================================
REM   Gravity Engine - Development Build
REM   by Nils DONTOT
REM   https://github.com/NilsDontot/GravityEngine
REM ================================================

echo.
echo ================================================
echo   Gravity Engine - Development Build
echo ================================================
echo.

cd /d "%~dp0.."
set PROJECT_ROOT=%cd%

REM Check if PyInstaller is installed
echo [1/4] Checking PyInstaller...
python -c "import PyInstaller" 2>nul
if errorlevel 1 (
    echo [INFO] PyInstaller not found. Installing...
    pip install pyinstaller
    if errorlevel 1 (
        echo [ERROR] Failed to install PyInstaller
        echo.
        pause
        exit /b 1
    )
    echo [OK] PyInstaller installed successfully
) else (
    echo [OK] PyInstaller is installed
)

echo.
echo [2/4] Cleaning previous build...
if exist build rmdir /s /q build
if exist *.spec del /q *.spec
if exist dist/GravityEngine_Dev.exe del /q dist/GravityEngine_Dev.exe

echo.
echo [3/4] Building development executable...
echo       (This may take 1-2 minutes)
echo.

pyinstaller --clean ^
    --onefile ^
    --name "GravityEngine_Dev" ^
    --add-data "assets;assets" ^
    src/gravity_engine.py

if errorlevel 1 (
    echo.
    echo ================================================
    echo   [ERROR] Build failed!
    echo ================================================
    echo.
    echo Please check the error messages above.
    echo.
    pause
    exit /b 1
)

echo.
echo [4/4] Build complete!
echo.
echo ================================================
echo   [SUCCESS] Development build completed!
echo ================================================
echo.
echo Location: dist\GravityEngine_Dev.exe
echo.
echo This version includes a console window for debugging.
echo.
pause
