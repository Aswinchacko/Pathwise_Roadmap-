# ⚡ PathWise - Quick Start Guide

Deploy your entire microservices stack in **5 minutes**!

---

## 🚀 3-Step Deployment

### Step 1: Setup Environment

```bash
cp env.template .env
nano .env  # Or use any text editor
```

**Add these required values:**
```env
MONGO_PASSWORD=YourSecurePassword123
JWT_SECRET=your-32-character-secret-key-here
GROQ_API_KEY=gsk_your_groq_api_key_here
FRONTEND_URL=https://your-app.vercel.app
```

### Step 2: Deploy

```bash
chmod +x deploy.sh
./deploy.sh
```

Wait 2-3 minutes for all services to start.

### Step 3: Verify

```bash
# Test deployment
chmod +x test-deployment.sh
./test-deployment.sh

# Or manually check
curl http://localhost/health
```

**That's it! All 9 services are running!** ✅

---

## 📋 What Just Happened?

You deployed:
- ✅ 9 microservices (Python FastAPI + Node.js)
- ✅ MongoDB database
- ✅ Nginx reverse proxy
- ✅ Health monitoring
- ✅ Auto-restart on failure

---

## 🔗 Access Your Services

All services available at: **http://localhost**

| Endpoint | Service |
|----------|---------|
| `/api/auth` | Authentication |
| `/api/roadmap` | Learning paths |
| `/api/chatbot` | AI assistant |
| `/api/jobs` | Job search |
| `/api/mentors` | Find mentors |
| `/api/projects` | Project ideas |
| `/api/resume` | Parse resumes |
| `/api/subscription` | Payments |
| `/api/resources` | Learning resources |

---

## 🛠️ Common Commands

```bash
# View all services
docker-compose ps

# View logs (all services)
docker-compose logs -f

# View logs (one service)
docker-compose logs -f roadmap-api

# Restart a service
docker-compose restart chatbot-service

# Stop everything
docker-compose down

# Start everything
docker-compose up -d
```

---

## 🌐 Deploy to Production

### DigitalOcean ($12/month)

```bash
# 1. Create Ubuntu 22.04 droplet
# 2. SSH in
ssh root@your-droplet-ip

# 3. Deploy
git clone https://github.com/yourusername/pathwise.git
cd pathwise
cp env.template .env
nano .env

chmod +x deploy-production.sh
./deploy-production.sh
```

### Update Vercel Frontend

Add these environment variables in Vercel:

```env
VITE_API_URL=http://your-server-ip
# Or with domain:
VITE_API_URL=https://api.yourdomain.com
```

---

## 🔧 Troubleshooting

**Services won't start?**
```bash
docker-compose logs [service-name]
```

**Port already in use?**
```bash
docker-compose down
sudo lsof -i :80  # Check what's using port 80
```

**Out of memory?**
```bash
docker stats  # Check resource usage
```

**Need to reset everything?**
```bash
docker-compose down -v  # Removes data too
./deploy.sh
```

---

## 📖 Full Documentation

- [Complete Deployment Guide](./README_DEPLOYMENT.md)
- [Docker Guide](./DOCKER_DEPLOYMENT.md)
- [Architecture Diagram](./PROJECT_FLOW.txt)

---

## 🆘 Need Help?

1. Check logs: `docker-compose logs -f`
2. Run health check: `./test-deployment.sh`
3. See [Troubleshooting Guide](./DOCKER_DEPLOYMENT.md#troubleshooting)

---

## ✅ Next Steps

1. ✅ Services running locally
2. 🔜 Deploy to production server
3. 🔜 Configure domain & SSL
4. 🔜 Update Vercel frontend
5. 🔜 Go live!

---

**Ready to deploy? Just run `./deploy.sh`!** 🎉

