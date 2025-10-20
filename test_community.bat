@echo off
echo ========================================
echo   Testing Community API Endpoints
echo ========================================
echo.

cd auth_back

echo [1] Testing GET /api/discussions...
curl -s http://localhost:5000/api/discussions > nul
if %errorlevel% equ 0 (
    echo ✓ GET /api/discussions - OK
) else (
    echo ✗ GET /api/discussions - FAILED
)
echo.

echo [2] Testing filtered discussions...
curl -s "http://localhost:5000/api/discussions?category=Web%%20Development" > nul
if %errorlevel% equ 0 (
    echo ✓ GET /api/discussions?category=Web Development - OK
) else (
    echo ✗ GET /api/discussions?category=Web Development - FAILED
)
echo.

echo ========================================
echo   Test Summary
echo ========================================
echo.
echo If all tests passed, the community backend is working!
echo.
echo To test the full feature:
echo 1. Open http://localhost:5173
echo 2. Log in to your account
echo 3. Click "Community" in the sidebar
echo 4. Try creating a question
echo 5. Try answering and voting
echo.
pause

