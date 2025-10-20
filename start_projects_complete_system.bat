@echo off
echo =========================================
echo   Starting Complete Projects System
echo =========================================
echo.

echo Starting Project Recommendation Service...
start "Project Recommendation Service" cmd /k "cd project_recommendation_service && call ..\venv\Scripts\activate && python main.py"

timeout /t 3 /nobreak > nul

echo Starting Frontend Dashboard...
start "Frontend Dashboard" cmd /k "cd dashboard && npm run dev"

timeout /t 2 /nobreak > nul

echo.
echo =========================================
echo   System Started Successfully!
echo =========================================
echo.
echo Services running:
echo   - Project Recommendation: http://localhost:5003
echo   - Frontend Dashboard: http://localhost:5173
echo.
echo Navigate to Projects page and enter your goal!
echo.
pause

