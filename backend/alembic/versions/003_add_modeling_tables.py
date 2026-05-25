"""Add modeling tables (assumptions, synergy_models, scenarios, valuation_outputs)

Revision ID: 003
Revises: 002
Create Date: 2024-01-15 10:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '003'
down_revision = '002'
branch_labels = None
depends_on = None


def upgrade():
    # Create assumptions table
    op.create_table(
        'assumptions',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('project_id', sa.Integer(), sa.ForeignKey('projects.id', ondelete='CASCADE'), nullable=False),
        sa.Column('version', sa.Integer(), nullable=False, default=1),
        sa.Column('name', sa.String(255), nullable=False),
        
        # Production assumptions
        sa.Column('decline_curve_type', sa.String(50), nullable=False),
        sa.Column('decline_rate', sa.DECIMAL(5, 4)),
        sa.Column('hyperbolic_b', sa.DECIMAL(3, 2)),
        sa.Column('oil_price_forecast', postgresql.JSON),
        sa.Column('gas_price_forecast', postgresql.JSON),
        
        # Cost assumptions
        sa.Column('opex_inflation_rate', sa.DECIMAL(5, 4)),
        sa.Column('capex_schedule', postgresql.JSON),
        sa.Column('transportation_cost_per_unit', sa.DECIMAL(10, 2)),
        sa.Column('ga_annual', sa.DECIMAL(15, 2)),
        
        # Deal assumptions
        sa.Column('purchase_price', sa.DECIMAL(15, 2)),
        sa.Column('debt_amount', sa.DECIMAL(15, 2)),
        sa.Column('equity_amount', sa.DECIMAL(15, 2)),
        sa.Column('discount_rate', sa.DECIMAL(5, 4)),
        sa.Column('tax_rate', sa.DECIMAL(5, 4)),
        sa.Column('exit_multiple', sa.DECIMAL(4, 2)),
        sa.Column('forecast_years', sa.Integer(), default=20),
        
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )
    
    op.create_index('idx_assumptions_project_id', 'assumptions', ['project_id'])
    op.create_index('idx_assumptions_version', 'assumptions', ['project_id', 'version'])
    
    # Create synergy_models table
    op.create_table(
        'synergy_models',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('assumptions_id', sa.Integer(), sa.ForeignKey('assumptions.id', ondelete='CASCADE'), nullable=False),
        sa.Column('category', sa.String(100), nullable=False),
        sa.Column('description', sa.Text()),
        sa.Column('target_value', sa.DECIMAL(15, 2), nullable=False),
        sa.Column('realization_schedule', postgresql.JSON, nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )
    
    op.create_index('idx_synergy_models_assumptions_id', 'synergy_models', ['assumptions_id'])
    
    # Create scenarios table
    op.create_table(
        'scenarios',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('project_id', sa.Integer(), sa.ForeignKey('projects.id', ondelete='CASCADE'), nullable=False),
        sa.Column('assumptions_id', sa.Integer(), sa.ForeignKey('assumptions.id', ondelete='CASCADE'), nullable=False),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('scenario_type', sa.String(50), nullable=False),
        sa.Column('description', sa.Text()),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )
    
    op.create_index('idx_scenarios_project_id', 'scenarios', ['project_id'])
    op.create_index('idx_scenarios_type', 'scenarios', ['scenario_type'])
    op.create_unique_constraint('uq_scenario_project_name', 'scenarios', ['project_id', 'name'])
    
    # Create valuation_outputs table
    op.create_table(
        'valuation_outputs',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('scenario_id', sa.Integer(), sa.ForeignKey('scenarios.id', ondelete='CASCADE'), nullable=False),
        sa.Column('year', sa.Integer(), nullable=False),
        
        # Production forecasts
        sa.Column('oil_production', sa.DECIMAL(15, 2)),
        sa.Column('gas_production', sa.DECIMAL(15, 2)),
        
        # Financial forecasts
        sa.Column('revenue', sa.DECIMAL(15, 2)),
        sa.Column('opex', sa.DECIMAL(15, 2)),
        sa.Column('capex', sa.DECIMAL(15, 2)),
        sa.Column('ebitda', sa.DECIMAL(15, 2)),
        sa.Column('ebitdax', sa.DECIMAL(15, 2)),
        sa.Column('depreciation', sa.DECIMAL(15, 2)),
        sa.Column('interest_expense', sa.DECIMAL(15, 2)),
        sa.Column('taxes', sa.DECIMAL(15, 2)),
        sa.Column('free_cash_flow', sa.DECIMAL(15, 2)),
        
        # Synergies
        sa.Column('synergy_value', sa.DECIMAL(15, 2)),
        
        # Debt
        sa.Column('debt_balance', sa.DECIMAL(15, 2)),
        sa.Column('debt_service', sa.DECIMAL(15, 2)),
        
        # Valuation metrics
        sa.Column('npv', sa.DECIMAL(15, 2)),
        sa.Column('irr', sa.DECIMAL(7, 4)),
        sa.Column('payback_period', sa.DECIMAL(5, 2)),
        sa.Column('roic', sa.DECIMAL(7, 4)),
        sa.Column('terminal_value', sa.DECIMAL(15, 2)),
        
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )
    
    op.create_index('idx_valuation_outputs_scenario_id', 'valuation_outputs', ['scenario_id'])
    op.create_index('idx_valuation_outputs_year', 'valuation_outputs', ['scenario_id', 'year'])
    op.create_unique_constraint('uq_valuation_scenario_year', 'valuation_outputs', ['scenario_id', 'year'])


def downgrade():
    op.drop_table('valuation_outputs')
    op.drop_table('scenarios')
    op.drop_table('synergy_models')
    op.drop_table('assumptions')
