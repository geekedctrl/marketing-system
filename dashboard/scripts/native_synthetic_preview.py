"""Run the native dashboard against in-memory synthetic responses on localhost.

From the repository root: python dashboard/scripts/native_synthetic_preview.py
Sign in with admin@example.com and synthetic. No real API or provider is used.
"""
import sys
from pathlib import Path

import httpx
import uvicorn

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.native import create_app  # noqa: E402
from validate_native_frontend import NativeFixture  # noqa: E402


if __name__ == "__main__":
    fixture = NativeFixture()
    uvicorn.run(
        create_app(httpx.MockTransport(fixture.respond)),
        host="127.0.0.1",
        port=8099,
        log_level="warning",
    )
