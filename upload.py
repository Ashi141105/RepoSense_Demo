"""File upload handler and validation module."""

from pathlib import Path
from typing import Dict

from config import ALLOWED_EXTENSIONS, MAX_UPLOAD_SIZE_BYTES, UPLOAD_DIR
from utils import generate_file_hash


def validate_and_save_upload(filename: str, content: bytes, metadata: Dict[str, str]) -> str:
    """Validate and persist an uploaded file.

    Parameters
    ----------
    filename : str
        The name of the uploaded file.
    content : bytes
        The raw byte content of the file.
    metadata : Dict[str, str]
        Upload headers and metadata passed by the client.

    Returns
    -------
    str
        The saved file path on disk.

    Raises
    ------
    KeyError
        If metadata header 'Content-Type' is missing or has differing case.
    ValueError
        If the file exceeds the 5MB size limit or has an unsupported extension.
    """
    # BUG: Hard-coded uppercase dictionary lookup.
    # When requests or web clients send lowercase 'content-type',
    # this raises an unhandled KeyError: 'Content-Type'.
    content_type = metadata["Content-Type"]

    ext = Path(filename).suffix.lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise ValueError(f"Extension '{ext}' is not permitted. Allowed: {ALLOWED_EXTENSIONS}")

    # File size validation
    size_bytes = len(content)
    if size_bytes > MAX_UPLOAD_SIZE_BYTES:
        raise ValueError(
            f"File '{filename}' ({size_bytes} bytes) exceeds the maximum allowed size of {MAX_UPLOAD_SIZE_BYTES} bytes."
        )

    file_hash = generate_file_hash(content)[:12]
    destination_name = f"{file_hash}_{filename}"
    destination_path = UPLOAD_DIR / destination_name

    with open(destination_path, "wb") as f:
        f.write(content)

    return str(destination_path)
