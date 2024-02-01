from fastapi import APIRouter, Depends, HTTPException
from typing import Annotated
from sqlalchemy import select
from sqlalchemy.orm import Session

from src.database import get_session
from src.models import Despesas
from src.schemas import DespesaPublic, DespesaSchema


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