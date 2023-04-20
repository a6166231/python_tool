@echo on
set pname=py2exe
pyinstaller -F %pname%.py
copy .\dist\%pname%.exe .\%pname%.exe

del *.spec
rd  .\dist /s /q
rd  .\build /s /q