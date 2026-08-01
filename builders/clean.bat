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
REM   Gravity Engine - Clean Build Files
REM   by Nils DONTOT
REM   https://github.com/NilsDontot/GravityEngine
REM ================================================

echo.
echo ================================================
echo   Gravity Engine - Cleanup
echo ================================================
echo.

cd /d "%~dp0.."
set PROJECT_ROOT=%cd%

echo Cleaning build artifacts...
echo.

REM Remove PyInstaller folders
if exist build (
    echo [INFO] Removing build/
    rmdir /s /q build
    echo [OK] build/ removed
) else (
    echo [SKIP] build/ not found
)

REM Remove spec files
if exist *.spec (
    echo [INFO] Removing .spec files
    del /q *.spec
    echo [OK] .spec files removed
) else (
    echo [SKIP] No .spec files found
)

REM Remove Python cache
if exist __pycache__ (
    echo [INFO] Removing __pycache__/
    rmdir /s /q __pycache__
    echo [OK] __pycache__/ removed
)

if exist src\__pycache__ (
    echo [INFO] Removing src/__pycache__/
    rmdir /s /q src\__pycache__
    echo [OK] src/__pycache__/ removed
)

REM Remove .pyc files
for /r %%i in (*.pyc) do (
    echo [INFO] Removing %%i
    del /q "%%i"
)

echo.
echo ================================================
echo   [SUCCESS] Cleanup complete!
echo ================================================
echo.
echo All build files have been removed.
echo You can now do a fresh build.
echo.
pause
