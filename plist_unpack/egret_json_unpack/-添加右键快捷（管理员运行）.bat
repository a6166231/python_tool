cd /d %~dp0
reg add "HKEY_CLASSES_ROOT\SystemFileAssociations\.png\shell\www" /v SubCommands /d "" /f
reg add "HKEY_CLASSES_ROOT\SystemFileAssociations\.png\shell\www\shell\unpack\command" /d "%~dp0\unpack.exe "^"%%1""^" /f

reg add "HKEY_CLASSES_ROOT\SystemFileAssociations\.json\shell\www" /v SubCommands /d "" /f
reg add "HKEY_CLASSES_ROOT\SystemFileAssociations\.json\shell\www\shell\unpack\command" /d "%~dp0\unpack.exe "^"%%1""^" /f

reg add "HKEY_LOCAL_MACHINE\SOFTWARE\Classes\Directory\background\shell\www" /v SubCommands /d "" /f
reg add "HKEY_LOCAL_MACHINE\SOFTWARE\Classes\Directory\background\shell\www\shell\unpack\command" /d %~dp0\unpack.exe /f

reg add "HKEY_LOCAL_MACHINE\SOFTWARE\Classes\Directory\shell\www" /v SubCommands /d "" /f
reg add "HKEY_LOCAL_MACHINE\SOFTWARE\Classes\Directory\shell\www\Shell\unpack\command" /d "%~dp0\unpack.exe "^"%%1""^" /f