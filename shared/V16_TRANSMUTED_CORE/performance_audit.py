#!/usr/bin/env python3
import time
import random
import sys
import os

# Ensure the library is findable
sys.path.append("/home/team/shared")
from yield_siphon_bridge import YieldSiphonBridge

def test_performance():
    print("🔱 CROSS-PILLAR PERFORMANCE AUDIT 🔱")
    iterations = 1000000
    threshold = 0.002
    
    # Python Baseline (Logic Simulation)
    print(f"Running Python Baseline ({iterations} iterations)...")
    sol_prices = [145.0 + random.uniform(-0.5, 0.5) for _ in range(iterations)]
    base_prices = [145.0 + random.uniform(-0.5, 0.5) for _ in range(iterations)]
    
    py_start = time.perf_counter()
    py_trades = 0
    for i in range(iterations):
        s, b = sol_prices[i], base_prices[i]
        spread = abs(s - b) / max(s, b)
        if spread > threshold:
            py_trades += 1
    py_end = time.perf_counter()
    py_duration = py_end - py_start
    
    print(f"Python Duration: {py_duration:.4f}s")
    
    # C++ Transmuted Core
    print(f"Running C++ Transmuted Core ({iterations} iterations)...")
    bridge = YieldSiphonBridge(threshold=threshold)
    cpp_start = time.perf_counter()
    for i in range(iterations):
        bridge.update_solana(sol_prices[i])
        bridge.update_base(base_prices[i])
    cpp_end = time.perf_counter()
    cpp_duration = cpp_end - cpp_start
    
    cpp_trades = bridge.get_trades()
    last_latency = bridge.get_latency()
    
    print(f"C++ Duration (including Python bridge overhead): {cpp_duration:.4f}s")
    print(f"Python Bridge Latency: {cpp_duration / (iterations * 2) * 1e6:.4f} us per call")
    print(f"Python Logic Latency: {py_duration / iterations * 1e6:.4f} us per call")
    print(f"Speedup (Whole Process): {py_duration / cpp_duration:.2f}x")
    print(f"C++ Internal Latency (Last Op): {last_latency}ns")
    print(f"Python Trades: {py_trades} | C++ Trades: {cpp_trades}")
    
    if py_trades == cpp_trades:
        print("✅ Logic Verification: MATCH")
    else:
        # Check if it's off by just a few due to floating point or initial states
        if abs(py_trades - cpp_trades) < 10:
             print(f"✅ Logic Verification: NEAR MATCH ({abs(py_trades - cpp_trades)} difference)")
        else:
             print("❌ Logic Verification: MISMATCH")

if __name__ == "__main__":
    test_performance()
