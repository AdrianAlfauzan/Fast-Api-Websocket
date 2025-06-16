"""add chat_rooms and chat_room_users with UUID

Revision ID: 0cbf0bb0177f
Revises: bc2e4d406a9d
Create Date: 2025-06-10 21:03:09.418078

"""
from alembic import op
import sqlalchemy as sa
import uuid

from sqlalchemy.dialects.postgresql import UUID, ENUM

# revision identifiers, used by Alembic.
revision = '0cbf0bb0177f'
down_revision = 'bc2e4d406a9d'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create ENUM type for role
    role_enum = ENUM('admin', 'member', name='chatroomuserrole')

    op.create_table(
        'chat_rooms',
        sa.Column('id', UUID(as_uuid=True), primary_key=True,default=uuid.uuid4, nullable=False),
        sa.Column('name', sa.String, nullable=False),
        sa.Column('description', sa.String, nullable=True),
        sa.Column('is_group', sa.Boolean, nullable=False, default=False),
        sa.Column('created_by', UUID(as_uuid=True),
        sa.ForeignKey('users.id'), nullable=False),
        sa.Column('created_at', sa.DateTime, server_default=sa.func.now(), nullable=False),
        sa.Column('updated_at', sa.DateTime, nullable=True),
    )

    op.create_table(
        'chat_room_users',
        sa.Column('chat_room_id', UUID(as_uuid=True),
        sa.ForeignKey('chat_rooms.id'), primary_key=True),
        sa.Column('user_id', UUID(as_uuid=True),sa.ForeignKey('users.id'), primary_key=True),
        sa.Column('joined_at', sa.DateTime,server_default=sa.func.now(), nullable=False),
        sa.Column('created_at', sa.DateTime, server_default=sa.func.now(), nullable=False),
        sa.Column('updated_at', sa.DateTime, nullable=True),
    )


def downgrade() -> None:
    op.drop_table('chat_room_users')
    op.drop_table('chat_rooms')
    op.execute("DROP TYPE IF EXISTS chatroomuserrole")
