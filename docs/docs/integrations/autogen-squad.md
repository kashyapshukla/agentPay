---
sidebar_position: 1
---

# Microsoft AutoGen: Multi-Agent Squads

When working with Microsoft AutoGen, you often have a **GroupChat** comprising multiple agents working together (e.g., a Coder, a Reviewer, and a Planner). 

AgentPay allows you to assign *independent budgets* to each agent to strictly monitor who is burning your LLM tokens!

## The Workflow

1. **Issue Independent Keys:** Give the Coder its own AgentPay Key, and the Planner its own AgentPay Key.
2. **Fund The Wallets:** Pre-fund the Coder with `$2.00` and the Planner with `$0.50` (since planning is cheap).
3. **Register Custom Tools:** AutoGen executes tools natively. We inject the Python Base SDK directly into the Coder.

```python
from autogen import AssistantAgent, UserProxyAgent
from agentpay import AgentPayClient

# Initialize our native Python Client
coder_pay_client = AgentPayClient(api_key="agnt_live_sk_coder...")

def report_code_execution(tokens_used: int) -> str:
    """Logs the cost of executing generated code against the wallet."""
    res = coder_pay_client.meter_event(
        agent_id="coder-agent-id", 
        event_name="code.execution", 
        units=tokens_used
    )
    return "Execution logged. Wallet balance successfully tracked."

# Attach to agent
coder = AssistantAgent(
    name="Coder",
    llm_config={"functions": [report_code_execution]}
)
```

### The Financial Safety Net
By siloing the wallets, if the Coder enters an infinite loop and hallucinates 50 bad scripts sequentially, it will simply **fail out safely** and lock down after automatically hitting its `$2.00` hard limit, saving your OpenAI bill instantly!
