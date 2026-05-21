# api/v1/endpoints/eda.py
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.dependencies import get_current_user
from db.database import get_db
from models.user import User
import repositories.demanda_repo as repo

router = APIRouter(prefix="/eda", tags=["EDA"])


@router.get("/resumen")
async def resumen(db: AsyncSession = Depends(get_db), _: User = Depends(get_current_user)):
    return await repo.get_resumen(db)

@router.get("/demanda-mensual")
async def demanda_mensual(db: AsyncSession = Depends(get_db), _: User = Depends(get_current_user)):
    return await repo.get_demanda_mensual(db)

@router.get("/demanda-por-region")
async def demanda_por_region(db: AsyncSession = Depends(get_db), _: User = Depends(get_current_user)):
    return await repo.get_demanda_por_region(db)

@router.get("/demanda-por-provincia")
async def demanda_por_provincia(db: AsyncSession = Depends(get_db), _: User = Depends(get_current_user)):
    return await repo.get_demanda_por_provincia(db)

@router.get("/demanda-por-estacion")
async def demanda_por_estacion(db: AsyncSession = Depends(get_db), _: User = Depends(get_current_user)):
    return await repo.get_demanda_por_estacion(db)

@router.get("/demanda-por-categoria")
async def demanda_por_categoria(db: AsyncSession = Depends(get_db), _: User = Depends(get_current_user)):
    return await repo.get_demanda_por_categoria(db)

@router.get("/demanda-por-tipo-agente")
async def demanda_por_tipo_agente(db: AsyncSession = Depends(get_db), _: User = Depends(get_current_user)):
    return await repo.get_demanda_por_tipo_agente(db)