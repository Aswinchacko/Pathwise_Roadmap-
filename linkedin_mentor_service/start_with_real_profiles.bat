@echo off
echo ============================================================
echo LinkedIn Mentor Service - Real Profiles Mode
echo ============================================================
echo.

cd /d "%~dp0"

REM Check if .env exists
if not exist ".env" (
    echo WARNING: No .env file found!
    echo.
    echo To get REAL profiles, create a .env file with:
    echo   SERPER_API_KEY=your_key_here
    echo   GROQ_API_KEY=your_key_here
    echo.
    echo Get free keys at:
    echo   - Serper: https://serper.dev/
    echo   - Groq: https://console.groq.com/
    echo.
    echo Press any key to continue with static data...
    pause >nul
)

REM Show current configuration
echo Checking configuration...
echo.

if exist ".env" (
    findstr "SERPER_API_KEY" .env >nul 2>&1
    if errorlevel 1 (
        echo [!] SERPER_API_KEY: Not found
        echo     Will use AI-generated profiles
    ) else (
        echo [OK] SERPER_API_KEY: Configured
        echo     Will find REAL LinkedIn profiles!
    )
    echo.
    
    findstr "GROQ_API_KEY" .env >nul 2>&1
    if errorlevel 1 (
        echo [!] GROQ_API_KEY: Not found
        echo     Will use static data
    ) else (
        echo [OK] GROQ_API_KEY: Configured
    )
    echo.
)

REM Activate venv if exists
if exist "venv\Scripts\activate.bat" (
    echo Activating virtual environment...
    call venv\Scripts\activate.bat
) else (
    echo Creating virtual environment...
    python -m venv venv
    call venv\Scripts\activate.bat
    echo Installing requirements...
    pip install -r requirements.txt
)

echo.
echo ============================================================
echo Starting service on http://localhost:8001
echo ============================================================
echo.
echo Service Status:
echo   - Health Check: http://localhost:8001/
echo   - API Docs: http://localhost:8001/docs
echo   - Frontend: http://localhost:5173/mentors
echo.
echo Press Ctrl+C to stop
echo ============================================================
echo.

python main.py

