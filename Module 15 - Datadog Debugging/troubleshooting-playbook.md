# Module 15: Troubleshooting Playbook

## Common Issues & Solutions

### Problem: "I can't find my logs in Datadog"
**Diagnostic Steps:**
1. **Service Name:** Are you filtering by `service:cdp-integration` (or whatever you named it)?
2. **Time Window:** Is the time picker set to "Past 15 minutes" or "Live"?
3. **Sampling:** Is Datadog sampling your logs (dropping 90%)? Check your `DD_LOGS_CONFIG_CONTAINER_COLLECT_ALL`.

**Solution:**
- Broaden the search (remove filters).
- Check the agent status on the server.

### Problem: "Correlation ID is missing"
**Diagnostic Steps:**
1. **Header:** Did the API response actually contain `X-Request-Id`? (CDP almost always sends it).
2. **Logging Logic:** Did your code extract it and put it in the log JSON?

**Solution:**
- Update your logging middleware to strictly capture `response.headers.get('x-request-id')`.

### Problem: "High Error Rate Alert is flapping"
**Diagnostic Steps:**
1. **Threshold:** Is the alert set to "Above 1%"?
2. **Traffic:** Do you have low traffic? (1 error in 10 requests = 10% error rate).

**Solution:**
- Use a "Count" threshold (e.g., "> 50 errors") instead of "Rate" for low-traffic services.

---

## Escalation Guide

### When to Escalate to T2
- **Evidence:** You have found a cluster of `500 Internal Server Error` logs from CDP with distinct `correlation_id`s.
- **Pattern:** The errors started happening after a specific time (e.g., deployment or outage).

### Required Information for Escalation
1. **Dashboard Snapshot**: Link to the Datadog graph showing the spike.
2. **Sample Logs**: Export a CSV of 5-10 error logs.
3. **Analysis**: "We see a 15% failure rate on `POST /transfers` starting at 10:00 UTC."

