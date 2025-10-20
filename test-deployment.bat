@echo off
REM PathWise Deployment Test Script for Windows
REM Tests all services after deployment

setlocal enabledelayedexpansion

echo.
echo ============================================
echo    PathWise Deployment Test
echo ============================================
echo.

set BASE_URL=http://localhost
if not "%1"=="" set BASE_URL=%1

echo Testing services at: %BASE_URL%
echo.

set total=0
set passed=0

REM Test function
call :test_endpoint "Nginx Health" "%BASE_URL%/health"
call :test_endpoint "Auth Service" "%BASE_URL%/api/auth/health"
call :test_endpoint "Roadmap API" "%BASE_URL%/api/roadmap/health"
call :test_endpoint "Chatbot Service" "%BASE_URL%/api/chatbot/health"
call :test_endpoint "Job Agent" "%BASE_URL%/api/jobs/health"
call :test_endpoint "Mentor Service" "%BASE_URL%/api/mentors/health"
call :test_endpoint "Project Service" "%BASE_URL%/api/projects/health"
call :test_endpoint "Resume Parser" "%BASE_URL%/api/resume/health"
call :test_endpoint "Subscription Service" "%BASE_URL%/api/subscription/health"
call :test_endpoint "Resources Service" "%BASE_URL%/api/resources/health"

echo.
echo === Docker Containers ===
docker ps --filter "name=pathwise" --format "{{.Names}}"

echo.
echo ============================================
echo            Test Summary
echo ============================================
echo.
echo Total Tests: %total%
echo Passed: %passed%
set /a failed=%total%-%passed%
echo Failed: %failed%
echo.

if %passed% == %total% (
    echo [SUCCESS] All tests passed! Deployment successful!
    exit /b 0
) else (
    echo [WARNING] Some tests failed. Check logs:
    echo   docker-compose logs -f
    exit /b 1
)

:test_endpoint
set /a total+=1
set "name=%~1"
set "url=%~2"

echo | set /p dummy="Testing %name%... "

curl -s -o nul -w "%%{http_code}" "%url%" --max-time 10 > temp_status.txt
set /p status=<temp_status.txt
del temp_status.txt

if "%status%"=="200" (
    echo [PASS] HTTP %status%
    set /a passed+=1
) else (
    echo [FAIL] HTTP %status%
)

goto :eof

