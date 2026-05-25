"""
API endpoints for financial modeling and valuation.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.api.deps import get_db, get_current_user
from app.models.user import User
from app.models.project import Project
from app.models.assumptions import Assumptions
from app.models.synergy_model import SynergyModel
from app.models.scenario import Scenario
from app.schemas.assumptions import (
    AssumptionsCreate,
    AssumptionsUpdate,
    AssumptionsResponse,
    AssumptionsWithSynergies,
    SynergyModelCreate,
    SynergyModelResponse
)
from app.schemas.scenario import (
    ScenarioCreate,
    ScenarioUpdate,
    ScenarioResponse,
    RunValuationRequest,
    ValuationSummary,
    ValuationResults,
    ComparisonResults
)
from app.engines.valuation_service import ValuationService

router = APIRouter()


# ==================== ASSUMPTIONS ENDPOINTS ====================

@router.post("/assumptions", response_model=AssumptionsResponse, status_code=status.HTTP_201_CREATED)
def create_assumptions(
    assumptions_data: AssumptionsCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Create new modeling assumptions for a project.
    
    This endpoint creates a new set of assumptions that define:
    - Production decline curves
    - Commodity price forecasts
    - Cost assumptions (OPEX, CAPEX)
    - Deal structure
    - Valuation parameters
    """
    # Verify project exists and user has access
    project = db.query(Project).filter(
        Project.id == assumptions_data.project_id,
        Project.owner_id == current_user.id
    ).first()
    
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    
    # Convert Pydantic models to dicts for JSON storage
    oil_price_forecast = [p.dict() for p in assumptions_data.oil_price_forecast]
    gas_price_forecast = [p.dict() for p in assumptions_data.gas_price_forecast]
    capex_schedule = [c.dict() for c in assumptions_data.capex_schedule]
    
    # Create assumptions
    assumptions = Assumptions(
        project_id=assumptions_data.project_id,
        version=assumptions_data.version,
        name=assumptions_data.name,
        decline_curve_type=assumptions_data.decline_curve_type,
        decline_rate=assumptions_data.decline_rate,
        hyperbolic_b=assumptions_data.hyperbolic_b,
        oil_price_forecast=oil_price_forecast,
        gas_price_forecast=gas_price_forecast,
        opex_inflation_rate=assumptions_data.opex_inflation_rate,
        capex_schedule=capex_schedule,
        transportation_cost_per_unit=assumptions_data.transportation_cost_per_unit,
        ga_annual=assumptions_data.ga_annual,
        purchase_price=assumptions_data.purchase_price,
        debt_amount=assumptions_data.debt_amount,
        equity_amount=assumptions_data.equity_amount,
        discount_rate=assumptions_data.discount_rate,
        tax_rate=assumptions_data.tax_rate,
        exit_multiple=assumptions_data.exit_multiple,
        forecast_years=assumptions_data.forecast_years
    )
    
    db.add(assumptions)
    db.commit()
    db.refresh(assumptions)
    
    return assumptions


@router.get("/assumptions/{assumptions_id}", response_model=AssumptionsWithSynergies)
def get_assumptions(
    assumptions_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get assumptions by ID with synergy models."""
    assumptions = db.query(Assumptions).filter(Assumptions.id == assumptions_id).first()
    
    if not assumptions:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Assumptions not found"
        )
    
    # Verify user has access to the project
    project = db.query(Project).filter(
        Project.id == assumptions.project_id,
        Project.owner_id == current_user.id
    ).first()
    
    if not project:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        )
    
    return assumptions


@router.get("/projects/{project_id}/assumptions", response_model=List[AssumptionsResponse])
def list_project_assumptions(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """List all assumptions for a project."""
    # Verify project exists and user has access
    project = db.query(Project).filter(
        Project.id == project_id,
        Project.owner_id == current_user.id
    ).first()
    
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    
    assumptions = db.query(Assumptions).filter(
        Assumptions.project_id == project_id
    ).order_by(Assumptions.version.desc()).all()
    
    return assumptions


@router.put("/assumptions/{assumptions_id}", response_model=AssumptionsResponse)
def update_assumptions(
    assumptions_id: int,
    assumptions_data: AssumptionsUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update existing assumptions."""
    assumptions = db.query(Assumptions).filter(Assumptions.id == assumptions_id).first()
    
    if not assumptions:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Assumptions not found"
        )
    
    # Verify user has access
    project = db.query(Project).filter(
        Project.id == assumptions.project_id,
        Project.owner_id == current_user.id
    ).first()
    
    if not project:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        )
    
    # Update fields
    update_data = assumptions_data.dict(exclude_unset=True)
    
    # Convert Pydantic models to dicts for JSON fields
    if 'oil_price_forecast' in update_data and update_data['oil_price_forecast']:
        update_data['oil_price_forecast'] = [p.dict() for p in update_data['oil_price_forecast']]
    if 'gas_price_forecast' in update_data and update_data['gas_price_forecast']:
        update_data['gas_price_forecast'] = [p.dict() for p in update_data['gas_price_forecast']]
    if 'capex_schedule' in update_data and update_data['capex_schedule']:
        update_data['capex_schedule'] = [c.dict() for c in update_data['capex_schedule']]
    
    for field, value in update_data.items():
        setattr(assumptions, field, value)
    
    db.commit()
    db.refresh(assumptions)
    
    return assumptions


