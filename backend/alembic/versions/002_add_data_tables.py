"""Add data tables (uploaded_files, production_data, financial_data)

Revision ID: 002
Revises: 001
Create Date: 2024-01-10 10:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '002'
down_revision = '001'
branch_labels = None
depends_on = None


def upgrade():
    # Create uploaded_files table
    op.create_table(
        'uploaded_files',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('project_id', sa.Integer(), nullable=False),
        sa.Column('filename', sa.String(), nullable=False),
        sa.Column('file_path', sa.String(), nullable=False),
        sa.Column('file_type', sa.String(), nullable=False),
        sa.Column('file_size', sa.Integer(), nullable=False),
        sa.Column('status', sa.String(), nullable=False, server_default='pending'),
        sa.Column('error_message', sa.Text(), nullable=True),
        sa.Column('quality_score', sa.Float(), nullable=True),
        sa.Column('uploaded_by', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('now()')),
        sa.Column('processed_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['project_id'], ['projects.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['uploaded_by'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_uploaded_files_id'), 'uploaded_files', ['id'], unique=False)

    # Create production_data table
    op.create_table(
        'production_data',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('project_id', sa.Integer(), nullable=False),
        sa.Column('file_id', sa.Integer(), nullable=True),
        sa.Column('date', sa.Date(), nullable=False),
        sa.Column('well_name', sa.String(), nullable=True),
        sa.Column('oil_volume', sa.Float(), nullable=True),
        sa.Column('gas_volume', sa.Float(), nullable=True),
        sa.Column('water_volume', sa.Float(), nullable=True),
        sa.Column('oil_price', sa.Float(), nullable=True),
        sa.Column('gas_price', sa.Float(), nullable=True),
        sa.Column('ngl_price', sa.Float(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('now()')),
        sa.ForeignKeyConstraint(['project_id'], ['projects.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['file_id'], ['uploaded_files.id'], ondelete='SET NULL'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_production_data_id'), 'production_data', ['id'], unique=False)
    op.create_index(op.f('ix_production_data_date'), 'production_data', ['date'], unique=False)

    # Create financial_data table
    op.create_table(
        'financial_data',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('project_id', sa.Integer(), nullable=False),
        sa.Column('file_id', sa.Integer(), nullable=True),
        sa.Column('date', sa.Date(), nullable=False),
        sa.Column('revenue', sa.Float(), nullable=True),
        sa.Column('operating_cost', sa.Float(), nullable=True),
        sa.Column('capex', sa.Float(), nullable=True),
        sa.Column('opex', sa.Float(), nullable=True),
        sa.Column('taxes', sa.Float(), nullable=True),
        sa.Column('royalties', sa.Float(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('now()')),
        sa.ForeignKeyConstraint(['project_id'], ['projects.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['file_id'], ['uploaded_files.id'], ondelete='SET NULL'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_financial_data_id'), 'financial_data', ['id'], unique=False)
    op.create_index(op.f('ix_financial_data_date'), 'financial_data', ['date'], unique=False)


def downgrade():
    op.drop_index(op.f('ix_financial_data_date'), table_name='financial_data')
    op.drop_index(op.f('ix_financial_data_id'), table_name='financial_data')
    op.drop_table('financial_data')
    op.drop_index(op.f('ix_production_data_date'), table_name='production_data')
    op.drop_index(op.f('ix_production_data_id'), table_name='production_data')
    op.drop_table('production_data')
    op.drop_index(op.f('ix_uploaded_files_id'), table_name='uploaded_files')
    op.drop_table('uploaded_files')
