from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from core.security import hash_password, verify_password, create_access_token
from core.dependencies import get_current_user, require_admin
from db.database import get_db

from models.user import User, Rol
from schemas.auth import RegisterRequest, LoginRequest, TokenResponse, UserResponse

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/registro", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def registro(
    body: RegisterRequest,
    db: AsyncSession = Depends(get_db),
    _admin: User = Depends(require_admin),
):
    """Crea un nuevo usuario. Requiere ser admin."""
    existing = await db.execute(select(User).where(User.mail == body.mail))
    if existing.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ya existe un usuario con ese mail",
        )

    user = User(
        nombre=body.nombre,
        mail=body.mail,
        password=hash_password(body.password),
        rol=body.rol,
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user


@router.post("/login", response_model=TokenResponse)
async def login(
    body: LoginRequest,
    db: AsyncSession = Depends(get_db),
):
    """Login con mail y password. Devuelve JWT + datos del usuario."""
    result = await db.execute(select(User).where(User.mail == body.mail))
    user = result.scalar_one_or_none()

    if not user or not verify_password(body.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales inválidas",
        )

    token = create_access_token({"sub": str(user.id), "rol": user.rol})
    return TokenResponse(
        access_token=token,
        user=UserResponse.model_validate(user),
    )


@router.get("/me", response_model=UserResponse)
async def me(current_user: User = Depends(get_current_user)):
    """Devuelve los datos del usuario autenticado."""
    return current_user