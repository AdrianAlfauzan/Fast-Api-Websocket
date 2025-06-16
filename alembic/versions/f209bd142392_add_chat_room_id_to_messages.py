"""add chat_room_id to messages

Revision ID: f209bd142392
Revises: 830ca613315d
Create Date: 2025-06-12 21:12:42.803167

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f209bd142392'
down_revision = '830ca613315d'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        'messages',
        sa.Column('chat_room_id', sa.UUID(as_uuid=True), sa.ForeignKey(
            'chat_rooms.id', ondelete='CASCADE'), nullable=True)
    )


def downgrade() -> None:
    op.drop_column('messages', 'chat_room_id')
