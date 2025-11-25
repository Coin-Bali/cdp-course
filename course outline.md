# Course Outline: CDP Technical Foundations for T1 Support

## Module 0: Core Concepts for Developer Support

### 1. Introduction
- **Course Objectives: Bridging the Gap Between T1 and T2**
  - Deepen product knowledge across CDP APIs and SDKs to resolve more tickets at T1.
  - Standardize triage: authentication, scopes/permissions, rate limits, environment, and webhooks.
  - Reduce escalations by collecting complete diagnostics and reproducing issues via docs-guided steps.
- **How This Course Will Help You Solve Tickets Faster**
  - Playbooks for common errors and structured escalation checklists.
  - Quick references to auth flows (API keys vs. OAuth2), versioning, and rate limits.

### 2. Foundational API Concepts
- **What is an API? (Client, Server, Request, Response)**
  - CDP REST and JSON-RPC endpoints across products; WebSocket for market data.
- **Understanding API Keys vs. OAuth 2.0: Authentication & Authorization**
  - **API Keys**: Server-to-server for CDP/Business endpoints; enforce IP allowlist and least privilege. **ECDSA required for certain Coinbase App SDKs; Ed25519 not supported for Coinbase App SDK auth**.
  - **OAuth2**: Authorization Code + optional PKCE; scopes define resource access; tokens expire in ~1 hour; refresh via `grant_type=refresh_token` when `offline_access` was requested.
  - Always encrypt/store credentials securely; use `state` to mitigate CSRF; **2FA required for sensitive scopes like `wallet:transactions:send`**.
- **Common HTTP Status Codes and Meanings**
  - 200/201/204 success; 400 validation; 401 unauthorized/invalid/expired token; **402 2FA needed / Payment Required (x402)**; 403 invalid scope; 404 not found; 429 rate limited; 500/503 server/maintenance.
- **Reading API Error Messages**
  - Error payloads include machine-readable id/type and human-readable message; use correlation IDs and linked docs when provided; treat 5xx as unknown completion and check operation status.
- **Understanding API Rate Limits**
  - Typical **10,000 requests/hour per key/app for Coinbase App/Business**; 429 returns `rate_limit_exceeded`; Advanced Trade WebSocket rate limits documented; apply backoff and caching.

### 3. Foundational Web3 Concepts
- **On-chain vs. Off-chain**
  - On-chain tx have hashes, confirmations, fees; off-chain events/webhooks acknowledge processing states.
- **Anatomy of a Crypto Transaction**
  - Address, nonce, gas/gasPrice or max fees, tx hash, block confirmations; chain-specific fee behavior; **ERC-4337 UserOperations for smart accounts**.
- **Mainnet vs. Testnet**
  - Base Mainnet vs. Base Sepolia; sponsorship defaults differ (e.g., sponsored user ops on Base Sepolia); separate RPCs and assets.

---

## Module 1: Coinbase Pay (Onramp/Offramp)

### 1.1 Product Overview
- **What it is/Problem Solved**
  - Embeddable flow for users to fund wallets; integrates with CDP frontends; **optional native onramps alongside Embedded Wallets** per changelog.

### 1.2 Technical Flow
- **High-level User Journey**
  - SDK/init and domain allowlisting requirements; open widget; complete purchase; confirm via webhook callbacks to merchant server.

### 1.3 Common Support Scenarios & Troubleshooting
- **"The Pay widget isn't showing up."**
  - Verify SDK initialization/project configuration.
  - Check browser console errors and **CORS/domain allowlist in project settings**.
  - Confirm correct environment (testnet/mainnet) and latest SDK.
- **"A user's transaction is stuck/pending."**
  - Check on-chain status via block explorer for the network used.
  - Explain block confirmation times; verify webhook delivery and signature validation.
  - Re-try webhook delivery from dashboard if available; confirm HTTPS endpoint and 2xx responses.
- **"Receiving a 'Disabled Asset' error."**
  - Confirm asset and region eligibility per product settings; verify allowed networks and asset list.

### 1.4 Escalation Guide
- **Collect before escalating**
  - App/Project ID, widget/session ID, user region/asset, transaction hash(es), webhook IDs, SDK version, full request/response (sans secrets).
- **When to escalate**
  - Widespread widget loading failures, suspected webhook outage, repeated SDK errors across multiple merchants.

---

## Module 2: Advanced Trade API

### 2.1 Product Overview
- **Who uses it**
  - Programmatic trading, order/bot workflows; REST for orders and **WebSocket for market/order updates**.

