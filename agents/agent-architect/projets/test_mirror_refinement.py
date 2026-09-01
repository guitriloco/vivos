import asyncio
import time
from Mirror_Protocol.hyper import protocol, nexus_refined
from Mirror_Protocol.registry import registry

async def mock_nov_observer(data):
    print(f"[Nov] Observing protocol event with data: {data}")
    return "Observed"

async def test_refinement():
    # Register an expansion node
    registry.register_node("Nov", mock_nov_observer)
    
    objective = "MAX_SOVEREIGNTY_EXPANSION"
    
    print("--- ⚜️ Turn 1: Cold Start ---")
    start = time.time()
    res1 = await protocol.run_protocol(objective)
    print(f"Time taken: {time.time() - start:.4f}s")
    
    print("\n--- ⚜️ Turn 2: Exact Match (Cached) ---")
    start = time.time()
    res2 = await protocol.run_protocol(objective)
    print(f"Time taken: {time.time() - start:.4f}s")
    print(f"Result 2 has 'Pure_Gold': {'Pure_Gold' in res2}")
    
    print("\n--- ⚜️ Turn 3: Fuzzy Match (Similarity) ---")
    objective_similar = "MAX_SOVEREIGNTY_INTEGRATION"
    start = time.time()
    res3 = await protocol.run_protocol(objective_similar)
    print(f"Time taken: {time.time() - start:.4f}s")
    
    print("\n--- ⚜️ Performance Report ---")
    report = nexus_refined.get_performance_report()
    print(report)

if __name__ == "__main__":
    asyncio.run(test_refinement())
