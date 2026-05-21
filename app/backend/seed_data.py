"""
Script de carga inicial de datos limpios a la DB.
Ahora pasa por el PipelineDemanda antes de insertar.
Ejecutar una sola vez: python seed_data.py
"""
import asyncio
import pandas as pd
from sqlalchemy import text
from db.database import AsyncSessionLocal, engine, Base
from models.registro_demanda import RegistroDemanda
from services.pipeline import PipelineDemanda
from core.config import settings        

BATCH_SIZE = 1000


async def seed():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    csv_path = settings.BASE_DATASET_PATH  
    print(f"Leyendo {csv_path}...")
    df_crudo = pd.read_csv(csv_path)
    print(f"Registros crudos: {len(df_crudo)}")

    pipeline = PipelineDemanda()
    df_limpio, stats = pipeline.limpiar(df_crudo)

    print(f"Registros después del pipeline: {len(df_limpio)}")
    print(f"Stats: {stats}")

    async with AsyncSessionLocal() as session:
        result = await session.execute(text("SELECT COUNT(*) FROM registros_demanda"))
        count = result.scalar()
        if count > 0:
            print(f"Ya existen {count} registros en la DB. Abortando para no duplicar.")
            return

        total = len(df_limpio)
        insertados = 0
        for i in range(0, total, BATCH_SIZE):
            batch = df_limpio.iloc[i:i + BATCH_SIZE]
            registros = [
                RegistroDemanda(**row.to_dict())
                for _, row in batch.iterrows()
            ]
            session.add_all(registros)
            await session.commit()
            insertados += len(registros)
            print(f"  Insertados {insertados}/{total}...")

    print(f"✅ Seed completo: {insertados} registros cargados y limpios.")


if __name__ == "__main__":
    asyncio.run(seed())