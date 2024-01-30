"""Change store_and_fwd_flag to Boolean

Revision ID: ad2947d34606
Revises: 1f0e865eb5e0
Create Date: 2024-01-30 19:03:15.994404

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ad2947d34606'
down_revision: Union[str, None] = '1f0e865eb5e0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('trips', 'store_and_fwd_flag', new_column_name='_store_and_fwd_flag')
    op.add_column('trips', sa.Column('store_and_fwd_flag', sa.Boolean(), nullable=True))
    op.execute("update trips set store_and_fwd_flag=true where _store_and_fwd_flag='Y'")
    op.execute("update trips set store_and_fwd_flag=false where _store_and_fwd_flag='N'")
    op.drop_column('trips', '_store_and_fwd_flag')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('trips', 'store_and_fwd_flag', new_column_name='_store_and_fwd_flag')
    op.add_column('trips', sa.Column('store_and_fwd_flag', sa.String(), nullable=True))
    op.execute("update trips set store_and_fwd_flag='Y' where _store_and_fwd_flag=true")
    op.execute("update trips set store_and_fwd_flag='N' where _store_and_fwd_flag=false")
    op.drop_column('trips', '_store_and_fwd_flag')
    # ### end Alembic commands ###
