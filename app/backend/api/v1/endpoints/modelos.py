from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel

from core.dependencies import get_current_user
from db.database import get_db
from models.user import User
from services.model_service import modelo

router = APIRouter(prefix="/modelos", tags=["Modelos"])


class PrediccionRequest(BaseModel):
    anio: int
    mes: int
    tipo_agente: str
    region: str
    provincia: str
    categoria_area: str
    categoria_demanda: str
    categoria_tarifa: str
    estacion: str


@router.get("/estado")
async def estado_modelo(
    _: User = Depends(get_current_user),
):
    """Estado actual del modelo entrenado."""
    return modelo.get_status()


@router.get("/metricas")
async def metricas_modelo(
    _: User = Depends(get_current_user),
):
    """
    Métricas del modelo activo.
    Entrena temporalmente para obtener métricas actualizadas.
    """
    if not modelo.is_ready:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="El modelo no está listo todavía.",
        )
    return {
        "algoritmo": "Gradient Boosting Regressor",
        "parametros": {
            "n_estimators": 100,
            "learning_rate": 0.1,
            "max_depth": 4,
            "random_state": 42,
        },
        "features_categoricas": modelo.FEATURES_CATEGORICAS,
        "features_numericas": modelo.FEATURES_NUMERICAS,
        "target": modelo.TARGET,
    }


@router.get("/importancia-features")
async def importancia_features(
    _: User = Depends(get_current_user),
):
    """Importancia de cada feature en el modelo entrenado."""
    try:
        return modelo.get_feature_importance()
    except RuntimeError as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=str(e),
        )


@router.get("/catalogos")
async def catalogos(
    db: AsyncSession = Depends(get_db),
    _: User = Depends(get_current_user),
):
    """
    Devuelve los valores únicos de cada categoría.
    El frontend los usa para construir los dropdowns del formulario de predicción.
    """
    from sqlalchemy import text

    queries = {
        "tipo_agente": "SELECT DISTINCT tipo_agente FROM registros_demanda ORDER BY tipo_agente",
        "region": "SELECT DISTINCT region FROM registros_demanda ORDER BY region",
        "provincia": "SELECT DISTINCT provincia FROM registros_demanda ORDER BY provincia",
        "categoria_area": "SELECT DISTINCT categoria_area FROM registros_demanda ORDER BY categoria_area",
        "categoria_demanda": "SELECT DISTINCT categoria_demanda FROM registros_demanda ORDER BY categoria_demanda",
        "tarifa": "SELECT DISTINCT tarifa FROM registros_demanda ORDER BY tarifa",
        "categoria_tarifa": "SELECT DISTINCT categoria_tarifa FROM registros_demanda ORDER BY categoria_tarifa",
        "estacion": "SELECT DISTINCT estacion FROM registros_demanda ORDER BY estacion",
    }

    catalogos = {}
    for campo, query in queries.items():
        result = await db.execute(text(query))
        catalogos[campo] = [row[0] for row in result.fetchall()]

    return catalogos


@router.post("/predecir")
async def predecir(
    body: PrediccionRequest,
    _: User = Depends(get_current_user),
):
    """
    Predice la demanda en MWh dado un conjunto de features.
    """
    try:
        resultado = modelo.predecir(body.model_dump())
        return {
            "demanda_estimada_mwh": resultado,
            "unidad": "MWh",
            "modelo": "Gradient Boosting Regressor",
        }
    except RuntimeError as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=str(e),
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Error en la predicción: {str(e)}",
        )