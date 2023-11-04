"""Add participants to meetings

Revision ID: 6c7b16355103
Revises: 
Create Date: 2023-11-03 14:06:32.423306

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6c7b16355103'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.add_column('meeting', sa.Column('participants', sa.Integer, nullable=True))

def downgrade():
    op.drop_column('meeting', 'participants')
