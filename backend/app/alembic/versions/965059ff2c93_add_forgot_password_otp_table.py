"""add expires_at to forgot_password_otp table

Revision ID: 965059ff2c93
Revises: 5da5cabbee33
Create Date: 2025-07-09 23:44:01.716733
"""

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '965059ff2c93'
down_revision = '5da5cabbee33'
branch_labels = None
depends_on = None

def upgrade() -> None:
    op.add_column('forgot_password_otp', sa.Column('expires_at', sa.DateTime(), nullable=False))

def downgrade() -> None:
    op.drop_column('forgot_password_otp', 'expires_at')
