# Module 1: Coinbase Onramp & Offramp

## Learning Objectives
- Understand Onramp and Offramp user flows and parameters
- Generate secure session-token-based URLs for buy/sell flows
- Configure domain allowlisting and redirects
- Know supported payment methods and regional constraints
- Implement webhooks verification and basic troubleshooting
- Identify escalation criteria and required diagnostics

---

## 1. Product Overview

- Onramp: Let users fund onchain apps from fiat and Coinbase balances using a hosted Coinbase flow.
- Offramp: Let users cash out onchain assets to fiat or Coinbase accounts via a hosted flow.
- Session Tokens: Secure, single-use tokens required for initializing URLs as of 2025-07-31.
- Guest Checkout: US users can deposit with Apple Pay or debit cards without a Coinbase account (limits apply).

References:
- Welcome to Onramp & Offramp
- Session Token Authentication and Changelog update
- Offramp Overview
- Supported Payment Methods

---

## 2. Technical Flows (High-level)

### 2.1 Onramp (Hosted UI)
1) Backend requests a session token with app credentials and init params
2) App constructs a hosted URL with `sessionToken` and optional presets (network, asset, amount)
3) User completes purchase in popup/new tab
4) Redirects to your `redirectUrl`; optionally listen via webhooks (beta) or poll transaction status

Example Onramp URL shape:
`https://pay.coinbase.com/buy/select-asset?sessionToken=<token>&defaultNetwork=base&presetFiatAmount=100`

Notes:
- Widget must open as popup or new tab (no iframe). For mobile, use Custom Tabs / SFSafariViewController.
- Domain allowlist must include your `redirectUrl`.

### 2.2 Offramp (Hosted UI)
1) Backend requests a session token
2) App constructs Offramp URL with `sessionToken`, `partnerUserId`, and `redirectUrl`
3) User clicks “Cash out now” in widget
4) App performs onchain send to the Coinbase-provided `to_address` with the specified `asset`/`amount`
5) Coinbase confirms onchain and deposits fiat/crypto per selected method

Example Offramp URL:
`https://pay.coinbase.com/v3/sell/input?sessionToken=<token>&partnerUserId=user123&redirectUrl=https://yourapp.com/success`

Required/Useful parameters (per docs):
- `sessionToken` (required)
- `partnerUserId` (required on certain flows; < 50 chars)
- `redirectUrl` (required; must be allowlisted)
- `defaultAsset`, `defaultNetwork`, `presetFiatAmount` or `presetCryptoAmount`
- `defaultCashoutMethod` (e.g., `FIAT_WALLET`, `CRYPTO_ACCOUNT`, `ACH_BANK_ACCOUNT`, `PAYPAL`)

Timeouts:
- Offramp sessions: user must perform the onchain send within 30 minutes of clicking “Cash out now”.

---

## 3. Supported Payment Methods

- CRYPTO_ACCOUNT: Buy, Sell – most countries supported
- FIAT_WALLET: Buy, Sell – most countries supported
- CARD: Buy, Sell, Guest Checkout – US and 90+ countries; US credit cards not supported
- ACH_BANK_ACCOUNT: Buy, Sell – US only
- PAYPAL: Sell – Canada, UK, and select regions

Always consult the latest Supported Payment Methods doc for changes.

---

## 4. Configuration Checklist

- Create/secure CDP API keys in environment variables
- Domain allowlist: include all `redirectUrl` domains (localhost allowed for testing)
- Use server-side session token generation (mandatory)
- Open widget in popup or new tab (not iframe; use recommended mobile components)
- For Offramp, implement a step to read `to_address`, `asset`, `network`, `sell_amount` and perform the onchain send promptly

---

## 5. Webhooks (Beta) and Verification

- Onramp webhooks are in beta per changelog; when enabled, verify signatures
- Signature header: `X-Hook0-Signature` (timestamp, header list, HMAC-SHA256)
- Use your webhook `secret` to compute expected signature and compare with timing-safe equality
- Reject stale timestamps to avoid replay attacks

Reference: Webhook signature verification

---

## 6. Troubleshooting Scenarios

- Widget does not open
  - Use popup/new-tab (not iframe); check browser policy and blockers
  - Confirm domain allowlist includes `redirectUrl`
  - Verify session token not expired/used

- Offramp stuck waiting for send
  - Ensure app reads `to_address`, `asset`, `network`, and `sell_amount` via status API and performs onchain send
  - Confirm onchain tx is broadcast to the correct network and has sufficient gas

- ‘Disabled asset’ or unsupported payment method
  - Validate asset/network availability; verify payment method by country

- Redirect errors
  - Exact `redirectUrl` must be allowlisted and URL-encoded where required

- Session token issues
  - Token must be single-use; create fresh per flow
  - Ensure backend clock is correct and credentials are valid

---

## 7. Escalation Guide

Collect before escalating:
- App/Project ID, environment
- Full URL (without secrets) and parameters used
- Session token ID (if available), partnerUserId
- RedirectUrl domain (and proof it’s allowlisted)
- For Offramp: the onchain tx hash, network, asset, and amounts
- Timestamps, user region, payment method, error screenshots/logs

When to escalate:
- Multiple developers report identical widget/session failures
- Session tokens consistently rejected within validity window
- Offramp status API returns inconsistent/undocumented states
- Suspected webhook delivery/signature issues across many events

---

## 8. Next Steps

- See Python scripts in `python/` for URL generation and webhook verification
- Fill `.env` with keys/secrets, copy from `.env.example`
- Test locally with `redirectUrl` on `http://localhost:PORT/callback`
