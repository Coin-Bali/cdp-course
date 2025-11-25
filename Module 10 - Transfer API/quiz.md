# Module 10: Knowledge Check

### Q1: What happens if you send a request with the same `Idempotency-Key` twice?
A) Two transactions are created.
B) The second request is ignored/returns the cached response of the first one.
C) An error `409 Conflict` is returned.

### Q2: Which HTTP status code indicates "2FA Token Required"?
A) 401 Unauthorized
B) 402 Payment Required
C) 403 Forbidden
D) 404 Not Found

### Q3: Can the Transfer API move fiat (USD) to a bank account?
A) Yes, if the destination is a linked bank account (via withdrawals).
B) No, only crypto.

### Q4: Is the Transfer API for "Onchain" or "Offchain" internal transfers?
A) Only Onchain.
B) Only Offchain (Coinbase to Coinbase).
C) Both. It can send to external crypto addresses (Onchain) and email addresses/Coinbase accounts (Offchain).

---
**Answers:**
1: B
2: B
3: A
4: C

