@echo off
REM PathWise Deployment Script for Windows
REM This script deploys the entire microservices stack on Windows

echo.
echo ============================================
echo    PathWise Deployment Manager
echo    Microservices Docker Deployment
echo ============================================
echo.

REM Check if Docker is running
docker info >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Docker is not running. Please start Docker Desktop.
    pause
    exit /b 1
)

echo [OK] Docker is running

REM Check if .env file exists
if not exist .env (
    echo [WARNING] .env file not found. Creating from env.template...
    if exist env.template (
        copy env.template .env >nul
        echo [INFO] Please edit .env file with your actual credentials before deployment!
        echo [INFO] Press any key after you've configured .env file...
        pause
    ) else (
        echo [ERROR] env.template not found. Cannot create .env file.
        pause
        exit /b 1
    )
)

echo [OK] .env file found

echo.
echo [INFO] Building Docker images...
docker-compose build

echo.
echo [INFO] Starting services...
docker-compose up -d

echo.
echo [INFO] Waiting for services to be healthy...
timeout /t 10 /nobreak >nul

echo.
echo [INFO] Checking service health...
docker ps --filter "name=pathwise"

echo.
echo ============================================
echo    Deployment Complete!
echo ============================================
echo.
echo Service URLs:
echo   Auth Service:         http://localhost/api/auth
echo   Roadmap API:          http://localhost/api/roadmap
echo   Chatbot Service:      http://localhost/api/chatbot
echo   Job Agent:            http://localhost/api/jobs
echo   Mentor Service:       http://localhost/api/mentors
echo   Project Service:      http://localhost/api/projects
echo   Resume Parser:        http://localhost/api/resume
echo   Subscription Service: http://localhost/api/subscription
echo   Resources Service:    http://localhost/api/resources
echo   Health Check:         http://localhost/health
echo.
echo Useful Commands:
echo   View logs:           docker-compose logs -f
echo   Stop services:       docker-compose down
echo   Restart services:    docker-compose restart
echo   View status:         docker-compose ps
echo.
echo MongoDB Connection:
echo   Internal: mongodb://mongodb:27017/pathwise
echo   External: mongodb://localhost:27017/pathwise
echo.

REM Open browser
echo Opening browser...
timeout /t 3 /nobreak >nul
start http://localhost/health

pause

