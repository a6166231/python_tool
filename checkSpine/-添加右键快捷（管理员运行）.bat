cd /d %~dp0
reg add "HKEY_LOCAL_MACHINE\SOFTWARE\Classes\Directory\background\shell\www" /v SubCommands /d "" /f
reg add "HKEY_LOCAL_MACHINE\SOFTWARE\Classes\Directory\background\shell\www\shell\checkSpine\command" /d %~dp0\checkSp.exe /f

reg add "HKEY_CLASSES_ROOT\SystemFileAssociations\.json\shell\www" /v SubCommands /d "" /f
reg add "HKEY_CLASSES_ROOT\SystemFileAssociations\.json\shell\www\shell\previewCurve\command" /d "%~dp0\previewCurve.exe "^"%%1""^" /f
reg add "HKEY_CLASSES_ROOT\SystemFileAssociations\.json\shell\www\shell\checkSpine\command" /d "%~dp0\checkSp.exe "^"%%1""^" /f