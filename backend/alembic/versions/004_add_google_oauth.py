"""Add Google OAuth fields to users table

Revision ID: 004
Revises: 003
Create Date: 2024-01-20 10:00:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '004'
down_revision = '003'
branch_labels = None
depends_on = None


def upgrade():
    # Make hashed_password nullable for OAuth users
    op.alter_column('users', 'hashed_password',
                    existing_type=sa.String(255),
                    nullable=True)
    
    # Add OAuth fields
    op.add_column('users', sa.Column('google_id', sa.String(255), nullable=True))
    op.add_column('users', sa.Column('oauth_provider', sa.String(50), nullable=True))
    op.add_column('users', sa.Column('profile_picture', sa.String(500), nullable=True))
    
    # Create indexes
    op.create_index('ix_users_google_id', 'users', ['google_id'], unique=True)


def downgrade():
    op.drop_index('ix_users_google_id', table_name='users')
    op.drop_column('users', 'profile_picture')
    op.drop_column('users', 'oauth_provider')
    op.drop_column('users', 'google_id')
    
    op.alter_column('users', 'hashed_password',
                    existing_type=sa.String(255),
                    nullable=False)
