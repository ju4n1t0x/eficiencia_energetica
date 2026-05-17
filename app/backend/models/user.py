import enum

from sqlalchemy import String, Integer, Enum
from sqlalchemy.orm import Mapped, mapped_column

from db.database import Base

class Rol(str, enum.Enum):
    admin = "admin"      # puede subir datasets y re-entrenar el modelo
    viewer = "viewer"    # solo puede visualizar EDA y predicciones

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    nombre: Mapped[str] = mapped_column(String(100), nullable=False)
    mail: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    rol: Mapped[Rol] = mapped_column(Enum(Rol), nullable=False, default=Rol.viewer)

