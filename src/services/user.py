import numpy as np
import time
from sqlmodel import Session, select
from src.models import User


class UserService:
    def __init__(self, session: Session = None):
        self.session = session

    async def get_users(self) -> list:
        """ Obtener todos los usuarios """
        try:
            statement = select(User)
            result = await self.session.exec(statement)
            users = result.all()
            return users
        except Exception as e:
            print(e)
            return []

    async def create_user(self, name: str, email: str) -> User:
        """ Crear un usuario """
        try:
            user = User(name=name, email=email)
            self.session.add(user)
            await self.session.commit()
            return user
        except Exception as e:
            print(e)
            return None

    async def update_user(self, user: User) -> User:
        """ Actualizar un usuario """
        try:
            self.session.add(user)
            await self.session.commit()
            return user
        except Exception as e:
            print(e)
            return None

    async def delete_user(self, user: User) -> User:
        """ Eliminar un usuario """
        try:
            await self.session.delete(user)
            await self.session.commit()
            return user
        except Exception as e:
            print(e)
            return None

    async def create_users_numpy(self, quantity: int) -> dict:
        """ Crear usuarios usando numpy para generar datos vectorizados (O(n)) """
        try:
            start_time = time.time()
            names = np.array([f"user_{i}" for i in range(1, quantity + 1)])
            emails = np.array([f"user_{i}@mail.com" for i in range(1, quantity + 1)])
            users = [
                User(name=str(names[i]), email=str(emails[i]))
                for i in range(quantity)
            ]
            self.session.add_all(users)
            await self.session.commit()
            final_time = time.time() - start_time
            return {
                "anount": len(users),
                "time": final_time
            }
        except Exception as e:
            print(e)
            return []

    async def create_users_for(self, quantity: int) -> list[User]:
        """ Crear usuarios con un for simple (O(n)) """
        try:
            start_time = time.time()
            users = []
            for i in range(1, quantity + 1):
                user = User(name=f"user_{i}", email=f"user_{i}@mail.com")
                self.session.add(user)
                users.append(user)
                await self.session.commit()
            
            end_time = time.time() - start_time
            return {
                "anount": len(users),
                "time": end_time
            }
        except Exception as e:
            print(e)
            return []
