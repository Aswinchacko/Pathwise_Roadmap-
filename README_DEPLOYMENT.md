# 🚀 PathWise - Complete Deployment Guide

## Quick Deployment (3 Commands)

```bash
# 1. Setup environment
cp env.template .env
nano .env  # Add your API keys

# 2. Deploy
chmod +x deploy.sh
./deploy.sh

# 3. Access
# API: http://localhost
# Services are running!
```

---

## 📦 What's Included

### ✅ 9 Microservices
- **Auth Service** (Node.js) - Authentication & Authorization
- **Roadmap API** (Python) - Learning path generation
- **Chatbot Service** (Python) - AI-powered assistant
- **Job Agent** (Python) - Job search & matching
- **Mentor Service** (Python) - Mentor recommendations
- **Project Service** (Python) - Project recommendations
- **Resume Parser** (Python) - Resume analysis
- **Subscription Service** (Python) - Payment handling
- **Resources Service** (Node.js) - Learning resources

### ✅ Infrastructure
- **MongoDB** - Database
- **Nginx** - Reverse proxy & load balancer

---

## 🏗️ Architecture

```
Internet
   ↓
Nginx (Port 80/443)
   ↓
┌─────────────────────────────────────┐
│  Microservices                      │
│  ├─ Auth (5000)                     │
│  ├─ Roadmap (8000)                  │
│  ├─ Chatbot (8004)                  │
│  ├─ Jobs (5007)                     │
│  ├─ Mentors (8006)                  │
│  ├─ Projects (8003)                 │
│  ├─ Resume (8007)                   │
│  ├─ Subscription (8005)             │
│  └─ Resources (8001)                │
└─────────────────────────────────────┘
   ↓
MongoDB (27017)
```

---

## 📋 Prerequisites

- Docker 20.10+
- Docker Compose 2.0+
- 4GB RAM (8GB recommended)
- 20GB disk space

### Install Docker

**Ubuntu/Debian:**
```bash
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
```

