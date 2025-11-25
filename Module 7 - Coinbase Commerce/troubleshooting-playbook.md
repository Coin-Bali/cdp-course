# Module 7: Troubleshooting Playbook

## Common Issues & Solutions

### Problem: "Webhook signature verification failed"
**Diagnostic Steps:**
1. **Secret Key:** Are you using the correct `Shared Secret` from the Commerce/Business Settings? (Not the API Key!).
2. **Header:** Are you reading `X-Cc-Webhook-Signature`?
3. **Body:** Are you verifying the *raw* request body bytes? (JSON parsers often change whitespace, breaking the hash).

**Solution:**
- Ensure you use the raw body for HMAC calculation.
- Verify the secret key has no extra spaces.

### Problem: "Not receiving webhooks"
**Diagnostic Steps:**
1. **Endpoint Reachability:** Is your server public? (Localhost won't work without a tunnel like Ngrok).
2. **HTTPS:** Commerce/Business requires HTTPS (except sometimes for test modes, but HTTPS is standard).
3. **Firewall:** Is your server blocking Coinbase IP ranges?

**Solution:**
- Use a tool like `webhook.site` to test if Coinbase is sending events.
- Check server logs for connection attempts.

### Problem: "Overpayment / Underpayment"
**Diagnostic Steps:**
1. **Check Timeline:** Look at the Charge timeline in the dashboard.
2. **Underpayment:** User sent less than the required amount (plus network fees deduction).
3. **Overpayment:** User sent too much.

**Solution:**
- **Underpayment:** Ask user to send the remainder or refund the partial amount (manually or via API if supported).
- **Overpayment:** Resolve the charge (accept it) or refund the excess.

---

## Escalation Guide

### When to Escalate to T2
- **Settlement Delay:** Funds confirmed on blockchain > 24 hours ago but Status is still "Pending".
- **Webhook Outage:** No webhooks received for ANY charges for > 1 hour.

### Required Information for Escalation
1. **Charge Code / ID**: The unique 8-char code (e.g., `ABC123XY`).
2. **Transaction Hash**: Of the customer's payment.
3. **Webhook Endpoint**: The URL configured in settings.
4. **Business/Commerce Account ID**.

