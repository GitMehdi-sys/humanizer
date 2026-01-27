@echo off
REM Diagnostic script for Humanize Web Application

echo ========================================
echo  Humanize Web App Diagnostics
echo ========================================
echo.

echo 1. Checking Python installation...
python --version
if %errorlevel% neq 0 (
    echo [ERROR] Python not found!
    echo Please install Python from https://www.python.org/downloads/
    goto :end
) else (
    echo [OK] Python is installed
)
echo.

echo 2. Checking current directory...
echo Current directory: %CD%
dir /b
echo.

echo 3. Checking if src folder exists...
if exist "src\humanize\__init__.py" (
    echo [OK] src\humanize\__init__.py found
) else (
    echo [ERROR] src\humanize\__init__.py NOT FOUND!
    echo Make sure you have the correct directory structure.
    goto :end
)
echo.

echo 4. Checking if webapp folder exists...
if exist "webapp\main.py" (
    echo [OK] webapp\main.py found
) else (
    echo [ERROR] webapp\main.py NOT FOUND!
    echo Make sure you have the correct directory structure.
    goto :end
)
echo.

echo 5. Checking if templates exist...
if exist "webapp\templates\base.html" (
    echo [OK] Templates folder found
) else (
    echo [ERROR] Templates NOT FOUND!
    goto :end
)
echo.

echo 6. Checking Python packages...
echo Checking FastAPI...
python -c "import fastapi; print('FastAPI version:', fastapi.__version__)" 2>nul
if %errorlevel% neq 0 (
    echo [ERROR] FastAPI not installed
    echo Run: pip install fastapi
) else (
    echo [OK] FastAPI is installed
)

echo Checking Uvicorn...
python -c "import uvicorn; print('Uvicorn version:', uvicorn.__version__)" 2>nul
if %errorlevel% neq 0 (
    echo [ERROR] Uvicorn not installed
    echo Run: pip install uvicorn[standard]
) else (
    echo [OK] Uvicorn is installed
)

echo Checking Jinja2...
python -c "import jinja2; print('Jinja2 version:', jinja2.__version__)" 2>nul
if %errorlevel% neq 0 (
    echo [ERROR] Jinja2 not installed
    echo Run: pip install jinja2
) else (
    echo [OK] Jinja2 is installed
)
echo.

echo 7. Testing humanize import...
set PYTHONPATH=%PYTHONPATH%;%CD%\src
python -c "import sys; sys.path.insert(0, 'src'); import humanize; print('Humanize loaded successfully'); print('Available functions:', dir(humanize)[:5])" 2>nul
if %errorlevel% neq 0 (
    echo [ERROR] Cannot import humanize module
) else (
    echo [OK] Humanize module imports correctly
)
echo.

echo 8. Testing webapp import...
python -c "import sys; sys.path.insert(0, 'src'); from webapp.main import app; print('WebApp loaded successfully')" 2>nul
if %errorlevel% neq 0 (
    echo [ERROR] Cannot import webapp.main
    echo This is likely the problem. Check the error above.
) else (
    echo [OK] WebApp imports correctly
)
echo.

echo ========================================
echo  Diagnostics Complete
echo ========================================
echo.
echo If all checks pass, try running: run.bat
echo.

:end
pause