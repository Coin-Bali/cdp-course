# Module 4: Troubleshooting Playbook

## Common Issues & Solutions

### Problem: "401 Unauthorized (Wallet Secret)"
**Diagnostic Steps:**
1. **Identify the Request:** Is this a *signing* operation (Create Wallet, Send Tx)?
2. **Check Credentials:** These operations require the `Wallet Secret` (X-Wallet-Auth header), not just the standard API Key.
3. **Env Var:** Ensure `CDP_WALLET_SECRET` is set in your `.env` and follows the PEM format (newlines replaced by `\n` if using the Python script helper).

**Solution:**
- Generate a new Wallet Secret in the CDP Portal if lost.
- Ensure the script loads the secret correctly.

### Problem: "Transaction Failed (Onchain)"
**Diagnostic Steps:**
1. **Check Error Code:** Is it `insufficient_funds`, `nonce_too_low`, or `gas_limit_exceeded`?
2. **Check Balance:** Does the server wallet have enough ETH (for gas) + Value to send?
3. **Network:** Are you sending a `base-sepolia` transaction but checking `base-mainnet` explorer?

**Solution:**
- Fund the wallet (use a Faucet for testnet).
- If `nonce` issue: The wallet might have sent another tx recently that is pending. Wait or resubmit with higher gas.

### Problem: "Wallet creation failed"
**Diagnostic Steps:**
1. **Permissions:** Does the API Key have `Wallets:Create` permission?
2. **Limit Reached:** Is the project hitting the max number of wallets allowed (default limits apply)?

**Solution:**
- Check permissions in Portal.
- Contact sales/support if wallet limit increase is needed.

---

## Escalation Guide

### When to Escalate to T2
- **Key Compromise:** Suspicion that a Server-Signer key has been leaked.
- **Systemic Signer Failure:** All signing requests returning 500 errors (indicates internal HSM/MPC issue).
- **Ledger Desync:** Wallet balance is correct onchain but shows 0 in the API for >1 hour.

### Required Information for Escalation
1. **Wallet ID**: The UUID of the CDP Wallet.
2. **Transaction Hash**: If generated.
3. **Request ID**: From the response header.
4. **SDK Version**: If using the Coinbase SDK (Node/Python).
5. **Network**: `base-sepolia`, `ethereum`, etc.

