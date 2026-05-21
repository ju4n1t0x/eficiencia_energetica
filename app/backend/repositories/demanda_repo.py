from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text


async def get_resumen(db: AsyncSession) -> dict:
    result = await db.execute(text("""
        SELECT
            COUNT(*)                             AS total_registros,
            ROUND(AVG(demanda_mwh)::numeric, 2)  AS demanda_promedio,
            ROUND(MIN(demanda_mwh)::numeric, 2)  AS demanda_minima,
            ROUND(MAX(demanda_mwh)::numeric, 2)  AS demanda_maxima,
            ROUND(SUM(demanda_mwh)::numeric, 2)  AS demanda_total,
            MIN(anio)                            AS anio_inicio,
            MAX(anio)                            AS anio_fin,
            COUNT(DISTINCT agente_nemo)          AS total_agentes,
            COUNT(DISTINCT provincia)            AS total_provincias
        FROM registros_demanda
    """))
    return dict(result.mappings().one())


async def get_demanda_mensual(db: AsyncSession) -> list[dict]:
    result = await db.execute(text("""
        SELECT anio, mes,
               ROUND(SUM(demanda_mwh)::numeric, 2) AS demanda_total
        FROM registros_demanda
        GROUP BY anio, mes
        ORDER BY anio, mes
    """))
    return [dict(r) for r in result.mappings().all()]


async def get_demanda_por_region(db: AsyncSession) -> list[dict]:
    result = await db.execute(text("""
        SELECT region,
               ROUND(SUM(demanda_mwh)::numeric, 2) AS demanda_total,
               ROUND(AVG(demanda_mwh)::numeric, 2) AS demanda_promedio,
               COUNT(*)                             AS registros
        FROM registros_demanda
        GROUP BY region
        ORDER BY demanda_total DESC
    """))
    return [dict(r) for r in result.mappings().all()]


async def get_demanda_por_provincia(db: AsyncSession) -> list[dict]:
    result = await db.execute(text("""
        SELECT provincia, region,
               ROUND(SUM(demanda_mwh)::numeric, 2) AS demanda_total,
               COUNT(*)                             AS registros
        FROM registros_demanda
        GROUP BY provincia, region
        ORDER BY demanda_total DESC
    """))
    return [dict(r) for r in result.mappings().all()]


async def get_demanda_por_estacion(db: AsyncSession) -> list[dict]:
    result = await db.execute(text("""
        SELECT estacion,
               ROUND(AVG(demanda_mwh)::numeric, 2) AS demanda_promedio,
               ROUND(SUM(demanda_mwh)::numeric, 2) AS demanda_total,
               COUNT(*)                             AS registros
        FROM registros_demanda
        GROUP BY estacion
        ORDER BY demanda_promedio DESC
    """))
    return [dict(r) for r in result.mappings().all()]


async def get_demanda_por_categoria(db: AsyncSession) -> list[dict]:
    result = await db.execute(text("""
        SELECT categoria_demanda,
               ROUND(AVG(demanda_mwh)::numeric, 2) AS demanda_promedio,
               ROUND(SUM(demanda_mwh)::numeric, 2) AS demanda_total,
               COUNT(*)                             AS registros
        FROM registros_demanda
        GROUP BY categoria_demanda
        ORDER BY demanda_total DESC
    """))
    return [dict(r) for r in result.mappings().all()]


async def get_demanda_por_tipo_agente(db: AsyncSession) -> list[dict]:
    result = await db.execute(text("""
        SELECT tipo_agente,
               ROUND(AVG(demanda_mwh)::numeric, 2) AS demanda_promedio,
               ROUND(SUM(demanda_mwh)::numeric, 2) AS demanda_total,
               COUNT(*)                             AS registros
        FROM registros_demanda
        GROUP BY tipo_agente
        ORDER BY demanda_total DESC
    """))
    return [dict(r) for r in result.mappings().all()]


# ── Catálogos para dropdowns del formulario de predicción ──────────────────

_CAMPOS_CATALOGO = [
    "tipo_agente", "region", "provincia", "categoria_area",
    "categoria_demanda", "tarifa", "categoria_tarifa", "estacion",
]

async def get_catalogos(db: AsyncSession) -> dict[str, list[str]]:
    catalogos = {}
    for campo in _CAMPOS_CATALOGO:
        result = await db.execute(
            text(f"SELECT DISTINCT {campo} FROM registros_demanda ORDER BY {campo}")
        )
        catalogos[campo] = [row[0] for row in result.fetchall()]
    return catalogos