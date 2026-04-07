---
sidebar_position: 4
---

# Deployment Options

## Option 1: Use the Hosted API (Recommended)

AgentPay is **already deployed and publicly available**. No setup, no cost, no infrastructure needed.

| Resource | URL |
|----------|-----|
| **Live API** | [https://agentpay-07bn.onrender.com](https://agentpay-07bn.onrender.com) |
| **Swagger Docs** | [https://agentpay-07bn.onrender.com/docs](https://agentpay-07bn.onrender.com/docs) |
| **Health Check** | [https://agentpay-07bn.onrender.com/v1/gateway/status](https://agentpay-07bn.onrender.com/v1/gateway/status) |

Simply point your SDK or cURL commands at the live URL and start building:
```python
from agentpay import AgentPayClient

client = AgentPayClient(
    api_key="agnt_live_sk_...",
    base_url="https://agentpay-07bn.onrender.com"
)
```

---

## Option 2: Self-Host with Docker (Full Control)

If you need data sovereignty or want to run AgentPay on your own infrastructure:

```bash
git clone https://github.com/kashyapshukla/agentPay.git
cd agentPay
docker-compose up --build -d
```

This spins up PostgreSQL, Redis, the API server, and the background aggregator worker locally.

---

## Option 3: Self-Host on Free Cloud Tiers ($0/month)

If you want your own dedicated cloud instance without paying:

| Component | Provider | Cost |
|-----------|----------|------|
| Documentation | [Vercel](https://vercel.com) | Free |
| PostgreSQL | [Neon.tech](https://neon.tech) | Free |
| Redis | [Upstash](https://upstash.com) | Free |
| API + Worker | [Render](https://render.com) | Free |
| CI/CD | GitHub Actions | Free |

### Steps:
1. Fork the [AgentPay repo](https://github.com/kashyapshukla/agentPay)
2. Create free accounts on Neon.tech (Postgres) and Upstash (Redis)
3. Deploy to Render: connect your fork, set `DATABASE_URL`, `REDIS_URL`, and `JWT_SECRET` as environment variables
4. Start command: `uvicorn core.main:app --host 0.0.0.0 --port 10000`

The `render.yaml` blueprint file in the repository makes this even easier — Render can auto-detect and configure everything for you.