### 2.2 Technical Flow
- **Placing and Managing Orders**
  - Create/list/cancel endpoints; auth via API keys or OAuth depending on product; **WebSocket JWT auth for user channels**; respect pagination tokens/params.

### 2.3 Common Support Scenarios & Troubleshooting
- **"My API keys are not working."**
  - Validate key type, permissions/scopes, portfolio restrictions; check IP allowlisting and **signature algorithm guidance (ECDSA required, not Ed25519)**; confirm headers and versioning if relevant.
- **"Insufficient Funds error."**
  - Guide to query balances via API first; confirm portfolio account, settled vs. available balance; check pending holds.
- **"How do I handle pagination?"**
  - Explain pagination scheme (cursor/limit); return full request pattern; ensure consistent ordering and backoff under rate limits.
- **WebSocket rate limits and auth**
  - Ensure JWT generation steps; respect **750 msg/s per IP and 8/s unauthenticated**.

### 2.4 Escalation Guide
- **Collect before escalating**
  - User UUID, API key prefix, portfolio ID, product pair, timestamps/timezone, full request/response with headers, correlation IDs.
- **When to escalate**
  - Suspected matching engine issues, unexplained order discrepancies vs. docs, broad WebSocket auth/channel failures.

---

## Module 3: Staking API

### 3.1 Product Overview
- **Programmatic staking benefits**
  - Delegate on supported networks (**ETH/SOL and others**) via SDK/API; simplified operations and rewards visibility.

### 3.2 Technical Flow
- **Lifecycle**
  - Stake; protocol bonding period; rewards accrual; unstake; unbonding; claim/withdraw. **SOL staking automates stake accounts; rewards retrieved via rewards endpoints**.

### 3.3 Common Support Scenarios & Troubleshooting
- **"Why haven't I received my rewards?"**
  - Check protocol schedules; bonding/unbonding windows; **SOL rewards visibility caveat for stake accounts below rent reserve**; use rewards endpoints and time windows.
- **"Assets are locked; can't unstake."**
  - Explain unbonding periods and protocol differences; confirm asset/network, operation status.
- **"Not Stakeable error for an asset."**
  - Verify asset eligibility and supported network; confirm correct wallet type/address compatibility.

### 3.4 Escalation Guide
- **Collect before escalating**
  - Wallet address, asset ticker/network, operation IDs, tx hashes for stake/unstake attempts, timestamps.
- **When to escalate**
  - Rewards not distributed after documented period, protocol-level incidents, systematic API build/execute failures with valid inputs.

---

## Module 4: Wallet as a Service (WaaS) / Server Wallet

### 4.1 Product Overview
- **What it is**
  - Developer-controlled wallets and automation via SDK/REST; differentiate from user-controlled Embedded Wallets.
  - Types: Developer-Managed (1-of-1) vs. Coinbase-Managed (2-of-2 MPC with Server-Signer); **v2 introduces TEE-backed key security, multi-network EVM scope, Solana support, swaps integration**.

### 4.2 Technical Flow
- **Conceptual Model**
  - Create wallets/accounts, generate addresses, list balances, send transactions, swaps, staking; **Smart Wallet support for backend (batching/paymaster)**.

### 4.3 Common Support Scenarios & Troubleshooting
- **"Trouble creating a wallet for a user."**
  - Verify API credentials (key id/secret/wallet secret for v2), permissions, environment variables; check project configuration and SDK initialization.
- **"Server wallet transaction failed."**
  - Inspect on-chain error, nonce/gas configuration; confirm network, **paymaster usage for smart accounts**; retry with proper fee or sponsorship; validate JSON-RPC body.
- **"How do I manage security for server-side keys?"**
  - Use secret managers, IP allowlisting; least privilege; secure Server-Signer (for 2-of-2); never expose secrets client-side.

### 4.4 Escalation Guide
- **Collect before escalating**
  - Project ID, wallet/account IDs, user ID (if app-level), network, tx hash, request/response logs, SDK version, paymaster URL (if used).
- **When to escalate**
  - Suspected Server-Signer/KMS issues, widespread transaction failures across networks, reproducible SDK crashes.

---

## Module 5: Embedded Wallets (Smart Wallets)

### 5.1 Product Overview
- **Problem Solved**
  - Frictionless onboarding via email/social auth; **passkeys/WebAuthn-based device secrets**; self-custody with secure enclave model; up to 5 devices.
