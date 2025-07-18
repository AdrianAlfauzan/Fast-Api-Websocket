"""create user table

Revision ID: e33bbd050e48
Revises: 
Create Date: 2025-05-22 18:04:10.318444

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
import uuid
# revision identifiers, used by Alembic.
revision = 'e33bbd050e48'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('perf_logs',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('method', sa.String(), nullable=False),
    sa.Column('url', sa.String(), nullable=False),
    sa.Column('req_headers', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
    sa.Column('req_body', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
    sa.Column('resp_status', sa.SmallInteger(), nullable=True),
    sa.Column('duration', sa.Float(), nullable=True),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text("timezone('Asia/Jakarta', now())"), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('revoked_tokens',
    sa.Column('token', sa.String(), nullable=False),
    sa.Column('revoked_at', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('token')
    )
    op.create_table('users',
    sa.Column('id', sa.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
    sa.Column('full_name', sa.String(), nullable=False),
    sa.Column('username', sa.String(), nullable=False),
    sa.Column('password', sa.String(), nullable=False),
    sa.Column('email', sa.String(), nullable=True),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text("timezone('Asia/Jakarta', now())"), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('deleted_at', sa.DateTime(), nullable=True),
    sa.Column('created_by', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    op.create_index(op.f('ix_users_id'), 'users', ['id'], unique=False)
    op.create_index(op.f('ix_users_username'), 'users', ['username'], unique=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_users_username'), table_name='users')
    op.drop_index(op.f('ix_users_id'), table_name='users')
    op.drop_table('users')
    op.drop_table('revoked_tokens')
    op.drop_table('perf_logs')
    # ### end Alembic commands ###
