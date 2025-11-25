# Module 5: Guided Labs & Exercises

## Lab 1: Environment Verification (Conceptual)
**Goal:** Ensure your development environment is ready for Embedded Wallets.

### Step 1: Check Node.js
Run: `node -v`
- Requirement: v18+ (ideally v20).

### Step 2: Verify Project ID
- Log in to CDP Portal.
- Navigate to Embedded Wallets.
- Copy your `Project ID`.
- Ensure you have created an "Allowed Domain" for `localhost:3000` (or your dev port).

### Step 3: Template Setup (Optional)
- If you haven't already, run:
  `npx create-coinbase-app@latest my-app`
- Follow the prompts.
- Select "Embedded Wallet" as the feature.

---

## Lab 2: Inspecting Local Storage (Frontend)
**Goal:** Understand where the wallet "session" lives (securely).

### Step 1: Open your App
Run your Embedded Wallet app (e.g., `npm run dev`).

### Step 2: Create/Sign In
Perform the login flow with your email.

### Step 3: Developer Tools
- Open Chrome DevTools (F12) -> Application Tab.
- Look at **Local Storage**.
- You typically won't see the *private key* (as it's in the secure enclave/passkey), but you might see session tokens or SDK state.
- **Action:** Clear Local Storage.
- **Result:** Reload the page. You should be logged out. This confirms session state management.

