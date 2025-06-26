@echo off
setlocal EnableDelayedExpansion

:: 1) Define logfile & key vars
set "LOGFILE=%~dp0setup_log.txt"
set "CHOCO_DIR=%ProgramData%\chocolatey"
set "CHOCO_BIN=%CHOCO_DIR%\bin\choco.exe"
set "SYSTEMROOT=%SystemRoot%"

:: 2) Check for Admin rights
NET SESSION >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo [%date% %time%] Not elevated – requesting Admin rights...>>"%LOGFILE%"
    goto UACPrompt
) else (
    echo [%date% %time%] Already elevated.>>"%LOGFILE%"
    goto gotAdmin
)

:UACPrompt
set "batchPath=%~f0"
set "batchArgs=%*"
echo Set UAC = CreateObject^("Shell.Application"^) > "%temp%\getadmin.vbs"
echo UAC.ShellExecute "%batchPath%", "%batchArgs%", "", "runas", 1 >> "%temp%\getadmin.vbs"
"%temp%\getadmin.vbs"
exit /b

:gotAdmin
cd /d "%~dp0"
echo [%date% %time%] Relaunched as Admin, working folder now %~dp0>>"%LOGFILE%"

:: 3) Ensure critical system paths are available
set "PATH=%SYSTEMROOT%\System32;%SYSTEMROOT%;%SYSTEMROOT%\System32\Wbem;%SYSTEMROOT%\System32\WindowsPowerShell\v1.0\"

:: 4) Main logic
call :main >>"%LOGFILE%" 2>&1
exit /b

:main
echo =====================================================
echo [%date% %time%] Starting Chocolatey install/repair...
echo =====================================================

:: 1) Check if choco exists
where choco >nul 2>&1
if not ERRORLEVEL 1 (
    echo [%date% %time%] Chocolatey already on PATH – skipping install.
    goto :post_install
)

:: 2) Clean broken or existing installs
if exist "%CHOCO_DIR%" (
    echo [%date% %time%] Found existing Chocolatey installation - removing...
    :: Take ownership first
    takeown /F "%CHOCO_DIR%" /R /A /D Y >nul 2>&1
    icacls "%CHOCO_DIR%" /grant Administrators:F /T /C >nul 2>&1
    :: Remove directory
    rmdir /s /q "%CHOCO_DIR%"
    if exist "%CHOCO_DIR%" (
        echo [%date% %time%] ERROR: Failed to remove existing Chocolatey installation! >&2
        exit /b 1
    )
    echo [%date% %time%] Successfully removed existing installation
)

:: 3) Install Chocolatey with full PowerShell path
echo [%date% %time%] Installing Chocolatey...
"%SYSTEMROOT%\System32\WindowsPowerShell\v1.0\powershell.exe" -NoProfile -ExecutionPolicy Bypass -Command "Set-ExecutionPolicy Bypass -Scope Process -Force; [Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))"
if ERRORLEVEL 1 (
    echo [%date% %time%] ERROR: choco install failed! >&2
    exit /b 1
)

:: 4) Verify installation and update current session
where choco >nul 2>&1
if ERRORLEVEL 1 (
    echo [%date% %time%] WARNING: choco not in PATH - attempting to add manually...
    set "PATH=%PATH%;%CHOCO_DIR%\bin"
    where choco >nul 2>&1
    if ERRORLEVEL 1 (
        echo [%date% %time%] ERROR: choco still not found after install! >&2
        exit /b 1
    )
)

:post_install
echo [%date% %time%] Chocolatey is installed or already present.

:: 5) Set environment variables
echo [%date% %time%] Writing SYSTEM environment variables…
setx /M ChocolateyInstall "%CHOCO_DIR%" >>"%LOGFILE%" 2>&1

:: 6) Update system PATH
for /f "skip=2 tokens=2,*" %%A in (
  'reg query "HKLM\SYSTEM\CurrentControlSet\Control\Session Manager\Environment" /v Path'
) do set "sysPath=%%B"

