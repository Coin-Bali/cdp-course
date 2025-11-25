# Module 4: Guided Labs & Exercises

## Lab 1: Create a Server Wallet (EVM)
**Goal:** Programmatically generate a new Ethereum-compatible wallet.

### Step 1: Setup
Ensure `CDP_API_KEY_ID` and `CDP_API_KEY_SECRET` are set.
**Note:** Creating a wallet is a read/write action but doesn't strictly require the *Wallet Secret* for simple creation in some versions, but *signing* definitely does. The provided script uses standard Auth.

### Step 2: Run the Script
```bash
python "Module 4 - Server Wallet/python/create_evm_account.py"
```

### Step 3: Output
- Save the `address` (e.g., `0x...`) from the JSON output.
- You will need this for the next lab.

---

## Lab 2: Fund the Wallet (Testnet)
**Goal:** Get ETH into your new server wallet so it can transact.

### Step 1: Get Address
Copy the address from Lab 1.

### Step 2: Use Faucet
- Go to [Coinbase Faucet](https://portal.cdp.coinbase.com/products/faucet) or a public Base Sepolia faucet.
- Paste the address.
- Request Base Sepolia ETH.

### Step 3: Verify
- Check the address on [Base Sepolia Blockscout](https://sepolia.basescan.org/).

---

## Lab 3: Send a Transaction
**Goal:** Move funds from your Server Wallet to another address.

### Step 1: Configure Env
- `CDP_WALLET_SECRET`: **Required** for this step! (The private key part of your API Key set specifically for wallets).
- `EVM_SOURCE_ADDRESS`: The address from Lab 1.
- `EVM_DESTINATION_ADDRESS`: Any other 0x address (e.g., your personal Metamask).

### Step 2: Run the Script
```bash
python "Module 4 - Server Wallet/python/send_evm_transaction.py"
```

### Step 3: Analyze
- If successful, it prints a `transactionHash`.
- Look up this hash on the explorer.

