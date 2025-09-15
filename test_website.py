#!/usr/bin/env python3
"""
Test script to validate the website and API endpoints
Created by: Copilot for ◉Ɗєиνιℓ
"""

import asyncio
import aiohttp
import json
import sys
from pathlib import Path

async def test_endpoint(session, url, method='GET', data=None, expected_status=200):
    """Test a single endpoint"""
    try:
        if method == 'GET':
            async with session.get(url) as response:
                status = response.status
                content = await response.text()
                
        elif method == 'POST':
            headers = {'Content-Type': 'application/json'}
            async with session.post(url, json=data, headers=headers) as response:
                status = response.status
                content = await response.text()
        
        success = status == expected_status
        print(f"{'✅' if success else '❌'} {method} {url} - Status: {status}")
        
        if not success:
            print(f"   Expected: {expected_status}, Got: {status}")
            print(f"   Response: {content[:200]}...")
        
        return success, status, content
    
    except Exception as e:
        print(f"❌ {method} {url} - Error: {str(e)}")
        return False, 0, str(e)

async def test_website_and_api(base_url="http://localhost:8000"):
    """Test all endpoints"""
    print(f"🧪 Testing Shan-D website and API at {base_url}")
    print("=" * 60)
    
    async with aiohttp.ClientSession() as session:
        tests = [
            # Test main website
            ("GET", "/", None, 200),
            
            # Test API endpoints
            ("GET", "/health", None, 200),
            ("GET", "/api/status", None, 200),
            
            # Test chat API
            ("POST", "/api/chat", {"message": "Hello test", "user_id": "test_user"}, 200),
            ("POST", "/api/chat", {}, 400),  # Should fail without message
        ]
        
        results = []
        for method, path, data, expected_status in tests:
            url = f"{base_url}{path}"
            success, status, content = await test_endpoint(session, url, method, data, expected_status)
            results.append((method, path, success, status))
            
            # For successful requests, validate content
            if success and path == "/":
                if "Shan_D_Superadvanced" in content and "chatBox" in content:
                    print("   ✅ Website HTML content looks correct")
                else:
                    print("   ⚠️ Website HTML content may be incomplete")
            
            elif success and path.startswith("/api/"):
                try:
                    json_data = json.loads(content)
                    print(f"   ✅ Valid JSON response: {list(json_data.keys())}")
                except:
                    print("   ⚠️ Non-JSON API response")
            
            print()
    
    # Summary
    print("=" * 60)
    passed = sum(1 for _, _, success, _ in results if success)
    total = len(results)
    
    print(f"🏁 Test Results: {passed}/{total} passed")
    
    if passed == total:
        print("🎉 All tests passed! Website should work correctly.")
        return True
    else:
        print("❌ Some tests failed. Please check the issues above.")
        return False

def test_static_files():
    """Test that static files exist"""
    print("📁 Checking static files...")
    
    static_dir = Path(__file__).parent / "static"
    index_file = static_dir / "index.html"
    
    if not static_dir.exists():
        print("❌ Static directory does not exist")
        return False
    
    if not index_file.exists():
        print("❌ index.html does not exist")
        return False
    
    # Check index.html content
    try:
        with open(index_file, 'r') as f:
            content = f.read()
        
        required_elements = [
            "Shan_D_Superadvanced",
            "chatBox",
            "sendMessage",
            "/api/chat"
        ]
        
        missing = [elem for elem in required_elements if elem not in content]
        
        if missing:
            print(f"❌ Missing elements in index.html: {missing}")
            return False
        else:
            print("✅ index.html contains all required elements")
            return True
    
    except Exception as e:
        print(f"❌ Error reading index.html: {e}")
        return False

if __name__ == "__main__":
    print("🔍 Shan-D Website Validation Test")
    print("Created by: Copilot for ◉Ɗєиνιℓ")
    print()
    
    # Test static files first
    static_ok = test_static_files()
    print()
    
    # Test if we should run server tests
    if len(sys.argv) > 1 and sys.argv[1] == "--with-server":
        server_ok = asyncio.run(test_website_and_api())
        
        if static_ok and server_ok:
            print("\n🌟 All tests passed! The website should work perfectly.")
            sys.exit(0)
        else:
            print("\n💥 Some tests failed.")
            sys.exit(1)
    else:
        if static_ok:
            print("✅ Static file validation passed!")
            print("💡 To test with a running server, use: python test_website.py --with-server")
        else:
            print("❌ Static file validation failed!")
            sys.exit(1)