import os
import time
import secrets
import json
import requests
import jwt
from cryptography.hazmat.primitives import serialization

API_HOST = "api.cdp.coinbase.com"
API_PATH = "/platform/v2/onramp/sessions"
API_URL = f"https://{API_HOST}{API_PATH}"


def build_jwt(key_id: str, key_secret_pem: str, method: str, host: str, path: str, expires_in: int = 120) -> str:
    private_key = serialization.load_pem_private_key(key_secret_pem.encode("utf-8"), password=None)
    now = int(time.time())
    payload = {
        "sub": key_id,  # full resource name like organizations/{org}/apiKeys/{key}
        "iss": "cdp",
        "nbf": now,
        "exp": now + expires_in,
        # For HTTP requests, CDP expects a single 'uri' claim as METHOD host/path
        "uri": f"{method} {host}{path}",
    }
    headers = {"kid": key_id, "nonce": secrets.token_hex()}
    token = jwt.encode(payload, private_key, algorithm="ES256", headers=headers)
    return token


def create_onramp_session(jwt_token: str, body: dict) -> dict:
    headers = {
        "Authorization": f"Bearer {jwt_token}",
        "Content-Type": "application/json",
        "Accept": "application/json",
    }
    resp = requests.post(API_URL, headers=headers, data=json.dumps(body), timeout=30)
    if resp.status_code not in (200, 201):
        raise RuntimeError(f"Onramp session error {resp.status_code}: {resp.text}")
    return resp.json()


def main() -> None:
    key_id = os.getenv("CDP_API_KEY_ID")
    key_secret = os.getenv("CDP_API_KEY_SECRET")
    redirect_url = os.getenv("REDIRECT_URL")

    # Required per docs: destinationAddress, purchaseCurrency, destinationNetwork
    destination_address = os.getenv("DESTINATION_ADDRESS")
    purchase_currency = os.getenv("PURCHASE_CURRENCY", os.getenv("DEFAULT_ASSET", "USDC"))
    destination_network = os.getenv("DESTINATION_NETWORK", os.getenv("DEFAULT_NETWORK", "base"))

    if not key_id or not key_secret:
        raise SystemExit("CDP_API_KEY_ID and CDP_API_KEY_SECRET are required")
    if not destination_address or not purchase_currency or not destination_network:
        raise SystemExit("DESTINATION_ADDRESS, PURCHASE_CURRENCY, and DESTINATION_NETWORK are required")

    jwt_token = build_jwt(
        key_id=key_id,
        key_secret_pem=key_secret,
        method="POST",
        host=API_HOST,
        path=API_PATH,
    )

    body: dict = {
        "destinationAddress": destination_address,
        "purchaseCurrency": purchase_currency,
        "destinationNetwork": destination_network,
    }

    # Optional for one-click: paymentAmount/paymentCurrency (+ quote fields if desired)
    payment_amount = os.getenv("PAYMENT_AMOUNT")
    payment_currency = os.getenv("PAYMENT_CURRENCY")
    if payment_amount and payment_currency:
        body["paymentAmount"] = str(payment_amount)
        body["paymentCurrency"] = payment_currency

    # Quote enhancements
    payment_method = os.getenv("PAYMENT_METHOD")  # e.g., CARD
    country = os.getenv("COUNTRY")                # e.g., US
    subdivision = os.getenv("SUBDIVISION")        # e.g., NY
    if payment_method and country and subdivision:
        body["paymentMethod"] = payment_method
        body["country"] = country
        body["subdivision"] = subdivision

    if redirect_url:
        body["redirectUrl"] = redirect_url

    client_ip = os.getenv("CLIENT_IP")
    if client_ip:
        body["clientIp"] = client_ip

    result = create_onramp_session(jwt_token, body)
    print(json.dumps(result, indent=2))
    session = result.get("session", {})
    if "onrampUrl" in session:
        print("\nOnramp URL:")
        print(session["onrampUrl"])


if __name__ == "__main__":
    main()
