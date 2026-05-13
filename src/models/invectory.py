from sqlmodel import SQLModel, Field

class Inventory(SQLModel, table=True):
    """ Inventory model """
    id: int = Field(primary_key=True, default= None)
    name: str = Field(max_length=255)
    amount: int = Field(default=0)
    class Config:
        schema = "inventory"