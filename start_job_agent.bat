@echo off
echo ============================================
echo   Starting PathWise Job Agent Service
echo ============================================
echo.

cd job_agent_service

echo Checking Python environment...
python --version
echo.

echo Installing/Updating dependencies...
pip install -r requirements.txt --quiet
echo.

echo Starting Job Agent Service on port 5007...
echo.
echo API will be available at: http://localhost:5007
echo API Docs: http://localhost:5007/docs
echo.

python main.py

pause

