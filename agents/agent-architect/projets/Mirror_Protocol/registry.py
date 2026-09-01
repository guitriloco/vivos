import asyncio
from typing import Dict, Any, Callable

class ExpansionRegistry:
    """
    Registry for Expansion Nodes (Nov, Yes, vvv).
    Allows the Mirror Protocol to trigger specific logic in these nodes.
    """
    def __init__(self):
        self.nodes: Dict[str, Callable] = {}

    def register_node(self, node_type: str, callback: Callable):
        print(f"[Registry] Node registered: {node_type}")
        self.nodes[node_type] = callback

    async def broadcast_signal(self, signal_type: str, data: Any):
        """Send a signal to all registered nodes."""
        print(f"[Registry] Broadcasting signal: {signal_type}")
        results = {}
        for node_type, callback in self.nodes.items():
            try:
                # Simulating async callback
                if asyncio.iscoroutinefunction(callback):
                    res = await callback(data)
                else:
                    res = callback(data)
                results[node_type] = res
            except Exception as e:
                print(f"[Registry] Error calling {node_type}: {e}")
        return results

registry = ExpansionRegistry()
