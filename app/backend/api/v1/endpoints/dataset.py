# api/v1/endpoints/dataset.py
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession
import pandas as pd
import io

from core.dependencies import require_admin
from db.database import get_db
from models.user import User
from models.dataset_upload import DatasetUpload
from services.pipeline import PipelineDemanda
from services.model_service import modelo
from schemas.dataset import UploadResponse, HistorialItem
import repositories.dataset_repo as repo

router = APIRouter(prefix="/dataset", tags=["Dataset"])


@router.post("/upload", response_model=UploadResponse, status_code=status.HTTP_201_CREATED)
async def upload_dataset(
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
    admin: User = Depends(require_admin),
):
    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Solo se aceptan archivos .csv")

    contenido = await file.read()
    try:
        df_crudo = pd.read_csv(io.BytesIO(contenido))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"Error al leer el CSV: {str(e)}")

    try:
        df_limpio, stats = PipelineDemanda().limpiar(df_crudo)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(e))

    if len(df_limpio) == 0:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                            detail="El CSV no contiene registros válidos después de la limpieza.")

    metricas_antes = modelo.last_metrics if modelo.is_ready else None

    await repo.insertar_registros(db, df_limpio)

    metricas_despues = await modelo.entrenar(db)

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
    await repo.registrar_upload(db, upload_log)

    return UploadResponse(
        mensaje="Dataset procesado y modelo re-entrenado exitosamente.",
        archivo=file.filename,
        stats_limpieza=stats,
        metricas_modelo=metricas_despues,
    )


@router.get("/historial", response_model=list[HistorialItem])
async def historial_uploads(
    db: AsyncSession = Depends(get_db),
    _: User = Depends(require_admin),
):
    return await repo.get_historial(db)