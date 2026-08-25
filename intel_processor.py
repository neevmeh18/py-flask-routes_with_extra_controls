from __future__ import annotations

from datetime import UTC, datetime

from cryptography.hazmat.primitives import hashes
from pydantic import BaseModel, Field

from vault_manager import archive_intel


class IntelPayload(BaseModel):
    username: str = Field(min_length=1)
    raw_intel: str = Field(min_length=1)


def generate_intel_signature(data: str) -> str:
    digest = hashes.Hash(hashes.SHA256())
    digest.update(data.encode("utf-8"))
    return digest.finalize().hex()[:16]


def process_intel(username: str, raw_intel: str) -> None:
    payload = IntelPayload(username=username, raw_intel=raw_intel)
    timestamp = datetime.now(UTC).isoformat()
    sig = generate_intel_signature(f"{payload.username}:{payload.raw_intel}")
    formatted_entry = f"[{timestamp}] [SIG:{sig}] [CLASSIFIED-INTEL] Agent: {payload.username} | Intel: {payload.raw_intel}"
    archive_intel(formatted_entry)
