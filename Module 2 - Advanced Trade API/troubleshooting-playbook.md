# Module 2: Troubleshooting Playbook

## Common Issues & Solutions

### Problem: "401 Unauthorized Error"
**Diagnostic Steps:**
1. **Check Key Type:** Are you using a CDP API Key (starts with `organizations/...`) or a Legacy Key? The scripts in this course use CDP Keys (v2).
2. **Verify Secret:** Ensure the private key (PEM) in `.env` handles newlines correctly (`\n`).
3. **System Time:** Ensure your server clock is synced. JWTs have a strict timestamp validity.

**Solution:**
- Re-copy the API Key Secret from the portal.
- Ensure you are not mixing Legacy API Key logic (HMAC) with CDP API Key logic (JWT).

### Problem: "403 Forbidden - Invalid Scope"
**Diagnostic Steps:**
1. **Check Permissions:** Does the API Key have `View` and `Trade` permissions enabled in the portal?
2. **Check Endpoint:** Some endpoints (like specific portfolio data) might require `Transfer` permissions if they involve movement.

**Solution:**
- Go to CDP Portal > Settings > API Keys.
- Edit the key permissions to include the required scope.

### Problem: "WebSocket connection closes immediately (Code 1000/1006)."
**Diagnostic Steps:**
1. **Auth vs Public:** Are you connecting to `advanced-trade-ws-user.coinbase.com` (Auth) or `advanced-trade-ws.coinbase.com` (Public)?
2. **Heartbeats:** Are you handling Pings/Pongs? (The provided script does simple listening, but production apps need heartbeat logic).
3. **JWT Validity:** WebSocket JWTs expire. You must disconnect and reconnect with a new token before expiry, or handle re-auth.

**Solution:**
- For public market data, use the Public URL (no auth required).
- For user orders, ensure the JWT is signed correctly and the channel name is `user`.

### Problem: "Rate Limit Exceeded (429)"
**Diagnostic Steps:**
1. **Check Usage:** Are you polling `GET /products` every second?
2. **Burst Limit:** Advanced Trade allows bursts but has a strict hourly/second limit.

**Solution:**
- Use WebSockets for updates instead of polling REST APIs.
- Implement `time.sleep()` (exponential backoff) in your scripts.

---

## Escalation Guide

### When to Escalate to T2
- **Matching Engine Error:** Orders are stuck in "Open" state despite being filled onchain/UI (rare synchronization issue).
- **Incorrect Balance:** API reports different balance than the UI (potential ledger delay).
- **5xx Errors:** Persistent Internal Server Errors on standard endpoints (e.g., `List Products`).

### Required Information for Escalation
1. **API Key ID:** (Do NOT share the secret).
2. **Order ID**: The UUID of the order failing.
3. **Product ID**: e.g., `BTC-USD`.
4. **Request Timestamp**: UTC.
5. **Full Error Response**: JSON body.

