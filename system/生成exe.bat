pyinstaller -F restart.py -w
copy .\dist\*.exe .
del *.spec

rd  .\dist /s /q
rd  .\build /s /q
