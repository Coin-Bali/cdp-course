# Module 3: Guided Labs & Exercises

## Lab 1: Build a Stake Operation
**Goal:** Create the unsigned transaction object for staking ETH.

### Step 1: Setup
Ensure `.env` has your `CDP_API_KEY_ID` and `CDP_API_KEY_SECRET`.
You also need a valid `STAKING_ADDRESS_ID` (a wallet ID from your CDP account) in `.env`.

### Step 2: Run the Script
```bash
python "Module 3 - Staking API/python/build_stake_operation.py"
```

### Step 3: Analysis
- Look at the JSON output.
- Identify the `unsigned_transaction` field.
- **Note:** This script only *builds* the operation. To execute it, you would need to sign this payload with your private key (which we don't do here for safety).

---

## Lab 2: Check Staking Rewards
**Goal:** Query historical rewards for a specific address.

### Step 1: Configure Env
Set `STAKING_REWARDS_PATH` in `.env`.
Example: `/platform/v1/stake/rewards/ethereum/<YOUR_WALLET_ADDRESS>`

### Step 2: Run the Script
```bash
python "Module 3 - Staking API/python/list_staking_rewards.py"
```

### Step 3: Observe
- If you have never staked, the list might be empty.
- If you have, you will see a list of reward payouts with timestamps and amounts.

