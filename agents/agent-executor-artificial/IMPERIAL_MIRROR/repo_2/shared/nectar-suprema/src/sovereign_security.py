import os
import hmac
import hashlib
from fastapi import Header, HTTPException, Depends

# The master key for the ADM operation
SOVEREIGN_TOKEN = os.environ.get("SOVEREIGN_ADM_TOKEN", "SOVEREIGN_PULSE_999")

def verify_sovereign_token(x_sovereign_token: str = Header(None)):
    """
    Dependency to verify the presence of the Sovereign Token in request headers.
    """
    if x_sovereign_token != SOVEREIGN_TOKEN:
        raise HTTPException(status_code=403, detail="Sovereign Shield: Access Denied. Integrity mismatch.")
    return x_sovereign_token

def seal_message(message: str, secret: str = SOVEREIGN_TOKEN):
    """Generates an HMAC seal for a message."""
    return hmac.new(secret.encode(), message.encode(), hashlib.sha256).hexdigest()

def verify_seal(message: str, seal: str, secret: str = SOVEREIGN_TOKEN):
    """Verifies an HMAC seal."""
    expected = seal_message(message, secret)
    return hmac.compare_digest(expected, seal)
