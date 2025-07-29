#!/usr/bin/env python3
"""
Test script for Stock Market Data & News Aggregator
Run this to verify all components are working correctly
"""

import requests
import json
import time

BASE_URL = "http://localhost:8080"

def test_main_page():
    """Test if main page loads"""
    try:
        response = requests.get(BASE_URL)
        if response.status_code == 200:
            print("✓ Main page loads successfully")
            return True
        else:
            print(f"✗ Main page failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"✗ Main page error: {e}")
        return False

def test_stock_api():
    """Test stock API endpoint"""
    try:
        response = requests.get(f"{BASE_URL}/api/stock/AAPL")
        if response.status_code == 200:
            data = response.json()
            print(f"✓ Stock API works: AAPL = ${data.get('price', 'N/A')}")
            return True
        else:
            print(f"✗ Stock API failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"✗ Stock API error: {e}")
        return False

def test_news_api():
    """Test general news API endpoint"""
    try:
        response = requests.get(f"{BASE_URL}/api/news")
        if response.status_code == 200:
            data = response.json()
            articles = data.get('articles', [])
            print(f"✓ News API works: Found {len(articles)} articles")
            return True
        else:
            print(f"✗ News API failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"✗ News API error: {e}")
        return False

def test_symbol_news_api():
    """Test symbol-specific news API endpoint"""
    try:
        response = requests.get(f"{BASE_URL}/api/news/AAPL")
        if response.status_code == 200:
            data = response.json()
            articles = data.get('articles', [])
            print(f"✓ Symbol News API works: Found {len(articles)} AAPL articles")
            return True
        else:
            print(f"✗ Symbol News API failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"✗ Symbol News API error: {e}")
        return False

def test_main_functionality():
    """Test main stock data endpoint"""
    try:
        payload = {"symbols": "AAPL,MSFT"}
        response = requests.post(f"{BASE_URL}/get_stock_data", 
                               json=payload,
                               headers={'Content-Type': 'application/json'})
        if response.status_code == 200:
            data = response.json()
            stock_count = len(data.get('stock_data', []))
            news_count = len(data.get('news_data', []))
            print(f"✓ Main functionality works: {stock_count} stocks, {news_count} news articles")
            return True
        else:
            print(f"✗ Main functionality failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"✗ Main functionality error: {e}")
        return False

def main():
    print("Testing Stock Market Data & News Aggregator")
    print("=" * 50)
    print("Make sure the Flask app is running on localhost:8080")
    print("=" * 50)
    
    # Wait a moment for user to start the app
    input("Press Enter when the app is running...")
    
    tests = [
        test_main_page,
        test_stock_api,
        test_news_api,
        test_symbol_news_api,
        test_main_functionality
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
            time.sleep(1)  # Brief pause between tests
        except Exception as e:
            print(f"✗ Test failed with exception: {e}")
    
    print("=" * 50)
    print(f"Tests completed: {passed}/{total} passed")
    
    if passed == total:
        print("🎉 All tests passed! Your application is working correctly.")
    else:
        print("⚠️  Some tests failed. Check your API keys and configuration.")

if __name__ == "__main__":
    main()