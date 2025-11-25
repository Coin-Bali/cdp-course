# Module 14: Troubleshooting Playbook

## Common Issues & Solutions

### Problem: "AgentKit not performing onchain actions"
**Diagnostic Steps:**
1. **Check Wallet:** Does the Agent's wallet have funds (if not sponsored)?
2. **Provider:** Is the `ActionProvider` (e.g., `WETHActionProvider`, `PythActionProvider`) correctly initialized and passed to the agent?
3. **Logs:** Check the Agent's "thought process" logs (if using LangChain). Is it trying to call the tool but failing, or not even selecting the tool?

**Solution:**
- Fund the agent wallet.
- Ensure the prompt explicitly asks for the action (e.g., "Swap 1 ETH to USDC" vs "What is the price?").

### Problem: "Base Appchain Bridge Stuck"
**Diagnostic Steps:**
1. **L1 vs L2:** Bridging involves two transactions (Deposit on L1/Base, Claim on Appchain). Did the first one confirm?
2. **Finality:** Appchains (L3) rely on L2 finality. This can take a few minutes.

**Solution:**
- Check the "Withdrawal Proof" status if moving back to Base.
- Ensure the user has the custom network added to their wallet.

### Problem: "Redirecting Support Tickets"
**Diagnostic Steps:**
1. **Product Identification:** Is the user asking about "Coinbase.com" login, "Pro" limits, or "Prime" custody?
2. **CDP Scope:** CDP Support handles *APIs* and *Builder Tools*. We do not handle Retail account lockouts or Exchange trading fees.

**Solution:**
- Use the **Redirection Templates** provided in the README.
- politely close the ticket after redirecting.

---

## Escalation Guide

### When to Escalate to T2 (CDP Engineering)
- **AgentKit SDK Bug:** The Python/Node SDK throws internal errors on valid inputs.
- **Appchain Downtime:** The Appchain RPC is unresponsive or not producing blocks.

### Required Information for Escalation
1. **Agent Framework**: LangChain / Eliza / etc.
2. **Appchain Chain ID**.
3. **RPC Endpoint**.
4. **Error Logs**.

