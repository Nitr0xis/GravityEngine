@echo off
python -m PyInstaller --onefile --noconsole ^
--icon="C:\Users\donto\Documents\Projects\Programming\GravityEngine\icon.ico" ^
--distpath "C:\Users\donto\Documents\Projects\Programming\GravityEngine" ^
"C:\Users\donto\Documents\Projects\Programming\GravityEngine\gravity_engine.py"

pause
