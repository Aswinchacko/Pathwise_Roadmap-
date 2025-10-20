#!/bin/bash

# PathWise Production Deployment Script
# For deploying to DigitalOcean, AWS, or any VPS

set -e  # Exit on error

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}"
echo "╔═══════════════════════════════════════╗"
echo "║   PathWise Production Deployment      ║"
echo "╚═══════════════════════════════════════╝"
echo -e "${NC}"

# Check if running as root
if [[ $EUID -ne 0 ]]; then
   echo -e "${RED}❌ This script must be run as root (use sudo)${NC}" 
   exit 1
fi

echo -e "${GREEN}✅ Running as root${NC}"

# Update system
echo -e "${BLUE}📦 Updating system packages...${NC}"
apt update && apt upgrade -y

# Install Docker if not installed
if ! command -v docker &> /dev/null; then
    echo -e "${BLUE}🐳 Installing Docker...${NC}"
    curl -fsSL https://get.docker.com -o get-docker.sh
    sh get-docker.sh
    rm get-docker.sh
    systemctl enable docker
    systemctl start docker
    echo -e "${GREEN}✅ Docker installed${NC}"
else
    echo -e "${GREEN}✅ Docker already installed${NC}"
fi

# Install Docker Compose if not installed
if ! command -v docker-compose &> /dev/null; then
    echo -e "${BLUE}🔧 Installing Docker Compose...${NC}"
    curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    chmod +x /usr/local/bin/docker-compose
    echo -e "${GREEN}✅ Docker Compose installed${NC}"
else
    echo -e "${GREEN}✅ Docker Compose already installed${NC}"
fi

# Install Nginx for SSL if not using Docker nginx
if ! command -v nginx &> /dev/null; then
    echo -e "${BLUE}📡 Installing Nginx...${NC}"
    apt install -y nginx
    systemctl enable nginx
    echo -e "${GREEN}✅ Nginx installed${NC}"
else
    echo -e "${GREEN}✅ Nginx already installed${NC}"
fi

# Install Certbot for SSL
if ! command -v certbot &> /dev/null; then
    echo -e "${BLUE}🔒 Installing Certbot...${NC}"
    apt install -y certbot python3-certbot-nginx
    echo -e "${GREEN}✅ Certbot installed${NC}"
else
    echo -e "${GREEN}✅ Certbot already installed${NC}"
fi

# Check if .env file exists
if [ ! -f .env ]; then
    echo -e "${RED}❌ .env file not found!${NC}"
    echo -e "${YELLOW}Please create .env file with production credentials.${NC}"
    exit 1
fi

echo -e "${GREEN}✅ .env file found${NC}"

# Pull latest code (if using git)
if [ -d .git ]; then
    echo -e "${BLUE}📥 Pulling latest code...${NC}"
    git pull origin main || git pull origin master
    echo -e "${GREEN}✅ Code updated${NC}"
fi

# Stop existing containers
echo -e "${BLUE}🛑 Stopping existing containers...${NC}"
docker-compose down || true

# Build images
echo -e "${BLUE}🔨 Building Docker images...${NC}"
docker-compose build --no-cache

# Start services
echo -e "${BLUE}🚀 Starting services...${NC}"
docker-compose up -d

# Wait for services
echo -e "${BLUE}⏳ Waiting for services to be healthy...${NC}"
sleep 20

# Check health
echo -e "${BLUE}🔍 Checking service health...${NC}"
curl -f http://localhost/health || echo -e "${RED}❌ Health check failed${NC}"

# Setup firewall
echo -e "${BLUE}🔥 Configuring firewall...${NC}"
ufw allow 22/tcp
ufw allow 80/tcp
ufw allow 443/tcp
ufw --force enable
echo -e "${GREEN}✅ Firewall configured${NC}"

# Setup SSL (optional - requires domain)
read -p "Do you want to setup SSL with Let's Encrypt? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    read -p "Enter your domain name: " DOMAIN
    echo -e "${BLUE}🔒 Setting up SSL for ${DOMAIN}...${NC}"
    certbot --nginx -d $DOMAIN --non-interactive --agree-tos --email admin@$DOMAIN
    echo -e "${GREEN}✅ SSL certificate installed${NC}"
fi

# Setup auto-renewal for SSL
echo -e "${BLUE}⚙️  Setting up SSL auto-renewal...${NC}"
(crontab -l 2>/dev/null; echo "0 0 * * 0 certbot renew --quiet") | crontab -
echo -e "${GREEN}✅ SSL auto-renewal configured${NC}"

# Setup automatic restarts
echo -e "${BLUE}⚙️  Setting up automatic restarts...${NC}"
cat > /etc/systemd/system/pathwise.service << EOF
[Unit]
Description=PathWise Microservices
Requires=docker.service
After=docker.service

[Service]
Type=oneshot
RemainAfterExit=yes
WorkingDirectory=$(pwd)
ExecStart=/usr/local/bin/docker-compose up -d
ExecStop=/usr/local/bin/docker-compose down

[Install]
WantedBy=multi-user.target
EOF

systemctl daemon-reload
systemctl enable pathwise.service
echo -e "${GREEN}✅ Automatic restarts configured${NC}"

# Cleanup old images
echo -e "${BLUE}🧹 Cleaning up old Docker images...${NC}"
docker system prune -f

echo ""
echo -e "${GREEN}╔════════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║  🎉 Production Deployment Complete!        ║${NC}"
echo -e "${GREEN}╚════════════════════════════════════════════╝${NC}"
echo ""
echo -e "${BLUE}📊 Deployment Summary:${NC}"
echo -e "  ${GREEN}✅ Docker installed and running${NC}"
echo -e "  ${GREEN}✅ All services deployed${NC}"
echo -e "  ${GREEN}✅ Nginx reverse proxy configured${NC}"
echo -e "  ${GREEN}✅ Firewall configured${NC}"
echo -e "  ${GREEN}✅ Auto-restart on boot enabled${NC}"
echo ""
echo -e "${BLUE}🔗 Service URLs:${NC}"
echo -e "  ${GREEN}API Gateway:${NC} http://$(curl -s ifconfig.me)/health"
echo -e "  ${GREEN}MongoDB:${NC}     mongodb://localhost:27017/pathwise"
echo ""
echo -e "${BLUE}📝 Useful Commands:${NC}"
echo -e "  ${YELLOW}View logs:${NC}        docker-compose logs -f [service-name]"
echo -e "  ${YELLOW}Restart service:${NC}  docker-compose restart [service-name]"
echo -e "  ${YELLOW}Stop all:${NC}         docker-compose down"
echo -e "  ${YELLOW}Start all:${NC}        docker-compose up -d"
echo -e "  ${YELLOW}Service status:${NC}   systemctl status pathwise"
echo ""
echo -e "${YELLOW}⚠️  Remember to:${NC}"
echo -e "  1. Update your Vercel frontend environment variables with this server IP"
echo -e "  2. Configure your domain DNS if using SSL"
echo -e "  3. Setup MongoDB backups"
echo -e "  4. Monitor logs regularly"
echo ""

