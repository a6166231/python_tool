cd /d %~dp0
reg add "HKEY_CLASSES_ROOT\SystemFileAssociations\.py\shell\www" /v SubCommands /d "" /f
reg add "HKEY_CLASSES_ROOT\SystemFileAssociations\.py\shell\www\shell\py2exe\command" /d "%~dp0\py2exe.exe "^"%%1""^" /f