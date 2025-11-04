# Module 2: Advanced Trade API

## Learning Objectives
- Understand Advanced Trade REST endpoints and WebSocket feeds
- Authenticate correctly for REST and WebSocket connections
- Triage common trading issues (auth, scopes/permissions, pagination, balances)
- Apply WebSocket rate limits and subscription best practices
- Know what to collect and when to escalate

---

## 1. Product Overview

- Programmatic trading: place, list, and cancel orders via REST; stream real-time data via WebSockets.
- REST base: `https://api.coinbase.com/api/v3/brokerage/{resource}` (orders, fills, products, portfolios, fees).
- WebSocket endpoints:
  - Market Data: `wss://advanced-trade-ws.coinbase.com` (mostly unauthenticated market channels)
  - User Order Data: `wss://advanced-trade-ws-user.coinbase.com` (requires JWT; user channel, heartbeats)

References:
- Advanced Trade REST API overview
- WebSocket overview and setup
- WebSocket rate limits

---

## 2. Technical Flows

### 2.1 REST – Placing and Managing Orders (High-level)
1) Generate a JWT (Bearer) using your API key (server-side) and include it in `Authorization: Bearer <jwt>`
2) Create an order via brokerage v3 endpoint (e.g., market/limit)
3) Query order/fill status, list orders, cancel orders
4) Handle pagination (cursor-based) and 429 backoff

Key considerations:
- Ensure keys/scopes/permissions match trading actions
- Validate portfolio context and product pair
- Monitor balances (available vs. hold)

### 2.2 WebSockets – Real-time Data
- Market data: subscribe to channels like `level2`, `ticker`, `candles`, `market_trades`
- User data: connect to user endpoint with JWT to receive order updates/fills
- JWT details: short-lived (≈120s); include `iss=cdp`, `sub=<api key id>`, `nbf/exp`, `kid` header, `nonce`

Rate limits (per docs):
- 750 messages/second per IP, 8/second unauthenticated
- Implement backpressure, resubscription, and heartbeats

---

## 3. Common Support Scenarios & Troubleshooting

### "API keys are not working"
- Verify key type and permissions; confirm correct product (Advanced Trade)
- Check IP allowlisting and JWT construction (signature algorithm, claims, `uri` for REST)
- Include full request/response with headers and correlation IDs

### "Insufficient funds"
- Query balances; differentiate settled vs. available; check open holds
- Confirm correct portfolio/account and product denomination

### "Pagination confusion"
- Use documented cursor/limit scheme; maintain consistent sort; implement retry/backoff on 429

### "WebSocket auth or rate limits"
- Ensure JWT generation for user endpoint; refresh tokens before expiry
- Adhere to 750 msg/s per IP and 8/s unauthenticated; consolidate subscriptions

---

## 4. Triage Checklists

### Authentication
- [ ] Confirm API key id/secret validity and permissions
- [ ] Verify JWT claims/headers and clock skew
- [ ] Confirm correct REST host/path and WebSocket endpoint

### Orders & Balances
- [ ] Validate product pair and portfolio context
- [ ] Check available vs. hold balances
- [ ] Retrieve recent order/fill history

### Rate Limits & Pagination
- [ ] Identify 429s; implement exponential backoff
- [ ] Use cursors consistently; avoid redundant polling

### WebSocket
- [ ] Use the right endpoint (market vs. user)
- [ ] Respect message limits; batch subscriptions
- [ ] Reconnect with jitter; resubscribe on connect

---

## 5. Escalation Guide

Collect before escalating:
- API key prefix (not full secret), portfolio ID, product pair
- Full REST request/response (headers), correlation IDs, approximate timestamps
- For WebSockets: endpoint used, channels, JWT issuance time, sample messages

When to escalate:
- Consistent authentication failures with valid tokens and correct endpoints
- Order status discrepancies vs. docs or widespread subscription issues
- WebSocket service instability across multiple developers

---

## 6. References
- Advanced Trade REST API introduction
- Advanced Trade REST endpoints (`/api/v3/brokerage/...`)
- WebSocket overview and setup
- WebSocket rate limits and channels

---

## 7. Python Samples (Quick Start)

See `python/` folder:
- `advanced_trade_jwt.py` – generate JWT for REST calls (host `api.coinbase.com`)
- `list_products.py` – GET `/api/v3/brokerage/products` with Bearer JWT
- `ws_market_data.py` – subscribe to `ticker` on `wss://advanced-trade-ws.coinbase.com`

Environment hints:
- Export a JWT for REST:
  - `export JWT=$(python python/advanced_trade_jwt.py)`
- Or provide `ADV_API_KEY_ID`/`ADV_API_KEY_SECRET` to sign WebSocket messages when needed

