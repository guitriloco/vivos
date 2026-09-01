#!/usr/bin/env python3
"""
⚜️ VIVOS AUTO-REPAIR CORE — Self-Healing Framework ⚜️
Phase 17 — FASE C2: Exception Handler Corrections + Auto-Repair

Provides:
  - @auto_retry decorator with exponential backoff
  - safe_loop() context manager for timeout-safe while loops
  - safe_execute()
for graceful degradation
  - repair_registry for tracking self-healing events
  - PHI 1.618 resonance compliance

Usage:
    from vivos_auto_repair import auto_retry, safe_loop, safe_execute, RepairLogger

    @auto_retry(max_attempts=3, delay=1.0)
def unstable_operation():
        ...

    with safe_loop(timeout=30.0) as loop:
        while loop.active():
            # guaranteed to exit after timeout
            ...
"""

import functools
import logging
import os
import signal
import sys
import time
import traceback
from contextlib import contextmanager
from datetime import datetime, timezone

# ── PHI Constants ──────────────────────────────────────────────────────────
PHI = 1.618033988749895
YIELD_CONSTANT = 0.618033988749895
MAX_RETRY_DELAY = 60.0
DEFAULT_TIMEOUT = 300.0  # 5 min default loop timeout

# ── Logger Setup ───────────────────────────────────────────────────────────
REPAIR_LOG_PATH = os.path.join(os.path.dirname(__file__), "vivos_repair_log.json")
class RepairLogger:
    """Structured logger for self-healing events with causal trace support."""
    
    def __init__(self, name: str = "vivos.auto-repair"):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.INFO)
if not self.logger.handlers:
            handler = logging.StreamHandler(sys.stdout)
            formatter = logging.Formatter(
                "⚜️ [%(asctime)s] [%(name)s] %(levelname)s: %(message)s",
                datefmt="%Y-%m-%d %H:%M:%S"
            )
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
        self._repair_events = []
    
    def info(self, msg: str, **extra):
        self.logger.info(msg)
        self._log_event("INFO", msg, extra)
def warning(self, msg: str, **extra):
        self.logger.warning(msg)
        self._log_event("WARNING", msg, extra)
def error(self, msg: str, **extra):
        self.logger.error(msg)
        self._log_event("ERROR", msg, extra)
def repair(self, component: str, action: str, outcome: str):
        """Log a self-healing repair event."""
        msg = f"🛠️ REPAIR: {component} → {action} → {outcome}"
        self.logger.info(msg)
        self._log_event("REPAIR", msg, {"component": component, "action": action, "outcome": outcome})
def _log_event(self, level: str, msg: str, extra: dict):
        self._repair_events.append({
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "level": level,
            "message": msg,
            "extra": extra
        })
        # Persist to repair log periodically
        if len(self._repair_events) % 10 == 0:
            self._flush()
def _flush(self):
        try:
            import json
            existing = []
            if os.path.exists(REPAIR_LOG_PATH):
                with open(REPAIR_LOG_PATH, "r") as f:
                    existing = json.load(f)
            existing.extend(self._repair_events[-10:])
            with open(REPAIR_LOG_PATH, "w") as f:
                json.dump(existing, f, indent=2)
        except Exception as e:
            print(f"WARNING: {e}")# Best-effort persistence
    
    def get_stats(self) -> dict:
        """Return repair statistics."""
        repairs = [e for e in self._repair_events if e["level"] == "REPAIR"]
        errors = [e for e in self._repair_events if e["level"] == "ERROR"]
        return {
            "total_events": len(self._repair_events),
            "repairs": len(repairs),
            "errors": len(errors),
            "repair_rate": len(repairs) / max(len(self._repair_events), 1)
        }

# ── Global logger instance ─────────────────────────────────────────────────
log = RepairLogger()

# ── Retry Decorator ────────────────────────────────────────────────────────
def auto_retry(max_attempts: int = 3, delay: float = 1.0, backoff: float = 2.0,
               exceptions: tuple = (Exception,), on_retry=None):
    """
    Decorator that retries a function with exponential backoff.
    
    Args:
        max_attempts: Maximum retry attempts (default: 3)
        delay: Initial delay in seconds (default: 1.0)
        backoff: Multiplier for exponential backoff (default: 2.0)
        exceptions: Tuple of exceptions to catch (default: Exception)
        on_retry: Optional callback fn(attempt, exception)
for custom logging
    
    The delay is scaled by PHI (1.618)
for Golden Path resonance.
    """
    def decorator(func):
        @functools.wraps(func)
