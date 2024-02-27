@echo on
set pname=quickTime
pyinstaller -F -p . %pname%.py
copy .\dist\%pname%.exe .\%pname%.exe

del *.spec
rd  .\dist /s /q
rd  .\build /s /q