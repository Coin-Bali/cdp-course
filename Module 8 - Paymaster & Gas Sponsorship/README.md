# Module 8: Paymaster & Gas Sponsorship

## 1. Product Overview
- **What is a Paymaster?**
  - A smart contract or service that pays for the gas fees of a transaction on behalf of the user.
  - Key component of **ERC-4337 (Account Abstraction)**.
- **Benefits**
  - **Gasless Experience**: Users don't need ETH to interact with dApps.
  - **Sponsorship**: Developers can subsidize specific transactions (e.g., "First 5 txs free").
  - **Fiat Payments**: Users can pay gas in USDC or other tokens (if supported).

## 2. Technical Flow
- **Integration Steps**
  1.  **Configure Policy**: Set up a Paymaster Policy in the CDP Portal (Global limits, User limits, Allowlisted contracts).
  2.  **Get Paymaster URL**: Copy the RPC URL (e.g., `https://api.developer.coinbase.com/rpc/v1/base/sepolia/...`).
  3.  **Client Integration**: Pass `paymasterUrl` to the Smart Wallet SDK or Wagmi config.
- **Base Sepolia vs. Mainnet**
  - **Base Sepolia**: Gas is typically sponsored automatically by CDP for testing.
  - **Base Mainnet**: Requires an active Paymaster Policy and funding (unless using free tier credits).

## 3. Common Support Scenarios & Troubleshooting
- **"Gas estimation error" / "Preverification failed"**
  - **Cause**: The Paymaster refused to sponsor the transaction.
  - **Fix**: Check Paymaster Policy limits (daily spend, per-user spend). Ensure the contract/method being called is allowlisted (if allowlisting is enabled).
- **"Policy Violation"**
  - **Cause**: The transaction exceeds the defined policy rules.
  - **Fix**: Review policy settings in CDP Portal. Increase limits or add the target contract to the allowlist.
- **"User has funds but tx fails"**
  - **Cause**: If `paymasterUrl` is provided, the wallet *expects* sponsorship. If sponsorship fails, the tx fails, even if the user has ETH.
  - **Fix**: Remove `paymasterUrl` to let the user pay, or fix the policy.

## 4. Escalation Guide
- **Collect Data**
  - Paymaster Project ID / Policy ID.
  - Full Error JSON (e.g., `code: -32600`, `message: "Policy violation"`).
  - Bundler URL used.
  - UserOp Hash (if available).
- **Escalate When**
  - "Internal JSON-RPC error" occurs repeatedly.
  - Sponsorship fails despite valid policy and sufficient credits.

## 5. Resources
- [Paymaster Documentation](https://docs.cdp.coinbase.com/paymaster/introduction/welcome)
- [ERC-4337 Specs](https://eips.ethereum.org/EIPS/eip-4337)

