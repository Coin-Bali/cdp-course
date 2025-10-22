# Module 0: Practical Exercises

## Exercise 1: Authentication Troubleshooting

### Scenario
A developer reports: "My API calls are returning 401 Unauthorized errors. I'm using the API key I created yesterday."

### Your Task
Walk through the diagnostic process and identify potential causes.

**Step 1: Initial Questions**
- What type of API key are they using?
- What permissions were granted?
- Are they using the correct signature algorithm?
- Is IP allowlisting configured?

**Step 2: Verification Steps**
- Check key validity in CDP portal
- Verify request format and headers
- Confirm IP allowlist settings
- Test with minimal request

**Step 3: Common Solutions**
- Regenerate API key if needed
- Update IP allowlist
- Switch to ECDSA algorithm
- Verify request format

### Expected Outcome
Identify the most likely cause and provide step-by-step resolution.

---

## Exercise 2: OAuth2 Flow Analysis

### Scenario
A developer is implementing OAuth2 for their web application and getting "Invalid redirect URI" errors.

### Your Task
Help them troubleshoot the OAuth2 implementation.

**Step 1: Verify Configuration**
- Check redirect URI in OAuth app settings
- Confirm URI matches exactly (including protocol, domain, path)
- Verify URL encoding if needed

**Step 2: Check Implementation**
- Validate state parameter (8+ characters)
- Confirm PKCE implementation
- Check scope requirements
- Verify token handling

**Step 3: Security Considerations**
- Ensure state parameter for CSRF protection
- Implement proper token storage
- Use HTTPS for redirect URIs
- Handle token refresh properly

### Expected Outcome
Provide complete OAuth2 implementation guidance with security best practices.

---

## Exercise 3: Rate Limiting Response

### Scenario
A developer's application is hitting rate limits frequently, causing 429 errors.

### Your Task
Design a rate limiting strategy for their application.

**Step 1: Analyze Current Usage**
- Review request patterns
- Identify burst vs. sustained requests
- Check for unnecessary API calls
- Analyze caching opportunities

**Step 2: Implement Solutions**
- Design exponential backoff strategy
- Identify data that can be cached
- Optimize request frequency
- Consider request batching

**Step 3: Monitoring and Alerts**
- Set up rate limit monitoring
- Create alert thresholds
- Implement usage tracking
- Plan for scaling

### Expected Outcome
Provide a comprehensive rate limiting strategy with implementation details.

---

## Exercise 4: Error Message Interpretation

### Scenario
A developer receives this error response:

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

### Your Task
Interpret this error and provide guidance.

**Step 1: Error Analysis**
- Identify the error type
- Understand the cause
- Check the documentation link
- Determine required action

**Step 2: Solution Steps**
- Verify current scopes
- Check endpoint requirements
- Update OAuth request
- Test with correct scopes

**Step 3: Prevention**
- Document scope requirements
- Implement scope validation
- Add error handling
- Create user guidance

### Expected Outcome
Provide clear interpretation and step-by-step resolution.

---

## Exercise 5: Network Environment Selection

### Scenario
A developer is building a DeFi application and needs to choose between Base Mainnet and Base Sepolia.

### Your Task
Guide them through the decision process.

**Step 1: Requirements Analysis**
- Identify use case (development vs. production)
- Check feature requirements
- Consider cost implications
- Evaluate security needs

**Step 2: Environment Comparison**
- Base Mainnet: Production, real value, paymaster required
- Base Sepolia: Testing, no real value, default sponsorship
- RPC endpoint differences
- Asset availability

**Step 3: Implementation Guidance**
- Set up correct RPC endpoints
- Configure environment variables
- Implement network switching
- Handle environment-specific features

### Expected Outcome
Provide clear guidance on environment selection and implementation.

---

## Exercise 6: Web3 Concept Application

### Scenario
A developer is confused about why their transaction is "pending" and wants to understand the difference between on-chain and off-chain operations.

### Your Task
Explain the concepts and help them understand their transaction status.

**Step 1: Concept Explanation**
- Define on-chain vs. off-chain
- Explain transaction lifecycle
- Describe confirmation process
- Identify gas fee requirements

**Step 2: Transaction Analysis**
- Check transaction hash on block explorer
- Verify network status
- Confirm gas settings
- Review account balance

**Step 3: Troubleshooting Steps**
- Provide block explorer links
- Explain confirmation times
- Suggest gas adjustments
- Offer monitoring solutions

### Expected Outcome
Provide clear explanation of Web3 concepts and practical troubleshooting steps.

---

## Exercise 7: Complete Troubleshooting Scenario

### Scenario
A developer reports: "My application was working yesterday, but today I'm getting 500 errors on all API calls. I haven't changed anything."

### Your Task
Conduct a complete troubleshooting investigation.

**Step 1: Information Gathering**
- Collect error details and timestamps
- Check CDP status page
- Verify recent changes
- Review error patterns

**Step 2: Diagnostic Process**
- Test with minimal requests
- Check authentication status
- Verify network connectivity
- Review rate limiting

**Step 3: Resolution Steps**
- Implement appropriate fixes
- Test resolution
- Document solution
- Plan prevention

**Step 4: Escalation Decision**
- Determine if T2 escalation needed
- Prepare escalation information
- Document troubleshooting steps
- Provide business impact assessment

### Expected Outcome
Complete troubleshooting investigation with clear resolution or escalation path.

