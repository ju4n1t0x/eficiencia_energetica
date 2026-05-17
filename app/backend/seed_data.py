"""
Script de carga inicial de datos limpios a la DB.
Ejecutar una sola vez: python seed_data.py
"""
import asyncio
import pandas as pd
from sqlalchemy import text
from db.database import AsyncSessionLocal, engine, Base
from models.registro_demanda import RegistroDemanda

CSV_PATH = "ml/base_dataset/demanda_limpia.csv"
BATCH_SIZE = 1000


async def seed():
    # Crear tablas si no existen
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    print(f"Leyendo {CSV_PATH}...")
    df = pd.read_csv(CSV_PATH)

    # Descartar columnas innecesarias
    df = df.drop(columns=["Unnamed: 0", "indice_tiempo"], errors="ignore")

    # Normalizar nombre de columna demanda
    if "demanda_MWh" in df.columns:
        df = df.rename(columns={"demanda_MWh": "demanda_mwh"})

    total = len(df)
    print(f"Total de registros a insertar: {total}")

    async with AsyncSessionLocal() as session:
        # Verificar si ya hay datos
        result = await session.execute(text("SELECT COUNT(*) FROM registros_demanda"))
        count = result.scalar()
        if count > 0:
            print(f"Ya existen {count} registros en la DB. Abortando para no duplicar.")
            return

        # Insertar en batches
        insertados = 0
        for i in range(0, total, BATCH_SIZE):
            batch = df.iloc[i:i + BATCH_SIZE]
            registros = [
                RegistroDemanda(**row.to_dict())
                for _, row in batch.iterrows()
            ]
            session.add_all(registros)
            await session.commit()
            insertados += len(registros)
            print(f"  Insertados {insertados}/{total}...")

    print(f"Seed completo: {insertados} registros cargados.")


if __name__ == "__main__":
    asyncio.run(seed())