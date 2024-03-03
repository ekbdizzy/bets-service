"""empty message

Revision ID: 3a0b2944df5c
Revises: 
Create Date: 2024-03-03 21:16:35.293140

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '3a0b2944df5c'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('bet',
    sa.Column('id', sa.Integer(), nullable=False, comment='Bet ID'),
    sa.Column('event_uuid', sa.UUID(), nullable=False, comment='Event unique ID'),
    sa.Column('amount', sa.Numeric(scale=2), nullable=False, comment='Bet amount'),
    sa.Column('status', sa.Enum('new', 'win', 'lose', name='betstatus'), nullable=False),
    sa.Column('win_amount', sa.Numeric(scale=2), nullable=False, comment='Win amount'),
    sa.Column('created_at', postgresql.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', postgresql.TIMESTAMP(timezone=True), nullable=False),
    sa.CheckConstraint('amount > 0', name='positive_amount'),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('bet')
    # ### end Alembic commands ###
