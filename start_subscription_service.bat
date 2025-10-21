@echo off
echo ========================================
echo Starting PathWise Subscription Service
echo ========================================
echo.

cd subscription_service

echo Activating virtual environment...
if exist venv\Scripts\activate.bat (
    call venv\Scripts\activate.bat
) else if exist ..\venv\Scripts\activate.bat (
    call ..\venv\Scripts\activate.bat
) else (
    echo Virtual environment not found. Using system Python...
)

echo.
echo Starting subscription service on port 8005...
echo.
python main.py

pause

