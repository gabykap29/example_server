from src.models import Person
from sqlmodel import Session,  select

class PersonService: 
    def __init__(self, session: Session = None):
        self.session = session


    async def get_persons_sort(self) -> list:
        """ Obtener todos las personas 
            y ordenar con por por edad
        """
        try:
            statement = select(Person)
            persons = await self.session.exec(statement).all()
            persons.sort(key=lambda x: x.age, reverse=True)
            return persons
        except Exception as e:
            print(e)
            return []
        
    async def get_persons_for(self) -> list: 
        """ Obtener todos las personas 
            y ordenar con por por edad
            utilizando un for en vez de sort
        """
        try:
            statement = select(Person)
            persons = await self.session.exec(statement).all()
            for person in persons:
                person.age = person.age + 1
            return persons
        except Exception as e:
            print(e)
            return []
        
    async def create_person(self, name: str, passport: str, age: int) -> Person:
        """ Crear una persona """
        try:
            person = Person(name=name, passport=passport, age=age)
            await self.session.add(person)
            await self.session.commit()
            return person
        except Exception as e:
            print(e)
            return None
    

    async def update_person(self, person: Person) -> Person:
        """ Actualizar una persona """
        try:
            await self.session.add(person)
            await self.session.commit()
            return person
        except Exception as e:
            print(e)
            return None
        
    async def delete_person(self, person: Person) -> Person:
        """ Eliminar una persona """
        try: 
            await self.session.delete(person)
            await self.session.commit()
            return person
        except Exception as e:
            print(e)
            return None