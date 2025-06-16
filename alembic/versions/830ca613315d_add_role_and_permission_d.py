"""add role and permission D

Revision ID: 830ca613315d
Revises: 0cbf0bb0177f
Create Date: 2025-06-10 21:19:37.947053

"""
from alembic import op
import sqlalchemy as sa
import uuid
from sqlalchemy.dialects.postgresql import UUID
# revision identifiers, used by Alembic.
revision = '830ca613315d'
down_revision = '0cbf0bb0177f'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'roles',
        sa.Column('id', UUID(as_uuid=True), primary_key=True,
                  default=uuid.uuid4, nullable=False),
        sa.Column('name', sa.String, unique=True, nullable=False),
        sa.Column('description', sa.String, nullable=True),
        sa.Column('created_at', sa.DateTime,
                  server_default=sa.func.now(), nullable=False),
        sa.Column('updated_at', sa.DateTime, nullable=True),
    )

    op.create_table(
        'permissions',
        sa.Column('id', UUID(as_uuid=True), primary_key=True,
                  default=uuid.uuid4, nullable=False),
        sa.Column('name', sa.String, unique=True, nullable=False),
        sa.Column('description', sa.String, nullable=True),
        sa.Column('created_at', sa.DateTime,
                  server_default=sa.func.now(), nullable=False),
        sa.Column('updated_at', sa.DateTime, nullable=True),
    )

    op.create_table(
        'user_roles',
        sa.Column('user_id', UUID(as_uuid=True),
                  sa.ForeignKey('users.id'), primary_key=True),
        sa.Column('role_id', UUID(as_uuid=True),
                  sa.ForeignKey('roles.id'), primary_key=True),
        sa.Column('created_at', sa.DateTime,
                  server_default=sa.func.now(), nullable=False),
        sa.Column('updated_at', sa.DateTime, nullable=True),
    )

    op.create_table(
        'role_permissions',
        sa.Column('role_id', UUID(as_uuid=True),
                  sa.ForeignKey('roles.id'), primary_key=True),
        sa.Column('permission_id', UUID(as_uuid=True),
                  sa.ForeignKey('permissions.id'), primary_key=True),
        sa.Column('created_at', sa.DateTime,
                  server_default=sa.func.now(), nullable=False),
        sa.Column('updated_at', sa.DateTime, nullable=True),
    )


def downgrade() -> None:
    op.drop_table('role_permissions')
    op.drop_table('user_roles')
    op.drop_table('permissions')
    op.drop_table('roles')
