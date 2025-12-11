@echo off
cd /d %~dp0

if not exist bot.pid (
    echo Bot is not running.
    pause
    exit /b
)

set /p PID=<bot.pid

echo Stopping bot (PID=%PID%)...

taskkill /PID %PID% /T /F

echo Bot stopped.
pause
