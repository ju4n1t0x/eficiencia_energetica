from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase
from core.config import settings

# Motor async - usa asyncpg como drive
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,
    pool_size=10,
    max_overflow=20,
)

# Fabrica de sesiones
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

# HBase para todos los modelos ORM
class Base(DeclarativeBase):
    pass


# Dependencia para FastAPI - inyecta la sesion en cada request
async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.close()
        except Exception:
            await session.rollback()
            raise 


