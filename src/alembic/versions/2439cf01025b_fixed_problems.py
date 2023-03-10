"""Fixed problems

Revision ID: 2439cf01025b
Revises: c405bbeba6da
Create Date: 2023-02-24 00:59:14.185166

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2439cf01025b'
down_revision = 'c405bbeba6da'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('password_hashed', sa.String(), nullable=True))
    op.add_column('users', sa.Column('role', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'role')
    op.drop_column('users', 'password_hashed')
    # ### end Alembic commands ###
