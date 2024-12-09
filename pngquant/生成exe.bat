@echo on
set pname=png_quant
pyinstaller -F %pname%.py
copy .\dist\%pname%.exe .\%pname%.exe

del *.spec
rd  .\dist /s /q
rd  .\build /s /q