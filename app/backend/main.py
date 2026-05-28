from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import select, text
import pandas as pd

from db.database import engine, Base, AsyncSessionLocal
from core.config import settings
from core.security import hash_password

from models import User, Rol
from models.registro_demanda import RegistroDemanda
from services.model_service import modelo
from services.pipeline import PipelineDemanda

# Routers
from api.v1.endpoints import auth as auth_router
from api.v1.endpoints import dataset as dataset_router
from api.v1.endpoints import eda as eda_router
from api.v1.endpoints import modelos as modelos_router


async def seed_admin():
    """Crea el usuario admin por defecto si no existe."""
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(User).where(User.rol == Rol.admin))
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


async def seed_dataset():
    """Carga el dataset CSV en la DB si está vacía."""
    BATCH_SIZE = 1000

    async with AsyncSessionLocal() as session:
        result = await session.execute(text("SELECT COUNT(*) FROM registros_demanda"))
        count = result.scalar()
        if count > 0:
            print(
                f"[seed] Ya existen {count} registros en la DB. Abortando para no duplicar."
            )
            return

    csv_path = settings.BASE_DATASET_PATH
    print(f"[seed] Leyendo {csv_path}...")
    df_crudo = pd.read_csv(csv_path)
    print(f"[seed] Registros crudos: {len(df_crudo)}")

    pipeline = PipelineDemanda()
    df_limpio, stats = pipeline.limpiar(df_crudo)
    print(f"[seed] Registros después del pipeline: {len(df_limpio)}")
    print(f"[seed] Stats: {stats}")

    async with AsyncSessionLocal() as session:
        total = len(df_limpio)
        insertados = 0
        for i in range(0, total, BATCH_SIZE):
            batch = df_limpio.iloc[i : i + BATCH_SIZE]
            registros = [RegistroDemanda(**dict(row)) for _, row in batch.iterrows()]
            session.add_all(registros)
            await session.commit()
            insertados += len(registros)
            print(f"[seed]   Insertados {insertados}/{total}...")

    print(f"[seed] Dataset completo: {insertados} registros cargados y limpios.")


@asynccontextmanager
async def lifespan(app: FastAPI):
    # 1. Crear tablas
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    # 2. Seed admin
    await seed_admin()

    # 3. Seed dataset
    await seed_dataset()

    # 4. Cargar / entrenar modelo ML
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
app.include_router(dataset_router.router, prefix=settings.API_PREFIX)
app.include_router(eda_router.router, prefix=settings.API_PREFIX)
app.include_router(modelos_router.router, prefix=settings.API_PREFIX)


@app.get("/health")
async def health_check():
    return {"status": "healthy"}
