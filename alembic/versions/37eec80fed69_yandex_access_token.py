"""yandex-access-token

Revision ID: 37eec80fed69
Revises: 7dc740e94f39
Create Date: 2025-03-14 17:12:42.890369

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '37eec80fed69'
down_revision: Union[str, None] = '7dc740e94f39'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('UserProfile', sa.Column('yandex_access_token', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('UserProfile', 'yandex_access_token')
    # ### end Alembic commands ###
