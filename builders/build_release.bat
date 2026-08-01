:: GravityEngine — N-body gravitational simulator
:: Copyright (C) 2026 Nils DONTOT
:: Contact: nils.dontot.pro@gmail.com
::
:: This program is free software: you can redistribute it and/or modify
:: it under the terms of the GNU General Public License as published by
:: the Free Software Foundation, either version 3 of the License, or
:: (at your option) any later version.
::
:: This program is distributed in the hope that it will be useful,
:: but WITHOUT ANY WARRANTY; without even the implied warranty of
:: MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
:: GNU General Public License for more details.
::
:: You should have received a copy of the GNU General Public License
:: along with this program. If not, see <https://www.gnu.org/licenses/>.

@echo off
REM ================================================
REM   Gravity Engine - Release Build
REM   by Nils DONTOT
REM   https://github.com/NilsDontot/GravityEngine
REM ================================================

echo.
echo ================================================
echo   Gravity Engine - Release Build
echo ================================================
echo.

cd /d "%~dp0.."
set PROJECT_ROOT=%cd%

REM Check if PyInstaller is installed
echo [1/5] Checking PyInstaller...
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
echo [2/5] Cleaning previous build...
if exist build rmdir /s /q build
if exist *.spec del /q *.spec
if exist dist/GravityEngine.exe del /q dist/GravityEngine.exe

echo.
echo [3/5] Checking for icon file...
if exist "assets\icon.ico" (
    echo [OK] Icon file found
    set ICON_PARAM=--icon "assets\icon.ico"
) else (
    echo [WARNING] No icon file found (assets\icon.ico)
    echo [INFO] Building without custom icon
    set ICON_PARAM=
)

echo.
echo [4/5] Building release executable...
echo       (This may take 2-3 minutes)
echo.

pyinstaller --clean ^
    --onefile ^
    --noconsole ^
    --name "GravityEngine" ^
    %ICON_PARAM% ^
    --add-data "assets;assets" ^
    src/run.py

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
echo [5/5] Calculating file size...
for %%I in ("dist\GravityEngine.exe") do set SIZE=%%~zI
set /a SIZE_MB=%SIZE% / 1048576

echo.
echo ================================================
echo   [SUCCESS] Release build completed!
echo ================================================
echo.
echo Location: dist\GravityEngine.exe
echo Size:     %SIZE_MB% MB (approx.)
echo.
echo This version has NO console window.
echo Ready for distribution!
echo.
echo Note: You can distribute this single .exe file.
echo       Users don't need Python installed.
echo.
pause
