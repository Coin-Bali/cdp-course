# Module 5: Troubleshooting Playbook

## Common Issues & Solutions

### Problem: "Wallet creation failed (500ms timeout)"
**Diagnostic Steps:**
1. **Browser Environment:** Embedded Wallets rely on browser APIs (WebAuthn). Is the user in an Incognito/Private window? (Some restrict local storage/keys).
2. **Domain Allowlist:** Is the current domain (e.g., `localhost:3000`) added to the Allowed Domains in the CDP Portal?
3. **Browser Support:** Is the browser extremely old or unsupported? (Passkeys require modern browser support).

**Solution:**
- Check the Browser Console for specific error messages (e.g., `NotAllowedError`).
- Ensure `https` is used (WebAuthn requires secure context, except `localhost`).
- Verify the Project ID is correct.

### Problem: "User cannot sign transaction (Passkey popup closed/failed)"
**Diagnostic Steps:**
1. **User Action:** Did the user accidentally cancel the biometric prompt?
2. **Device State:** Is the device biometric sensor working?
3. **Cross-Device:** Are they trying to sign on a device different from where the key was created (without Cloud sync)?

**Solution:**
- Guide user to retry and ensure they complete the OS prompt.
- Explain that keys are device-bound unless synced via iCloud/Google Password Manager.

### Problem: "Gas estimation error (UserOp failed)"
**Diagnostic Steps:**
1. **Paymaster Config:** Are you using a Paymaster? If so, is the policy allowing this transaction?
2. **Balance:** If NOT using a Paymaster, does the Smart Wallet address have ETH?
3. **Network:** Is the chain ID correct? (Base vs Base Sepolia).

**Solution:**
- Fund the Smart Wallet if self-paying.
- Check Paymaster logs in CDP Portal if sponsorship is expected.

---

## Escalation Guide

### When to Escalate to T2
- **Service Outage:** Widespread inability to create wallets across all users/regions.
- **Key Recovery Failure:** User followed all recovery steps but Backup mechanism is failing to restore the wallet.
- **Paymaster Bundler Errors:** Persistent "Bundler" errors that are not policy-related.

### Required Information for Escalation
1. **Project ID**: The CDP project UUID.
2. **Wallet Address**: The Smart Account address (0x...).
3. **User ID**: The internal user ID if available.
4. **Browser/OS Version**: Crucial for WebAuthn issues.
5. **Error Logs**: Full console output/stack trace.
