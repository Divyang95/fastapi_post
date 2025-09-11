"""add content column to posts table

Revision ID: 466f6ef867cd
Revises: 53358294768d
Create Date: 2025-09-10 17:48:39.278720

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '466f6ef867cd'
down_revision: Union[str, Sequence[str], None] = '53358294768d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass 



def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('posts','content')
    pass 
