# Module 7: Coinbase Commerce / Business Payments

## Learning Objectives
- Summarize why Coinbase Commerce is being sunsetted and what the Coinbase Business APIs now handle.
- Understand merchants’ onchain payment lifecycle, including charge creation, timeline updates, webhooks, and settlement semantics.
- Triage webhook delivery issues, mismatched amounts, and charge expirations using Commerce diagnostics before pushing to Business support.
- Know what diagnostic data to include when escalating Commerce issues and when escalation should shift to Coinbase Business.

---

## 1. Product Overview & Transition Context
- **Commerce**: Onchain payment solution for merchants that accepts crypto and settles in USDC; includes REST APIs for charges, checkouts, and webhook confirmation.
- **Migration**: Commerce is being sunsetted and replaced by the broader **Coinbase Business APIs**, which consolidate payments, payouts, trading, and custody workflows. New integrations should target Business APIs, and Commerce customers are guided to migrate their charge-based flows.
- **Key differences**:
  - Commerce is charge-centric with webhooks (`charge:confirmed`, `charge:failed`), while Business is account-based with richer OAuth/key options.
  - Commerce uses shared secrets for webhook signature verification (`X-CC-WEBHOOK-SIGNATURE`), Business uses CB-VERSION + OAuth or API keys for authentication.
- Merchants migrating need to map Commerce charge IDs to Business transaction IDs and adapt their reconciliation/webhook handling.

---

## 2. Technical Flow (Commerce)
1. **Charge Creation**: POST `/charges` with `name`, `description`, `pricing_type` (fixed, no-input, or dynamic). Response returns `charge.code`, `metadata`, `pricing.usd`.  
2. **Customer Payment**: User pays via hosted checkout; Commerce updates `timeline` events (e.g., `charge:pending`, `charge:confirmed`).  
3. **Webhooks & Settlement**: Commerce sends webhook events to merchant `notification_url` with HMAC signature; merchant verifies `X-CC-WEBHOOK-SIGNATURE` using shared secret. On confirmed payment, Coinbase settles funds into merchant wallet/external account.
4. **Merchant Confirmation**: Merchant reads timeline or webhook to confirm success; can use `/charges/{code}` to poll status.

### Webhooks
- Required headers: `X-CC-WEBHOOK-SIGNATURE`, `User-Agent: Coinbase Commerce`.  
- The JSON payload includes `event.type`, `event.data.id`, `event.data.code`, and `event.data.timeline`.  
- Replays are available from the Commerce dashboard; useful when `notification_url` returns non-2xx responses.

---

## 3. Common Support Scenarios & Troubleshooting
### “I’m not receiving webhooks.”
- Confirm the endpoint is HTTPS and reachable; Commerce requires TLS 1.2+.
- Check logs for non-2xx responses; use Commerce dashboard to replay events.
- Validate signatures on headers with the shared secret. If you see `signature mismatch`, confirm the payload (stream vs. text) and time drifts.

### “Customer paid wrong amount or currency.”
- Commerce auto-converts to USDC; check the `pricing` object and timeline for `charge:resolved`.
- If the webhook shows `overpaid`, handle the `timeline` event and optionally refund or alert the user.
- Use `supporting_data` (wallet address + network) provided in the event to reconcile.

### “My checkout session expired.”
- Charges expire after the configured `payment_window`; poll the timeline for `charge:expired`.
- Quick fix: create a fresh charge and direct the user to the new `hosted_url`.
- Ensure the merchant clock is synced; extremely skewed clocks may trigger `expired` or `invalid_signature`.

---

## 4. Escalation Guide
### Collect before Escalating
- Charge ID/code, origin app domain, webhook payload, and HTTP response codes.
- Merchant account status, whether funds were confirmed (timeline + onchain hash + network), and any `timeline` errors.
- Shared secret used for signatures and any proxy/load balancer details.

### When to Escalate
- Confirmed funds missing from merchant account after 24+ hours or multiple `charge:confirmed` with no settlement.
- Platform-wide webhook delivery failure (multiple merchants or repeated retries).
- Credential rotation issues (shared secret/API key) or suspected Commerce backend outage.
- Full migration blockers: e.g., Commerce features missing that are required and require Business-specific adjustments.

### Post-Sunset Migration
- Direct Commerce tickets about migrating to Business APIs to the new Business Payment support channel when customers need account-based payments, OAuth, or deferred settlement features.
- Provide Business-specific docs (OAuth, CB-VERSION header, rate limits, error codes) to T2 teams handling migration requests.

---

## 5. Python Reference Snippet (Charge Creation)
```python
import os, requests
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("COMMERCE_API_KEY")
BASE_URL = "https://api.commerce.coinbase.com"

def create_charge():
    headers = {
        "X-CC-Api-Key": API_KEY,
        "X-CC-Version": "2021-03-05",
        "Content-Type": "application/json",
    }
    payload = {
        "name": "CDP T1 Demo Charge",
        "description": "Test payment",
        "pricing_type": "fixed_price",
        "local_price": {"amount": "25.00", "currency": "USD"},
        "metadata": {"support_ticket": "ABC-123"},
    }
    resp = requests.post(f"{BASE_URL}/charges", headers=headers, json=payload, timeout=15)
    resp.raise_for_status()
    return resp.json()

if __name__ == "__main__":
    print(create_charge()["data"]["hosted_url"])
```

Note: Commerce requires `X-CC-Version` header and API Key authorization. Business APIs now prefer OAuth or API keys with `CB-VERSION`.

---

## 6. Resources
- [Commerce Introduction & Charges](https://docs.cdp.coinbase.com/commerce/introduction/welcome)
- [Commerce API Reference](https://docs.cdp.coinbase.com/api-reference/commerce-api/rest-api/introduction)
- [Coinbase Business APIs Overview](https://docs.cdp.coinbase.com/coinbase-business/introduction/welcome)
- [Business Error Messages](https://docs.cdp.coinbase.com/coinbase-business/api-architecture/error-messages)
- [Business Versioning & Rate Limits](https://docs.cdp.coinbase.com/coinbase-business/api-architecture/versioning)

---

## 6. Scripts & Exercises
1. Copy `.env.example` into `.env` and populate `COMMERCE_API_KEY`, `COMMERCE_SHARED_SECRET`, and `BUSINESS_BEARER_TOKEN`. Keep these secrets out of Git.
2. Use `python/python/verify_webhook.py --payload samples/charge_webhook.json --signature '<header value>'` to validate Commerce webhook payloads before trusting them in production. The script compares HMAC SHA256 signatures and prints the event type/charge code, matching the troubleshooting points above.
3. Run `python/python/business_accounts.py` after populating `BUSINESS_BEARER_TOKEN` to confirm you can reach the Business API, inspect accounts, and verify the `CB-VERSION` header is required.
4. See `exercises.md` for hands-on tasks that exercise webhook handling, expiration failures, and the Commerce → Business migration checklist.