echo !sysPath! | find /I "%CHOCO_DIR%\bin" >nul
if ERRORLEVEL 1 (
    echo [%date% %time%] Appending Chocolatey to SYSTEM PATH…
    setx /M Path "!sysPath!;%CHOCO_DIR%\bin" >>"%LOGFILE%" 2>&1
) else (
    echo [%date% %time%] Chocolatey already in SYSTEM PATH.
)

:: 7) Refresh current session
echo [%date% %time%] Refreshing current session environment…
set "PATH=%sysPath%;%CHOCO_DIR%\bin"
if exist "%CHOCO_DIR%\bin\refreshenv.cmd" (
    call "%CHOCO_DIR%\bin\refreshenv.cmd"
)

echo [%date% %time%] Final PATH: %PATH%
echo [%date% %time%] Setup complete!
exit /b 0

:: === Check if Git is installed ===
echo Checking for Git installation... >>%LOGFILE% 2>&1
where git >>%LOGFILE% 2>&1
if errorlevel 1 (
    echo Git not found. Downloading Git installer... >>%LOGFILE% 2>&1
    powershell -Command "Invoke-WebRequest -Uri https://github.com/git-for-windows/git/releases/download/v2.50.0.windows.1/Git-2.50.0-64-bit.exe -OutFile Git-2.50.0-64-bit.exe" >>%LOGFILE% 2>&1
    if errorlevel 1 (
        echo ERROR: Failed to download Git installer. >>%LOGFILE%
        pause
        exit /b
    )
    echo Installing Git silently... >>%LOGFILE%
    start /wait Git-2.50.0-64-bit.exe /VERYSILENT /NORESTART >>%LOGFILE% 2>&1
    if errorlevel 1 (
        echo ERROR: Git installation failed. >>%LOGFILE%
        pause
        exit /b
    )
    del Git-2.50.0-64-bit.exe
    where git >>%LOGFILE% 2>&1
    if errorlevel 1 (
        echo WARNING: Git installed but not in PATH. >>%LOGFILE%
        pause
        exit /b
    )
)

:: === Check if Python is installed ===
echo Checking for Python... >>%LOGFILE%
where python >>%LOGFILE% 2>&1
if errorlevel 1 (
    echo Python not found. Installing Python 3.10.0... >>%LOGFILE%
    powershell -Command "Invoke-WebRequest -Uri https://www.python.org/ftp/python/3.10.0/python-3.10.0-amd64.exe -OutFile python-3.10.0-amd64.exe" >>%LOGFILE% 2>&1
    if errorlevel 1 exit /b
    start /wait python-3.10.0-amd64.exe /quiet InstallAllUsers=1 PrependPath=1 Include_test=0 >>%LOGFILE% 2>&1
    if errorlevel 1 exit /b
    del python-3.10.0-amd64.exe
)

:: === Check if Poetry is installed ===
echo Checking for Poetry... >>%LOGFILE%
set "POETRY_PATH="
for /f "delims=" %%p in ('where poetry 2^>nul') do (
    set "POETRY_PATH=%%p"
    goto PoetryFound
)

:InstallPoetry
echo Poetry not found. Installing... >>%LOGFILE%
powershell -Command "Invoke-WebRequest -Uri https://install.python-poetry.org -OutFile install-poetry.py" >>%LOGFILE% 2>&1
if errorlevel 1 exit /b
python install-poetry.py >>%LOGFILE% 2>&1
if errorlevel 1 exit /b
del install-poetry.py
set PATH=%USERPROFILE%\AppData\Roaming\Python\Scripts;%USERPROFILE%\AppData\Local\Programs\Python\Python310\Scripts;%PATH%
goto :eof

:PoetryFound
echo Poetry found at: %POETRY_PATH% >>%LOGFILE%


:: === Check for existing project ===
echo Checking for project folder... >>%LOGFILE%

if exist apps\ (
    if exist configuration\ (
        if exist manage.py (
            echo Project already present in current directory. >>%LOGFILE%
            goto AfterClone
        )
    )
)

echo Project not found in current folder. Preparing to clone... >>%LOGFILE%

