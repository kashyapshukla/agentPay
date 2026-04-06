---
sidebar_position: 1
---

# Introduction to AgentPay

**AgentPay** is a powerful B2A (Business-to-Agent) infrastructure that provides autonomous AI agents with digital identity and strict, budget-bound wallets.

## Getting Started in 3 Commands

Deploying AgentPay is designed to be ridiculously fast. Start your local instance by spinning up the interconnected Docker cluster:

```bash
# 1. Clone the repository
git clone https://github.com/agentpay/agentpay.git
cd agentpay

# 2. Build and run the services natively
docker-compose up --build -d

# 3. Verify it is running
curl http://localhost:8000/v1/gateway/status
```

## How It Works

Traditional payments require human intervention via browsers or Stripe checkpoints. AgentPay relies entirely on:
1. **Agent Identity**: You issue your LangChain or AutoGen agents an API key (`agnt_live_sk_...`).
2. **ACID Wallets**: You allocate a predefined budget (e.g., $10) into a secure PostgreSQL wallet governed by row-level locking.
3. **Usage Metering**: Sub-agents autonomously execute actions across third-party APIs, and those APIs charge back against the agent's unique balance limitlessly without overdraftings.
