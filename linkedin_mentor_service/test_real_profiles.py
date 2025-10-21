#!/usr/bin/env python3
"""
Test script to verify real profile search is working
"""
import os
import requests
from dotenv import load_dotenv

load_dotenv()

def test_api_keys():
    """Test if API keys are configured"""
    print("=" * 60)
    print("Testing API Key Configuration")
    print("=" * 60)
    
    serper_key = os.getenv('SERPER_API_KEY', '')
    groq_key = os.getenv('GROQ_API_KEY', '')
    
    print(f"\n✓ Serper API Key: {'✓ Configured' if serper_key else '✗ Not found'}")
    if serper_key:
        print(f"  Key starts with: {serper_key[:10]}...")
    
    print(f"\n✓ Groq API Key: {'✓ Configured' if groq_key else '✗ Not found'}")
    if groq_key:
        print(f"  Key starts with: {groq_key[:10]}...")
    
    if not serper_key:
        print("\n⚠️  Warning: No Serper API key found!")
        print("   Service will use AI-generated profiles instead of real ones.")
        print("   Get a free key at: https://serper.dev/")
    
    if not groq_key:
        print("\n⚠️  Warning: No Groq API key found!")
        print("   Service will use static curated data.")
        print("   Get a free key at: https://console.groq.com/")
    
    return bool(serper_key and groq_key)

def test_service_health():
    """Test if service is running"""
    print("\n" + "=" * 60)
    print("Testing Service Health")
    print("=" * 60)
    
    try:
        response = requests.get("http://localhost:8001/api/mentors/health", timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            print(f"\n✓ Service Status: {data.get('status', 'unknown')}")
            print(f"✓ MongoDB: {data.get('mongodb', 'unknown')}")
            print(f"✓ AI Search: {data.get('ai_search', 'unknown')}")
            print(f"✓ Groq API: {data.get('groq_api', 'unknown')}")
            print(f"✓ Search Mode: {data.get('search_mode', 'unknown')}")
            
            return True
        else:
            print(f"\n✗ Service error: {response.status_code}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("\n✗ Service is not running!")
        print("   Start it with: cd linkedin_mentor_service && python main.py")
        return False
    except Exception as e:
        print(f"\n✗ Error: {e}")
        return False

def test_real_profile_search():
    """Test real profile search"""
    print("\n" + "=" * 60)
    print("Testing Real Profile Search")
    print("=" * 60)
    
    # First, we need to create a test roadmap in MongoDB
    print("\n⚠️  Note: This test requires a roadmap in MongoDB")
    print("   Create one at: http://localhost:5173/roadmap")
    
    user_id = input("\nEnter your user ID (or press Enter to skip): ").strip()
    
    if not user_id:
        print("\n⚠️  Skipping profile search test")
        return False
    
    try:
        print(f"\n🔍 Searching for mentors for user: {user_id}")
        print("   This may take 5-10 seconds...")
        
        payload = {
            "user_id": user_id,
            "limit": 5,
            "experience_level": "intermediate",
            "refresh_cache": True
        }
        
        response = requests.post(
            "http://localhost:8001/api/mentors/scrape",
            json=payload,
            timeout=60
        )
        
        if response.status_code == 200:
            data = response.json()
            
            print(f"\n✓ Success!")
            print(f"  Total found: {data.get('total_found', 0)}")
            print(f"  Search source: {data.get('search_source', 'unknown')}")
            print(f"  Cached: {data.get('cached', False)}")
            print(f"  Message: {data.get('message', 'N/A')}")
            
            if data.get('search_source') == 'real':
                print("\n🎉 SUCCESS! Real profiles are working!")
            elif data.get('search_source') == 'ai':
                print("\n⚠️  Using AI-generated profiles")
                print("   To get real profiles, add SERPER_API_KEY to .env")
            else:
                print("\n⚠️  Using static curated data")
            
            # Show sample mentor
            if data.get('mentors'):
                print(f"\n📋 Sample mentor:")
                mentor = data['mentors'][0]
                print(f"  Name: {mentor.get('name')}")
                print(f"  Title: {mentor.get('title')}")
                print(f"  Company: {mentor.get('company', 'N/A')}")
                print(f"  Real profile: {mentor.get('is_real_profile', False)}")
                print(f"  AI generated: {mentor.get('is_ai_generated', False)}")
                print(f"  Profile URL: {mentor.get('profile_url')}")
            
            return True
        else:
            error_data = response.json()
            print(f"\n✗ Error: {error_data.get('detail', 'Unknown error')}")
            return False
            
    except Exception as e:
        print(f"\n✗ Error: {e}")
        return False

def main():
    print("\n🎯 Real LinkedIn Profiles - Test Suite\n")
    
    # Test 1: Check API keys
    keys_ok = test_api_keys()
    
    # Test 2: Check service health
    service_ok = test_service_health()
    
    if not service_ok:
        print("\n" + "=" * 60)
        print("⚠️  Service is not running. Start it first!")
        print("=" * 60)
        return
    
    # Test 3: Test real profile search
    test_real_profile_search()
    
    # Summary
    print("\n" + "=" * 60)
    print("Test Summary")
    print("=" * 60)
    
    if keys_ok:
        print("\n✓ Configuration: All API keys configured")
        print("✓ Expected behavior: Real profiles from Google search")
    else:
        print("\n⚠️  Configuration: Missing API keys")
        print("⚠️  Expected behavior: AI-generated or static profiles")
    
    print("\n📖 Setup Guide: linkedin_mentor_service/REAL_PROFILES_SETUP.md")
    print("🌐 Frontend: http://localhost:5173/mentors")
    print("🔧 Service: http://localhost:8001")
    
    print("\n" + "=" * 60)

if __name__ == "__main__":
    main()

