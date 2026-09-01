# Yes Usage Guide

This guide explains how to interact with the Yes Yield Execution Engine.

## 🛠 Prerequisites

- Python 3.10+
- FastAPI
- Uvicorn

## 💻 Running the Service

```bash
# From the root of the Yes repository
python api/main.py
```
The service will start on `http://0.0.0.0:8002`.

## 🌐 API Interaction

### `POST /execute`
Submits a strategic objective for yield maximization.

**Payload:**
```json
{
  "objective": "OPTIMIZE_TOKEN_LIQUIDITY"
}
```

**Response:**
```json
{
  "status": "success",
  "yield": "MAXIMIZED",
  "timestamp": 1714320000.0
}
```

## 🐚 CLI Tools

### `conquer.sh`
Executes the manual Conqueror Protocol sequence.
```bash
bash scripts/conquer.sh
```
