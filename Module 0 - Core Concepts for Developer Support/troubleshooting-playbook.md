# Module 0: Troubleshooting Playbook

## Authentication Issues

### Problem: "My API keys are not working"
**Diagnostic Steps:**
1. Verify key type and permissions
2. Check IP allowlisting settings
3. Confirm signature algorithm (ECDSA or Ed25519)
4. Validate request headers and format
5. Check key expiration, server time and rotation 

**Common Solutions:**
- Regenerate API key with correct permissions
- Update IP allowlist in CDP portal
- Switch to ECDSA signature algorithm
- Verify request format and headers
- Check for typos in key/secret

### Problem: "OAuth2 authentication failing"
**Diagnostic Steps:**
1. Verify client ID and secret
2. Check redirect URI matches exactly
3. Validate state parameter (8+ characters)
4. Confirm PKCE implementation (S256)
5. Check scope requirements

**Common Solutions:**
- Update redirect URI in OAuth app settings
- Implement proper state parameter
- Add PKCE with S256 method
- Request only necessary scopes
- Handle token refresh properly

### Problem: "Getting 2FA required error"
**Diagnostic Steps:**
1. Confirm user has 2FA enabled
2. Check if scope requires 2FA
3. Verify 2FA token format
4. Check token expiration

**Solution:**
- Retry request with CB-2FA-TOKEN header
- Ensure 2FA token is current
- Handle 402 status code properly

## Rate Limiting Issues

### Problem: "Getting rate limited frequently"
**Diagnostic Steps:**
1. Check current rate limit status
2. Analyze request patterns
3. Identify burst vs. sustained requests
4. Review caching implementation

**Solutions:**
- Implement exponential backoff
- Cache non-volatile data
- Optimize request frequency
- Use appropriate request batching
- Monitor rate limit headers

### Problem: "WebSocket rate limiting"
**Diagnostic Steps:**
1. Check connection count per IP
2. Verify message frequency
3. Review subscription patterns
4. Confirm authentication status

**Solutions:**
- Limit concurrent connections
- Implement message queuing
- Use authenticated channels when possible
- Optimize subscription management

## Network and Environment Issues

### Problem: "Wrong network errors"
**Diagnostic Steps:**
1. Verify RPC endpoint configuration
2. Check network parameter in requests
3. Confirm asset availability
4. Validate environment settings

**Solutions:**
- Use correct RPC URLs for environment
- Update network parameters
- Verify asset support
- Check environment variables

### Problem: "Transaction failures"
**Diagnostic Steps:**
1. Check account balance
2. Verify gas settings
3. Confirm network status
4. Review transaction parameters

**Solutions:**
- Ensure sufficient balance
- Adjust gas limits/fees
- Check network congestion
- Validate transaction data

## Error Message Interpretation

### Common Error Patterns

**Authentication Errors:**
- `authentication_error` - Generic auth failure
- `invalid_token` - Token expired/invalid
- `invalid_scope` - Missing permissions
- `unauthorized` - Not authorized for operation

**Validation Errors:**
- `param_required` - Missing required parameter
- `validation_error` - Invalid request format
- `invalid_request` - Malformed request

**Resource Errors:**
- `not_found` - Resource doesn't exist
- `resource_exhausted` - Quota exceeded
- `rate_limit_exceeded` - Too many requests

### Error Response Analysis

**Standard Format:**
```json
{
  "errors": [
    {
      "id": "error_type",
      "message": "Human readable description",
      "url": "Documentation link"
    }
  ]
}
```

**Key Fields:**
- `id`: Machine-readable error type
- `message`: Human-readable description
- `url`: Link to relevant documentation
- `correlationId`: For debugging support

## Escalation Criteria

### When to Escalate to T2

**Authentication Issues:**
- Multiple valid keys failing
- OAuth service outages
- Widespread 2FA failures
- Signature algorithm issues

**Rate Limiting:**
- Unexplained rate limit behavior
- WebSocket connection issues
- API quota problems
- Performance degradation

**Network Issues:**
- RPC endpoint failures
- Asset availability problems
- Transaction processing delays
- Network-specific errors

**System Issues:**
- 5xx errors with unknown status
- Service unavailability
- Data inconsistencies
- Security concerns

### Information to Include in Escalation

**Required Information:**
- Full request/response payloads
- Headers and authentication details
- Timestamps and correlation IDs
- User context and environment
- Steps to reproduce
- Suspected root cause
- Relevant documentation links

**Optional Information:**
- Screenshots or logs
- Previous similar issues
- Workaround attempts
- Business impact assessment

## Prevention Strategies

### Proactive Monitoring
- Set up rate limit alerts
- Monitor authentication failures
- Track error rates by endpoint
- Review user feedback patterns

### Documentation Maintenance
- Keep error message references current
- Update troubleshooting guides
- Maintain escalation procedures
- Document common solutions

### Training and Knowledge Sharing
- Regular team updates on new errors
- Share resolution patterns
- Document lessons learned
- Cross-train on different products

## Quick Decision Tree

```
Authentication Issue?
├─ API Key → Check algorithm, permissions, IP allowlist
├─ OAuth2 → Verify scopes, state, PKCE, tokens
└─ 2FA → Add CB-2FA-TOKEN header

Rate Limiting?
├─ 429 Error → Implement backoff, check patterns
├─ WebSocket → Limit connections, optimize messages
└─ Quota → Review usage, request increase

Network Issue?
├─ Wrong Network → Check RPC, environment
├─ Transaction Fail → Verify balance, gas, status
└─ Asset Issue → Confirm availability, support

Still Failing?
└─ Escalate with full diagnostic information
```