@router.delete("/assumptions/{assumptions_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_assumptions(
    assumptions_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Delete assumptions."""
    assumptions = db.query(Assumptions).filter(Assumptions.id == assumptions_id).first()
    
    if not assumptions:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Assumptions not found"
        )
    
    # Verify user has access
    project = db.query(Project).filter(
        Project.id == assumptions.project_id,
        Project.owner_id == current_user.id
    ).first()
    
    if not project:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        )
    
    db.delete(assumptions)
    db.commit()
    
    return None


# ==================== SYNERGY MODEL ENDPOINTS ====================

@router.post("/assumptions/{assumptions_id}/synergies", response_model=SynergyModelResponse, status_code=status.HTTP_201_CREATED)
def create_synergy_model(
    assumptions_id: int,
    synergy_data: SynergyModelCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Create a synergy model for assumptions.
    
    Synergy models define:
    - Category (operational, procurement, workforce, infrastructure)
    - Target annual value
    - Realization schedule (how synergies ramp up over time)
    """
    # Verify assumptions exist and user has access
    assumptions = db.query(Assumptions).filter(Assumptions.id == assumptions_id).first()
    
    if not assumptions:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Assumptions not found"
        )
    
    project = db.query(Project).filter(
        Project.id == assumptions.project_id,
        Project.owner_id == current_user.id
    ).first()
    
    if not project:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        )
    
    # Convert realization schedule to dict
    realization_schedule = [r.dict() for r in synergy_data.realization_schedule]
    
    # Create synergy model
    synergy_model = SynergyModel(
        assumptions_id=assumptions_id,
        category=synergy_data.category,
        description=synergy_data.description,
        target_value=synergy_data.target_value,
        realization_schedule=realization_schedule
    )
    
    db.add(synergy_model)
    db.commit()
    db.refresh(synergy_model)
    
    return synergy_model


@router.get("/assumptions/{assumptions_id}/synergies", response_model=List[SynergyModelResponse])
def list_synergy_models(
    assumptions_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """List all synergy models for assumptions."""
    # Verify assumptions exist and user has access
    assumptions = db.query(Assumptions).filter(Assumptions.id == assumptions_id).first()
    
    if not assumptions:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Assumptions not found"
        )
    
    project = db.query(Project).filter(
        Project.id == assumptions.project_id,
        Project.owner_id == current_user.id
    ).first()
    
    if not project:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        )
    
    synergy_models = db.query(SynergyModel).filter(
        SynergyModel.assumptions_id == assumptions_id
    ).all()
    
    return synergy_models


@router.delete("/synergies/{synergy_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_synergy_model(
    synergy_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Delete a synergy model."""
    synergy_model = db.query(SynergyModel).filter(SynergyModel.id == synergy_id).first()
    
    if not synergy_model:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Synergy model not found"
        )
    
    # Verify user has access
    assumptions = db.query(Assumptions).filter(Assumptions.id == synergy_model.assumptions_id).first()
    project = db.query(Project).filter(
        Project.id == assumptions.project_id,
        Project.owner_id == current_user.id
    ).first()
    
    if not project:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        )
    
    db.delete(synergy_model)
    db.commit()
    
    return None


# ==================== SCENARIO ENDPOINTS ====================

@router.post("/scenarios", response_model=ScenarioResponse, status_code=status.HTTP_201_CREATED)
def create_scenario(
    scenario_data: ScenarioCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Create a valuation scenario.
    
    Scenarios link assumptions to a project and define the scenario type
    (Bull/Base/Bear/Custom).
    """
    # Verify project exists and user has access
    project = db.query(Project).filter(
        Project.id == scenario_data.project_id,
        Project.owner_id == current_user.id
    ).first()
    
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    
    # Verify assumptions exist
    assumptions = db.query(Assumptions).filter(
        Assumptions.id == scenario_data.assumptions_id
    ).first()
    
    if not assumptions:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Assumptions not found"
        )
    
    # Check for duplicate scenario name
    existing = db.query(Scenario).filter(
        Scenario.project_id == scenario_data.project_id,
        Scenario.name == scenario_data.name
    ).first()
    
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Scenario with this name already exists for this project"
        )
    
    # Create scenario
    scenario = Scenario(
        project_id=scenario_data.project_id,
        assumptions_id=scenario_data.assumptions_id,
        name=scenario_data.name,
        scenario_type=scenario_data.scenario_type,
        description=scenario_data.description
    )
    
    db.add(scenario)
    db.commit()
    db.refresh(scenario)
    
    return scenario


