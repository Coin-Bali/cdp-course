import sys
import os
import requests
import json
from dotenv import load_dotenv, find_dotenv

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))
from utils.cdp_auth import generate_jwt

load_dotenv(find_dotenv())

def list_staking_rewards():
    key_id = os.getenv("CDP_API_KEY_ID")
    key_secret = os.getenv("CDP_API_KEY_SECRET")
    
    # e.g., /platform/v1/stake/rewards/ethereum/<address>
    path = os.getenv("STAKING_REWARDS_PATH")
    
    if not key_id or not key_secret or not path:
        print("Error: CDP_API_KEY_ID, CDP_API_KEY_SECRET, and STAKING_REWARDS_PATH must be set in .env")
        return

    host = "api.cdp.coinbase.com"
    method = "GET"
    url = f"https://{host}{path}"

    try:
        token = generate_jwt(key_id, key_secret, method, host, path)
    except Exception as e:
        print(f"Error generating JWT: {e}")
        return

    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json",
    }

    print(f"Fetching rewards from {url}...")
    try:
        resp = requests.get(url, headers=headers)
        resp.raise_for_status()
        print("Rewards Data:")
        print(json.dumps(resp.json(), indent=2))
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        if 'resp' in locals():
            print(resp.text)

if __name__ == "__main__":
    list_staking_rewards()
