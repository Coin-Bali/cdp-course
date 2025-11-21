#!/usr/bin/env python3
"""Simple Coinbase SIWC OAuth helper with PKCE and a redirect listener."""
import base64
import hashlib
import os
import secrets
import threading
import time
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs, urlparse

import requests
from dotenv import load_dotenv

load_dotenv()

AUTH_URL = "https://login.coinbase.com/oauth2/auth"
TOKEN_URL = "https://login.coinbase.com/oauth2/token"

CLIENT_ID = os.getenv("COINBASE_CLIENT_ID")
CLIENT_SECRET = os.getenv("COINBASE_CLIENT_SECRET")
REDIRECT_URI = os.getenv("COINBASE_REDIRECT_URI", "http://localhost:8080/callback")
SCOPES = os.getenv("COINBASE_SCOPES", "wallet:user:read wallet:accounts:read offline_access")


def generate_code_verifier(length: int = 96) -> str:
    raw = secrets.token_urlsafe(length)
    return raw[:128]


def generate_code_challenge(verifier: str) -> str:
    digest = hashlib.sha256(verifier.encode("utf-8")).digest()
    return base64.urlsafe_b64encode(digest).decode("utf-8").rstrip("=")


def build_authorization_url(code_challenge: str, state: str) -> str:
    params = {
        "response_type": "code",
        "client_id": CLIENT_ID,
        "redirect_uri": REDIRECT_URI,
        "scope": SCOPES,
        "state": state,
        "code_challenge": code_challenge,
        "code_challenge_method": "S256",
    }
    return f"{AUTH_URL}?{requests.compat.urlencode(params)}"


def exchange_code_for_token(code: str, code_verifier: str) -> dict:
    payload = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": REDIRECT_URI,
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "code_verifier": code_verifier,
    }
    resp = requests.post(TOKEN_URL, data=payload, timeout=15)
    resp.raise_for_status()
    return resp.json()


def refresh_access_token(refresh_token: str) -> dict:
    payload = {
        "grant_type": "refresh_token",
        "refresh_token": refresh_token,
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
    }
    resp = requests.post(TOKEN_URL, data=payload, timeout=15)
    resp.raise_for_status()
    return resp.json()


class OAuthCallbackHandler(BaseHTTPRequestHandler):
    server_version = "SIWC-OAuth-Callback/1.0"

    def do_GET(self):
        parsed = urlparse(self.path)
        params = parse_qs(parsed.query)
        code = params.get("code", [None])[0]
        state = params.get("state", [None])[0]
        if code:
            self.server.auth_code = code
            self.server.auth_state = state
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.end_headers()
        message = "<h1>Authorization Received</h1><p>You can close this tab.</p>"
        self.wfile.write(message.encode("utf-8"))
        threading.Thread(target=self.server.shutdown, daemon=True).start()

    def log_message(self, format, *args):  # suppress console noise
        return


def parse_redirect_host_port() -> tuple[str, int]:
    parsed = urlparse(REDIRECT_URI)
    if parsed.scheme != "http":
        raise ValueError("This helper only supports http redirect URIs for local testing.")
    host = parsed.hostname or "localhost"
    port = parsed.port or 80
    return host, port


def main():
    if not CLIENT_ID or not CLIENT_SECRET:
        raise SystemExit("Set COINBASE_CLIENT_ID and COINBASE_CLIENT_SECRET in your environment.")

    host, port = parse_redirect_host_port()
    code_verifier = generate_code_verifier()
    code_challenge = generate_code_challenge(code_verifier)
    state = secrets.token_urlsafe(32)
    auth_url = build_authorization_url(code_challenge, state)

    server = HTTPServer((host, port), OAuthCallbackHandler)
    server.auth_code = None
    server.auth_state = None

    print("+-------------------------------+")
    print("|  SIWC Authorization Helper   |")
    print("+-------------------------------+")
    print(f"Listening for callback on: {REDIRECT_URI}")
    print("1. Open the following URL in your browser:")
    print(auth_url)
    print("2. Complete the Coinbase consent screen. The helper will automatically capture the code.")
    print("Waiting for the authorization response... (press Ctrl+C to cancel)")

    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()

    while server.auth_code is None:
        time.sleep(0.5)

    if server.auth_state != state:
        print("Warning: OAuth state mismatch. Do not trust this response.")

    tokens = exchange_code_for_token(server.auth_code, code_verifier)
    print("\n== Tokens ==")
    for key in ("access_token", "refresh_token", "expires_in", "scope"):
        if key in tokens:
            print(f"{key}: {tokens[key]}")

    if refresh := tokens.get("refresh_token"):
        prompt = input("Refresh token now to verify refresh flow? (y/N): ").strip().lower()
        if prompt == "y":
            refreshed = refresh_access_token(refresh)
            print("\n== Refreshed Tokens ==")
            for key in ("access_token", "refresh_token", "expires_in", "scope"):
                if key in refreshed:
                    print(f"{key}: {refreshed[key]}")

    server.server_close()
    thread.join(timeout=1)


if __name__ == "__main__":
    main()
