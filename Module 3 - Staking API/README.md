# Module 3: Staking API

## Learning Objectives
- Understand staking concepts and supported networks (ETH shared/dedicated, SOL)
- Follow the staking lifecycle: stake → rewards → unstake → claim/withdraw
- Use Staking API/SDK options correctly per protocol
- Triage common issues (eligibility, rewards visibility, unbonding)
- Know escalation criteria and required diagnostics

---

## 1. Product Overview

- Staking API enables programmatic staking for self-custodial builders across multiple networks.
- Supported (per docs):
  - ETH Shared: any-amount staking on shared validators
  - ETH Dedicated: increments of 32 ETH on dedicated validators
  - SOL Staking: any-amount staking; API manages stake accounts automatically

References:
- Staking API introduction
- SOL Staking overview and usage
- Staking FAQ

---

## 2. Technical Flows (High-level)

### 2.1 Stake
1) Build staking operation with network, asset, address, and protocol-specific options
2) Execute/sign as required by API/SDK
3) Record operation ID and monitor status

Examples of options (illustrative):
- ETH partial/shared: mode=partial, amount (wei)
- ETH dedicated: mode=dedicated, amount=32 ETH multiples
- SOL: amount (lamports), API manages stake accounts

### 2.2 Rewards
- Rewards accrue per protocol schedules
- For SOL: rewards endpoint provides earned rewards; historical rewards may be limited if stake accounts dropped below rent reserve (doc caveat)
- USD conversion is computed near the reward period end via Coinbase rates

### 2.3 Unstake / Claim
- Initiate unstake per protocol (unbonding delays vary)
- SOL: unstake then claim rewards
- ETH: protocol-specific exits; dedicated vs shared differ in operational details

---

## 3. Common Support Scenarios & Troubleshooting

### "Not receiving rewards"
- Verify protocol schedule and bonding/unbonding windows
- SOL: note rent-reserve caveat for historical rewards below reserve; use rewards endpoint time windows
- Confirm correct wallet/address and network

### "Not stakeable / unsupported asset/network"
- Check asset eligibility and network support
- Ensure using correct wallet type (external address for SOL; not App/Prime per docs)

### "Unstake delays / locked assets"
- Explain protocol unbonding periods and state transitions
- Provide expected timelines and how to monitor operation status

---

## 4. Triage Checklists

### Operation Context
- [ ] Asset and network (e.g., ETH mainnet, SOL)
- [ ] Wallet/address and type (external vs App/Prime)
- [ ] Operation IDs and timestamps
- [ ] Amounts and mode (partial/dedicated)

### Rewards
- [ ] Reward periods and accrual expectations
- [ ] Rewards endpoint queries and time ranges
- [ ] USD conversion timestamps

### Protocol Constraints
- [ ] Unbonding/exit periods explained to developer
- [ ] Minimum amounts (e.g., dedicated 32 ETH)
- [ ] Known limitations (e.g., SOL rent reserve history)

---

## 5. Escalation Guide

Collect before escalating:
- Wallet address(es), asset, network
- Operation IDs and related tx hashes
- Timestamps/timezone; reward windows queried
- Endpoint requests/responses (minus secrets)

When to escalate:
- Rewards data inconsistent with documented schedules after grace windows
- Reproducible build/execute failures for valid inputs across multiple users
- Protocol-level incident indicators or widespread API instability

---

## 6. References
- Staking API – Introduction and usage
- SOL Staking – Overview and usage
- Staking FAQ – Rewards, risks, and definitions

---

## 7. Python Samples (Quick Start)

See `python/` folder:
- `staking_jwt.py` – generate JWT for CDP platform staking endpoints
- `build_stake_operation.py` – POST `/platform/v1/stake/build` with options (e.g., ETH partial)
- `list_staking_rewards.py` – GET rewards for an address (path configurable)

Environment hints:
- Export a JWT for staking build:
  - `export REQUEST_METHOD=POST`
  - `export REQUEST_PATH=/platform/v1/stake/build`
  - `export JWT=$(python python/staking_jwt.py)`
- Then run build:
  - `export STAKE_NETWORK_ID=ethereum-hoodi`
  - `export STAKE_ASSET_ID=ETH`
  - `export STAKE_ADDRESS_ID=0xYOUR_ADDRESS`
  - `export STAKE_MODE=partial`
  - `export STAKE_AMOUNT_WEI=100000000000000000`  # 0.1 ETH
  - `python python/build_stake_operation.py`

