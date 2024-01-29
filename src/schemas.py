import datetime

from pydantic import BaseModel

class ReceitaSchema(BaseModel):
    descricao: str
    valor: int
    data: datetime.date
    
class ReceitaPublic(ReceitaSchema):
    id: int