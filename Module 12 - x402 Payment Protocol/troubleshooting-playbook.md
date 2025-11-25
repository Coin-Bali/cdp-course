# Module 12: Troubleshooting Playbook

## Common Issues & Solutions

### Problem: "Client gets 402 Payment Required"
**Diagnostic Steps:**
1. **This is normal!** Check if the client handles it.
2. **Header:** Does the response include `WWW-Authenticate: x402 ...`?
3. **Details:** Can the client parse the `address`, `amount`, and `asset` from the header?

**Solution:**
- Ensure the client is programmed to catch 402, parse the header, make a payment, and retry.

### Problem: "Payment sent but resource not unlocked"
**Diagnostic Steps:**
1. **Proof:** Did the client send the `X-Payment-Response` header with the transaction hash?
2. **Verification:** Did the server call the Facilitator API to verify the hash?
3. **Confirmation:** Is the transaction confirmed onchain?

**Solution:**
- Check the server logs to see if the Facilitator verification failed.
- Ensure the client sent the *exact* amount required (wei precision).

### Problem: "Facilitator returns 'Invalid Payment'"
**Diagnostic Steps:**
1. **Replay:** Is the client trying to use the same transaction hash for a second request? (Payments are usually one-time use).
2. **Mismatch:** Did the user pay the wrong address or on the wrong network?

**Solution:**
- Use a fresh transaction for every request (unless the service sells "access tokens" or "time", but x402 basic flow is per-resource).

---

## Escalation Guide

### When to Escalate to T2
- **Facilitator Down:** The verify endpoint returns 500s.
- **False Negative:** A valid, confirmed transaction is permanently rejected by the verify endpoint.

### Required Information for Escalation
1. **Transaction Hash**: 0x...
2. **Network**: Base/Base Sepolia.
3. **Facilitator Request ID**.
4. **Seller Address**.

