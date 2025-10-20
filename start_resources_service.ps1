# PowerShell script to start Resources Service
Write-Host "Starting PathWise Resources Service..." -ForegroundColor Green

# Set environment variables
$env:NODE_ENV = "development"
$env:PORT = "8001"
$env:MONGODB_URI = "mongodb://localhost:27017/pathwise_resources"
$env:CORS_ORIGIN = "http://localhost:5173"
$env:RATE_LIMIT_WINDOW_MS = "900000"
$env:RATE_LIMIT_MAX_REQUESTS = "100"

# Change to resources_service directory
Set-Location "resources_service"

Write-Host "Environment configured:" -ForegroundColor Yellow
Write-Host "  NODE_ENV: $env:NODE_ENV" -ForegroundColor Cyan
Write-Host "  PORT: $env:PORT" -ForegroundColor Cyan
Write-Host "  CORS_ORIGIN: $env:CORS_ORIGIN" -ForegroundColor Cyan

Write-Host "`nStarting standalone server..." -ForegroundColor Green

# Start the server
try {
    node standalone_server.js
} catch {
    Write-Host "Error starting server: $_" -ForegroundColor Red
    Write-Host "Make sure Node.js is installed and dependencies are available" -ForegroundColor Yellow
}

Write-Host "`nPress any key to exit..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")


