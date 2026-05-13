from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    """Schema para crear un usuario."""
    name: str
    email: str


class UserUpdate(BaseModel):
    """Schema para actualizar un usuario."""
    name: str | None = None
    email: str | None = None


class UserResponse(BaseModel):
    """Schema de respuesta para un usuario."""
    id: int
    name: str
    email: str

    model_config = {"from_attributes": True}


class UserBulkCreate(BaseModel):
    """Schema para crear usuarios en bulk."""
    quantity: int