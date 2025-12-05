@echo off
setlocal ENABLEDELAYEDEXPANSION
color 0A

echo ==========================================
echo   CasaSquire Bot - Установка
echo ==========================================
echo.

REM 1. Проверяем наличие Python
where python >nul 2>&1
if errorlevel 1 (
    echo.
    echo [ERROR] Python не найден.
    echo.
    echo Чтобы установить Python правильно, сделайте следующее:
    echo 1. Откройте страницу загрузки: https://www.python.org/downloads/windows/
    echo 2. Скачайте Python 3.11 или выше.
    echo 3. ВНИМАНИЕ: на первом экране установщика поставьте галочку:
    echo.
    echo ---------------------------------------------------------
    echo ^|  Python 3.X Setup                                     ^|
    echo ^|                                                       ^|
    echo ^|  [ ] Install launcher for all users (recommended)     ^|
    echo ^|  [✔] Add python.exe to PATH   ^<--- ОБЯЗАТЕЛЬНО        ^|
    echo ^|                                                       ^|
    echo ^|       * без этой галочки бот не запустится *          ^|
    echo ^|                                                       ^|
    echo ^|            [ Install Now ]                            ^|
    echo ---------------------------------------------------------
    echo.
    echo Можно открыть страницу загрузки Python автоматически.
    echo.
    choice /M "Открыть https://www.python.org/downloads/windows/ в браузере?"
    if errorlevel 1 start https://www.python.org/downloads/windows/
    echo.
    echo После установки закройте это окно и снова запустите install.bat.
    echo.
    pause
    exit /b 1
)

echo [INFO] Python найден, проверяю версию...

REM 1.1 Проверяем, что Python >= 3.11
for /f %%i in ('python -c "import sys; print(sys.version_info[:2] >= (3, 11))"') do set PY_OK=%%i

if /I not "!PY_OK!"=="True" (
    echo.
    echo [ERROR] Обнаружен Python версии ниже 3.11.
    echo Пожалуйста, установите Python 3.11 или выше.
    echo.
    pause
    exit /b 1
)

echo [OK] Подходит версия Python 3.11+.
echo.

REM 2. Создаем venv (если уже есть — пропускаем)
if not exist venv (
    echo [INFO] Создаю виртуальное окружение...
    python -m venv venv
) else (
    echo [INFO] Виртуальное окружение уже существует, пропускаю создание.
)

REM 3. Ставим зависимости
echo.
echo [INFO] Активирую виртуальное окружение...
call venv\Scripts\activate

echo [INFO] Устанавливаю зависимости...
pip install --upgrade pip
pip install -r requirements.txt

REM 4. Спрашиваем у пользователя BOT_TOKEN и OWNER_ID и создаём .env

:ASK_TOKEN
echo.
echo Для работы бота нужен токен, который выдаёт @BotFather.
echo Сейчас откроется окно Telegram с ботом BotFather.
echo В Telegram отправьте команду /newbot или выберите уже созданного бота.
echo.
start https://t.me/BotFather
echo.
set /p BOT_TOKEN=Введите BOT_TOKEN (скопируйте из BotFather и вставьте сюда): 
if "%BOT_TOKEN%"=="" (
    echo [ERROR] BOT_TOKEN не может быть пустым. Попробуйте ещё раз.
    goto ASK_TOKEN
)
echo.

:ASK_OWNER
echo.
echo Чтобы получить ваш Telegram ID (OWNER_ID), сейчас откроется бот userinfobot.
echo Отправьте ему любое сообщение, он вернёт ваш числовой ID.
start https://t.me/userinfobot
echo.
set /p OWNER_ID=Введите ваш OWNER_ID (только цифры): 
if "%OWNER_ID%"=="" (
    echo [ERROR] OWNER_ID не может быть пустым. Попробуйте ещё раз.
    goto ASK_OWNER
)
REM Простая проверка, что там хотя бы не пустая строка и не буквы
for /f "delims=0123456789" %%A in ("%OWNER_ID%") do (
    if not "%%A"=="" (
        echo [ERROR] OWNER_ID должен быть числом. Попробуйте ещё раз.
        goto ASK_OWNER
    )
)

REM 5. Пишем .env (перезаписываем файл)
echo.
> .env echo BOT_TOKEN=!BOT_TOKEN!
>> .env echo OWNER_ID=!OWNER_ID!

REM 6. Настраиваем автозапуск через Планировщик задач
echo.
echo [INFO] Настраиваю автозапуск бота через Планировщик задач...

REM Путь к скрипту run.bat
set "RUN_PATH=%~dp0run.bat"

REM Имя задачи в Windows
set "TASK_NAME=CasaSquireBot"

REM Проверяем, есть ли уже такая задача
schtasks /Query /TN "%TASK_NAME%" >nul 2>&1
if %ERRORLEVEL%==0 (
    echo [INFO] Задача "%TASK_NAME%" уже существует — удаляю старую...
    schtasks /Delete /TN "%TASK_NAME%" /F >nul
)

REM Создаем новую задачу (БЕЗ RL HIGHEST => без админ-права)
schtasks /Create ^
    /SC ONLOGON ^
    /TN "%TASK_NAME%" ^
    /TR "\"%RUN_PATH%\"" ^
    /F

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo [ERROR] Не удалось создать задачу автозапуска.
    echo Можно будет запустить бота вручную через run.bat.
    echo.
    pause
    exit /b 1
)

echo.
echo [OK] Автозапуск бота настроен успешно.
echo При следующем входе в систему бот запустится автоматически.
echo.

echo [INFO] Установка завершена. Можно запускать бота командой:
echo   run.bat
echo.
pause
