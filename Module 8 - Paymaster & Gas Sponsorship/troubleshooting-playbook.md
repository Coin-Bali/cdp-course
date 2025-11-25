# Module 8: Troubleshooting Playbook

## Common Issues & Solutions

### Problem: "Gas Estimation Error / Preverification Failed"
**Diagnostic Steps:**
1. **Check Sponsorship:** Are you using a Paymaster? If so, check the Paymaster logs in the CDP Portal.
2. **User Funds:** If NOT sponsored, does the user have enough ETH for gas?
3. **Policy:** If sponsored, did the transaction violate a policy (e.g., daily limit exceeded)?

**Solution:**
- Fund the user wallet if self-paying.
- Adjust Paymaster policy limits in the portal.
- Ensure `paymasterAndData` is correctly populated in the UserOperation.

### Problem: "Paymaster Policy Rejection"
**Diagnostic Steps:**
1. **Error Message:** Look for `DENIED_ERROR` or `rejected due to...`.
2. **Global Limit:** Has your organization hit the monthly/global cap ($15k on Mainnet)?
3. **Allowlist:** Is the contract address or function selector allowlisted?

**Solution:**
- Request a limit increase if needed.
- Add the target contract to the allowlist.

### Problem: "Bundler Error: UserOp Reverted"
**Diagnostic Steps:**
1. **Simulation:** The Bundler simulates the transaction before sending. If it reverts, the smart contract logic failed.
2. **Trace:** Inspect the call trace if available.

**Solution:**
- Debug the smart contract logic (e.g., `require` statements failing).
- Ensure parameters passed to the contract function are valid.

---

## Escalation Guide

### When to Escalate to T2
- **Bundler Outage:** Consistent 500 errors from the Bundler endpoint.
- **Paymaster Credits:** Limits are correct but Paymaster is still rejecting valid transactions.

### Required Information for Escalation
1. **Project ID**: `c631...`
2. **UserOperation Hash**: `0x...`
3. **Bundler URL**: `https://api.developer.coinbase.com/rpc/v1/base/...`
4. **Paymaster Policy ID** (if applicable).
5. **Time of Failure**: UTC.

