@echo off
echo.
echo ===============================================================
echo   PATHWISE - Complete Mentor Scraping System Launcher
echo ===============================================================
echo.
echo This will start all required services:
echo   1. MongoDB (database)
echo   2. Roadmap API (port 8001)
echo   3. Mentor Scraping Service (port 8004) 
echo   4. Frontend Dashboard (port 5173)
echo.
echo ===============================================================
echo.

echo [1/4] Checking MongoDB...
mongosh --eval "db.version()" >nul 2>&1
if errorlevel 1 (
    echo WARNING: MongoDB not running!
    echo Please start MongoDB first: mongod
    echo.
    pause
    exit /b 1
) else (
    echo ✓ MongoDB is running
)

echo.
echo [2/4] Starting Roadmap API (port 8001)...
start cmd /k "cd roadmap_api && echo Starting Roadmap API... && python main.py"
timeout /t 3 >nul

echo.
echo [3/4] Starting Mentor Scraping Service (port 8004)...
start cmd /k "cd mentor_recommendation_service && echo Starting Mentor Scraping Service... && python main.py"
timeout /t 3 >nul

echo.
echo [4/4] Starting Frontend Dashboard (port 5173)...
start cmd /k "cd dashboard && echo Starting Frontend... && npm run dev"
timeout /t 5 >nul

echo.
echo ===============================================================
echo   All Services Started!
echo ===============================================================
echo.
echo Services running:
echo   ✓ MongoDB         - localhost:27017
echo   ✓ Roadmap API     - http://localhost:8001
echo   ✓ Mentor Service  - http://localhost:8004
echo   ✓ Frontend        - http://localhost:5173
echo.
echo ===============================================================
echo.
echo NEXT STEPS:
echo   1. Open browser: http://localhost:5173
echo   2. Go to Roadmap page
echo   3. Create a roadmap: "Become a React Developer"
echo   4. Go to Mentors page
echo   5. See real LinkedIn profiles scraped!
echo.
echo Watch the Mentor Service terminal for scraping logs!
echo.
echo ===============================================================
echo.
echo Press any key to open the frontend...
pause >nul

start http://localhost:5173/mentors

echo.
echo Enjoy your LinkedIn mentor scraping system!
echo.
pause

