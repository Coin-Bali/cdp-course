# Module 9: Troubleshooting Playbook

## Common Issues & Solutions

### Problem: "Slippage Error / Reverted"
**Diagnostic Steps:**
1. **Market Volatility:** Is the market moving fast? (e.g., Meme coin launch).
2. **Settings:** Is `slippage_bps` too low? (Default might be 1% or 100 bps).
3. **Liquidity:** Is there enough liquidity for the trade size?

**Solution:**
- Increase `slippage_bps` (carefully).
- Retry the quote to get a fresher price.

### Problem: "Insufficient Allowance"
**Diagnostic Steps:**
1. **Approval:** Has the user approved the "Swap Router" to spend their tokens?
2. **Check:** The quote response often includes an `issues` field indicating if `allowance` is needed.

**Solution:**
- User must submit an `approve()` transaction for the token *before* the swap transaction can succeed.

### Problem: "Quote Liquidity Unavailable"
**Diagnostic Steps:**
1. **Token Pair:** Are you trying to swap obscure tokens?
2. **Amount:** Is the amount too large (price impact too high) or too small (dust)?

**Solution:**
- Check if the token is tradable on DEXs (Uniswap/Aerodrome) manually.
- Try a smaller amount.

---

## Escalation Guide

### When to Escalate to T2
- **Bad Pricing:** Consistently seeing prices >5% worse than public DEXs (indicates routing issue).
- **Stuck Approvals:** User approved, but API still says `allowance` required.

### Required Information for Escalation
1. **Quote ID**: If available.
2. **From/To Token**: Contract addresses.
3. **Amount**: Input amount.
4. **Time**: UTC.
5. **User Address**: 0x...

