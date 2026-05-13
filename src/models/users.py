from sqlmodel import SQLModel, Field

class User(SQLModel, table=True):
    """ User model """
    id: int = Field(primary_key=True, default= None)
    name: str = Field(max_length=255)
    email: str = Field(max_length=255)

    class Config:
        schema = "users"