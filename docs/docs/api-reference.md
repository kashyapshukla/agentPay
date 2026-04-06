---
sidebar_position: 2
---

# API Reference

The entire REST API operates on JSON standards.

## Authentication

### Generate an Agent Key
```bash
curl -X POST http://localhost:8000/v1/auth/keys \
-H "Content-Type: application/json" \
-d '{"scopes": ["pay:send"]}'
```

### Validate and Get Token
```bash
curl -X POST http://localhost:8000/v1/auth/token \
-H "Content-Type: application/json" \
-d '{"api_key": "agnt_live_sk_..."}'
```

## Billing and Metering

### Top-up Wallet
```bash
curl -X POST http://localhost:8000/v1/billing/wallets/{agent_id}/topup \
-H "Content-Type: application/json" \
-d '{"amount": 10.0}'
```

### Submit a Metering Event
Logs an event natively and synchronously deducts units.
```bash
curl -X POST http://localhost:8000/v1/billing/meter \
-H "Content-Type: application/json" \
-d '{
  "agent_id": "{agent_id}",
  "event": "llm.completion",
  "units": 15
}'
```
