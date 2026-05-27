# api/v1/endpoints/modelos.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from core.dependencies import get_current_user
from db.database import get_db
from models.user import User
from services.model_service import modelo
from schemas.prediccion import PrediccionRequest, PrediccionResponse
import repositories.demanda_repo as repo

router = APIRouter(prefix="/modelos", tags=["Modelos"])


@router.get("/estado")
async def estado_modelo():
    return modelo.get_status()


@router.get("/metricas")
async def metricas_modelo():
    if not modelo.is_ready:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                            detail="El modelo no está listo todavía.")
    return {
        "algoritmo": "Gradient Boosting Regressor",
        "parametros": {"n_estimators": 100, "learning_rate": 0.1,
                       "max_depth": 4, "random_state": 42},
        "features_categoricas": modelo.FEATURES_CATEGORICAS,
        "features_numericas": modelo.FEATURES_NUMERICAS,
        "target": modelo.TARGET,
    }


@router.get("/importancia-features")
async def importancia_features():
    try:
        return modelo.get_feature_importance()
    except RuntimeError as e:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=str(e))


@router.get("/catalogos")
async def catalogos(db: AsyncSession = Depends(get_db) ):
    return await repo.get_catalogos(db)


@router.post("/predecir", response_model=PrediccionResponse)
async def predecir(body: PrediccionRequest ):
    try:
        resultado = modelo.predecir(body.model_dump())
        return PrediccionResponse(
            demanda_estimada_mwh=resultado,
            unidad="MWh",
            modelo="Gradient Boosting Regressor",
        )
    except RuntimeError as e:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                            detail=f"Error en la predicción: {str(e)}")