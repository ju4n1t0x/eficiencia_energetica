from pydantic import BaseModel, EmailStr
from models.user import Rol


# ---------- Request ----------

class RegisterRequest(BaseModel):
    nombre: str
    mail: EmailStr
    password: str
    rol: Rol = Rol.viewer


class LoginRequest(BaseModel):
    mail: EmailStr
    password: str


# ---------- Response ----------

class UserResponse(BaseModel):
    id: int
    nombre: str
    mail: EmailStr
    rol: Rol

    model_config = {"from_attributes": True}


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse