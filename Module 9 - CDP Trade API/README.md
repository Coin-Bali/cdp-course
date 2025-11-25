# Module 9: CDP Trade API (Onchain Swaps)

## 1. Product Overview
- **What is the CDP Trade API?**
  - An API to execute **Onchain Token Swaps** (DEX Aggregation).
  - Uses **0x** technology to find the best price across decentralized exchanges (Uniswap, Curve, Balancer, etc.).
  - **Distinct from Advanced Trade**: Advanced Trade connects to Coinbase's centralized order book. CDP Trade API connects to decentralized liquidity pools.
- **Use Cases**
  - In-app token swaps for wallets.
  - Automated trading bots on Base/Ethereum.
  - DeFi portfolio rebalancing.

## 2. Technical Flow
- **Lifecycle**
  1.  **Get Quote**: Call `GET /v2/evm/swaps/quote` (or `POST` for payload) to check rates, gas fees, and slippage.
  2.  **Approve Token** (If selling a token): User must `approve` the swap contract to spend their tokens (ERC-20 allowance).
  3.  **Sign & Execute**: Sign the transaction payload returned by the quote and broadcast it (via Server Wallet or external wallet).

## 3. Common Support Scenarios & Troubleshooting
- **"Swap failed / Reverted"**
  - **Cause**: Slippage exceeded (price moved), insufficient gas, or insufficient token balance/allowance.
  - **Fix**: Increase slippage tolerance; ensure ETH for gas; check ERC-20 allowance.
- **"Rate seems wrong / High slippage"**
  - **Cause**: Low liquidity for the token pair.
  - **Fix**: Compare with other aggregators. Large orders on low-liquidity pairs have high price impact.
- **"Unsupported Token"**
  - **Cause**: Token not verified or has no liquidity on supported DEXes.
  - **Fix**: Verify contract address and network (Base vs Ethereum).

## 4. Escalation Guide
- **Collect Data**
  - Token Pair (Address In -> Address Out).
  - Amount.
  - Network (Base/Eth).
  - Quote ID (if available).
  - Transaction Hash (if executed).
- **Escalate When**
  - "No liquidity" error for major pairs (e.g., ETH-USDC).
  - Systematic quote failures.

## 5. Resources
- [Trade API Documentation](https://docs.cdp.coinbase.com/trade-api/welcome)
- [0x Protocol](https://0x.org/)

