import uuid
from datetime import datetime
from sqlalchemy import Column, String, Float, DateTime, ForeignKey, Boolean
from core.database.database import Base

def generate_uuid():
    return str(uuid.uuid4())

class AgentKey(Base):
    __tablename__ = "agent_keys"

    id = Column(String, primary_key=True, default=generate_uuid)
    key_prefix = Column(String, unique=True, index=True, nullable=False) # agnt_live_sk_...
    hashed_key = Column(String, nullable=False)
    scopes = Column(String, nullable=False) # comma-separated scopes
    created_at = Column(DateTime, default=datetime.utcnow)
    is_active = Column(Boolean, default=True)

class Wallet(Base):
    __tablename__ = "wallets"

    id = Column(String, primary_key=True, default=generate_uuid)
    agent_id = Column(String, ForeignKey("agent_keys.id"), nullable=False, unique=True)
    balance = Column(Float, default=0.0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class SpendAuditLog(Base):
    __tablename__ = "spend_audit_logs"

    id = Column(String, primary_key=True, default=generate_uuid)
    agent_id = Column(String, ForeignKey("agent_keys.id"), nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
    action = Column(String, nullable=False)
    amount = Column(Float, nullable=False)
    balance_after = Column(Float, nullable=False)

class MeteringBucket(Base):
    __tablename__ = "metering_buckets"

    id = Column(String, primary_key=True, default=generate_uuid)
    agent_id = Column(String, ForeignKey("agent_keys.id"), nullable=False, index=True)
    time_bucket = Column(DateTime, nullable=False, index=True)
    resolution = Column(String, nullable=False) # e.g., "hourly", "daily"
    total_units = Column(Float, default=0.0)
    total_cost = Column(Float, default=0.0)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
