#!/usr/bin/env python3
"""
Test script to verify API connections and application functionality
"""

import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

def test_alpha_vantage():
    """Test Alpha Vantage API connection"""
    api_key = os.getenv("ALPHA_VANTAGE_API_KEY")
    if not api_key or api_key == "demo":
        print("ERROR: Alpha Vantage API key not set (using demo)")
        return False
    
    url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol=AAPL&apikey={api_key}"
    try:
        response = requests.get(url, timeout=10)
        data = response.json()
        if "Global Quote" in data:
            print("SUCCESS: Alpha Vantage API connected")
            return True
        else:
            print(f"ERROR: Alpha Vantage API error: {data}")
            return False
    except Exception as e:
        print(f"ERROR: Alpha Vantage API failed: {e}")
        return False

def test_news_api():
    """Test NewsAPI connection"""
    api_key = os.getenv("NEWS_API_KEY")
    if not api_key or api_key == "demo":
        print("ERROR: NewsAPI key not set (using demo)")
        return False
    
    url = f"https://newsapi.org/v2/everything?q=finance&apiKey={api_key}&pageSize=1"
    try:
        response = requests.get(url, timeout=10)
        data = response.json()
        if data.get("status") == "ok":
            print("SUCCESS: NewsAPI connected")
            return True
        else:
            print(f"ERROR: NewsAPI error: {data}")
            return False
    except Exception as e:
        print(f"ERROR: NewsAPI failed: {e}")
        return False

def test_flask_app():
    """Test if Flask app is running"""
    try:
        response = requests.get("http://localhost:8080", timeout=5)
        if response.status_code == 200:
            print("SUCCESS: Flask app is running")
            return True
        else:
            print(f"ERROR: Flask app returned status {response.status_code}")
            return False
    except Exception as e:
        print(f"ERROR: Flask app not accessible: {e}")
        return False

def test_api_endpoints():
    """Test Flask API endpoints"""
    base_url = "http://localhost:8080"
    
    # Test stock endpoint
    try:
        response = requests.get(f"{base_url}/api/stock/AAPL", timeout=10)
        if response.status_code == 200:
            print("SUCCESS: Stock API endpoint working")
        else:
            print(f"ERROR: Stock API endpoint failed: {response.status_code}")
    except Exception as e:
        print(f"ERROR: Stock API endpoint error: {e}")
    
    # Test news endpoint
    try:
        response = requests.get(f"{base_url}/api/news", timeout=10)
        if response.status_code == 200:
            print("SUCCESS: News API endpoint working")
        else:
            print(f"ERROR: News API endpoint failed: {response.status_code}")
    except Exception as e:
        print(f"ERROR: News API endpoint error: {e}")
    
    # Test POST endpoint
    try:
        payload = {"symbols": "AAPL"}
        response = requests.post(f"{base_url}/get_stock_data", json=payload, timeout=15)
        if response.status_code == 200:
            print("SUCCESS: POST endpoint working")
        else:
            print(f"ERROR: POST endpoint failed: {response.status_code}")
    except Exception as e:
        print(f"ERROR: POST endpoint error: {e}")

def main():
    print("API Connection Test")
    print("=" * 30)
    
    # Test external APIs
    alpha_ok = test_alpha_vantage()
    news_ok = test_news_api()
    
    print("\nFlask Application Test")
    print("=" * 30)
    
    # Test Flask app
    flask_ok = test_flask_app()
    
    if flask_ok:
        test_api_endpoints()
    
    print("\nSummary")
    print("=" * 30)
    if not alpha_ok:
        print("WARNING: Get Alpha Vantage API key: https://www.alphavantage.co/support/#api-key")
    if not news_ok:
        print("WARNING: Get NewsAPI key: https://newsapi.org/register")
    if not flask_ok:
        print("WARNING: Start Flask app: python app.py")
    
    if alpha_ok and news_ok and flask_ok:
        print("SUCCESS: All systems working!")
    else:
        print("WARNING: Some issues found - check above")

if __name__ == "__main__":
    main()