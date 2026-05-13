from fastapi import FastAPI
from src.database import create_db_and_tables
from contextlib import asynccontextmanager
from src.routes import inventory_router, persons_router, user_router


@asynccontextmanager
async def lifepan(app: FastAPI):
    """ Crear una sesión de la base de datos """
    await create_db_and_tables()
    yield

app = FastAPI(lifespan=lifepan)

app.include_router(inventory_router)
app.include_router(persons_router)
app.include_router(user_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)