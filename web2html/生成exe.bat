pyinstaller -F generate_single_html.py
copy .\dist\generate_single_html.exe .\generate_single_html.exe
del *.spec

rd  .\dist /s /q
rd  .\build /s /q
