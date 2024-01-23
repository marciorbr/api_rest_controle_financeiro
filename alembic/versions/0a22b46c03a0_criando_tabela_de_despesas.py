"""criando tabela de despesas

Revision ID: 0a22b46c03a0
Revises: 900b4dedbe5d
Create Date: 2024-01-23 14:09:05.169100

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0a22b46c03a0'
down_revision: Union[str, None] = '900b4dedbe5d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('despesas',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('descricao', sa.String(), nullable=False),
    sa.Column('valor', sa.Integer(), nullable=False),
    sa.Column('data', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('receitas',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('descricao', sa.String(), nullable=False),
    sa.Column('valor', sa.Integer(), nullable=False),
    sa.Column('data', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('receitas')
    op.drop_table('despesas')
    # ### end Alembic commands ###