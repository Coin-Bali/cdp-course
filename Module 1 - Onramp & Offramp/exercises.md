# Module 1: Guided Labs & Exercises

## Lab 1: Create an Onramp Session
**Goal:** Generate a functional URL that allows a user to buy crypto.

### Prerequisites
- Python installed
- `requirements.txt` installed (`pip install -r requirements.txt`)
- `.env` file configured with `CDP_API_KEY_ID`, `CDP_API_KEY_SECRET`, and `CDP_APP_ID`.

### Step 1: Configure the Environment
1. Open `.env`.
2. Ensure `DESTINATION_ADDRESS` is set to your wallet address (e.g., Metamask).
3. Set `DESTINATION_NETWORK` to `base-sepolia` (for testing) or `base` (for mainnet).

### Step 2: Run the Script
Run the session creation script:
```bash
python "Module 1 - Onramp & Offramp/python/create_onramp_session.py"
```

### Step 3: Test the URL
1. Copy the `onrampUrl` from the console output.
2. Paste it into a browser.
3. **Observe:**
   - Does it ask for a Coinbase login? (It should).
   - Does it pre-fill the asset (ETH/USDC) and network?
   - Attempt to proceed (if on Testnet, no real funds needed).

---

## Lab 2: Webhook Verification (Manual Simulation)
**Goal:** Understand how to securely verify a webhook signature.

### Step 1: Start the Verifier
Run the webhook verifier script:
```bash
python "Module 1 - Onramp & Offramp/python/webhook_verifier.py"
```

### Step 2: Simulate a Request
In a new terminal, send a fake webhook (this will fail verification because we can't easily spoof the signature without the secret key code, but observe the log):
```bash
curl -X POST http://localhost:5000/webhook \
  -H "Content-Type: application/json" \
  -d '{"event_type": "transaction_success"}'
```

### Step 3: Analyze Logs
Check the python terminal. It should say **"Invalid Signature"**. This confirms the security logic is working!

