from pydantic import BaseModel


class PersonCreate(BaseModel):
    """Schema para crear una persona."""
    name: str
    passport: str
    age: int


class PersonUpdate(BaseModel):
    """Schema para actualizar una persona."""
    name: str | None = None
    passport: str | None = None
    age: int | None = None


class PersonResponse(BaseModel):
    """Schema de respuesta para una persona."""
    id: int
    name: str
    passport: str
    age: int

    model_config = {"from_attributes": True}