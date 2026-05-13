from fastapi import APIRouter, Depends, HTTPException
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select

from src.database.database import get_session
from src.models import User
from src.services.user import UserService
from src.schemas.user import UserCreate, UserUpdate, UserResponse, UserBulkCreate

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/", response_model=list[UserResponse])
async def get_users(session: AsyncSession = Depends(get_session)) -> list[UserResponse]:
    """Obtener todos los usuarios."""
    service = UserService(session=session)
    users = await service.get_users()
    return users


@router.post("/", response_model=UserResponse, status_code=201)
async def create_user(
    user_data: UserCreate,
    session: AsyncSession = Depends(get_session),
) -> UserResponse:
    """Crear un nuevo usuario."""
    service = UserService(session=session)
    user = await service.create_user(name=user_data.name, email=user_data.email)
    if user is None:
        raise HTTPException(status_code=400, detail="Error al crear el usuario")
    return user


@router.post("/bulk-numpy", response_model=dict, status_code=201)
async def create_users_numpy(
    data: UserBulkCreate,
    session: AsyncSession = Depends(get_session),
) -> dict:
    """Crear usuarios usando numpy (vectorizado)."""
    service = UserService(session=session)
    result = await service.create_users_numpy(data.quantity)
    if not result:
        raise HTTPException(status_code=400, detail="Error al crear los usuarios")
    return result


@router.post("/bulk-for", response_model=dict, status_code=201)
async def create_users_for(
    data: UserBulkCreate,
    session: AsyncSession = Depends(get_session),
) -> dict:
    """Crear usuarios con un for simple."""
    service = UserService(session=session)
    result = await service.create_users_for(data.quantity)
    if not result:
        raise HTTPException(status_code=400, detail="Error al crear los usuarios")
    return result


@router.put("/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: int,
    user_data: UserUpdate,
    session: AsyncSession = Depends(get_session),
) -> UserResponse:
    """Actualizar un usuario existente."""
    statement = select(User).where(User.id == user_id)
    result = await session.exec(statement)
    user = result.first()
    if user is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    update_dict = user_data.model_dump(exclude_unset=True)
    for key, value in update_dict.items():
        setattr(user, key, value)
    service = UserService(session=session)
    updated_user = await service.update_user(user)
    if updated_user is None:
        raise HTTPException(status_code=400, detail="Error al actualizar el usuario")
    return updated_user


@router.delete("/{user_id}", response_model=UserResponse)
async def delete_user(
    user_id: int,
    session: AsyncSession = Depends(get_session),
) -> UserResponse:
    """Eliminar un usuario por su ID."""
    statement = select(User).where(User.id == user_id)
    result = await session.exec(statement)
    user = result.first()
    if user is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    service = UserService(session=session)
    deleted_user = await service.delete_user(user)
    if deleted_user is None:
        raise HTTPException(status_code=400, detail="Error al eliminar el usuario")
    return deleted_user