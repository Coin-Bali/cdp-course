#!/usr/bin/env python3
"""Fetch Coinbase Business accounts and balances."""
import os
import requests
from dotenv import load_dotenv
from pathlib import Path

load_dotenv(dotenv_path=Path(__file__).parents[1] / ".env")

BASE_URL = "https://api.coinbase.com/v2"
TOKEN = os.getenv("BUSINESS_BEARER_TOKEN")
CB_VERSION = os.getenv("CB_VERSION", "2024-01-06")


def get_headers():
    if not TOKEN:
        raise SystemExit("Set BUSINESS_BEARER_TOKEN in your Module 7 .env file before running this script.")
    return {
        "Authorization": f"Bearer {TOKEN}",
        "CB-VERSION": CB_VERSION,
        "Content-Type": "application/json",
    }


def fetch_accounts():
    resp = requests.get(f"{BASE_URL}/accounts", headers=get_headers(), timeout=15)
    resp.raise_for_status()
    return resp.json()


def main():
    print("Fetching Coinbase Business accounts...")
    data = fetch_accounts()
    for acct in data.get("data", []):
        print(f"Account: {acct['name']} ({acct['currency']})")
        balance = acct.get("balance", {})
        print(f"  Balance: {balance.get('amount')} {balance.get('currency')}")
        print(f"  ID: {acct['id']}")
        print("  Status:", acct.get("status"))
        print("  -----")


if __name__ == "__main__":
    main()
