# Module 15: Guided Labs & Exercises

## Lab 1: Search for a "Needle" (Logs)
**Goal:** Practice Datadog Query Syntax.

### Step 1: Open Logs Explorer
(Use your company's Datadog or a sandbox).

### Step 2: Build Query
Find all error logs for the `cdp-api` service that happened on the `base-sepolia` network.
**Query:** `service:cdp-api status:error env:base-sepolia`

### Step 3: Refine
Find only those with "Rate Limit" in the message.
**Query:** `service:cdp-api status:error env:base-sepolia "rate limit"`

---

## Lab 2: Correlate a Trace (APM)
**Goal:** Go from a Log to a Trace.

### Step 1: Find a Log
Click on a log entry from Lab 1.

### Step 2: Trace Tab
Click the "Trace" tab or "View Trace" button.

### Step 3: Analyze Waterfall
Look at the flame graph.
- How long did the HTTP request take?
- Did the database call happen before or after the API call?
- **Observation:** This tells you if the *latency* was inside your app (DB) or outside (CDP).

