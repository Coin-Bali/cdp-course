# Module 5: Embedded Wallets (Smart Wallets)

## Learning Objectives
- Understand Embedded Wallets architecture, passkeys/WebAuthn, and device model
- Initialize the Frontend SDK and integrate with React hooks/components or Wagmi
- Use Smart Accounts (ERC-4337), batching, and gas sponsorship via Paymaster
- Triage common issues (domain allowlist, device compatibility, sponsorship errors)
- Know escalation criteria and required diagnostics

---

## 1. Product Overview

- Frontend SDK provides user-controlled embedded wallets with passkeys/WebAuthn; CDP cannot access user keys.
- Smart Accounts (ERC-4337) enable batching and gas sponsorship via Paymaster.
- Native Onramps integrate alongside Embedded Wallets.

References:
- Frontend SDK packages (@coinbase/cdp-core, cdp-hooks, cdp-react, cdp-wagmi, cdp-solana-standard-wallet)
- React Hooks guide; Wagmi integration; Smart Accounts and Paymaster guides
- Changelog: Smart Accounts support; native Onramps

---

## 2. Technical Flows (High-level)

### 2.1 Initialization & Auth
1) Initialize SDK with `projectId`
2) End-user sign-in (email OTP or supported methods)
3) Create wallet; connect via hooks or Wagmi connector

### 2.2 Smart Accounts & Sponsorship
- Enable smart account features (ERC-4337) via SDK configuration
- Use Paymaster URL or proxy to sponsor gas (Base Sepolia: default sponsorship; Mainnet: configure Paymaster)
- Use Wagmi experimental hooks (`useCapabilities`, `useWriteContracts`)

### 2.3 Domain Allowlisting
- Exact domain matching and HTTPS required
- Configure allowed origins in portal to avoid CORS/widget initialization failures

---

## 3. Common Support Scenarios & Troubleshooting

### "User cannot create a wallet"
- Verify SDK init (`projectId`) and allowed domains
- Check device/browser support for passkeys/WebAuthn; ensure biometrics/security enabled
- Try alternate device or disable privacy features blocking WebAuthn

### "Gas sponsorship failing"
- Inspect Paymaster error codes (e.g., UNAUTHORIZED, GAS_ESTIMATION_ERROR, DENIED_ERROR, UNAVAILABLE_ERROR)
- Confirm policy limits, contract/method allowlisting, and paymaster URL or proxy
- Check network (Base Mainnet vs Base Sepolia) and user op structure

### "Widget or Onramp not appearing"
- Confirm domain allowlist and HTTPS
- Check console/network errors; verify session token (for onramp) not expired/used

---

## 4. Triage Checklists

### Initialization & Environment
- [ ] `projectId` correct; SDK versions noted
- [ ] Domain allowlist includes current origin (exact match)
- [ ] Network and sponsorship config (Base Mainnet vs Sepolia)

### Paymaster & Smart Accounts
- [ ] Paymaster URL/proxy configured
- [ ] Policy limits and allowlisted contracts/methods
- [ ] Error codes/logs captured from hooks/user operations

### Device & Browser
- [ ] OS/browser versions and WebAuthn support
- [ ] Passkeys/biometrics enabled
- [ ] Third-party blockers or strict privacy settings assessed

---

## 5. Escalation Guide

Collect before escalating:
- `projectId`, SDK versions, app URL (origin)
- Device/browser (brand, OS, version), steps to reproduce
- For sponsorship: Paymaster URL/proxy, policy settings, error payloads
- Console/network logs and any correlation IDs

When to escalate:
- Systemic init/auth failures across many domains/users
- Paymaster or smart account infrastructure issues across multiple apps
- Documented behavior mismatches or persistent SDK crashes

---

## 6. Next.js Starter Template Setup Instructions

### Prerequisites
- Node.js 22+ installed
- A CDP Portal account and project created
- Your local domain (`http://localhost:3000`) configured in CDP Portal Domains Configuration

### Step 1: Configure Domain in CDP Portal
Before creating your app, ensure your development domain is allowlisted:

1. Navigate to **CDP Portal** → **Domains Configuration**
2. Click **Add domain**
3. For local development, add: `http://localhost:3000` (or your preferred port)
4. Click **Add domain** again to save
5. **Important**: For production apps, only add your actual production domain. Do not add `localhost` to production CDP projects.

