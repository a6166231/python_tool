@echo on
set pname=quickTime

pyinstaller --clean -F -p . %pname%.py --icon=.\icon\icon.ico -w --upx-dir F:\tool\upx-4.2.2-win32
copy .\dist\%pname%.exe .\%pname%.exe

del *.spec
rd  .\dist /s /q
rd  .\build /s /q