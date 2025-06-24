@echo off
setlocal

:: Ask for GitHub credentials
set /p GITHUB_USER=GitHub Username: 
set /p GITHUB_PASS=GitHub Token/Password: 

:: Check Python
where python >nul 2>nul
if errorlevel 1 (
    echo Python not found. Installing Python 3.10.0...
    curl -o python-3.10.0-amd64.exe https://www.python.org/ftp/python/3.10.0/python-3.10.0-amd64.exe
    start /wait python-3.10.0-amd64.exe /quiet InstallAllUsers=1 PrependPath=1 Include_test=0
    del python-3.10.0-amd64.exe
)

:: Install Poetry if not installed
where poetry >nul 2>nul
if errorlevel 1 (
    echo Installing Poetry...
    curl -sSL https://install.python-poetry.org | python -
    set PATH=%USERPROFILE%\AppData\Roaming\Python\Scripts;%PATH%
)

:: Clone repo (optional)
:: git clone https://%GITHUB_USER%:%GITHUB_PASS%@github.com/your/repo.git

:: Setup project
call poetry install
call poetry shell
call poetry run python manage.py migrate
call poetry run python manage.py runserver

endlocal
pause