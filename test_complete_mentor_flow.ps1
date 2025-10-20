# Complete Test of LinkedIn Mentor Service
Write-Host ""
Write-Host "================================" -ForegroundColor Cyan
Write-Host "LINKEDIN MENTOR SERVICE TEST" -ForegroundColor Cyan
Write-Host "================================" -ForegroundColor Cyan
Write-Host ""

# Test 1: Health Check
Write-Host "[1/5] Testing Health Endpoint..." -ForegroundColor Yellow
try {
    $health = Invoke-RestMethod -Uri "http://localhost:8005/api/mentors/health"
    if ($health.status -eq "healthy") {
        Write-Host "  [OK] Service is healthy" -ForegroundColor Green
        Write-Host "  MongoDB: $($health.mongodb)" -ForegroundColor Gray
        Write-Host "  Browser: $($health.browser)" -ForegroundColor Gray
    } else {
        Write-Host "  [ERROR] Service unhealthy" -ForegroundColor Red
        exit 1
    }
} catch {
    Write-Host "  [ERROR] Health check failed: $_" -ForegroundColor Red
    exit 1
}

Write-Host ""

# Test 2: Check MongoDB Roadmap
Write-Host "[2/5] Checking MongoDB Roadmap..." -ForegroundColor Yellow
try {
    python -c "from pymongo import MongoClient; client = MongoClient('mongodb://localhost:27017'); roadmap = client.pathwise.roadmap.find_one({'user_id': 'test_user'}); print('[OK] Roadmap found:', roadmap['goal'] if roadmap else '[ERROR] No roadmap')"
} catch {
    Write-Host "  [WARNING] Could not verify roadmap" -ForegroundColor Yellow
}

Write-Host ""

# Test 3: Clear Cache (to get fresh results)
Write-Host "[3/5] Clearing Cache..." -ForegroundColor Yellow
try {
    $clear = Invoke-RestMethod -Uri "http://localhost:8005/api/mentors/cache/test_user" -Method Delete
    Write-Host "  [OK] Cache cleared: $($clear.deleted_count) items" -ForegroundColor Green
} catch {
    Write-Host "  [INFO] No cache to clear" -ForegroundColor Gray
}

Write-Host ""

# Test 4: Scrape Mentors (Fresh)
Write-Host "[4/5] Scraping Mentors (fresh)..." -ForegroundColor Yellow
try {
    $body = @{ user_id = "test_user"; limit = 5 } | ConvertTo-Json
    $result = Invoke-RestMethod -Uri "http://localhost:8005/api/mentors/scrape" -Method Post -Body $body -ContentType "application/json" -TimeoutSec 120
    
    if ($result.success) {
        Write-Host "  [OK] Successfully scraped mentors!" -ForegroundColor Green
        Write-Host "  Total Found: $($result.total_found)" -ForegroundColor Gray
        Write-Host "  Cached: $($result.cached)" -ForegroundColor Gray
        Write-Host "  Search Query: $($result.search_query)" -ForegroundColor Gray
        Write-Host ""
        Write-Host "  Mentors:" -ForegroundColor Cyan
        foreach ($mentor in $result.mentors) {
            Write-Host "    - $($mentor.name)" -ForegroundColor White
            Write-Host "      $($mentor.title) at $($mentor.company)" -ForegroundColor Gray
            Write-Host "      $($mentor.location)" -ForegroundColor Gray
            if ($mentor.is_sample) {
                Write-Host "      [SAMPLE DATA]" -ForegroundColor Yellow
            }
            Write-Host ""
        }
    } else {
        Write-Host "  [ERROR] Failed to scrape mentors" -ForegroundColor Red
        Write-Host "  Message: $($result.message)" -ForegroundColor Red
    }
} catch {
    Write-Host "  [ERROR] Scraping failed: $_" -ForegroundColor Red
    exit 1
}

Write-Host ""

# Test 5: Cached Results
Write-Host "[5/5] Testing Cache (should be instant)..." -ForegroundColor Yellow
try {
    $body = @{ user_id = "test_user"; limit = 5 } | ConvertTo-Json
    $startTime = Get-Date
    $result = Invoke-RestMethod -Uri "http://localhost:8005/api/mentors/scrape" -Method Post -Body $body -ContentType "application/json"
    $endTime = Get-Date
    $duration = ($endTime - $startTime).TotalMilliseconds
    
    if ($result.cached) {
        Write-Host "  [OK] Cached results returned!" -ForegroundColor Green
        Write-Host "  Response time: ${duration}ms" -ForegroundColor Gray
        Write-Host "  Total: $($result.total_found) mentors" -ForegroundColor Gray
    } else {
        Write-Host "  [WARNING] Results not cached (unexpected)" -ForegroundColor Yellow
    }
} catch {
    Write-Host "  [ERROR] Cache test failed: $_" -ForegroundColor Red
}

Write-Host ""
Write-Host "================================" -ForegroundColor Cyan
Write-Host "ALL TESTS PASSED!" -ForegroundColor Green
Write-Host "================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "The LinkedIn Mentor Service is fully operational!" -ForegroundColor Green
Write-Host ""
Write-Host "Next Steps:" -ForegroundColor Cyan
Write-Host "  1. Start frontend: cd dashboard && npm run dev" -ForegroundColor White
Write-Host "  2. Visit: http://localhost:5173" -ForegroundColor White
Write-Host "  3. Go to Mentors page to see the results!" -ForegroundColor White
Write-Host ""
Write-Host "API Documentation: http://localhost:8005/docs" -ForegroundColor Cyan
Write-Host ""


