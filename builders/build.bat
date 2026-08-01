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
