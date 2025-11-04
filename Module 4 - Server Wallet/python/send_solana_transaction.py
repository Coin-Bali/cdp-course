import os
import json
import requests

API_HOST = os.getenv("REQUEST_HOST", "api.cdp.coinbase.com")
SOL_SEND_PATH = os.getenv("SOL_SEND_PATH", "/platform/v2/solana/send")
API_URL = f"https://{API_HOST}{SOL_SEND_PATH}"


def main() -> None:
    bearer = os.getenv("JWT")
    if not bearer:
        raise SystemExit("Set JWT env var (export JWT=$(python server_wallet_jwt.py)) before running")

    network = os.getenv("SOL_NETWORK", "solana-devnet")
    b64_tx = os.getenv("SOL_B64_TX")
    if not b64_tx:
        raise SystemExit("Set SOL_B64_TX to a base64 encoded Solana transaction")

    body = {
        "network": network,
        "transaction": b64_tx,
    }

    headers = {
        "Authorization": f"Bearer {bearer}",
        "Accept": "application/json",
        "Content-Type": "application/json",
    }

    resp = requests.post(API_URL, headers=headers, data=json.dumps(body), timeout=30)
    print(resp.status_code)
    print(resp.text)


if __name__ == "__main__":
    main()