@router.get("/scenarios/{scenario_id}", response_model=ScenarioResponse)
def get_scenario(
    scenario_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get scenario by ID."""
    scenario = db.query(Scenario).filter(Scenario.id == scenario_id).first()
    
    if not scenario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Scenario not found"
        )
    
    # Verify user has access
    project = db.query(Project).filter(
        Project.id == scenario.project_id,
        Project.owner_id == current_user.id
    ).first()
    
    if not project:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        )
    
    return scenario


@router.get("/projects/{project_id}/scenarios", response_model=List[ScenarioResponse])
def list_project_scenarios(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """List all scenarios for a project."""
    # Verify project exists and user has access
    project = db.query(Project).filter(
        Project.id == project_id,
        Project.owner_id == current_user.id
    ).first()
    
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    
    scenarios = db.query(Scenario).filter(
        Scenario.project_id == project_id
    ).order_by(Scenario.created_at.desc()).all()
    
    return scenarios


@router.put("/scenarios/{scenario_id}", response_model=ScenarioResponse)
def update_scenario(
    scenario_id: int,
    scenario_data: ScenarioUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update a scenario."""
    scenario = db.query(Scenario).filter(Scenario.id == scenario_id).first()
    
    if not scenario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Scenario not found"
        )
    
    # Verify user has access
    project = db.query(Project).filter(
        Project.id == scenario.project_id,
        Project.owner_id == current_user.id
    ).first()
    
    if not project:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        )
    
    # Update fields
    update_data = scenario_data.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(scenario, field, value)
    
    db.commit()
    db.refresh(scenario)
    
    return scenario


@router.delete("/scenarios/{scenario_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_scenario(
    scenario_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Delete a scenario."""
    scenario = db.query(Scenario).filter(Scenario.id == scenario_id).first()
    
    if not scenario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Scenario not found"
        )
    
    # Verify user has access
    project = db.query(Project).filter(
        Project.id == scenario.project_id,
        Project.owner_id == current_user.id
    ).first()
    
    if not project:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        )
    
    db.delete(scenario)
    db.commit()
    
    return None


# ==================== VALUATION ENDPOINTS ====================

@router.post("/valuation/run", response_model=ValuationSummary)
def run_valuation(
    request: RunValuationRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Run valuation for a scenario.
    
    This endpoint:
    1. Loads historical data
    2. Applies assumptions
    3. Generates forecasts
    4. Calculates cash flows
    5. Computes valuation metrics (NPV, IRR, etc.)
    6. Stores results in database
    """
    # Verify scenario exists and user has access
    scenario = db.query(Scenario).filter(Scenario.id == request.scenario_id).first()
    
    if not scenario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Scenario not found"
        )
    
    project = db.query(Project).filter(
        Project.id == scenario.project_id,
        Project.owner_id == current_user.id
    ).first()
    
    if not project:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        )
    
    # Run valuation
    try:
        valuation_service = ValuationService(db)
        results = valuation_service.run_valuation(
            scenario_id=str(request.scenario_id),
            periods_per_year=request.periods_per_year
        )
        return results
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Valuation failed: {str(e)}"
        )


@router.get("/valuation/results/{scenario_id}", response_model=ValuationResults)
def get_valuation_results(
    scenario_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get stored valuation results for a scenario.
    
    Returns complete annual data and metrics.
    """
    # Verify scenario exists and user has access
    scenario = db.query(Scenario).filter(Scenario.id == scenario_id).first()
    
    if not scenario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Scenario not found"
        )
    
    project = db.query(Project).filter(
        Project.id == scenario.project_id,
        Project.owner_id == current_user.id
    ).first()
    
    if not project:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        )
    
    # Get results
    try:
        valuation_service = ValuationService(db)
        results = valuation_service.get_valuation_results(str(scenario_id))
        return results
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )


@router.post("/valuation/compare", response_model=ComparisonResults)
def compare_scenarios(
    scenario_ids: List[int],
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Compare multiple scenarios side-by-side.
    
    Returns key metrics for each scenario for easy comparison.
    """
    # Verify all scenarios exist and user has access
    for scenario_id in scenario_ids:
        scenario = db.query(Scenario).filter(Scenario.id == scenario_id).first()
        
        if not scenario:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Scenario {scenario_id} not found"
            )
        
        project = db.query(Project).filter(
            Project.id == scenario.project_id,
            Project.owner_id == current_user.id
        ).first()
        
        if not project:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied"
            )
    
    # Compare scenarios
    try:
        valuation_service = ValuationService(db)
        results = valuation_service.compare_scenarios([str(sid) for sid in scenario_ids])
        return results
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Comparison failed: {str(e)}"
        )
