"""create chat tables

Revision ID: bc2e4d406a9d
Revises: e33bbd050e48
Create Date: 2025-06-07 17:14:50.016919

"""
from alembic import op
import sqlalchemy as sa
import uuid

# revision identifiers, used by Alembic.
revision = 'bc2e4d406a9d'
down_revision = 'e33bbd050e48'
branch_labels = None
depends_on = None


def upgrade() -> None:
  

    op.create_table(
        'conversations',
        sa.Column('id', sa.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
        sa.Column('created_at', sa.DateTime, server_default=sa.func.now()),
    )

    op.create_table(
        'conversation_users',
        sa.Column('conversation_id', sa.UUID(as_uuid=True), sa.ForeignKey('conversations.id', ondelete='CASCADE')),
        sa.Column('user_id', sa.UUID(as_uuid=True), sa.ForeignKey('users.id', ondelete='CASCADE')),
        sa.PrimaryKeyConstraint('conversation_id', 'user_id')
    )

    op.create_table(
        'messages',
        sa.Column('id', sa.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
        sa.Column('conversation_id', sa.UUID(as_uuid=True), sa.ForeignKey('conversations.id', ondelete='CASCADE')),
        sa.Column('sender_id', sa.UUID(as_uuid=True), sa.ForeignKey('users.id')),
        sa.Column('content', sa.Text, nullable=False),
        sa.Column('message_type', sa.Enum('text', 'image', 'video', 'file', name='message_type_enum')),
        sa.Column('seen', sa.Boolean, default=False),
        sa.Column('sent_at', sa.DateTime, server_default=sa.func.now()),
        sa.Column('created_at', sa.DateTime, server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime, server_default=sa.func.now(), onupdate=sa.func.now()),
    )



def downgrade() -> None:
    op.drop_table('messages')
    op.drop_table('conversation_users')
    op.drop_table('conversations')
    op.drop_table('users')
    sa.Enum(name='message_type_enum').drop(op.get_bind())
