# PathWise Groq Chatbot - Complete Setup Guide 🤖

## What is This?

A **ChatGPT-like chatbot** powered by **Groq API** that can answer **ANYTHING**:
- Technical questions ✅
- Coding help ✅
- Career advice ✅
- Explanations ✅
- Project ideas ✅
- General knowledge ✅
- And much more!

## Quick Start (3 Steps)

### 1️⃣ Start the Chatbot Service

Run this command from the project root:

```bash
start_groq_chatbot.bat
```

**OR** the old command still works:

```bash
start_chatbot_system.bat
```

### 2️⃣ Start the Dashboard

In a new terminal:

```bash
start_frontend.bat
```

### 3️⃣ Open Your Browser

Navigate to: **http://localhost:5173**

Go to the **Chatbot** page and start asking anything!

## Test the Service

Want to make sure everything works?

```bash
test_groq_chatbot.bat
```

This will run comprehensive tests including:
- ✅ Health check
- ✅ Conversation flow
- ✅ Chat management
- ✅ Various question types

## Example Conversations

### Technical Questions
```
You: "What is machine learning?"
Bot: "Machine learning is a subset of artificial intelligence..."

You: "Explain it with an example"
Bot: "Sure! Imagine you want to teach a computer to recognize..."
```

### Coding Help
```
You: "Write a Python function to calculate fibonacci"
Bot: "Here's a Python function to calculate Fibonacci numbers:

def fibonacci(n):
    if n <= 0:
        return 0
    elif n == 1:
        return 1
    else:
        return fibonacci(n-1) + fibonacci(n-2)"
```

### Career Advice
```
You: "How do I become a full-stack developer?"
Bot: "To become a full-stack developer, you'll need to master both frontend and backend technologies..."
```

### Explanations
```
You: "Explain quantum computing in simple terms"
Bot: "Imagine regular computers as light switches that can be either ON or OFF..."
```

## Features

### 💬 Natural Conversations
- Maintains context throughout the conversation
- Remembers what you talked about
- Natural, intelligent responses

### 📁 Chat Management
- Create multiple chats
- Load previous conversations
- Edit chat titles
- Delete chats

### 🚀 Powered by Groq
- Uses Llama 3.3 70B Versatile model
- Fast responses (1-5 seconds)
- High-quality answers

### 💾 Persistent Storage
- Chats saved to MongoDB
- Automatic in-memory fallback
- History preserved across sessions

## API Endpoints

If you want to integrate programmatically:

### Send a Message
```http
POST http://localhost:8004/chat
Content-Type: application/json

{
  "message": "Your question here",
  "user_id": "your_user_id"
}
```

### Get Chat History
```http
GET http://localhost:8004/chats/{user_id}
```

### API Documentation
Full interactive docs: **http://localhost:8004/docs**

## Architecture

```
┌──────────────┐
│   Dashboard  │  ← You interact here
│  (React UI)  │
└──────┬───────┘
       │ HTTP
       │
┌──────▼────────────────┐
│  Chatbot Service      │
│  Port: 8004           │
│                       │
│  ┌────────────────┐  │
│  │  Groq API      │  │ ← AI Brain (Llama 3.3 70B)
│  │  Integration   │  │
│  └────────────────┘  │
└──────┬────────────────┘
       │
   ┌───▼────┐
   │MongoDB │ ← Chat storage
   └────────┘
```

## Troubleshooting

### ❌ "Service unavailable"

**Solution:** Make sure the chatbot service is running
```bash
start_groq_chatbot.bat
```

### ❌ "Groq API key not configured"

**Solution:** The `.env` file should already have your key. If not:
1. Open `chatbot_service/.env`
2. Add: `GROQ_API_KEY=your_key_here`

### ❌ "MongoDB connection failed"

**Don't worry!** The service automatically uses in-memory storage as fallback.

Your chats will work but won't persist across restarts.

To fix: Install and start MongoDB locally.

### ❌ Chat history not showing

**Solution:** 
1. Check browser console for errors
2. Make sure service is running: http://localhost:8004/health
3. Refresh the page

### ⏱️ Responses are slow

This is normal! The Groq API can take 1-5 seconds depending on:
- Question complexity
- API load
- Internet speed

## Configuration

### Change Port

Edit `chatbot_service/.env`:
```env
PORT=8004  # Change to your desired port
```

### Adjust Response Length

Edit `chatbot_service/main.py`:
```python
max_tokens=2000  # Increase for longer responses
```

### Change AI Model

Edit `chatbot_service/main.py`:
```python
"model": "llama-3.3-70b-versatile"  # Try other Groq models
```

Available models:
- `llama-3.3-70b-versatile` (Best for general chat)
- `llama-3.1-8b-instant` (Faster, less detailed)
- `mixtral-8x7b-32768` (Alternative option)

## Files Created

```
PathWise/
├── chatbot_service/
│   ├── main.py                  # Main service
│   ├── start_server.py          # Startup script
│   ├── test_chatbot.py          # Test suite
│   ├── requirements.txt         # Dependencies
│   ├── .env                     # Configuration
│   └── README.md                # Documentation
│
├── start_groq_chatbot.bat       # Start service (NEW)
├── start_chatbot_system.bat     # Start service (UPDATED)
├── test_groq_chatbot.bat        # Test service (NEW)
└── GROQ_CHATBOT_SETUP.md        # This file
```

## What Makes This Better?

### Compared to Regular Chatbots:
✅ Uses state-of-the-art AI (Llama 3.3 70B)
✅ Can answer ANYTHING like ChatGPT
✅ Maintains conversation context
✅ Fast responses (powered by Groq)

### Compared to Hardcoded Responses:
✅ No need to program responses
✅ Understands natural language
✅ Learns from conversation context
✅ Handles unexpected questions

### Compared to ChatGPT:
✅ Integrated into your platform
✅ Customizable for your needs
✅ Your own chat history
✅ No external dependencies (besides API)

## Next Steps

1. ✅ Start the service
2. ✅ Test it out
3. 🎨 Customize the UI if needed
4. 🚀 Deploy to production

## Support

### Service Status
Check if service is running:
```
http://localhost:8004/health
```

### API Documentation
Interactive API docs:
```
http://localhost:8004/docs
```

### Run Tests
```bash
test_groq_chatbot.bat
```

## Success Indicators

✅ Service starts without errors
✅ Health check returns "healthy"
✅ Test suite passes
✅ Dashboard shows chatbot page
✅ You can send messages and get responses

---

## 🎉 You're All Set!

Your Groq-powered chatbot is now ready to answer anything like ChatGPT!

Try asking:
- "Explain machine learning"
- "Write a Python function"
- "Give me career advice"
- "What is quantum computing?"
- Literally anything!

**Enjoy your AI assistant!** 🤖✨

