import os
import json
import time
import secrets
import jwt
from cryptography.hazmat.primitives import serialization
from websocket import WebSocketApp

WS_URL = "wss://advanced-trade-ws.coinbase.com"


def build_ws_jwt(key_id: str, key_secret_pem: str, expires_in: int = 120) -> str:
    private_key = serialization.load_pem_private_key(key_secret_pem.encode("utf-8"), password=None)
    now = int(time.time())
    payload = {
        "iss": "cdp",
        "nbf": now,
        "exp": now + expires_in,
        "sub": key_id,
    }
    headers = {"kid": key_id, "nonce": secrets.token_hex()}
    return jwt.encode(payload, private_key, algorithm="ES256", headers=headers)


def on_open(ws: WebSocketApp):
    print("WS open")
    # Optional JWT for market data (most channels don't require auth)
    jwt_token = None
    key_id = os.getenv("ADV_API_KEY_ID") or os.getenv("CDP_API_KEY_ID")
    key_secret = os.getenv("ADV_API_KEY_SECRET") or os.getenv("CDP_API_KEY_SECRET")
    if key_id and key_secret:
        jwt_token = build_ws_jwt(key_id, key_secret)

    message = {
        "type": "subscribe",
        "channel": "ticker",
        "product_ids": ["BTC-USD"],
    }
    if jwt_token:
        message["jwt"] = jwt_token
    ws.send(json.dumps(message))


def on_message(ws: WebSocketApp, message: str):
    data = json.loads(message)
    print(data)


def on_error(ws: WebSocketApp, error: Exception):
    print("WS error:", error)


def on_close(ws: WebSocketApp, code, reason):
    print("WS closed", code, reason)


def main() -> None:
    ws = WebSocketApp(WS_URL, on_open=on_open, on_message=on_message, on_error=on_error, on_close=on_close)
    ws.run_forever()


if __name__ == "__main__":
    main()
