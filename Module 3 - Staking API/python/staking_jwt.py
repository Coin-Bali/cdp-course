import os
import time
import secrets
import jwt
from cryptography.hazmat.primitives import serialization

# Generates a Bearer JWT for CDP platform staking REST endpoints
# Env vars required:
#   CDP_API_KEY_ID: organizations/{org_id}/apiKeys/{key_id}
#   CDP_API_KEY_SECRET: PEM EC private key (ES256)
#   REQUEST_METHOD: e.g., POST
#   REQUEST_HOST: default api.cdp.coinbase.com
#   REQUEST_PATH: e.g., /platform/v1/stake/build
# Optional:
#   EXPIRES_IN seconds (default 120)


def main() -> None:
    key_id = os.getenv("CDP_API_KEY_ID")
    key_secret = os.getenv("CDP_API_KEY_SECRET")
    method = os.getenv("REQUEST_METHOD", "POST")
    host = os.getenv("REQUEST_HOST", "api.cdp.coinbase.com")
    path = os.getenv("REQUEST_PATH", "/platform/v1/stake/build")
    expires_in = int(os.getenv("EXPIRES_IN", "120"))

    if not key_id or not key_secret:
        raise SystemExit("CDP_API_KEY_ID and CDP_API_KEY_SECRET are required")

    private_key = serialization.load_pem_private_key(key_secret.encode("utf-8"), password=None)

    now = int(time.time())
    payload = {
        "sub": key_id,
        "iss": "cdp",
        "nbf": now,
        "exp": now + expires_in,
        "uri": f"{method} {host}{path}",
    }
    headers = {"kid": key_id, "nonce": secrets.token_hex()}

    token = jwt.encode(payload, private_key, algorithm="ES256", headers=headers)
    print(token)


if __name__ == "__main__":
    main()
