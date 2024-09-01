"""price

Revision ID: e53af3e8682a
Revises: 402da8b323dd
Create Date: 2024-09-01 17:19:15.879703

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e53af3e8682a'
down_revision: Union[str, None] = '402da8b323dd'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('subscription', sa.Column('price', sa.Integer(), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('subscription', 'price')
    # ### end Alembic commands ###
