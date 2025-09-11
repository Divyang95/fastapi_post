"""add users table

Revision ID: 628b533abf42
Revises: 466f6ef867cd
Create Date: 2025-09-10 18:17:44.305950

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '628b533abf42'
down_revision: Union[str, Sequence[str], None] = '466f6ef867cd'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table('users', 
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('email', sa.Integer(), nullable=False),
                    sa.Column('password', sa.Integer(), nullable=False),
                    sa.Column('created_at', sa.TIMESTAMP(timezone=True),
                              server_default=sa.text('now()') ,nullable=False),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('email')
                    
                    )

    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('users')
    pass
