from sqlalchemy import Integer, String, Float, DateTime, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.database import Base


class DatasetUpload(Base):
    __tablename__ = "dataset_uploads"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    # Quién subió el archivo
    usuario_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id"), nullable=False
    )

    # Info del archivo
    nombre_archivo: Mapped[str] = mapped_column(String(255), nullable=False)
    registros_totales: Mapped[int] = mapped_column(Integer, nullable=False)
    registros_insertados: Mapped[int] = mapped_column(Integer, nullable=False)
    registros_descartados: Mapped[int] = mapped_column(Integer, nullable=False)

    # Métricas del modelo antes del re-entrenamiento
    r2_antes: Mapped[float | None] = mapped_column(Float, nullable=True)
    mae_antes: Mapped[float | None] = mapped_column(Float, nullable=True)

    # Métricas del modelo después del re-entrenamiento
    r2_despues: Mapped[float | None] = mapped_column(Float, nullable=True)
    mae_despues: Mapped[float | None] = mapped_column(Float, nullable=True)

    # Auditoría
    subido_en: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    # Relación con User
    usuario: Mapped["User"] = relationship("User", lazy="selectin")