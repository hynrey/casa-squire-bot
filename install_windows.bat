@echo off
setlocal ENABLEDELAYEDEXPANSION
color 0A

REM Force working directory to the folder of this script
cd /d "%~dp0"

REM --- Check for administrator rights ---
net session >nul 2>&1
if %errorlevel% NEQ 0 (
    echo [ERROR] This installer must be run as Administrator.
    echo.
    echo Right-click on install_windows.bat and choose:
    echo   "Run as administrator"
    echo.
    pause
    goto END
)

echo ==========================================
echo   CasaSquire Bot - Setup
echo ==========================================
echo.

REM 1. Check if Python exists
where python >nul 2>&1
if errorlevel 1 (
    echo.
    echo [ERROR] Python was not found in PATH.
    echo Please install Python 3.11 or higher from:
    echo   https://www.python.org/downloads/windows/
    echo.
    echo After installation, close this window and run install_windows.bat again.
    echo.
    pause
    goto END
)

echo [INFO] Python found, checking version...

REM 1.1 Check that Python >= 3.11
for /f %%i in ('python -c "import sys; print(sys.version_info[:2] >= (3, 11))"') do set PY_OK=%%i

if /I not "!PY_OK!"=="True" (
    echo.
    echo [ERROR] Python version is lower than 3.11.
    echo Please install Python 3.11 or higher.
    echo.
    pause
    goto END
)

echo [OK] Python version is 3.11+.
echo.

REM 2. Create venv (if not exists)
if not exist venv (
    echo [INFO] Creating virtual environment...
    python -m venv venv
    if errorlevel 1 (
        echo.
        echo [ERROR] Failed to create virtual environment.
        echo Make sure you have permissions and try again.
        echo.
        pause
        goto END
    )
) else (
    echo [INFO] Virtual environment already exists, skipping creation.
)

REM 3. Install dependencies
echo.
echo [INFO] Activating virtual environment...
call venv\Scripts\activate
if errorlevel 1 (
    echo.
    echo [ERROR] Failed to activate virtual environment.
    echo Check that folder "venv\Scripts" exists.
    echo.
    pause
    goto END
)

echo [INFO] Checking requirements.txt...
if not exist requirements.txt (
    echo.
    echo [ERROR] requirements.txt not found in current folder.
    echo Put install_windows.bat and requirements.txt in the same directory.
    echo.
    pause
    goto END
)

echo [INFO] Upgrading pip inside venv...
python -m pip install --upgrade pip
if errorlevel 1 (
    echo.
    echo [ERROR] Failed to upgrade pip.
    echo You can try to run:
    echo   venv\Scripts\python.exe -m pip install --upgrade pip
    echo manually.
    echo.
    pause
    goto END
)

echo [INFO] Installing dependencies from requirements.txt...
python -m pip install -r requirements.txt
if errorlevel 1 (
    echo.
    echo [ERROR] Failed to install dependencies from requirements.txt.
    echo Check the file and your internet connection.
    echo.
    pause
    goto END
)

REM 4. Ask for BOT_TOKEN and OWNER_ID, create .env

:ASK_TOKEN
echo.
echo Bot needs a token from @BotFather.
echo Telegram with BotFather will be opened now.
echo Create a new bot or use an existing one and copy its token.
echo.
start https://t.me/BotFather
echo.
set /p BOT_TOKEN=Enter BOT_TOKEN (paste from BotFather):
if "%BOT_TOKEN%"=="" (
    echo [ERROR] BOT_TOKEN cannot be empty. Try again.
    goto ASK_TOKEN
)
echo.

:ASK_OWNER
echo.
echo To get your Telegram ID (OWNER_ID), Telegram bot @userinfobot will be opened now.
echo Send any message to it and copy your numeric ID.
start https://t.me/userinfobot
echo.
set /p OWNER_ID=Enter your OWNER_ID (numbers only):
if "%OWNER_ID%"=="" (
    echo [ERROR] OWNER_ID cannot be empty. Try again.
    goto ASK_OWNER
)
REM Check that OWNER_ID contains only digits
for /f "delims=0123456789" %%A in ("%OWNER_ID%") do (
    if not "%%A"=="" (
        echo [ERROR] OWNER_ID must be a number. Try again.
        goto ASK_OWNER
    )
)

REM 5. Write .env (overwrite)
echo.
> .env echo BOT_TOKEN=!BOT_TOKEN!
>> .env echo OWNER_IDS=!OWNER_ID!

REM 6. Create autorun task in Task Scheduler
echo.
echo [INFO] Configuring bot autorun via Task Scheduler...

REM Path to run.bat
set "RUN_PATH=%~dp0run_windows.bat"

REM Task name
set "TASK_NAME=CasaSquireBot"

REM Remove old task if exists
schtasks /Query /TN "%TASK_NAME%" >nul 2>&1
if %ERRORLEVEL%==0 (
    echo [INFO] Task "%TASK_NAME%" already exists, deleting old one...
    schtasks /Delete /TN "%TASK_NAME%" /F >nul
)

REM Create new task
@REM schtasks /Create /SC ONLOGON /TN "%TASK_NAME%" /TR "\"%RUN_PATH%\"" /F >nul 2>&1
schtasks /Create /SC ONLOGON /TN "%TASK_NAME%" /TR "\"%RUN_PATH%\"" /RL LIMITED /F >nul 2>&1

if errorlevel 1 (
    echo [WARN] Failed to create autorun task.
    echo You can:
    echo   - run install_windows.bat as Administrator to enable autorun, or
    echo   - run the bot manually using run.bat.
) else (
    echo [OK] Autorun has been configured successfully.
    echo [INFO] Starting bot via Task Scheduler...
    schtasks /Run /TN "%TASK_NAME%"
)

:END
exit
