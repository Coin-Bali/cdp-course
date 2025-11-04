import os
import requests

API_HOST = os.getenv("REQUEST_HOST", "api.cdp.coinbase.com")
REWARDS_PATH = os.getenv("STAKE_REWARDS_PATH", "/platform/v1/stake/rewards")
API_URL = f"https://{API_HOST}{REWARDS_PATH}"


def main() -> None:
    bearer = os.getenv("JWT")
    if not bearer:
        raise SystemExit("Set JWT env var (export JWT=$(python staking_jwt.py)) before running")

    address = os.getenv("STAKE_ADDRESS_ID")
    if not address:
        raise SystemExit("Set STAKE_ADDRESS_ID to the wallet address to query rewards for")

    params = {
        "address_id": address,
        # Optional time window filters; add via env if needed
        "start_time": os.getenv("REWARDS_START_TIME"),
        "end_time": os.getenv("REWARDS_END_TIME"),
    }
    # Remove None values
    params = {k: v for k, v in params.items() if v}

    headers = {
        "Authorization": f"Bearer {bearer}",
        "Accept": "application/json",
    }
    resp = requests.get(API_URL, headers=headers, params=params, timeout=30)
    print(resp.status_code)
    print(resp.text)


if __name__ == "__main__":
    main()
