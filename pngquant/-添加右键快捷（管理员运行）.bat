cd /d %~dp0
reg add "HKEY_CLASSES_ROOT\SystemFileAssociations\.png\shell\www" /v SubCommands /d "" /f
reg add "HKEY_CLASSES_ROOT\SystemFileAssociations\.png\shell\www\shell\png_quant\command" /d "%~dp0\png_quant.exe "^"%%1""^" /f

reg add "HKEY_LOCAL_MACHINE\SOFTWARE\Classes\Directory\background\shell\www" /v SubCommands /d "" /f
reg add "HKEY_LOCAL_MACHINE\SOFTWARE\Classes\Directory\background\shell\www\shell\png_quant\command" /d %~dp0\png_quant.exe /f

reg add "HKEY_LOCAL_MACHINE\SOFTWARE\Classes\Directory\shell\www" /v SubCommands /d "" /f
reg add "HKEY_LOCAL_MACHINE\SOFTWARE\Classes\Directory\shell\www\Shell\png_quant\command" /d "%~dp0\png_quant.exe "^"%%1""^" /f