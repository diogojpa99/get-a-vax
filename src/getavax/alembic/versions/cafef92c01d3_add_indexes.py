"""add_indexes

Revision ID: cafef92c01d3
Revises: 
Create Date: 2023-05-22 19:27:00.034124

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cafef92c01d3'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_index('idx_dates', 'vaccine_user_schedule_event_scheduled', ['s_at_date'])


def downgrade():
    op.drop_index('idx_dates', 'vaccine_user_schedule_event_scheduled')
