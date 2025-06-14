#!/usr/bin/env python3
"""
Test script for VirtualTA Knowledge Base API
Run this after your server is deployed to verify everything works.
"""

import requests
import json
import sys
import time

def test_api(base_url):
    """Test the API endpoints"""
    print(f"🧪 Testing API at: {base_url}")
    print("=" * 50)
    
    # Test 1: Health Check
    print("1️⃣ Testing Health Check...")
    try:
        response = requests.get(f"{base_url}/health", timeout=10)
        if response.status_code == 200:
            health_data = response.json()
            print("✅ Health check passed!")
            print(f"   Database: {health_data.get('database', 'unknown')}")
            print(f"   API Key Set: {health_data.get('api_key_set', False)}")
            print(f"   Discourse Chunks: {health_data.get('discourse_chunks', 0)}")
            print(f"   Markdown Chunks: {health_data.get('markdown_chunks', 0)}")
        else:
            print(f"❌ Health check failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Health check error: {e}")
        return False
    
    print()
    
    # Test 2: Web Interface
    print("2️⃣ Testing Web Interface...")
    try:
        response = requests.get(base_url, timeout=10)
        if response.status_code == 200:
            print("✅ Web interface accessible!")
            print(f"   Content type: {response.headers.get('content-type', 'unknown')}")
        else:
            print(f"❌ Web interface failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Web interface error: {e}")
    
    print()
    
    # Test 3: API Documentation
    print("3️⃣ Testing API Documentation...")
    try:
        response = requests.get(f"{base_url}/docs", timeout=10)
        if response.status_code == 200:
            print("✅ API documentation accessible!")
        else:
            print(f"❌ API docs failed: {response.status_code}")
    except Exception as e:
        print(f"❌ API docs error: {e}")
    
    print()
    
    # Test 4: Query API (only if API key is set)
    print("4️⃣ Testing Query API...")
    
    # Check if API key is configured from health check
    try:
        health_response = requests.get(f"{base_url}/health", timeout=10)
        health_data = health_response.json()
        api_key_set = health_data.get('api_key_set', False)
        
        if not api_key_set:
            print("⚠️  API key not configured - skipping query test")
            print("   To test queries, add your API key to .env file")
        else:
            # Test query
            test_query = {
                "question": "What is artificial intelligence?"
            }
            
            response = requests.post(
                f"{base_url}/query",
                json=test_query,
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                print("✅ Query API works!")
                print(f"   Answer length: {len(data.get('answer', ''))}")
                print(f"   Number of sources: {len(data.get('links', []))}")
                if data.get('answer'):
                    preview = data['answer'][:100] + "..." if len(data['answer']) > 100 else data['answer']
                    print(f"   Answer preview: {preview}")
            else:
                print(f"❌ Query API failed: {response.status_code}")
                print(f"   Response: {response.text}")
    except Exception as e:
        print(f"❌ Query API error: {e}")
    
    print()
    print("🎉 API Testing Complete!")
    print()
    print("Next steps:")
    print("- Visit the web interface in your browser")
    print("- Read API_USAGE_GUIDE.md for detailed documentation")
    print("- Share your ngrok URL with others!")
    
    return True

def main():
    """Main function"""
    if len(sys.argv) > 1:
        base_url = sys.argv[1].rstrip('/')
    else:
        # Default to localhost for testing
        base_url = "http://localhost:8000"
        print("No URL provided, testing localhost...")
        print("Usage: python test_api.py https://your-ngrok-url.ngrok.io")
        print()
    
    test_api(base_url)

if __name__ == "__main__":
    main() 