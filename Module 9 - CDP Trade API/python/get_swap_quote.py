import sys
import os
import requests
import json
from dotenv import load_dotenv, find_dotenv

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))
from utils.cdp_auth import generate_jwt

load_dotenv(find_dotenv())

def get_swap_quote():
    key_id = os.getenv("CDP_API_KEY_ID")
    key_secret = os.getenv("CDP_API_KEY_SECRET")

    if not key_id or not key_secret:
        print("Error: CDP_API_KEY_ID and CDP_API_KEY_SECRET required")
        return

    host = "api.cdp.coinbase.com"
    path = "/platform/v2/evm/swaps/quote"
    method = "GET"
    url = f"https://{host}{path}"

    params = {
        "network": os.getenv("SWAP_NETWORK", "base"),
        "fromToken": os.getenv("SWAP_FROM_TOKEN_ADDRESS"),
        "toToken": os.getenv("SWAP_TO_TOKEN_ADDRESS"),
        "fromAmount": os.getenv("SWAP_FROM_AMOUNT"),
        "taker": os.getenv("SWAP_TAKER_ADDRESS"),
    }
    
    # Filter None
    params = {k: v for k, v in params.items() if v}

    try:
        token = generate_jwt(key_id, key_secret, method, host, path)
    except Exception as e:
        print(f"Error generating JWT: {e}")
        return

    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json"
    }

    print(f"Getting Swap Quote...")
    try:
        resp = requests.get(url, headers=headers, params=params)
        resp.raise_for_status()
        print("Quote:")
        print(json.dumps(resp.json(), indent=2))
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        if 'resp' in locals():
            print(resp.text)

if __name__ == "__main__":
    get_swap_quote()
