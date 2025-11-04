import os
import json
import requests

API_HOST = os.getenv("REQUEST_HOST", "api.cdp.coinbase.com")
API_PATH = os.getenv("STAKE_BUILD_PATH", "/platform/v1/stake/build")
API_URL = f"https://{API_HOST}{API_PATH}"


def main() -> None:
    bearer = os.getenv("JWT")
    if not bearer:
        raise SystemExit("Set JWT env var (export JWT=$(python staking_jwt.py)) before running")

    # Example body, customize via env vars
    network_id = os.getenv("STAKE_NETWORK_ID", "ethereum-hoodi")
    asset_id = os.getenv("STAKE_ASSET_ID", "ETH")
    address_id = os.getenv("STAKE_ADDRESS_ID", "0xYOUR_ADDRESS")
    action = os.getenv("STAKE_ACTION", "stake")  # stake | unstake | claim
    mode = os.getenv("STAKE_MODE", "partial")    # partial | dedicated | full (protocol-specific)
    amount = os.getenv("STAKE_AMOUNT_WEI")         # string in native base units when required

    body = {
        "network_id": network_id,
        "asset_id": asset_id,
        "address_id": address_id,
        "action": action,
        "options": {
            "mode": mode,
        },
    }
    if amount:
        body["options"]["amount"] = amount

    headers = {
        "Authorization": f"Bearer {bearer}",
        "Content-Type": "application/json",
        "Accept": "application/json",
    }

    resp = requests.post(API_URL, headers=headers, data=json.dumps(body), timeout=30)
    print(resp.status_code)
    print(resp.text)


if __name__ == "__main__":
    main()
