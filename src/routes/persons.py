from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from src.database.database import get_session
from src.models import Person
from src.services.persons import PersonService
from src.schemas.persons import PersonCreate, PersonUpdate, PersonResponse

router = APIRouter(prefix="/persons", tags=["persons"])


@router.get("/sorted", response_model=list[PersonResponse])
async def get_persons_sorted(session: AsyncSession = Depends(get_session)) -> list[PersonResponse]:
    """Obtener todas las personas ordenadas por edad de forma descendente."""
    service = PersonService(session=session)
    persons = await service.get_persons_sort()
    return persons


@router.get("/incremented-age", response_model=list[PersonResponse])
async def get_persons_incremented_age(
    session: AsyncSession = Depends(get_session),
) -> list[PersonResponse]:
    """Obtener todas las personas con la edad incrementada en 1."""
    service = PersonService(session=session)
    persons = await service.get_persons_for()
    return persons


@router.post("/", response_model=PersonResponse, status_code=201)
async def create_person(
    person_data: PersonCreate,
    session: AsyncSession = Depends(get_session),
) -> PersonResponse:
    """Crear una nueva persona."""
    service = PersonService(session=session)
    person = await service.create_person(
        name=person_data.name,
        passport=person_data.passport,
        age=person_data.age,
    )
    if person is None:
        raise HTTPException(status_code=400, detail="Error al crear la persona")
    return person


@router.put("/{person_id}", response_model=PersonResponse)
async def update_person(
    person_id: int,
    person_data: PersonUpdate,
    session: AsyncSession = Depends(get_session),
) -> PersonResponse:
    """Actualizar una persona existente."""
    statement = select(Person).where(Person.id == person_id)
    result = await session.exec(statement)
    person = result.first()
    if person is None:
        raise HTTPException(status_code=404, detail="Persona no encontrada")
    update_dict = person_data.model_dump(exclude_unset=True)
    for key, value in update_dict.items():
        setattr(person, key, value)
    service = PersonService(session=session)
    updated_person = await service.update_person(person)
    if updated_person is None:
        raise HTTPException(status_code=400, detail="Error al actualizar la persona")
    return updated_person


@router.delete("/{person_id}", response_model=PersonResponse)
async def delete_person(
    person_id: int,
    session: AsyncSession = Depends(get_session),
) -> PersonResponse:
    """Eliminar una persona por su ID."""
    statement = select(Person).where(Person.id == person_id)
    result = await session.exec(statement)
    person = result.first()
    if person is None:
        raise HTTPException(status_code=404, detail="Persona no encontrada")
    service = PersonService(session=session)
    deleted_person = await service.delete_person(person)
    if deleted_person is None:
        raise HTTPException(status_code=400, detail="Error al eliminar la persona")
    return deleted_person