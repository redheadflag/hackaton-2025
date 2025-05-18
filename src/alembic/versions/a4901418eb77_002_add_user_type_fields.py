"""002 add user type fields

Revision ID: a4901418eb77
Revises: 5c8fc2256a85
Create Date: 2025-05-18 11:45:57.205574

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'a4901418eb77'
down_revision: Union[str, None] = '5c8fc2256a85'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    usertype_enum = sa.Enum('HUMAN', 'ROBOT', name='usertype')
    usertype_enum.create(op.get_bind())
    op.create_unique_constraint(None, 'channels', ['slug'])
    op.add_column('users', sa.Column('is_oracle', sa.Boolean(), nullable=False, server_default=sa.sql.expression.false()))
    op.add_column('users', sa.Column('user_type', sa.Enum('HUMAN', 'ROBOT', name='usertype'), nullable=True))
    op.create_unique_constraint(None, 'users', ['login'])


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint(None, 'users', type_='unique')
    op.drop_column('users', 'user_type')
    op.drop_column('users', 'is_oracle')
    op.drop_constraint(None, 'channels', type_='unique')
    