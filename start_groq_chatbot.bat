@echo off
echo ================================================
echo 🤖 Starting PathWise Groq Chatbot Service
echo ================================================
echo.

cd chatbot_service

echo 📦 Installing dependencies...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo ❌ Failed to install dependencies
    pause
    exit /b 1
)

echo.
echo ✅ Dependencies installed
echo.
echo 🔧 Loading environment from .env file...
echo    Make sure chatbot_service/.env exists with your GROQ_API_KEY
echo.
REM Environment variables will be loaded from .env file by launcher.py
set PORT=8004
set MONGODB_URI=mongodb://localhost:27017/

echo.
echo 🚀 Starting Groq-powered chatbot service...
echo.
echo 📍 Service: http://localhost:8004
echo 📚 API Docs: http://localhost:8004/docs
echo 🔍 Health: http://localhost:8004/health
echo.
echo 💬 This chatbot can answer ANYTHING like ChatGPT!
echo    - Technical questions
echo    - Coding help
echo    - Career advice
echo    - Explanations
echo    - And much more!
echo.
echo ================================================

python launcher.py

pause

