#!/usr/bin/env python3
"""
DeepSeek API Test Script

This script tests the DeepSeek API integration to verify:
1. API key configuration
2. API connectivity
3. Response parsing
4. DeepseekService functionality
5. Fallback behavior

Usage:
    python backend/app/utils/test.py
"""

import asyncio
import os
import sys
import json
import logging
from pathlib import Path
import dotenv

dotenv.load_dotenv()

# Add the backend directory to the Python path
backend_dir = Path(__file__).parent.parent.parent
sys.path.insert(0, str(backend_dir))

from app.config import settings
from app.services.deepseek import DeepseekService
from app.utils.ai_utils import call_deepseek

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)
logger = logging.getLogger(__name__)


def test_config():
    """Test if the configuration is loaded correctly"""
    print("=" * 60)
    print("1. TESTING CONFIGURATION")
    print("=" * 60)
    
    print(f"DeepSeek API Key: {'✓ SET' if settings.deepseek_api_key else '✗ NOT SET'}")

    
    print(f"DeepSeek API URL: {settings.deepseek_api_url}")
    
    # Check environment variable directly
    env_key = os.getenv("DEEPSEEK_API_KEY")
    print(f"Environment variable: {'✓ SET' if env_key else '✗ NOT SET'}")

    return bool(settings.deepseek_api_key)


def test_ai_utils():
    """Test the ai_utils call_deepseek function"""
    print("\n" + "=" * 60)
    print("3. TESTING AI_UTILS FUNCTION")
    print("=" * 60)
    
    test_prompt = "Generate 3 simple search queries for learning Python programming"
    
    try:
        print(f"Testing prompt: {test_prompt}")
        response = call_deepseek(test_prompt)
        
        print(f"✓ Success! Response length: {len(response)} characters")
        print(f"Response preview: {response[:200]}...")
        
        return True, response
        
    except Exception as e:
        print(f"✗ Error: {str(e)}")
        return False, ""


async def test_api_direct():
    """Test direct API call to DeepSeek"""
    print("\n" + "=" * 60)
    print("4. TESTING DIRECT API CALL")
    print("=" * 60)
    
    if not settings.deepseek_api_key:
        print("✗ Cannot test direct API - no API key configured")
        return False, None
    
    import httpx
    
    url = "https://api.deepseek.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {settings.deepseek_api_key}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "deepseek-chat",
        "messages": [
            {"role": "user", "content": "Say 'Hello, API test successful!' and nothing else."}
        ],
        "max_tokens": 50
    }
    
    try:
        print("Making direct API call...")
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(url, headers=headers, json=data)
            
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            content = result["choices"][0]["message"]["content"]
            print(f"✓ Success! Response: {content}")
            return True, content
        else:
            print(f"✗ API Error: {response.status_code}")
            print(f"Response: {response.text}")
            return False, None
            
    except Exception as e:
        print(f"✗ Exception: {str(e)}")
        return False, None


async def run_all_tests():
    """Run all tests"""
    print("DeepSeek API Test Suite")
    print("=" * 60)
    
    results = {}
    
    # Test 1: Configuration
    results['config'] = test_config()
    
    # Test 3: AI Utils (only if we have API key)
    if settings.deepseek_api_key:
        results['ai_utils'], ai_response = test_ai_utils()
    else:
        results['ai_utils'] = False
        print("\n" + "=" * 60)
        print("3. SKIPPING AI_UTILS TEST - NO API KEY")
        print("=" * 60)
    
    # Test 4: Direct API (only if we have API key)
    if settings.deepseek_api_key:
        results['api_direct'], api_response = await test_api_direct()
    else:
        results['api_direct'] = False
        print("\n" + "=" * 60)
        print("4. SKIPPING DIRECT API TEST - NO API KEY")
        print("=" * 60)
    
    # Test 5: Fallback behavior
    results['fallback'] = test_fallback_behavior()
    
    # Summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    
    for test_name, passed in results.items():
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"{test_name.upper():15} {status}")
    
    total_tests = len(results)
    passed_tests = sum(results.values())
    
    print(f"\nOverall: {passed_tests}/{total_tests} tests passed")
    
    if not results['config']:
        print("\n🚨 NEXT STEPS:")
        print("1. Create backend/.env file")
        print("2. Add: DEEPSEEK_API_KEY=sk-your_actual_key_here")
        print("3. Get API key from: https://platform.deepseek.com/")
        print("4. Restart Docker containers: docker-compose down && docker-compose up -d")
    elif passed_tests == total_tests:
        print("\n🎉 All tests passed! DeepSeek API is working correctly.")
        return 0  # Success exit code
    else:
        print("\n⚠️  Some tests failed. Check the logs above for details.")
        return 1  # Failure exit code


if __name__ == "__main__":
    exit_code = asyncio.run(run_all_tests())
    sys.exit(exit_code)
