# Module 10: Troubleshooting Playbook

## Common Issues & Solutions

### Problem: "402 Two Factor Required"
**Diagnostic Steps:**
1. **Scope:** Are you using `wallet:transactions:send`? This sensitive scope triggers 2FA.
2. **User Settings:** Does the user have 2FA enabled on their Coinbase account?

**Solution:**
- Catch the 402 error.
- Prompt the user for their 2FA code (SMS/Authy).
- Retry the request with the `CB-2FA-TOKEN` header.

### Problem: "Transaction Pending (Manual Review)"
**Diagnostic Steps:**
1. **Status:** Check the API response `status`. Is it `pending` or `waiting_for_clearing`?
2. **Compliance:** Large transfers might trigger internal compliance reviews.

**Solution:**
- Wait. Do not resend.
- Check `resource_path` for updates.

### Problem: "Idempotency Error"
**Diagnostic Steps:**
1. **Key Reuse:** Are you sending the same `idem` field for a *new* transaction?
2. **Payload:** Did you change the amount but keep the same idempotency key?

**Solution:**
- Generate a unique idempotency key (UUID) for every *new* logical transaction.
- Reuse the key only when retrying the *exact same* transaction (e.g., after a timeout).

---

## Escalation Guide

### When to Escalate to T2
- **Stuck Funds:** Money left the account but did not arrive onchain after >24 hours.
- **Double Spend:** Using Idempotency failed and two transactions were created (Rare/Critical).

### Required Information for Escalation
1. **Account ID**: `primary` or UUID.
2. **Transaction ID**: The internal Coinbase ID (not just the hash).
3. **Idempotency Key Used**.
4. **Time**: UTC.

