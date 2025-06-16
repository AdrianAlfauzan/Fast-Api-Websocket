"""create webrtc rooms and participants table

Revision ID: 6b5b8e2a8c30
Revises: f209bd142392
Create Date: 2025-06-16 10:47:07.944815

"""
from alembic import op
import sqlalchemy as sa
import uuid


# revision identifiers, used by Alembic.
revision = '6b5b8e2a8c30'
down_revision = 'f209bd142392'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'rooms',
        sa.Column('id', sa.UUID(as_uuid=True), primary_key=True,
                  default=uuid.uuid4, nullable=False),
        sa.Column('name', sa.String, nullable=False),
        sa.Column('created_by', sa.UUID(as_uuid=True),
                  sa.ForeignKey('users.id'), nullable=False),
        sa.Column('created_at', sa.DateTime,
                  server_default=sa.func.now(), nullable=False),
    )

    op.create_table(
        'room_participants',
        sa.Column('room_id', sa.UUID(as_uuid=True), sa.ForeignKey('rooms.id', ondelete='CASCADE'), primary_key=True),
        sa.Column('user_id', sa.UUID(as_uuid=True), sa.ForeignKey('users.id', ondelete='CASCADE'), primary_key=True),
        sa.Column('joined_at', sa.DateTime, server_default=sa.func.now(), nullable=False),
    )


def downgrade() -> None:
    op.drop_table('room_participants')
    op.drop_table('rooms')
