# Module 1: Troubleshooting Playbook

## Common Issues & Solutions

### Problem: "The Onramp widget is not loading / blank screen."
**Diagnostic Steps:**
1. **Check SDK Initialization:** Ensure `CoinbaseWalletSDK` is initialized correctly with the `appId`.
2. **Browser Console:** Look for CORS errors (Cross-Origin Resource Sharing).
3. **Domain Allowlist:**
   - Go to CDP Portal > Onramp > Settings.
   - Verify the domain hosting the widget is added (e.g., `localhost:3000` or `myapp.com`).
4. **Network Restrictions:** VPNs or firewalls might block Coinbase domains.

**Solution:**
- Add the domain to the allowlist.
- Ensure `https://` is used (except for localhost).
- Update to the latest version of the SDK.

### Problem: "Transaction is stuck in 'Pending' state."
**Diagnostic Steps:**
1. **Identify the Stage:**
   - **Fiat Stage:** Has the user's bank charged them?
   - **Crypto Stage:** Is the transaction hash generated?
2. **Check Webhooks:**
   - Did your server receive a `ONRAMP_TRANSACTION_SUCCESS` webhook?
   - Check the `transaction_status` endpoint.
3. **Block Explorer:** If a hash exists, check BaseScan/Etherscan.

**Solution:**
- If Fiat failed: User must contact their bank or retry with a different method.
- If Crypto pending: Explain block confirmation times (usually fast on Base, slower on Ethereum).

### Problem: "Asset or Country not supported error."
**Diagnostic Steps:**
1. **Check Eligibility:**
   - Is the user in a supported country? (e.g., Japan is not supported).
   - Is the asset supported in that region? (Some assets are restricted in NY/UK).
2. **Verify Config:**
   - Check the `destinationNetwork` and `purchaseCurrency` params passed to the session.

**Solution:**
- Use the `Onramp Config` API to fetch supported countries and assets dynamically.
- Direct user to use a different payment method or asset if restricted.

---

## Escalation Guide

### When to Escalate to T2
- **System Outage:** Multiple users reporting 500 errors or widget failure simultaneously.
- **Webhook Failure:** Webhooks are not being delivered despite 200 OK status on your endpoint.
- **Missing Funds:** Transaction confirmed onchain > 1 hour ago but not reflected in user balance (and not a sync issue).

### Required Information for Escalation
1. **App ID / Project ID**: `c631...`
2. **Session ID / Tracking ID**: Found in the URL or SDK logs.
3. **User Reference**: `partnerUserId` used during init.
4. **Transaction Hash**: If available.
5. **Time of Incident**: UTC timestamp.
6. **Browser/Device**: e.g., Chrome on iOS.

---

## FAQ / Scripts

**Q: Can I test without real money?**
A: Yes! Use the **Base Sepolia** testnet. You can simulate the flow, but actual fiat processing is mocked.

**Q: Why is the fee different than expected?**
A: Fees include Network Fees (Gas) + Coinbase Fee + Spread. These fluctuate with network congestion.

**Q: How do I handle chargebacks?**
A: Onramp guarantees settlement. Chargebacks are handled by Coinbase, not the developer (unless using specific partner flows).

