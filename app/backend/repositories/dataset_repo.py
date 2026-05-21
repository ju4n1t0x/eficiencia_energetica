import pandas as pd
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from models.registro_demanda import RegistroDemanda
from models.dataset_upload import DatasetUpload

BATCH_SIZE = 1_000


async def insertar_registros(db: AsyncSession, df: pd.DataFrame) -> int:
    """Inserta el DataFrame limpio en la DB en batches. Devuelve cantidad insertada."""
    total = len(df)
    insertados = 0
    for i in range(0, total, BATCH_SIZE):
        batch = df.iloc[i : i + BATCH_SIZE]
        registros = [RegistroDemanda(**row.to_dict()) for _, row in batch.iterrows()]
        db.add_all(registros)
        await db.commit()
        insertados += len(registros)
    return insertados


async def registrar_upload(db: AsyncSession, upload: DatasetUpload) -> DatasetUpload:
    """Persiste el log de una carga de dataset."""
    db.add(upload)
    await db.commit()
    await db.refresh(upload)
    return upload


async def get_historial(db: AsyncSession) -> list[DatasetUpload]:
    """Devuelve todos los uploads ordenados por fecha descendente."""
    result = await db.execute(
        select(DatasetUpload).order_by(DatasetUpload.subido_en.desc())
    )
    return result.scalars().all()