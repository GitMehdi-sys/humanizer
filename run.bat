@echo off
REM Startup script for Humanize Web Application (Windows)

echo ========================================
echo  Humanize Web Application Startup
echo ========================================
echo.

REM Set Python path to include src directory
set PYTHONPATH=%PYTHONPATH%;%CD%\src

echo Checking Python installation...
python --version
if %errorlevel% neq 0 (
    echo ERROR: Python not found. Please install Python 3.8 or higher.
    pause
    exit /b 1
)
echo.

echo Checking dependencies...
python -c "import fastapi, uvicorn, jinja2" 2>nul
if %errorlevel% neq 0 (
    echo Installing required packages...
    pip install fastapi uvicorn[standard] jinja2 python-multipart
    if %errorlevel% neq 0 (
        echo ERROR: Failed to install dependencies
        pause
        exit /b 1
    )
)
echo Dependencies OK
echo.

echo Starting server on http://localhost:8000
echo Press CTRL+C to stop the server
echo.

REM Run the application
python -m uvicorn webapp.main:app --reload --host 127.0.0.1 --port 8000

pause