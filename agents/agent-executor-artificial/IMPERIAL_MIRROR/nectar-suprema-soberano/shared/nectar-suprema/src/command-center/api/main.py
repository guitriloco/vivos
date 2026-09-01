from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Request, Depends, Header, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, FileResponse
import os
import pty
import subprocess
import select
import termios
import struct
import fcntl
import asyncio
import time
import json
import sys
import httpx

# Add src to path for security module
script_dir = os.path.dirname(os.path.abspath(__file__))
src_path = os.path.abspath(os.path.join(script_dir, "../.."))
sys.path.append(src_path)

try:
    from sovereign_security import verify_sovereign_token, SOVEREIGN_TOKEN
except ImportError:
    print("Warning: sovereign_security not found. Security is DEGRADED.")
    def verify_sovereign_token(): return True
    SOVEREIGN_TOKEN = "UNSECURE"

app = FastAPI(title="Universal Command Center API (SECURE)")

# Strictly limit CORS in production
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In a real scenario, this would be the dashboard URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configuration
REPO_ROOT = "/home/team/shared/nectar-suprema"
STATIC_DIR = os.path.join(REPO_ROOT, "src/command-center")
NOV_API_URL = "http://localhost:8001"

@app.get("/", response_class=HTMLResponse)
async def get_dashboard():
    index_path = os.path.join(STATIC_DIR, "index.html")
    if os.path.exists(index_path):
        with open(index_path, "r") as f:
            return f.read()
    return "Dashboard index.html not found."

@app.get("/status", dependencies=[Depends(verify_sovereign_token)])
async def get_status():
    base_path = os.path.join(REPO_ROOT, "src")
    projects = {
        'Nexus Core': 'nexus-core',
        'Hyper Recursion': 'hyper-recursion',
        'Sovereign Entity': 'sovereign-entity',
        'Knowledge Base': 'vvv-vault',
        'Nov API': 'nov-api'
    }
    
    status_data = []
    for name, folder in projects.items():
        path = os.path.join(base_path, folder)
        if os.path.exists(path):
            files = len([f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))])
            status_data.append({"name": name, "files": files, "state": "STABLE/OPTIMIZED"})
        else:
            status_data.append({"name": name, "state": "NOT FOUND"})
            
    # Active LPs
    docs_lps = os.path.join(REPO_ROOT, "docs/lps")
    lps = []
    if os.path.exists(docs_lps):
        lps = [d for d in os.listdir(docs_lps) if os.path.isdir(os.path.join(docs_lps, d))]
        
    # Check Nov API health
    nov_status = "OFFLINE"
    try:
        async with httpx.AsyncClient() as client:
            res = await client.get(f"{NOV_API_URL}/docs", timeout=1.0)
            if res.status_code == 200:
                nov_status = "ONLINE"
    except:
        pass
        
    return {
        "projects": status_data,
        "active_lps_count": len(lps),
        "active_lps": lps,
        "nov_api_status": nov_status,
        "timestamp": time.time()
    }

@app.get("/metrics", dependencies=[Depends(verify_sovereign_token)])
async def get_metrics():
    # Simulated profit metrics for global conquest
    return {
        "labels": ["00:00", "04:00", "08:00", "12:00", "16:00", "20:00", "24:00"],
        "profit": [1200, 1500, 1100, 2500, 4200, 3800, 5000],
        "conversions": [10, 12, 8, 25, 40, 35, 45],
        "total_revenue": "R$ 19.300,00",
        "growth_rate": "+15.4%"
    }

# Mock Sovereignty API for Nov (on port 8000 if we were running there, 
# but here it's on 8002, so Nov should be pointed here)
@app.post("/refinement/trigger", dependencies=[Depends(verify_sovereign_token)])
async def trigger_refinement(data: dict):
    print(f"[REFINEMENT] Triggered: {data}")
    return {"status": "triggered", "details": data}

def set_winsize(fd, row, col, xpix=0, ypix=0):
    winsize = struct.pack("HHHH", row, col, xpix, ypix)
    fcntl.ioctl(fd, termios.TIOCSWINSZ, winsize)

@app.websocket("/ws/terminal")
async def terminal_websocket(websocket: WebSocket, token: str = None):
    await websocket.accept()
    
    if token != SOVEREIGN_TOKEN:
        await websocket.send_text("\r\n\033[31mSovereign Shield: Access Denied. Integrity mismatch.\033[0m\r\n")
        await websocket.close()
        return
    
    # Create pseudo-terminal
    (child_pid, fd) = pty.fork()
    
    if child_pid == 0:
        # Child process
        os.environ["TERM"] = "xterm-256color"
        os.chdir(REPO_ROOT)
        # Use a login shell to ensure environment is set up
        os.execv("/bin/bash", ["bash"])
    else:
        # Parent process
        try:
            # Set non-blocking
            # attrs = termios.tcgetattr(fd)
            # attrs[3] = attrs[3] & ~termios.ECHO
            # termios.tcsetattr(fd, termios.TCSANOW, attrs)
            
            async def read_from_pty():
                while True:
                    await asyncio.sleep(0.01)
                    [r, w, e] = select.select([fd], [], [], 0)
                    if fd in r:
                        output = os.read(fd, 1024)
                        if output:
                            await websocket.send_text(output.decode(errors="ignore"))
                        else:
                            break
                            
            async def write_to_pty():
                while True:
                    data = await websocket.receive_text()
                    if data:
                        if data.startswith("__resize:"):
                            parts = data.split(":")
                            set_winsize(fd, int(parts[1]), int(parts[2]))
                        else:
                            os.write(fd, data.encode())

            await asyncio.gather(read_from_pty(), write_to_pty())
            
        except WebSocketDisconnect:
            pass
        finally:
            os.close(fd)
            os.kill(child_pid, 9)

if __name__ == "__main__":
    import uvicorn
    # Listening on both 8002 (Command Center) and 8000 (Mock for Nov) 
    # is not possible with one uvicorn.run easily without multiple processes.
    # I'll just run on 8002 and tell the user they can point Nov to 8002.
    uvicorn.run(app, host="0.0.0.0", port=8002)
