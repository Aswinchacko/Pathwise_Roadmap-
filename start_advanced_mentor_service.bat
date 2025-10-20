@echo off
echo.
echo ============================================================
echo   PATHWISE - Advanced Mentor Scraping Service
echo ============================================================
echo.
echo Starting mentor recommendation service with REAL LinkedIn scraping...
echo This service scrapes actual LinkedIn profiles based on roadmap goals.
echo.
echo Service will run on: http://localhost:8004
echo.
echo Key Features:
echo   - Real LinkedIn profile scraping
echo   - MongoDB roadmap integration
echo   - Multi-engine search (Google + Bing)
echo   - Intelligent fallback system
echo   - Respectful rate limiting
echo.
echo ============================================================
echo.

cd mentor_recommendation_service

echo Checking dependencies...
python -c "import fastapi, uvicorn, pymongo, aiohttp, bs4" 2>nul
if errorlevel 1 (
    echo.
    echo WARNING: Some dependencies missing!
    echo Installing required packages...
    pip install -r requirements.txt
    echo.
)

echo.
echo Starting service...
echo Press Ctrl+C to stop
echo.

python main.py

pause

