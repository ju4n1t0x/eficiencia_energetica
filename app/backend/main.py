from contextlib import asynccontextmanager
from fastapi import FastAPI
from db.database import engine, Base
from core.config import settings

from models import User


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Crear tablas al iniciar la aplicación
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    # Al cerrar liberar conexiones
    await engine.dispose()

app = FastAPI(
    title="Eficiencia Energética API",
    version="1.0.0",
    lifespan=lifespan,
)

@app.get("/health")
async def health_check():
    return {"status": "healthy"}