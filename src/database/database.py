from sqlalchemy.ext.asyncio import create_async_engine
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel

sqlite_name = "database.db"

sqlite_url = f"sqlite+aiosqlite:///{sqlite_name}"

engine = create_async_engine(sqlite_url, echo=True)


async_session_factory = sessionmaker(
    engine, expire_on_commit=False, class_=AsyncSession
)

async def get_session():
    """ Obtener una sesión de la base de datos """
    async with async_session_factory() as session:
        yield session    

async def create_db_and_tables():
    """ 
    Crea las tablas de forma asíncrona. 
    Usamos engine.begin() para manejar la transacción de DDL.
    """
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)