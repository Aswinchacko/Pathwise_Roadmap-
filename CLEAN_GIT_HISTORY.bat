@echo off
REM Script to clean git history and remove all secrets

echo ================================================
echo   Cleaning Git History - Removing All Secrets
echo ================================================
echo.

echo [INFO] This will create a new git history without secrets
echo [INFO] Your files will remain unchanged on disk
echo.

pause

echo.
echo [STEP 1] Backing up current state...
git branch backup-with-secrets

echo [STEP 2] Removing .git folder...
rmdir /s /q .git

echo [STEP 3] Initializing fresh repository...
git init

echo [STEP 4] Staging all files (with .gitignore protection)...
git add .

echo [STEP 5] Creating initial commit...
git commit -m "Initial commit - Complete PathWise microservices with Docker deployment"

echo [STEP 6] Connecting to GitHub...
git remote add origin https://github.com/Aswinchacko/Pathwise_Roadmap-.git

echo.
echo ================================================
echo   Git history cleaned successfully!
echo ================================================
echo.
echo Next step: Push to GitHub
echo   git push -u origin master --force
echo.
echo WARNING: This will replace all history on GitHub
echo          Make sure you want to do this!
echo.
pause

