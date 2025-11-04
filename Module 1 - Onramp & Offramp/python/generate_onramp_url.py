import os
import urllib.parse

# Generates an Onramp hosted URL using an existing session token
# Per docs: https://pay.coinbase.com/buy/select-asset?sessionToken=<token>&defaultNetwork=base&presetFiatAmount=100

BASE_URL = "https://pay.coinbase.com/buy/select-asset"


def build_onramp_url(session_token: str,
                     default_network: str | None = None,
                     default_asset: str | None = None,
                     preset_fiat_amount: str | None = None,
                     preset_crypto_amount: str | None = None,
                     redirect_url: str | None = None) -> str:
    params: dict[str, str] = {"sessionToken": session_token}
    if default_network:
        params["defaultNetwork"] = default_network
    if default_asset:
        params["defaultAsset"] = default_asset
    # Only one of presetFiatAmount or presetCryptoAmount should be provided
    if preset_fiat_amount and preset_crypto_amount:
        raise ValueError("Provide only one of preset_fiat_amount or preset_crypto_amount")
    if preset_fiat_amount:
        params["presetFiatAmount"] = str(preset_fiat_amount)
    if preset_crypto_amount:
        params["presetCryptoAmount"] = str(preset_crypto_amount)
    if redirect_url:
        params["redirectUrl"] = redirect_url
    return f"{BASE_URL}?{urllib.parse.urlencode(params)}"


def main() -> None:
    session_token = os.getenv("SESSION_TOKEN")
    if not session_token:
        raise SystemExit("SESSION_TOKEN env var is required (single-use token from your backend)")

    default_network = os.getenv("DEFAULT_NETWORK", "base")
    default_asset = os.getenv("DEFAULT_ASSET", "USDC")
    redirect_url = os.getenv("REDIRECT_URL")
    preset_fiat_amount = os.getenv("PRESET_FIAT_AMOUNT")
    preset_crypto_amount = os.getenv("PRESET_CRYPTO_AMOUNT")

    url = build_onramp_url(
        session_token=session_token,
        default_network=default_network,
        default_asset=default_asset,
        preset_fiat_amount=preset_fiat_amount,
        preset_crypto_amount=preset_crypto_amount,
        redirect_url=redirect_url,
    )
    print(url)


if __name__ == "__main__":
    main()
