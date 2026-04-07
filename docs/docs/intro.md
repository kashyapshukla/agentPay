---
sidebar_position: 1
---

# Introduction to AgentPay

**AgentPay** is a powerful B2A (Business-to-Agent) infrastructure that provides autonomous AI agents with digital identity and strict, budget-bound wallets.

## 🎉 Live API — Ready to Use

AgentPay is already deployed and publicly available. No setup required!

**Live API:** [https://agentpay-07bn.onrender.com](https://agentpay-07bn.onrender.com)  
**Swagger Docs:** [https://agentpay-07bn.onrender.com/docs](https://agentpay-07bn.onrender.com/docs)

Try it right now:
```bash
curl https://agentpay-07bn.onrender.com/v1/gateway/status
```

## Quick Start — Use the Live API

You don't need to install or deploy anything. Start using AgentPay in 2 steps:

### 1. Create an Agent Key
```bash
curl -X POST https://agentpay-07bn.onrender.com/v1/auth/keys \
  -H "Content-Type: application/json" \
  -d '{"scopes": ["pay:send"]}'

# Returns:
# {"api_key": "agnt_live_sk_a39f...", "agent_id": "0a2a60c2-..."}
```

### 2. Fund the Wallet & Start Metering
```bash
# Fund the agent with $10
curl -X POST https://agentpay-07bn.onrender.com/v1/billing/wallets/{agent_id}/topup \
  -H "Content-Type: application/json" \
  -d '{"amount": 10.0}'

# Log a metering event (deducts from wallet)
curl -X POST https://agentpay-07bn.onrender.com/v1/billing/meter \
  -H "Content-Type: application/json" \
  -d '{"agent_id": "{agent_id}", "event": "llm.completion", "units": 15}'
```

That's it — your agent now has identity, budget, and metering!

## Want to Self-Host Instead?

If you prefer running your own instance, see the [Deployment Guide](./deployment).

```bash
git clone https://github.com/kashyapshukla/agentPay.git
cd agentPay
docker-compose up --build -d
```

## How It Works

Traditional payments require human intervention via browsers or Stripe checkpoints. AgentPay relies entirely on:
1. **Agent Identity**: You issue your LangChain or AutoGen agents an API key (`agnt_live_sk_...`).
2. **ACID Wallets**: You allocate a predefined budget (e.g., $10) into a secure PostgreSQL wallet governed by row-level locking.
3. **Usage Metering**: Sub-agents autonomously execute actions across third-party APIs, and those APIs charge back against the agent's unique balance without overdrafting.
