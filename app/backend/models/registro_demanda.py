from sqlalchemy import Integer, String, Float, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column

from db.database import Base


class RegistroDemanda(Base):
    __tablename__ = "registros_demanda"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    # Temporales
    anio: Mapped[int] = mapped_column(Integer, nullable=False, index=True)
    mes: Mapped[int] = mapped_column(Integer, nullable=False, index=True)
    estacion: Mapped[str] = mapped_column(String(20), nullable=False)

    # Agente
    agente_nemo: Mapped[str] = mapped_column(String(50), nullable=False)
    agente_descripcion: Mapped[str] = mapped_column(String(255), nullable=False)
    tipo_agente: Mapped[str] = mapped_column(String(50), nullable=False)

    # Geografía
    region: Mapped[str] = mapped_column(String(100), nullable=False)
    provincia: Mapped[str] = mapped_column(String(100), nullable=False)

    # Categorías
    categoria_area: Mapped[str] = mapped_column(String(100), nullable=False)
    categoria_demanda: Mapped[str] = mapped_column(String(100), nullable=False)
    tarifa: Mapped[str] = mapped_column(String(100), nullable=False)
    categoria_tarifa: Mapped[str] = mapped_column(String(100), nullable=False)

    # Variable objetivo
    demanda_mwh: Mapped[float] = mapped_column(Float, nullable=False)

    # Auditoría - se llena automáticamente
    cargado_en: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )