"""fix

Revision ID: 3965f645543d
Revises: 93ddca33c59b
Create Date: 2025-05-21 00:35:28.801597

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3965f645543d'
down_revision: Union[str, None] = '93ddca33c59b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('object_photos', sa.Column('description', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('object_photos', 'description')
    # ### end Alembic commands ###
