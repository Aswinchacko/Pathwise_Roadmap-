# 🐳 PathWise Docker Deployment Guide

Complete guide for deploying PathWise microservices using Docker.

---

## 📋 Table of Contents

1. [Quick Start](#quick-start)
2. [Local Development](#local-development)
3. [Production Deployment](#production-deployment)
4. [Service Architecture](#service-architecture)
5. [Environment Configuration](#environment-configuration)
6. [Troubleshooting](#troubleshooting)
7. [Maintenance](#maintenance)

---

## 🚀 Quick Start

### Prerequisites

- Docker 20.10+
- Docker Compose 2.0+
- 4GB RAM minimum
- 20GB disk space

### Deploy in 3 Steps

```bash
# 1. Clone repository
git clone https://github.com/yourusername/pathwise.git
cd pathwise

# 2. Configure environment
cp .env.example .env
nano .env  # Edit with your credentials

# 3. Deploy
chmod +x deploy.sh
./deploy.sh
```

**That's it!** All services will be running at `http://localhost`

---

## 💻 Local Development

### Start All Services

```bash
docker-compose up -d
```

### View Logs

```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f roadmap-api
docker-compose logs -f chatbot-service
```

### Stop Services

```bash
docker-compose down
```

### Rebuild After Code Changes

```bash
docker-compose up -d --build [service-name]
```

### Access MongoDB

```bash
# Using Docker
docker exec -it pathwise-mongodb mongosh -u admin -p changeme

# Or from host
mongosh mongodb://admin:changeme@localhost:27017/pathwise?authSource=admin
```

---

## 🌐 Production Deployment

### DigitalOcean Droplet

**1. Create Droplet**
- Ubuntu 22.04 LTS
- $12/month (2GB RAM) minimum
- Add SSH key

**2. SSH into Server**

```bash
ssh root@your-server-ip
```

**3. Clone and Deploy**

```bash
# Clone repository
git clone https://github.com/yourusername/pathwise.git
cd pathwise

# Copy and configure environment
cp .env.example .env
nano .env  # Add production credentials

# Run production deployment
chmod +x deploy-production.sh
./deploy-production.sh
```

**4. Configure Domain (Optional)**

```bash
# Point your domain to server IP
# Then run:
certbot --nginx -d api.yourdomain.com
```

### AWS EC2

**1. Launch Instance**
- Ubuntu 22.04 LTS
- t3.medium or larger
- Security Group: Allow ports 22, 80, 443

**2. Deploy**

```bash
ssh -i your-key.pem ubuntu@ec2-instance-ip
sudo su
# Follow DigitalOcean steps above
```

### Google Cloud Platform

**1. Create VM**

```bash
gcloud compute instances create pathwise-server \
  --machine-type=e2-medium \
  --image-family=ubuntu-2204-lts \
  --image-project=ubuntu-os-cloud \
  --boot-disk-size=50GB
```

**2. Deploy**

```bash
gcloud compute ssh pathwise-server
sudo su
# Follow deployment steps
```

---

## 🏗️ Service Architecture

```
┌─────────────────────────────────────────────────┐
│  Nginx Reverse Proxy (Port 80/443)             │
│  http://your-domain.com                         │
└─────────────┬───────────────────────────────────┘
              │
    ┌─────────┴─────────┐
    │                   │
┌───▼────────────┐ ┌───▼────────────┐
│  Auth Service  │ │  Roadmap API   │
│  Port 5000     │ │  Port 8000     │
└────────────────┘ └────────────────┘
         │                 │
    ┌────┴────┬───────────┴────┬───────────┐
┌───▼────┐ ┌─▼────┐ ┌─────▼──┐ ┌────▼─────┐
│Chatbot │ │Jobs  │ │Mentors │ │Projects  │
│8004    │ │5007  │ │8006    │ │8003      │
└────────┘ └──────┘ └────────┘ └──────────┘
         │                 │
    ┌────┴────┬───────────┴────┐
┌───▼────┐ ┌─▼────────┐ ┌──▼────────┐
│Resume  │ │Subscribe │ │Resources  │
│8007    │ │8005      │ │8001       │
└────────┘ └──────────┘ └───────────┘
         │
    ┌────▼────────────┐
    │  MongoDB        │
    │  Port 27017     │
    └─────────────────┘
```

---

## ⚙️ Environment Configuration

### Required Variables

```env
# MongoDB
MONGO_USERNAME=admin
MONGO_PASSWORD=your-secure-password

# JWT
JWT_SECRET=your-super-secret-jwt-key-32-chars-min

# Frontend
FRONTEND_URL=https://your-app.vercel.app

# AI Services
GROQ_API_KEY=your-groq-api-key
```

### Optional Variables

```env
# Job Search APIs
RAPIDAPI_KEY=your-rapidapi-key
ADZUNA_APP_ID=your-adzuna-app-id
ADZUNA_API_KEY=your-adzuna-api-key

# Payment
RAZORPAY_KEY_ID=your-razorpay-key-id
RAZORPAY_KEY_SECRET=your-razorpay-key-secret

# OAuth
GITHUB_CLIENT_ID=your-github-id
GITHUB_CLIENT_SECRET=your-github-secret
LINKEDIN_CLIENT_ID=your-linkedin-id
LINKEDIN_CLIENT_SECRET=your-linkedin-secret
GOOGLE_CLIENT_ID=your-google-id
GOOGLE_CLIENT_SECRET=your-google-secret
```

---

## 🔧 Troubleshooting

### Service Won't Start

```bash
# Check logs
docker-compose logs [service-name]

# Check if port is already in use
netstat -tulpn | grep [port]

# Restart specific service
docker-compose restart [service-name]
```

### MongoDB Connection Failed

```bash
# Check MongoDB is running
docker ps | grep mongodb

# Check MongoDB logs
docker-compose logs mongodb

# Restart MongoDB
docker-compose restart mongodb
```

### Out of Memory

```bash
# Check memory usage
docker stats

# Increase swap space
sudo fallocate -l 4G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
```

### Service Health Check Failing

```bash
# Check individual service health
curl http://localhost/health
curl http://localhost:5000/health
curl http://localhost:8000/health

# Rebuild unhealthy service
docker-compose up -d --build --force-recreate [service-name]
```

### Nginx 502 Bad Gateway

```bash
# Check if backend services are running
docker-compose ps

# Check nginx logs
docker-compose logs nginx

# Restart nginx
docker-compose restart nginx
```

---

## 🛠️ Maintenance

### Update Services

```bash
# Pull latest code
git pull origin main

# Rebuild and restart
docker-compose up -d --build
```

### Backup MongoDB

```bash
# Backup
docker exec pathwise-mongodb mongodump \
  --out /data/backup \
  --username admin \
  --password changeme \
  --authenticationDatabase admin

# Restore
docker exec pathwise-mongodb mongorestore \
  /data/backup \
  --username admin \
  --password changeme \
  --authenticationDatabase admin
```

### Clean Up Docker

```bash
# Remove unused images
docker image prune -a

# Remove unused volumes
docker volume prune

# Full cleanup
docker system prune -a --volumes
```

### Monitor Resource Usage

```bash
# Real-time stats
docker stats

# Service-specific stats
docker stats pathwise-roadmap pathwise-chatbot
```

### View All Service URLs

```bash
echo "Auth:         http://localhost/api/auth"
echo "Roadmap:      http://localhost/api/roadmap"
echo "Chatbot:      http://localhost/api/chatbot"
echo "Jobs:         http://localhost/api/jobs"
echo "Mentors:      http://localhost/api/mentors"
echo "Projects:     http://localhost/api/projects"
echo "Resume:       http://localhost/api/resume"
echo "Subscription: http://localhost/api/subscription"
echo "Resources:    http://localhost/api/resources"
```

---

## 📊 Service Ports

| Service | Internal Port | External Access |
|---------|--------------|-----------------|
| MongoDB | 27017 | localhost:27017 |
| Auth | 5000 | /api/auth |
| Roadmap | 8000 | /api/roadmap |
| Chatbot | 8004 | /api/chatbot |
| Jobs | 5007 | /api/jobs |
| Mentors | 8006 | /api/mentors |
| Projects | 8003 | /api/projects |
| Resume | 8007 | /api/resume |
| Subscription | 8005 | /api/subscription |
| Resources | 8001 | /api/resources |
| Nginx | 80/443 | localhost |

---

## 🔐 Security Best Practices

1. **Change default passwords** in `.env`
2. **Use strong JWT secret** (32+ characters)
3. **Enable firewall** on production server
4. **Setup SSL** with Let's Encrypt
5. **Regular backups** of MongoDB
6. **Keep Docker updated**
7. **Monitor logs** for suspicious activity
8. **Limit MongoDB access** to internal network
9. **Use environment-specific** `.env` files
10. **Never commit** `.env` to git

---

## 📝 Quick Commands Reference

```bash
# Start all services
docker-compose up -d

# Stop all services
docker-compose down

# View logs
docker-compose logs -f

# Restart a service
docker-compose restart [service-name]

# Rebuild a service
docker-compose up -d --build [service-name]

# Check service status
docker-compose ps

# Access MongoDB
docker exec -it pathwise-mongodb mongosh

# View resource usage
docker stats

# Remove all containers and volumes
docker-compose down -v
```

---

## 🆘 Support

- **Issues:** [GitHub Issues](https://github.com/yourusername/pathwise/issues)
- **Docs:** [Full Documentation](./docs/)
- **Email:** support@pathwise.com

---

## 📄 License

MIT License - See LICENSE file for details

---

**Ready to deploy? Run `./deploy.sh` and you're live in minutes!** 🚀

