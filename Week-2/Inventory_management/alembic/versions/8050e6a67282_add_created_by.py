"""add created_by

Revision ID: 8050e6a67282
Revises: 
Create Date: 2026-04-27 11:27:01.945530
"""

from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '8050e6a67282'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    # 1. Add column as nullable first
    op.add_column('categories', sa.Column('created_by', sa.Integer(), nullable=True))

    # 2. Fill existing rows (IMPORTANT: make sure user with id=1 exists)
    op.execute("UPDATE categories SET created_by = 1")

    # 3. Add foreign key constraint
    op.create_foreign_key(
        'fk_categories_created_by',
        'categories',
        'users',
        ['created_by'],
        ['id']
    )

    # 4. Make column NOT NULL
    op.alter_column('categories', 'created_by', nullable=False)


def downgrade() -> None:
    """Downgrade schema."""

    # Drop foreign key first
    op.drop_constraint('fk_categories_created_by', 'categories', type_='foreignkey')

    # Then drop column
    op.drop_column('categories', 'created_by')