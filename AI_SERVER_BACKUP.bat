@echo off

set DATA=%date:~-4%%date:~3,2%%date:~0,2%
set DEST=E:\Backup\AI-Server\%DATA%

mkdir "%DEST%" 2>nul

xcopy "E:\AI-Server\server" "%DEST%\server" /E /I /Y
xcopy "E:\AI-Server\client" "%DEST%\client" /E /I /Y
xcopy "E:\AI-Server\manager" "%DEST%\manager" /E /I /Y
xcopy "E:\AI-Server\database" "%DEST%\database" /E /I /Y

echo Backup completato in:
echo %DEST%

pause
