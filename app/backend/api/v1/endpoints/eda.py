from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text

from core.dependencies import get_current_user
from db.database import get_db
from models.user import User

router = APIRouter(prefix="/eda", tags=["EDA"])


@router.get("/resumen")
async def resumen(
    db: AsyncSession = Depends(get_db),
    _: User = Depends(get_current_user),
):
    """Estadísticas generales del dataset."""
    result = await db.execute(text("""
        SELECT
            COUNT(*)                        AS total_registros,
            ROUND(AVG(demanda_mwh)::numeric, 2)  AS demanda_promedio,
            ROUND(MIN(demanda_mwh)::numeric, 2)  AS demanda_minima,
            ROUND(MAX(demanda_mwh)::numeric, 2)  AS demanda_maxima,
            ROUND(SUM(demanda_mwh)::numeric, 2)  AS demanda_total,
            MIN(anio)                        AS anio_inicio,
            MAX(anio)                        AS anio_fin,
            COUNT(DISTINCT agente_nemo)      AS total_agentes,
            COUNT(DISTINCT provincia)        AS total_provincias
        FROM registros_demanda
    """))
    row = result.mappings().one()
    return dict(row)


@router.get("/demanda-mensual")
async def demanda_mensual(
    db: AsyncSession = Depends(get_db),
    _: User = Depends(get_current_user),
):
    """Demanda total por año y mes. Para graficar serie temporal."""
    result = await db.execute(text("""
        SELECT
            anio,
            mes,
            ROUND(SUM(demanda_mwh)::numeric, 2) AS demanda_total
        FROM registros_demanda
        GROUP BY anio, mes
        ORDER BY anio, mes
    """))
    rows = result.mappings().all()
    return [dict(r) for r in rows]


@router.get("/demanda-por-region")
async def demanda_por_region(
    db: AsyncSession = Depends(get_db),
    _: User = Depends(get_current_user),
):
    """Demanda total y promedio agrupada por región."""
    result = await db.execute(text("""
        SELECT
            region,
            ROUND(SUM(demanda_mwh)::numeric, 2)  AS demanda_total,
            ROUND(AVG(demanda_mwh)::numeric, 2)  AS demanda_promedio,
            COUNT(*)                              AS registros
        FROM registros_demanda
        GROUP BY region
        ORDER BY demanda_total DESC
    """))
    rows = result.mappings().all()
    return [dict(r) for r in rows]


@router.get("/demanda-por-provincia")
async def demanda_por_provincia(
    db: AsyncSession = Depends(get_db),
    _: User = Depends(get_current_user),
):
    """Demanda total agrupada por provincia."""
    result = await db.execute(text("""
        SELECT
            provincia,
            region,
            ROUND(SUM(demanda_mwh)::numeric, 2) AS demanda_total,
            COUNT(*)                             AS registros
        FROM registros_demanda
        GROUP BY provincia, region
        ORDER BY demanda_total DESC
    """))
    rows = result.mappings().all()
    return [dict(r) for r in rows]


@router.get("/demanda-por-estacion")
async def demanda_por_estacion(
    db: AsyncSession = Depends(get_db),
    _: User = Depends(get_current_user),
):
    """Demanda promedio por estación del año."""
    result = await db.execute(text("""
        SELECT
            estacion,
            ROUND(AVG(demanda_mwh)::numeric, 2) AS demanda_promedio,
            ROUND(SUM(demanda_mwh)::numeric, 2) AS demanda_total,
            COUNT(*)                             AS registros
        FROM registros_demanda
        GROUP BY estacion
        ORDER BY demanda_promedio DESC
    """))
    rows = result.mappings().all()
    return [dict(r) for r in rows]


@router.get("/demanda-por-categoria")
async def demanda_por_categoria(
    db: AsyncSession = Depends(get_db),
    _: User = Depends(get_current_user),
):
    """Demanda promedio por categoría de demanda."""
    result = await db.execute(text("""
        SELECT
            categoria_demanda,
            ROUND(AVG(demanda_mwh)::numeric, 2) AS demanda_promedio,
            ROUND(SUM(demanda_mwh)::numeric, 2) AS demanda_total,
            COUNT(*)                             AS registros
        FROM registros_demanda
        GROUP BY categoria_demanda
        ORDER BY demanda_total DESC
    """))
    rows = result.mappings().all()
    return [dict(r) for r in rows]


@router.get("/demanda-por-tipo-agente")
async def demanda_por_tipo_agente(
    db: AsyncSession = Depends(get_db),
    _: User = Depends(get_current_user),
):
    """Demanda promedio por tipo de agente."""
    result = await db.execute(text("""
        SELECT
            tipo_agente,
            ROUND(AVG(demanda_mwh)::numeric, 2) AS demanda_promedio,
            ROUND(SUM(demanda_mwh)::numeric, 2) AS demanda_total,
            COUNT(*)                             AS registros
        FROM registros_demanda
        GROUP BY tipo_agente
        ORDER BY demanda_total DESC
    """))
    rows = result.mappings().all()
    return [dict(r) for r in rows]