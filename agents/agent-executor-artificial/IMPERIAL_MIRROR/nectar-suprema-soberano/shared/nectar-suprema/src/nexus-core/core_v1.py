import time
import asyncio
from fastapi import FastAPI

app = FastAPI(title="Nexus_Core v1.0")

@app.get("/pulse")
async def pulse():
    return {"status": "online", "latency": "minimal", "timestamp": time.time()}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
