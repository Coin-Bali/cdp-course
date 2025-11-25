import sys
import os
import requests
import json
from dotenv import load_dotenv, find_dotenv

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))
from utils.cdp_auth import generate_jwt

load_dotenv(find_dotenv())

def check_paymaster_status():
    # Paymaster RPC URL usually contains the Client API Key:
    # https://api.developer.coinbase.com/rpc/v1/base-sepolia/<KEY>
    rpc_url = os.getenv("PAYMASTER_RPC_URL")
    
    if not rpc_url:
        print("Error: PAYMASTER_RPC_URL required in .env")
        return

    # Note: If you are using a restricted Paymaster that requires Server-Side Auth (JWT),
    # you would generate a token here. Most RPC endpoints use the key in the URL.
    # key_id = os.getenv("CDP_API_KEY_ID")
    # key_secret = os.getenv("CDP_API_KEY_SECRET")
    # token = generate_jwt(...)
    
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json"
    }

    payload = {
        "jsonrpc": "2.0",
        "method": "eth_chainId",
        "params": [],
        "id": 1
    }

    print(f"Checking Paymaster at {rpc_url}...")
    try:
        resp = requests.post(rpc_url, headers=headers, json=payload)
        resp.raise_for_status()
        print("Response:")
        print(json.dumps(resp.json(), indent=2))
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    check_paymaster_status()
