# Module 12: Guided Labs & Exercises

## Lab 1: Simulate x402 Flow (Client & Server)
**Goal:** Run a local Seller and Buyer to see the 402 handshake in action.

### Step 1: Start the Seller
Open a terminal:
```bash
python "Module 12 - x402 Payment Protocol/python/x402_seller_server.py"
```
*Keep this terminal open.*

### Step 2: Run the Buyer
Open a **new** terminal:
```bash
python "Module 12 - x402 Payment Protocol/python/x402_buyer_client.py"
```

### Step 3: Observe the Handshake
1. **Buyer** requests resource -> **Seller** returns 402.
2. **Buyer** parses header (sees 1 USDC required).
3. **Buyer** "simulates" payment (generates mock hash).
4. **Buyer** retries with header.
5. **Seller** verifies and returns 200 OK.

**Challenge:** Modify the Seller code to require `10 USDC` and see if the Buyer logic adapts (it parses the header, so it should!).

