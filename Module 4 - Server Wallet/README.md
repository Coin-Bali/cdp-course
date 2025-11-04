# Module 4: Server Wallet (WaaS) v2

## Learning Objectives
- Understand v2 Server Wallet capabilities vs v1
- Create and use EVM EOAs, Smart Accounts (ERC-4337), and Solana accounts
- Apply policy and gas sponsorship concepts; integrate swaps
- Triage common issues (auth, network selection, nonce/gas, policy blocks)
- Know pricing model, when to escalate, and what diagnostics to collect

---

## 1. Product Overview

- v2 Server Wallet secures keys in AWS Nitro Enclave TEE and exposes SDK/REST for programmatic wallets.
- Multi-network: EVM (multiple networks per wallet) and Solana.
- Supports EVM EOAs and Smart Accounts (batching, gas sponsorship, spend permissions).
- Integrated swaps/trade from wallet accounts.

References:
- v2 Server Wallet – Welcome & Quickstart
- Accounts (EOA vs Smart Accounts; Solana support)
- Pricing ($0.005 per wallet operation)
- Paymaster (for gas sponsorship)

---

## 2. Technical Flows (High-level)

### 2.1 Account Lifecycle
1) Create account (EVM EOA or Solana; optional Smart Account)
2) Fund (faucets on testnets)
3) Send transaction / sign message
4) Optional: swaps via integrated APIs

### 2.2 Smart Accounts (ERC-4337)
- Batch multiple calls; sponsor gas via Paymaster
- Owner EOA required; one smart account per owner (CDP limitation)
- Deploy on first operation (CREATE2)

### 2.3 Solana Accounts
- Native transactions and message signing
- Batch multiple instructions per transaction
- Fee payer settable for sponsorship-like patterns

### 2.4 Pricing Model
- Write operations billed at $0.005 each (e.g., account creation = 1; send txn = 2; policy eval = 1)
- Billed monthly; reads are free

---

## 3. Common Support Scenarios & Troubleshooting

### "Cannot send transaction"
- Verify network (Base, Ethereum, Arbitrum, Optimism, Polygon, etc.)
- Check balances and nonce; ensure viem/web3 configured to correct RPC
- For Smart Accounts, ensure Paymaster configured and policies allow method/contract

### "Smart account userOp failing"
- Inspect Paymaster response/error (e.g., GAS_ESTIMATION_ERROR, UNAUTHORIZED)
- Confirm sponsorship policy limits and allowlisting of contract/method
- Check bundler availability and network selection

### "Solana send failing"
- Verify recent blockhash handling and fee payer setup
- Confirm lamports and instruction set are valid; check devnet vs mainnet

### "Swaps failing or price mismatch"
- Rebuild quote close to execution time; confirm token approvals/allowances
- Validate network and slippage settings

---

## 4. Triage Checklists

### Authentication & Setup
- [ ] API key id/secret valid; JWT generation correct
- [ ] Environment/network configured
- [ ] SDK version noted

### Transaction Context
- [ ] Account type (EOA/Smart/Solana), address, and network
- [ ] Nonce and gas/fees (EVM) or lamports/fee payer (Solana)
- [ ] Paymaster URL/policy (if used)

### Policies & Sponsorship
- [ ] Contract/method allowlisting
- [ ] Spend limits (per-user/global) and time windows
- [ ] Error codes captured from Paymaster/Bundler

---

## 5. Escalation Guide

Collect before escalating:
- Project ID, account IDs/addresses, network
- Full request/response (minus secrets), SDK versions, timestamps
- For Smart Accounts: userOp payload, Paymaster/bundler endpoints, error codes
- For Solana: serialized tx, program IDs, instruction list

When to escalate:
- Reproducible failures across multiple networks/accounts with valid inputs
- Paymaster/bundler systemic errors, or widespread TEE/signing issues
- Swap API persistent inconsistencies vs documented behavior

---

## 6. References
- v2 Server Wallet – Welcome, Quickstart, Pricing
- Accounts (EOA vs Smart Accounts; Solana features)
- Paymaster – Introduction & integration guides

---

## 7. Python Samples (Quick Start)

See `python/` folder:
- `server_wallet_jwt.py` – generate JWT for v2 REST endpoints
- `create_evm_account.py` – POST create EVM EOA
- `send_evm_transaction.py` – POST send EVM transaction (minimal fields)
- `create_solana_account.py` – POST create Solana account
- `send_solana_transaction.py` – POST send base64 Solana transaction

Environment hints:
- Export a JWT for EVM account creation:
  - `export REQUEST_METHOD=POST`
  - `export REQUEST_PATH=/platform/v2/evm/accounts`
  - `export JWT=$(python python/server_wallet_jwt.py)`
- Create EVM account:
  - `python python/create_evm_account.py`
- Send EVM transaction:
  - `export REQUEST_PATH=/platform/v2/evm/send`
  - `export JWT=$(python python/server_wallet_jwt.py)`
  - `export EVM_ADDRESS=0xYOUR_ADDRESS`
  - `export EVM_TO_ADDRESS=0x0000000000000000000000000000000000000000`
  - `export EVM_VALUE_WEI=1000`
  - `python python/send_evm_transaction.py`

