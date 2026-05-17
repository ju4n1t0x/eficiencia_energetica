from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import select

from db.database import engine, Base, AsyncSessionLocal
from core.config import settings
from core.security import hash_password

from models import User, Rol
from services.model_service import modelo

# Routers
from api.v1.endpoints import auth as auth_router


async def seed_admin():
    """Crea el usuario admin por defecto si no existe."""
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(User).where(User.rol == Rol.admin)
        )
        if result.scalar_one_or_none() is None:
            admin = User(
                nombre="Administrador",
                mail=settings.ADMIN_MAIL,
                password=hash_password(settings.ADMIN_PASSWORD),
                rol=Rol.admin,
            )
            session.add(admin)
            await session.commit()
            print(f"[seed] Admin creado: {settings.ADMIN_MAIL}")
        else:
            print("[seed] Admin ya existe, se omite la creación.")


@asynccontextmanager
async def lifespan(app: FastAPI):
    # 1. Crear tablas
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    # 2. Seed admin
    await seed_admin()

    # 3. Cargar / entrenar modelo ML
    async with AsyncSessionLocal() as db:
        await modelo.init(db)

    yield

    # Al cerrar liberar conexiones
    await engine.dispose()

app = FastAPI(
    title="Eficiencia Energética API",
    description="API para análisis y predicción de demanda energética - CAMMESA",
    version="1.0.0",
    lifespan=lifespan,
        swagger_ui_oauth2_redirect_url=None,
    components={
        "securitySchemes": {
            "BearerAuth": {
                "type": "http",
                "scheme": "bearer",
                "bearerFormat": "JWT",
            }
        }
    },
)

# CORS para el frontend React/Vite
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(auth_router.router, prefix=settings.API_PREFIX)

@app.get("/health")
async def health_check():
    return {"status": "healthy"}