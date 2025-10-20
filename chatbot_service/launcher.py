"""
Launcher that ensures environment is loaded before starting
"""
import os
import sys

# Load environment variables from .env file
from dotenv import load_dotenv
load_dotenv()

# Set default values if not in .env
if 'GROQ_API_KEY' not in os.environ:
    os.environ['GROQ_API_KEY'] = ''
    print("⚠️ GROQ_API_KEY not found in environment")
if 'PORT' not in os.environ:
    os.environ['PORT'] = '8004'
if 'MONGODB_URI' not in os.environ:
    os.environ['MONGODB_URI'] = 'mongodb://localhost:27017/'

print("✅ Environment variables loaded")
if os.environ.get('GROQ_API_KEY'):
    print(f"   GROQ_API_KEY: {os.environ['GROQ_API_KEY'][:10]}...{os.environ['GROQ_API_KEY'][-4:]}")

# Now import and run
print("🚀 Starting chatbot service...")
import uvicorn
from main import app

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8004)

