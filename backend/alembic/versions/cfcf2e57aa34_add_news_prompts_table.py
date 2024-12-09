"""add_news_prompts_table

Revision ID: cfcf2e57aa34
Revises: 6ac9f7773258
Create Date: 2024-12-09 08:28:00.932789

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'cfcf2e57aa34'
down_revision: Union[str, None] = '6ac9f7773258'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass