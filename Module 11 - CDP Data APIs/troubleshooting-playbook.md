# Module 11: Troubleshooting Playbook

## Common Issues & Solutions

### Problem: "Node API 429 Too Many Requests"
**Diagnostic Steps:**
1. **Rate Limit:** The free tier allows ~50 requests/second. Are you bursting above this?
2. **Efficiency:** Are you polling `eth_blockNumber` in a tight loop?
3. **Key Usage:** Is the Client API Key being used by thousands of users simultaneously?

**Solution:**
- Implement caching for data that doesn't change often (e.g., chainId).
- Use WebSockets (`wss://`) for real-time events instead of polling HTTP.
- Upgrade to a paid plan if volume is consistently high.

### Problem: "SQL Query Timeout"
**Diagnostic Steps:**
1. **Complexity:** Are you doing a `SELECT *` on the entire `transactions` table?
2. **Filters:** Are you missing `WHERE` clauses on indexed columns (like `block_number` or `block_timestamp`)?

**Solution:**
- Always adding a time range or block range filter: `WHERE block_number > 1000000`.
- Use `LIMIT` to test queries.

### Problem: "Price data is stale"
**Diagnostic Steps:**
1. **Endpoint:** Are you using the `spot` endpoint? This is a mid-market price and updates frequently but might lag CEX order books slightly.
2. **Asset:** Is it a low-liquidity asset?

**Solution:**
- For precise execution prices, use the Trade API quote.
- For display purposes, the Spot Price API is sufficient.

---

## Escalation Guide

### When to Escalate to T2
- **Node Outage:** `5xx` errors on `eth_chainId` or basic methods for >10 minutes.
- **Data Gap:** SQL API missing blocks that are confirmed onchain > 1 hour ago.

### Required Information for Escalation
1. **RPC URL**: (Mask the key).
2. **Method**: e.g., `eth_call`.
3. **SQL Query**: The exact query string failing.
4. **Time**: UTC.

