# Module 11: Knowledge Check

### Q1: What is the primary advantage of the SQL API over standard JSON-RPC?
A) It is faster for single-block lookups.
B) It allows complex filtering and aggregation (e.g., "Show all transactions by user X in the last month") without scraping the chain.
C) It costs more gas.

### Q2: If you receive a `429` error from the Node API, what should you do?
A) Retry immediately.
B) Implement a backoff strategy (wait and retry).
C) Switch to Bitcoin.

### Q3: Which method is best for listening to real-time events (like new blocks)?
A) Polling `eth_getBlockByNumber` every second via HTTP.
B) Using a WebSocket subscription (`eth_subscribe`).
C) Sending an email.

### Q4: The `Spot Price` API returns what kind of price?
A) The exact price you will get if you buy now.
B) The mid-market price (average of buy and sell), useful for display but not execution.
C) The price from 24 hours ago.

---
**Answers:**
1: B
2: B
3: B
4: B

