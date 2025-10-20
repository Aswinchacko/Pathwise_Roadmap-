# 🚀 START HERE - Groq Chatbot Setup

## ✅ What's Been Created

A **complete ChatGPT-like chatbot microservice** powered by Groq API that can answer **ANY** question.

## 🎯 Quick Start (3 Steps)

### Step 1: Start the Chatbot Service

```bash
start_groq_chatbot.bat
```

**Important**: Keep this terminal window open!

### Step 2: Start the Dashboard

In a **NEW** terminal:

```bash
start_frontend.bat
```

### Step 3: Use It!

1. Open your browser: **http://localhost:5173**
2. Navigate to the **Chatbot** page
3. Start asking anything!

## 🧪 Test It First

Before using the dashboard, test if the service works:

```bash
test_groq_chatbot_quick.bat
```

## 📁 Files Created

### Service Files (chatbot_service/)
- `main.py` - Core chatbot service with Groq API
- `start_server.py` - Startup script
- `test_chatbot.py` - Test suite
- `requirements.txt` - Dependencies
- `.env` - Configuration (Groq API key)

### Startup Scripts (Root)
- `start_groq_chatbot.bat` - Start chatbot service
- `start_complete_chatbot_system.bat` - Start everything at once
- `test_groq_chatbot.bat` - Full tests
- `test_groq_chatbot_quick.bat` - Quick test

## 💡 What You Can Ask

**Technical**
- "What is machine learning?"
- "Explain Docker"
- "How does blockchain work?"

**Coding**
- "Write a Python function to sort"
- "Debug this code: [code]"
- "Explain recursion"

**Career**
- "How to become a data scientist?"
- "What skills for DevOps?"
- "Learning roadmap for AI"

**Anything else!**
- "Explain quantum physics"
- "How does photosynthesis work?"
- "What is the meaning of life?"

## 🔧 Troubleshooting

### Service won't start?

1. Check if port 8004 is available:
   ```bash
   netstat -ano | findstr :8004
   ```

2. Make sure `.env` file exists in `chatbot_service/`:
   ```bash
   dir chatbot_service\.env
   ```

3. Check Groq API key in `.env`:
   Open `chatbot_service/.env` and verify `GROQ_API_KEY` is set

### No response from bot?

1. Check service health:
   ```
   http://localhost:8004/health
   ```
   Should show: `"groq_api": "configured"`

2. If it shows `"not_configured"`:
   - Edit `chatbot_service/.env`
   - Add/verify: `GROQ_API_KEY=your_key_here`
   - Restart the service

### Frontend can't connect?

1. Make sure chatbot service is running (Step 1)
2. Check it's responding: http://localhost:8004/health
3. Clear browser cache (Ctrl+F5)

## 📡 API Endpoints

- **Health**: http://localhost:8004/health
- **API Docs**: http://localhost:8004/docs
- **Chat**: POST http://localhost:8004/chat

## 🎨 Features

✅ **ChatGPT-like** - Answers anything
✅ **Context-aware** - Remembers conversation
✅ **Fast** - Powered by Groq API (Llama 3.3 70B)
✅ **Persistent** - Saves chat history to MongoDB
✅ **Multi-user** - Supports multiple users
✅ **Beautiful UI** - Already integrated with dashboard

## 📚 Documentation

- **Quick Reference**: `GROQ_CHATBOT_QUICK_REFERENCE.md`
- **Complete Guide**: `GROQ_CHATBOT_COMPLETE.md`
- **Setup Guide**: `GROQ_CHATBOT_SETUP.md`
- **Service README**: `chatbot_service/README.md`

## 🎉 You're Ready!

Just run:

```bash
start_groq_chatbot.bat
```

Then in another terminal:

```bash
start_frontend.bat
```

Open **http://localhost:5173** and start chatting! 🤖💬

---

## ⚡ One-Command Start

Want to start everything at once?

```bash
start_complete_chatbot_system.bat
```

This will:
1. Install all dependencies
2. Start the chatbot service
3. Start the dashboard
4. Open in two separate windows

---

## 🆘 Need Help?

1. **Test the service**: `test_groq_chatbot_quick.bat`
2. **Check health**: http://localhost:8004/health
3. **View API docs**: http://localhost:8004/docs
4. **Check logs**: Look at the terminal where service is running

---

**Built with**: FastAPI + Groq API + MongoDB + React
**Model**: Llama 3.3 70B Versatile
**Status**: ✅ READY TO USE

