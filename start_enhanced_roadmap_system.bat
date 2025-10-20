@echo off
echo Starting Enhanced Roadmap System...
echo.

echo 1. Starting MongoDB (if not running)...
net start MongoDB 2>nul
if %errorlevel% neq 0 (
    echo MongoDB service not found or already running
)

echo.
echo 2. Starting Roadmap API...
cd roadmap_api
start "Roadmap API" cmd /k "python main.py"
cd ..

echo.
echo 3. Waiting for API to start...
timeout /t 5 /nobreak >nul

echo.
echo 4. Starting Dashboard...
cd dashboard
start "Dashboard" cmd /k "npm run dev"
cd ..

echo.
echo 5. Running Enhanced System Tests...
timeout /t 10 /nobreak >nul
python test_enhanced_roadmap_system.py

echo.
echo ✅ Enhanced Roadmap System Started!
echo.
echo 📊 Services:
echo   - Roadmap API: http://localhost:8000
echo   - Dashboard: http://localhost:5173
echo   - Health Check: http://localhost:8000/health
echo.
echo 📚 Documentation: ENHANCED_ROADMAP_SYSTEM.md
echo 🧪 Test Results: See above output
echo.
pause

