"""
PathWise Groq-Powered Chatbot Service
A ChatGPT-like chatbot using Groq API
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime
import os
import uuid
import logging
import random
from dotenv import load_dotenv
import requests
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
import re

# Configure logging first
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Load environment variables
import pathlib
env_path = pathlib.Path(__file__).parent / '.env'
logger.info(f"Loading .env from: {env_path}")
logger.info(f".env exists: {env_path.exists()}")
load_dotenv(dotenv_path=env_path)

# Configuration
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
MONGODB_URI = os.getenv('MONGODB_URI', 'mongodb://localhost:27017/')
DB_NAME = 'pathwise'

def get_groq_api_key():
    """Get Groq API key from environment"""
    return os.getenv('GROQ_API_KEY', '')

# Log Groq API key status at startup
def log_api_key_status():
    groq_key = get_groq_api_key()
    logger.info(f"Groq API Key loaded: {'YES' if groq_key else 'NO'} (length: {len(groq_key)})")
    return groq_key

# Check key on startup
initial_key = log_api_key_status()

# Initialize FastAPI app
app = FastAPI(
    title="PathWise Groq Chatbot API",
    description="ChatGPT-like chatbot powered by Groq API",
    version="1.0.0"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# MongoDB setup
mongo_client = None
db = None
chats_collection = None

try:
    mongo_client = MongoClient(MONGODB_URI, serverSelectionTimeoutMS=5000)
    mongo_client.admin.command('ping')
    db = mongo_client[DB_NAME]
    chats_collection = db['chats']
    logger.info("✅ Connected to MongoDB")
except ConnectionFailure:
    logger.warning("⚠️ MongoDB not available - using in-memory storage")
except Exception as e:
    logger.warning(f"⚠️ MongoDB error: {e} - using in-memory storage")

# In-memory storage fallback
chats_memory = {}

# Pydantic models
class ChatMessage(BaseModel):
    message: str
    user_id: str = "anonymous"
    chat_id: Optional[str] = None

class NewChatRequest(BaseModel):
    user_id: str
    title: str = "New Chat"

class ChatResponse(BaseModel):
    chat_id: str
    message_id: str
    response: str
    timestamp: str
    suggestions: List[str] = []
    confidence: Optional[float] = None
    roadmap_metadata: Optional[Dict[str, Any]] = None

class CreateRoadmapRequest(BaseModel):
    user_id: str
    chat_id: str
    title: str
    goal: str
    domain: Optional[str] = None

class CreateRoadmapResponse(BaseModel):
    success: bool
    roadmap_id: str
    message: str


def extract_roadmap_title(user_message: str, ai_response: str) -> str:
    """Extract a good title for the roadmap from the conversation"""
    # Look for common patterns in the user message
    if 'learn' in user_message.lower():
        if 'python' in user_message.lower():
            return "Learn Python Programming"
        elif 'react' in user_message.lower():
            return "Learn React Development"
        elif 'javascript' in user_message.lower():
            return "Learn JavaScript"
        elif 'data science' in user_message.lower():
            return "Learn Data Science"
        elif 'web development' in user_message.lower():
            return "Learn Web Development"
    
    # Try to extract from AI response headers
    import re
    header_match = re.search(r'##\s+(.+)', ai_response)
    if header_match:
        return header_match.group(1).strip()
    
    # Fallback to first part of user message
    return user_message[:50] + "..." if len(user_message) > 50 else user_message

def extract_domain_from_message(message: str) -> str:
    """Extract domain/category from the user message"""
    message_lower = message.lower()
    
    if any(word in message_lower for word in ['python', 'django', 'flask']):
        return "Python Development"
    elif any(word in message_lower for word in ['javascript', 'react', 'vue', 'angular', 'node']):
        return "Frontend Development"
    elif any(word in message_lower for word in ['data science', 'machine learning', 'ai', 'pandas', 'numpy']):
        return "Data Science"
    elif any(word in message_lower for word in ['web development', 'html', 'css', 'frontend']):
        return "Web Development"
    elif any(word in message_lower for word in ['mobile', 'ios', 'android', 'flutter', 'react native']):
        return "Mobile Development"
    elif any(word in message_lower for word in ['devops', 'docker', 'kubernetes', 'aws', 'cloud']):
        return "DevOps"
    else:
        return "General Learning"

def extract_learning_steps_from_chat(chat_content: str) -> List[Dict[str, Any]]:
    """
    Extract learning steps from chat content using AI
    """
    groq_api_key = get_groq_api_key()
    if not groq_api_key:
        return []
    
    try:
        # Create a prompt to extract structured learning steps
        extraction_prompt = f"""
        Analyze this chat conversation and extract a structured learning roadmap.
        Return ONLY a JSON array of learning steps in this exact format:
        [
            {{
                "category": "Step Name",
                "skills": ["skill1", "skill2", "skill3"],
                "description": "Brief description of what to learn"
            }}
        ]
        
        Chat content:
        {chat_content}
        
        Focus on practical, actionable learning steps. Return only the JSON array, no other text.
        """
        
        response = requests.post(
            GROQ_API_URL,
            headers={
                "Authorization": f"Bearer {groq_api_key}",
                "Content-Type": "application/json"
            },
            json={
                "model": "llama-3.3-70b-versatile",
                "messages": [{"role": "user", "content": extraction_prompt}],
                "temperature": 0.3,
                "max_tokens": 1500
            },
            timeout=30
        )
        
        if response.status_code == 200:
            ai_response = response.json()['choices'][0]['message']['content']
            # Try to extract JSON from the response
            import json
            try:
                # Find JSON array in the response
                json_match = re.search(r'\[.*\]', ai_response, re.DOTALL)
                if json_match:
                    steps = json.loads(json_match.group())
                    return steps
            except:
                pass
        
        # Fallback: create basic steps from content
        return [
            {
                "category": "Learning Foundation",
                "skills": ["Basic concepts", "Fundamentals"],
                "description": "Start with the basics mentioned in the conversation"
            },
            {
                "category": "Practical Application",
                "skills": ["Hands-on practice", "Real projects"],
                "description": "Apply what you've learned through practical exercises"
            }
        ]
        
    except Exception as e:
        logger.error(f"Error extracting learning steps: {e}")
        return []

def call_groq_api(messages: List[Dict[str, str]], temperature: float = 0.7, max_tokens: int = 2000) -> str:
    """
    Call Groq API to get chatbot response
    """
    groq_api_key = get_groq_api_key()
    if not groq_api_key:
        raise HTTPException(status_code=500, detail="Groq API key not configured")
    
    try:
        response = requests.post(
            GROQ_API_URL,
            headers={
                "Authorization": f"Bearer {groq_api_key}",
                "Content-Type": "application/json"
            },
            json={
                "model": "llama-3.3-70b-versatile",  # Best model for general conversation
                "messages": messages,
                "temperature": temperature,
                "max_tokens": max_tokens
            },
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            return result['choices'][0]['message']['content'].strip()
        elif response.status_code == 401:
            logger.error("Groq API authentication failed")
            raise HTTPException(status_code=500, detail="AI service authentication failed")
        elif response.status_code == 429:
            logger.error("Groq API rate limit exceeded")
            raise HTTPException(status_code=429, detail="Rate limit exceeded, please try again later")
        else:
            logger.error(f"Groq API error: {response.status_code} - {response.text}")
            raise HTTPException(status_code=500, detail="AI service error")
            
    except requests.exceptions.Timeout:
        logger.error("Groq API timeout")
        raise HTTPException(status_code=504, detail="AI service timeout")
    except requests.exceptions.ConnectionError:
        logger.error("Groq API connection error")
        raise HTTPException(status_code=503, detail="AI service unavailable")
    except Exception as e:
        logger.error(f"Unexpected error calling Groq API: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


def get_chat(user_id: str, chat_id: str) -> Optional[Dict]:
    """Get chat from MongoDB or memory"""
    if chats_collection is not None:
        try:
            return chats_collection.find_one({"user_id": user_id, "chat_id": chat_id})
        except:
            pass
    return chats_memory.get(f"{user_id}_{chat_id}")


def save_chat(chat_data: Dict):
    """Save chat to MongoDB or memory"""
    if chats_collection is not None:
        try:
            chats_collection.update_one(
                {"user_id": chat_data["user_id"], "chat_id": chat_data["chat_id"]},
                {"$set": chat_data},
                upsert=True
            )
            return
        except Exception as e:
            logger.warning(f"MongoDB save failed: {e}")
    
    # Fallback to memory
    chats_memory[f"{chat_data['user_id']}_{chat_data['chat_id']}"] = chat_data


def get_user_chats(user_id: str, limit: int = 20) -> List[Dict]:
    """Get all chats for a user"""
    if chats_collection is not None:
        try:
            chats = list(chats_collection.find(
                {"user_id": user_id},
                sort=[("last_message_at", -1)],
                limit=limit
            ))
            # Remove MongoDB _id field
            for chat in chats:
                chat.pop('_id', None)
            return chats
        except:
            pass
    
    # Fallback to memory
    user_chats = [
        chat for key, chat in chats_memory.items()
        if key.startswith(f"{user_id}_")
    ]
    return sorted(user_chats, key=lambda x: x.get('last_message_at', ''), reverse=True)[:limit]


def delete_chat_db(user_id: str, chat_id: str) -> bool:
    """Delete chat from MongoDB or memory"""
    if chats_collection is not None:
        try:
            result = chats_collection.delete_one({"user_id": user_id, "chat_id": chat_id})
            return result.deleted_count > 0
        except:
            pass
    
    # Fallback to memory
    key = f"{user_id}_{chat_id}"
    if key in chats_memory:
        del chats_memory[key]
        return True
    return False


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "service": "PathWise Groq Chatbot",
        "version": "1.0.0",
        "status": "running",
        "powered_by": "Groq API"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    mongo_status = "connected" if chats_collection is not None else "disconnected"
    groq_status = "configured" if get_groq_api_key() else "not_configured"
    
    return {
        "status": "healthy",
        "mongodb": mongo_status,
        "groq_api": groq_status,
        "timestamp": datetime.now().isoformat()
    }


@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatMessage):
    """
    Send a message and get AI response
    Works like ChatGPT - can answer anything!
    """
    user_id = request.user_id
    message = request.message
    chat_id = request.chat_id
    
    # Create new chat if needed
    if not chat_id:
        chat_id = str(uuid.uuid4())
        chat_data = {
            "chat_id": chat_id,
            "user_id": user_id,
            "title": message[:50] + "..." if len(message) > 50 else message,
            "created_at": datetime.now().isoformat(),
            "last_message_at": datetime.now().isoformat(),
            "messages": [],
            "message_count": 0
        }
    else:
        # Load existing chat
        chat_data = get_chat(user_id, chat_id)
        if not chat_data:
            raise HTTPException(status_code=404, detail="Chat not found")
    
    # Add user message to chat
    message_id = str(uuid.uuid4())
    user_message = {
        "id": message_id,
        "role": "user",
        "content": message,
        "timestamp": datetime.now().isoformat()
    }
    chat_data["messages"].append(user_message)
    
    # Prepare conversation history for Groq API
    # Include last 10 messages for context (5 exchanges)
    conversation_history = []
    recent_messages = chat_data["messages"][-10:]
    
    for msg in recent_messages:
        conversation_history.append({
            "role": msg["role"],
            "content": msg["content"]
        })
    
    # Get AI response from Groq with structured prompt
    try:
        # Add system prompt for better structure
        system_prompt = {
            "role": "system",
            "content": """You are a helpful AI assistant. Please provide well-structured, clear, and comprehensive responses. Use markdown formatting with:
        - **Bold** for important terms
        - ## Headers for main sections
        - ### Subheaders for subsections
        - Bullet points for lists
        - Code blocks for code examples
        - Numbered lists for steps
        - Tables when appropriate

        Make your responses easy to read and well-organized."""
        }
        
        # Check if the message is asking for a roadmap/learning path
        roadmap_keywords = [
            'roadmap', 'learning path', 'step by step', 'how to learn', 
            'learning plan', 'study plan', 'curriculum', 'syllabus',
            'what should I learn', 'where to start', 'beginner guide',
            'tutorial path', 'learning journey', 'skill development'
        ]
        
        is_roadmap_request = any(keyword in message.lower() for keyword in roadmap_keywords)
        
        # Add system prompt to conversation
        structured_conversation = [system_prompt] + conversation_history
        ai_response = call_groq_api(structured_conversation)
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"Error getting AI response: {e}")
        raise HTTPException(status_code=500, detail="Failed to get AI response")
    
    # Add AI message to chat
    bot_message_id = str(uuid.uuid4())
    bot_message = {
        "id": bot_message_id,
        "role": "assistant",
        "content": ai_response,
        "timestamp": datetime.now().isoformat()
    }
    chat_data["messages"].append(bot_message)
    
    # Update chat metadata
    chat_data["last_message_at"] = datetime.now().isoformat()
    chat_data["message_count"] = len(chat_data["messages"])
    
    # Save chat
    save_chat(chat_data)
    
    # Prepare response with roadmap metadata if applicable
    response_data = {
        "chat_id": chat_id,
        "message_id": bot_message_id,
        "response": ai_response,
        "timestamp": datetime.now().isoformat(),
        "suggestions": [],
        "confidence": 0.95
    }
    
    # Add roadmap metadata if this is a roadmap request
    if is_roadmap_request:
        response_data["roadmap_metadata"] = {
            "is_roadmap_request": True,
            "suggested_title": extract_roadmap_title(message, ai_response),
            "suggested_goal": message,
            "suggested_domain": extract_domain_from_message(message)
        }
    
    return ChatResponse(**response_data)


@app.post("/chats/new")
async def create_new_chat(request: NewChatRequest):
    """Create a new chat"""
    chat_id = str(uuid.uuid4())
    chat_data = {
        "chat_id": chat_id,
        "user_id": request.user_id,
        "title": request.title,
        "created_at": datetime.now().isoformat(),
        "last_message_at": datetime.now().isoformat(),
        "messages": [],
        "message_count": 0
    }
    
    save_chat(chat_data)
    
    return {
        "chat_id": chat_id,
        "title": request.title,
        "created_at": chat_data["created_at"]
    }


@app.get("/chats/{user_id}")
async def get_chats(user_id: str, limit: int = 20):
    """Get user's chat history"""
    chats = get_user_chats(user_id, limit)
    
    # Format response
    formatted_chats = []
    for chat in chats:
        formatted_chats.append({
            "chat_id": chat["chat_id"],
            "title": chat["title"],
            "created_at": chat["created_at"],
            "last_message_at": chat.get("last_message_at", chat["created_at"]),
            "message_count": chat.get("message_count", 0)
        })
    
    return {"chats": formatted_chats}


