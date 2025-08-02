#!/usr/bin/env python3
"""
Simple test script for non-Docker deployment
Tests systemd services and nginx load balancer
"""

import requests
import time
import subprocess
import sys

def check_service_status(service_name):
    """Check if systemd service is running"""
    try:
        result = subprocess.run(['systemctl', 'is-active', service_name], 
                              capture_output=True, text=True)
        return result.stdout.strip() == 'active'
    except:
        return False

def test_server(url, name):
    """Test if server is responding"""
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
    """Test nginx load balancer"""
    print(f"\n🔄 Testing nginx load balancer ({rounds} requests)...")
    
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

def main():
    print("🧪 Stock Market Aggregator - No Docker Deployment Test")
    print("=" * 55)
    
    # Check systemd services
    print("🔍 Checking systemd services...")
    if check_service_status('stock-market-app'):
        print("✅ stock-market-app service is running")
    else:
        print("❌ stock-market-app service not running")
    
    if check_service_status('nginx'):
        print("✅ nginx service is running")
    else:
        print("❌ nginx service not running")
    
    print()
    
    # Test URLs
    web01_url = "http://172.20.0.11:8080"
    web02_url = "http://172.20.0.12:8080"
    lb_url = "http://localhost"  # nginx on port 80
    
    if len(sys.argv) > 1:
        lb_url = sys.argv[1]
    
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
    else:
        print("\n⚠️  Skipping load balancer tests due to server issues")
    
    print("\n" + "=" * 55)
    if web01_ok and web02_ok:
        print("🎉 No-Docker deployment test completed successfully!")
    else:
        print("⚠️  Some issues found. Check server configurations.")

if __name__ == "__main__":
    main()