from pydantic import BaseModel

class Transaction(BaseModel):
    data: dict