# Quick test script for LinkedIn Mentor Scraping Service
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Testing LinkedIn Mentor Scraping Service" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Test 1: Health Check
Write-Host "1. Testing Health Endpoint..." -ForegroundColor Yellow
try {
    $health = Invoke-RestMethod -Uri "http://localhost:8005/api/mentors/health" -Method Get
    Write-Host "[OK] Service is healthy!" -ForegroundColor Green
    Write-Host "   Status: $($health.status)" -ForegroundColor Gray
    Write-Host "   MongoDB: $($health.mongodb)" -ForegroundColor Gray
    Write-Host "   Browser: $($health.browser)" -ForegroundColor Gray
} catch {
    Write-Host "[ERROR] Health check failed: $_" -ForegroundColor Red
    exit 1
}

Write-Host ""

# Test 2: Root Endpoint
Write-Host "2. Testing Root Endpoint..." -ForegroundColor Yellow
try {
    $root = Invoke-RestMethod -Uri "http://localhost:8005/" -Method Get
    Write-Host "[OK] Root endpoint working!" -ForegroundColor Green
    Write-Host "   Service: $($root.service)" -ForegroundColor Gray
} catch {
    Write-Host "[ERROR] Root endpoint failed: $_" -ForegroundColor Red
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Service is ready!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "To test scraping (requires MongoDB with roadmap):" -ForegroundColor Yellow
Write-Host '  $body = @{ user_id = "test_user"; limit = 5 } | ConvertTo-Json'
Write-Host '  Invoke-RestMethod -Uri "http://localhost:8005/api/mentors/scrape" -Method Post -Body $body -ContentType "application/json"'
Write-Host ""
Write-Host "API Documentation: http://localhost:8005/docs" -ForegroundColor Cyan
Write-Host ""


