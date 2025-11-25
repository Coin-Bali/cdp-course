# Module 11: CDP Data & Oracle APIs + Node API

## 1. Product Overview
- **CDP Node API (RPC)**
  - Provides reliable, scalable **JSON-RPC** access to blockchain networks (Base Mainnet, Base Sepolia, Ethereum, etc.).
  - **Replaces**: Public endpoints (which have low rate limits) and other 3rd party providers.
  - **Standard Methods**: Supports standard EVM methods like `eth_getBlockByNumber`, `eth_call`, `eth_sendRawTransaction`.
- **SQL API**
  - Zero-infrastructure indexing solution.
  - Query real-time and historical onchain data (Base) using SQL.
  - **Use Case**: Analytics, user history, token transfers.
- **Spot Prices (Data API)**
  - Retrieve real-time spot prices, buy/sell prices, and exchange rates.
  - **Use Case**: Displaying fiat values in wallets.
- **Mesh Data API**
  - Standardized blockchain data access (Blocks, Transactions) across networks.

## 2. Technical Flow

### 2.1 CDP Node API (RPC)
- **Endpoint**: `https://api.developer.coinbase.com/rpc/v1/{network}/{API_KEY}`.
- **Auth**: The **Client API Key** is embedded in the URL for frontend/client-side use.
- **Rate Limits**: Free tier includes generous limits (e.g., 50 RPS on Base).

### 2.2 SQL API
- **Endpoint**: `POST /v2/data/query` (Executes SQL).
- **Auth**: CDP API Key (JWT).
- **Schema**: Base tables (blocks, transactions, logs, traces).

### 2.3 Spot Prices
- **Endpoint**: `GET /v2/prices/:currency_pair/spot` (Public).
- **Auth**: None required for public data, but rate limits apply.

## 3. Common Support Scenarios & Troubleshooting

### Node API
- **"429 Too Many Requests"**
  - **Cause**: Exceeded Rate Limit (RPS).
  - **Fix**: Implement backoff/retry logic; request limit increase if Enterprise.
- **"Invalid API Key"**
  - **Cause**: Typo in URL or key disabled.
  - **Fix**: Regenerate Client API Key in Portal -> Node.
- **"Method not supported"**
  - **Cause**: Using non-standard or debug methods not enabled on the tier.
  - **Fix**: Check supported methods list for Base Node.

### SQL API
- **"SQL Query Timeout"**
  - **Cause**: Query scans too many rows or is inefficient.
  - **Fix**: Add `WHERE` clauses (e.g., filter by `block_number` or `block_timestamp`), use `LIMIT`.
- **"Price data is stale"**
  - **Cause**: User checking `spot` (mid-market) vs `buy` (includes spread/fees).
  - **Fix**: Explain difference between Spot, Buy, and Sell prices. Use `CB-VERSION` header if format issues occur.

## 4. Escalation Guide
- **Collect Data**
  - Node RPC URL (mask key).
  - JSON-RPC Method & Params.
  - SQL Query String.
  - Request ID / Correlation ID.
- **Escalate When**
  - Node API returns 5xx errors consistently.
  - Latency spikes on specific methods (e.g., `eth_call` taking >5s).

## 5. Resources
- [CDP Node API Docs](https://docs.cdp.coinbase.com/node/welcome)
- [SQL API Documentation](https://docs.cdp.coinbase.com/data/sql-api/welcome)
- [Data API (Prices) Docs](https://docs.cdp.coinbase.com/coinbase-app/track-apis/prices)
