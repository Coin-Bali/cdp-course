import requests
import json
import time

# This script acts as a sophisticated Buyer Client that:
# 1. Calls an API.
# 2. Catches the 402 Payment Required.
# 3. Parses the payment details.
# 4. "Simulates" a payment (since we can't sign real txs without a private key here).
# 5. Retries the request with the proof.

TARGET_API_URL = "http://localhost:5002/premium-data"

def run_buyer_flow():
    # --- Step 1: Initial Request ---
    print(f"1. Requesting: {TARGET_API_URL}")
    resp = requests.get(TARGET_API_URL)
    
    if resp.status_code == 200:
        print("Success! Resource received immediately (Maybe free?).")
        print(resp.json())
        return

    if resp.status_code != 402:
        print(f"Unexpected Error: {resp.status_code}")
        return

    # --- Step 2: Parse 402 Response ---
    print("\n2. Received 402 Payment Required")
    auth_header = resp.headers.get("WWW-Authenticate")
    print(f"   Header: {auth_header}")
    
    # Basic parsing of the x402 header string (e.g., x402 scheme="exact", network="base", ...)
    # In production, use a robust parser or regex.
    details = {}
    if auth_header and auth_header.startswith("x402"):
        # Strip 'x402 ' and split by comma
        params = auth_header[5:].split(",") 
        for p in params:
            key, val = p.split("=")
            details[key.strip()] = val.strip().strip('"')
    
    print(f"   Parsed Details: {json.dumps(details, indent=2)}")
    
    payment_address = details.get("address")
    amount = details.get("amount")
    asset = details.get("asset")
    
    if not all([payment_address, amount]):
        print("   Error: Missing payment details in header.")
        return

    # --- Step 3: Execute Payment (Simulation) ---
    print(f"\n3. Simulating Payment of {amount} units of {asset} to {payment_address}...")
    # IN REALITY: You would use web3.py or a wallet to sign and broadcast a transaction here.
    # tx_hash = w3.eth.send_transaction(...)
    
    # We simulate a tx hash for the demo
    mock_tx_hash = "0x" + "a" * 64 
    print(f"   Payment Sent! Tx Hash: {mock_tx_hash}")
    
    # --- Step 4: Retry with Proof ---
    print("\n4. Retrying Request with Payment Proof...")
    headers = {
        "X-Payment-Response": mock_tx_hash
    }
    
    retry_resp = requests.get(TARGET_API_URL, headers=headers)
    
    if retry_resp.status_code == 200:
        print("\n5. Success! Payment Verified.")
        print("   Data:", retry_resp.json())
    elif retry_resp.status_code == 402:
        print("\n   Failed: Payment rejected or insufficient.")
        print("   Server Message:", retry_resp.text)
    else:
        print(f"\n   Error: {retry_resp.status_code}")

if __name__ == "__main__":
    print("--- x402 Buyer Client Demo ---")
    print("Note: Ensure 'python x402_seller_server.py' is running in another terminal.\n")
    try:
        run_buyer_flow()
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to localhost:5002. Is the Seller Server running?")

