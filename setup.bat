@echo off
setlocal ENABLEEXTENSIONS

:: === Ask user for GitHub credentials ===
set /p GITHUB_USER=GitHub Username: 
set /p GITHUB_PASS=GitHub Token/Password: 

:: === Check if Python is installed ===
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

:: === Check if Poetry is installed, install if missing ===
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

:: === Clone project repository (optional/manual step) ===
:: git clone https://github.com/metetrkn/aktiv-generation-uppsala.git

:: === Install project dependencies using Poetry ===
call poetry install || exit /b

:: === Ensure Poetry is using the correct Python interpreter ===
call poetry env use python || exit /b

:: === Copy .env file if it doesn't already exist ===
if exist .env.example (
    if not exist .env copy .env.example .env >nul && echo .env file created.
) else (
    echo .env.example not found, skipping copy.
)

:: === Download and install PostgreSQL 17.5 ===
echo Installing PostgreSQL 17.5...
powershell -Command "Invoke-WebRequest -Uri \"https://www.enterprisedb.com/postgresql-tutorial-resources-training-1?uuid=69f95902-b451-4735-b7e4-1b62209d4dfd&campaignId=postgres_rc_17\" -OutFile postgresql-installer.exe"
if errorlevel 1 exit /b
start /wait postgresql-installer.exe
if errorlevel 1 exit /b

:: === Start PostgreSQL service ===
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

:: === Enter Poetry shell ===
call poetry shell || exit /b

:: === Ask user to manually update .env with credentials ===
echo.
echo *** Please update the .env file with your credentials now. ***
echo Press any key to continue once done...
pause >nul

:: === Apply Django migrations ===
call poetry run python manage.py migrate || exit /b

:: === Collect static files (for production setup) ===
call poetry run python manage.py collectstatic --noinput || exit /b

:: === Create Django superuser (interactive) ===
call poetry run python manage.py createsuperuser || exit /b

:: === Start the Django development server ===
call poetry run python manage.py runserver || exit /b

endlocal
pause
