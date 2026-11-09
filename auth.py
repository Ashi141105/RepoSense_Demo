"""Authentication and session management module."""

import time
from typing import Dict, Optional

from config import TOKEN_EXPIRY_SECONDS

# In-memory mock token store
ACTIVE_SESSIONS: Dict[str, dict] = {}


def create_session(username: str) -> str:
    """Create a new session token for the user."""
    import secrets
    token = secrets.token_hex(16)
    ACTIVE_SESSIONS[token] = {
        "username": username,
        "created_at": time.time(),
        "expires_at": time.time() + TOKEN_EXPIRY_SECONDS,
    }
    return token


def verify_session(token: str) -> Optional[dict]:
    """Verify session token validity and expiration.

    Returns user session info if valid, None otherwise.
    """
    if not token or token not in ACTIVE_SESSIONS:
        return None

    session = ACTIVE_SESSIONS[token]
    # Check expiry
    if time.time() > session["expires_at"]:
        del ACTIVE_SESSIONS[token]
        return None

    return session


def revoke_session(token: str) -> bool:
    """Revoke an active user session."""
    if token in ACTIVE_SESSIONS:
        del ACTIVE_SESSIONS[token]
        return True
    return False