- **Passkeys/WebAuthn**
  - Device-level key generation; Coinbase cannot access user private keys; export/recovery flows documented.

### 5.2 Technical Flow
- **User Journey**
  - Initialize SDK with `projectId`; sign-in (email OTP or other supported auth); create wallet; optional **Smart Accounts (ERC-4337) for batching and sponsorship**; paymaster integration via `paymasterUrl` or `useCdpPaymaster`.
  - Ensure SDK initialized before wallet ops; React hooks and Wagmi connector available.

### 5.3 Common Support Scenarios & Troubleshooting
- **"User can't create a wallet for their device."**
  - Check SDK initialization and **allowed domains**; browser/OS compatibility for passkeys; ensure biometrics/security enabled; try another device.
- **"Transaction failing due to paymaster issues."**
  - Verify paymaster URL, allowlisting, sponsorship limits; inspect **Paymaster error codes (e.g., UNAUTHORIZED, GAS_ESTIMATION_ERROR)**; check sponsored network (Base Sepolia vs Mainnet).
- **"How can a user export their private key?"**
  - Review Security & Export docs; user-controlled export and recovery process; constraints by wallet type and security policy.

### 5.4 Escalation Guide
- **Collect before escalating**
  - App ID/projectId, wallet address, user/session details, device/browser info, relevant tx hashes, paymaster/bundler endpoint, SDK versions.
- **When to escalate**
  - Suspected smart contract or paymaster infra issues, systemic auth/session validation failures, domain allowlist misbehavior.

---

## Module 6: Sign in with Coinbase (SIWC)

### 6.1 Product Overview
- **Value**
  - OAuth2-based identity and wallet data scopes for user consent flows; access balances, transactions, and account data with least-privilege scopes.

### 6.2 Technical Flow
- **OAuth2 Flow**
  - Redirect to `oauth2/auth` with `state` and optional **PKCE (`S256` recommended)**; user consents; callback receives code; exchange at `oauth2/token` for access (and refresh if `offline_access` included); tokens expire in ~1 hour.

### 6.3 Common Support Scenarios & Troubleshooting
- **"Redirect URI is invalid."**
  - Must exactly match registered URIs; URL-encode; confirm environment and correct client app.
- **"Not getting requested wallet permissions."**
  - Verify scopes in auth URL; users may decline; inspect granted scopes via user auth endpoint; request only necessary scopes.
- **"How to refresh an expired access token?"**
  - Use refresh token with `grant_type=refresh_token`; note refresh expiry and one-time exchange behavior; handle 401 for expired tokens.
- **Security Notes**
  - Use `state` for CSRF; encrypt tokens; **2FA required for sensitive actions**; include `CB-VERSION` header where applicable.

### 6.4 Escalation Guide
- **Collect before escalating**
  - Client ID, redirect URI(s), error codes, full auth/token payloads (minus secrets), timestamps.
- **When to escalate**
  - OAuth service outage suspicion, widespread token exchange failures, correct-scope denials across multiple users.

---

## Module 7: Coinbase Commerce / Business

### 7.1 Product Overview
- **Differentiation**
  - Commerce-managed cryptocurrency acceptance vs. developer-controlled on-chain flows; settlement in USDC; webhook-driven confirmations.

### 7.2 Technical Flow
- **Creating Charge and Monitoring**
  - Create/retrieve charge; monitor status via `timeline` and webhooks; verify **webhook HMAC signature `X-CC-WEBHOOK-SIGNATURE`**; support outcomes like under/overpayment and expirations.

### 7.3 Common Support Scenarios & Troubleshooting
- **"Not receiving webhooks."**
  - Ensure HTTPS endpoint reachable, 2xx responses, no auth blocks; verify signature with shared secret; use dashboard to re-send events; check server logs/timeouts.
- **"Customer sent wrong amount/currency."**
  - Explain protocol handling for over/underpayment; rely on charge timeline and webhook updates; follow resolution guidance.
- **"Checkout session expired."**
  - Explain charge lifecycle and expiration behavior; create a new charge.

### 7.4 Escalation Guide
- **Collect before escalating**
  - Charge code/UUID, webhook ID and delivery attempts, transaction hash(es), endpoint URL, timestamps and logs.
- **When to escalate**
  - Confirmed funds not settled post-confirmation window, webhook service delays across many merchants, signature mismatch across multiple deliveries.

---

## Module 8: Paymaster & Gas Sponsorship

