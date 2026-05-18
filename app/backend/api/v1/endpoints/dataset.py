from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession
import pandas as pd
import io

from core.dependencies import require_admin
from db.database import get_db
from models.user import User
from models.dataset_upload import DatasetUpload
from models.registro_demanda import RegistroDemanda
from services.pipeline import PipelineDemanda
from services.model_service import modelo

router = APIRouter(prefix="/dataset", tags=["Dataset"])

BATCH_SIZE = 1000


@router.post("/upload", status_code=status.HTTP_201_CREATED)
async def upload_dataset(
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
    admin: User = Depends(require_admin),
):
    """
    Sube un nuevo CSV de demanda energética.
    Solo admins. Limpia los datos, los inserta en la DB y re-entrena el modelo.
    """
    # 1. Validar extensión
    if not file.filename.endswith(".csv"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Solo se aceptan archivos .csv",
        )

    # 2. Leer el archivo
    contenido = await file.read()
    try:
        df_crudo = pd.read_csv(io.BytesIO(contenido))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error al leer el CSV: {str(e)}",
        )

    # 3. Limpiar con el pipeline
    try:
        pipeline = PipelineDemanda()
        df_limpio, stats = pipeline.limpiar(df_crudo)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(e),
        )

    if len(df_limpio) == 0:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="El CSV no contiene registros válidos después de la limpieza.",
        )

    # 4. Guardar métricas actuales del modelo antes de re-entrenar
    metricas_antes = None
    if modelo.is_ready:
        # Las guardamos del último entrenamiento — por ahora None hasta tener historial
        metricas_antes = {"r2": None, "mae": None}

    # 5. Insertar registros limpios en la DB en batches
    total = len(df_limpio)
    insertados = 0
    for i in range(0, total, BATCH_SIZE):
        batch = df_limpio.iloc[i:i + BATCH_SIZE]
        registros = [
            RegistroDemanda(**row.to_dict())
            for _, row in batch.iterrows()
        ]
        db.add_all(registros)
        await db.commit()
        insertados += len(registros)

    # 6. Re-entrenar el modelo con todos los datos acumulados
    metricas_despues = await modelo.entrenar(db)

    # 7. Registrar la carga en el historial
    upload_log = DatasetUpload(
        usuario_id=admin.id,
        nombre_archivo=file.filename,
        registros_totales=stats["registros_originales"],
        registros_insertados=stats["registros_insertados"],
        registros_descartados=stats["registros_descartados"],
        r2_antes=metricas_antes["r2"] if metricas_antes else None,
        mae_antes=metricas_antes["mae"] if metricas_antes else None,
        r2_despues=metricas_despues["r2"],
        mae_despues=metricas_despues["mae"],
    )
    db.add(upload_log)
    await db.commit()

    return {
        "mensaje": "Dataset procesado y modelo re-entrenado exitosamente.",
        "archivo": file.filename,
        "stats_limpieza": stats,
        "metricas_modelo": metricas_despues,
    }


@router.get("/historial", status_code=status.HTTP_200_OK)
async def historial_uploads(
    db: AsyncSession = Depends(get_db),
    admin: User = Depends(require_admin),
):
    """Devuelve el historial de cargas de datasets. Solo admins."""
    from sqlalchemy import select
    result = await db.execute(
        select(DatasetUpload).order_by(DatasetUpload.subido_en.desc())
    )
    uploads = result.scalars().all()
    return uploads