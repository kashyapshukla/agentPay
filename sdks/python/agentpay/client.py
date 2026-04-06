import httpx
from typing import Optional, Dict, Any

class AgentPayClient:
    def __init__(self, api_key: str, base_url: str = "http://localhost:8000"):
        self.api_key = api_key
        self.base_url = base_url
        self._jwt_token: Optional[str] = None
        self._authenticate()

    def _authenticate(self):
        with httpx.Client(base_url=self.base_url) as client:
            res = client.post("/v1/auth/token", json={"api_key": self.api_key})
            if res.status_code != 200:
                raise Exception(f"Failed to authenticate: {res.text}")
            self._jwt_token = res.json().get("access_token")

    def meter_event(self, agent_id: str, event_name: str, units: int, metadata: Dict[str, Any] = None) -> Dict[str, Any]:
        """Meter an event, natively deducting from the agent's budget."""
        metadata = metadata or {}
        payload = {
            "agent_id": agent_id,
            "event": event_name,
            "units": units,
            "metadata": metadata
        }
        with httpx.Client(base_url=self.base_url) as client:
            headers = {"Authorization": f"Bearer {self._jwt_token}"} if self._jwt_token else {}
            res = client.post("/v1/billing/meter", json=payload, headers=headers)
            res.raise_for_status()
            return res.json()

    def topup_wallet(self, agent_id: str, amount: float) -> Dict[str, Any]:
        """Add funds to the wallet."""
        payload = {"amount": amount}
        with httpx.Client(base_url=self.base_url) as client:
            headers = {"Authorization": f"Bearer {self._jwt_token}"} if self._jwt_token else {}
            res = client.post(f"/v1/billing/wallets/{agent_id}/topup", json=payload, headers=headers)
            res.raise_for_status()
            return res.json()
