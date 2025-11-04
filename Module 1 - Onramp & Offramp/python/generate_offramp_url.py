import os
import urllib.parse

# Generates an Offramp hosted URL using an existing session token
# Per docs: https://pay.coinbase.com/v3/sell/input?sessionToken=<token>&partnerUserId=<id>&redirectUrl=<url>&defaultAsset=USDC

BASE_URL = "https://pay.coinbase.com/v3/sell/input"


def build_offramp_url(session_token: str,
                      partner_user_id: str,
                      redirect_url: str,
                      default_asset: str | None = None,
                      default_network: str | None = None,
                      preset_fiat_amount: str | None = None,
                      preset_crypto_amount: str | None = None,
                      disable_edit: bool | None = None,
                      default_cashout_method: str | None = None,
                      fiat_currency: str | None = None) -> str:
    params: dict[str, str] = {
        "sessionToken": session_token,
        "partnerUserId": partner_user_id,
        "redirectUrl": redirect_url,
    }
    if default_asset:
        params["defaultAsset"] = default_asset
    if default_network:
        params["defaultNetwork"] = default_network
    if preset_fiat_amount and preset_crypto_amount:
        raise ValueError("Provide only one of preset_fiat_amount or preset_crypto_amount")
    if preset_fiat_amount:
        params["presetFiatAmount"] = str(preset_fiat_amount)
    if preset_crypto_amount:
        params["presetCryptoAmount"] = str(preset_crypto_amount)
    if disable_edit is not None:
        params["disableEdit"] = "true" if disable_edit else "false"
    if default_cashout_method:
        params["defaultCashoutMethod"] = default_cashout_method
    if fiat_currency:
        params["fiatCurrency"] = fiat_currency
    return f"{BASE_URL}?{urllib.parse.urlencode(params)}"


def main() -> None:
    session_token = os.getenv("SESSION_TOKEN")
    partner_user_id = os.getenv("PARTNER_USER_ID")
    redirect_url = os.getenv("REDIRECT_URL")

    if not session_token:
        raise SystemExit("SESSION_TOKEN env var is required (single-use token from your backend)")
    if not partner_user_id:
        raise SystemExit("PARTNER_USER_ID env var is required (<50 chars unique user id)")
    if not redirect_url:
        raise SystemExit("REDIRECT_URL env var is required and must be domain-allowlisted")

    default_network = os.getenv("DEFAULT_NETWORK", "base")
    default_asset = os.getenv("DEFAULT_ASSET", "USDC")
    preset_fiat_amount = os.getenv("PRESET_FIAT_AMOUNT")
    preset_crypto_amount = os.getenv("PRESET_CRYPTO_AMOUNT")
    default_cashout_method = os.getenv("DEFAULT_CASHOUT_METHOD")
    fiat_currency = os.getenv("FIAT_CURRENCY")

    url = build_offramp_url(
        session_token=session_token,
        partner_user_id=partner_user_id,
        redirect_url=redirect_url,
        default_asset=default_asset,
        default_network=default_network,
        preset_fiat_amount=preset_fiat_amount,
        preset_crypto_amount=preset_crypto_amount,
        default_cashout_method=default_cashout_method,
        fiat_currency=fiat_currency,
    )
    print(url)


if __name__ == "__main__":
    main()
