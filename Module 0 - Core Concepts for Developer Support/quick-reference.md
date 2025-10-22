# Module 0: Quick Reference Guide

## Authentication Methods

### API Keys
- **Use Case**: Server-to-server, own account access
- **Algorithm**: ECDSA (NOT Ed25519 for Coinbase App SDKs)
- **Security**: IP allowlisting, environment variables
- **Permissions**: View, Trade, Transfer

### OAuth2
- **Use Case**: Third-party app access to user accounts
- **Flow**: Authorization Code + optional PKCE
- **Security**: State parameter (8+ chars), S256 PKCE
- **Tokens**: Access (1 hour), Refresh (1.5 years)

## HTTP Status Codes

| Code | Meaning | Action |
|------|---------|--------|
| 200/201/204 | Success | None |
| 400 | Bad Request | Check parameters |
| 401 | Unauthorized | Check auth |
| **402** | **2FA Required** | **Add CB-2FA-TOKEN header** |
| 403 | Forbidden | Check scopes |
| 404 | Not Found | Verify resource |
| 429 | Rate Limited | Implement backoff |
| 500/503 | Server Error | Check status |

## Rate Limits

- **Standard**: 10,000 requests/hour per key/app
- **OAuth**: 10,000 per authorized user
- **WebSocket**: 750 msg/s per IP, 8/s unauthenticated
- **Response**: `rate_limit_exceeded` error

## Error Response Format

```json
{
  "errors": [
    {
      "id": "error_type",
      "message": "description",
      "url": "doc_link"
    }
  ]
}
```

## Common Error Types

- `rate_limit_exceeded` - Too many requests
- `invalid_scope` - Missing permissions
- `two_factor_required` - 2FA needed
- `authentication_error` - Auth failed
- `not_found` - Resource missing

## Network Environments

### Base Mainnet
- Production environment
- Real value transactions
- Paymaster required
- Higher gas costs

### Base Sepolia
- Test environment
- No real value
- Default sponsorship
- Lower gas costs

## Security Checklist

### API Keys
- [ ] ECDSA algorithm
- [ ] IP allowlisting
- [ ] Environment variables
- [ ] Least privilege

### OAuth2
- [ ] State parameter (8+ chars)
- [ ] PKCE (S256)
- [ ] Minimal scopes
- [ ] Encrypted tokens
- [ ] 2FA for sensitive ops

## Troubleshooting Steps

1. **Collect**: Request/response, headers, timestamps
2. **Authenticate**: Check keys, scopes, permissions
3. **Rate Limit**: Identify 429s, implement backoff
4. **Environment**: Verify network, RPC, assets
5. **Escalate**: Include all data, suspected cause

## Web3 Concepts

### On-chain
- Blockchain recorded
- Transaction hashes
- Gas fees required
- Block confirmations

### Off-chain
- CDP processed
- Webhook acknowledged
- No gas fees
- API operations

### Transaction Components
- From/To addresses
- Value amount
- Gas fees
- Nonce sequence
- Transaction hash

### Smart Accounts (ERC-4337)
- UserOperations
- Batch operations
- Gas sponsorship
- Account abstraction
