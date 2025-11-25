# Module 13: Troubleshooting Playbook

## Common Issues & Solutions

### Problem: "Faucet limit exceeded"
**Diagnostic Steps:**
1. **History:** Have you requested funds for this address recently?
2. **IP Limit:** Are multiple developers using the same office IP?

**Solution:**
- Wait 24 hours.
- Use a different faucet (QuickNode, Alchemy, etc.).
- Use the "Coinbase Wallet" in-app faucet if available.

### Problem: "Funds not arriving"
**Diagnostic Steps:**
1. **Network:** Did you request Sepolia ETH but check Base Mainnet?
2. **Sync:** Is your wallet synced?

**Solution:**
- Check the transaction hash provided by the faucet on the explorer.

### Problem: "Need more than the limit"
**Solution:**
- Bridge real ETH from Mainnet to Base (if you need Mainnet ETH).
- For testnet, accumulate over days or ask in the Discord `#faucet` channel if available.

---

## Escalation Guide

### When to Escalate to T2
- **Faucet Empty:** The faucet wallet itself has no funds (balance 0).
- **System Error:** Faucet UI returns 500 errors consistently.

### Required Information for Escalation
1. **Wallet Address**: 0x...
2. **Faucet Used**: Portal / Wallet / Public.
3. **Error Message**.

