"""Main application server providing upload and authentication endpoints."""

from typing import Dict, Optional

from auth import create_session, verify_session
from config import BASE_DIR, MAX_UPLOAD_SIZE_BYTES
from upload import validate_and_save_upload
from utils import format_bytes_human


class AppServer:
    """Mock application handler for triage demo."""

    def __init__(self, name: str = "RepoSense-Demo-Vault"):
        self.name = name

    def handle_login(self, username: str) -> Dict[str, str]:
        """Log in a user and return an active session token."""
        token = create_session(username)
        return {"status": "ok", "token": token, "user": username}

    def handle_upload(
        self,
        token: str,
        filename: str,
        content: bytes,
        headers: Optional[Dict[str, str]] = None,
    ) -> Dict[str, str]:
        """Authenticate user and handle file upload dispatch."""
        session = verify_session(token)
        if not session:
            return {"status": "error", "message": "Unauthorized session token."}

        headers = headers or {}
        # Delegates to upload.py
        saved_path = validate_and_save_upload(
            filename=filename,
            content=content,
            metadata=headers,
        )

        return {
            "status": "success",
            "path": saved_path,
            "size": format_bytes_human(len(content)),
        }


if __name__ == "__main__":
    print("RepoSense Demo Server initializing...")
    server = AppServer()
    session = server.handle_login("test_user")
    print(f"Logged in: {session}")
