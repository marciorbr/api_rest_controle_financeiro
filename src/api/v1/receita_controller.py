from fastapi import APIRouter, Depends, HTTPException
from typing import Annotated
from sqlalchemy import select
from sqlalchemy.orm import Session

from src.database import get_session
from src.schemas import ReceitaSchema, ReceitaPublic
from src.models import Receitas


router = APIRouter(prefix='/api/v1/receita', tags=['receita'])

Session = Annotated[Session, Depends(get_session)]

@router.post('/', response_model=ReceitaPublic )
def criar_receita(receita: ReceitaSchema, session: Session):
    receita_descricao = session.scalar(select(Receitas).where(Receitas.descricao == receita.descricao))
    
    if receita_descricao:
        raise HTTPException(status_code=400, detail='Essa descição de receita já existe')


    new_receita: Receitas = Receitas(
        descricao=receita.descricao,
        valor=receita.valor,
        data=receita.data,
    )
    session.add(new_receita)
    session.commit()
    session.refresh(new_receita)

    return new_receita

