"""add_prompt_columns_new

Revision ID: [leave this as generated]
Revises: [leave this as generated]
Create Date: [leave this as generated]

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic
revision = '[leave as is]'
down_revision = '[leave as is]'
branch_labels = None
depends_on = None

def upgrade() -> None:
    # Add columns to prompts table
    op.add_column('prompts', sa.Column('refresh_interval', sa.Integer(), nullable=True, server_default='24'))
    op.add_column('prompts', sa.Column('max_articles', sa.Integer(), nullable=True, server_default='100'))
    op.add_column('prompts', sa.Column('custom_categories', postgresql.JSON(), nullable=True))
    op.add_column('prompts', sa.Column('source_preferences', postgresql.JSON(), nullable=True))
    op.add_column('prompts', sa.Column('llm_provider', sa.String(), nullable=True))
    op.add_column('prompts', sa.Column('llm_config', postgresql.JSON(), nullable=True))
    op.add_column('prompts', sa.Column('layout_settings', postgresql.JSON(), nullable=True))
    op.add_column('prompts', sa.Column('sorting_preferences', postgresql.JSON(), nullable=True))
    op.add_column('prompts', sa.Column('meta_info', postgresql.JSON(), nullable=True))

def downgrade() -> None:
    # Remove columns from prompts table
    op.drop_column('prompts', 'refresh_interval')
    op.drop_column('prompts', 'max_articles')
    op.drop_column('prompts', 'custom_categories')
    op.drop_column('prompts', 'source_preferences')
    op.drop_column('prompts', 'llm_provider')
    op.drop_column('prompts', 'llm_config')
    op.drop_column('prompts', 'layout_settings')
    op.drop_column('prompts', 'sorting_preferences')
    op.drop_column('prompts', 'meta_info')