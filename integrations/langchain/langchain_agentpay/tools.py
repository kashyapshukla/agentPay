from typing import Optional, Type, Any
from langchain_core.tools import BaseTool
from pydantic import BaseModel, Field
from agentpay.client import AgentPayClient

class AgentPayMeterInput(BaseModel):
    agent_id: str = Field(description="The Agent ID making the payment/metering.")
    event_name: str = Field(description="The name of the action or API event being billed.")
    units: int = Field(description="The number of usage units to meter/charge.")
    metadata: Optional[dict] = Field(default=None, description="Optional metadata containing extra context.")

class AgentPayMeterTool(BaseTool):
    name: str = "agentpay_meter"
    description: str = "Use this tool to track usage, log metering events, or spend money out of your wallet for specific external APIs or tasks."
    args_schema: Type[BaseModel] = AgentPayMeterInput
    api_key: str = Field(..., description="The live Agent API key.")
    base_url: str = Field(default="http://localhost:8000")
    
    _client: Any = None
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._client = AgentPayClient(api_key=self.api_key, base_url=self.base_url)

    def _run(self, agent_id: str, event_name: str, units: int, metadata: dict = None) -> str:
        try:
            res = self._client.meter_event(agent_id=agent_id, event_name=event_name, units=units, metadata=metadata)
            return f"Successfully logged meter event '{event_name}' for {units} units. Cost incurred: ${res.get('cost_incurred')}."
        except Exception as e:
            return f"Error executing AgentPay metering: {str(e)}"