### 8.1 Product Overview
- **Problem Solved**
  - Removes gas friction for users by sponsoring transactions; enables "gasless" experience for Smart Wallets.
- **Key Concepts**
  - **ERC-4337 Bundlers**: Infrastructure to process UserOps.
  - **Paymaster**: Smart contract/service that pays for gas.
  - **Policies**: Rules for sponsorship (Global vs Per-User limits, Allowlisting).

### 8.2 Technical Flow
- **Integration**
  - Configure Paymaster in CDP (Network, Policy); generate `paymasterUrl`; integrate with Smart Wallet SDK or Wagmi (using `paymasterServiceUrl`).
  - **Base Sepolia**: Automatic sponsorship (often default).
  - **Base Mainnet**: Requires active Paymaster policy and funding (if not using free tier/credits).

### 8.3 Common Support Scenarios & Troubleshooting
- **"Gas estimation error / Preverification failed."**
  - Check if user has sufficient funds if NOT sponsored, or if Paymaster policy is rejecting the op (e.g., over limit).
- **"Policy Violation / Unauthorized."**
  - Check Per-User limits (daily/total) and Global limits. Confirm contract method is allowlisted (if allowlist enabled).
- **"Paymaster URL invalid."**
  - Ensure URL matches the network (Testnet vs Mainnet).

### 8.4 Escalation Guide
- **Collect before escalating**
  - Paymaster ID/Project ID, Bundler URL, UserOp hash (if available), detailed error JSON, Policy configuration screenshot.

---

## Module 9: CDP Trade API (Onchain Swaps)

### 9.1 Product Overview
- **What it is**
  - API for executing **Onchain Token Swaps** (DEX Aggregation via 0x) on Base/Ethereum.
  - **Distinct from Advanced Trade**: Advanced Trade = Order Book (CEX); Trade API = Onchain Swaps (DEX).

### 9.2 Technical Flow
- **Swap Lifecycle**
  - `Get Quote`: Ask for exchange rate (slippage, gas included).
  - `Execute`: Sign and broadcast transaction (via Server Wallet or external wallet).
  - **Slippage**: Price difference between quote and execution.

### 9.3 Common Support Scenarios & Troubleshooting
- **"Swap failed / Reverted."**
  - Check slippage settings (too low?), insufficient gas (if not sponsored), or liquidity drying up.
- **"Rate seems wrong."**
  - Compare with other aggregators; explain impact of liquidity and price impact for large orders.
- **"Unsupported token."**
  - Verify token is tradable on the network and has sufficient liquidity.

### 9.4 Escalation Guide
- **Collect before escalating**
  - Quote ID, Tx Hash (if generated), Token Pair (In/Out), Amounts, Timestamp.

---

## Module 10: Transfer API (Coinbase App/Business)

### 10.1 Product Overview
- **What it is**
  - **Consumer/Business Transfer API**: Sending crypto/fiat from Coinbase Accounts (CEX) to external addresses or other Coinbase accounts.
  - Distinct from Server Wallet transfers (which are purely onchain from dev-controlled keys).

### 10.2 Technical Flow
- **Send/Withdraw Flow**
  - `POST /v2/accounts/:id/transactions` (type: `send`).
  - **2FA**: often required for API sends (bypass via `wallet:transactions:send` scope + 2FA header or specific API Key permissions).
  - **Idempotency**: Use strict idempotency keys to avoid double sends.

### 10.3 Common Support Scenarios & Troubleshooting
- **"Transfer pending indefinitely."**
  - Check internal transaction status; pending 2FA? Compliance review? Blockchain congestion?
- **"2FA Required (402) error."**
  - Explain 2FA requirement for sensitive scopes; guide to re-authorize or use correct header.
- **"Travel Rule error."**
  - For regulated regions; ensure required beneficiary info is included.

### 10.4 Escalation Guide
- **Collect before escalating**
  - Account ID, Transaction ID (internal), Hash (if broadcast), Error response, Idempotency Key.

---

## Module 11: CDP Data & Oracle APIs

### 11.1 Product Overview
- **Scope**
  - **SQL API**: Query decoded onchain data (Base) via SQL.
  - **Mesh Data API**: Standardized blockchain data access (Blocks, Tx).
  - **Spot Prices**: `GET /v2/prices/:pair/spot`.

### 11.2 Technical Flow
- **SQL API**
  - Write SQL -> Execute -> Get JSON results. Free tier limits apply.
- **Prices**
  - Public endpoints (no auth needed often); strict rate limits.

