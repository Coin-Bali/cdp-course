import sys
import os
import requests
import json
from dotenv import load_dotenv, find_dotenv

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))
from utils.cdp_auth import generate_jwt

load_dotenv(find_dotenv())

def send_money_v2():
    key_id = os.getenv("CDP_API_KEY_ID")
    key_secret = os.getenv("CDP_API_KEY_SECRET")
    
    account_id = os.getenv("TRANSFER_SOURCE_ACCOUNT_ID")
    to_addr = os.getenv("TRANSFER_TO_ADDRESS")

    if not all([key_id, key_secret, account_id, to_addr]):
        print("Error: Missing required env vars for transfer.")
        return

    host = "api.coinbase.com"
    path = f"/v2/accounts/{account_id}/transactions"
    method = "POST"
    url = f"https://{host}{path}"

    payload = {
        "type": "send",
        "to": to_addr,
        "amount": "0.001", # Example
        "currency": "ETH",
    }

    try:
        token = generate_jwt(key_id, key_secret, method, host, path)
    except Exception as e:
        print(f"Error generating JWT: {e}")
        return

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "CB-VERSION": "2023-07-06"
    }

    print(f"Sending Money...")
    try:
        resp = requests.post(url, headers=headers, json=payload)
        resp.raise_for_status()
        print("Transaction:")
        print(json.dumps(resp.json(), indent=2))
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        if 'resp' in locals():
            print(resp.text)

if __name__ == "__main__":
    send_money_v2()
