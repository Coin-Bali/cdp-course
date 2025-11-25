import sys
import os
import requests
import json
from dotenv import load_dotenv, find_dotenv

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))
from utils.cdp_auth import generate_jwt

load_dotenv(find_dotenv())

def send_solana_transaction():
    key_id = os.getenv("CDP_API_KEY_ID")
    key_secret = os.getenv("CDP_API_KEY_SECRET")
    wallet_secret = os.getenv("CDP_WALLET_SECRET")

    source_addr = os.getenv("SOLANA_SOURCE_ADDRESS")
    
    # Base64 encoded serialized transaction (placeholder)
    tx_payload = os.getenv("SOLANA_TRANSACTION_PAYLOAD")

    if not all([key_id, key_secret, wallet_secret, source_addr, tx_payload]):
        print("Error: Missing required env vars for Solana transaction.")
        return

    host = "api.cdp.coinbase.com"
    path = f"/platform/v2/solana/accounts/{source_addr}/transactions"
    method = "POST"
    url = f"https://{host}{path}"

    payload = {
        "transaction": tx_payload,
        "network": os.getenv("SOLANA_NETWORK", "solana-devnet")
    }

    try:
        auth_token = generate_jwt(key_id, key_secret, method, host, path)
        wallet_auth_token = generate_jwt(key_id, wallet_secret, method, host, path)
    except Exception as e:
        print(f"Error generating JWTs: {e}")
        return

    headers = {
        "Authorization": f"Bearer {auth_token}",
        "X-Wallet-Auth": f"Bearer {wallet_auth_token}",
        "Content-Type": "application/json",
        "Accept": "application/json",
    }

    print(f"Sending Solana Transaction from {source_addr}...")
    try:
        resp = requests.post(url, headers=headers, json=payload)
        resp.raise_for_status()
        print("Transaction Sent:")
        print(json.dumps(resp.json(), indent=2))
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        if 'resp' in locals():
            print(resp.text)

if __name__ == "__main__":
    send_solana_transaction()
