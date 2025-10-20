#!/bin/bash

# PathWise Deployment Script
# This script deploys the entire microservices stack

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Banner
echo -e "${BLUE}"
echo "╔═══════════════════════════════════════╗"
echo "║   PathWise Deployment Manager         ║"
echo "║   Microservices Docker Deployment     ║"
echo "╚═══════════════════════════════════════╝"
echo -e "${NC}"

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo -e "${RED}❌ Docker is not installed. Please install Docker first.${NC}"
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo -e "${RED}❌ Docker Compose is not installed. Please install Docker Compose first.${NC}"
    exit 1
fi

echo -e "${GREEN}✅ Docker and Docker Compose are installed${NC}"

# Check if .env file exists
if [ ! -f .env ]; then
    echo -e "${YELLOW}⚠️  .env file not found. Creating from .env.example...${NC}"
    if [ -f .env.example ]; then
        cp .env.example .env
        echo -e "${YELLOW}📝 Please edit .env file with your actual credentials before deployment!${NC}"
        echo -e "${YELLOW}   nano .env${NC}"
        read -p "Press Enter after you've configured .env file..."
    else
        echo -e "${RED}❌ .env.example not found. Cannot create .env file.${NC}"
        exit 1
    fi
fi

echo -e "${BLUE}🔧 Building Docker images...${NC}"
docker-compose build

echo -e "${BLUE}🚀 Starting services...${NC}"
docker-compose up -d

echo -e "${BLUE}⏳ Waiting for services to be healthy...${NC}"
sleep 10

# Check service health
echo -e "${BLUE}🔍 Checking service health...${NC}"

services=("mongodb" "auth-service" "roadmap-api" "chatbot-service" "job-agent" "mentor-service" "project-service" "resume-parser" "subscription-service" "resources-service" "nginx")

for service in "${services[@]}"; do
    status=$(docker inspect --format='{{.State.Health.Status}}' pathwise-${service} 2>/dev/null || echo "no-health-check")
    
    if [ "$status" = "healthy" ] || [ "$status" = "no-health-check" ]; then
        if docker ps | grep -q pathwise-${service}; then
            echo -e "${GREEN}✅ ${service} is running${NC}"
        else
            echo -e "${RED}❌ ${service} is not running${NC}"
        fi
    else
        echo -e "${YELLOW}⚠️  ${service} status: ${status}${NC}"
    fi
done

echo ""
echo -e "${GREEN}🎉 Deployment Complete!${NC}"
echo ""
echo -e "${BLUE}📊 Service URLs:${NC}"
echo -e "  ${GREEN}Auth Service:${NC}         http://localhost/api/auth"
echo -e "  ${GREEN}Roadmap API:${NC}          http://localhost/api/roadmap"
echo -e "  ${GREEN}Chatbot Service:${NC}      http://localhost/api/chatbot"
echo -e "  ${GREEN}Job Agent:${NC}            http://localhost/api/jobs"
echo -e "  ${GREEN}Mentor Service:${NC}       http://localhost/api/mentors"
echo -e "  ${GREEN}Project Service:${NC}      http://localhost/api/projects"
echo -e "  ${GREEN}Resume Parser:${NC}        http://localhost/api/resume"
echo -e "  ${GREEN}Subscription Service:${NC} http://localhost/api/subscription"
echo -e "  ${GREEN}Resources Service:${NC}    http://localhost/api/resources"
echo -e "  ${GREEN}Health Check:${NC}         http://localhost/health"
echo ""
echo -e "${BLUE}📝 Useful Commands:${NC}"
echo -e "  ${YELLOW}View logs:${NC}           docker-compose logs -f"
echo -e "  ${YELLOW}Stop services:${NC}       docker-compose down"
echo -e "  ${YELLOW}Restart services:${NC}    docker-compose restart"
echo -e "  ${YELLOW}View status:${NC}         docker-compose ps"
echo ""
echo -e "${BLUE}🔗 MongoDB Connection:${NC}"
echo -e "  ${GREEN}Internal:${NC} mongodb://mongodb:27017/pathwise"
echo -e "  ${GREEN}External:${NC} mongodb://localhost:27017/pathwise"
echo ""

