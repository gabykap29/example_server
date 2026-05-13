from pydantic import BaseModel


class InventoryCreate(BaseModel):
    """Schema para crear un inventario."""
    name: str
    amount: int = 0


class InventoryUpdate(BaseModel):
    """Schema para actualizar un inventario."""
    name: str | None = None
    amount: int | None = None


class InventoryResponse(BaseModel):
    """Schema de respuesta para un inventario."""
    id: int
    name: str
    amount: int

    model_config = {"from_attributes": True}


class InventoryBulkCreate(BaseModel):
    """Schema para crear múltiples inventarios."""
    items: list[InventoryCreate]


class InventoryBulkFromFileCreate(BaseModel):
    """Schema para crear inventarios desde archivo JSON."""
    quantity: int