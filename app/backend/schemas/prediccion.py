from pydantic import BaseModel


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


class PrediccionResponse(BaseModel):
    demanda_estimada_mwh: float
    unidad: str
    modelo: str