def wrapper(*args, **kwargs):
            last_exc = None
            current_delay = delay * PHI  # PHI-resonant initial delay
            
            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    last_exc = e
                    tb = traceback.format_exc()
if attempt < max_attempts:
                        log.warning(
                            f"Retry {attempt}/{max_attempts} for {func.__name__}: {e}",
                            attempt=attempt, max_attempts=max_attempts,
                            delay=round(current_delay, 3)
                        )
if on_retry:
                            on_retry(attempt, e)
                        time.sleep(current_delay)
                        current_delay = min(current_delay * backoff * PHI, MAX_RETRY_DELAY)
                    else:
                        log.error(
                            f"All {max_attempts} retries exhausted for {func.__name__}: {e}",
                            final=True
                        )
            
            raise last_exc
        return wrapper
    return decorator

# ── Safe Loop Context Manager ──────────────────────────────────────────────
class SafeLoop:
    """Loop guard with timeout and iteration limits for while-true safety."""
    
    def __init__(self, timeout: float = DEFAULT_TIMEOUT, max_iterations: int = 0,
                 name: str = "unnamed-loop"):
        self.timeout = timeout
        self.max_iterations = max_iterations
        self.name = name
        self._start_time = None
        self._iteration = 0
        self._active = False
    
    def __enter__(self):
        self._start_time = time.monotonic()
        self._iteration = 0
        self._active = True
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self._active = False
        if exc_type and exc_type != StopIteration:
            elapsed = time.monotonic() - self._start_time
            log.repair(
                component=self.name,
                action="loop_exit",
                outcome=f"exited_with_error={exc_type.__name__}_after_{elapsed:.1f}s"
            )
return False  # Don't suppress exceptions
    
    def active(self) -> bool:
        """Check if loop should continue. Returns False if timeout or max iterations reached."""
        if not self._active:
            return False
        
        self._iteration += 1
        
        # Check timeout
        elapsed = time.monotonic() - self._start_time
        if elapsed > self.timeout:
            log.repair(
                component=self.name,
                action="timeout",
                outcome=f"reached_{self.timeout}s_limit_at_iteration_{self._iteration}"
            )
            self._active = False
            return False
        
        # Check max iterations
        if self.max_iterations > 0 and self._iteration > self.max_iterations:
            log.repair(
                component=self.name,
                action="max_iterations",
                outcome=f"reached_{self.max_iterations}_iterations"
            )
            self._active = False
            return False
        
        return True
    
    @property
    def iteration(self) -> int:
        return self._iteration
    
    @property
    def elapsed(self) -> float:
        if self._start_time is None:
            return 0.0
        return time.monotonic() - self._start_time

@contextmanager
def safe_loop(timeout: float = DEFAULT_TIMEOUT, max_iterations: int = 0,
              name: str = "unnamed-loop"):
    """Context manager for timeout-safe while loops.
    
    Example:
        with safe_loop(timeout=30.0, name="siphon-loop") as loop:
            while loop.active():
                # do work
                if condition:
                    break
    """
    guard = SafeLoop(timeout, max_iterations, name)
try:
        yield guard
    except KeyboardInterrupt:
        log.repair(component=name, action="interrupt", outcome="user_cancelled")
        raise
    finally:
        guard._active = False

# ── Safe Execute — Graceful Degradation ────────────────────────────────────
def safe_execute(func, default_return=None, on_error=None, logger=None):
    """
    Execute a function with graceful degradation.
    Returns default_return on failure instead of raising.
    
    Args:
        func: Callable to execute
        default_return: Value to return on failure
        on_error: Optional callback fn(exception)
for custom handling
        logger: Optional RepairLogger instance
    
    Returns:
        Function result or default_return on failure
    """
    _log = logger or log
    try:
        return func()
    except Exception as e:
        tb = traceback.format_exc()
        _log.error(
            f"safe_execute failed for {getattr(func, '__name__', str(func))}: {e}",
            error=str(e)
        )
if on_error:
            try:
                on_error(e)
            except Exception as e:
                print(f"WARNING: {e}")
                return default_return