@app.get("/chats/{user_id}/{chat_id}")
async def get_chat_messages(user_id: str, chat_id: str):
    """Get messages for a specific chat"""
    chat_data = get_chat(user_id, chat_id)
    
    if not chat_data:
        raise HTTPException(status_code=404, detail="Chat not found")
    
    return {
        "chat_id": chat_id,
        "title": chat_data["title"],
        "messages": chat_data["messages"],
        "created_at": chat_data["created_at"],
        "last_message_at": chat_data.get("last_message_at", chat_data["created_at"])
    }


@app.delete("/chats/{user_id}/{chat_id}")
async def delete_chat(user_id: str, chat_id: str):
    """Delete a chat"""
    success = delete_chat_db(user_id, chat_id)
    
    if not success:
        raise HTTPException(status_code=404, detail="Chat not found")
    
    return {"success": True, "message": "Chat deleted successfully"}


@app.put("/chats/{user_id}/{chat_id}/title")
async def update_chat_title(user_id: str, chat_id: str, title: str):
    """Update chat title"""
    chat_data = get_chat(user_id, chat_id)
    
    if not chat_data:
        raise HTTPException(status_code=404, detail="Chat not found")
    
    chat_data["title"] = title
    save_chat(chat_data)
    
    return {"success": True, "title": title}


