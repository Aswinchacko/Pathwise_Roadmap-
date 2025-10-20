# 🪟 PathWise - Windows Deployment Guide

Complete guide for deploying PathWise on Windows using Docker Desktop.

---

## 📋 Prerequisites

### 1. Install Docker Desktop

1. Download from: https://www.docker.com/products/docker-desktop
2. Install and restart your computer
3. Open Docker Desktop and wait for it to start

**Verify Installation:**
```powershell
docker --version
docker-compose --version
```

### 2. System Requirements

- Windows 10/11 Pro, Enterprise, or Education
- WSL 2 enabled
- 8GB RAM minimum (16GB recommended)
- 20GB free disk space
- Virtualization enabled in BIOS

---

## 🚀 Quick Deployment (Windows)

### Step 1: Setup Environment

```powershell
# In PowerShell or CMD
cd D:\PathWise

# Copy environment template
copy env.template .env

# Edit with Notepad
notepad .env
```

**Add these required values:**
```env
MONGO_PASSWORD=YourSecurePassword123
JWT_SECRET=your-32-character-secret-key-here
GROQ_API_KEY=gsk_your_groq_api_key_here
FRONTEND_URL=https://your-app.vercel.app
```

### Step 2: Deploy

**Using Batch File (Recommended):**
```cmd
deploy.bat
```

**Or Using Docker Compose Directly:**
```powershell
docker-compose up -d
```

### Step 3: Verify

```cmd
test-deployment.bat
```

**Or check manually:**
```powershell
# Check if all services are running
docker ps

# Test health endpoint
curl http://localhost/health
```

---

## 🛠️ Common Commands (Windows)

### Start Services
```cmd
docker-compose up -d
```

### Stop Services
```cmd
docker-compose down
```

### View Logs (All Services)
```cmd
docker-compose logs -f
```

### View Logs (Specific Service)
```cmd
docker-compose logs -f roadmap-api
```

### Restart Service
```cmd
docker-compose restart chatbot-service
```

### Check Status
```cmd
docker-compose ps
```

### Rebuild Service
```cmd
docker-compose up -d --build roadmap-api
```

### Access MongoDB
```cmd
docker exec -it pathwise-mongodb mongosh
```

---

## 🌐 Access Services

After deployment, access at:

| Service | URL |
|---------|-----|
| Health Check | http://localhost/health |
| Auth API | http://localhost/api/auth |
| Roadmap API | http://localhost/api/roadmap |
| Chatbot | http://localhost/api/chatbot |
| Jobs | http://localhost/api/jobs |
| Mentors | http://localhost/api/mentors |
| Projects | http://localhost/api/projects |
| Resume | http://localhost/api/resume |
| Subscription | http://localhost/api/subscription |
| Resources | http://localhost/api/resources |

Open in browser: http://localhost/health

---

## 🔧 Windows-Specific Troubleshooting

### Docker Desktop Not Starting

**Solution 1: Enable WSL 2**
```powershell
# Run as Administrator
wsl --install
wsl --set-default-version 2
```

**Solution 2: Enable Virtualization**
1. Restart computer
2. Enter BIOS (usually F2, F10, or Del)
3. Enable Intel VT-x or AMD-V
4. Save and restart

**Solution 3: Update Docker Desktop**
- Uninstall Docker Desktop
- Download latest version
- Reinstall

### Port Conflicts (Port 80 in use)

**Check what's using port 80:**
```powershell
netstat -ano | findstr :80
```

**Common culprits:**
- IIS (Internet Information Services)
- Skype
- VMware
- Other web servers

**Stop IIS:**
```powershell
# Run as Administrator
net stop http
```

**Or change nginx port in docker-compose.yml:**
```yaml
nginx:
  ports:
    - "8080:80"  # Changed from 80:80
```

Then access at: http://localhost:8080

### MongoDB Won't Start

**Check Docker resources:**
1. Docker Desktop → Settings → Resources
2. Increase RAM to at least 4GB
3. Increase disk space to 50GB

**Reset Docker:**
```powershell
# Stop all containers
docker-compose down

# Remove all volumes
docker-compose down -v

# Restart
deploy.bat
```

### "Drive not shared" Error

