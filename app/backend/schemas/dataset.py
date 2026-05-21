# schemas/dataset.py
from datetime import datetime
from pydantic import BaseModel


class StatsLimpieza(BaseModel):
    registros_originales: int
    registros_insertados: int
    registros_descartados: int
    detalle: list[str]


class MetricasModelo(BaseModel):
    r2: float
    mae: float
    rmse: float


class UploadResponse(BaseModel):
    mensaje: str
    archivo: str
    stats_limpieza: StatsLimpieza
    metricas_modelo: MetricasModelo


class HistorialItem(BaseModel):
    id: int
    nombre_archivo: str
    registros_totales: int
    registros_insertados: int
    registros_descartados: int
    r2_antes: float | None
    mae_antes: float | None
    r2_despues: float | None
    mae_despues: float | None
    subido_en: datetime

    model_config = {"from_attributes": True}