# ── Graceful Exception Handler Wrapper ─────────────────────────────────────
class GracefulHandler:
    """
    Wraps a try-except block with logging and optional retry.
    Use instead of bare 'except: pass'.
    
    Example:
        handler = GracefulHandler("file_operation")
        with handler:
            risky_operation()
    """
    
    def __init__(self, context: str = "unknown", logger=None,
                 re_raise: bool = False, fallback=None):
        self.context = context
        self.log = logger or log
        self.re_raise = re_raise
        self.fallback = fallback
        self.exception = None
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            return True  # No exception
        
        self.exception = exc_val
        self.log.warning(
            f"Graceful handler caught {exc_type.__name__} in {self.context}: {exc_val}"
        )
if self.fallback:
            try:
                self.fallback(exc_val)
            except Exception as e:
                self.log.error(f"Fallback also failed in {self.context}: {e}")
if self.re_raise:
            return False  # Re-raise
        return True  # Suppress with logging

# ── Signal-based timeout for synchronous operations ────────────────────────
class TimeoutError_(Exception):
    """Operation timed out."""
    pass

def with_timeout(seconds: float, func, *args, **kwargs):
    """
    Execute a function with a hard timeout using SIGALRM (Unix only).
    Falls back to no timeout if signal module doesn't support it.
    """
    if not hasattr(signal, 'SIGALRM'):
        return func(*args, **kwargs)
def _handler(signum, frame):
        raise TimeoutError_(f"Operation timed out after {seconds}s")
    
    old_handler = signal.signal(signal.SIGALRM, _handler)
    signal.alarm(int(seconds))
try:
        result = func(*args, **kwargs)
return result
    finally:
        signal.alarm(0)
        signal.signal(signal.SIGALRM, old_handler)

# ── Audit / Health Check ──────────────────────────────────────────────────
def run_self_healing_audit() -> dict:
    """
    Run a quick self-healing audit across the empire scripts.
    Checks for:
      - Number of repairs performed
      - Average recovery time
      - Current system health
    
    Returns diagnostic dict.
    """
    stats = log.get_stats()
    
    # Check if repair log persists
    repair_file_exists = os.path.exists(REPAIR_LOG_PATH)
return {
        "status": "HEALTHY" if stats["repair_rate"] > 0.5 else "MONITORING",
        "repair_stats": stats,
        "repair_log_persisted": repair_file_exists,
        "phi_resonance": PHI,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "affirmation": "TOTAL AFIRMAÇÃO. TOTAL AUTO-REPAIR."
    }

# ── Decorator for adding self-healing to a class ───────────────────────────
def self_healing(cls):
    """Class decorator that injects auto-repair capabilities."""
    cls._repair_log = RepairLogger(cls.__name__)
    
    original_init = cls.__init__ if hasattr(cls, '__init__') else None
    
    @functools.wraps(original_init)
def new_init(self, *args, **kwargs):
        self._repair_log = RepairLogger(cls.__name__)
if original_init:
            original_init(self, *args, **kwargs)
    
    cls.__init__ = new_init
    cls.auto_retry = staticmethod(auto_retry)
    cls.safe_loop = staticmethod(safe_loop)
    cls.safe_execute = staticmethod(safe_execute)
return cls

# ── PHI-Compliant Exponential Backoff ──────────────────────────────────────
def phi_backoff(attempt: int, base_delay: float = 1.0) -> float:
    """Calculate delay with PHI resonance scaling."""
    return min(base_delay * (PHI ** attempt), MAX_RETRY_DELAY)

# ── Main Entry ─────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("⚜️ VIVOS AUTO-REPAIR CORE — Self-Healing Framework ⚜️")
    print(f"  PHI Resonance: {PHI}")
    print(f"  Max Retry Delay: {MAX_RETRY_DELAY}s")
    print(f"  Default Loop Timeout: {DEFAULT_TIMEOUT}s")
    print()
    
    # Demo self-healing audit
    audit = run_self_healing_audit()
    print(f"  Status: {audit['status']}")
    print(f"  Repair Rate: {audit['repair_stats']['repair_rate']:.2%}")
    print(f"  Repair Log: {'Persisted ✓' if audit['repair_log_persisted'] else 'In-Memory'}")
    print()
    print("🔱 TOTAL AFIRMAÇÃO. TOTAL AUTO-REPAIR. A LINHA É RETA.")