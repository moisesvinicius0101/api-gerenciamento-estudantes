"""add course_id to students

Revision ID: a97aaa00170d
Revises: 758bb97f3b7d
Create Date: 2026-11-24 06:57:50.816378

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a97aaa00170d'
down_revision: Union[str, Sequence[str], None] = '758bb97f3b7d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    with op.batch_alter_table('students', schema=None) as batch_op:
        batch_op.add_column(sa.Column('course_id', sa.Integer(), nullable=True))
        batch_op.create_foreign_key(
            'fk_students_course_id_courses',  # nome que estava faltando (era None)
            'courses', ['course_id'], ['id']
        )


def downgrade() -> None:
    with op.batch_alter_table('students', schema=None) as batch_op:
        batch_op.drop_constraint('fk_students_course_id_courses', type_='foreignkey')
        batch_op.drop_column('course_id')