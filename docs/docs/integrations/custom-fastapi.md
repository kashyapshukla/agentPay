---
sidebar_position: 3
---

# Custom Python Backend (FastAPI / Django)

If you are not using a sophisticated AI framework and are explicitly building a raw Python backend triggering text generation manually (e.g. `openai.chat.completions.create`), you can rapidly deploy the raw **Python SDK** (`agentpay`) to meter your users or nested sub-systems explicitly.

## The Implementation

You install the native client explicitly using standard tooling: `pip install agentpay`.

```python
from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from agentpay import AgentPayClient
import openai

app = FastAPI()
client = AgentPayClient(api_key="agnt_live_sk_backend...")

class PromptRequest(BaseModel):
    query: str
    user_isolated_agent_id: str

@app.post("/generate")
def generate_text(req: PromptRequest):
    # 1. Meter the query constraints FIRST BEFORE Compute!
    try:
        # We charge 1 unit per generation
        client.meter_event(
            agent_id=req.user_isolated_agent_id,
            event_name="raw.llm.completion",
            units=1
        )
    except Exception as e:
        raise HTTPException(
            status_code=402, 
            detail="Agent Wallet strictly out of funds. Top up required."
        )

    # 2. Only run the expensive OpenAI call if AgentPay allowed the constraint!
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": req.query}]
    )
    
    return {"text": response.choices[0].message.content}
```

### Global Financial Guardrails
This architecture ensures that your native systems are globally load-balanced and strictly capped financially *before* they ever execute expensive compute tasks at the edge!
