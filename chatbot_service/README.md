# PathWise Groq-Powered Chatbot Service

## Overview

A ChatGPT-like chatbot microservice powered by **Groq API** using the Llama 3.3 70B model. This service can answer anything just like ChatGPT - from technical questions to career advice, coding help, explanations, and more.

## Features

✨ **ChatGPT-like Conversations**
- Answer any question like ChatGPT
- Maintains conversation context
- Natural, intelligent responses

🧠 **Powered by Groq API**
- Uses Llama 3.3 70B Versatile model
- Fast response times
- High-quality answers

💬 **Full Chat Management**
- Create, load, and delete chats
- Edit chat titles
- Persistent chat history
- Multiple conversations per user

💾 **Dual Storage**
- MongoDB for persistent storage
- In-memory fallback
- Automatic failover

🔒 **Production Ready**
- FastAPI backend
- CORS support
- Error handling
- Logging

## Quick Start

### 1. Install Dependencies

```bash
cd chatbot_service
pip install -r requirements.txt
```

### 2. Configure Environment

The `.env` file is already configured with your Groq API key:

```env
GROQ_API_KEY=your_key_here
MONGODB_URI=mongodb://localhost:27017/
PORT=8004
```

### 3. Start the Service

**Windows:**
```bash
cd chatbot_service
python start_server.py
```

**Or use the batch file from root:**
```bash
start_chatbot_system.bat
```

### 4. Test the Service

```bash
cd chatbot_service
python test_chatbot.py
```

## API Endpoints

### Chat Endpoints

#### Send Message
```http
POST /chat
Content-Type: application/json

{
  "message": "Hello, explain machine learning",
  "user_id": "user123",
  "chat_id": "optional-existing-chat-id"
}
```

**Response:**
```json
{
  "chat_id": "uuid",
  "message_id": "uuid",
  "response": "Machine learning is...",
  "timestamp": "2024-01-01T12:00:00",
  "suggestions": [],
  "confidence": 0.95
}
```

#### Create New Chat
```http
POST /chats/new
Content-Type: application/json

{
  "user_id": "user123",
  "title": "My Chat"
}
```

#### Get User Chats
```http
GET /chats/{user_id}?limit=20
```

#### Get Chat Messages
```http
GET /chats/{user_id}/{chat_id}
```

#### Delete Chat
```http
DELETE /chats/{user_id}/{chat_id}
```

#### Update Chat Title
```http
PUT /chats/{user_id}/{chat_id}/title?title=New%20Title
```

### System Endpoints

#### Health Check
```http
GET /health
```

#### Root
```http
GET /
```

## Usage Examples

### Basic Conversation

```python
import requests

# Start a conversation
response = requests.post('http://localhost:8004/chat', json={
    'message': 'What is recursion in programming?',
    'user_id': 'user123'
})

data = response.json()
print(data['response'])
chat_id = data['chat_id']

# Follow-up question
response = requests.post('http://localhost:8004/chat', json={
    'message': 'Can you show me a Python example?',
    'user_id': 'user123',
    'chat_id': chat_id
})

print(response.json()['response'])
```

### Question Types the Bot Can Answer

✅ **Technical Questions**
- "Explain quantum computing"
- "What is the difference between SQL and NoSQL?"
- "How does Docker work?"

✅ **Coding Help**
- "Write a Python function to reverse a string"
- "Debug this JavaScript code: [code]"
- "Explain this algorithm: [algorithm]"

✅ **Career Advice**
- "How do I become a data scientist?"
- "What skills do I need for DevOps?"
- "Should I learn React or Vue?"

✅ **Explanations**
- "Explain blockchain in simple terms"
- "How does the internet work?"
- "What is functional programming?"

✅ **Project Ideas**
- "Give me project ideas for my portfolio"
- "What should I build to learn Django?"
- "Suggest machine learning projects"

✅ **General Knowledge**
- "What is photosynthesis?"
- "Explain the theory of relativity"
- "Who invented the computer?"

## Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `GROQ_API_KEY` | Your Groq API key | Required |
| `MONGODB_URI` | MongoDB connection string | `mongodb://localhost:27017/` |
| `PORT` | Service port | `8004` |
| `HOST` | Service host | `0.0.0.0` |
| `CORS_ORIGINS` | Allowed origins | `*` |

### Groq API Configuration

The service uses:
- **Model**: `llama-3.3-70b-versatile`
- **Temperature**: 0.7 (balanced creativity)
- **Max Tokens**: 2000 (detailed responses)
- **Timeout**: 30 seconds

You can modify these in `main.py` if needed.

## Architecture

```
┌─────────────┐
│   Frontend  │ (React Dashboard)
└──────┬──────┘
       │ HTTP
       │
┌──────▼──────────────────┐
│  Chatbot Service        │
│  (FastAPI)              │
│                         │
│  ┌─────────────────┐   │
│  │  Groq API       │   │
│  │  Integration    │   │
│  └─────────────────┘   │
│                         │
│  ┌─────────────────┐   │
│  │  Chat Manager   │   │
│  └─────────────────┘   │
└──────┬──────────────────┘
       │
   ┌───▼────┐
   │ MongoDB│ (Optional)
   └────────┘
```

## Testing

### Run All Tests

```bash
cd chatbot_service
python test_chatbot.py
```

This will test:
1. Health check
2. Conversation flow
3. Chat management
4. Various question types

### Manual Testing

Visit the API documentation:
```
http://localhost:8004/docs
```

Try the interactive Swagger UI!

## Troubleshooting

### Service won't start

1. **Check Groq API Key**
   ```bash
   # Verify .env file exists and has GROQ_API_KEY
   ```

2. **Port already in use**
   ```bash
   # Change PORT in .env file
   ```

3. **Dependencies missing**
   ```bash
   pip install -r requirements.txt
   ```

### No response from chatbot

1. **Groq API issues**
   - Check API key is valid
   - Check rate limits
   - Check internet connection

2. **Timeout errors**
   - Groq API might be slow
   - Increase timeout in main.py

### MongoDB errors

- Service will automatically fall back to in-memory storage
- Chats will be lost on restart without MongoDB
- To fix: Install and start MongoDB

## Performance

- **Response Time**: 1-5 seconds (depends on Groq API)
- **Concurrent Users**: 50+ (can be scaled)
- **Context Window**: Last 10 messages (5 exchanges)
- **Max Message Length**: No hard limit

## Security

- CORS enabled for specified origins
- Input validation on all endpoints
- No sensitive data in logs
- API key stored in environment variables

## Integration with Frontend

The frontend (`dashboard/src/pages/Chatbot.jsx`) is already configured to use this service on port 8004.

Make sure both services are running:
1. Chatbot service: `http://localhost:8004`
2. Dashboard: `http://localhost:5173`

## Future Enhancements

- [ ] Streaming responses
- [ ] File upload support
- [ ] Image understanding
- [ ] Voice input/output
- [ ] Multi-language support
- [ ] Advanced context management
- [ ] Rate limiting per user
- [ ] Analytics and logging

## License

Part of the PathWise platform.

---

**Questions?** Check the API docs at `http://localhost:8004/docs`

