@echo off
echo ========================================
echo   PathWise Community - Stack Overflow Style
echo ========================================
echo.

echo [1/3] Seeding sample discussions...
cd auth_back
call node seedDiscussions.js
if %errorlevel% neq 0 (
    echo ERROR: Failed to seed discussions
    pause
    exit /b 1
)
echo ✓ Sample discussions seeded successfully!
echo.

echo [2/3] Starting backend server...
start "PathWise Backend" cmd /k "npm start"
timeout /t 3 /nobreak > nul
echo ✓ Backend server started on http://localhost:5000
echo.

echo [3/3] Starting frontend...
cd ..\dashboard
start "PathWise Frontend" cmd /k "npm run dev"
timeout /t 3 /nobreak > nul
echo ✓ Frontend started on http://localhost:5173
echo.

echo ========================================
echo   Community feature is ready!
echo ========================================
echo.
echo Open your browser to: http://localhost:5173
echo Navigate to Community section
echo.
echo Press any key to exit...
pause > nul

