@echo off
echo Starting Razorpay Subscription Service...
echo.

cd subscription_service

echo Checking environment...
if not exist .env (
    echo Creating .env file...
    echo RAZORPAY_KEY_ID=rzp_test_1DP5mmOlF5G5ag > .env
    echo RAZORPAY_KEY_SECRET=thisisasecretkey >> .env
    echo MONGODB_URL=mongodb://localhost:27017 >> .env
    echo FRONTEND_URL=http://localhost:5173 >> .env
    echo .env file created!
)

echo Installing dependencies...
pip install -r requirements.txt

echo.
echo Starting subscription service on port 8005...
echo Press Ctrl+C to stop the service
echo.

python main.py

pause
