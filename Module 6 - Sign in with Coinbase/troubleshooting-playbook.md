# Module 6: Troubleshooting Playbook

## Common Issues & Solutions

### Problem: "Redirect URI mismatch error"
**Diagnostic Steps:**
1. **Check URL:** Does the `redirect_uri` in your code match *exactly* what is in the CDP Portal?
   - `http` vs `https`
   - Trailing slashes (`/callback` vs `/callback/`)
   - Port numbers (`:5000` vs `:3000`)
2. **Encoding:** Is the URI properly URL-encoded in the query string?

**Solution:**
- Copy-paste the URI from the Portal to your `.env` file.
- Ensure `redirect_uri` matches in both the AUTHORIZE request and the TOKEN exchange request.

### Problem: "Invalid Scope"
**Diagnostic Steps:**
1. **Check Scopes:** Are you requesting a scope (e.g., `wallet:transactions:send`) that your OAuth client is not configured for?
2. **Typos:** Check for spelling (e.g., `wallet:user:read` vs `user:read`).

**Solution:**
- Verify the list of requested scopes against the allowed scopes in documentation.

### Problem: "Token Exchange Failed (Invalid Grant)"
**Diagnostic Steps:**
1. **Code Reuse:** Are you trying to use the same `code` twice? Auth codes are one-time use.
2. **Expiry:** Did more than ~10 minutes pass between getting the code and swapping it?
3. **PKCE:** If using PKCE, is the `code_verifier` correct and matching the `code_challenge` sent earlier?

**Solution:**
- Ensure atomic exchange (swap code for token immediately).
- Verify PKCE logic (S256).

---

## Escalation Guide

### When to Escalate to T2
- **OAuth Service 500s:** The `login.coinbase.com` page is returning server errors.
- **Scope Bugs:** You have the permission, but the API returns 403 Forbidden consistently.

### Required Information for Escalation
1. **Client ID**: Your OAuth App ID.
2. **Redirect URI**: The specific URI failing.
3. **Timestamps**: UTC time of the flow.
4. **Error Description**: The `error_description` param in the URL redirect or JSON response.

