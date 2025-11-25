# Module 14: Guided Labs & Exercises

## Lab 1: The "Not Our Bug" Game
**Goal:** Correctly identify which Coinbase product team owns a ticket.

### Scenario 1
**Ticket:** "I cannot withdraw my USD from Coinbase.com to my Chase bank account. The button is greyed out."
**Action:** Who owns this?
- [ ] CDP Support
- [ ] Retail Support (Help Center)
- [ ] Prime Support
*Answer: Retail Support.*

### Scenario 2
**Ticket:** "My API Key for `api.coinbase.com` is getting 401s when I try to trade programmatically."
**Action:** Who owns this?
- [ ] Retail Support
- [ ] CDP Support (Advanced Trade API)
- [ ] Cloud Support
*Answer: CDP Support (You!).*

### Scenario 3
**Ticket:** "I want to launch a Base Appchain for my gaming studio."
**Action:** Who owns this?
- [ ] CDP Sales / Appchains Team
- [ ] Retail Support
*Answer: CDP Sales / Appchains Team.*

---

## Lab 2: AgentKit Concept (Thought Experiment)
**Goal:** Design an Agent's Toolset.

### Challenge
You are building an AI Agent to "Manage a Portfolio". Which CDP Action Providers should you give it?
1. `WalletActionProvider` (Get Balance, Transfer)?
2. `TradeActionProvider` (Swap)?
3. `TwitterActionProvider` (Post tweets)?

*Discussion:* To manage a portfolio, it definitely needs Wallet and Trade. Twitter is optional but cool!

