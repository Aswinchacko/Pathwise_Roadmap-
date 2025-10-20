#!/usr/bin/env python3
"""
Simple startup script for LinkedIn Mentor Scraping Service
"""
import uvicorn
import sys

print("="*60)
print("LinkedIn Mentor Scraping Service")
print("="*60)
print(f"Python version: {sys.version}")
print("Starting service on http://localhost:8001")
print("Press Ctrl+C to stop")
print("="*60)

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8001,
        reload=True,
        log_level="info"
    )


