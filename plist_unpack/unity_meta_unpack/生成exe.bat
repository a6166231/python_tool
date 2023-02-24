pyinstaller -F .\unpack.py
copy .\dist\unpack.exe .\unpack.exe
del *.spec

rd  .\dist /s /q
rd  .\build /s /q
