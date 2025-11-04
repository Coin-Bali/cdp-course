import os
import requests

API_HOST = "api.coinbase.com"
API_PATH = "/api/v3/brokerage/products"
API_URL = f"https://{API_HOST}{API_PATH}"


def main() -> None:
    bearer = os.getenv("JWT")
    if not bearer:
        raise SystemExit("Set JWT env var (export JWT=$(python advanced_trade_jwt.py)) before running")

    headers = {
        "Authorization": f"Bearer {bearer}",
        "Accept": "application/json",
    }
    resp = requests.get(API_URL, headers=headers, timeout=30)
    print(resp.status_code)
    print(resp.text)


if __name__ == "__main__":
    main()
