import sys
import os
import requests
from dotenv import load_dotenv, find_dotenv

# Add root directory to sys.path to allow importing utils
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))
from utils.cdp_auth import generate_jwt

load_dotenv(find_dotenv())

def list_end_users():
    key_id = os.getenv("CDP_API_KEY_ID")
    key_secret = os.getenv("CDP_API_KEY_SECRET")
    
    if not key_id or not key_secret:
        print("Error: CDP_API_KEY_ID and CDP_API_KEY_SECRET must be set in .env")
        return

    host = "api.cdp.coinbase.com"
    path = "/platform/v2/end-users"
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
    
    print(f"Requesting {url}...")
    try:
        resp = requests.get(url, headers=headers, timeout=30)
        print(f"Status Code: {resp.status_code}")
        print(resp.text)
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")

if __name__ == "__main__":
    list_end_users()
