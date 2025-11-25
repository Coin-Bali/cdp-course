# Module 10: Transfer API (Coinbase App & Business)

## 1. Product Overview
- **What is the Transfer API?**
  - Enables programmatic sending/receiving of crypto and fiat from **Coinbase Accounts** (Custodial/CEX).
  - **Target Audience**:
    - **Coinbase App Users**: Sending funds to friends or external wallets via OAuth apps.
    - **Business Users**: Automating payouts or treasury management.
- **Difference from Server Wallet**:
  - **Transfer API**: Moves funds from *Coinbase Custody* (Coinbase holds keys).
  - **Server Wallet**: Moves funds from *Developer-Controlled Wallets* (You/MPC hold keys).

## 2. Technical Flow
- **Send Money (Consumer v2)**
  - **Endpoint**: `POST /v2/accounts/:account_id/transactions`
  - **Auth**: OAuth2 (Scope: `wallet:transactions:send`) or API Key (Permissions: `wallet:transactions:send`).
  - **2FA**: Often required. If 402 returned, user must authorize via 2FA (or use `CB-2FA-Token` header).
- **Business Transfers**
  - **Endpoint**: `POST /api/v3/brokerage/accounts/:account_uuid/transfers` (Withdrawal).
  - **Auth**: CDP API Key (Business Portfolio).

## 3. Common Support Scenarios & Troubleshooting
- **"Transfer pending / stuck"**
  - **Cause**: Internal compliance checks, blockchain congestion, or waiting for 2FA.
  - **Fix**: Check `status` field (`pending`, `completed`, `failed`). If `pending` for >1 hour, escalate for compliance review.
- **"402 2FA Required"**
  - **Cause**: API Key or OAuth token requires 2FA verification for this action.
  - **Fix**: Re-authenticate with 2FA or provide `CB-2FA-Token` header (if supported by flow).
- **"Invalid Address / Destination Tag"**
  - **Cause**: Sending XRP/XLM/etc. without a Memo/Tag.
  - **Fix**: Ensure `destination_tag` or `memo` field is included for Memo-based chains.

## 4. Escalation Guide
- **Collect Data**
  - Account ID.
  - Transaction ID (Internal UUID).
  - Transaction Hash (if broadcast).
  - Destination Address.
- **Escalate When**
  - Transaction shows "Completed" in API but no Hash generated.
  - "Funds frozen" errors.

## 5. Resources
- [Coinbase App API (v2) Docs](https://docs.cdp.coinbase.com/coinbase-app/introduction/welcome)
- [Business Transfer API Docs](https://docs.cdp.coinbase.com/coinbase-business/introduction/welcome)

