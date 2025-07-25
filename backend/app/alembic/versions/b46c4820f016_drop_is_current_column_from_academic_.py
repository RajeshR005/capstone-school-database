"""drop is_current column from academic_years

Revision ID: b46c4820f016
Revises: dbc60d4fdc44
Create Date: 2025-07-08 12:10:12.323531

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'b46c4820f016'
down_revision = 'dbc60d4fdc44'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('academic_years', 'is_current')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('academic_years', sa.Column('is_current', mysql.INTEGER(), autoincrement=False, nullable=True))
    # ### end Alembic commands ###
