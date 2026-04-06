from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from pydantic import BaseModel

from core.database.database import get_db
from core.database.models import Wallet, SpendAuditLog
from core.services.redis_client import emit_metering_event

router = APIRouter(prefix="/v1/billing", tags=["billing"])

class MeterEventRequest(BaseModel):
    agent_id: str
    event: str
    units: int
    metadata: dict = {}

class WalletTopupRequest(BaseModel):
    amount: float

@router.post("/meter")
async def meter_event(req: MeterEventRequest, db: AsyncSession = Depends(get_db)):
    # Async emit to Redis stream
    await emit_metering_event(req.agent_id, req.event, req.units, req.metadata)
    
    # Calculate cost per unit (dummy pricing for MVP)
    # real system would cross-reference event to price catalog
    cost = req.units * 0.001 
    
    if cost > 0:
        # Atomic debit using row locking
        result = await db.execute(
            select(Wallet).where(Wallet.agent_id == req.agent_id).with_for_update()
        )
        wallet = result.scalars().first()
        
        if not wallet:
            raise HTTPException(status_code=404, detail="Wallet not found")
            
        if wallet.balance < cost:
            raise HTTPException(status_code=402, detail="Insufficient funds")
            
        wallet.balance -= cost
        
        audit_log = SpendAuditLog(
            agent_id=req.agent_id,
            action=req.event,
            amount=cost,
            balance_after=wallet.balance
        )
        db.add(audit_log)
        await db.commit()
        
    return {"status": "recorded", "cost_incurred": cost}

@router.post("/wallets/{agent_id}/topup")
async def topup_wallet(agent_id: str, req: WalletTopupRequest, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Wallet).where(Wallet.agent_id == agent_id).with_for_update()
    )
    wallet = result.scalars().first()
    
    if not wallet:
        raise HTTPException(status_code=404, detail="Wallet not found")
        
    wallet.balance += req.amount
    
    audit_log = SpendAuditLog(
        agent_id=agent_id,
        action="wallet.topup",
        amount=req.amount,
        balance_after=wallet.balance
    )
    db.add(audit_log)
    await db.commit()
    
    return {"agent_id": agent_id, "new_balance": wallet.balance}
