"""added subscription indexes

Revision ID: ac70d1b2d43e
Revises: 8209406713d1
Create Date: 2025-04-27 00:06:31.370837

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ac70d1b2d43e'
down_revision: Union[str, None] = '8209406713d1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_index(op.f('ix_subscriptions_followed_id'), 'subscriptions', ['followed_id'], unique=False)
    op.create_index(op.f('ix_subscriptions_follower_id'), 'subscriptions', ['follower_id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_subscriptions_follower_id'), table_name='subscriptions')
    op.drop_index(op.f('ix_subscriptions_followed_id'), table_name='subscriptions')
    # ### end Alembic commands ###
