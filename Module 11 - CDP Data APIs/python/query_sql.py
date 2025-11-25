import sys
import os
import requests
import json
from dotenv import load_dotenv, find_dotenv

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))
from utils.cdp_auth import generate_jwt

load_dotenv(find_dotenv())

def run_sql_query():
    key_id = os.getenv("CDP_API_KEY_ID")
    key_secret = os.getenv("CDP_API_KEY_SECRET")

    if not key_id or not key_secret:
        print("Error: keys required")
        return

    host = "api.cdp.coinbase.com"
    path = "/platform/v2/data/query/run"
    method = "POST"
    url = f"https://{host}{path}"

    payload = {
        "sql": "SELECT block_number, transaction_hash FROM base.transactions WHERE block_number > 1000000 LIMIT 5"
    }

    try:
        token = generate_jwt(key_id, key_secret, method, host, path)
    except Exception as e:
        print(f"Error generating JWT: {e}")
        return

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }

    print("Running SQL Query...")
    try:
        resp = requests.post(url, headers=headers, json=payload)
        resp.raise_for_status()
        print("Result:")
        print(json.dumps(resp.json(), indent=2))
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        if 'resp' in locals():
            print(resp.text)

if __name__ == "__main__":
    run_sql_query()

