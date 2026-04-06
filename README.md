# 🤖 AgentPay

**B2A (Business-to-Agent) Infrastructure for Autonomous AI Agents**

AgentPay is an open-source, self-hostable API platform that gives autonomous AI agents their own digital identity and budget-bound wallets. Stop handing your credit card to AI — issue them strict, pre-funded debit cards instead.

---

## ⚡ The Problem

When you build autonomous agents with LangChain, AutoGen, or CrewAI, they inevitably need to **spend money** — calling paid APIs, purchasing datasets, or accessing gated content. Today, developers either:

- Hardcode their personal API keys (dangerous)
- Build fragile webhook state machines (painful)
- Manually approve every transaction (defeats autonomy)

**AgentPay solves this.** You issue each agent a unique API key, fund its wallet with a strict budget, and let it operate autonomously — knowing it can never overspend.

---

## 🏗️ Architecture

```
┌──────────────────────────────────────────────────────┐
│                   Developer / Human                   │
│         (Creates keys, funds wallets, sets limits)    │
└────────────────────────┬─────────────────────────────┘
                         │
                    REST API (FastAPI)
                         │
          ┌──────────────┼──────────────┐
          │              │              │
    ┌─────▼─────┐  ┌─────▼─────┐  ┌────▼─────┐
    │   Auth    │  │  Billing  │  │ Gateway  │
    │  Module   │  │  Module   │  │  Module  │
    │           │  │           │  │          │
    │ • Keys    │  │ • Wallets │  │ • Status │
    │ • JWT     │  │ • Meter   │  │ • Health │
    │ • Scopes  │  │ • Audit   │  │          │
    └─────┬─────┘  └─────┬─────┘  └──────────┘
          │              │
    ┌─────▼──────────────▼─────┐
    │      PostgreSQL (ACID)    │
    │  • Agent Keys             │
    │  • Wallets (row-locking)  │
    │  • Spend Audit Logs       │
    │  • Metering Buckets       │
    └──────────────────────────┘
                         │
    ┌────────────────────▼─────┐
    │    Redis Streams          │
    │  • Real-time metering     │
    │  • Async event ingestion  │
    └────────────┬─────────────┘
                 │
    ┌────────────▼─────────────┐
    │   Aggregator Worker       │
    │  • Hourly/Daily rollups   │
    │  • Consumer Group based   │
    └──────────────────────────┘
```

---

## 🚀 Quick Start (3 Commands)

```bash
# 1. Clone the repository
git clone https://github.com/kashyapshukla/agentPay.git
cd agentPay

# 2. Build and run all services
docker-compose up --build -d

# 3. Verify it's running
curl http://localhost:8000/v1/gateway/status
```

That's it. You now have a running AgentPay instance with PostgreSQL, Redis, the API server, and the background aggregator worker.

---

## 📖 How It Works

### Step 1: Create an Agent Identity
```bash
curl -X POST http://localhost:8000/v1/auth/keys \
  -H "Content-Type: application/json" \
  -d '{"scopes": ["pay:send"]}'

# Response:
# {"api_key": "agnt_live_sk_a39f...", "agent_id": "0a2a60c2-..."}
```

### Step 2: Fund the Wallet
The **human developer** allocates a strict budget. The agent has zero ability to top-up its own wallet.
```bash
curl -X POST http://localhost:8000/v1/billing/wallets/{agent_id}/topup \
  -H "Content-Type: application/json" \
  -d '{"amount": 10.0}'

# Response:
# {"agent_id": "0a2a60c2-...", "new_balance": 10.0}
```

### Step 3: Agent Spends Autonomously
When the agent calls a paid API, the service meters the usage. The wallet is atomically debited using PostgreSQL row-level locking — no double-spending, no overdrafts.
```bash
curl -X POST http://localhost:8000/v1/billing/meter \
  -H "Content-Type: application/json" \
  -d '{"agent_id": "0a2a60c2-...", "event": "llm.completion", "units": 20}'

# Response:
# {"status": "recorded", "cost_incurred": 0.02}
```

### Step 4: Budget Exceeded? Automatically Blocked.
If the agent tries to spend more than its balance, the API returns an error. The agent stops. Your money is safe.

---

## 🐍 Python SDK

Install the native SDK to interact with AgentPay programmatically:

```bash
pip install ./sdks/python
```