if not exist aktiv-generation-uppsala (
    mkdir aktiv-generation-uppsala >>%LOGFILE% 2>&1
    echo Created 'aktiv-generation-uppsala' folder. >>%LOGFILE%
)

cd aktiv-generation-uppsala || (
    echo ERROR: Failed to enter 'aktiv-generation-uppsala' directory. >>%LOGFILE%
    echo Failed to change directory.
    pause
    exit /b
)

:: Check again if project was already cloned
if exist apps\ (
    if exist configuration\ (
        if exist manage.py (
            echo Project already exists inside 'aktiv-generation-uppsala'. Skipping clone. >>%LOGFILE%
            goto AfterClone
        )
    )
)

echo Cloning project into current folder... >>%LOGFILE%
git clone https://github.com/metetrkn/aktiv-generation-uppsala.git . >>%LOGFILE% 2>&1
if errorlevel 1 (
    echo ERROR: Git clone failed. >>%LOGFILE%
    pause
    exit /b
)

:AfterClone
echo Done checking and cloning project. >>%LOGFILE%


:: === Set Poetry to use current Python ===
echo Configuring Poetry interpreter... >>%LOGFILE%
call poetry env use python >>%LOGFILE% 2>&1 || exit /b


echo NO PROBLEM UNTIL NOW... >>%LOGFILE%


:: === Install dependencies ===
echo Installing dependencies... >>%LOGFILE%
call poetry install >>%LOGFILE% 2>&1 || exit /b



:: === Copy .env file ===
echo Checking for .env file... >>%LOGFILE%
if exist .env.example (
    if not exist .env copy .env.example .env >nul && echo .env file created. >>%LOGFILE%
) else (
    echo .env.example not found, skipping. >>%LOGFILE%
)

:: === PostgreSQL password prompt ===
set /p POSTGRES_PASS=Enter password for PostgreSQL superuser (postgres):

:: === Install PostgreSQL ===
echo Installing PostgreSQL... >>%LOGFILE%
powershell -Command "Invoke-WebRequest -Uri \"https://www.enterprisedb.com/postgresql-tutorial-resources-training-1?uuid=69f95902-b451-4735-b7e4-1b62209d4dfd&campaignId=postgres_rc_17\" -OutFile postgresql-installer.exe" >>%LOGFILE% 2>&1
if errorlevel 1 exit /b
start /wait postgresql-installer.exe --mode unattended --unattendedmodeui none --superpassword %POSTGRES_PASS% --servicename postgresql-x64-17 >>%LOGFILE% 2>&1
if errorlevel 1 exit /b

:: === Start PostgreSQL service ===
echo Starting PostgreSQL service... >>%LOGFILE%
net start postgresql-x64-17 >>%LOGFILE% 2>&1

:: === Check if PostgreSQL is running ===
sc query postgresql-x64-17 | findstr /I "RUNNING" >>%LOGFILE%
if errorlevel 1 (
    echo ERROR: PostgreSQL service is not running. >>%LOGFILE%
    pause
    exit /b
)

:: === Poetry shell ===
echo Launching Poetry shell... >>%LOGFILE%
call poetry shell >>%LOGFILE% 2>&1 || exit /b

:: === .env update reminder ===
echo.
echo *** Please update the .env file with your credentials now. ***
echo Press any key to continue once done...
pause >nul

:: === Django migrations ===
echo Running Django migrations... >>%LOGFILE%
call poetry run python manage.py migrate >>%LOGFILE% 2>&1 || exit /b

:: === Collect static files ===
echo Collecting static files... >>%LOGFILE%
call poetry run python manage.py collectstatic --noinput >>%LOGFILE% 2>&1 || exit /b

:: === Create superuser ===
echo Creating superuser... >>%LOGFILE%
call poetry run python manage.py createsuperuser >>%LOGFILE% 2>&1 || exit /b

:: === Run dev server ===
echo Starting Django dev server... >>%LOGFILE%
call poetry run python manage.py runserver >>%LOGFILE% 2>&1 || exit /b

endlocal
echo.
echo Setup completed. Press any key to close this window.
pause >nul
