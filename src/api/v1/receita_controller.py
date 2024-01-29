from fastapi import APIRouter, Depends
from typing import Annotated
from sqlalchemy.orm import Session

from src.database import get_session
from src.schemas import ReceitaSchema, ReceitaPublic
from src.models import Receitas


router = APIRouter(prefix='/api/v1/receita', tags=['receita'])

Session = Annotated[Session, Depends(get_session)]

@router.post('/', response_model=ReceitaPublic )
def criar_receita(receita: ReceitaSchema, session: Session):
    new_receita: Receitas = Receitas(
        descricao=receita.descricao,
        valor=receita.valor,
        data=receita.data,
    )
    session.add(new_receita)
    session.commit()
    session.refresh(new_receita)

    return new_receita