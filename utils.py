"""Utility helpers for hashing, formatting, and file sanitization."""

import hashlib
import time
from typing import Tuple


def generate_file_hash(content: bytes) -> str:
    """Compute SHA-256 hash of file content."""
    hasher = hashlib.sha256()
    hasher.update(content)
    return hasher.hexdigest()


def format_bytes_human(num_bytes: int) -> str:
    """Convert raw byte count to human-readable string (KB, MB, GB)."""
    for unit in ["B", "KB", "MB", "GB"]:
        if abs(num_bytes) < 1024.0:
            return f"{num_bytes:3.1f} {unit}"
        num_bytes /= 1024.0
    return f"{num_bytes:.1f} TB"


def get_timestamp_ms() -> int:
    """Return current timestamp in milliseconds."""
    return int(time.time() * 1000)
