import os
from dotenv import load_dotenv
from pathlib import Path

print("Testing environment variable loading...")
print("-" * 50)

# Test 1: Direct env var
print(f"1. Direct os.getenv: {os.getenv('GROQ_API_KEY', 'NOT FOUND')[:30]}...")

# Test 2: Load from .env
env_path = Path("chatbot_service") / ".env"
print(f"\n2. .env path: {env_path}")
print(f"   .env exists: {env_path.exists()}")

if env_path.exists():
    load_dotenv(dotenv_path=env_path)
    print(f"   After load_dotenv: {os.getenv('GROQ_API_KEY', 'NOT FOUND')[:30]}...")

# Test 3: Read file directly
if env_path.exists():
    with open(env_path, 'r') as f:
        content = f.read()
        print(f"\n3. File content ({len(content)} bytes):")
        for line in content.split('\n')[:4]:
            if 'GROQ' in line:
                print(f"   {line[:60]}...")

