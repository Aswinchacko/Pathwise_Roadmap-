@echo off
echo ========================================
echo LinkedIn Mentor Scraping Service
echo ========================================
echo.

cd /d "%~dp0linkedin_mentor_service"

REM Check if venv exists
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
    echo.
)

REM Activate venv
call venv\Scripts\activate.bat

REM Install/update requirements
echo Checking dependencies...
pip install -r requirements.txt -q

REM Check MongoDB
echo.
echo Checking MongoDB connection...
python -c "from pymongo import MongoClient; client = MongoClient('mongodb://localhost:27017', serverSelectionTimeoutMS=2000); client.server_info(); print('✅ MongoDB connected')" 2>nul
if errorlevel 1 (
    echo ❌ MongoDB not running!
    echo Please start MongoDB first: mongod
    pause
    exit /b 1
)

REM Start the service
echo.
echo ========================================
echo Starting LinkedIn Mentor Scraping Service
echo API: http://localhost:8001
echo Docs: http://localhost:8001/docs
echo ========================================
echo.
echo Press Ctrl+C to stop the service
echo.

python -m uvicorn main:app --reload --host 0.0.0.0 --port 8001


