# Module 13: Guided Labs & Exercises

## Lab 1: Check Testnet Balance
**Goal:** Verify your balance on Base Sepolia.

### Step 1: Setup
- Ensure `BASE_SEPOLIA_ADDRESS` is set in `.env`.

### Step 2: Run Script
```bash
python "Module 13 - Faucets & Testnet Tools/python/check_base_balance.py"
```

### Step 3: Observe
- It prints the balance in ETH.
- **Action:** Go to a faucet, request funds, wait 10 seconds, and run the script again. You should see the balance increase.

---

## Lab 2: Explore the Explorer
**Goal:** Navigate BaseScan.

### Step 1: Go to Explorer
Visit [sepolia.basescan.org](https://sepolia.basescan.org).

### Step 2: Search
Paste your `BASE_SEPOLIA_ADDRESS`.

### Step 3: Verify
Find the transaction from the Faucet. Note the `From` address (the Faucet's wallet).

