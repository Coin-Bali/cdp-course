import sys
import os
import json
import requests
from dotenv import load_dotenv, find_dotenv

# Add root directory to sys.path to allow importing utils
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))
from utils.cdp_auth import generate_jwt

load_dotenv(find_dotenv())

def create_onramp_session():
    key_id = os.getenv("CDP_API_KEY_ID")
    key_secret = os.getenv("CDP_API_KEY_SECRET")
    
    if not key_id or not key_secret:
        print("Error: CDP_API_KEY_ID and CDP_API_KEY_SECRET must be set in .env")
        return

    host = "api.cdp.coinbase.com"
    path = "/platform/v2/onramp/sessions"
    method = "POST"
    url = f"https://{host}{path}"

    # Required parameters
    destination_address = os.getenv("DESTINATION_ADDRESS")
    purchase_currency = os.getenv("PURCHASE_CURRENCY", "USDC")
    destination_network = os.getenv("DESTINATION_NETWORK", "base")
    
    if not destination_address:
        print("Error: DESTINATION_ADDRESS is required in .env")
        return

    payload = {
        "destinationAddress": destination_address,
        "purchaseCurrency": purchase_currency,
        "destinationNetwork": destination_network,
    }

    # Optional parameters
    if os.getenv("PAYMENT_AMOUNT"):
        payload["paymentAmount"] = os.getenv("PAYMENT_AMOUNT")
        payload["paymentCurrency"] = os.getenv("PAYMENT_CURRENCY", "USD")
    
    if os.getenv("REDIRECT_URL"):
        payload["redirectUrl"] = os.getenv("REDIRECT_URL")

    try:
        token = generate_jwt(key_id, key_secret, method, host, path)
    except Exception as e:
        print(f"Error generating JWT: {e}")
        return

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "Accept": "application/json",
    }

    print(f"Creating Onramp Session with payload: {json.dumps(payload, indent=2)}")
    try:
        resp = requests.post(url, headers=headers, json=payload, timeout=30)
        resp.raise_for_status()
        data = resp.json()
        print("Session Created Successfully:")
        print(json.dumps(data, indent=2))
        
        if "session" in data and "onrampUrl" in data["session"]:
            print(f"\nOnramp URL: {data['session']['onrampUrl']}")
    except requests.exceptions.RequestException as e:
        print(f"Error creating session: {e}")
        if 'resp' in locals():
            print(resp.text)

if __name__ == "__main__":
    create_onramp_session()
