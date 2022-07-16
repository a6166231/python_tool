cd /d %~dp0
reg add "HKEY_LOCAL_MACHINE\SOFTWARE\Classes\Directory\background\shell\www" /v SubCommands /d "" /f
reg add "HKEY_LOCAL_MACHINE\SOFTWARE\Classes\Directory\background\shell\www\shell\checkSpine\command" /d %~dp0\checkSp.exe /f