import sys
import os
import requests
import json
from dotenv import load_dotenv, find_dotenv

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))
from utils.cdp_auth import generate_jwt

load_dotenv(find_dotenv())

def list_products():
    key_id = os.getenv("CDP_API_KEY_ID")
    key_secret = os.getenv("CDP_API_KEY_SECRET")
    
    if not key_id or not key_secret:
        print("Error: CDP_API_KEY_ID and CDP_API_KEY_SECRET must be set in .env")
        return

    host = "api.coinbase.com"
    path = "/api/v3/brokerage/products"
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

    print("Listing Advanced Trade Products...")
    try:
        resp = requests.get(url, headers=headers)
        resp.raise_for_status()
        data = resp.json()
        print(f"Found {len(data.get('products', []))} products.")
        # Print first 2 for brevity
        print(json.dumps(data.get('products', [])[:2], indent=2))
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        if 'resp' in locals():
            print(resp.text)

if __name__ == "__main__":
    list_products()
