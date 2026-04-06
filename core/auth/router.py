import os
import uuid
from datetime import datetime, timedelta
import jwt
import bcrypt
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from core.database.database import get_db
from core.database.models import AgentKey, Wallet
from pydantic import BaseModel

router = APIRouter(prefix="/v1/auth", tags=["auth"])

JWT_SECRET = os.getenv("JWT_SECRET", "supersecretjwtkey_change_me_in_prod")

class CreateKeyRequest(BaseModel):
    scopes: list[str] = ["pay:send", "data:read"]

class IssueTokenRequest(BaseModel):
    api_key: str

def get_password_hash(password):
    pwd_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(pwd_bytes, salt).decode('utf-8')

def verify_password(plain_password, hashed_password):
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

@router.post("/keys", status_code=status.HTTP_201_CREATED)
async def create_agent_key(req: CreateKeyRequest, db: AsyncSession = Depends(get_db)):
    raw_key = f"agnt_live_sk_{uuid.uuid4().hex}"
    hashed_key = get_password_hash(raw_key)
    
    agent_key = AgentKey(
        key_prefix=raw_key[:20],
        hashed_key=hashed_key,
        scopes=",".join(req.scopes)
    )
    db.add(agent_key)
    await db.flush() # To get the ID
    
    # Pre-fund wallet with 0 balance
    wallet = Wallet(agent_id=agent_key.id, balance=0.0)
    db.add(wallet)
    
    await db.commit()
    
    return {"api_key": raw_key, "agent_id": agent_key.id}

@router.post("/token")
async def issue_token(req: IssueTokenRequest, db: AsyncSession = Depends(get_db)):
    key_prefix = req.api_key[:20]
    result = await db.execute(select(AgentKey).where(AgentKey.key_prefix == key_prefix))
    agent_key = result.scalars().first()
    
    if not agent_key or not verify_password(req.api_key, agent_key.hashed_key):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid API key")
        
    payload = {
        "sub": agent_key.id,
        "scopes": agent_key.scopes,
        "exp": datetime.utcnow() + timedelta(hours=1)
    }
    token = jwt.encode(payload, JWT_SECRET, algorithm="HS256")
    return {"access_token": token, "token_type": "bearer"}
