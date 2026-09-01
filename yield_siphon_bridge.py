#!/usr/bin/env python3
"""
🔱 C++ YIELD SIPHON BINDING — Python Wrapper 🔱
Bridge between C++ core and Python modules.
Optimized for Phase 16/17 Cross-Pillar Speedup.

Exports:
  YieldSiphonBridge — Full class wrapper (recommended for new code)
  CppEngine         — Alias for YieldSiphonBridge (used by optimized modules)
  run_benchmark(n)  — Standalone benchmark function returning avg ns/op
"""
import ctypes
import os

_LIB_CACHE = None

def _get_lib():
    global _LIB_CACHE
    if _LIB_CACHE is not None:
        return _LIB_CACHE
    lib_path = "/home/team/shared/V16_TRANSMUTED_CORE/libsiphon_bridge.so"
    if not os.path.exists(lib_path):
        raise RuntimeError(f"Cannot find C++ shared library: {lib_path}")
    lib = ctypes.CDLL(lib_path)
    _LIB_CACHE = lib
    return lib


class YieldSiphonBridge:
    """C++ Arbitrage Engine bridge via ctypes.

    Wraps every engine function with nanosecond-precision latency measurement.
    """

    def __init__(self, threshold=0.005):
        self.lib = _get_lib()
        # Define types
        self.lib.engine_create.restype = ctypes.c_void_p
        self.lib.engine_create.argtypes = [ctypes.c_double]
        self.lib.engine_destroy.argtypes = [ctypes.c_void_p]
        self.lib.engine_update_solana.restype = ctypes.c_int64
        self.lib.engine_update_solana.argtypes = [ctypes.c_void_p, ctypes.c_double]
        self.lib.engine_update_base.restype = ctypes.c_int64
        self.lib.engine_update_base.argtypes = [ctypes.c_void_p, ctypes.c_double]
        self.lib.engine_get_spread.restype = ctypes.c_double
        self.lib.engine_get_spread.argtypes = [ctypes.c_void_p]
        self.lib.engine_get_trades.restype = ctypes.c_uint64
        self.lib.engine_get_trades.argtypes = [ctypes.c_void_p]
        self.lib.engine_get_latency.restype = ctypes.c_int64
        self.lib.engine_get_latency.argtypes = [ctypes.c_void_p]
        self.lib.run_benchmark.restype = ctypes.c_double
        self.lib.run_benchmark.argtypes = [ctypes.c_int]
        # Initialize
        self.ptr = self.lib.engine_create(ctypes.c_double(threshold))

    def __del__(self):
        if hasattr(self, 'ptr') and self.ptr:
            self.lib.engine_destroy(self.ptr)

    def update_solana(self, price):
        """Update SOLANA price. Returns latency in nanoseconds."""
        return self.lib.engine_update_solana(self.ptr, ctypes.c_double(price))

    def update_base(self, price):
        """Update BASE price. Returns latency in nanoseconds."""
        return self.lib.engine_update_base(self.ptr, ctypes.c_double(price))

    def get_spread(self):
        """Get current SOLANA/BASE spread ratio."""
        return self.lib.engine_get_spread(self.ptr)

    def get_trades(self):
        """Get arbitrage trade count."""
        return self.lib.engine_get_trades(self.ptr)

    def get_latency(self):
        """Get last operation latency in nanoseconds."""
        return self.lib.engine_get_latency(self.ptr)


def run_benchmark(iterations=100000):
    """Run standalone C++ benchmark.

    Returns average nanoseconds per operation across *iterations* rounds.
    This function is independent of any YieldSiphonBridge instance.
    """
    lib = _get_lib()
    lib.run_benchmark.restype = ctypes.c_double
    lib.run_benchmark.argtypes = [ctypes.c_int]
    return lib.run_benchmark(ctypes.c_int(iterations))


# Alias for backward compatibility with optimized modules
CppEngine = YieldSiphonBridge


if __name__ == "__main__":
    import time
    bridge = YieldSiphonBridge(0.005)
    print("=== C++ Bridge Test ===")
    bridge.update_solana(145.0)
    bridge.update_base(146.0)
    print(f"  Spread: {bridge.get_spread():.6f}")
    print(f"  Trades: {bridge.get_trades()}")
    avg_ns = run_benchmark(50000)
    print(f"  C++ Native: {avg_ns:.3f} ns/op ({avg_ns/1000:.3f} us)")
    print("TOTAL AFIRMAÇÃO.")