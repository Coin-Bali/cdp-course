# Module 14: Coinbase Ecosystem Overview (for Redirection)

## Learning Objectives
- Know when a developer question is outside CDP scope and which teams/products to hand off to.  
- Understand the high-level differentiators for Base, Coinbase Exchange/Pro, International Exchange, Coinbase Retail, Prime, and Derivatives.  
- Practice collecting diagnostic clues during triage so escalations are routed to the right group quickly.  
- Provide polite redirection messaging, links, and resources that help T1 stay focused on CDP-only products.

---

## 1. Base (Ethereum Layer 2) & Appchains
- **What it is**: Base is Coinbase’s low-fee Ethereum L2, incubated by Coinbase and now open to public builders.
- **Base Appchains**: Dedicated Layer 3 chains (L3s) built on top of Base for specific apps requiring high throughput.
  - **Key Clues**: "Appchain", "L3", "Custom Gas Token", "Dedicated Sequencer".
- **Support Scope**: 
  - **In Scope**: Issues with CDP tools *connecting* to Base (e.g., Server Wallet on Base, Paymaster on Base).
  - **Out of Scope**: Protocol-level issues, Node operations, Bridge delays (unless using OnchainKit Bridge), Appchain deployment.
- **Redirect Guidance**: Point developers to [Base Docs](https://docs.base.org/), Base Discord, or Appchain specific support channels (often Enterprise).

---

## 2. AgentKit (AI Agents)
- **What it is**: A toolkit for building AI agents that can perform onchain actions (Trade, Transfer, Deploy).
- **Key Clues**: "Agent", "LangChain", "Python SDK", "Autonomous trading".
- **Support Scope**:
  - **In Scope**: Failures in the *underlying CDP actions* (e.g., "Agent failed to sign transaction via Server Wallet").
  - **Out of Scope**: AI logic errors ("My agent is hallucinating"), Model integration issues (OpenAI API errors).
- **Redirect Guidance**: Direct to AgentKit docs or the specific AI framework's community if the issue is logic-related.

---

## 3. Coinbase Exchange / Pro (Retail Trading)
- **What it is**: Coinbase Exchange (also marketed as Coinbase Pro) is the professional trading interface for retail customers, separate from the Advanced Trade API.  
- **Key Clues**: Topics about UI trading, viewing balances on pro.coinbase.com, deposit/withdraw statuses, KYC or asset listing on retail order books.  
- **CDP Scope**: We support advanced trade/order APIs, but not the retail UI or trading account setup.  
- **Redirect**: Send to Coinbase customer support (help.coinbase.com) or the Exchange/Pro help center; mention “retail exchange limits and login issues are not handled within CDP.”

---

## 4. Coinbase International Exchange
- **What it is**: Perpetual futures + spot trading platform for non-US institutional users.  
- **Key Clues**: Questions referencing perpetual products, margin, or spread trading outside the United States.  
- **Redirect**: Escalate to International Exchange support with the client’s region and product references; remind the developer that CDP Advanced Trade API is separate and runs on Coinbase Developer Platform endpoints.

---

## 5. Coinbase Retail
- **What it is**: The consumer-facing Coinbase mobile/web app used for buying/selling crypto.  
- **Key Clues**: Login issues, 2FA resets, identity verification, deposit holds, or wallet/portfolio questions unrelated to CDP APIs.  
- **Redirect**: Route to retail support (help.coinbase.com) and remind the developer to open a ticket inside their Coinbase account. Mention that CDP support cannot access retail account data.

---

## 6. Coinbase Prime
- **What it is**: Institutional prime brokerage (custody, OTC, advanced trading) targeted at large financial firms (https://docs.cdp.coinbase.com/prime/introduction/welcome).  
- **Key Clues**: Mentions of custody account numbers, prime financing, or API access request for institutional trading.  
- **Redirect**: Escalate to the Prime ops/account team, collecting the account ID, request type, and sample logs; let them know Prime has dedicated support channels outside CDP.

---

## 7. Coinbase Derivatives
- **What it is**: CFTC-regulated US futures exchange with REST,FIX,SBE,UDP interfaces for institutional derivatives trading (https://docs.cdp.coinbase.com/derivatives/introduction/welcome).  
- **Key Clues**: References to futures, margin, or API names from derivatives documentation.  
- **Redirect**: Send to Coinbase Derivatives support desk; emphasize that derivatives APIs are regulated and not in CDP’s remit.

---

## 8. Redirection Best Practices
- **Collect context**: Always ask “Which Coinbase product/page are you on?” and capture URLs, account types, product names, and any error codes or request IDs.  
- **Offer helpful alternatives**: Even when redirecting, provide the direct doc link or support portal relevant to their issue (e.g., Base docs for RPC issues, help.coinbase.com for retail).  
- **Clarify scope**: Explain that CDP focuses on developer-facing APIs (Onramp, Trade API, Staking, Server/Embedded wallets, SIWC, etc.) and refer others to the right team for fast resolution.

---

## 9. Useful Links
- CDP Docs Home: https://docs.cdp.coinbase.com/index  
- Coinbase Prime APIs: https://docs.cdp.coinbase.com/prime/introduction/welcome  
- Coinbase Derivatives: https://docs.cdp.coinbase.com/derivatives/introduction/welcome  
- Coinbase Business OAuth/Accounts/Payments: https://docs.cdp.coinbase.com/coinbase-business/introduction/welcome  
- AgentKit Docs: https://docs.cdp.coinbase.com/agent-kit/welcome

---

## 10. Redirection Message Templates
- **Base question**: “Thanks for the details. Base is Coinbase’s Layer 2 network, and RPC/deployment questions are handled in the Base docs/Discord. Please try the Base developer guides here and feel free to reach out to the Base community channels for chain-specific RPC or node support. CDP support stays focused on API products.”
- **Appchain question**: "Base Appchains (L3s) are dedicated chains. Support for appchain infrastructure or custom gas tokens is usually handled by the specific Appchain provider or Base engineering team. I recommend reaching out via your enterprise support channel or Base Discord."
- **AgentKit question**: "Since this appears to be an issue with the AI model's logic (hallucination/looping) rather than the underlying wallet action, I recommend checking the LangChain/Framework docs. If the agent fails to *sign* the transaction via CDP Wallet, we can certainly help investigate the wallet error."
- **Exchange/Pro issue**: “It sounds like this is happening inside the Coinbase Exchange/Pro trading UI, which is separate from the Advanced Trade API. I recommend opening a ticket via help.coinbase.com or the Exchange help center, since our CDP team focuses on the developer APIs.”
- **International Exchange question**: “This looks like an International Exchange futures/perpetual question. That team has dedicated regional support; please submit your case with your region and product name directly through the International Exchange support desk so they can help.”
- **Retail login/account issue**: “Retail account access, sign-in, and fraud holds are owned by the Coinbase retail team. Please visit help.coinbase.com and submit under the ‘Account access’ category because CDP doesn’t have visibility into retail profiles.”
- **Prime/Institutional request**: “For Prime custody/trading/capital markets support you’ll want the Coinbase Prime operations team. Share your account ID and request type with Prime support—CDP T1 only handles the developer APIs, not Prime-specific infrastructure.”
- **Derivatives question**: “Derivatives/futures APIs run under Coinbase Derivatives because they are CFTC-regulated. Please ping the Coinbase Derivatives support desk and include the instrument/product name so they can triage your request quickly.”
