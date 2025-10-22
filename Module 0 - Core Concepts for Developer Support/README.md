# Module 0: Core Concepts for Developer Support

## Learning Objectives
By the end of this module, you will be able to:
- Understand the fundamental differences between API keys and OAuth2 authentication
- Interpret HTTP status codes and error messages from CDP APIs
- Apply rate limiting best practices and troubleshooting techniques
- Distinguish between on-chain and off-chain operations
- Identify the correct network environment for different CDP products

---

## 1. Introduction

### Course Objectives: Bridging the Gap Between T1 and T2

This course is designed to empower T1 support agents with deeper technical knowledge of the Coinbase Developer Platform (CDP) ecosystem. Our goal is to:

- **Reduce Escalations**: Resolve more tickets at T1 by understanding the technical nuances of CDP products
- **Standardize Triage**: Create consistent diagnostic approaches for common issues
- **Improve Resolution Time**: Provide structured troubleshooting playbooks and escalation criteria

### How This Course Will Help You Solve Tickets Faster

- **Structured Playbooks**: Step-by-step troubleshooting guides for common scenarios
- **Quick Reference Materials**: Essential information for rapid ticket resolution
- **Escalation Checklists**: Clear criteria for when and how to escalate to T2

---

## 2. Foundational API Concepts

### What is an API? (Client, Server, Request, Response)

An API (Application Programming Interface) is a set of protocols and tools that allows different software applications to communicate with each other.

