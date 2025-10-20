@echo off
echo ========================================
echo Starting AI Learning Path Service
echo ========================================
echo.

cd learning_path_service

echo Installing dependencies...
pip install -r requirements.txt --quiet

echo.
echo Starting service on port 8003...
echo Press Ctrl+C to stop
echo.

python main.py

pause

