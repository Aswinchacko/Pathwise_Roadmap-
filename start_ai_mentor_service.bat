@echo off
echo ====================================
echo AI-Powered Mentor Search Service
echo ====================================
echo.

REM Check if we're in the right directory
if not exist "linkedin_mentor_service\main.py" (
    echo [ERROR] Run this script from the PathWise root directory
    echo Current directory: %CD%
    pause
    exit /b 1
)

echo [1/4] Checking MongoDB...
tasklist /FI "IMAGENAME eq mongod.exe" 2>NUL | find /I /N "mongod.exe">NUL
if "%ERRORLEVEL%"=="0" (
    echo    ✓ MongoDB is running
) else (
    echo    ✗ MongoDB is NOT running
    echo    Please start MongoDB first!
    echo.
    echo    Quick start: net start MongoDB
    pause
    exit /b 1
)

echo.
echo [2/4] Checking Groq API Key...

REM Check if chatbot_service/.env exists
if exist "chatbot_service\.env" (
    echo    ✓ Found chatbot_service/.env
    findstr /C:"GROQ_API_KEY=gsk" chatbot_service\.env >NUL 2>&1
    if %ERRORLEVEL% EQU 0 (
        echo    ✓ Groq API Key found in chatbot_service/.env
        echo    📝 Service will use this key for AI search
    ) else (
        echo    ⚠ No valid Groq API key in chatbot_service/.env
        echo    📝 Service will use static fallback mode
    )
) else (
    echo    ⚠ chatbot_service/.env not found
)

REM Check if linkedin_mentor_service/.env exists
if exist "linkedin_mentor_service\.env" (
    echo    ✓ Found linkedin_mentor_service/.env
    findstr /C:"GROQ_API_KEY=gsk" linkedin_mentor_service\.env >NUL 2>&1
    if %ERRORLEVEL% EQU 0 (
        echo    ✓ Groq API Key found in linkedin_mentor_service/.env
        echo    📝 Service will use this key for AI search
    )
)

echo.
echo [3/4] Installing dependencies...
cd linkedin_mentor_service
if exist "requirements.txt" (
    echo    Installing Python packages...
    pip install -r requirements.txt --quiet
    if %ERRORLEVEL% EQU 0 (
        echo    ✓ Dependencies installed
    ) else (
        echo    ⚠ Some dependencies may have failed
    )
) else (
    echo    ✗ requirements.txt not found
)

echo.
echo [4/4] Starting AI-Powered Mentor Service...
echo.
echo ┌─────────────────────────────────────────────────┐
echo │  Service: http://localhost:8001                  │
echo │  Health:  http://localhost:8001/api/mentors/health│
echo │  Docs:    http://localhost:8001/docs            │
echo └─────────────────────────────────────────────────┘
echo.
echo 🤖 AI Features:
echo    - Groq-powered web search for real mentors
echo    - Automatic fallback to static data
echo    - Based on user's roadmap goal
echo.
echo Press Ctrl+C to stop the service
echo.

REM Start the service
python main.py

cd ..
pause

