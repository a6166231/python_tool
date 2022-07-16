pyinstaller -F checkSpine.py --icon=.\icon\icon.ico
copy .\dist\checkSpine.exe .\checkSp.exe
del *.spec

rd  .\dist /s /q
rd  .\build /s /q
