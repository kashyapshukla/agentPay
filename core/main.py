from fastapi import FastAPI
from core.database.database import engine, Base
from core.auth.router import router as auth_router
from core.billing.router import router as billing_router
from core.gateway.router import router as gateway_router

app = FastAPI(title="AgentPay API", description="B2A API Platform MVP", version="1.0.0")

@app.on_event("startup")
async def startup_event():
    async with engine.begin() as conn:
        # Create tables as requested for the MVP instead of Alembic
        await conn.run_sync(Base.metadata.create_all)

app.include_router(auth_router)
app.include_router(billing_router)
app.include_router(gateway_router)

@app.get("/")
def root():
    return {"message": "Welcome to AgentPay! Documentation available at /docs"}
