# Module 2: Guided Labs & Exercises

## Lab 1: Fetch Market Data (REST)
**Goal:** Retrieve the list of tradable pairs and their status.

### Step 1: Setup
Ensure `.env` has your `CDP_API_KEY_ID` and `CDP_API_KEY_SECRET`.

### Step 2: Run the Script
```bash
python "Module 2 - Advanced Trade API/python/list_products.py"
```

### Step 3: Analysis
- Look at the output.
- Find `BTC-USD`.
- Note the `status` (should be `online`).
- **Challenge:** Modify the script to print only products where `quote_currency_id` is "USDC".

---

## Lab 2: Listen to Real-Time Ticks (WebSocket)
**Goal:** Stream live price updates for BTC-USD.

### Step 1: Run the Script
```bash
python "Module 2 - Advanced Trade API/python/ws_market_data.py"
```

### Step 2: Observe
- You should see a flood of JSON messages (`ticker` channel).
- **Note:** This script uses the public WebSocket, so no API Key is strictly required for *market data*.

### Step 3: Disconnect
- The script is set to run for 10 seconds and then close.
- **Challenge:** Change the subscription to `ETH-USD`.

---

## Lab 3: Check Authentication (JWT)
**Goal:** Verify your API Keys are working for signed requests.

### Step 1: Run the JWT Generator
```bash
python "Module 2 - Advanced Trade API/python/advanced_trade_jwt.py"
```

### Step 2: Verify
- If it prints a long string starting with `ey...`, your keys are valid and the signing logic is correct.
- If it errors, check your `.env` file format.

