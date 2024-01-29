from fastapi import APIRouter, Depends, HTTPException
from typing import Annotated
from sqlalchemy import select
from sqlalchemy.orm import Session

from src.database import get_session
from src.schemas import ReceitaSchema, ReceitaPublic, ReceitaList
from src.models import Receitas


router = APIRouter(prefix='/api/v1/receita', tags=['receita'])

Session = Annotated[Session, Depends(get_session)]

@router.post('/', response_model=ReceitaPublic )
def criar_receita(receita: ReceitaSchema, session: Session):
    receita_descricao = session.scalar(select(Receitas).where(Receitas.descricao == receita.descricao))
    
    if receita_descricao and receita_descricao.data.month == receita.data.month:
        raise HTTPException(status_code=400, detail='Já existe uma receita com essa descrição cadastrada esse mês')

    new_receita: Receitas = Receitas(
        descricao=receita.descricao,
        valor=receita.valor,
        data=receita.data,
    )
    session.add(new_receita)
    session.commit()
    session.refresh(new_receita)

    return new_receita


@router.get('/', response_model=ReceitaList)
def listar_receitas(session: Session):
    query = select(Receitas)
    receitas = session.scalars(query).all()

    return {'receitas': receitas}
