from sqlmodel import Session, select
from src.models import Inventory
import time
import random

class InventoryService:
    def __init__(self, session: Session):
        self.session = session

    async def create_all(self, inventories: list[Inventory]) -> dict:
        """ Crear todos los inventarios uno a uno
            complejidad O(n)
        """
        try:
            for inventory in inventories:
                self.session.add(inventory)
            await self.session.commit()
            return inventories
        except Exception as e:
            print(e)
            return []
        
    async def create_all_async(self, inventories: list) -> list:
        """ Crea todos los inventarios pero se lo delega a la base de datos
        complejidad O(1)
        """
        try:
            self.session.add_all(inventories)
            await self.session.commit()
            return inventories
        except Exception as e:
            print(e)
            return []

    async def get_inventory(self) -> dict:
        """ Obtener todos los inventarios """
        try:
            start_time = time.time()
            statement = select(Inventory)
            result = await self.session.exec(statement)
            inventory = result.all()
            n = random.randint(0, 100)
            inventory_filter = list(filter(lambda x: x.name == f"producto_{n}", inventory))
            inventory_filter.sort(key=lambda x: x.amount, reverse=True)

            print("after filtering: ", len(inventory_filter), f"producto_{n}")

            return {
                "amount": len(inventory_filter),
                "time": time.time() - start_time
            }
        except Exception as e:
            print(e)
            return []

    async def get_inventory_all(self) -> list:
        """ Obtener todos los inventarios """
        try:
            start_time = time.time()
            n = random.randint(0, 100)
            statement = select(Inventory).order_by(Inventory.id.desc()).where(Inventory.name == f"producto_{n}")
            result = await self.session.exec(statement)
            inventory = result.all()

            return {
                "amount": len(inventory),
                "time": time.time() - start_time
            }
        except Exception as e:
            print(e)
            return []
    async def create_inventory(self, name: str, amount: int) -> Inventory:
        """ Crear un inventario """
        try:
            inventory = Inventory(name=name, amount=amount)
            self.session.add(inventory)
            await self.session.commit()
            return inventory
        except Exception as e:
            print(e)
            return None

    async def update_inventory(self, inventory: Inventory) -> Inventory:
        """ Actualizar un inventario """
        try:
            self.session.add(inventory)
            await self.session.commit()
            return inventory
        except Exception as e:
            print(e)
            return None

    async def delete_inventory(self, inventory: Inventory) -> Inventory:
        """ Eliminar un inventario """
        try:
            await self.session.delete(inventory)
            await self.session.commit()
            return inventory
        except Exception as e:
            print(e)
            return None
