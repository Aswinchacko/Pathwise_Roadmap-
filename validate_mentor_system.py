#!/usr/bin/env python3
"""
Complete Validation Script for LinkedIn Mentor System
Tests all components and verifies system is ready to use
"""
import os
import sys
import requests
from pymongo import MongoClient
import subprocess
import time

class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    END = '\033[0m'

def print_header(text):
    print(f"\n{Colors.BLUE}{'='*60}")
    print(f"{text}")
    print(f"{'='*60}{Colors.END}\n")

def print_success(text):
    print(f"{Colors.GREEN}✓ {text}{Colors.END}")

def print_error(text):
    print(f"{Colors.RED}✗ {text}{Colors.END}")

def print_warning(text):
    print(f"{Colors.YELLOW}⚠ {text}{Colors.END}")

def print_info(text):
    print(f"{Colors.BLUE}ℹ {text}{Colors.END}")

def check_file_exists(filepath, description):
    """Check if a file exists"""
    if os.path.exists(filepath):
        print_success(f"{description}: {filepath}")
        return True
    else:
        print_error(f"{description} not found: {filepath}")
        return False

def check_mongodb():
    """Check MongoDB connection"""
    print_info("Checking MongoDB...")
    try:
        client = MongoClient('mongodb://localhost:27017', serverSelectionTimeoutMS=2000)
        client.server_info()
        
        db = client['pathwise']
        roadmap_count = db.roadmap.count_documents({})
        mentors_count = db.mentors.count_documents({})
        
        print_success(f"MongoDB connected")
        print_info(f"  - Roadmaps in DB: {roadmap_count}")
        print_info(f"  - Mentors in DB: {mentors_count}")
        return True
    except Exception as e:
        print_error(f"MongoDB connection failed: {e}")
        print_warning("Start MongoDB with: mongod")
        return False

def check_service_running(url, name):
    """Check if a service is running"""
    print_info(f"Checking {name}...")
    try:
        response = requests.get(url, timeout=2)
        print_success(f"{name} is running on {url}")
        return True
    except:
        print_warning(f"{name} is not running on {url}")
        return False

def check_python_packages():
    """Check required Python packages"""
    print_info("Checking Python packages...")
    required_packages = [
        'fastapi',
        'uvicorn',
        'pymongo',
        'selenium',
        'webdriver_manager'
    ]
    
    missing = []
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
            print_success(f"  {package} installed")
        except ImportError:
            print_error(f"  {package} not installed")
            missing.append(package)
    
    if missing:
        print_warning(f"Install missing packages: pip install {' '.join(missing)}")
        return False
    return True

def check_chrome():
    """Check if Chrome is installed"""
    print_info("Checking Chrome browser...")
    chrome_paths = [
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
        "/usr/bin/google-chrome",
        "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
    ]
    
    for path in chrome_paths:
        if os.path.exists(path):
            print_success(f"Chrome found: {path}")
            return True
    
    print_warning("Chrome not found. Install from: https://www.google.com/chrome/")
    return False

def validate_system():
    """Complete system validation"""
    print_header("LinkedIn Mentor System Validation")
    
    all_checks = []
    
    # 1. Check files
    print_header("1. Checking Files")
    files_to_check = [
        ('linkedin_mentor_service/main.py', 'Scraping service'),
        ('linkedin_mentor_service/requirements.txt', 'Python dependencies'),
        ('linkedin_mentor_service/start_server.bat', 'Startup script'),
        ('dashboard/src/pages/Mentors.jsx', 'Frontend component'),
        ('dashboard/src/pages/Mentors.css', 'Frontend styles'),
        ('LINKEDIN_MENTOR_SCRAPING_SETUP.md', 'Setup documentation'),
        ('QUICK_START_LINKEDIN_MENTORS.md', 'Quick start guide'),
        ('IMPLEMENTATION_COMPLETE.md', 'Implementation summary'),
    ]
    
    files_ok = all(check_file_exists(f, d) for f, d in files_to_check)
    all_checks.append(('Files', files_ok))
    
    # 2. Check MongoDB
    print_header("2. Checking MongoDB")
    mongodb_ok = check_mongodb()
    all_checks.append(('MongoDB', mongodb_ok))
    
    # 3. Check Python packages
    print_header("3. Checking Python Dependencies")
    packages_ok = check_python_packages()
    all_checks.append(('Python Packages', packages_ok))
    
    # 4. Check Chrome
    print_header("4. Checking Chrome Browser")
    chrome_ok = check_chrome()
    all_checks.append(('Chrome Browser', chrome_ok))
    
    # 5. Check services
    print_header("5. Checking Services")
    services = [
        ('http://localhost:8005/api/mentors/health', 'LinkedIn Scraping Service (Port 8005)'),
        ('http://localhost:5173', 'Frontend (Port 5173)'),
        ('http://localhost:8000/health', 'Roadmap API (Port 8000)'),
    ]
    
    for url, name in services:
        service_ok = check_service_running(url, name)
        all_checks.append((name, service_ok))
    
    # Summary
    print_header("Validation Summary")
    
    passed = sum(1 for _, ok in all_checks if ok)
    total = len(all_checks)
    
    for name, ok in all_checks:
        if ok:
            print_success(f"{name}")
        else:
            print_error(f"{name}")
    
    print(f"\n{Colors.BLUE}Score: {passed}/{total} checks passed{Colors.END}")
    
    if passed == total:
        print(f"\n{Colors.GREEN}{'='*60}")
        print("🎉 System is ready to use!")
        print("="*60 + Colors.END)
        print("\nNext steps:")
        print("1. If services aren't running, start them:")
        print("   - start_linkedin_mentor_service.bat")
        print("   - cd dashboard && npm run dev")
        print("2. Create a roadmap in the app")
        print("3. Visit the Mentors page to see real LinkedIn profiles")
    else:
        print(f"\n{Colors.RED}{'='*60}")
        print("❌ System needs attention")
        print("="*60 + Colors.END)
        print("\nFix the failed checks above, then run this script again.")
        print("\nQuick fixes:")
        if not mongodb_ok:
            print("  - Start MongoDB: mongod")
        if not packages_ok:
            print("  - Install packages: cd linkedin_mentor_service && pip install -r requirements.txt")
        print("  - Start services: start_linkedin_mentor_service.bat")
    
    return passed == total

if __name__ == "__main__":
    try:
        success = validate_system()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\nValidation cancelled by user")
        sys.exit(1)
    except Exception as e:
        print_error(f"Validation error: {e}")
        sys.exit(1)


