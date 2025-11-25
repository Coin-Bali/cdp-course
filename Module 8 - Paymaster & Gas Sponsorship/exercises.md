# Module 8: Guided Labs & Exercises

## Lab 1: Check Paymaster Status
**Goal:** Verify your Paymaster RPC endpoint is active.

### Step 1: Setup
- Ensure `.env` has `PAYMASTER_RPC_URL`.
- It should look like: `https://api.developer.coinbase.com/rpc/v1/base-sepolia/<YOUR_API_KEY>`

### Step 2: Run the Check
```bash
python "Module 8 - Paymaster & Gas Sponsorship/python/check_paymaster.py"
```

### Step 3: Observe
- You should see a JSON-RPC response with the `chainId`.
- **Challenge:** Modify the script to call `pm_getPaymasterStubData` (requires constructing a dummy UserOp, which is advanced, but you can read the docs to see the params).

---

## Lab 2: Configure a Policy (Portal)
**Goal:** Set up a gas policy in the CDP Portal.

### Step 1: Log in to CDP
- Go to the **Paymaster** section.

### Step 2: Create Policy
- Set a **Global Limit** (e.g., $10).
- Set a **Per-User Limit** (e.g., 5 ops/day).

### Step 3: Allowlist (Optional)
- Add a specific contract address (e.g., a known USDC address on Sepolia) to test allowlisting.