---

## Exercise 8: Security Best Practices

### Scenario
A developer is asking about storing API keys securely in their application.

### Your Task
Provide comprehensive security guidance.

**Step 1: Current Practices Assessment**
- Review current storage methods
- Identify security risks
- Check access controls
- Evaluate encryption

**Step 2: Security Recommendations**
- Environment variable storage
- Secret management services
- Access control implementation
- Regular key rotation

**Step 3: Implementation Guidance**
- Secure storage setup
- Access control configuration
- Monitoring and alerting
- Incident response planning

### Expected Outcome
Provide comprehensive security best practices with implementation guidance.

---

## Exercise 9: API Integration Planning

### Scenario
A developer wants to integrate multiple CDP APIs and needs guidance on authentication strategy.

### Your Task
Design an authentication strategy for their use case.

**Step 1: Requirements Analysis**
- Identify required APIs
- Determine access patterns
- Check permission requirements
- Evaluate security needs

**Step 2: Strategy Design**
- Choose authentication methods
- Plan permission structure
- Design security measures
- Consider scalability

**Step 3: Implementation Plan**
- Authentication setup
- Permission configuration
- Security implementation
- Testing and validation

### Expected Outcome
Provide comprehensive authentication strategy with implementation plan.

---

## Exercise 10: Error Handling Implementation

### Scenario
A developer wants to implement robust error handling for their CDP API integration.

### Your Task
Design an error handling strategy.

**Step 1: Error Analysis**
- Identify common error types
- Understand error patterns
- Check retry requirements
- Evaluate user experience

**Step 2: Strategy Design**
- Error classification system
- Retry logic implementation
- User notification system
- Logging and monitoring

**Step 3: Implementation**
- Error handling code
- Retry mechanisms
- User feedback systems
- Monitoring setup

### Expected Outcome
Provide comprehensive error handling strategy with implementation details.

---

## Exercise Solutions and Discussion

### Exercise 1 Solution
**Most Likely Causes:**
1. Wrong signature algorithm (Ed25519 instead of ECDSA)
2. IP allowlist blocking requests
3. Insufficient permissions
4. Malformed request format

**Resolution Steps:**
1. Verify ECDSA algorithm usage
2. Check IP allowlist settings
3. Confirm required permissions
4. Validate request format

### Exercise 2 Solution
**Common Issues:**
1. Redirect URI mismatch
2. Missing state parameter
3. Incorrect PKCE implementation
4. Scope requirements

**Resolution Steps:**
1. Update redirect URI in OAuth app
2. Implement state parameter (8+ chars)
3. Add PKCE with S256 method
4. Request appropriate scopes

### Exercise 3 Solution
**Rate Limiting Strategy:**
1. Implement exponential backoff
2. Cache non-volatile data
3. Optimize request patterns
4. Monitor usage and set alerts

**Implementation:**
- Backoff: Start with 1s, double each retry
- Caching: Cache data for 5-10 minutes
- Patterns: Batch requests when possible
- Monitoring: Track 429 responses

### Exercise 4 Solution
**Error Interpretation:**
- Error: Missing or invalid OAuth scope
- Cause: Requested scope not granted or doesn't exist
- Action: Check scope requirements and update OAuth request

**Resolution:**
1. Verify endpoint scope requirements
2. Update OAuth authorization URL
3. Test with correct scopes
4. Implement scope validation

### Exercise 5 Solution
**Environment Selection:**
- Development: Base Sepolia (testnet, default sponsorship)
- Production: Base Mainnet (real value, paymaster required)

**Implementation:**
- Set up environment variables
- Configure RPC endpoints
- Implement network switching
- Handle environment-specific features

### Exercise 6 Solution
**Concept Explanation:**
- On-chain: Recorded on blockchain, has hash, requires gas
- Off-chain: Processed by CDP, webhook acknowledged, no gas

**Transaction Status:**
- Pending: In mempool, waiting for confirmation
- Confirmed: Included in block
- Finalized: Sufficient confirmations

### Exercise 7 Solution
**Troubleshooting Steps:**
1. Check CDP status page
2. Verify authentication
3. Test with minimal requests
4. Check network connectivity
5. Review recent changes

**Resolution:**
- If service issue: Wait for resolution
- If auth issue: Regenerate keys
- If network issue: Check connectivity
- If unknown: Escalate with full details

### Exercise 8 Solution
**Security Best Practices:**
1. Use environment variables
2. Implement secret management
3. Enable access controls
4. Rotate keys regularly
5. Monitor for breaches

**Implementation:**
- Store keys in environment variables
- Use services like AWS Secrets Manager
- Implement least privilege access
- Set up key rotation schedule
- Monitor access logs

### Exercise 9 Solution
**Authentication Strategy:**
- API Keys: For server-to-server operations
- OAuth2: For user account access
- Permissions: Least privilege principle
- Security: IP allowlisting, encryption

**Implementation:**
- Set up API keys with minimal permissions
- Implement OAuth2 for user access
- Configure IP allowlisting
- Encrypt stored credentials

### Exercise 10 Solution
**Error Handling Strategy:**
1. Classify errors by type
2. Implement retry logic
3. Provide user feedback
4. Log for monitoring

**Implementation:**
- 4xx errors: User input issues
- 5xx errors: Server issues, retry
- Rate limits: Exponential backoff
- Network errors: Retry with backoff
