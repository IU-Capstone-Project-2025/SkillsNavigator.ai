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
    logger.info("=" * 60)
    logger.info("1. TESTING CONFIGURATION")
    logger.info("=" * 60)

    logger.info(f"DeepSeek API Key: {'✓ SET' if settings.deepseek_api_key else '✗ NOT SET'}")

    logger.info(f"DeepSeek API URL: {settings.deepseek_api_url}")

    # Check environment variable directly
    env_key = os.getenv("DEEPSEEK_API_KEY")
    logger.info(f"Environment variable: {'✓ SET' if env_key else '✗ NOT SET'}")

    return bool(settings.deepseek_api_key)


async def test_deepseek_service():
    """Test the DeepseekService class"""
    logger.info("\n" + "=" * 60)
    logger.info("2. TESTING DEEPSEEK SERVICE")
    logger.info("=" * 60)

    service = DeepseekService()

    logger.info(f"Service API Key: {'✓ SET' if service.api_key else '✗ NOT SET'}")
    logger.info(f"Service API URL: {service.api_url}")

    # Test with sample data
    test_area = "Web Development"
    test_level = "beginner"
    test_skills = "React and JavaScript"

    logger.info(f"\nTesting with:")
    logger.info(f"  Area: {test_area}")
    logger.info(f"  Level: {test_level}")
    logger.info(f"  Skills: {test_skills}")

    try:
        logger.info("\nCalling generate_search_queries...")
        queries = await service.generate_search_queries(
            area=test_area,
            current_level=test_level,
            desired_skills=test_skills
        )

        logger.info(f"✓ Success! Generated {len(queries)} queries:")
        for i, query in enumerate(queries, 1):
            logger.info(f"  {i}. {query}")

        return True, queries

    except Exception as e:
        logger.info(f"✗ Error: {str(e)}")
        return False, []


def test_ai_utils():
    """Test the ai_utils call_deepseek function"""
    logger.info("\n" + "=" * 60)
    logger.info("3. TESTING AI_UTILS FUNCTION")
    logger.info("=" * 60)

    test_prompt = "Generate 3 simple search queries for learning Python programming"

    try:
        logger.info(f"Testing prompt: {test_prompt}")
        response = call_deepseek(test_prompt)

        logger.info(f"✓ Success! Response length: {len(response)} characters")
        logger.info(f"Response preview: {response[:200]}...")

        return True, response

    except Exception as e:
        logger.info(f"✗ Error: {str(e)}")
        return False, ""


async def test_api_direct():
    """Test direct API call to DeepSeek"""
    logger.info("\n" + "=" * 60)
    logger.info("4. TESTING DIRECT API CALL")
    logger.info("=" * 60)

    if not settings.deepseek_api_key:
        logger.info("✗ Cannot test direct API - no API key configured")
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
        logger.info("Making direct API call...")
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(url, headers=headers, json=data)

        logger.info(f"Status Code: {response.status_code}")

        if response.status_code == 200:
            result = response.json()
            content = result["choices"][0]["message"]["content"]
            logger.info(f"✓ Success! Response: {content}")
            return True, content
        else:
            logger.info(f"✗ API Error: {response.status_code}")
            logger.info(f"Response: {response.text}")
            return False, None

    except Exception as e:
        logger.info(f"✗ Exception: {str(e)}")
        return False, None


def test_fallback_behavior():
    """Test the fallback behavior when API is not available"""
    logger.info("\n" + "=" * 60)
    logger.info("5. TESTING FALLBACK BEHAVIOR")
    logger.info("=" * 60)

    # Create a service with no API key to test fallback
    from app.services.deepseek import DeepseekService

    # Temporarily override the API key
    original_key = settings.deepseek_api_key
    settings.deepseek_api_key = ""

    try:
        service = DeepseekService()

        # Test fallback queries
        fallback_queries = service._generate_fallback_queries(
            area="Python Programming",
            current_level="beginner",
            desired_skills="web development"
        )

        logger.info(f"✓ Fallback generated {len(fallback_queries)} queries:")
        for i, query in enumerate(fallback_queries, 1):
            logger.info(f"  {i}. {query}")

        return True

    finally:
        # Restore original API key
        settings.deepseek_api_key = original_key


async def run_all_tests():
    """Run all tests"""
    logger.info("DeepSeek API Test Suite")
    logger.info("=" * 60)

    results = {}

    # Test 1: Configuration
    results['config'] = test_config()

    # Test 2: DeepSeek Service
    results['service'], service_queries = await test_deepseek_service()

    # Test 3: AI Utils (only if we have API key)
    if settings.deepseek_api_key:
        results['ai_utils'], ai_response = test_ai_utils()
    else:
        results['ai_utils'] = False
        logger.info("\n" + "=" * 60)
        logger.info("3. SKIPPING AI_UTILS TEST - NO API KEY")
        logger.info("=" * 60)

    # Test 4: Direct API (only if we have API key)
    if settings.deepseek_api_key:
        results['api_direct'], api_response = await test_api_direct()
    else:
        results['api_direct'] = False
        logger.info("\n" + "=" * 60)
        logger.info("4. SKIPPING DIRECT API TEST - NO API KEY")
        logger.info("=" * 60)

    # Test 5: Fallback behavior
    results['fallback'] = test_fallback_behavior()

    # Summary
    logger.info("\n" + "=" * 60)
    logger.info("TEST SUMMARY")
    logger.info("=" * 60)

    for test_name, passed in results.items():
        status = "✓ PASS" if passed else "✗ FAIL"
        logger.info(f"{test_name.upper():15} {status}")

    total_tests = len(results)
    passed_tests = sum(results.values())

    logger.info(f"\nOverall: {passed_tests}/{total_tests} tests passed")

    if not results['config']:
        logger.info("\n🚨 NEXT STEPS:")
        logger.info("1. Create backend/.env file")
        logger.info("2. Add: DEEPSEEK_API_KEY=sk-your_actual_key_here")
        logger.info("3. Get API key from: https://platform.deepseek.com/")
        logger.info("4. Restart Docker containers: docker-compose down && docker-compose up -d")
    elif passed_tests == total_tests:
        logger.info("\n🎉 All tests passed! DeepSeek API is working correctly.")
        return 0  # Success exit code
    else:
        logger.info("\n⚠️  Some tests failed. Check the logs above for details.")
        return 1  # Failure exit code


if __name__ == "__main__":
    exit_code = asyncio.run(run_all_tests())
    sys.exit(exit_code)
