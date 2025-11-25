import sys
import os
import requests
import json
from dotenv import load_dotenv, find_dotenv

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))
from utils.cdp_auth import generate_jwt

load_dotenv(find_dotenv())

def get_business_accounts():
    key_id = os.getenv("BUSINESS_API_KEY_ID")
    key_secret = os.getenv("BUSINESS_API_KEY_SECRET")
    
    if not key_id or not key_secret:
        print("Error: BUSINESS_API_KEY_ID and BUSINESS_API_KEY_SECRET must be set in .env")
        return

    host = "api.coinbase.com"
    path = "/api/v3/brokerage/accounts"
    method = "GET"
    url = f"https://{host}{path}"

    try:
        # Note: Business API Keys are often distinct from CDP keys but use same signing for v2/v3
        # If this fails, ensure the key type supports this JWT method or use legacy signing.
        token = generate_jwt(key_id, key_secret, method, host, path)
    except Exception as e:
        print(f"Error generating JWT: {e}")
        return

    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json",
        "CB-VERSION": "2023-07-06"
    }

    print(f"Fetching Accounts from {url}...")
    try:
        resp = requests.get(url, headers=headers)
    resp.raise_for_status()
        print("Accounts:")
        print(json.dumps(resp.json(), indent=2))
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        if 'resp' in locals():
            print(resp.text)

if __name__ == "__main__":
    get_business_accounts()
