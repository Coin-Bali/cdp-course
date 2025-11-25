import sys
import os
import requests
import json
from dotenv import load_dotenv, find_dotenv

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))
from utils.cdp_auth import generate_jwt

load_dotenv(find_dotenv())

def build_stake_operation():
    key_id = os.getenv("CDP_API_KEY_ID")
    key_secret = os.getenv("CDP_API_KEY_SECRET")
    
    if not key_id or not key_secret:
        print("Error: CDP_API_KEY_ID and CDP_API_KEY_SECRET must be set in .env")
        return

    host = "api.cdp.coinbase.com"
    path = "/platform/v1/stake/build"
    method = "POST"
    url = f"https://{host}{path}"

    # Ensure STAKING_ADDRESS_ID is set
    address_id = os.getenv("STAKING_ADDRESS_ID")
    if not address_id:
        print("Error: STAKING_ADDRESS_ID required in .env")
        return

    payload = {
        "network_id": os.getenv("STAKING_NETWORK_ID", "ethereum-hoodi"),
        "asset_id": os.getenv("STAKING_ASSET_ID", "ETH"),
        "address_id": address_id,
        "action": "stake",
        "options": {
            "mode": "partial",
            "amount": "100000000000000000" # 0.1 ETH
        }
    }

    try:
        token = generate_jwt(key_id, key_secret, method, host, path)
    except Exception as e:
        print(f"Error generating JWT: {e}")
        return

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "Accept": "application/json",
    }

    print(f"Building Stake Operation: {json.dumps(payload, indent=2)}")
    try:
        resp = requests.post(url, headers=headers, json=payload)
        resp.raise_for_status()
        print("Operation Built Successfully:")
        print(json.dumps(resp.json(), indent=2))
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        if 'resp' in locals():
            print(resp.text)

if __name__ == "__main__":
    build_stake_operation()
