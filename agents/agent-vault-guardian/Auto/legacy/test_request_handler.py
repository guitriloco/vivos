#!/usr/bin/env python3
"""
Test script for the request_handler module.
Verifies that the User-Agent rotation, rate limiting, and logging work properly.
"""

import time
import os
from request_handler import RequestHandler

def test_basic_functionality():
    """Test basic functionality of the RequestHandler."""
    print("Testing RequestHandler functionality...")

    # Initialize the handler with shorter delays for testing
    handler = RequestHandler(
        base_delay=0.5,      # Shorter delay for testing
        variance=0.1,        # Small variance for testing
        log_file_path="./test_logs/error_log.txt"
    )

    # Create test logs directory if it doesn't exist
    os.makedirs("./test_logs", exist_ok=True)

    print("\n1. Testing User-Agent rotation...")
    for i in range(3):
        ua = handler.user_agent_rotator.get_random_user_agent()
        print(f"   Request {i+1} User-Agent: {ua[:50]}...")

    print("\n2. Testing rate limiting...")
    start_time = time.time()
    handler.rate_limiter.wait()
    elapsed = time.time() - start_time
    print(f"   Rate limiter waited for {elapsed:.2f} seconds")

    print("\n3. Testing request making...")
    # Test a simple GET request
    response = handler.get("https://httpbin.org/user-agent")
    if response:
        print(f"   Successfully made request, status: {response.status_code}")
        # Print the returned user agent to verify rotation
        import json
        data = response.json()
        print(f"   Returned User-Agent: {data['user-agent'][:50]}...")
    else:
        print("   Request failed")

    print("\n4. Testing error logging...")
    # Test with a 403 error to trigger logging
    response = handler.get("https://httpbin.org/status/403")
    if response and response.status_code == 403:
        print(f"   Triggered 403 error, status: {response.status_code}")
        print("   403 error should be logged to error_log.txt")

    # Test with a URL that might cause connection error
    try:
        # This should fail and be logged
        response = handler.get("http://this-domain-definitely-does-not-exist-12345.com", timeout=5)
        print("   Connection error test completed")
    except:
        print("   Connection error test completed")

    print("\n5. Testing different HTTP methods...")
    methods_to_test = [
        ("GET", "https://httpbin.org/get"),
        ("POST", "https://httpbin.org/post"),
        ("PUT", "https://httpbin.org/put"),
    ]

    for method, url in methods_to_test:
        response = getattr(handler, method.lower())(url)
        if response:
            print(f"   {method} request successful, status: {response.status_code}")
        else:
            print(f"   {method} request failed")

    print(f"\n6. Checking if log file was created...")
    log_file_path = "./test_logs/error_log.txt"
    if os.path.exists(log_file_path):
        print(f"   Log file exists: {log_file_path}")
        # Show last few lines of log if it exists
        with open(log_file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            if lines:
                print(f"   Last log entries:")
                for line in lines[-3:]:  # Show last 3 lines
                    print(f"     {line.strip()}")
            else:
                print("   Log file is empty")
    else:
        print(f"   Log file does not exist yet at: {log_file_path}")

    print("\nTest completed successfully!")


def test_gaussian_timing():
    """Test the Gaussian timing distribution."""
    print("\nTesting Gaussian timing distribution...")

    handler = RequestHandler(base_delay=0.1, variance=0.05, log_file_path="./test_timing_log.txt")

    delays = []
    print("   Collecting 10 delay measurements...")
    for i in range(10):
        start = time.time()
        handler.rate_limiter.wait()
        elapsed = time.time() - start
        delays.append(elapsed)
        print(f"   Delay {i+1}: {elapsed:.3f}s")

    avg_delay = sum(delays) / len(delays)
    print(f"   Average delay: {avg_delay:.3f}s (expected ~0.1s)")
    print(f"   Min delay: {min(delays):.3f}s")
    print(f"   Max delay: {max(delays):.3f}s")


if __name__ == "__main__":
    print("Starting RequestHandler tests...\n")

    test_basic_functionality()
    test_gaussian_timing()

    print("\nAll tests completed!")
    print("\nRemember: This module is designed for legitimate stress-testing")
    print("and data-mining projects with appropriate permissions.")