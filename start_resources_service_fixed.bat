@echo off
echo Starting PathWise Resources Service...

cd resources_service

:: Set environment variables
set NODE_ENV=development
set PORT=8001
set MONGODB_URI=mongodb://localhost:27017/pathwise_resources
set CORS_ORIGIN=http://localhost:5173
set RATE_LIMIT_WINDOW_MS=900000
set RATE_LIMIT_MAX_REQUESTS=100

:: Start the service
echo Starting Resources Service on port 8001...
node server.js

pause


