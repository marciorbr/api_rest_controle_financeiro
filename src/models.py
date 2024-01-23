import datetime

from sqlalchemy.orm import  Mapped, DeclarativeBase, mapped_column

class Base(DeclarativeBase):
    pass

class Receitas(Base):
    __tablename__ = 'receitas'

    id: Mapped[int] = mapped_column(primary_key=True)
    descricao: Mapped[str]
    valor: Mapped[int]
    data: Mapped[datetime.datetime]

class Despesas(Base):
    __tablename__ = 'despesas'

    id: Mapped[int] = mapped_column(primary_key=True)
    descricao: Mapped[str]
    valor: Mapped[int]
    data: Mapped[datetime.datetime]