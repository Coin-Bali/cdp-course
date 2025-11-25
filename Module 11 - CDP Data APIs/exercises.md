# Module 11: Guided Labs & Exercises

## Lab 1: Query the Node API
**Goal:** Fetch the latest block from Base Mainnet using the Node RPC.

### Step 1: Setup
- Ensure `CDP_NODE_RPC_URL` is set in `.env`.
- It should look like: `https://api.developer.coinbase.com/rpc/v1/base/<YOUR_KEY>`

### Step 2: Run the Script
```bash
python "Module 11 - CDP Data APIs/python/node_rpc_block.py"
```

### Step 3: Observe
- See the Block Number, Hash, and Transaction Count.
- **Challenge:** Modify the script to get the balance of a specific address using `eth_getBalance`.

---

## Lab 2: Run a SQL Query (Challenge)
**Goal:** Use the SQL API to find high-value transactions.

### Step 1: Setup
- Ensure `CDP_API_KEY_ID` and `CDP_API_KEY_SECRET` are set.

### Step 2: Run the Query
```bash
python "Module 11 - CDP Data APIs/python/query_sql.py"
```

### Step 3: Analyze
- The script runs a query for blocks > 1,000,000.
- Look at the JSON output.
- **Experiment:** Change the SQL query in the python file to select `from_address` from `base.transactions`.

