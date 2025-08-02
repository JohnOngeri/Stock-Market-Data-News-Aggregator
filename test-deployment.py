#!/usr/bin/env python3
"""
Simple deployment test script for Stock Market Aggregator
Tests both individual servers and load balancer
"""

import requests
import time
import sys

def test_server(url, name):
    """Test if a server is responding"""
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            print(f"✅ {name} is working")
            return True
        else:
            print(f"❌ {name} returned status {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ {name} failed: {e}")
        return False

def test_load_balancer(lb_url, rounds=6):
    """Test load balancer round-robin"""
    print(f"\n🔄 Testing load balancer round-robin ({rounds} requests)...")
    
    for i in range(rounds):
        try:
            response = requests.get(lb_url, timeout=10)
            if response.status_code == 200:
                print(f"Request {i+1}: ✅ Success")
            else:
                print(f"Request {i+1}: ❌ Status {response.status_code}")
            time.sleep(1)
        except Exception as e:
            print(f"Request {i+1}: ❌ Failed - {e}")

def test_api_functionality(base_url):
    """Test API endpoints"""
    print(f"\n🧪 Testing API functionality...")
    
    # Test stock API
    try:
        response = requests.get(f"{base_url}/api/stock/AAPL", timeout=15)
        if response.status_code == 200:
            print("✅ Stock API working")
        else:
            print("❌ Stock API failed")
    except Exception as e:
        print(f"❌ Stock API error: {e}")
    
    # Test news API
    try:
        response = requests.get(f"{base_url}/api/news", timeout=15)
        if response.status_code == 200:
            print("✅ News API working")
        else:
            print("❌ News API failed")
    except Exception as e:
        print(f"❌ News API error: {e}")

def main():
    print("🧪 Stock Market Aggregator - Deployment Test")
    print("=" * 50)
    
    # Default URLs - modify these for your setup
    web01_url = "http://172.20.0.11:8080"
    web02_url = "http://172.20.0.12:8080"
    lb_url = "http://your-lb-ip"  # Replace with actual LB IP
    
    # Allow custom URLs from command line
    if len(sys.argv) > 1:
        lb_url = sys.argv[1]
    if len(sys.argv) > 2:
        web01_url = sys.argv[2]
    if len(sys.argv) > 3:
        web02_url = sys.argv[3]
    
    print(f"Testing URLs:")
    print(f"  Load Balancer: {lb_url}")
    print(f"  Web01: {web01_url}")
    print(f"  Web02: {web02_url}")
    print()
    
    # Test individual servers
    print("🖥️  Testing individual servers...")
    web01_ok = test_server(web01_url, "Web01")
    web02_ok = test_server(web02_url, "Web02")
    
    # Test load balancer
    if web01_ok and web02_ok:
        test_load_balancer(lb_url)
        test_api_functionality(lb_url)
    else:
        print("\n⚠️  Skipping load balancer tests due to server issues")
    
    print("\n" + "=" * 50)
    if web01_ok and web02_ok:
        print("🎉 Deployment test completed successfully!")
    else:
        print("⚠️  Some issues found. Check server configurations.")

if __name__ == "__main__":
    main()