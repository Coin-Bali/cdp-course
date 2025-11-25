import os
import requests
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

# Format: https://api.developer.coinbase.com/rpc/v1/base/{YOUR_API_KEY}
CDP_NODE_RPC_URL = os.getenv("CDP_NODE_RPC_URL") 

def get_latest_block():
    if not CDP_NODE_RPC_URL:
        print("Error: CDP_NODE_RPC_URL not set in .env")
        return

    headers = {"Content-Type": "application/json"}
    
    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "eth_getBlockByNumber",
        "params": ["latest", False]
    }

    try:
        print(f"Fetching latest block...") 
        response = requests.post(CDP_NODE_RPC_URL, headers=headers, json=payload)
        response.raise_for_status()
        print(response.json())

    except requests.exceptions.RequestException as e:
        print(f"RPC Connection Error: {e}")

if __name__ == "__main__":
    get_latest_block()
