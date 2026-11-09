"""Configuration settings for RepoSense Demo application."""

import os
from pathlib import Path

# Base directories
BASE_DIR = Path(__file__).resolve().parent
UPLOAD_DIR = BASE_DIR / "uploads"
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

# Upload limits
MAX_UPLOAD_SIZE_BYTES = 5 * 1024 * 1024  # 5 MB
ALLOWED_EXTENSIONS = {".png", ".jpg", ".jpeg", ".pdf", ".txt"}

# Security settings
SECRET_KEY = os.environ.get("DEMO_SECRET_KEY", "reposense-demo-secret-key-123")
TOKEN_EXPIRY_SECONDS = 3600  # 1 hour
