import os
import asyncio
import time
import logging
import httpx
import psutil
from typing import Dict, Any, Optional, List
import google.generativeai as genai

try:
    import pynvml
    NVML_AVAILABLE = True
except ImportError:
    NVML_AVAILABLE = False

# Configuração de Logging de Elite
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - APEX-CORE - %(levelname)s - %(message)s'
)
logger = logging.getLogger("APEX-CORE")

class Telemetry:
    def __init__(self):
        self.start_time = time.time()
        self.nvml_initialized = False
        if NVML_AVAILABLE:
            try:
                pynvml.nvmlInit()
                self.nvml_initialized = True
            except Exception:
                pass

    def get_stats(self) -> Dict[str, Any]:
        gpu_stats = []
        if self.nvml_initialized:
            try:
                device_count = pynvml.nvmlDeviceGetCount()
                for i in range(device_count):
                    handle = pynvml.nvmlDeviceGetHandleByIndex(i)
                    util = pynvml.nvmlDeviceGetUtilizationRates(handle)
                    mem = pynvml.nvmlDeviceGetMemoryInfo(handle)
                    gpu_stats.append({
                        "id": i,
                        "util": util.gpu,
                        "vram_used": mem.used / (1024**2),
                        "vram_total": mem.total / (1024**2)
                    })
            except: pass
        
        return {
            "cpu_usage": psutil.cpu_percent(),
            "ram_usage": psutil.virtual_memory().percent,
            "gpu": gpu_stats,
            "uptime": time.time() - self.start_time
        }

class HybridBrain:
    def __init__(self, gemini_key: Optional[str] = None, ollama_url: str = "http://localhost:11434"):
        self.gemini_key = gemini_key
        if gemini_key:
            genai.configure(api_key=gemini_key)
        self.ollama_url = ollama_url
        self.threshold = 3.0

    async def think(self, prompt: str, model_local: str = "llama3") -> str:
        if self.gemini_key:
            try:
                start = time.time()
                model = genai.GenerativeModel('gemini-1.5-flash')
                response = await asyncio.wait_for(
                    asyncio.to_thread(model.generate_content, prompt),
                    timeout=self.threshold
                )
                return response.text
            except Exception as e:
                logger.warning(f"Fallback para IA Local: {e}")
        
        return await self._think_local(prompt, model_local)

    async def _think_local(self, prompt: str, model: str) -> str:
        try:
            async with httpx.AsyncClient(timeout=60.0) as client:
                resp = await client.post(
                    f"{self.ollama_url}/api/generate",
                    json={"model": model, "prompt": prompt, "stream": False}
                )
                return resp.json().get("response", "Erro na IA Local")
        except Exception as e:
            return f"CRITICAL_FAILURE: {e}"

class ApexCore:
    def __init__(self, gemini_key: Optional[str] = None):
        self.telemetry = Telemetry()
        self.brain = HybridBrain(gemini_key=gemini_key)
        self.running = True

    async def pulse(self):
        """Monitoramento de ciclo de vida e saúde."""
        logger.info("ApexCore em pulsação ativa.")
        while self.running:
            stats = self.telemetry.get_stats()
            # Se CPU > 90%, log de alerta (O Carrasco cuidará da purga se integrado)
            if stats['cpu_usage'] > 90:
                logger.warning(f"ALERTA DE SOBRECARGA: CPU em {stats['cpu_usage']}%")
            await asyncio.sleep(10)

    async def start(self):
        await self.pulse()

if __name__ == "__main__":
    core = ApexCore(gemini_key=os.getenv("GEMINI_API_KEY"))
    asyncio.run(core.start())
