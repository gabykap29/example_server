from sqlmodel import Session, select
from src.models import Inventory
import time

class InventoryService:
    def __init__(self, session: Session = None):
        self.session = session

    async def create_all(self, inventories: list) -> dict:
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
            statement = select(Inventory).where(Inventory.name == "producto_1")
            result = await self.session.exec(statement)
            inventory = result.all()
            inventory.sort(key=lambda x: x.amount, reverse=True)
            return {
                "amount": inventory,
                "time": time.time() - start_time
            }
        except Exception as e:
            print(e)
            return []
    async def get_inventory_all(self) -> list:
        """ Obtener todos los inventarios """
        try:
            start_time = time.time()
            statement = select(Inventory).order_by(Inventory.id.desc())
            result = await self.session.exec(statement)
            inventory = result.all()
            inventory_filter = filter(lambda x: x.name == "producto_1", inventory)

            return {
                "inventories": inventory_filter,
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