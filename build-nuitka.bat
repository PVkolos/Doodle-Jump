nuitka ^
  --onefile ^
  --windows-console-mode=disable ^
  --follow-imports ^
  --include-data-dir=doodle_jump/data=data ^
  --product-version="1.0.2.0" ^
  --file-version="1.0.2.0" ^
  --company-name="brandonzorn" ^
  --product-name="Doodle-Jump" ^
  --windows-icon-from-ico="dj.ico" ^
  -o "Doodle-Jump" ^
  --output-dir=build_nuitka/ ^
  doodle_jump/main.py
