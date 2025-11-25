# Module 12: x402 Payment Protocol

## 1. Product Overview
- **What is x402?**
  - An open protocol for **Payment Required (HTTP 402)** flows.
  - Enables APIs and content to be monetized instantly via crypto without subscriptions or accounts.
  - **Facilitator**: Coinbase service (API) that verifies and settles payments.
  - **Bazaar**: Discovery catalog for x402 services.

## 2. Technical Flow (The "Handshake")

### Step 1: Client Request
- Client sends `GET /premium-data`.
- Server checks for Payment Proof header (`Authorization` or `X-Payment-Response`).
- If missing, Server returns **402 Payment Required**.
  - Header: `WWW-Authenticate: x402 scheme="exact", network="base", address="0x...", amount="1000000", asset="0x..."`
  - Body: JSON with details (optional but recommended).

### Step 2: Client Payment
- Client parses the 402 header.
- Client sends an onchain transaction (e.g., `transfer` of USDC on Base) to the `address`.
- Client waits for tx hash.

### Step 3: Client Retry with Proof
- Client resends `GET /premium-data`.
- Header: `X-Payment-Response: <tx_hash>` (or signed proof object).

### Step 4: Server Verification
- Server receives request with `X-Payment-Response`.
- Server calls CDP Facilitator: `POST /v2/x402/verify`.
- If valid, Server returns **200 OK** with the data.

## 3. Common Support Scenarios & Troubleshooting
- **"API returns 402 error"**
  - **Cause**: This is intended. The client must pay.
  - **Fix**: Ensure the client handles x402 responses (using `useX402` or custom logic).
- **"Payment sent but verified failed"**
  - **Cause**: Transaction not confirmed yet, wrong amount sent (wei vs ether units), or wrong asset (USDC vs ETH).
  - **Fix**: Check transaction status on explorer. Verify headers match the sent transaction.
- **"Facilitator verification error"**
  - **Cause**: Replay attack (using same tx hash twice) or Facilitator API key issues on seller side.

## 4. Escalation Guide
- **Collect Data**
  - API Endpoint.
  - Transaction Hash (Payment).
  - Facilitator Request ID (if available).
  - 402 Response Headers.
- **Escalate When**
  - Valid payments are consistently rejected by the Facilitator.
  - Protocol-level integration issues.

## 5. Resources
- [x402 Documentation](https://docs.cdp.coinbase.com/x402/welcome)
- [x402 GitHub](https://github.com/coinbase/x402)
