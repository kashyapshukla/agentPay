import os
import ssl
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import declarative_base

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+asyncpg://agentpay:agentpay_password@localhost:5432/agentpay_db")

# Render/Neon provide postgresql:// URLs — convert to asyncpg driver
if DATABASE_URL.startswith("postgresql://"):
    DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://", 1)

# Strip query params that asyncpg doesn't support (e.g. channel_binding, sslmode)
_parsed = urlparse(DATABASE_URL)
_params = parse_qs(_parsed.query)
_unsupported = {"channel_binding", "sslmode"}
_clean_params = {k: v[0] for k, v in _params.items() if k not in _unsupported}
_clean_url = urlunparse(_parsed._replace(query=urlencode(_clean_params)))

# Detect if we need SSL (any cloud-hosted DB)
_needs_ssl = "neon.tech" in DATABASE_URL or "render.com" in DATABASE_URL or "supabase" in DATABASE_URL
_connect_args = {}
if _needs_ssl:
    _ssl_ctx = ssl.create_default_context()
    _ssl_ctx.check_hostname = False
    _ssl_ctx.verify_mode = ssl.CERT_NONE
    _connect_args["ssl"] = _ssl_ctx

engine = create_async_engine(_clean_url, echo=False, pool_size=5, connect_args=_connect_args)
AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
Base = declarative_base()

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
