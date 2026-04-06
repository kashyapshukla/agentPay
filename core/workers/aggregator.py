import asyncio
import json
from datetime import datetime
from sqlalchemy.future import select

from core.database.database import AsyncSessionLocal, Base, engine
from core.database.models import MeteringBucket
from core.services.redis_client import redis_client

import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

STREAM_NAME = "metering_events"
GROUP_NAME = "aggregator_group"

async def init_redis_group():
    try:
        await redis_client.xgroup_create(STREAM_NAME, GROUP_NAME, mkstream=True)
    except Exception as e:
        if "BUSYGROUP" not in str(e):
            logger.error(f"Error creating CG: {e}")

async def process_event(event_id, event_data: dict):
    agent_id = event_data.get("agent_id")
    units = float(event_data.get("units", 0.0))
    cost = units * 0.001

    now = datetime.utcnow()
    hourly_bucket = now.replace(minute=0, second=0, microsecond=0)
    daily_bucket = now.replace(hour=0, minute=0, second=0, microsecond=0)

    async with AsyncSessionLocal() as db:
        for resolution, time_bucket in [("hourly", hourly_bucket), ("daily", daily_bucket)]:
            result = await db.execute(
                select(MeteringBucket)
                .where(MeteringBucket.agent_id == agent_id,
                       MeteringBucket.resolution == resolution,
                       MeteringBucket.time_bucket == time_bucket)
                .with_for_update()
            )
            bucket = result.scalars().first()
            if not bucket:
                bucket = MeteringBucket(
                    agent_id=agent_id,
                    time_bucket=time_bucket,
                    resolution=resolution,
                    total_units=units,
                    total_cost=cost
                )
                db.add(bucket)
            else:
                bucket.total_units += units
                bucket.total_cost += cost
        await db.commit()
    logger.info(f"Aggregated event {event_id} for agent {agent_id} units:{units} cost:{cost}.")

async def run_worker():
    logger.info("Initializing Aggregator Worker...")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    await init_redis_group()
    logger.info("Listening for metering events...")

    while True:
        try:
            messages = await redis_client.xreadgroup(GROUP_NAME, "worker-1", {STREAM_NAME: ">"}, count=10, block=5000)
            if not messages:
                continue
            
            for stream, events in messages:
                for event_id, event_data in events:
                    await process_event(event_id, event_data)
                    await redis_client.xack(STREAM_NAME, GROUP_NAME, event_id)
        except Exception as e:
            logger.error(f"Worker Error: {e}")
            await asyncio.sleep(5)

if __name__ == "__main__":
    asyncio.run(run_worker())
