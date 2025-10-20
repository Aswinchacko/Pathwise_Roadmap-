@echo off
echo Starting PathWise Resources Scraping Test...

:: Kill any existing processes on port 8001
echo Stopping any existing services...
for /f "tokens=5" %%a in ('netstat -aon ^| find ":8001" ^| find "LISTENING"') do taskkill /f /pid %%a 2>nul

:: Start the resources service
echo Starting Resources Service...
cd resources_service
start "Resources Service" cmd /k "node standalone_server.js"

:: Wait a moment for the service to start
echo Waiting for service to start...
timeout /t 3 /nobreak >nul

:: Open the test page
echo Opening test page...
cd ..
start "" "test_complete_scraping.html"

echo.
echo ✅ Resources Service started on http://localhost:8001
echo ✅ Test page opened in your browser
echo.
echo You can now test the scraping functionality!
echo.
echo To stop the service, close the Resources Service window.
pause


