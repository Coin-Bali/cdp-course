# Module 6: Sign in with Coinbase (SIWC)

## Learning Objectives
- Explain Coinbase OAuth2 scopes, grant types, redirect URIs, and PKCE requirements
- Walk through the SIWC authorization, token exchange, refresh, and 2FA flows
- Troubleshoot invalid redirect URIs, missing scopes, and token errors from the SIWC playground
- Capture the diagnostics teams need when handing SIWC escalations to T2

---

## 1. Product Overview
- SIWC exposes Coinbase identities and wallet data through OAuth2; it shares the same security posture as Coinbase App/Biz.
- Request granular scopes in the authorization URL (e.g., `wallet:accounts:read`, `wallet:user:read`, `offline_access`).
- `offline_access` allows issuance of refresh tokens (valid 1.5 years and single-use during refresh flow).
- Use `state` (>=8 characters) and PKCE (`S256` recommended) for CSRF protection and improved security.
- Redirect URI must exactly match the value registered in the CDP portal; mismatches yield the “invalid redirect URI” error.

References:
- OAuth2 reference (authorize + token endpoints)
- Access & refresh token docs (expiration, single-use refresh, 402 two-factor)
- Scopes list (permission matrix for wallet endpoints)

---

## 2. Authentication & SIWC Flow
1. Construct authorization URL to `https://login.coinbase.com/oauth2/auth`:
   - Required params: `response_type=code`, `client_id`, `redirect_uri`, `scope`.
   - Optional but recommended: `state`, `code_challenge` (PKCE), `code_challenge_method=S256`.
2. User authenticates on Coinbase and the `code` + `state` are posted to the registered redirect URI.
3. Exchange the code at `https://login.coinbase.com/oauth2/token`:
   - Use `grant_type=authorization_code`, include `code_verifier` if PKCE used.
   - Keep `client_secret`/`code_verifier` off the browser (server-side only).
4. Store access token (~1 hour) and refresh token (1.5 years, single refresh per token).
5. Refresh via `grant_type=refresh_token`; do not resend `code`/`redirect_uri`.

### Optional: PKCE, 2FA, Refresh
- PKCE: Generate a random verifier, SHA256 hash for challenge, include in `/auth`, reuse verifier when exchanging code.
- 2FA-enabled users trigger a 402 with `two_factor_required`; re-submit the identical request with `CB-2FA-TOKEN`.
- Refresh responses provide new access/refresh pair; old refresh token becomes invalid immediately after use.

### Sample Flow Reference Snippet
```go
// Build auth URL with PKCE and state
params.Add("response_type", "code")
params.Add("client_id", clientID)
params.Add("redirect_uri", redirectURI)
params.Add("scope", "wallet:user:read,wallet:accounts:read,offline_access")
params.Add("state", state)
params.Add("code_challenge", codeChallenge)
params.Add("code_challenge_method", "S256")
```

---

## 3. Common Support Scenarios & Troubleshooting
### “Redirect URI is invalid.”
- Confirm domain/port/case exactly matches the portal entry.
- Check whether using http vs https; OAuth redirect is case-sensitive and must be URL-encoded.
- Re-save the redirect URI in the portal to refresh the project cache.
### “I’m not getting the wallet scopes I requested.”
- Use GET `/user/auth` to see granted scopes vs requested ones.
- Make sure the user granted consent; unauthorized/truncated scopes show up as empty or omitted.
- Certain scopes (e.g., `wallet:transactions:send`) may trigger additional security (2FA) requirements.
### “Access token expired / 401 responses.”
- Access tokens live for ~1 hour; use the refresh token or re-auth.
- Refresh token expires after 1.5 years and is single-use; log refresh errors and prompt user to re-auth if refresh fails.
- Check for time drift between servers and Coinbase; >60 seconds drift can invalidate tokens.

---

## 4. Escalation Guide
### Collect before escalating
- `client_id`/`projectId`, environment (production vs sandbox), and redirect URI.
- Authorization request (URL with query params) and token exchange payload (exclude secrets).
- Scope set, `state` value, PKCE usage, and CB-2FA token if 402 triggered.
- Any Coinbase error codes/messages + correlation IDs from headers.

### When to escalate
- Tokens failing due to suspected OAuth service outage or repeated `invalid_grant` despite valid code/verifier.
- Hash mismatches for PKCE or redirect URI errors that persist after portal refresh.
- 2FA requests (`CB-2FA-TOKEN`) failing repeatedly but only for a subset of users.

---

## 5. Python Codealong: SIWC OAuth Flow
- `python/siwc_oauth_flow.py` builds the authorize URL (with PKCE + `state`) and spins up a lightweight HTTP listener for your registered redirect URI.
- It prints the URL, waits for Coinbase to POST the auth code, exchanges the code for access/refresh tokens, and optionally refreshes immediately to prove the refresh flow.
- Uses environment variables from `.env` / `.env.example`: `COINBASE_CLIENT_ID`, `COINBASE_CLIENT_SECRET`, `COINBASE_REDIRECT_URI`, and `COINBASE_SCOPES`.
- Requires `requests` + `python-dotenv`. Install via `pip install -r requirements.txt` at the repo root.

## 6. Hands-on Exercise
1. Copy `.env.example` to `.env` and populate credentials. Make sure your `COINBASE_REDIRECT_URI` matches the one registered on the CDP portal (e.g., `http://localhost:8080/callback`).
2. Confirm Node or web app (if any) listening on that URI is disabled so the python helper can bind the port.
3. Run `python python/siwc_oauth_flow.py` from the Module 6 folder. The helper prints the authorization URL and awaits the callback.
4. Open the URL in a browser, sign in, and accept the requested scopes (`wallet:user:read`, `wallet:accounts:read`, `offline_access`). If you added `wallet:transactions:send`, be ready to handle 2FA (a 402 response and `CB-2FA-TOKEN` header).
5. Once tokens appear in your terminal, review the access/refresh expiry. Note the `scope` string and ensure it matches your request.
6. (Optional) Answer: What happens when you try exchanging the same refresh token twice? Why does Coinbase issue a warning? Document findings in the module's `exercises.md` or Slack for the cohort.

## 7. Resources
- [Coinbase App OAuth2 Reference](https://docs.cdp.coinbase.com/coinbase-app/authentication-authorization/oauth2/reference)
- [Coinbase Business OAuth2 Reference](https://docs.cdp.coinbase.com/coinbase-business/authentication-authorization/oauth2/reference)
- [Access & Refresh Tokens](https://docs.cdp.coinbase.com/coinbase-app/authentication-authorization/oauth2/access-and-refresh-tokens)
- [OAuth2 Scopes](https://docs.cdp.coinbase.com/coinbase-app/authentication-authorization/oauth2/scopes)
- [Integration Guide + PKCE](https://docs.cdp.coinbase.com/coinbase-app/authentication-authorization/oauth2/integrations)