**Windows:** Download [Docker Desktop](https://www.docker.com/products/docker-desktop)

**Mac:** Download [Docker Desktop](https://www.docker.com/products/docker-desktop)

---

## 🚀 Deployment Options

### Option 1: Local Development

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

### Option 2: DigitalOcean Droplet ($12/month)

```bash
# 1. Create Ubuntu 22.04 droplet
# 2. SSH into server
ssh root@your-droplet-ip

# 3. Deploy
git clone https://github.com/yourusername/pathwise.git
cd pathwise
cp env.template .env
nano .env  # Configure

chmod +x deploy-production.sh
./deploy-production.sh
```

### Option 3: AWS EC2

```bash
# 1. Launch t3.medium instance (Ubuntu 22.04)
# 2. Configure security group (ports 22, 80, 443)
# 3. Deploy
ssh -i your-key.pem ubuntu@ec2-ip
sudo su
# Follow DigitalOcean steps
```

### Option 4: Production with Resource Limits

```bash
# Use production compose file
docker-compose -f docker-compose.prod.yml up -d
```

---

## ⚙️ Configuration

### 1. Copy Environment Template

```bash
cp env.template .env
```

### 2. Edit `.env` File

**Required:**
```env
MONGO_USERNAME=admin
MONGO_PASSWORD=YourSecurePassword123!
JWT_SECRET=your-super-secret-jwt-key-32-chars-minimum
GROQ_API_KEY=gsk_your_groq_api_key
FRONTEND_URL=https://your-app.vercel.app
```

**Optional (for full features):**
```env
RAPIDAPI_KEY=your_rapidapi_key
RAZORPAY_KEY_ID=rzp_test_your_key
GITHUB_CLIENT_ID=your_github_id
LINKEDIN_CLIENT_ID=your_linkedin_id
```

### 3. Get API Keys

- **GROQ_API_KEY:** https://console.groq.com
- **RAPIDAPI_KEY:** https://rapidapi.com/letscrape-6bRBa3QguO5/api/jsearch
- **RAZORPAY:** https://dashboard.razorpay.com/
- **GitHub OAuth:** https://github.com/settings/developers
- **LinkedIn OAuth:** https://www.linkedin.com/developers/

---

## 🎯 Service URLs

After deployment, access services at:

| Service | URL | Description |
|---------|-----|-------------|
| Health Check | `http://localhost/health` | System health |
| Auth | `http://localhost/api/auth` | Authentication |
| Roadmap | `http://localhost/api/roadmap` | Learning paths |
| Chatbot | `http://localhost/api/chatbot` | AI assistant |
| Jobs | `http://localhost/api/jobs` | Job search |
| Mentors | `http://localhost/api/mentors` | Find mentors |
| Projects | `http://localhost/api/projects` | Project ideas |
| Resume | `http://localhost/api/resume` | Parse resumes |
| Subscription | `http://localhost/api/subscription` | Payments |
| Resources | `http://localhost/api/resources` | Learning resources |

---

## 🔍 Verification

### Test All Services

```bash
# Health check
curl http://localhost/health

# Test auth service
curl http://localhost/api/auth/health

# Test roadmap
curl http://localhost/api/roadmap/health

# View all running containers
docker-compose ps
```

### Expected Output

```
NAME                    STATUS          PORTS
pathwise-auth           Up 2 minutes    0.0.0.0:5000->5000/tcp
pathwise-roadmap        Up 2 minutes    0.0.0.0:8000->8000/tcp
pathwise-chatbot        Up 2 minutes    0.0.0.0:8004->8004/tcp
pathwise-jobs           Up 2 minutes    0.0.0.0:5007->5007/tcp
pathwise-mentors        Up 2 minutes    0.0.0.0:8006->8006/tcp
pathwise-projects       Up 2 minutes    0.0.0.0:8003->8003/tcp
pathwise-resume         Up 2 minutes    0.0.0.0:8007->8007/tcp
pathwise-subscription   Up 2 minutes    0.0.0.0:8005->8005/tcp
pathwise-resources      Up 2 minutes    0.0.0.0:8001->8001/tcp
pathwise-mongodb        Up 2 minutes    0.0.0.0:27017->27017/tcp
pathwise-nginx          Up 2 minutes    0.0.0.0:80->80/tcp
```

---

## 🛠️ Common Commands

```bash
# Start services
docker-compose up -d

# Stop services
docker-compose down

# View logs (all services)
docker-compose logs -f

# View logs (specific service)
docker-compose logs -f roadmap-api

# Restart a service
docker-compose restart chatbot-service

# Rebuild and restart
docker-compose up -d --build roadmap-api

# Check resource usage
docker stats

# Access MongoDB
docker exec -it pathwise-mongodb mongosh -u admin -p yourpassword

# Remove everything (including data)
docker-compose down -v
```

---

## 🔧 Troubleshooting

### Service won't start

```bash
# Check logs
docker-compose logs [service-name]

# Check if port is in use
netstat -tulpn | grep [port]

# Force recreate
docker-compose up -d --force-recreate [service-name]
```

### MongoDB connection failed

```bash
# Check MongoDB logs
docker-compose logs mongodb

# Restart MongoDB
docker-compose restart mongodb

# Verify connection
docker exec -it pathwise-mongodb mongosh -u admin -p yourpassword
```

### Out of disk space

```bash
# Clean unused images
docker system prune -a

# Remove old volumes
docker volume prune
```

### Nginx 502 error

```bash
# Check backend services
docker-compose ps

# Restart nginx
docker-compose restart nginx

# Check nginx logs
docker-compose logs nginx
```

---

## 📊 Monitoring

### View Resource Usage

```bash
docker stats
```

### Check Service Health

```bash
# Create health check script
cat > check-health.sh << 'EOF'
#!/bin/bash
services=("auth" "roadmap" "chatbot" "jobs" "mentors" "projects" "resume" "subscription" "resources")
for service in "${services[@]}"; do
  status=$(curl -s -o /dev/null -w "%{http_code}" http://localhost/api/$service/health)
  if [ "$status" = "200" ]; then
    echo "✅ $service: healthy"
  else
    echo "❌ $service: unhealthy ($status)"
  fi
done
EOF

chmod +x check-health.sh
./check-health.sh
```

---

## 🔐 Production Security

### 1. Setup Firewall

```bash
ufw allow 22/tcp
ufw allow 80/tcp
ufw allow 443/tcp
ufw enable
```

### 2. Setup SSL (Let's Encrypt)

```bash
# Install certbot
apt install certbot python3-certbot-nginx -y

# Get certificate
certbot --nginx -d api.yourdomain.com

# Auto-renewal
certbot renew --dry-run
```

### 3. Secure MongoDB

```bash
# Change default password in .env
MONGO_PASSWORD=$(openssl rand -base64 32)

# Restrict MongoDB to internal network only
# Edit docker-compose.yml - remove external port exposure
```

---

## 💾 Backup & Restore

### Backup MongoDB

```bash
# Create backup
docker exec pathwise-mongodb mongodump \
  --out /backup \
  --username admin \
  --password yourpassword \
  --authenticationDatabase admin

# Copy backup to host
docker cp pathwise-mongodb:/backup ./backup-$(date +%Y%m%d)
```

### Restore MongoDB

```bash
# Copy backup to container
docker cp ./backup pathwise-mongodb:/restore

# Restore
docker exec pathwise-mongodb mongorestore \
  /restore \
  --username admin \
  --password yourpassword \
  --authenticationDatabase admin
```

---

## 🔄 Updates & Maintenance

### Update Services

```bash
# Pull latest code
git pull origin main

# Rebuild and restart
docker-compose up -d --build

# Or rebuild specific service
docker-compose up -d --build roadmap-api
```

### Clean Up

```bash
# Remove unused images
docker image prune -a

# Remove stopped containers
docker container prune

# Full cleanup (careful!)
docker system prune -a --volumes
```

---

## 📈 Scaling

### Scale Individual Services

```bash
# Scale chatbot to 3 instances
docker-compose up -d --scale chatbot-service=3

# Scale job agent to 2 instances
docker-compose up -d --scale job-agent=2
```

### Production Scaling Options

1. **Vertical:** Upgrade server (more RAM/CPU)
2. **Horizontal:** Multiple servers with load balancer
3. **Kubernetes:** For enterprise-scale deployment

---

## 📝 Environment Variables Reference

See `env.template` for all available variables and descriptions.

**Priority:** Required > Recommended > Optional

---

## 🆘 Support

- **Documentation:** [DOCKER_DEPLOYMENT.md](./DOCKER_DEPLOYMENT.md)
- **Issues:** GitHub Issues
- **Email:** support@pathwise.com

---

## ✅ Pre-Deployment Checklist

- [ ] Docker & Docker Compose installed
- [ ] `.env` file created and configured
- [ ] All API keys obtained
- [ ] Firewall configured (if production)
- [ ] Domain DNS configured (if using SSL)
- [ ] MongoDB backup strategy planned
- [ ] Monitoring tools setup

---

## 🎉 Success!

If you see all services healthy, you're ready!

**Next Steps:**
1. Configure Vercel frontend with backend URL
2. Test all endpoints
3. Setup monitoring & alerts
4. Plan backup strategy
5. Go live! 🚀

---

**Happy Deploying!** 🐳

