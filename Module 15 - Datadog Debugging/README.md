# Module 15: Datadog Debugging Playbook for Support Engineers

## 1. Overview
This module guides Support Engineers on how to use Datadog to investigate customer issues with Coinbase Developer Platform (CDP) APIs. It focuses on **querying**, **analyzing**, and **correlating** existing logs and metrics rather than instrumenting code.

## 2. Key Data Concepts for CDP

### 2.1 Important Tags & Facets
When filtering data in Datadog (Logs or APM), these are your primary search keys:

| Field/Tag | Description | Example |
|-----------|-------------|---------|
| `service` | Identifies the specific CDP service | `cdp-api`, `waas-backend`, `paymaster-service` |
| `env` | Environment | `production`, `base-sepolia` |
| `http.status_code` | Response status | `429`, `500`, `402` |
| `cdp.correlation_id` | Unique ID for a specific request | `93a5-4b21-8832-1234` |
| `cdp.project_id` | Customer's Project ID | `c631...` |
| `cdp.method` | HTTP Method | `POST`, `GET` |

## 3. Investigation Workflows

### Workflow A: Investigating a Specific Failure (The "Needle in a Haystack")
**Scenario**: A customer reports "My API call failed at 10:05 AM" or provides a `correlation_id`.

1. **Navigate to Logs > Search**.
2. **Time Range**: Set to +/- 15 minutes of the reported time.
3. **Search Query**:
   - If you have an ID: `cdp.correlation_id:<THE_ID>`
   - If generic: `service:cdp-api status:error @cdp.project_id:<PROJECT_ID>`
4. **Analyze the Log JSON**:
   - Expand the log entry.
   - Look at `error.message` or `error.stack` for the root cause (e.g., "Invalid signature", "Insufficient funds").
   - **Tip**: Check the `duration` field. Was it a timeout (>30s)?

### Workflow B: Diagnosing "Is it just me or is CDP down?" (The "Haystack" View)
**Scenario**: Multiple customers report issues, or a customer claims "CDP is broken".

1. **Navigate to Dashboards > CDP System Health** (Hypothetical shared dashboard).
2. **Check Error Rates**:
   - Look for spikes in `5xx` errors across `service:cdp-api`.
   - A global spike indicates a system outage.
   - A flat line suggests a customer-specific configuration issue.
3. **Check Latency (p95, p99)**:
   - Is latency elevated for specific endpoints (e.g., `POST /v2/evm/transactions`)?

### Workflow C: Troubleshooting Rate Limits
**Scenario**: Customer claims they are getting 429s but "shouldn't be".

1. **Navigate to Logs > Analytics (or Patterns)**.
2. **Query**: `service:cdp-api http.status_code:429 @cdp.project_id:<PROJECT_ID>`.
3. **Visualizations**:
   - **Timeseries**: Is it a burst (vertical spike) or sustained traffic?
   - **Top List**: Group by `@http.url_details.path`. Are they spamming a specific endpoint (e.g., `eth_getBalance`)?
4. **Resolution**:
   - If **Burst**: Advise implementing exponential backoff.
   - If **Sustained**: Check their tier limits.

### Workflow D: Tracing "Stuck" Transactions (APM)
**Scenario**: Customer says "I sent the request, got a 200 OK, but nothing happened onchain."

1. **Navigate to APM > Traces**.
2. **Filter**: `service:cdp-api resource:/v2/evm/transactions`.
3. **Find the Trace**: Filter by the customer's `project_id` or time.
4. **Inspect the Flame Graph**:
   - **Span 1 (API Ingress)**: 200 OK.
   - **Child Span (Database/Queue)**: Did it fail to write to the mempool?
   - **Child Span (Blockchain Node)**: Did the node reject it (e.g., "nonce too low")?
   - **Finding**: Often the API accepts the request (200) but fails asynchronously. Logs correlated to this trace will reveal the async failure.

## 4. Cheat Sheet: Common Search Queries

| Goal | Datadog Query |
|------|---------------|
| **Find specific error** | `service:cdp* status:error "wallet failed"` |
| **Check customer 429s** | `status:error http.status_code:429 @project_id:xyz` |
| **Slow requests (>5s)** | `service:cdp-api duration:>5s` |
| **Webhook Failures** | `service:webhooks status:error @event_type:charge:confirmed` |

## 5. Escalation Template (for T2)
When escalating to Engineering/T2 based on Datadog findings, attach:

- **Link to Log/Trace**: (Use the "Share" -> "Copy Link" button in Datadog)
- **Correlation ID**: `...`
- **Observation**: "I see a spike in 500s on `POST /transfers` starting at 14:00 UTC."
- **Impact**: "Affecting all users" vs "Single project <ID>".
