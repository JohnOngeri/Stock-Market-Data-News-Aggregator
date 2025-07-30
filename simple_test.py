#!/usr/bin/env python3
"""
Simple test script for Stock Market Data & News Aggregator
This script provides a quick way to verify the application is working correctly.
"""

import requests
import json
import sys
import os
from datetime import datetime

def test_home_page(base_url):
    """Test that the home page loads correctly"""
    try:
        response = requests.get(base_url, timeout=10)
        if response.status_code == 200:
            print("✅ Home page loads successfully")
            return True
        else:
            print(f"❌ Home page failed with status code: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Home page test failed: {e}")
        return False

def test_stock_api(base_url):
    """Test the stock API endpoint"""
    try:
        response = requests.get(f"{base_url}/api/stock/AAPL", timeout=10)
        if response.status_code == 200:
            data = response.json()
            if 'symbol' in data and 'price' in data:
                print("✅ Stock API endpoint working")
                return True
            else:
                print("❌ Stock API returned invalid data format")
                return False
        else:
            print(f"❌ Stock API failed with status code: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Stock API test failed: {e}")
        return False

def test_news_api(base_url):
    """Test the news API endpoint"""
    try:
        response = requests.get(f"{base_url}/api/news", timeout=10)
        if response.status_code == 200:
            data = response.json()
            if 'articles' in data:
                print("✅ News API endpoint working")
                return True
            else:
                print("❌ News API returned invalid data format")
                return False
        else:
            print(f"❌ News API failed with status code: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ News API test failed: {e}")
        return False

def test_post_endpoint(base_url):
    """Test the POST endpoint for stock data"""
    try:
        payload = {"symbols": "AAPL,MSFT"}
        response = requests.post(f"{base_url}/get_stock_data", 
                               json=payload, timeout=15)
        if response.status_code == 200:
            data = response.json()
            if 'stock_data' in data and 'news_data' in data:
                print("✅ POST endpoint working")
                return True
            else:
                print("❌ POST endpoint returned invalid data format")
                return False
        else:
            print(f"❌ POST endpoint failed with status code: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ POST endpoint test failed: {e}")
        return False

def test_static_files(base_url):
    """Test that static files are served correctly"""
    try:
        # Test CSS file
        response = requests.get(f"{base_url}/static/css/style.css", timeout=10)
        if response.status_code == 200:
            print("✅ CSS file served correctly")
        else:
            print("❌ CSS file not found")
            return False
        
        # Test JavaScript file
        response = requests.get(f"{base_url}/static/js/main.js", timeout=10)
        if response.status_code == 200:
            print("✅ JavaScript file served correctly")
            return True
        else:
            print("❌ JavaScript file not found")
            return False
    except Exception as e:
        print(f"❌ Static files test failed: {e}")
        return False

def test_error_handling(base_url):
    """Test error handling for invalid endpoints"""
    try:
        response = requests.get(f"{base_url}/nonexistent", timeout=10)
        if response.status_code == 404:
            print("✅ 404 error handling working")
            return True
        else:
            print(f"❌ 404 error handling failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error handling test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🧪 Stock Market Data & News Aggregator - Simple Test")
    print("=" * 60)
    print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Get base URL from command line or use default
    if len(sys.argv) > 1:
        base_url = sys.argv[1].rstrip('/')
    else:
        base_url = "http://localhost:8080"
    
    print(f"Testing application at: {base_url}")
    print()
    
    # Run tests
    tests = [
        ("Home Page", test_home_page),
        ("Stock API", test_stock_api),
        ("News API", test_news_api),
        ("POST Endpoint", test_post_endpoint),
        ("Static Files", test_static_files),
        ("Error Handling", test_error_handling)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"Testing {test_name}...")
        if test_func(base_url):
            passed += 1
        print()
    
    # Summary
    print("=" * 60)
    print(f"Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Application is working correctly.")
        return 0
    else:
        print("⚠️  Some tests failed. Please check the application.")
        return 1

if __name__ == "__main__":
    sys.exit(main()) 