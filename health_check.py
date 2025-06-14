#!/usr/bin/env python3
"""
Health check script for the deployed VirtualTA API
"""
import requests
import sys
import os

def check_health(base_url):
    """Check if the API is healthy"""
    try:
        # Health endpoint check
        response = requests.get(f"{base_url}/health", timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            print("✅ API is healthy!")
            print(f"   Database: {data.get('database', 'unknown')}")
            print(f"   API Key configured: {data.get('api_key_set', False)}")
            print(f"   Discourse chunks: {data.get('discourse_chunks', 0)}")
            print(f"   Markdown chunks: {data.get('markdown_chunks', 0)}")
            return True
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Health check error: {e}")
        return False

if __name__ == "__main__":
    if len(sys.argv) > 1:
        url = sys.argv[1]
    else:
        url = os.environ.get("RENDER_EXTERNAL_URL", "http://localhost:10000")
    
    print(f"Checking health of: {url}")
    is_healthy = check_health(url)
    sys.exit(0 if is_healthy else 1) 