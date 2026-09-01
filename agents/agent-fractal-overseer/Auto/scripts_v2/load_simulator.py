import requests
import time
import concurrent.futures
import argparse

def send_request(url):
    try:
        response = requests.get(url, timeout=1)
        return response.status_code
    except Exception:
        return None

def simulate_load(url, rps, duration):
    print(f"Simulating {rps} requests per second to {url} for {duration} seconds...")
    start_time = time.time()
    total_requests = 0
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=rps) as executor:
        while time.time() - start_time < duration:
            cycle_start = time.time()
            futures = [executor.submit(send_request, url) for _ in range(rps)]
            total_requests += rps
            
            # Sleep to maintain RPS
            elapsed = time.time() - cycle_start
            if elapsed < 1:
                time.sleep(1 - elapsed)
    
    print(f"Finished simulation. Total requests sent: {total_requests}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Load Simulator for DevOps Squad")
    parser.add_argument("--url", default="http://localhost:3000", help="Target URL")
    parser.add_argument("--rps", type=int, default=10, help="Requests per second")
    parser.add_argument("--duration", type=int, default=60, help="Duration in seconds")
    
    args = parser.parse_args()
    simulate_load(args.url, args.rps, args.duration)
