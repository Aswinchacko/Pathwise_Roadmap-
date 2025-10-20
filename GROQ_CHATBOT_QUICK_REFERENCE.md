# 🤖 Groq Chatbot - Quick Reference Card

## 🚀 Start Commands

```bash
# Start everything (recommended)
start_complete_chatbot_system.bat

# Or start individually:
start_groq_chatbot.bat      # Just the chatbot service
start_frontend.bat           # Just the dashboard
```

## 🧪 Test Commands

```bash
test_groq_chatbot_quick.bat  # Quick test (30 seconds)
test_groq_chatbot.bat        # Full test suite (2-3 minutes)
```

## 🌐 URLs

| Service | URL | Purpose |
|---------|-----|---------|
| Dashboard | http://localhost:5173 | Main UI - Go to Chatbot page |
| Chatbot API | http://localhost:8004 | Backend service |
| API Docs | http://localhost:8004/docs | Interactive API documentation |
| Health Check | http://localhost:8004/health | Service status |

## 📡 Quick API Examples

### Send Message
```bash
curl -X POST http://localhost:8004/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello!", "user_id": "test"}'
```

### Get Chats
```bash
curl http://localhost:8004/chats/test_user
```

## 💬 Example Questions to Try

**Technical**
- "What is machine learning?"
- "Explain Docker containers"
- "How does blockchain work?"

**Coding**
- "Write a Python function to sort a list"
- "Debug this code: [paste code]"
- "Explain recursion with an example"

**Career**
- "How do I become a data scientist?"
- "What skills for DevOps?"
- "Give me a learning roadmap"

**General**
- "Explain quantum physics simply"
- "What is the meaning of life?"
- "How does photosynthesis work?"

## 🔧 Configuration Files

| File | Purpose |
|------|---------|
| `chatbot_service/.env` | API keys and configuration |
| `chatbot_service/main.py` | Core service code |
| `dashboard/src/services/chatbotService.js` | Frontend API client |

## 🐛 Quick Troubleshooting

| Problem | Solution |
|---------|----------|
| Service won't start | Check if port 8004 is in use |
| No AI response | Check Groq API key in `.env` |
| Frontend can't connect | Make sure service is running |
| Slow responses | Normal! API takes 1-5 seconds |

## 📊 Service Status

Check health:
```bash
curl http://localhost:8004/health
```

Expected response:
```json
{
  "status": "healthy",
  "mongodb": "connected/disconnected",
  "groq_api": "configured"
}
```

## 🎯 Key Features

✅ **ChatGPT-like** - Can answer anything
✅ **Context-aware** - Remembers conversation
✅ **Fast** - Powered by Groq API
✅ **Persistent** - Saves chat history
✅ **Multi-user** - Supports multiple users
✅ **Production-ready** - Error handling, logging

## 📁 Important Files

```
chatbot_service/
  main.py          ← Core service
  .env             ← Your API key
  start_server.py  ← Startup script

Root:
  start_complete_chatbot_system.bat  ← Start everything
  GROQ_CHATBOT_COMPLETE.md           ← Full docs
```

## 🎨 Customization Quick Tips

**Change AI Model** (in `main.py`):
```python
"model": "llama-3.3-70b-versatile"  # Current - best quality
"model": "llama-3.1-8b-instant"     # Faster, less detail
```

**Adjust Response Length** (in `main.py`):
```python
max_tokens=2000  # Current - detailed
max_tokens=1000  # Shorter
max_tokens=4000  # Longer
```

**Change Temperature** (in `main.py`):
```python
temperature=0.7  # Current - balanced
temperature=0.3  # More focused
temperature=1.0  # More creative
```

## 🚨 Common Issues

**"Cannot connect to service"**
→ Run: `start_groq_chatbot.bat`

**"Groq API key not configured"**
→ Check: `chatbot_service/.env` has `GROQ_API_KEY`

**"Request timeout"**
→ Normal for complex questions, wait or increase timeout

**"Rate limit exceeded"**
→ Wait a moment, Groq API has rate limits

## 📱 Access Points

**For Users:**
1. Open http://localhost:5173
2. Click on "Chatbot" in navigation
3. Start chatting!

**For Developers:**
1. API Docs: http://localhost:8004/docs
2. Health: http://localhost:8004/health
3. Test: `test_groq_chatbot_quick.bat`

## 🎉 Success Indicators

✅ Terminal shows "Uvicorn running on..."
✅ Health check returns "healthy"
✅ Dashboard loads without errors
✅ Can send message and get response
✅ Response is relevant and intelligent

## 📞 Quick Help

**Service not starting?**
```bash
cd chatbot_service
python start_server.py
```

**Want to see logs?**
Check the terminal where service is running

**Need to reset?**
Close all terminals, restart with:
```bash
start_complete_chatbot_system.bat
```

## 💡 Pro Tips

1. **Keep conversation focused** - Bot maintains context
2. **Be specific** - Better questions = better answers
3. **Use follow-ups** - "Explain that more" works!
4. **Try different topics** - Bot knows many subjects
5. **Check API docs** - Interactive docs are helpful

---

## 🎊 You're Ready!

Run this ONE command:
```bash
start_complete_chatbot_system.bat
```

Then open: **http://localhost:5173**

Start asking anything! 🚀

