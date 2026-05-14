import json
import math
from pathlib import Path

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from src.database.database import get_session
from src.models import Inventory
from src.services.inventory import InventoryService
from src.schemas.inventory import InventoryCreate, InventoryUpdate, InventoryBulkFromFileCreate

router = APIRouter(prefix="/inventory", tags=["inventory"])


@router.get("/")
async def get_inventory(
    session: AsyncSession = Depends(get_session),
) -> dict:
    """Obtener todos los inventarios. 
        ordenamiento utilizado .sort (timsort)
    """
    service = InventoryService(session=session)
    inventory = await service.get_inventory()
    return inventory

@router.get("/all")
async def get_inventory_all(
    session: AsyncSession = Depends(get_session),
) -> dict:
    """Obtener todos los inventarios.
        ordenamiento delegando a la base de datos. 
    """
    service = InventoryService(session=session)
    inventory = await service.get_inventory_all()
    return inventory


@router.post("/", status_code=201)
async def create_inventory(
    inventory_data: InventoryCreate,
    session: AsyncSession = Depends(get_session),
):
    """Crear un nuevo inventario."""
    service = InventoryService(session=session)
    item = await service.create_inventory(
        name=inventory_data.name,
        amount=inventory_data.amount,
    )
    if item is None:
        raise HTTPException(status_code=400, detail="Error al crear el inventario")
    return item


@router.put("/{inventory_id}",)
async def update_inventory(
    inventory_id: int,
    inventory_data: InventoryUpdate,
    session: AsyncSession = Depends(get_session),
):
    """Actualizar un inventario existente."""
    statement = select(Inventory).where(Inventory.id == inventory_id)
    result = await session.exec(statement)
    item = result.first()
    if item is None:
        raise HTTPException(status_code=404, detail="Inventario no encontrado")
    update_dict = inventory_data.model_dump(exclude_unset=True)
    for key, value in update_dict.items():
        setattr(item, key, value)
    service = InventoryService(session=session)
    updated_item = await service.update_inventory(item)
    if updated_item is None:
        raise HTTPException(status_code=400, detail="Error al actualizar el inventario")
    return updated_item


@router.delete("/{inventory_id}",)
async def delete_inventory(
    inventory_id: int,
    session: AsyncSession = Depends(get_session),
):
    """Eliminar un inventario por su ID."""
    statement = select(Inventory).where(Inventory.id == inventory_id)
    result = await session.exec(statement)
    item = result.first()
    if item is None:
        raise HTTPException(status_code=404, detail="Inventario no encontrado")
    service = InventoryService(session=session)
    deleted_item = await service.delete_inventory(item)
    if deleted_item is None:
        raise HTTPException(status_code=400, detail="Error al eliminar el inventario")
    return deleted_item


@router.post("/bulk", status_code=201)
async def create_bulk_from_file(
    data: InventoryBulkFromFileCreate,
    session: AsyncSession = Depends(get_session),
):
    """Crear inventarios desde archivo JSON de forma síncrona (O(n))."""
    json_path = Path(__file__).resolve().parent.parent.parent / "bulk.json"
    with open(json_path, "r") as f:
        bulk_data = json.load(f)
    items = bulk_data["items"]
    if len(items) < data.quantity:
        n = math.ceil(data.quantity // len(items))
        items = (items * n)[:data.quantity]
    else:
        items = bulk_data["items"][:data.quantity]

    inventories = [
        Inventory(name=item["name"], amount=item["amount"])
        for item in items
    ]
    service = InventoryService(session=session)
    result = await service.create_all(inventories)
    if not result:
        raise HTTPException(status_code=400, detail="Error al crear los inventarios")
    return result


@router.post("/bulck", status_code=201)
async def create_bulck_from_file(
    data: InventoryBulkFromFileCreate,
    session: AsyncSession = Depends(get_session),
):
    """Crear inventarios desde archivo JSON de forma asíncrona (O(1))."""
    json_path = Path(__file__).resolve().parent.parent.parent / "bulk_async.json"
    with open(json_path, "r") as f:
        bulk_data = json.load(f)
    items = bulk_data["items"][:data.quantity]
    inventories = [
        Inventory(name=item["name"], amount=item["amount"])
        for item in items
    ]
    service = InventoryService(session=session)
    result = await service.create_all_async(inventories)
    if not result:
        raise HTTPException(status_code=400, detail="Error al crear los inventarios")
    return result
