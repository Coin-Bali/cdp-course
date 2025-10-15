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
  - 200/201/204 success; 400 validation; 401 unauthorized/invalid/expired token; **402 2FA needed**; 403 invalid scope; 404 not found; 429 rate limited; 500/503 server/maintenance.
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
- **"User can't create a wallet on their device."**
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
 
## Module 8: Coinbase Ecosystem Overview (for Redirection)
 
### 8.1 Module Goal
- **Purpose**
  - Recognize questions outside CDP scope and redirect correctly to reduce misrouted tickets.
 
### 8.2 Base
- **What it is**
  - Ethereum L2 for low-cost dApps.
- **Key Takeaway**
  - Queries about Base RPCs, contract deployment, node issues are out-of-scope for CDP T1.
- **Where to Redirect**
  - Base documentation, Base Discord/community, Base status pages.
 
### 8.3 Coinbase Exchange / Pro
- **What it is**
  - Professional trading UI distinct from Advanced Trade API.
- **Key Takeaway**
  - Clarify UI vs API; asset listing questions are non-CDP.
- **Where to Redirect**
  - Standard Coinbase customer support for Exchange/Pro.
 
### 8.4 Coinbase International Exchange
- **What it is**
  - Perpetual futures/spot for eligible non-US institutions.
- **Key Takeaway**
  - Confirm whether they mean Advanced Trade API vs International Exchange API.
- **Where to Redirect**
  - International Exchange support channels.
 
### 8.5 Coinbase retail
- **Scope**
  - Login/account access queries are retail support, not CDP.
- **Redirect**
  - Coinbase retail customer support.
 
### 8.6 Coinbase Prime
- **What it is**
  - Institutional custody/trading/financing.
- **Key Takeaway**
  - Separate platform and APIs from CDP.
- **Where to Redirect**
  - Prime account manager/Prime support.
 
### 8.7 Coinbase Derivatives
- **What it is**
  - CFTC-regulated US futures exchange.
- **Key Takeaway**
  - API access for these products is not CDP.
- **Where to Redirect**
  - Coinbase Derivatives support channels.
 
---
 
## Handy Triage Checklists (Appendix)
 
### Authentication
- API key type, permissions/scopes, IP allowlist; OAuth `state`, PKCE; token expiry and refresh; **2FA for sensitive scopes**; secure storage.
 
### Headers/Versioning
- Include required headers (`CB-VERSION` where applicable); correct content types; correlation IDs.
 
### Rate Limits
- Identify 429 responses; apply exponential backoff; cache non-volatile data; respect WebSocket limits.
 
### Webhooks
- HTTPS only; verify signatures; capture delivery logs; allow re-delivery; idempotency at receiver.
 
### Environments
- Confirm network (Base Mainnet vs Base Sepolia) and RPC endpoints; paymaster sponsorship differences.
 
### On-chain
- Inspect tx hash/status, nonce, gas; interpret revert data; protocol-specific delays (staking).
 
### Paymaster Troubleshooting
- **Policy Limits**: Per-user and global spend limits; gas policy configuration; allowlisting contracts/methods.
- **Error Codes**: UNAUTHORIZED, GAS_ESTIMATION_ERROR, DENIED_ERROR, UNAVAILABLE_ERROR.
- **Common Issues**: Insufficient gas, invalid paymaster signature, policy violations.
 
### Domain Allowlisting (Embedded Wallets)
- CORS configuration for allowed domains; exact match requirements; HTTPS enforcement.
- Browser compatibility for passkeys/WebAuthn; device-specific key storage.
 
### Staking-Specific
- **SOL Limitations**: External addresses only (not Coinbase App/Prime addresses); rent reserve considerations for historical rewards.
- **ETH Staking**: Shared vs. dedicated validators; 32 ETH minimum for dedicated; onchain billing setup.
- **Rewards**: Protocol-specific schedules; USD conversion rates; historical data limitations.
 
### Server Wallet v2 vs v1
- **v2 Features**: TEE-backed security, multi-network EVM scope, Solana support, integrated swaps.
- **Migration**: v1 USDC rewards phasing out; encourage v2 adoption.
- **Pricing**: $0.005 per wallet operation; usage-based billing.
 
### Advanced Trade WebSocket
- **Rate Limits**: 750 messages/second per IP; 8/second unauthenticated.
- **Authentication**: JWT tokens for user-specific channels; market data channels public.
- **Connection Management**: Proper subscription handling; reconnection logic.
 
### Error Response Patterns
- **Standard Format**: `{"errors": [{"id": "error_type", "message": "description", "url": "doc_link"}]}`
- **Common Types**: `rate_limit_exceeded`, `invalid_scope`, `two_factor_required`, `authentication_error`.
- **Validation Errors**: Multiple errors in array for 400 responses.
 
### Security Best Practices
- **API Keys**: ECDSA signature algorithm (not Ed25519 for Coinbase App); IP allowlisting; least privilege permissions.
- **OAuth2**: State parameter for CSRF; PKCE for additional security; encrypted token storage.
- **2FA**: Required for `wallet:transactions:send` scope; CB-2FA-TOKEN header for retry requests.
 
### Network-Specific Considerations
- **Base Sepolia**: Default sponsorship for user operations; testnet environment.
- **Base Mainnet**: Paymaster configuration required; production environment.
- **Ethereum**: Higher gas costs; different confirmation times.
- **Solana**: Different transaction model; account-based vs. UTXO.
 
### Webhook Security
- **Commerce**: `X-CC-WEBHOOK-SIGNATURE` HMAC verification; shared secret validation.
- **General**: HTTPS endpoints only; 2xx response codes; signature verification before processing.
- **Retry Logic**: Exponential backoff; idempotency handling; delivery confirmation.
 
### Troubleshooting Workflow
1. **Collect**: Full request/response, headers, timestamps, correlation IDs, user context.
2. **Reproduce**: Use docs-guided steps; test with minimal configuration.
3. **Isolate**: Check authentication, permissions, rate limits, network status.
4. **Escalate**: Include all collected data; specify suspected root cause; reference relevant docs.
