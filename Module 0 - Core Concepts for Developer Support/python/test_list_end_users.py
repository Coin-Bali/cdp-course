import os
import requests

API_HOST = "api.cdp.coinbase.com"
API_PATH = "/platform/v2/end-users"
API_URL = f"https://{API_HOST}{API_PATH}"


def main() -> None:
    bearer = os.getenv("JWT")
    if not bearer:
        raise SystemExit("Set JWT env var (export JWT=$(python cdp_jwt.py)) before running")

    headers = {
        "Authorization": f"Bearer {bearer}",
        "Accept": "application/json",
    }
    resp = requests.get(API_URL, headers=headers, timeout=30)
    print(resp.status_code)
    print(resp.text)


if __name__ == "__main__":
    main()
