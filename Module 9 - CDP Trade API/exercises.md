# Module 9: Guided Labs & Exercises

## Lab 1: Get a Swap Quote
**Goal:** Fetch a real-time quote for swapping ETH to USDC on Base.

### Step 1: Setup
- Ensure `.env` has `CDP_API_KEY_ID` and `CDP_API_KEY_SECRET`.
- Ensure `SWAP_FROM_TOKEN_ADDRESS` (WETH) and `SWAP_TO_TOKEN_ADDRESS` (USDC) are set for Base.

### Step 2: Run the Script
```bash
python "Module 9 - CDP Trade API/python/get_swap_quote.py"
```

### Step 3: Analyze
- Check the `price` and `toAmount`.
- Look for `liquidityAvailable: true`.
- **Challenge:** Change the amount to something huge (e.g., 1,000,000 ETH) and see if liquidity fails.

---

## Lab 2: Slippage Experiment
**Goal:** Understand how slippage inputs affect the quote.

### Step 1: Modify Script
- Open `get_swap_quote.py`.
- Change `slippageBps` to `0` (0%).

### Step 2: Run
- Run the script.
- **Observe:** It might still work for a quote, but executing this onchain would likely fail instantly due to *any* price movement.
- **Action:** Change it back to `50` (0.5%) or `100` (1%).

