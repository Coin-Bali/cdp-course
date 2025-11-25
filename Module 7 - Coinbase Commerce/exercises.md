# Module 7: Guided Labs & Exercises

## Lab 1: Verify a Webhook
**Goal:** Write/Run code to verify a Commerce webhook signature.

### Step 1: Setup
- Ensure `.env` has `COMMERCE_WEBHOOK_SECRET`.
- If you don't have a real one, generate a random string for testing: `openssl rand -hex 32`.

### Step 2: Run the Verifier
```bash
python "Module 7 - Coinbase Commerce/python/verify_webhook.py"
```

### Step 3: Send a Test Payload
In a separate terminal:
```bash
# You need to calculate the signature first for this to pass!
# Or, simpler: Just run the script and observe that it listens.
# To truly test "Success", you'd need a script to GENERATE the signature too.
```
*Self-Correction:* Since we only provided the *Verification* script, the lab is to run it and understand the code structure. If you want to simulate a *valid* request, you'd need a generator.
**Challenge:** Write a small python script to generating a signature using your secret and a dummy payload, then send it to localhost:5000.

---

## Lab 2: List Business Accounts
**Goal:** Fetch balances/accounts using the Business API (formerly Prime/Exchange/Commerce convergence).

### Step 1: Setup
Ensure `BUSINESS_API_KEY_ID` and `BUSINESS_API_KEY_SECRET` are set in `.env`.

### Step 2: Run
```bash
python "Module 7 - Coinbase Commerce/python/business_accounts.py"
```

### Step 3: Observe
- View the list of accounts (Wallets) and their balances.
