cd /d %~dp0
reg add "HKEY_CLASSES_ROOT\SystemFileAssociations\.csv\shell\www" /v SubCommands /d "" /f
reg add "HKEY_CLASSES_ROOT\SystemFileAssociations\.csv\shell\www\shell\excel2ts\command" /d "%~dp0\excel2ts.exe "^"%%1""^" /f

reg add "HKEY_CLASSES_ROOT\SystemFileAssociations\.xls\shell\www" /v SubCommands /d "" /f
reg add "HKEY_CLASSES_ROOT\SystemFileAssociations\.xls\shell\www\shell\excel2ts\command" /d "%~dp0\excel2ts.exe "^"%%1""^" /f

reg add "HKEY_CLASSES_ROOT\SystemFileAssociations\.xlsx\shell\www" /v SubCommands /d "" /f
reg add "HKEY_CLASSES_ROOT\SystemFileAssociations\.xlsx\shell\www\shell\excel2ts\command" /d "%~dp0\excel2ts.exe "^"%%1""^" /f
