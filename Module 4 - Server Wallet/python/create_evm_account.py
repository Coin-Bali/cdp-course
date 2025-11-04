import os
import requests

API_HOST = os.getenv("REQUEST_HOST", "api.cdp.coinbase.com")
EVM_ACCOUNTS_PATH = os.getenv("EVM_ACCOUNTS_PATH", "/platform/v2/evm/accounts")
API_URL = f"https://{API_HOST}{EVM_ACCOUNTS_PATH}"


def main() -> None:
    bearer = os.getenv("JWT")
    if not bearer:
        raise SystemExit("Set JWT env var (export JWT=$(python server_wallet_jwt.py)) before running")

    headers = {
        "Authorization": f"Bearer {bearer}",
        "Accept": "application/json",
        "Content-Type": "application/json",
    }

    resp = requests.post(API_URL, headers=headers, timeout=30)
    print(resp.status_code)
    print(resp.text)


if __name__ == "__main__":
    main()
