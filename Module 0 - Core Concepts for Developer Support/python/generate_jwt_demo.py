import sys
import os
from dotenv import load_dotenv, find_dotenv

# Add root directory to sys.path to allow importing utils
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))
from utils.cdp_auth import generate_jwt

load_dotenv(find_dotenv())

def main():
    key_id = os.getenv("CDP_API_KEY_ID")
    key_secret = os.getenv("CDP_API_KEY_SECRET")
    
    if not key_id or not key_secret:
        print("Error: CDP_API_KEY_ID and CDP_API_KEY_SECRET must be set in .env")
        return

    method = "GET"
    host = "api.cdp.coinbase.com"
    path = "/platform/v2/end-users"

    try:
        token = generate_jwt(key_id, key_secret, method, host, path)
        print(f"Generated JWT:\n{token}")
    except Exception as e:
        print(f"Error generating JWT: {e}")

if __name__ == "__main__":
    main()

