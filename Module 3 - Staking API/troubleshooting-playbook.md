# Module 3: Troubleshooting Playbook

## Common Issues & Solutions

### Problem: "Asset not stakeable error"
**Diagnostic Steps:**
1. **Check Asset & Network:** Is the user trying to stake `BTC`? (Only ETH, SOL, etc. are supported). Is the network correct (`ethereum-mainnet` vs `ethereum-hoodi`)?
2. **Check Address Compatibility:** Is the address a valid Staking address? (For some protocols, you cannot stake from a contract address without specific setup).
3. **Minimum Amount:** Is the amount below the protocol minimum? (e.g., Partial ETH staking has very low minimums, but Dedicated requires 32 ETH).

**Solution:**
- Verify the asset is on the supported list.
- Ensure the network ID in the API call matches the environment (Testnet vs Mainnet).

### Problem: "Rewards are not showing up"
**Diagnostic Steps:**
1. **Check Protocol:**
   - **ETH:** Rewards auto-compound or accumulate depending on the method (Partial vs Dedicated).
   - **SOL:** Rewards are added to the stake account balance at the end of each epoch (~2-3 days).
2. **Rent Reserve (SOL):** For Solana, if the stake account balance is close to the rent reserve, rewards might not be immediately visible/withdrawable until the account is closed or topped up.
3. **Timeframe:** Has the bonding period passed? (ETH: ~12-24h to activate; SOL: 1 epoch to activate).

**Solution:**
- Explain the protocol-specific timeline (Activation queue + Bonding period).
- For SOL, check if the account is in "Active" state.

### Problem: "403 Forbidden when staking"
**Diagnostic Steps:**
1. **Permissions:** Does the API Key have `Trade` or `Transfer` permissions? Staking is often considered a "Transfer" or specific "Staking" action depending on the granular scopes.
2. **Restricted Region:** Is the user in a jurisdiction where staking is restricted (e.g., parts of US/Canada for retail)?

**Solution:**
- Update API Key permissions.
- Verify user's verified region in their profile.

---

## Escalation Guide

### When to Escalate to T2
- **Slashing Event:** User reports a loss of principal due to validator slashing. (Critical Severity).
- **Stuck Unbonding:** Assets have been in "Unbonding" state for significantly longer than the protocol standard (e.g., ETH > 10 days without finalization).
- **Double Signing:** Any report of validator double-signing.

### Required Information for Escalation
1. **Stake Operation ID**: The UUID returned by the build/sign call.
2. **Validator Address**: The validator they delegated to.
3. **User Address**: The wallet address holding the stake.
4. **Asset & Network**: e.g., `SOL` on `mainnet`.
5. **Time of Initial Request**: UTC.

