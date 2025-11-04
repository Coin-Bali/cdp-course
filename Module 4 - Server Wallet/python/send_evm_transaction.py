import os
import json
import requests

API_HOST = os.getenv("REQUEST_HOST", "api.cdp.coinbase.com")
EVM_SEND_PATH = os.getenv("EVM_SEND_PATH", "/platform/v2/evm/send")
API_URL = f"https://{API_HOST}{EVM_SEND_PATH}"


def main() -> None:
    bearer = os.getenv("JWT")
    if not bearer:
        raise SystemExit("Set JWT env var (export JWT=$(python server_wallet_jwt.py)) before running")

    address = os.getenv("EVM_ADDRESS")
    network = os.getenv("EVM_NETWORK", "base-sepolia")
    to_addr = os.getenv("EVM_TO_ADDRESS", "0x0000000000000000000000000000000000000000")
    value_wei = os.getenv("EVM_VALUE_WEI", "1000")

    if not address:
        raise SystemExit("Set EVM_ADDRESS to the server wallet EVM address")

    body = {
        "address": address,
        "network": network,
        "transaction": {
            "to": to_addr,
            "value": value_wei,
        },
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
