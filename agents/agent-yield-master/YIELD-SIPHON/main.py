import os
import sys
import asyncio
import importlib.util
from loguru import logger

# Add fusion_core, sdk, and .vivos to path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(BASE_DIR, 'fusion_core'))
sys.path.append(BASE_DIR)
sys.path.append(os.path.join(BASE_DIR, 'sdk'))
sys.path.append(os.path.join(BASE_DIR, '.vivos'))

def load_vivos_interlace():
    from vivos_interlace import VivosInterlace
    return VivosInterlace()

async def run_arbitrage(interlace):
    logger.info("Starting Arbitrage Engine...")
    from arbitrage.engine import ArbitrageEngine
    engine = ArbitrageEngine()
    
    # Wrap execute_trade to feed into interlace
    original_execute = engine.execute_trade
    async def wrapped_execute(direction, spread):
        await original_execute(direction, spread)
        await interlace.process_yield(
            source=f"ARBITRAGE_{direction}",
            amount=100.0 * spread,
            metadata={"direction": direction, "spread": spread}
        )
    engine.execute_trade = wrapped_execute
    await engine.start()

async def run_rex(interlace):
    logger.info("Starting REX Orchestrator...")
    from rex.rex_orchestrator import RexOrchestrator
    rex = RexOrchestrator()
    # Continuous cycle
    while True:
        await rex.run_cycle(["https://api.external-source.com/v1"], mode="CAUSAL_SIPHON")
        await asyncio.sleep(300)

async def run_money_printer():
    logger.info("Starting MoneyPrinterTurbo Service...")
    # This service is uvicorn based, better run as subprocess or in separate task
    import subprocess
    process = await asyncio.create_subprocess_exec(
        sys.executable, "fusion_fusion_core/money_printer/main.py",
        cwd=BASE_DIR,
        env={**os.environ, "PYTHONPATH": f"{os.environ.get('PYTHONPATH', '')}:{BASE_DIR}/fusion_core/money_printer"}
    )
    await process.wait()

async def run_vivos_pulse():
    logger.info("Starting VIVOS Pulse Service...")
    process = await asyncio.create_subprocess_exec(
        sys.executable, ".vivos/pulse.py",
        cwd=BASE_DIR,
        env={**os.environ, "PYTHONPATH": f"{os.environ.get('PYTHONPATH', '')}:{BASE_DIR}/sdk:{BASE_DIR}"}
    )
    await process.wait()

async def main():
    logger.success("YIELD-SIPHON Colonial Fusion v13.0 ACTIVE")
    print(f"DEBUG: sys.path = {sys.path}")
    
    try:
        interlace = load_vivos_interlace()
    except Exception as e:
        logger.error(f"Failed to load interlace: {e}")
        import traceback
        traceback.print_exc()
        return
    
    # Run services concurrently
    try:
        import traceback
        await asyncio.gather(
            run_arbitrage(interlace),
            run_rex(interlace),
            run_money_printer(),
            run_vivos_pulse(),
        )
    except Exception as e:
        logger.error(f"Fusion Error: {e}")
        traceback.print_exc()

if __name__ == "__main__":
    os.makedirs(os.path.join(BASE_DIR, "data"), exist_ok=True)
    asyncio.run(main())
