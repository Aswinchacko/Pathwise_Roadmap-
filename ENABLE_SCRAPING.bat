@echo off
echo ==========================================
echo Enable LinkedIn Web Scraping
echo ==========================================
echo.
echo WARNING: Web scraping may not work due to:
echo - Google/Bing blocking bots
echo - LinkedIn CAPTCHA challenges
echo - IP rate limiting
echo.
echo Current mode: Curated profiles (recommended)
echo.
choice /C YN /M "Enable experimental web scraping anyway"
if errorlevel 2 goto :cancel

echo.
echo Setting environment variable...
setx ENABLE_LINKEDIN_SCRAPING "true"

echo.
echo ==========================================
echo Web scraping ENABLED for current session
echo ==========================================
echo.
echo Restart the service for changes to take effect:
echo   start_linkedin_mentor_service.bat
echo.
echo To disable later, run:
echo   setx ENABLE_LINKEDIN_SCRAPING "false"
echo.
pause
exit

:cancel
echo.
echo Keeping curated mode (recommended)
echo.
pause

