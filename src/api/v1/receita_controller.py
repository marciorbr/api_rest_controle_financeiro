from fastapi import APIRouter, Depends, HTTPException
from typing import Annotated
from sqlalchemy import select
from sqlalchemy.orm import Session
from datetime import date

from src.database import get_session
from src.schemas import ReceitaSchema, ReceitaPublic, ReceitaList, ReceitaUpdate
from src.models import Receitas

from src.services import verifica_duplicidade_receitas


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


@router.get('/{id}', response_model=ReceitaPublic)
def detalhes_receita(id: int, session: Session):
    receita = session.scalar(select(Receitas).where(Receitas.id == id))

    if not receita:
        raise HTTPException(status_code=404, detail='Receita não encontrada')
    
    return receita

@router.put('/{id}', response_model=ReceitaPublic)
def atualizar_receita(id: int, session: Session, receita: ReceitaUpdate):
    
    q_receita = session.scalar(select(Receitas).where(Receitas.id == id))

    if not q_receita:
        raise HTTPException(status_code=404, detail='Receita não encontrada')
    
    data_mes_atual = date.today()
    receita_descricao = session.scalar(select(Receitas).where(Receitas.descricao == receita.descricao))
    if receita_descricao and receita_descricao.data.month == data_mes_atual.month:
        raise HTTPException(status_code=400, detail='Já existe uma receita com essa descrição cadastrada esse mês')
    
    for key, value in receita.model_dump(exclude_unset=True).items():
        setattr(q_receita, key, value)

    session.add(q_receita)
    session.commit()
    session.refresh(q_receita)

    return q_receita