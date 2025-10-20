@echo off
echo Starting LinkedIn Mentor Scraping Service...
echo.

cd /d "%~dp0"

REM Check if venv exists
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate venv
call venv\Scripts\activate.bat

REM Install requirements
echo Installing requirements...
pip install -r requirements.txt

REM Start server
echo.
echo Starting server on http://localhost:8005
echo.
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8005


