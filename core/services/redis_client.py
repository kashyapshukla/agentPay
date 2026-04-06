import os
import redis.asyncio as redis
import json

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")

redis_client = redis.from_url(REDIS_URL, decode_responses=True)

async def emit_metering_event(agent_id: str, event: str, units: int, metadata: dict):
    stream_name = "metering_events"
    payload = {
        "agent_id": agent_id,
        "event": event,
        "units": str(units),
        "metadata": json.dumps(metadata)
    }
    await redis_client.xadd(stream_name, payload)
