# Module 7 Exercises: Commerce → Business

1. **Webhook Veriﬁcation Lab**
   - Copy `samples/charge_webhook.json` to a temporary file and compute the HMAC SHA256 signature with your `COMMERCE_SHARED_SECRET` (or use the signature from a real webhook). Run `python python/verify_webhook.py --payload samples/charge_webhook.json --signature '<your_signature>'` and note whether it matches.
   - If the script reports a mismatch, double-check that the payload was not pretty-printed and that you copied the raw bytes Coinbase sent.

2. **Charge Lifecycle Playbook**
   - Use the Commerce API (script above or CLI) to create a charge. Let it expire (or simulate by editing the charge timeline). Document the sequence of timeline statuses (`NEW`, `PENDING`, `CONFIRMED`, `EXPIRED`) and which webhooks you expect at each stage.

3. **Business Accounts Check**
   - Run `python python/business_accounts.py` to confirm your Business access token and `CB-VERSION`. Capture at least one account ID and currency/type pair that you can provide when a ticket mentions “missing settlement”.
   - Note the CB-VERSION date printed in your environment and what happens if you remove the header from the request (you should see a warning or failure).

4. **Migration Thought Experiment**
   - Given a Commerce merchant using `charge:confirmed` webhooks to deposit USD funds, map their workflow to Business APIs (accounts/payouts). Document what data (charge code, timeline with `event.data.id`, webhook timestamp) should move into the Business request/response flow.
   - Keep these notes handy for when T1 needs to escalate a Commerce -> Business migration case.
