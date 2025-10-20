"""
Simple runner that loads .env before starting the service
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Load .env first
env_path = Path(__file__).parent / '.env'
print(f"Loading .env from: {env_path}")
print(f".env exists: {env_path.exists()}")

load_dotenv(dotenv_path=env_path)

# Verify key loaded
groq_key = os.getenv('GROQ_API_KEY', '')
print(f"Groq API Key loaded: {'YES' if groq_key else 'NO'}")
if groq_key:
    print(f"Key length: {len(groq_key)}")
    print(f"Key preview: {groq_key[:20]}...")

if not groq_key:
    print("ERROR: No Groq API key found!")
    print(f"Please check {env_path} file")
    sys.exit(1)

# Now import and run
print("\nStarting server...\n")
import uvicorn
from main import app

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8004)

