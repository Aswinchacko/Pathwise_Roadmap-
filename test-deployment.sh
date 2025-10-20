#!/bin/bash

# PathWise Deployment Test Script
# Tests all services after deployment

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}"
echo "╔═══════════════════════════════════════╗"
echo "║   PathWise Deployment Test            ║"
echo "╚═══════════════════════════════════════╝"
echo -e "${NC}"

# Test URLs
BASE_URL="${1:-http://localhost}"

echo -e "${BLUE}Testing services at: ${BASE_URL}${NC}\n"

# Function to test endpoint
test_endpoint() {
    local name=$1
    local url=$2
    local expected=${3:-200}
    
    echo -n "Testing ${name}... "
    
    status=$(curl -s -o /dev/null -w "%{http_code}" "${url}" --max-time 10)
    
    if [ "$status" = "$expected" ]; then
        echo -e "${GREEN}✅ PASS${NC} (HTTP $status)"
        return 0
    else
        echo -e "${RED}❌ FAIL${NC} (HTTP $status, expected $expected)"
        return 1
    fi
}

# Test counters
total=0
passed=0

# Health Checks
echo -e "${YELLOW}=== Health Checks ===${NC}"

test_endpoint "Nginx Health" "${BASE_URL}/health" && ((passed++))
((total++))

test_endpoint "Auth Service" "${BASE_URL}/api/auth/health" && ((passed++))
((total++))

test_endpoint "Roadmap API" "${BASE_URL}/api/roadmap/health" && ((passed++))
((total++))

test_endpoint "Chatbot Service" "${BASE_URL}/api/chatbot/health" && ((passed++))
((total++))

test_endpoint "Job Agent" "${BASE_URL}/api/jobs/health" && ((passed++))
((total++))

test_endpoint "Mentor Service" "${BASE_URL}/api/mentors/health" && ((passed++))
((total++))

test_endpoint "Project Service" "${BASE_URL}/api/projects/health" && ((passed++))
((total++))

test_endpoint "Resume Parser" "${BASE_URL}/api/resume/health" && ((passed++))
((total++))

test_endpoint "Subscription Service" "${BASE_URL}/api/subscription/health" && ((passed++))
((total++))

test_endpoint "Resources Service" "${BASE_URL}/api/resources/health" && ((passed++))
((total++))

echo ""
echo -e "${YELLOW}=== Docker Containers ===${NC}"

# Check if running locally
if docker ps &> /dev/null; then
    containers=$(docker ps --filter "name=pathwise" --format "{{.Names}}" | wc -l)
    expected_containers=11
    
    echo "Running containers: $containers/$expected_containers"
    
    if [ "$containers" -eq "$expected_containers" ]; then
        echo -e "${GREEN}✅ All containers running${NC}"
    else
        echo -e "${RED}❌ Some containers missing${NC}"
        echo "Expected containers:"
        echo "  - pathwise-mongodb"
        echo "  - pathwise-auth"
        echo "  - pathwise-roadmap"
        echo "  - pathwise-chatbot"
        echo "  - pathwise-jobs"
        echo "  - pathwise-mentors"
        echo "  - pathwise-projects"
        echo "  - pathwise-resume"
        echo "  - pathwise-subscription"
        echo "  - pathwise-resources"
        echo "  - pathwise-nginx"
        echo ""
        echo "Currently running:"
        docker ps --filter "name=pathwise" --format "  - {{.Names}}"
    fi
else
    echo -e "${YELLOW}ℹ️  Docker not accessible (remote deployment?)${NC}"
fi

# Summary
echo ""
echo -e "${BLUE}╔═══════════════════════════════════════╗${NC}"
echo -e "${BLUE}║           Test Summary                ║${NC}"
echo -e "${BLUE}╚═══════════════════════════════════════╝${NC}"
echo ""
echo "Total Tests: $total"
echo -e "Passed: ${GREEN}$passed${NC}"
echo -e "Failed: ${RED}$((total - passed))${NC}"
echo ""

if [ "$passed" -eq "$total" ]; then
    echo -e "${GREEN}🎉 All tests passed! Deployment successful!${NC}"
    exit 0
else
    echo -e "${RED}⚠️  Some tests failed. Check logs:${NC}"
    echo "  docker-compose logs -f"
    exit 1
fi

