import os
import time
import secrets
import jwt
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import ec, ed25519

def generate_jwt(api_key_id, api_key_secret, request_method=None, request_host=None, request_path=None, expires_in=120):
    """
    Generates a CDP Bearer Token (JWT) for authenticating requests.
    Supports both ECDSA (ES256) and Ed25519 (EdDSA) keys.
    
    Args:
        api_key_id (str): The API Key ID.
        api_key_secret (str): The API Key Private Key (PEM format).
        request_method (str, optional): HTTP Method (GET, POST). If None, 'uri' claim is omitted (for WebSockets).
        request_host (str, optional): Hostname (e.g. api.cdp.coinbase.com).
        request_path (str, optional): URI Path (e.g. /v2/orders).
        expires_in (int): Token expiration in seconds.
    """
    if not api_key_id or not api_key_secret:
        raise ValueError("api_key_id and api_key_secret are required")

    # Normalize key secret (handle potential escaped newlines from .env)
    if "\\n" in api_key_secret:
        api_key_secret = api_key_secret.replace("\\n", "\n")

    # Load the private key
    try:
        private_key = serialization.load_pem_private_key(
            api_key_secret.encode('utf-8'),
            password=None
        )
    except Exception as e:
        raise ValueError(f"Failed to load private key: {e}")

    # Determine algorithm based on key type
    if isinstance(private_key, ec.EllipticCurvePrivateKey):
        algorithm = 'ES256'
    elif isinstance(private_key, ed25519.Ed25519PrivateKey):
        algorithm = 'EdDSA'
    else:
        raise ValueError("Unsupported key type. Must be ECDSA or Ed25519.")

    now = int(time.time())
    jwt_payload = {
        'sub': api_key_id,
        'iss': "cdp",
        'nbf': now,
        'exp': now + expires_in,
    }

    # Add URI claim only if method/host/path are provided (REST API)
    if request_method and request_host and request_path:
        jwt_payload['uri'] = f"{request_method} {request_host}{request_path}"

    headers = {
        'kid': api_key_id,
        'nonce': secrets.token_hex()
    }

    jwt_token = jwt.encode(
        jwt_payload,
        private_key,
        algorithm=algorithm,
        headers=headers
    )
    
    return jwt_token
