# Module 6 Exercises: SIWC OAuth

1. **Drop-in Lab**: Run `python python/siwc_oauth_flow.py` and complete the authorization flow with scopes `wallet:user:read`, `wallet:accounts:read`, and `offline_access`. Capture the printed access & refresh tokens and confirm the `scope` string matches what you requested.
2. **Redirect URI Mismatch**: Temporarily change `COINBASE_REDIRECT_URI` in your `.env` to a URL not registered in the portal. Re-run the script and inspect the Coinbase error message. Add a note to your lab notes that explains why the redirect URIs must match exactly.
3. **Refresh Token Notes**: After refreshing once, re-run the helper and try to reuse the old refresh token (copy it somewhere before refreshing). Document what error Coinbase returns when a refresh token is used twice.
4. **2FA Simulation**: If your sandbox user requires 2FA, trigger a 402 response (`two_factor_required`). Use the `CB-2FA-TOKEN` header value that appears in the response to replay the request (you can edit the script or use curl). Note how quickly the token expires and what headers are required.
5. **Escalation Checklist**: For each run, log the `state`, `code_verifier`, and the `code` you received. When a `state` mismatch or invalid code occurs, reference these logs when filling out the SIWC escalation checklist in the README.
