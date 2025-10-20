@echo off
echo ================================================
echo 🚀 Starting Complete PathWise Chatbot System
echo ================================================
echo.
echo This will start:
echo   1. Groq Chatbot Service (Backend)
echo   2. React Dashboard (Frontend)
echo.
echo ================================================

echo.
echo 📦 Step 1: Installing chatbot dependencies...
cd chatbot_service
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo ❌ Failed to install chatbot dependencies
    pause
    exit /b 1
)
cd ..

echo.
echo 📦 Step 2: Installing dashboard dependencies...
cd dashboard
call npm install
if %errorlevel% neq 0 (
    echo ❌ Failed to install dashboard dependencies
    pause
    exit /b 1
)
cd ..

echo.
echo ✅ All dependencies installed!
echo.

echo 🚀 Step 3: Starting Chatbot Service...
start "PathWise Chatbot Service" cmd /k "cd chatbot_service && python launcher.py"

echo ⏳ Waiting for chatbot service to initialize...
timeout /t 5 /nobreak > nul

echo.
echo 🚀 Step 4: Starting Dashboard...
start "PathWise Dashboard" cmd /k "cd dashboard && npm run dev"

echo.
echo ================================================
echo ✅ System is starting!
echo ================================================
echo.
echo 🤖 Chatbot Service: http://localhost:8004
echo 📚 API Docs: http://localhost:8004/docs
echo.
echo 🌐 Dashboard: http://localhost:5173
echo 💬 Go to Dashboard → Chatbot page
echo.
echo 💡 Tips:
echo    - Ask anything like ChatGPT
echo    - The bot can help with coding, career advice, explanations
echo    - Your chats are saved automatically
echo.
echo ================================================
echo.
echo Two windows opened:
echo   1. Chatbot Service (Keep this running)
echo   2. Dashboard (Keep this running)
echo.
echo Press any key to close this window (services will keep running)
pause

