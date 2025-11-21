#!/usr/bin/env python3
"""Verify Coinbase Commerce webhook payloads locally."""
import argparse
import base64
import hashlib
import hmac
import json
import os
import sys
from pathlib import Path

from dotenv import load_dotenv

load_dotenv(dotenv_path=Path(__file__).parents[1] / ".env")

SECRET = os.getenv("COMMERCE_SHARED_SECRET")


def compute_signature(payload: bytes, secret: str) -> str:
    digest = hmac.new(secret.encode(), payload, hashlib.sha256).digest()
    return base64.b64encode(digest).decode("utf-8")


def main():
    parser = argparse.ArgumentParser(description="Validate Coinbase Commerce webhook payload.")
    parser.add_argument("--payload", required=True, help="Path to the raw webhook JSON payload")
    parser.add_argument("--signature", required=True, help="Value of the X-CC-WEBHOOK-SIGNATURE header")
    args = parser.parse_args()

    if not SECRET:
        print("COMMERCE_SHARED_SECRET is required (set it via .env or environment).")
        sys.exit(1)

    payload_bytes = Path(args.payload).read_bytes()
    expected = compute_signature(payload_bytes, SECRET)

    is_valid = hmac.compare_digest(expected, args.signature)
    print("Signature Match:" , is_valid)
    if not is_valid:
        print("Expected:", expected)
        print("Received:", args.signature)
        print("Tip: ensure no whitespace changes and that you use the exact payload Coinbase posted (raw, not pretty-printed).")
    else:
        print("Payload looks authentic. Continue processing event data.")

    event = json.loads(payload_bytes)
    print("Event type:", event.get("event", {}).get("type"))
    print("Charge code:", event.get("event", {}).get("data", {}).get("code"))


if __name__ == "__main__":
    main()