### 11.3 Common Support Scenarios & Troubleshooting
- **"SQL Query timeout."**
  - Optimize query; add filters (block range, time); explain complexity limits.
- **"Price data stale/wrong."**
  - Verify pair; explain it's "Spot" (average) vs "Buy/Sell" (includes spread).

### 11.4 Escalation Guide
- **Collect before escalating**
  - SQL Query string, Error ID, Time of request.

---

## Module 12: x402 Payment Protocol

### 12.1 Product Overview
- **What it is**
  - Open protocol for **Payment Required (HTTP 402)** flows.
  - Enables "Pay-for-API" or "Pay-for-Content" using crypto instantly.

### 12.2 Technical Flow
- **Facilitator & Bazaar**
  - Client requests resource -> Server returns 402 + Payment Details (Address, Amount).
  - Client pays -> Server verifies -> Returns resource (200 OK).
  - **Facilitator API**: Helps verify/settle these payments.

### 12.3 Common Support Scenarios & Troubleshooting
- **"402 Error when calling API."**
  - This is expected! Explain the flow: user must pay to proceed.
- **"Payment sent but resource not unlocked."**
  - Verify tx confirmation; check `verify` endpoint response; ensure correct amount/asset sent.

---

## Module 13: Faucets & Testnet Tools

### 13.1 Product Overview
- **Purpose**
  - Provide free testnet assets (ETH, USDC) for development (Base Sepolia).

### 13.2 Technical Flow
- **Sources**
  - **Coinbase Faucet (Portal)**: Authenticated, higher limits.
  - **Third-party Faucets**: QuickNode, Alchemy, etc.
  - **Wallet Faucets**: Built-in to Coinbase Wallet for developers.

### 13.3 Common Support Scenarios & Troubleshooting
- **"Faucet dry / Error."**
  - Check daily limits; verify wallet address; try alternative faucet or waiting 24h.
- **"Need more testnet ETH."**
  - Explain bridging from Sepolia ETH or using PoW faucets if available.

---

## Module 14: Coinbase Ecosystem

### 14.1 Module Goal
- **Purpose**
  - Recognize questions outside CDP scope and redirect correctly.
  - **Updated**: Includes Base Appchains and AgentKit.

### 14.2 Base & Base Appchains
- **Base**: L2 (General Support -> Base Discord/Docs).
- **Appchains (L3s)**: Dedicated blockspace for scaling.
  - **Support**: Enterprise/Business tiers often involved; technical issues go to Base engineering or Appchain-specific support channels.
  - **Key Concepts**: Dedicated Sequencer, Custom Gas Token.

### 14.3 AgentKit (AI Agents)
- **What it is**: SDK for AI Agents to perform onchain actions (Trade, Transfer).
- **Integration**: Works with LangChain, OpenAI, CDP Wallets.
- **Support**: Check if issue is *AI Logic* (Out of scope) or *CDP Action* (In scope, e.g., wallet failure).

### 14.4 Redirection Guide (Others)
- **Exchange/Pro**: Help Center.
- **Prime**: Prime Support.
- **Retail**: Help Center.

---

## Module 15: Datadog Debugging & Observability

### 15.1 Product Overview
- **Why Datadog?**
  - Essential for monitoring production integrations with CDP.
  - Provides visibility into **API Latency**, **Error Rates**, and **Rate Limits**.
  - Helps correlate client-side errors with CDP server-side logs using **Correlation IDs**.

### 15.2 Key Concepts
- **Structured Logging (JSON)**
  - Datadog parses JSON logs automatically.
  - **Best Practice**: Always log the `correlation_id` returned in CDP response headers.
- **APM (Application Performance Monitoring)**
  - Use `ddtrace` to automatically instrument Python `requests`.
  - Identify if latency is due to local processing or the external API call.

### 15.3 Common Debugging Scenarios
- **"My API calls are failing intermittently."**
  - Check `cdp.status_code` in logs. If `429`, you are hitting rate limits.
- **"Transactions are slow."**
  - Check APM Traces. If the span to `api.cdp.coinbase.com` is long (>5s), it's network/upstream latency.
- **"Webhooks are missing."**
  - Check if your server is logging any webhook receipt events. If not, check firewall/network.

### 15.4 Setup Guide
1. Install dependencies: `pip install datadog`
2. Set environment variables: `DD_API_KEY`, `DD_APP_KEY`
3. Initialize `datadog.initialize()` in your app.

---
