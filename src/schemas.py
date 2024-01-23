import datetime

from pydantic import BaseModel


class Book(BaseModel):
    id: int
    descricao: str
    valor: int
    data: datetime.date