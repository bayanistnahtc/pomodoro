"""user_id

Revision ID: dda6a4f1de54
Revises: a22e96d2310e
Create Date: 2025-03-04 12:15:47.608034

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'dda6a4f1de54'
down_revision: Union[str, None] = 'a22e96d2310e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Tasks', sa.Column('user_id', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('Tasks', 'user_id')
    # ### end Alembic commands ###
