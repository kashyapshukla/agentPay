---
sidebar_position: 2
---

# API Reference

AgentPay is live and publicly accessible. Use the endpoints below directly.

**Base URL:** `https://agentpay-07bn.onrender.com`  
**Interactive Docs:** [Swagger UI](https://agentpay-07bn.onrender.com/docs)

## Authentication

### Generate an Agent Key
```bash
curl -X POST https://agentpay-07bn.onrender.com/v1/auth/keys \
  -H "Content-Type: application/json" \
  -d '{"scopes": ["pay:send"]}'
```

**Response:**
```json
{
  "api_key": "agnt_live_sk_a39fa465...",
  "agent_id": "0a2a60c2-6560-4d71-..."
}
```

### Exchange Key for JWT Token
```bash
curl -X POST https://agentpay-07bn.onrender.com/v1/auth/token \
  -H "Content-Type: application/json" \
  -d '{"api_key": "agnt_live_sk_..."}'
```

## Billing and Metering

### Top-up Wallet
```bash
curl -X POST https://agentpay-07bn.onrender.com/v1/billing/wallets/{agent_id}/topup \
  -H "Content-Type: application/json" \
  -d '{"amount": 10.0}'
```

**Response:**
```json
{
  "agent_id": "0a2a60c2-...",
  "new_balance": 10.0
}
```

### Submit a Metering Event
Logs an event and synchronously deducts units from the wallet.
```bash
curl -X POST https://agentpay-07bn.onrender.com/v1/billing/meter \
  -H "Content-Type: application/json" \
  -d '{
    "agent_id": "{agent_id}",
    "event": "llm.completion",
    "units": 15
  }'
```

**Response:**
```json
{
  "status": "recorded",
  "cost_incurred": 0.015
}
```

### Gateway Status
```bash
curl https://agentpay-07bn.onrender.com/v1/gateway/status
```

## Endpoint Summary

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/v1/auth/keys` | Create a new agent API key |
| `POST` | `/v1/auth/token` | Exchange API key for JWT token |
| `POST` | `/v1/billing/wallets/{agent_id}/topup` | Add funds to agent wallet |
| `POST` | `/v1/billing/meter` | Log metering event & debit wallet |
| `GET`  | `/v1/gateway/status` | Health check |
