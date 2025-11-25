# Module 10: Guided Labs & Exercises

## Lab 1: Send Money (Simulation)
**Goal:** Attempt to send crypto (or check 2FA requirement).

### Step 1: Setup
- Ensure `.env` has `CDP_API_KEY_ID` and `CDP_API_KEY_SECRET`.
- **Warning:** This script uses *Real Money* if you have a funded Coinbase account and valid API keys. Use small amounts or just observe the 2FA behavior.

### Step 2: Run the Script
```bash
python "Module 10 - Transfer API/python/send_money_v2.py"
```

### Step 3: Observe
- If you don't have the 2FA header set, you will likely get a `402` error.
- **This is a success for the lab!** It confirms you are hitting the endpoint and security is enforcing 2FA.

---

## Lab 2: Check Account Balance (via Transfer API)
**Goal:** Read the balance of your primary account.

### Step 1: Modify Script (Challenge)
- Create a new script or modify existing to call `GET /v2/accounts`.
- Use the same JWT generation logic.

### Step 2: Run
- Verify you can see your account list.

