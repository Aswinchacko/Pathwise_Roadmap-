@echo off
echo ================================================
echo 🤖 Starting PathWise Groq Chatbot System
echo ================================================
echo.

cd chatbot_service

echo 📦 Installing Python dependencies...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo ❌ Failed to install dependencies
    pause
    exit /b 1
)

echo.
echo 🚀 Starting Groq-powered Chatbot Service...
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

python start_server.py

pause
