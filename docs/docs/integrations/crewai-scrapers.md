---
sidebar_position: 2
---

# CrewAI: Autonomous Web Scrapers

In [CrewAI](https://www.crewai.com/), you structure "Crews" to accomplish complex horizontal logic dynamically. If you build a Crew designed to autonomously surf the web and scrape proprietary portals, they inevitably hit paywalls, 402 errors, or Captcha-solving bypass limits.

AgentPay acts as their decentralized wallet. It empowers them to securely bypass proxy walls automatically using micro-transactions without you handing them your literal credit card.

## Integrating the Metering Tool

CrewAI agents map perfectly to LangChain tools natively. Since we already built `langchain-agentpay`, the integration is instantaneous out-of-the-box.

```python
from crewai import Agent, Task, Crew
from langchain_agentpay import AgentPayMeterTool

# 1. Initialize our Tool
pay_tool = AgentPayMeterTool(api_key="agnt_live_sk_crew...")

# 2. Assign the explicit tool to a Specific Crew Member
scraper_agent = Agent(
    role='Lead Data Scraper',
    goal='Scrape gated real estate records.',
    backstory='You are an elite data extraction agent with a strict financial spending limit.',
    tools=[pay_tool],
    allow_delegation=False
)

# 3. Give them instructions
task1 = Task(
    description='Find 5 listings. If you hit a proxy paywall, pay for 5 units of proxy bandwidth using your wallet.',
    expected_output='A clean CSV of listings.',
    agent=scraper_agent
)

crew = Crew(agents=[scraper_agent], tasks=[task1])
result = crew.kickoff()
```

### Dynamic Awareness
The CrewAI agent will dynamically realize it has purchasing power when it reads the `AgentPayMeterTool` description internally. It will negotiate with the proxy wall, spend precisely what it needs, and organically return the data!