**Key Components:**
- **Client**: The application making the request (e.g., a developer's app)
- **Server**: The system processing the request (e.g., CDP APIs)
- **Request**: The message sent from client to server
- **Response**: The message sent back from server to client

**CDP API Types:**
- **REST APIs**: Standard HTTP requests for most CDP operations
- **JSON-RPC**: For blockchain interactions and smart contract calls
- **WebSocket**: Real-time data streams (e.g., Advanced Trade market data)

### Understanding API Keys vs. OAuth 2.0: Authentication & Authorization

#### API Keys
**When to Use**: Server-to-server communication, accessing your own account data

**Key Characteristics:**
- Created through the CDP portal
- **Critical**: Must use ECDSA signature algorithm (Ed25519 NOT supported for Coinbase App SDKs)
- IP allowlisting recommended for security
- Simple permission model: View, Trade, Transfer

**Security Best Practices:**
- Store in environment variables, never in code
- Use least privilege principle
- Enable IP allowlisting when possible
- Rotate keys regularly

#### OAuth 2.0
**When to Use**: Third-party applications accessing user accounts

**Key Characteristics:**
- Authorization Code flow with optional PKCE
- Fine-grained scopes: `service-name:resource:action` pattern
- Access tokens expire in ~1 hour
- Refresh tokens available with `offline_access` scope

**OAuth2 Flow:**
1. Redirect user to authorization URL with `state` parameter
2. User grants permissions
3. Server receives authorization code
4. Exchange code for access token
5. Use access token for API calls

**Security Requirements:**
- **State parameter**: Minimum 8 characters for CSRF protection
- **PKCE**: Use S256 method for additional security
- **2FA**: Required for sensitive scopes like `wallet:transactions:send`
- **Token Storage**: Encrypt access and refresh tokens

### Common HTTP Status Codes and Meanings

| Code | Meaning | Action Required |
|------|---------|----------------|
| 200 | OK | Success - no action needed |
| 201 | Created | Success - resource created |
| 204 | No Content | Success - resource deleted |
| 400 | Bad Request | Check request parameters |
| 401 | Unauthorized | Check authentication |
| **402** | **2FA Required** | **Retry with CB-2FA-TOKEN header** |
| 403 | Forbidden | Check scopes/permissions |
| 404 | Not Found | Verify resource exists |
| 429 | Rate Limited | Implement backoff strategy |
| 500 | Internal Server Error | Check operation status |
| 503 | Service Unavailable | Check CDP status page |

### Reading API Error Messages

CDP APIs return structured error responses with:
- **Machine-readable ID**: For programmatic handling
- **Human-readable message**: For user understanding
- **Correlation ID**: For debugging and support
- **Documentation links**: For additional context

**Example Error Response:**
```json
{
  "errors": [
    {
      "id": "invalid_scope",
      "message": "Invalid scope",
      "url": "http://developers.coinbase.com/api#permissions"
    }
  ]
}
```

**Important**: 5xx errors don't guarantee failure - always check operation status.

### Understanding API Rate Limits

**Standard Limits:**
- **Coinbase App/Business**: 10,000 requests/hour per key/app
- **OAuth**: Scales with authorized users (10,000 per user)
- **Advanced Trade WebSocket**: 750 messages/second per IP, 8/second unauthenticated

**Rate Limit Response:**
```json
{
  "errors": [
    {
      "id": "rate_limit_exceeded",
      "message": "Too many requests"
    }
  ]
}
```

**Best Practices:**
- Implement exponential backoff
- Cache non-volatile data
- Use appropriate request patterns
- Monitor rate limit headers

---

## 3. Foundational Web3 Concepts

### On-chain vs. Off-chain

**On-chain Operations:**
- Recorded on the blockchain
- Have transaction hashes
- Require gas fees
- Need block confirmations
- Examples: Token transfers, smart contract interactions

**Off-chain Operations:**
- Processed by CDP services
- Acknowledged via webhooks
- No gas fees required
- Examples: Account creation, API operations, data queries

### Anatomy of a Crypto Transaction

**Key Components:**
- **From Address**: Sender's wallet address
- **To Address**: Recipient's wallet address
- **Value**: Amount being transferred
- **Gas**: Fee paid to miners/validators
- **Nonce**: Transaction sequence number
- **Hash**: Unique transaction identifier

**Transaction States:**
1. **Pending**: Submitted to mempool
2. **Confirmed**: Included in a block
3. **Finalized**: Sufficient confirmations received

**Smart Account Transactions (ERC-4337):**
- UserOperations instead of traditional transactions
- Support for batching multiple operations
- Gas sponsorship capabilities
- Account abstraction features

### Mainnet vs. Testnet

**Base Mainnet:**
- Production environment
- Real value transactions
- Paymaster configuration required
- Higher gas costs
- Full feature set

**Base Sepolia:**
- Test environment
- No real value
- Default sponsorship for user operations
- Lower gas costs
- Limited feature set

**Network Selection:**
- Use testnet for development and testing
- Use mainnet for production applications
- Ensure correct RPC endpoints
- Verify asset availability

---

## 4. Practical Troubleshooting Framework

### Step 1: Collect Information
- Full request/response payloads
- Headers and authentication details
- Timestamps and correlation IDs
- User context and environment details

### Step 2: Verify Authentication
- Check API key type and permissions
- Validate OAuth scopes and token expiry
- Confirm IP allowlisting settings
- Verify signature algorithms

### Step 3: Check Rate Limits
- Identify 429 responses
- Implement appropriate backoff
- Review request patterns
- Consider caching strategies

### Step 4: Validate Environment
- Confirm correct network (mainnet vs testnet)
- Check RPC endpoint configuration
- Verify asset availability
- Review webhook settings

### Step 5: Escalate When Needed
- Include all collected information
- Specify suspected root cause
- Reference relevant documentation
- Provide reproduction steps

---

## 5. Quick Reference Checklists

### Authentication Checklist
- [ ] API key type matches use case
- [ ] Permissions/scopes are sufficient
- [ ] IP allowlisting configured (if applicable)
- [ ] Signature algorithm is ECDSA (not Ed25519)
- [ ] Credentials stored securely

### OAuth2 Checklist
- [ ] State parameter included (8+ characters)
- [ ] PKCE implemented (S256 recommended)
- [ ] Scopes requested are minimal
- [ ] Tokens encrypted in storage
- [ ] 2FA enabled for sensitive operations

### Rate Limiting Checklist
- [ ] 429 responses identified
- [ ] Exponential backoff implemented
- [ ] Non-volatile data cached
- [ ] Request patterns optimized
- [ ] Rate limit headers monitored

### Network Environment Checklist
- [ ] Correct network selected
- [ ] RPC endpoints configured
- [ ] Asset availability confirmed
- [ ] Webhook endpoints secured
- [ ] Environment variables set

---

## 6. Common Error Scenarios and Solutions

### Authentication Errors
**Problem**: 401 Unauthorized
**Solution**: Check API key validity, permissions, and IP allowlisting

**Problem**: 403 Invalid Scope
**Solution**: Verify OAuth scopes match endpoint requirements

**Problem**: 402 2FA Required
**Solution**: Retry request with CB-2FA-TOKEN header

### Rate Limiting Errors
**Problem**: 429 Too Many Requests
**Solution**: Implement exponential backoff, cache data, optimize requests

### Network Errors
**Problem**: Connection timeouts
**Solution**: Check network connectivity, firewall settings, RPC endpoints

**Problem**: Transaction failures
**Solution**: Verify gas settings, network status, account balances

---

## 7. Next Steps

After completing this module, you should be able to:
1. Identify the appropriate authentication method for different scenarios
2. Interpret error messages and status codes accurately
3. Apply rate limiting best practices
4. Distinguish between on-chain and off-chain operations
5. Select the correct network environment for testing and production

**Ready for Module 1**: Coinbase Pay (Onramp/Offramp) troubleshooting and support scenarios.
