from datetime import date
from fastapi import APIRouter, Depends, HTTPException
from typing import Annotated
from sqlalchemy import select
from sqlalchemy.orm import Session

from src.database import get_session
from src.models import Despesas
from src.schemas import DespesaPublic, DespesaSchema, DespesaList, DespesaUpdate


router = APIRouter(prefix='/api/v1/despesa', tags=['despesa'])

Session = Annotated[Session, Depends(get_session)]

@router.post('/', response_model=DespesaPublic )
def criar_despesa(despesa: DespesaSchema, session: Session):
    despesa_descricao = session.scalar(select(Despesas).where(Despesas.descricao == despesa.descricao))
    
    if despesa_descricao and despesa_descricao.data.month == despesa.data.month:
        raise HTTPException(status_code=400, detail='Já existe uma despesa com essa descrição cadastrada esse mês')

    new_despesa: Despesas = Despesas(
        descricao=despesa.descricao,
        valor=despesa.valor,
        data=despesa.data,
    )
    session.add(new_despesa)
    session.commit()
    session.refresh(new_despesa)

    return new_despesa

@router.get('/', response_model=DespesaList)
def listar_despesas(session: Session):
    query = select(Despesas)
    despesas = session.scalars(query).all()

    return {'despesas': despesas}

@router.get('/{id}', response_model=DespesaPublic)
def detalhes_despesa(id: int, session: Session):
    despesa = session.scalar(select(Despesas).where(Despesas.id == id))

    if not despesa:
        raise HTTPException(status_code=404, detail='Despesa não encontrada')
    
    return despesa

@router.put('/{id}', response_model=DespesaPublic)
def atualizar_despesa(id: int, session: Session, despesa: DespesaUpdate):
    
    q_despesa = session.scalar(select(Despesas).where(Despesas.id == id))

    if not q_despesa:
        raise HTTPException(status_code=404, detail='Despesa não encontrada')
    
    data_mes_atual = date.today()
    
    despesa_descricao = session.scalar(select(Despesas).where(Despesas.descricao == despesa.descricao))
    if despesa_descricao and despesa_descricao.data.month == data_mes_atual.month:
        raise HTTPException(status_code=400, detail='Já existe uma despesa com essa descrição cadastrada esse mês')
    
    for key, value in despesa.model_dump(exclude_unset=True).items():
        setattr(q_despesa, key, value)

    session.add(q_despesa)
    session.commit()
    session.refresh(q_despesa)

    return q_despesa