"""Fix category relationships

Revision ID: 6ac9f7773258
Revises: 35f6f1fd6f1c
Create Date: 2024-12-09 08:21:23.143965

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6ac9f7773258'
down_revision: Union[str, None] = '35f6f1fd6f1c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass