"""renomeia name para title em courses

Revision ID: 758bb97f3b7d
Revises: 311a780a938a
Create Date: 2026-11-19 08:46:55.326128

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '758bb97f3b7d'
down_revision: Union[str, Sequence[str], None] = '311a780a938a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    with op.batch_alter_table('courses', schema=None) as batch_op:
        batch_op.alter_column('name', new_column_name='title')


def downgrade() -> None:
    """Downgrade schema."""
    with op.batch_alter_table('courses', schema=None) as batch_op:
        batch_op.alter_column('title', new_column_name='name')
