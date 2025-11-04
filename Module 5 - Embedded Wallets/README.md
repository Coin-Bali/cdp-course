# Module 5: Embedded Wallets (Smart Wallets)

## Learning Objectives
- Understand Embedded Wallets architecture, passkeys/WebAuthn, and device model
- Initialize the Frontend SDK and integrate with React hooks/components or Wagmi
- Use Smart Accounts (ERC-4337), batching, and gas sponsorship via Paymaster
- Triage common issues (domain allowlist, device compatibility, sponsorship errors)
- Know escalation criteria and required diagnostics

---

## 1. Product Overview

- Frontend SDK provides user-controlled embedded wallets with passkeys/WebAuthn; CDP cannot access user keys.
- Smart Accounts (ERC-4337) enable batching and gas sponsorship via Paymaster.
- Native Onramps integrate alongside Embedded Wallets.

References:
- Frontend SDK packages (@coinbase/cdp-core, cdp-hooks, cdp-react, cdp-wagmi, cdp-solana-standard-wallet)
- React Hooks guide; Wagmi integration; Smart Accounts and Paymaster guides
- Changelog: Smart Accounts support; native Onramps

---

## 2. Technical Flows (High-level)

### 2.1 Initialization & Auth
1) Initialize SDK with `projectId`
2) End-user sign-in (email OTP or supported methods)
3) Create wallet; connect via hooks or Wagmi connector

### 2.2 Smart Accounts & Sponsorship
- Enable smart account features (ERC-4337) via SDK configuration
- Use Paymaster URL or proxy to sponsor gas (Base Sepolia: default sponsorship; Mainnet: configure Paymaster)
- Use Wagmi experimental hooks (`useCapabilities`, `useWriteContracts`)

### 2.3 Domain Allowlisting
- Exact domain matching and HTTPS required
- Configure allowed origins in portal to avoid CORS/widget initialization failures

---

## 3. Common Support Scenarios & Troubleshooting

### "User cannot create a wallet"
- Verify SDK init (`projectId`) and allowed domains
- Check device/browser support for passkeys/WebAuthn; ensure biometrics/security enabled
- Try alternate device or disable privacy features blocking WebAuthn

### "Gas sponsorship failing"
- Inspect Paymaster error codes (e.g., UNAUTHORIZED, GAS_ESTIMATION_ERROR, DENIED_ERROR, UNAVAILABLE_ERROR)
- Confirm policy limits, contract/method allowlisting, and paymaster URL or proxy
- Check network (Base Mainnet vs Base Sepolia) and user op structure

### "Widget or Onramp not appearing"
- Confirm domain allowlist and HTTPS
- Check console/network errors; verify session token (for onramp) not expired/used

---

## 4. Triage Checklists

### Initialization & Environment
- [ ] `projectId` correct; SDK versions noted
- [ ] Domain allowlist includes current origin (exact match)
- [ ] Network and sponsorship config (Base Mainnet vs Sepolia)

### Paymaster & Smart Accounts
- [ ] Paymaster URL/proxy configured
- [ ] Policy limits and allowlisted contracts/methods
- [ ] Error codes/logs captured from hooks/user operations

### Device & Browser
- [ ] OS/browser versions and WebAuthn support
- [ ] Passkeys/biometrics enabled
- [ ] Third-party blockers or strict privacy settings assessed

---

## 5. Escalation Guide

Collect before escalating:
- `projectId`, SDK versions, app URL (origin)
- Device/browser (brand, OS, version), steps to reproduce
- For sponsorship: Paymaster URL/proxy, policy settings, error payloads
- Console/network logs and any correlation IDs

When to escalate:
- Systemic init/auth failures across many domains/users
- Paymaster or smart account infrastructure issues across multiple apps
- Documented behavior mismatches or persistent SDK crashes

---

## 6. References
- Frontend SDK overview and packages
- React Hooks; Wagmi integration; Smart Accounts
- Paymaster introduction and proxy guide

