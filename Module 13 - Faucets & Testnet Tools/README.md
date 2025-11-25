# Module 13: Faucets & Testnet Tools

## 1. Product Overview
- **Purpose**
  - Provide developers with **Testnet Assets** (ETH, USDC) to build and test applications without spending real money.
  - **Base Sepolia**: The primary testnet for Base.
- **Key Tools**
  - **Coinbase Faucet (Portal)**: Authenticated faucet for CDP developers (higher limits).
  - **Wallet Faucets**: Integrated into Coinbase Wallet / Server Wallet SDK.
  - **Third-Party Faucets**: QuickNode, Alchemy, Superchain Faucet.

## 2. Technical Flow
- **Requesting Funds**
  - **Web**: Visit [portal.cdp.coinbase.com/products/faucet](https://portal.cdp.coinbase.com/products/faucet). Connect wallet/Authenticate -> Request Funds.
  - **SDK**: Some SDKs (like Server Wallet) have built-in `faucet` methods for testnets.
  - **Discord**: Some communities offer faucet bots.

## 3. Common Support Scenarios & Troubleshooting
- **"Faucet says 'Dry' or 'Error'"**
  - **Cause**: Faucet wallet is empty, or user hit daily rate limit.
  - **Fix**: Wait 24h; try a different faucet (Superchain vs Base); explain limits.
- **"I need more than the limit"**
  - **Cause**: Enterprise/High-volume testing.
  - **Fix**: Bridge Sepolia ETH from Ethereum Sepolia to Base Sepolia (using Base Bridge).
- **"Testnet funds didn't arrive"**
  - **Cause**: Network congestion or wrong address/network (e.g., sending Sepolia ETH to Mainnet).
  - **Fix**: Check explorer (Base Sepolia Scan). Ensure user is on **Base Sepolia**, not Base Mainnet.

## 4. Escalation Guide
- **Collect Data**
  - Wallet Address.
  - Faucet used (Portal, Third-party).
  - Time of request.
  - Error message screenshot.
- **Escalate When**
  - Coinbase Portal Faucet is down for >1 hour (internal outage).
  - Systematic failure for all users.

## 5. Resources
- [Base Faucet Docs](https://docs.base.org/tools/network-faucets)
- [Superchain Faucet](https://app.optimism.io/faucet)

