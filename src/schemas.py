import datetime

from pydantic import BaseModel

class ReceitaSchema(BaseModel):
    descricao: str
    valor: int
    data: datetime.date
    
class ReceitaPublic(ReceitaSchema):
    id: int

class ReceitaList(BaseModel):
    receitas: list[ReceitaPublic]

class ReceitaUpdate(BaseModel):
    descricao: str | None = None
    valor: int | None = None
    data: datetime.date | None = None

class Message(BaseModel):
    detail: str