@app.post("/roadmap/create-from-chat", response_model=CreateRoadmapResponse)
async def create_roadmap_from_chat(request: CreateRoadmapRequest):
    """Create a roadmap from a chat conversation"""
    try:
        # Get the chat data
        chat_data = get_chat(request.user_id, request.chat_id)
        if not chat_data:
            raise HTTPException(status_code=404, detail="Chat not found")
        
        # Extract all messages from the chat
        chat_content = ""
        for message in chat_data.get("messages", []):
            role = message.get("role", "")
            content = message.get("content", "")
            if role == "user":
                chat_content += f"User: {content}\n\n"
            elif role == "assistant":
                chat_content += f"Assistant: {content}\n\n"
        
        # Extract learning steps using AI
        steps = extract_learning_steps_from_chat(chat_content)
        
        # Create roadmap document
        roadmap_id = f"roadmap_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{random.randint(1000, 9999)}"
        
        roadmap_doc = {
            "roadmap_id": roadmap_id,
            "title": request.title,
            "goal": request.goal,
            "domain": request.domain or "General Learning",
            "user_id": request.user_id,
            "steps": steps,
            "created_at": datetime.now(),
            "updated_at": datetime.now(),
            "source": "chat_generated",
            "chat_id": request.chat_id,
            "difficulty": "Intermediate",
            "estimated_hours": len(steps) * 20,  # Estimate 20 hours per step
            "prerequisites": "Based on chat conversation",
            "learning_outcomes": f"Complete learning path for: {request.goal}"
        }
        
        # Save to MongoDB
        if db:
            roadmap_collection = db['roadmap']
            roadmap_collection.insert_one(roadmap_doc)
            logger.info(f"Created roadmap {roadmap_id} from chat {request.chat_id}")
        else:
            logger.warning("MongoDB not available - roadmap not saved")
        
        return CreateRoadmapResponse(
            success=True,
            roadmap_id=roadmap_id,
            message=f"Roadmap '{request.title}' created successfully with {len(steps)} learning steps"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating roadmap from chat: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to create roadmap: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv('PORT', 8004))
    uvicorn.run(app, host="0.0.0.0", port=port)

