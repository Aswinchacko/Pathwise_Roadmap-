@echo off
echo ===================================
echo Roadmap Data Reload Script
echo ===================================
echo.

REM Activate virtual environment if it exists
if exist "venv\Scripts\activate.bat" (
    call venv\Scripts\activate.bat
    echo Virtual environment activated
) else (
    echo Warning: Virtual environment not found
)

echo.
python reload_roadmap_data.py

echo.
pause

