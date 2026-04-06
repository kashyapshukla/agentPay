---
sidebar_position: 4
---

# Deploy Core (100% Free Tier)

Deploying AgentPay publicly shouldn't drain your startup budget. Since AgentPay is open-source, we optimized the architecture so you can host the entire cluster for **$0/month** by intelligently routing the infrastructure to the best free tiers available in the modern cloud landscape.

## The $0 Blueprint

Instead of paying $15/mo for a monolithic DigitalOcean VPS or AWS EC2, you can split the stack natively:

1. **Frontend (Docusaurus)** ➔ **Vercel**
2. **PostgreSQL Database** ➔ **Neon.tech**
3. **Redis Stream Cache** ➔ **Upstash**
4. **FastAPI & Worker** ➔ **Render (Free Services)**

### 1. Host the Docs on Vercel
Vercel hosts static React frontend sites completely for free.
- Login to Vercel and import your AgentPay GitHub repository.
- Root Directory: `docs/`
- Build Command: `npm run build`
- Output Directory: `build`
Your setup documentation and homepage will be instantly live globally!

### 2. Procure Free Databases
1. Go to [Neon.tech](https://neon.tech) to provision an ultra-fast Serverless Postgres instance snippet for $0.
2. Go to [Upstash](https://upstash.com) to provision a Serverless Redis instance for $0 natively focused on high throughput streams.

### 3. Deploy the Backend via Render
Render offers free Web Services and Background Workers that automatically sleep when unused, making it perfect for OSS projects.

Connect your Render account to your GitHub repository and spin up two environments:

*   **Web Service (`AgentPay API`)**
    *   Start Command: `uvicorn core.main:app --host 0.0.0.0 --port 10000`
    *   Environment Variables: Paste the `JWT_SECRET`, the Neon `DATABASE_URL`, and Upstash `REDIS_URL`.
*   **Background Worker (`Aggregator`)**
    *   Start Command: `python -m core.workers.aggregator`
    *   Environment Variables: Paste the exact same Database connection keys.

By centralizing the databases to external stateless providers, your AgentPay web-services can dynamically scale up and down safely, without running a single VM! Your architecture is now permanently online, robust, and costs **absolutely nothing**.
