@echo off
REM Setup script for Provider Lookup application (Windows)
REM This script:
REM 1. Creates a virtual environment
REM 2. Installs all required dependencies
REM 3. Imports data from the CSV file
REM 4. Runs the Flask application

echo ==== Provider Lookup Setup Script (Windows) ====
echo Setting up the application...

REM Check if Python is installed
python --version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo Python is not installed or not in PATH. Please install Python and try again.
    exit /b 1
)

REM Check for data file
set DATA_FILE=data\endpoint_pfile_20250407-20250413.csv
if not exist %DATA_FILE% (
    echo Data file not found: %DATA_FILE%
    echo Please download the NPI data file and place it in the data directory.
    echo You can download it from: https://download.cms.gov/nppes/NPI_Files.html
    
    REM Ask if user wants to continue without data import
    set /p CONTINUE=Continue without importing data? (y/n): 
    if /i not "%CONTINUE%"=="y" (
        echo Setup aborted.
        exit /b 1
    )
    set SKIP_IMPORT=true
) else (
    set SKIP_IMPORT=false
)

REM Create virtual environment if it doesn't exist
if not exist venv (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Install dependencies
echo Installing dependencies...
pip install --upgrade pip
pip install werkzeug==2.0.3
pip install flask==2.0.1
pip install sqlalchemy==1.4.46
pip install flask-sqlalchemy==2.5.1
pip install flask-migrate==3.1.0
pip install python-dotenv==0.19.0
pip install numpy==1.21.6 
pip install pandas==1.3.5
pip install gunicorn==20.1.0
pip install pymysql==1.0.2

REM Create .env file if it doesn't exist
if not exist .env (
    echo Creating .env file...
    
    REM Generate random secret key
    for /f "tokens=*" %%a in ('python -c "import secrets; print(secrets.token_hex(16))"') do set SECRET_KEY=%%a
    
    echo SECRET_KEY=%SECRET_KEY%>.env
    echo FLASK_APP=run.py>>.env
    echo FLASK_ENV=development>>.env
    echo DATABASE_URL=sqlite:///provider_lookup.db>>.env
    echo # GOOGLE_MAPS_API_KEY=your-api-key-here>>.env
)

REM Create database tables
echo Initializing database...
start /b python run.py
timeout /t 3 /nobreak >nul
taskkill /f /im python.exe >nul 2>&1

REM Import data if available
if "%SKIP_IMPORT%"=="false" (
    echo Importing data (this may take some time)...
    python scripts\import_data.py %DATA_FILE%
)

echo Setup complete!
echo.
echo To run the application:
echo 1. Activate the virtual environment: venv\Scripts\activate
echo 2. Start the server: python run.py
echo.
echo Starting the application now...
python run.py