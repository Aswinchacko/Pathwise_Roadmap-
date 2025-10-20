#!/usr/bin/env python3
"""Create a test roadmap in MongoDB for testing mentor scraping"""
from pymongo import MongoClient
from datetime import datetime

def create_test_roadmap():
    try:
        # Connect to MongoDB
        client = MongoClient('mongodb://localhost:27017', serverSelectionTimeoutMS=5000)
        db = client['pathwise']
        roadmap_collection = db['roadmap']
        
        print("[INIT] Creating test roadmap...")
        
        # Create test roadmap
        test_roadmap = {
            "user_id": "test_user",
            "goal": "Become a Full Stack Developer",
            "domain": "Web Development",
            "source": "user_generated",
            "created_at": datetime.now(),
            "steps": [
                {"title": "Learn HTML/CSS", "completed": False},
                {"title": "Master JavaScript", "completed": False},
                {"title": "Learn React", "completed": False},
                {"title": "Learn Node.js", "completed": False},
                {"title": "Learn Databases", "completed": False}
            ]
        }
        
        # Insert or update
        result = roadmap_collection.update_one(
            {"user_id": "test_user"},
            {"$set": test_roadmap},
            upsert=True
        )
        
        if result.upserted_id:
            print(f"[OK] Created new roadmap with ID: {result.upserted_id}")
        else:
            print(f"[OK] Updated existing roadmap (matched: {result.matched_count})")
        
        # Verify
        found = roadmap_collection.find_one({"user_id": "test_user"})
        if found:
            print(f"[OK] Verified roadmap exists")
            print(f"     Goal: {found['goal']}")
            print(f"     Domain: {found['domain']}")
        else:
            print("[ERROR] Roadmap not found after insert!")
        
        print("")
        print("[SUCCESS] Test roadmap created successfully!")
        print("")
        print("Now you can test the mentor scraping service:")
        print('  $body = @{ user_id = "test_user"; limit = 3 } | ConvertTo-Json')
        print('  Invoke-RestMethod -Uri "http://localhost:8005/api/mentors/scrape" -Method Post -Body $body -ContentType "application/json"')
        
    except Exception as e:
        print(f"[ERROR] Failed to create test roadmap: {e}")
        return False
    
    return True

if __name__ == "__main__":
    create_test_roadmap()


