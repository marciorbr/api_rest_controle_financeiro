import datetime

from pydantic import BaseModel

class Message(BaseModel):
    detail: str

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

class DespesaSchema(BaseModel):
    descricao: str
    valor: int
    data: datetime.date
    
class DespesaPublic(DespesaSchema):
    id: int

class DespesaList(BaseModel):
    despesas: list[DespesaPublic]