---
sidebar_position: 1.5
title: The Developer Journey
---

# Integrating AgentPay: The User Journey

AgentPay is **already deployed and live**. You don't need to set up anything. Just follow the steps below to integrate it into your AI project.

**Live API:** `https://agentpay-07bn.onrender.com`

## 1. Issue an Identity (The Onboarding)

Normally, you would pass your own personal Stripe or OpenAI credit card to the agent. With AgentPay, you issue the agent its own unique **Passport**.

Hit the live API to create an isolated key specifically for your agent:
```bash
curl -X POST https://agentpay-07bn.onrender.com/v1/auth/keys \
  -H "Content-Type: application/json" \
  -d '{"scopes": ["pay:send"]}'

# Returns:
# {"api_key": "agnt_live_sk_a39f...", "agent_id": "0a2a60c2-..."}
```

## 2. Fund the Agent (The Centralized Budgeting)

This step happens **strictly outside of the agent's control**. The human developer (or their centralized analytics backend) acts as the central bank issuing predefined debit cards.

Right after creating the identity, the developer explicitly dictates the budget. You allocate exactly **$5.00** to this new sub-agent using root system privileges:

```bash
curl -X POST https://agentpay-07bn.onrender.com/v1/billing/wallets/0a2a60c2-.../topup \
  -H "Content-Type: application/json" \
  -d '{"amount": 5.0}'
```

By completing this step, your agent is mathematically constrained. When you hand the keys over to the LangChain script in Step 3, the agent only knows its `api_key`. It has absolutely no route or endpoint parameter available to "top up" its own wallet. It can never spend more than $5.00 without you explicitly calling this API again!

## 3. Plugging it into your Code (The SDK)

Now, you go back to your Python project where your LangChain or custom agent lives.
Instead of writing complex web-hooks or state machines to track spending, you simply drop in the `langchain-agentpay` integration we built.

```python
from langchain.agents import initialize_agent, AgentType
from langchain_agentpay import AgentPayMeterTool

# 1. Initialize the tool with your Agent's API key
#    It connects to the live API automatically
pay_tool = AgentPayMeterTool(
    api_key="agnt_live_sk_a39f...",
    base_url="https://agentpay-07bn.onrender.com"
)

# 2. Give the tool directly to your Langchain Agent
tools = [pay_tool] # Mix it with your WebSearch or Compute tools!
agent = initialize_agent(tools, llm, agent=AgentType.OPENAI_FUNCTIONS)

# 3. Watch it work autonomously!
agent.run("Research the stock market and if the API costs money, pay for it using your wallet.")
```

## 4. Autonomous Metering (The Background)

When the agent decides to execute a task using a paid API, it invokes the `AgentPayMeterTool`. This tool securely streams a metering event to the live backend.

1. **Redis ingest**: The event is ingested instantly so your Python script doesn't slow down.
2. **ACID debit**: The $5.00 wallet in PostgreSQL drops to $4.98 securely using strict row-locking, preventing double-spending.
3. **Aggregation**: Our background worker builds an hourly dashboard of the agent's spending so you can log in later and see exactly where the money went!

That's it. Your agent is now financially autonomous, mathematically constrained, and entirely plug-and-play!
