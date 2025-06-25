@echo off
setlocal ENABLEEXTENSIONS

:: === Welcome message ===
echo Hi, welcome to Aktiv-Generation-Uppsala website localhost setup installation wizard.
echo To automatically install this web app on your local machine, you need to clone the project into your local system.
echo.
pause

:: === Function to check for Q to exit ===
:checkQuit
set "KEY="
set /p "KEY=Press any key to continue, or Q then Enter to quit: "
if /I "%KEY%"=="Q" (
    echo Setup aborted by user.
    exit /b
)
goto :eof

:: === Check if Git is installed ===
echo Checking for Git installation...
where git >nul 2>nul
if errorlevel 1 (
    echo Git not found. Downloading Git installer...
    powershell -Command "Invoke-WebRequest -Uri https://github.com/git-for-windows/git/releases/download/v2.50.0.windows.1/Git-2.50.0-64-bit.exe -OutFile Git-2.50.0-64-bit.exe"
    if errorlevel 1 (
        echo ERROR: Failed to download Git installer. Please install Git manually.
        pause
        exit /b
    )
    echo Installing Git silently...
    start /wait Git-2.50.0-64-bit.exe /VERYSILENT /NORESTART
    if errorlevel 1 (
        echo ERROR: Git installation failed. Please install Git manually.
        pause
        exit /b
    )
    del Git-2.50.0-64-bit.exe

    :: Check if Git is now in PATH
    where git >nul 2>nul
    if errorlevel 1 (
        echo WARNING: Git was installed but is not in your PATH.
        echo Please add Git to your PATH environment variable manually before continuing.
        pause
        exit /b
    )
) else (
    echo Git is already installed.
)
call :checkQuit

:: === Check if Python is installed ===
echo Checking for Python installation...
where python >nul 2>nul
if errorlevel 1 (
    echo Python not found. Installing Python 3.10.0...
    powershell -Command "Invoke-WebRequest -Uri https://www.python.org/ftp/python/3.10.0/python-3.10.0-amd64.exe -OutFile python-3.10.0-amd64.exe"
    if errorlevel 1 exit /b
    start /wait python-3.10.0-amd64.exe /quiet InstallAllUsers=1 PrependPath=1 Include_test=0
    if errorlevel 1 exit /b
    del python-3.10.0-amd64.exe
) else (
    echo Python is already installed.
)
call :checkQuit

:: === Check if Poetry is installed, install if missing ===
echo Checking for Poetry installation...
where poetry >nul 2>nul
if errorlevel 1 (
    echo Installing Poetry...
    powershell -Command "Invoke-WebRequest -Uri https://install.python-poetry.org -OutFile install-poetry.py"
    if errorlevel 1 exit /b
    python install-poetry.py
    if errorlevel 1 exit /b
    del install-poetry.py
    set PATH=%USERPROFILE%\AppData\Roaming\Python\Scripts;%USERPROFILE%\AppData\Local\Programs\Python\Python310\Scripts;%PATH%
) else (
    echo Poetry is already installed.
)
call :checkQuit

:: === Check if project is already cloned ===
echo Checking for existing project folder structure...
if exist apps\ if exist configuration\ if exist manage.py (
    echo Project already present. Skipping clone.
) else (
    echo Cloning project into 'aktiv-generation-uppsala' directory...
    git clone https://github.com/metetrkn/aktiv-generation-uppsala.git aktiv-generation-uppsala
    if errorlevel 1 (
        echo ERROR: Failed to clone project.
        pause
        exit /b
    )
    cd aktiv-generation-uppsala
)
call :checkQuit

:: === Install project dependencies using Poetry ===
echo Installing project dependencies with Poetry...
call poetry install || exit /b
call :checkQuit

:: === Ensure Poetry is using the correct Python interpreter ===
echo Setting Poetry to use the Python interpreter...
call poetry env use python || exit /b
call :checkQuit

:: === Copy .env file if it doesn't already exist ===
echo Checking for .env file...
if exist .env.example (
    if not exist .env copy .env.example .env >nul && echo .env file created.
) else (
    echo .env.example not found, skipping copy.
)
call :checkQuit

:: === Prompt for PostgreSQL superuser password ===
set /p POSTGRES_PASS=Enter password for PostgreSQL superuser (postgres):

:: === Download and install PostgreSQL 17.5 silently ===
echo Downloading and installing PostgreSQL 17.5 silently...
powershell -Command "Invoke-WebRequest -Uri \"https://www.enterprisedb.com/postgresql-tutorial-resources-training-1?uuid=69f95902-b451-4735-b7e4-1b62209d4dfd&campaignId=postgres_rc_17\" -OutFile postgresql-installer.exe"
if errorlevel 1 exit /b
start /wait postgresql-installer.exe --mode unattended --unattendedmodeui none --superpassword %POSTGRES_PASS% --servicename postgresql-x64-17
if errorlevel 1 exit /b
call :checkQuit

:: === Start PostgreSQL service ===
echo Starting PostgreSQL service...
net start postgresql-x64-17 >nul 2>nul

:: === Verify that PostgreSQL service is running ===
sc query postgresql-x64-17 | findstr /I "RUNNING" >nul
if errorlevel 1 (
    echo ERROR: PostgreSQL service is not running. Please verify manually.
    pause
    exit /b
) else (
    echo PostgreSQL service is running.
)
call :checkQuit

:: === Enter Poetry shell ===
echo Entering Poetry shell...
call poetry shell || exit /b
call :checkQuit

:: === Ask user to manually update .env with credentials ===
echo.
echo *** Please update the .env file with your credentials now. ***
echo Press any key to continue once done...
pause >nul

:: === Apply Django migrations ===
echo Applying Django migrations...
call poetry run python manage.py migrate || exit /b
call :checkQuit

:: === Collect static files (for production setup) ===
echo Collecting static files...
call poetry run python manage.py collectstatic --noinput || exit /b
call :checkQuit

:: === Create Django superuser (interactive) ===
echo Creating Django superuser (interactive)...
call poetry run python manage.py createsuperuser || exit /b
call :checkQuit

:: === Start the Django development server ===
echo Starting Django development server...
call poetry run python manage.py runserver || exit /b

endlocal
pause
