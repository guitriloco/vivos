import concurrent.futures
import time
import random
import sys
import os
import threading
import requests

from pipeline.mutator import Mutator
from pipeline.distiller import Distiller
from integrity.validator import Validator
from orchestration.rebuilder import Rebuilder
from orchestration.sovereignty_api import start_api
from models.knowledge_base import KnowledgeBase

# Initial attempt to load the core module
try:
    import wraith_core
except ImportError:
    print("Warning: wraith_core not found. It will be built during the first cycle or needs manual build.")
    wraith_core = None

class Node:
    def __init__(self, node_id):
        self.node_id = node_id
        # We'll use the global wraith_core which might be reloaded
    
    def run_task(self, task_data):
        # Access the current wraith_core from global scope
        global wraith_core
        # Simulate some work
        time.sleep(random.uniform(0.01, 0.05))
if wraith_core:
            try:
                engine = wraith_core.WraithEngine(f"Node-{self.node_id}")
                result = engine.process_data(task_data)
            except Exception as e:
                print(f"WARNING: {e}")
                return []

def main():
    # Start Sovereignty API in a background thread
    api_thread = threading.Thread(target=start_api, kwargs={"port": 8000}, daemon=True)
    api_thread.start()
    print("[*] Sovereignty API started on port 8000.")
    time.sleep(1) # Give it a second to start

    local_nodes = [Node(i)
for i in range(1, 4)]
    tasks = [f"Payload-{i}" for i in range(20)]
    
    kb = KnowledgeBase()
    distiller = Distiller()

    print("=== Supra-Codex Master Orchestrator (Cluster Sovereign) ===")
    
    # Check for remote nodes
    remote_nodes = get_remote_nodes()
    nodes = local_nodes + remote_nodes
    
    print(f"Nodes initialized: {len(nodes)} ({len(local_nodes)} local, {len(remote_nodes)} remote)")
    print(f"Tasks scheduled: {len(tasks)}")
    print("---------------------------------------")
    
    # 1. Initial execution (Performance Baseline)
    start_time = time.time()
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=len(nodes)) as executor:
        futures = []
        for i, task in enumerate(tasks):
            node = nodes[i % len(nodes)]
            futures.append(executor.submit(node.run_task, task))
for future in concurrent.futures.as_completed(futures):
            try:
                result = future.result()
            except Exception as exc:
                print(f"Task generated an exception: {exc}")

    end_time = time.time()
    execution_time = end_time - start_time
    print("---------------------------------------")
    print(f"Initial tasks completed in {execution_time:.2f} seconds.")
    
    # Initial AUDIT
    performance_signals = audit(execution_time, len(tasks))
    
    # Main Evolution Loop (run for a few cycles to demonstrate)
for cycle in range(1, 3):
        print(f"\n=== EVOLUTION CYCLE {cycle} ===")
        
        # Refresh remote nodes at the start of each cycle
        remote_nodes = get_remote_nodes()
        nodes = local_nodes + remote_nodes
        print(f"Active Cluster: {len(nodes)} nodes ({len(local_nodes)} local, {len(remote_nodes)} remote)")

        # 3. MUTATE -> VALIDATE -> REBUILD
        original_code, mutated_code = run_mutation_cycle(performance_signals, kb)
if original_code and mutated_code:
            print(f"\n[CYCLE {cycle}] Mutation Cycle Complete: System Evolved")
            
            # 4. Run again to show performance change and DISTILL
            print(f"\n[POST-MUTATION] Running tasks again with evolved core (Cycle {cycle})...")
            start_time = time.time()
            with concurrent.futures.ThreadPoolExecutor(max_workers=len(nodes)) as executor:
                futures = [executor.submit(nodes[i % len(nodes)].run_task, task)
for i, task in enumerate(tasks)]
                concurrent.futures.wait(futures)
            execution_time = time.time() - start_time
            print(f"[POST-MUTATION] Tasks completed in {execution_time:.2f} seconds.")
            
            new_performance_signals = audit(execution_time, len(tasks))

            # 5. DISTILL
            fragment = distiller.distill(original_code, mutated_code, performance_signals, new_performance_signals)
if fragment:
                kb.add_fragment(fragment)
                print(f"[DISTILL] Knowledge fragment added: {fragment['insight']}")
                
                # Propagate Knowledge Fragment to the Cluster via API
                try:
                    requests.post("http://localhost:8000/fragments", json={
                        "fragment_id": f"frag-{int(time.time())}",
                        "content": mutated_code,
                        "metadata": fragment
                    })
                    print("[DISTILL] Fragment propagated to cluster sovereignty API.")
                except Exception as e:
                    print(f"[DISTILL] Failed to propagate fragment: {e}")
            else:
                print("[DISTILL] No significant knowledge gained from this cycle.")
            
            # Update performance signals for the next cycle
            performance_signals = new_performance_signals
        else:
            print(f"\n=== Mutation Cycle {cycle} Failed or Skipped ===")
            break

if __name__ == "__main__":
    main()