1. Docker Desktop → Settings → Resources → File Sharing
2. Add `D:\` drive (or your project location)
3. Apply & Restart

### Slow Performance

**Increase Docker Resources:**
1. Docker Desktop → Settings → Resources
2. CPUs: 4+
3. Memory: 8GB+
4. Disk: 50GB+
5. Apply & Restart

**Use WSL 2 Backend:**
1. Docker Desktop → Settings → General
2. Enable "Use WSL 2 based engine"
3. Apply & Restart

---

## 📊 Monitoring (Windows)

### View Resource Usage

**PowerShell:**
```powershell
docker stats
```

### Docker Desktop GUI
1. Open Docker Desktop
2. Click on "Containers" tab
3. View CPU, Memory usage

### Windows Task Manager
- Press `Ctrl + Shift + Esc`
- Look for "Docker Desktop" and "Vmmem" processes

---

## 🔐 Windows Firewall

### Allow Docker Ports

```powershell
# Run as Administrator
New-NetFirewallRule -DisplayName "Docker HTTP" -Direction Inbound -LocalPort 80 -Protocol TCP -Action Allow
New-NetFirewallRule -DisplayName "Docker HTTPS" -Direction Inbound -LocalPort 443 -Protocol TCP -Action Allow
```

---

## 📁 Windows File Paths

### Project Location
```
D:\PathWise\
```

### Docker Volumes
```
C:\ProgramData\Docker\volumes\
```

### Docker Desktop Data
```
%LOCALAPPDATA%\Docker\
```

### WSL 2 Location
```
\\wsl$\docker-desktop-data\
```

---

## 💾 Backup (Windows)

### Backup MongoDB

```cmd
REM Create backup directory
mkdir backups

REM Backup MongoDB
docker exec pathwise-mongodb mongodump --out /backup
docker cp pathwise-mongodb:/backup ./backups/backup-%date:~-4,4%%date:~-10,2%%date:~-7,2%
```

### Automated Backup Script

Create `backup.bat`:
```batch
@echo off
set BACKUP_DIR=backups\backup-%date:~-4,4%%date:~-10,2%%date:~-7,2%_%time:~0,2%%time:~3,2%%time:~6,2%
mkdir "%BACKUP_DIR%"
docker exec pathwise-mongodb mongodump --out /backup
docker cp pathwise-mongodb:/backup "%BACKUP_DIR%"
echo Backup created: %BACKUP_DIR%
```

Run daily with Task Scheduler.

---

## 🔄 Updates (Windows)

### Update Services

```cmd
REM Pull latest code
git pull origin main

REM Rebuild and restart
docker-compose up -d --build
```

### Update Docker Desktop

1. Docker Desktop → Check for updates
2. Download and install
3. Restart Docker Desktop

---

## 🆘 Getting Help

### View Logs
```cmd
docker-compose logs -f [service-name]
```

### Docker Desktop Logs
1. Docker Desktop → Troubleshoot
2. View logs
3. Download diagnostics

### Clean Everything
```cmd
REM Stop all containers
docker-compose down

REM Remove all Docker data
docker system prune -a --volumes

REM Restart Docker Desktop

REM Deploy again
deploy.bat
```

---

## ✅ Windows Deployment Checklist

- [ ] Docker Desktop installed and running
- [ ] WSL 2 enabled
- [ ] Virtualization enabled in BIOS
- [ ] `.env` file configured
- [ ] Ports 80 and 443 available
- [ ] At least 8GB RAM allocated to Docker
- [ ] Project drive shared with Docker
- [ ] Windows Firewall allows Docker
- [ ] All services deployed (`deploy.bat`)
- [ ] Health checks passing (`test-deployment.bat`)

---

## 🎯 Next Steps

1. ✅ Services running on Windows
2. 🔜 Test all endpoints
3. 🔜 Configure frontend (Vercel)
4. 🔜 Deploy backend to cloud (optional)
5. 🔜 Go live!

---

## 💡 Windows Pro Tips

### Use Windows Terminal
- Better than CMD
- Download from Microsoft Store
- Supports tabs and split panes

### Use VS Code
- Better terminal integration
- Docker extension available
- Easy to edit files

### Docker Desktop Dashboard
- Visual container management
- View logs in GUI
- Easy restart/stop controls

### PowerShell Profile
Add to `$PROFILE`:
```powershell
# Docker aliases
function docker-up { docker-compose up -d }
function docker-down { docker-compose down }
function docker-logs { docker-compose logs -f $args }
function docker-restart { docker-compose restart $args }
```

---

## 📝 Common Issues & Solutions

| Issue | Solution |
|-------|----------|
| Port 80 in use | Stop IIS or change port |
| Docker won't start | Enable WSL 2 / Virtualization |
| Slow performance | Increase Docker resources |
| Drive not shared | Add drive in Docker settings |
| Build fails | Check .dockerignore |
| Memory issues | Increase RAM in Docker settings |

---

**Ready to deploy on Windows? Run `deploy.bat`!** 🚀

