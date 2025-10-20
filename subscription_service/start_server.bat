@echo off
echo Starting PathWise Subscription Service...
cd /d "%~dp0"

REM Check if virtual environment exists
if not exist "venv\" (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
call venv\Scripts\activate

REM Install dependencies
echo Installing dependencies...
pip install -r requirements.txt

REM Start the service
echo Starting Subscription Service on port 8004...
python main.py

pause


