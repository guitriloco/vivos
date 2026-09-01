import os
import time
import asyncio
import psutil
import logging
import random
from typing import List, Dict, Any

logging.basicConfig(level=logging.INFO, format='%(asctime)s - ELITE-DEFENSE - %(levelname)s - %(message)s')
logger = logging.getLogger("ELITE-DEFENSE")

class EliteCarrasco:
    """Kill-Switch Adaptativo (Darwinismo Sistêmico)."""
    def __init__(self, cpu_limit: float = 20.0):
        self.cpu_limit = cpu_limit
        self.essential_procs = ['apex_core.py', 'sshd']

    def purge(self):
        """Elimina processos ineficientes que drenam recursos."""
        current_pid = os.getpid()
        killed = 0
        for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'cmdline']):
            try:
                pinfo = proc.info
                if pinfo['pid'] == current_pid: continue
                
                cmdline = " ".join(pinfo['cmdline'] or [])
                if any(x in cmdline for x in self.essential_procs): continue
                
                if pinfo['cpu_percent'] > self.cpu_limit:
                    logger.warning(f"PURGE: {pinfo['name']} (PID: {pinfo['pid']}) consumindo {pinfo['cpu_percent']}% CPU.")
                    proc.terminate()
                    killed += 1
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        if killed:
            logger.info(f"Darwinismo aplicado: {killed} processos purgados.")

class EliteStealth:
    """Ofuscação de rede e fingerprinting dinâmico."""
    def __init__(self):
        self.base_headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "DNT": "1",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1"
        }
        self.ua_list = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:122.0) Gecko/20100101 Firefox/122.0"
        ]

    def get_stealth_headers(self) -> Dict[str, str]:
        headers = self.base_headers.copy()
        headers["User-Agent"] = random.choice(self.ua_list)
        # Jitter de versão Chromium
        ver = random.randint(120, 122)
        headers["Sec-Ch-Ua"] = f'"Not A(Brand";v="99", "Chromium";v="{ver}", "Google Chrome";v="{ver}"'
        return headers

    async def sleep_jitter(self, range_min: float = 1.0, range_max: float = 4.0):
        await asyncio.sleep(random.uniform(range_min, range_max))
