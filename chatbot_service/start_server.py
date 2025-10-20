"""
Startup script for PathWise Groq Chatbot Service
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def check_environment():
    """Check if all required environment variables are set"""
    groq_key = os.getenv('GROQ_API_KEY', '')
    
    if not groq_key:
        print("⚠️  WARNING: GROQ_API_KEY not found in environment")
        print("   The chatbot will not work without this key")
        print("   Please add GROQ_API_KEY to your .env file")
        return False
    
    print(f"✅ Groq API Key found: {groq_key[:10]}...")
    return True

def main():
    """Start the chatbot service"""
    print("🤖 Starting PathWise Groq Chatbot Service...")
    print("=" * 60)
    
    # Check environment
    env_ok = check_environment()
    
    if not env_ok:
        print("\n❌ Environment check failed!")
        print("   Please configure your .env file and try again")
        sys.exit(1)
    
    print("\n📋 Configuration:")
    print(f"   Port: {os.getenv('PORT', '8004')}")
    print(f"   MongoDB: {os.getenv('MONGODB_URI', 'mongodb://localhost:27017/')}")
    
    print("\n🚀 Starting server...")
    print("   API docs will be available at: http://localhost:8004/docs")
    print("   Health check: http://localhost:8004/health")
    print("\n" + "=" * 60)
    
    # Start the server
    import uvicorn
    port = int(os.getenv('PORT', 8004))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)

if __name__ == "__main__":
    main()

