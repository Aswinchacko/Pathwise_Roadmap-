@echo off
echo ========================================
echo Testing AI Learning Path Service
echo ========================================
echo.
echo Make sure the service is running on port 8003
echo.
pause

cd learning_path_service
python test_service.py

pause



