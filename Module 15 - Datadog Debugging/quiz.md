# Module 15: Knowledge Check

### Q1: What is a `correlation_id`?
A) A unique string (UUID) that links a client's request to the server's internal logs.
B) A password.
C) A timestamp.

### Q2: You see a 500 error in your logs. Who is likely at fault?
A) The user (Bad input).
B) The server (CDP or your backend) crashed or had an unhandled exception.
C) The network provider.

### Q3: Which Datadog tool helps you visualize the "Time taken" for each step of a request?
A) Log Explorer
B) APM (Application Performance Monitoring) / Traces
C) Metrics

### Q4: If you are hitting Rate Limits (`429`), what metric should you alert on?
A) `system.cpu.usage`
B) `cdp.rate_limit.hit` (or count of `status:429` logs)
C) `wallet.balance`

---
**Answers:**
1: A
2: B
3: B
4: B

