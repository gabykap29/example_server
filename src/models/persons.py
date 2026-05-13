from sqlmodel import SQLModel, Field

class Person(SQLModel, table=True):
    """ Person model """
    id: int = Field(primary_key=True, default= None)
    name: str = Field( max_length=255)
    passport: str = Field( max_length=255)
    age: int = Field(default=0)
    
    class Config:
        schema = "persons"