### Step 2: Get Your Project ID
1. In CDP Portal, select your project from the top-left dropdown
2. Click the **gear icon** to view project details
3. Copy the **Project ID** value (you'll need this in the next step)

### Step 3: Create the Next.js App

#### Option A: Interactive Setup (Recommended)
Run the CLI command and follow the interactive prompts:

```bash
npm create @coinbase/cdp-app@latest my-nextjs-app
```

The CLI will prompt you for:
- **Project name**: Enter a name (defaults to `cdp-app`)
- **Template**: Select `Next.js Full Stack App`
- **CDP Project ID**: Paste your Project ID from Step 2
- **Account Type**: Choose one of:
  - `EVM EOA (Regular Accounts)` - Standard Ethereum accounts
  - `EVM Smart Accounts` - ERC-4337 smart accounts with batching and gas sponsorship
  - `Solana Accounts` - Solana blockchain support
- **Onramp Configuration** (Next.js only): Enable or disable Coinbase Onramp integration
- **Domain Whitelist Confirmation**: Confirm you've added `http://localhost:3000` to your CDP Portal

#### Option B: Command-Line Arguments
Pre-configure the setup using command-line arguments:

```bash
# Create a Next.js app with EVM Smart Accounts and Onramp enabled
npm create @coinbase/cdp-app@latest my-nextjs-app \
  --template nextjs \
  --project-id YOUR_PROJECT_ID \
  --account-type evm-smart \
  --onramp

# Create a Next.js app with Solana support
npm create @coinbase/cdp-app@latest my-solana-app \
  --template nextjs \
  --project-id YOUR_PROJECT_ID \
  --account-type solana

# Create a Next.js app with regular EVM accounts (default)
npm create @coinbase/cdp-app@latest my-app \
  --template nextjs \
  --project-id YOUR_PROJECT_ID \
  --account-type evm-eoa \
  --no-onramp
```

**Available Command-Line Arguments:**
- `<directory>`: Optional project directory name (defaults to `cdp-app`)
- `--template <name>`: Template type (`react`, `nextjs`, `react-native`)
- `--project-id <id>`: Your CDP Project ID
- `--account-type <type>`: Account type (`evm-eoa`, `evm-smart`, `solana`)
- `--onramp`: Enable Coinbase Onramp (Next.js only)
- `--no-onramp`: Disable Coinbase Onramp

### Step 4: Install Dependencies and Run

Navigate to your project directory and start the development server:

```bash
cd my-nextjs-app
npm install  # or pnpm install / yarn install
npm run dev  # or pnpm dev / yarn dev
```

Your app will be available at `http://localhost:3000`.

### What's Included in the Next.js Template

The Next.js starter template includes:
- **Next.js 15** with App Router
- **TypeScript** for type safety
- **CDP React components** for authentication and wallet management
- **Example transaction components** for Base Sepolia
- **ESLint** with Next.js configuration
- **Viem** for type-safe Ethereum interactions
- **Onramp integration** (optional, Next.js only)

### Step 5: Configure Environment Variables (If Using Onramp)

If you enabled Onramp during setup, you'll need to configure API keys:

1. Navigate to **CDP Portal** → **API Keys** tab
2. Create a Secret API Key (enter a nickname, restrictions optional)
3. Copy the **API Key ID** and **API Key Secret**
4. In your project, locate the `.env.local` file (or create it)
5. Add your credentials:
   ```
   CDP_API_KEY_ID=your-api-key-id
   CDP_API_KEY_SECRET=your-api-key-secret
   ```

**Security Note**: For better security, use environment variables instead of downloading the API key file. Never commit `.env.local` to version control.

### Step 6: Understanding the Project Structure

Key files and directories in the generated Next.js app:

- `app/` - Next.js App Router pages and layouts
- `components/` - React components including CDP wallet components
- `.env.local` - Environment variables (API keys, project ID)
- `package.json` - Dependencies including `@coinbase/cdp-core`, `@coinbase/cdp-react`, etc.

### Troubleshooting Setup Issues

**"Domain not whitelisted" error:**
- Verify `http://localhost:3000` is added in CDP Portal → Domains Configuration
- Ensure exact match (including protocol and port)
- Wait a few seconds after adding for changes to propagate

**"Invalid Project ID" error:**
- Double-check the Project ID copied from CDP Portal
- Ensure you're using the correct project (check top-left dropdown in portal)

**Onramp not working:**
- Verify API keys are set in `.env.local`
- Ensure you selected the Next.js template (Onramp requires server-side code)
- Check that Onramp was enabled during setup (`--onramp` flag or interactive prompt)

**Build/TypeScript errors:**
- Ensure Node.js 22+ is installed: `node --version`
- Try deleting `node_modules` and reinstalling: `rm -rf node_modules && npm install`

### Next Steps

After setup, explore:
- **Authentication flows**: Email OTP, social login options
- **Wallet operations**: Creating accounts, sending transactions
- **Smart Accounts**: If using `evm-smart`, explore batching and gas sponsorship
- **React Hooks**: Use `@coinbase/cdp-hooks` for state management
- **Wagmi Integration**: Connect CDP wallets to Wagmi for DeFi integrations

---

## 7. References
- Frontend SDK overview and packages
- React Hooks; Wagmi integration; Smart Accounts
- Paymaster introduction and proxy guide
- Next.js Integration Guide
- `create-cdp-app` CLI documentation

