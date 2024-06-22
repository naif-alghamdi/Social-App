"""add contant colume to post table

Revision ID: f3a5b8a9e28f
Revises: d597ea9e42fd
Create Date: 2024-06-18 17:20:33.108542

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f3a5b8a9e28f'
down_revision: Union[str, None] = 'd597ea9e42fd'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("posts", sa.Column('content', sa.String, nullable=False))


def downgrade() -> None:
    op.drop_column("posts", "content")