```python
from agentpay import AgentPayClient

client = AgentPayClient(api_key="agnt_live_sk_a39f...")

# Top up a wallet
client.topup_wallet(agent_id="0a2a60c2-...", amount=5.0)

# Meter an event
result = client.meter_event(
    agent_id="0a2a60c2-...",
    event_name="llm.completion",
    units=15
)
print(result)  # {"status": "recorded", "cost_incurred": 0.015}
```

---

## 🦜 LangChain Integration

Give your LangChain agents explicit financial autonomy:

```bash
pip install ./integrations/langchain
```

```python
from langchain.agents import initialize_agent, AgentType
from langchain_agentpay import AgentPayMeterTool

# Initialize the payment tool
pay_tool = AgentPayMeterTool(api_key="agnt_live_sk_a39f...")

# Attach to any LangChain agent
tools = [pay_tool, your_search_tool, your_code_tool]
agent = initialize_agent(tools, llm, agent=AgentType.OPENAI_FUNCTIONS)

# The agent now knows how to spend money from its wallet
agent.run("Research competitors. If data costs money, pay for it.")
```

---

## 🔌 Framework Integrations

AgentPay works with any AI agent framework:

| Framework | Integration | How |
|-----------|------------|-----|
| **LangChain** | `langchain-agentpay` | Native `BaseTool` subclass |
| **Microsoft AutoGen** | Python SDK | Register as a callable function |
| **CrewAI** | `langchain-agentpay` | Attach as a Crew tool |
| **Custom Python** | Python SDK | Direct `AgentPayClient` calls |

See the [Integration Examples](docs/docs/integrations/) for detailed walkthroughs.

---

## 🏛️ Project Structure

```
agentpay/
├── core/                         # FastAPI Backend
│   ├── auth/router.py            # Agent key generation & JWT tokens
│   ├── billing/router.py         # Wallet top-ups & metering
│   ├── gateway/router.py         # Health check endpoint
│   ├── database/
│   │   ├── database.py           # Async SQLAlchemy engine
│   │   └── models.py             # AgentKey, Wallet, SpendAuditLog, MeteringBucket
│   ├── services/
│   │   └── redis_client.py       # Redis stream client
│   ├── workers/
│   │   └── aggregator.py         # Background Redis → PostgreSQL aggregator
│   └── main.py                   # FastAPI app entrypoint
├── sdks/
│   └── python/                   # Native Python SDK (agentpay)
├── integrations/
│   └── langchain/                # LangChain tool wrapper (langchain-agentpay)
├── docs/                         # Docusaurus documentation site
├── docker-compose.yml            # Local development (includes Postgres & Redis)
├── docker-compose.prod.yml       # Production (connects to external DBs)
├── .env.example                  # Environment variable template
├── .github/workflows/test.yml    # CI/CD pipeline
├── Dockerfile                    # Python 3.11 container
└── requirements.txt              # Python dependencies
```

---

## 🌐 API Reference

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/v1/auth/keys` | Create a new agent API key |
| `POST` | `/v1/auth/token` | Exchange API key for JWT session token |
| `POST` | `/v1/billing/wallets/{agent_id}/topup` | Add funds to an agent's wallet |
| `POST` | `/v1/billing/meter` | Log a metering event and debit the wallet |
| `GET`  | `/v1/gateway/status` | Health check |

Full interactive docs available at `http://localhost:8000/docs` (Swagger UI).

---

## 🚢 Deployment ($0/month)

AgentPay is designed to be deployed entirely on free tiers:

| Component | Provider | Cost |
|-----------|----------|------|
| Documentation | [Vercel](https://vercel.com) | Free |
| PostgreSQL | [Neon.tech](https://neon.tech) | Free |
| Redis | [Upstash](https://upstash.com) | Free |
| API + Worker | [Render](https://render.com) | Free |
| CI/CD | GitHub Actions | Free |

See the [Deployment Guide](docs/docs/deployment.md) for step-by-step instructions.

---

## 🛠️ Tech Stack

- **API**: Python 3.11, FastAPI, Uvicorn
- **Database**: PostgreSQL (async via SQLAlchemy + asyncpg)
- **Cache**: Redis Streams (async via redis-py)
- **Auth**: bcrypt hashing + JWT session tokens
- **Containers**: Docker & Docker Compose
- **Docs**: Docusaurus (React)
- **CI/CD**: GitHub Actions

---

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'feat: add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

The CI pipeline will automatically validate your code on every PR.

---

## 📄 License

This project is open-source under the [MIT License](LICENSE).

---

<p align="center">
  <b>AgentPay</b> — Stop giving AI your credit card. Give them a debit card instead.
</p>