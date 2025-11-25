# Module 6: Guided Labs & Exercises

## Lab 1: Run the OAuth2 Flow
**Goal:** Successfully authenticate a user and get an Access Token.

### Step 1: Setup
- Ensure `.env` has `SIWC_CLIENT_ID`, `SIWC_CLIENT_SECRET`, and `SIWC_REDIRECT_URI`.
- Ensure `SIWC_REDIRECT_URI` matches `http://localhost:5000/callback` (or your port).

### Step 2: Start the Server
```bash
python "Module 6 - Sign in with Coinbase/python/siwc_oauth_flow.py"
```

### Step 3: Execute Flow
1. Open `http://localhost:5000` in your browser.
2. Click **Start OAuth2 Flow**.
3. Log in to Coinbase (if asked).
4. **Consent:** Click "Allow" on the permission screen.
5. **Success:** You should be redirected back and see your `Access Token` and `Refresh Token`.

---

## Lab 2: Refresh a Token
**Goal:** Use the Refresh Token to get a new Access Token.

### Step 1: Get Refresh Token
- Copy the `refresh_token` from the output of Lab 1 (or check your terminal logs).
- Add it to `.env` as `SIWC_REFRESH_TOKEN` (optional, or just use the UI link if the script supports session).

### Step 2: Trigger Refresh
- Click the **"Refresh Token"** link on the demo page (or navigate to `/refresh_token`).
- **Observe:** The Access Token string changes. The expiration timer resets.

### Step 3: Verify
- If successful, the OAuth lifecycle is working correctly!
