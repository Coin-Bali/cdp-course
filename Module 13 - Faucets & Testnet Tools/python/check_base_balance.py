import requests
import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

def check_base_sepolia_balance():
    target_address = os.getenv("BASE_SEPOLIA_ADDRESS")
    if not target_address:
        print("Error: BASE_SEPOLIA_ADDRESS not set in .env")
        return

    rpc_url = "https://sepolia.base.org" 

    headers = {"Content-Type": "application/json"}

    payload = {
        "jsonrpc": "2.0",
        "method": "eth_getBalance",
        "params": [target_address, "latest"],
        "id": 1
    }

    print(f"Checking balance for {target_address}...")

    try:
        response = requests.post(rpc_url, headers=headers, json=payload)
        response.raise_for_status()
        rpc_response = response.json()

        if "result" in rpc_response:
            balance_wei = int(rpc_response["result"], 16)
            balance_eth = balance_wei / (10**18)
            print(f"Balance: {balance_eth} ETH")
        else:
            print(rpc_response)
        
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    check_base_sepolia_balance()
